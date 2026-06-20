import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_money_paths_manager_proof_facade_reexports_stage_modules() -> None:
    from agent_company_core import money_paths_manager_proof as facade
    from agent_company_core import money_paths_manager_proof_core
    from agent_company_core import money_paths_manager_proof_packets
    from agent_company_core import money_paths_manager_proof_preflight
    from agent_company_core import money_paths_manager_proof_queue

    assert facade.manager_proof_task_template is money_paths_manager_proof_core.manager_proof_task_template
    assert facade.manager_proof_task_queue_score is money_paths_manager_proof_core.manager_proof_task_queue_score
    assert facade.write_manager_proof_task_packets is money_paths_manager_proof_packets.write_manager_proof_task_packets
    assert facade.write_manager_proof_task_promotion_preflight is money_paths_manager_proof_preflight.write_manager_proof_task_promotion_preflight
    assert facade.write_manager_proof_task_promotion_queue is money_paths_manager_proof_queue.write_manager_proof_task_promotion_queue
