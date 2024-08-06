# backend-challenge

## Repostas:

## 1 - Consulta SQL que retorna o nome, e-mail e a descrição do papel e as descrição das permissões que um usuário possui:

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