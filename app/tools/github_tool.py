from app.config import get_settings
import httpx

class GitHubTool:
    def __init__(self):
        self.settings = get_settings()  
        self.base_url = "https://api.github.com"
        self.client = httpx.Client(
            headers={"Authorization": f"Bearer {self.settings.github_token}",
            "Accept": "application/vnd.github.v3+json"}, base_url=self.base_url
            )
    
    def fetch_pr(self,owner,repo_name,pr_number):
        response = self.client.get(f"/repos/{owner}/{repo_name}/pulls/{pr_number}")
        if response.status_code != 200:
            return None   
        data = response.json()

        title = data.get("title")
        description = data.get("body")
        author = data.get("user", {}).get("login")
        
        
        response = self.client.get(f"/repos/{owner}/{repo_name}/pulls/{pr_number}/files")
        if response.status_code != 200:
            return None 
        files = response.json()
        file_list = [{"filename": file.get("filename"), "patch": file.get("patch", "")} for file in files]
        return {
            "title": title,
            "description": description,
            "author": author,
            "files": file_list
        }
    def post_comment(self,owner,repo_name,pr_number,comment):
        response = self.client.post(f'/repos/{owner}/{repo_name}/issues/{pr_number}/comments', json = {"body": comment})
        return response.status_code == 201