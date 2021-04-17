import os
import requests


class GithubApi:
    API_URL = os.environ.get("GITHUB_API_URL", "https://api.github.com/orgs/")
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

    def get_organization(self, login: str):
        """Busca uma organização no Github

        :login: login da organização no Github
        """
        headers = {'Authorization': f'token {self.GITHUB_TOKEN}'}
        public_repos_response = requests.get(
            f"{self.API_URL}{login}", headers=headers)
        public_repos_response.raise_for_status()

        if not "name" in public_repos_response.json().keys():
            return {
            'name': "",
            'repositories': public_repos_response.json()["public_repos"]
            }

        return {
            'name': public_repos_response.json()["name"],
            'repositories': public_repos_response.json()["public_repos"]
            }

    def get_organization_public_members(self, login: str) -> int:
        """Retorna todos os membros públicos de uma organização

        :login: login da organização no Github
        """
        headers = {'Authorization': f'token {self.GITHUB_TOKEN}'}
        public_members_response = requests.get(
            f"{self.API_URL}{login}/public_members", headers=headers)
        public_members_response.raise_for_status()

        return len(public_members_response.json())
