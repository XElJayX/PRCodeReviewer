from celery import Celery
from app.config import get_settings
from app.agent.graph import build_graph



celery_app = Celery(
    "autoreviewer",
    broker=get_settings().redis_url,
    backend=get_settings().redis_url
)

@celery_app.task
def run_review_task(owner:str, repo_name:str, pr_number:int):
    agent = build_graph()
    result = agent.invoke({
        "owner": owner,
        "repo_name": repo_name,
        "pr_number": pr_number,
        "pr_details": None,
        "review": None,
        "comment_posted": False
    })
    return result["comment_posted"]