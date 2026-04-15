from app.agent.graph import build_graph

def test_graph_construction():
    agent = build_graph()

    result = agent.invoke({
    "owner": "XElJayX",
    "repo_name": "TexttoSQL",
    "pr_number": 1,
    "pr_details": None,
    "review": None,
    "comment_posted": False
    })

    print (result["review"])
    print('---'*20)
    print (result["comment_posted"])


if __name__ == "__main__":
    test_graph_construction()