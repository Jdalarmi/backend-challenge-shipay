# backend-challenge

## Repostas:

## 1 - Consulta SQL que retorna o nome, e-mail e a descrição do papel e as descrições das permissões que um usuário possui:

```
SELECT
    u."name" AS user_name,
    u.email AS user_email,
    r.description AS role_description,
    c.description AS claim_description
FROM
    users u
JOIN
    roles r ON u.role_id = r.id
LEFT JOIN
    user_claims uc ON u.id = uc.user_id
LEFT JOIN
    claims c ON uc.claim_id = c.id;

```

## 2 - Utilizando SQLAlchemy a implementação esta disponível na construção do endpoint:

GET: http://127.0.0.1:8000/v1/users/

Diretorio: app/routes/shipay_routes.py

A consulta utilizada segue abaixo:
```
query = session.query(User).options(
        joinedload(User.role),
        joinedload(User.claims)
    )
    users = query.all()
```

## 3 - Endpoint da API REST que lista o papel de um usuario pelo role_id

GET: http://localhost:8000/v1/roles/{role_id}

## 4 - Para criar usuario deve ser feito requisição do tipo POST para endpoint abaixo:

POST: http://localhost:8000/v1/roles/

Na resposta foi implementado praticas de HATEOAS que permite guiar usuario através de link paraa criar um papel para usuario se o mesmo for atribuido a um papel que não existe.

## 5 -  Execução do projeto e deploy:

- Para executar projeto local, é necessario ter docker instalado o que facilita e previne erros de dependencia, para isso basta estar na pasta raiz onde se encontra os arquivos DockerFile e docker-compose.yml e executar comando:

```docker-compose up -d --build```

Aguarde o build ser concluido, logo após é possível acessar a documentação do swagger da API REST em: http://localhost:8000/docs

# Deploy

Para deploy como projeto est com dockerizado é possivel apenas subir a imagem para local necessario e rodar.

## 6.1 - Qual comando posso utilizar para listar os logs (no stdio) do Pod de Jobs?

````kubectl logs -n staging jobs-77f78ccf9b-7jpct````

## 6.2 - De acordo com o log capturado, o que pode estar originando a falha?

A mensagem de erro: AttributeError: module 'core.settings' has no attribute ‘WALLET_X_TOKEN_MAX_AGE'

Indica que variável WALLET_X_TOKEN_MAX_AGE não esta definida no modulo core.settings.

## 7 - Code Review do arquivo bot.py
- As revisões se encontram em formato de comentarios no codigo.

## 8 - Qual ou quais Padrões de Projeto/Design Patterns você utilizaria para normalizar serviços de terceiros (tornar múltiplas interfaces de diferentes fornecedores uniforme), por exemplo serviços de disparos de e-mails, ou então disparos de SMS.

-

