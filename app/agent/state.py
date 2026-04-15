from typing import TypedDict, Optional


class ReviewState(TypedDict):
    owner: str
    repo_name: str
    pr_number: int
    pr_details: Optional[dict] 
    review: Optional[str] 
    comment_posted: bool 
