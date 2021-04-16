from rest_framework import viewsets, status
from rest_framework.response import Response
import requests

from api import models, serializers
from api.integrations.github import GithubApi

# TODOS:
# 1 - Buscar organização pelo login através da API do Github
# 2 - Armazenar os dados atualizados da organização no banco
# 3 - Retornar corretamente os dados da organização
# 4 - Retornar os dados de organizações ordenados pelo score na listagem da API


class OrganizationViewSet(viewsets.ModelViewSet):

    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
    lookup_field = "login"
    base_url = "https://api.github.com/orgs/"

    def retrieve(self, request, login=None):
        if request.method == 'GET' and not login:
            return Response(self.serializer_class(self.queryset).data, \
                status=status.HTTP_200_OK)

        elif request.method == 'GET' and login:
            try:
                public_members_value = self.getPublicMembers(login)
                public_repos_value, name = self.getPublicRepositories(login)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

            priority = public_members_value + public_repos_value
            new_org, _ = models.Organization.objects.update_or_create(
                    login=login, name=name, score=priority)

            return Response(self.serializer_class(new_org).data, \
                status=status.HTTP_200_OK)

        elif request.method == 'DELETE':
            try:
                self.serializer_class(self.queryset.get(login=login)).delete()

            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

            return Response(status=status.HTTP_200_OK)

    def getPublicMembers(self, login):
        public_members_response = requests.get(
            f"{self.base_url}{login}/public_members")
        public_members_response.raise_for_status()

        return len(public_members_response.json())

    def getPublicRepositories(self, login):
        public_repos_response = requests.get(
            f"{self.base_url}{login}")
        public_repos_response.raise_for_status()

        return public_repos_response.json()["public_repos"], \
                public_repos_response.json()["name"]
