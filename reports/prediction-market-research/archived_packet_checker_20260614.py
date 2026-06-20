#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any

PACKET_RE = re.compile(
    r"^- review=(?P<review>\w+)(?P<meta>.*?)\n"
    r"\s+(?P<market>[^\n]+)\n"
    r"\s+close=(?P<close>[^\s]+).*?result=(?P<result>[^\s]*)\s+expirationValue=(?P<expiration>[^\n]*)\n"
    r"\s+yes=(?P<yes>[^\s]+)\s+no=(?P<no>[^\s]+)\n"
    r"\s+source:\s+(?P<source>\S+)",
    re.M | re.S,
)
HEADER_RE = re.compile(r"^(?P<key>[A-Za-z ]+):\s*(?P<value>.+)$", re.M)
EVENT_RE = re.compile(r"^- status=(?P<status>[^\s]+) series=(?P<series>[^\s]+) event=(?P<event>[^\s]+)", re.M)


def scalar(meta: str, key: str) -> str:
    match = re.search(rf"(?:^|\s){re.escape(key)}=([^\s]*)", meta)
    return match.group(1).strip() if match else ""


def number(value: str) -> float | None:
    try:
        if value == "":
            return None
        return float(value)
    except ValueError:
        return None


def quote_pair(pair: str) -> tuple[float | None, float | None]:
    left, _, right = pair.partition("/")
    return number(left), number(right)


def parse_headers(text: str) -> dict[str, str]:
    return {m.group("key").strip(): m.group("value").strip() for m in HEADER_RE.finditer(text)}


def parse_packets(path: Path) -> tuple[dict[str, str], list[dict[str, Any]], dict[str, int]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    headers = parse_headers(text)
    event_counts: dict[str, int] = {}
    for event in EVENT_RE.finditer(text):
        status = event.group("status")
        event_counts[status] = event_counts.get(status, 0) + 1

    packets: list[dict[str, Any]] = []
    for match in PACKET_RE.finditer(text):
        row = match.groupdict()
        meta = row["meta"]
        flags = scalar(meta, "flags")
        yes_bid, yes_ask = quote_pair(row["yes"])
        no_bid, no_ask = quote_pair(row["no"])
        packets.append(
            {
                "input": str(path),
                "review": row["review"].lower() == "true",
                "status": scalar(meta, "status"),
                "flags": [f for f in flags.split(",") if f],
                "market": row["market"].strip(),
                "close": row["close"],
                "result": row["result"],
                "expirationValue": row["expiration"].strip(),
                "winner": scalar(meta, "winner") or row["result"],
                "winningAsk": number(scalar(meta, "winningAsk")),
                "losingBid": number(scalar(meta, "losingBid")),
                "directEdge": number(scalar(meta, "directEdge")),
                "yesBid": yes_bid,
                "yesAsk": yes_ask,
                "noBid": no_bid,
                "noAsk": no_ask,
                "source": row["source"],
            }
        )
    return headers, packets, event_counts


def evaluate(packet: dict[str, Any], stale_winning_ask_max: float, stale_losing_bid_min: float) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    flags = set(packet["flags"])
    if not packet["review"]:
        reasons.append("review_false")
    if "pre_close" in flags or "official_value_not_seen" in flags:
        reasons.append("pre_close_or_official_value_missing")
    if not (packet["result"] or packet["expirationValue"]):
        reasons.append("missing_result_or_expiration_value")
    if "not_active" in flags or packet["status"] == "finalized":
        reasons.append("not_active_or_finalized")

    has_stale_winning_ask = packet["winningAsk"] is not None and packet["winningAsk"] < stale_winning_ask_max
    has_stale_losing_bid = packet["losingBid"] is not None and packet["losingBid"] > stale_losing_bid_min
    if not (has_stale_winning_ask or has_stale_losing_bid):
        reasons.append("no_nonterminal_stale_quote")

    reasons.extend(["fees_unverified", "depth_unverified", "venue_eligibility_unverified", "real_money_gate_absent"])
    return len(reasons) == 0, reasons


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline archived Kalshi packet parser/checker")
    parser.add_argument("paths", nargs="+", help="Local archived Markdown packet files")
    parser.add_argument("--stale-winning-ask-max", type=float, default=0.98)
    parser.add_argument("--stale-losing-bid-min", type=float, default=0.02)
    args = parser.parse_args()

    all_packets: list[dict[str, Any]] = []
    files: list[dict[str, Any]] = []
    event_status_counts: dict[str, int] = {}
    for raw in args.paths:
        path = Path(raw)
        headers, packets, events = parse_packets(path)
        all_packets.extend(packets)
        files.append({"path": str(path), "headers": headers, "parsed_packets": len(packets)})
        for key, value in events.items():
            event_status_counts[key] = event_status_counts.get(key, 0) + value

    killed: list[dict[str, Any]] = []
    actionable: list[dict[str, Any]] = []
    reason_counts: dict[str, int] = {}
    for packet in all_packets:
        keep, reasons = evaluate(packet, args.stale_winning_ask_max, args.stale_losing_bid_min)
        for reason in reasons:
            reason_counts[reason] = reason_counts.get(reason, 0) + 1
        row = {
            "input": packet["input"],
            "market": packet["market"],
            "close": packet["close"],
            "result": packet["result"],
            "yesBid": packet["yesBid"],
            "yesAsk": packet["yesAsk"],
            "noBid": packet["noBid"],
            "noAsk": packet["noAsk"],
            "flags": packet["flags"],
            "reasons": reasons,
            "source": packet["source"],
        }
        (actionable if keep else killed).append(row)

    output = {
        "generated_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "mode": "offline_local_archived_packets_only",
        "network_calls": False,
        "accounts_or_credentials": False,
        "orders_or_trades": False,
        "realized_usd": 0,
        "thresholds": {
            "stale_winning_ask_max": args.stale_winning_ask_max,
            "stale_losing_bid_min": args.stale_losing_bid_min,
        },
        "files": files,
        "event_status_counts": event_status_counts,
        "parsed_packets": len(all_packets),
        "actionable_candidates": len(actionable),
        "killed_candidates": len(killed),
        "reason_counts": dict(sorted(reason_counts.items())),
        "actionable": actionable,
        "killed_sample": killed[:20],
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if output["actionable_candidates"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
