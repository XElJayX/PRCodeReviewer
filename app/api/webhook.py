from fastapi import APIRouter, Request
from app.agent.graph import build_graph


router = APIRouter()

@router.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()
    action = payload.get("action")
    if action == "opened":
        owner = payload["repository"]["owner"]["login"]
        repo_name = payload["repository"]["name"]
        pr_number = payload["number"]
        graph = build_graph()
        result = graph.invoke({
            "owner": owner,
            "repo_name": repo_name,
            "pr_number": pr_number,
            "pr_details": None,
            "review": None,
            "comment_posted": False
        })
        return {"status": "ok"} if result["comment_posted"] else {"status": "failed"}
    return {"status": "ignored"}