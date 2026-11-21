---
status: accepted
---

# Evoluir o protótipo, reauditando todas as regras

A versão nova do Octante é construída evoluindo o protótipo, e não reescrevendo do zero. A stack (Python, Flask e SQLite) continua, o banco começa limpo, porque o protótipo só tem dados de teste e o projeto de exemplo, e os testes existentes são aproveitados. Em troca, nenhuma regra de negócio, requisito funcional ou requisito não funcional do protótipo é aceito só por estar escrito e testado: todos passam pela auditoria da elicitação, conferidos contra o PMBOK 7. O que for alterado ou descartado é reimplementado, mesmo que já tenha teste. A reescrita foi considerada porque as regras do protótipo não nasceram de um processo de requisitos, mas a auditoria resolve isso sem jogar fora o que está certo.

Decisões de origem: Q39, Q46 e Q47 em `docs/requisitos/decisoes-elicitacao.md`.
