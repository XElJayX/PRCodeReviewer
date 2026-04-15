from app.agent.state import ReviewState
from app.tools.github_tool import GitHubTool
from langchain_groq import ChatGroq
from app.config import get_settings
from langgraph.graph import StateGraph, END

def fetch_pr_node(state: ReviewState) -> dict:
    tool = GitHubTool()
    owner = state["owner"]
    repo_name = state["repo_name"]
    pr_number = state["pr_number"]

    result = tool.fetch_pr(owner, repo_name, pr_number)
    return {"pr_details": result}

def analyze_code_node(state: ReviewState) -> dict:
    pr_details=state.get("pr_details")

    pr_title = pr_details.get("title", "")
    pr_description = pr_details.get("description", "")
    files_changed = pr_details.get("files", [])

    groq_api_key = get_settings().groq_api_key

    llm = ChatGroq(api_key=groq_api_key,
                    model="llama-3.3-70b-versatile")
    prompt = f"""You are an expert code reviewer with strong experience in software engineering best practices, security, performance optimization, and clean code principles.

                ## Pull Request Context
                Title:
                {pr_title}

                Description:
                {pr_description}

                Files Changed:
                {files_changed}

                ## Instructions
                Review the code changes carefully and provide a detailed review with the following:

                1. **Summary**
                - Brief overview of what the PR does

                2. **Major Issues**
                - Bugs, logical errors, security vulnerabilities, or breaking changes
                - Be specific and reference relevant parts of the code

                3. **Code Quality & Best Practices**
                - Naming, structure, readability, maintainability
                - Any violations of common coding standards

                4. **Performance Considerations**
                - Inefficient algorithms or unnecessary computations
                - Suggestions for optimization

                5. **Security Concerns**
                - Potential vulnerabilities (e.g., injection risks, improper validation)

                6. **Suggestions for Improvement**
                - Concrete recommendations with examples where possible

                7. **Overall Verdict**
                - Approve / Request Changes / Comment Only
                - Short justification

                ## Output Format
                - Use clear headings for each section
                - Use bullet points where appropriate
                - Reference code snippets or file names when relevant
                - Be concise but thorough in your analysis, and ensure your feedback is actionable for the developer."""
    
    response = llm.invoke(prompt)

    return {"review": response.content}


def post_comment_node(state: ReviewState) -> dict:
    owner = state.get("owner")
    repo_name = state.get("repo_name")
    pr_number = state.get("pr_number")
    review = state.get("review")
    
    tool = GitHubTool()

    post = tool.post_comment(owner,repo_name,pr_number,review)
    return {"comment_posted": post}

 
 def build_graph():
    graph= StateGraph(ReviewState)

    graph.add_node("fetch_pr",fetch_pr_node)
    graph.add_node("analyze_code",analyze_code_node)
    graph.add_node("post_comment",post_comment_node)

    graph.set_entry_point("fetch_pr")

    graph.add_edge("fetch_pr","analyze_code")
    graph.add_edge("analyze_code","post_comment")
    graph.add_edge("post_comment",END)
    
    return graph.compile()