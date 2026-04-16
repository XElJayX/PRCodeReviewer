from fastapi import APIRouter, Request, HTTPException
import hmac
import hashlib
from app.config import get_settings
from app.worker import run_review_task

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
        run_review_task.delay(owner, repo_name, pr_number)
        return {"status": "queued"}
    return {"status": "ignored"}

