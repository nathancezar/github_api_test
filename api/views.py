from rest_framework import viewsets, status
from rest_framework.response import Response

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

    def retrieve(self, request, login=None):
        # GET sem o login deve retornar todas as organizações
        # ordenadas pelo score
        if request.method == 'GET' and not login:
            return Response(self.serializer_class(self.queryset).data, \
                status=status.HTTP_200_OK)

        # GET com o login deve retornar as informações da organização,
        # caso exista, e salvar no banco de dados.
        # Caso já exista no banco, atualiza os dados.
        elif request.method == 'GET' and login:
            try:
                new_org = self.create_or_update_organization(login)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

            return Response(self.serializer_class(new_org).data, \
                status=status.HTTP_200_OK)

        # DELETE com login deve remover a organização do banco de dados
        elif request.method == 'DELETE' and login:
            try:
                self.serializer_class(self.queryset.get(login=login)).delete()
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

            return Response(status=status.HTTP_200_OK)

        # DELETE sem login deve gerar erro
        elif request.method == 'DELETE' and not login:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create_or_update_organization(self, login: str):
        """Retorna um QuerySet da nova organização cadastrada

        :login: login da organização no Github
        """
        public_members = GithubApi().get_organization_public_members(login)
        organization = GithubApi().get_organization(login)
        priority = public_members + organization['repositories']
        new_org, _ = models.Organization.objects.update_or_create(
            login=login, name=organization['name'], score=priority)

        return new_org
