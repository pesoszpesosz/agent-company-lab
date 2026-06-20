"""Compatibility facade for service-worker queue commands."""

from __future__ import annotations

from .service_worker_dequeue import (
    service_worker_dequeue_result_paths,
    service_worker_dequeue_route,
    write_service_worker_dequeue_plan,
)
from .service_worker_request_queue import write_service_worker_queue

__all__ = [
    "service_worker_dequeue_result_paths",
    "service_worker_dequeue_route",
    "write_service_worker_dequeue_plan",
    "write_service_worker_queue",
]
