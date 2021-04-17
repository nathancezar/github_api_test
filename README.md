# API desenvolvida para Teste Técnico Desenvolvedor(a) Python Júnior

A API pode ser acessada em https://teste-vough-api.herokuapp.com/api/

## ENDPOINTS

```
GET /api/orgs/<login>/
```
:login = login de uma organização cadastrada no GitHub.

Deve retornar os dados da organização:

```
{
    "login": "string",
    "name": "string",
    "score": int
}
```
:score = a soma da quantidade de mombros públicos + a quantidade de
repositórios públicos da organização.

```
GET /api/orgs/
```

Retorna os dados de todas as organizações pesquisadas.

```
[
  {
    "login": "string",
    "name": "string",
    "score": int
  },
  {
    "login": "string",
    "name": "string",
    "score": int
  },
  ...
]
```

```
DELETE /api/orgs/<login>/
```
:login = login de uma organização cadastrada no GitHub.

Deleta a organização com o login enviado.