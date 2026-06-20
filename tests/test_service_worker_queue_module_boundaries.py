import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_service_worker_queue_facade_reexports_queue_and_dequeue_modules() -> None:
    from agent_company_core import service_worker_dequeue
    from agent_company_core import service_worker_queue
    from agent_company_core import service_worker_request_queue

    assert service_worker_queue.write_service_worker_queue is service_worker_request_queue.write_service_worker_queue
    assert service_worker_queue.service_worker_dequeue_route is service_worker_dequeue.service_worker_dequeue_route
    assert service_worker_queue.service_worker_dequeue_result_paths is service_worker_dequeue.service_worker_dequeue_result_paths
    assert service_worker_queue.write_service_worker_dequeue_plan is service_worker_dequeue.write_service_worker_dequeue_plan


def test_service_worker_dequeue_route_remains_read_only_for_approval_like_status() -> None:
    from agent_company_core.service_worker_dequeue import service_worker_dequeue_route

    decision = service_worker_dequeue_route({"status": "approved", "worker_type": "local_runtime_adapter"})

    assert decision["route"] == "ready_for_manual_local_runtime_review_no_worker_start"
    assert decision["dequeue_allowed"] is False
    assert decision["worker_started"] is False
    assert decision["service_request_updated"] is False
    assert decision["approval_granted"] is False
