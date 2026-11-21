---
status: accepted
---

# Só um Supervisor recebe o papel de Administrador

O papel de Administrador (usuários, backups, lixeira e LGPD) só pode ser dado a quem já é Supervisor. O motivo é o backup: ele é o banco inteiro e inclui os pareceres do supervisor, que nenhum gerente de projetos pode ler, nem pela tela, nem por exportação, nem por backup. As alternativas eram criptografar os pareceres ou deixá-los fora do backup, e as duas complicariam a restauração. Para o sistema nunca ficar sem administração, sempre existe pelo menos um Administrador ativo.

Decisões de origem: Q7, Q21, Q22, Q52 e Q58 em `docs/requisitos/decisoes-elicitacao.md`.
