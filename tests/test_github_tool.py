import app.tools.github_tool as github_tool

tool = github_tool.GitHubTool()

response = tool.fetch_pr("XElJayX", "TexttoSQL",1)

print(response)