---
status: accepted
---

# Só o PMBOK 7 é referência, e a tela mostra a origem de cada regra

O PMBOK 7 é a única referência das regras de gerenciamento de projetos do Octante. O protótipo foi feito sem processo de requisitos e trouxe regras de outras fontes: o PMBOK 6, a grade de Mendelow, os nomes das categorias de saliência de Mitchell, Agle e Wood, o formato de visão de Moore, o pré-mortem e as convenções do *Standard for Earned Value Management*. Na auditoria da elicitação, essas regras são não conformidades: saem ou são trocadas pelo que o PMBOK 7 diz, e não ficam nem com um rótulo de origem. Quando o PMBOK 7 não trata de algo que o app precisa decidir, como uma escala de notas, um prazo em dias ou o fluxo de revisão do supervisor, a regra só existe por decisão explícita do responsável pelo produto, registrada em `docs/requisitos/decisoes-elicitacao.md` como regra do PMO. Nesse caso, e só nele, o PMO pode pedir sugestões, e outras fontes podem servir de base para elas. Como o Octante ensina o PMBOK enquanto é usado, essa diferença aparece na tela: os campos do PMBOK vêm primeiro, com a seção citada, e as regras do PMO ficam abaixo, num bloco "Campos do PMO".

A primeira versão desta decisão aceitava modelos de fora do PMBOK 7 com um rótulo de origem. Foi corrigida em 17/11/2026 porque contrariava a regra do responsável pelo produto: "eu ja tinha deixado claro que o PMBOK 7 é a unica referência".

A auditoria da Abordagem e tailoring achou mais três casos, tratados da mesma forma: o Cynefin com 4 domínios e o nome "claro", quando o PMBOK 7 tem 5 contextos; a dimensão "acordo sobre requisitos" da matriz de Stacey original, quando o PMBOK 7 usa a incerteza dos requisitos; e o nome do método Scrum num modelo de projeto. A dos Princípios achou mais três: o termo "prontidão" (readiness), que o PMBOK 7 não usa; o ROI acumulado e o selo "viável" pelo VPL, quando o PMBOK 7 define o ROI pela média dos benefícios líquidos e lê o resultado pela razão benefício-custo; e uma nota calculada para cada princípio, quando o PMBOK 7 diz que os princípios não são prescritivos.

Decisões de origem: Q49, Q61, Q66, Q68, Q86, Q102, Q105, Q106, Q113, Q125, Q126, Q127, Q138, Q140 e Q143 em `docs/requisitos/decisoes-elicitacao.md`.
