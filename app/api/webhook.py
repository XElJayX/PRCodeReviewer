from fastapi import APIRouter, Request, HTTPException
from app.agent.graph import build_graph
import hmac
import hashlib
from app.config import get_settings

router = APIRouter()


def verify_signature(payload_bytes:bytes, signature_header: str)-> bool:
    secret = get_settings().webhook_secret.encode("utf-8")
    expected = hmac.new(secret, payload_bytes, hashlib.sha256).hexdigest()
    expected_header = f"sha256={expected}"
    return hmac.compare_digest(expected_header, signature_header)

    
@router.post("/webhook")
async def handle_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256","")
    if not verify_signature(body, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")
    
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

