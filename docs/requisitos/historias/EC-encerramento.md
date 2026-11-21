# Histórias da Entrega 1: Encerramento (épico #20)

Rascunho para a revisão do responsável pelo produto, antes de criar as issues (Q228). Cada história sai da [ERS 1.0](../ERS.md), seção 3.2.17. Marco: Entrega 1. Rótulos: `enhancement`, `needs-triage`. Testes exigidos em cada uma: RNF-MAN-14 (válido e inválido de cada regra, com o código no teste), RNF-MAN-15 (valores-limite de cada entrada) e RNF-MAN-16 (acesso, com o papel aceito e o recusado).

---

## RF-EC-01 · Ver o encerramento do projeto

**História:** Como gerente do projeto, quero ver o encerramento do projeto, com o checklist, a comparação com o planejado e os objetivos do termo, para preparar o encerramento sabendo o que falta.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-EC-01 | O sistema deve mostrar o encerramento do projeto: o checklist automático, o checklist manual, a comparação com o planejado e os objetivos do termo. | Q64, Q65, Q112, Q174a | alterado | 1 | teste |
| RN-EC-02 | O checklist automático deve conferir: entregas aceitas ou canceladas; mudanças rejeitadas ou implementadas; questões resolvidas; riscos encerrados; nenhum benefício só planejado; pelo menos uma lição; fases concluídas, exceto a fase chamada Encerramento; aquisições fora das ativas; conformidade sem pendente nem em andamento; grupos de mudança organizacional adotados; e nenhum membro ativo. | PMBOK 7 §2.3.5 e §4.6 | alterado | 1 | teste |
| RN-EC-04 | O encerramento deve comparar o escopo total com o aceito, o orçamento no término com o custo real e mostrar o fim planejado. | PMBOK 7 p. 47 | confirmado | 1 | teste |
| RN-EC-11 | As lições com alcance outras equipes ou organização devem aparecer em destaque no encerramento. | PMBOK 7 §2.5.8.1, p. 77 | confirmado | 1 | teste |

**Critérios de aceite:**
- **RN-EC-02, válido:** Dado um projeto com cada item do checklist automático cumprido, quando o gerente abre o encerramento, então cada item aparece como feito.
- **RN-EC-02, inválido:** Dado um projeto com uma mudança só aprovada, ainda não implementada, quando o gerente abre o encerramento, então o item das mudanças aparece como pendente. Vale o mesmo para cada um dos outros itens: um caso pendente para cada.
- **RN-EC-04, válido:** Dado um projeto com escopo, orçamento e custo real, quando o gerente abre o encerramento, então a tela mostra o escopo total e o aceito, o orçamento no término e o custo real, e o fim planejado.
- **RN-EC-04, inválido:** Dado um projeto sem orçamento nem itens, quando o gerente abre o encerramento, então a comparação mostra "sem dados", sem erro.
- **RN-EC-11, válido:** Dado uma lição com alcance organização, quando o gerente abre o encerramento, então a lição aparece em destaque.
- **RN-EC-11, inválido:** Dado uma lição com alcance projeto, quando o gerente abre o encerramento, então ela aparece sem destaque.

**Fora desta história:** o checklist manual e a regra que esconde os itens de módulo desligado (RN-EC-03, Entrega 2).

---

## RF-EC-02 · Registrar a avaliação final

**História:** Como gerente do projeto, quero registrar a avaliação final dos objetivos e dos benefícios em relação ao termo, para levar o encerramento à revisão do supervisor.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-EC-02 | O sistema deve permitir registrar a avaliação final do projeto. | Q64, Q65 | alterado | 1 | teste |
| RN-EC-05 | Encerrar ou cancelar deve exigir a avaliação dos objetivos e dos benefícios em relação ao termo de abertura. | PMBOK 7 p. 47 | confirmado | 1 | teste |

**Critérios de aceite:**
- **RF-EC-02, válido:** Dado um projeto em andamento, quando o gerente grava a avaliação final, então ela fica registrada e aparece no encerramento.
- **RN-EC-05, válido:** Dado um projeto com a avaliação final registrada, quando o supervisor encerra ou cancela, então a avaliação não bloqueia a ação.
- **RN-EC-05, inválido:** Dado um projeto sem a avaliação final, quando o supervisor tenta encerrar ou cancelar, então o sistema recusa e mostra o erro junto do campo.

**Fora desta história:** o envio do encerramento para revisão, que usa a RF-PM-02.

---

## RF-EC-03 · Encerrar o projeto

**História:** Como supervisor, quero encerrar um projeto em andamento depois da revisão do encerramento e do aceite final, para fechar formalmente o projeto.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-EC-03 | O sistema deve permitir que um supervisor encerre o projeto em andamento. | Q29, Q63, Q64, Q65 | alterado | 1 | teste |
| RN-EC-05 | Encerrar ou cancelar deve exigir a avaliação dos objetivos e dos benefícios em relação ao termo de abertura. | PMBOK 7 p. 47 | confirmado | 1 | teste |
| RN-EC-07 | Encerrar com pendência no checklist automático ou manual deve exigir justificativa. | Regra do PMO | confirmado | 1 | teste |
| RN-EC-08 | Ao encerrar ou cancelar, o sistema deve gravar a situação e a data de encerramento. | PMBOK 7 p. 166 | confirmado | 1 | teste |
| RN-EC-12 | Somente um supervisor deve encerrar ou cancelar o projeto. | Regra do PMO | novo | 1 | teste |
| RN-EC-13 | Encerrar deve exigir o aceite final registrado; cancelar não exige. | PMBOK 7 §4.4.3, p. 180 | novo | 1 | teste |
| RN-EC-15 | Encerrar deve exigir o encerramento, com o checklist e a avaliação final, liberado na revisão. | Regra do PMO | novo | 1 | teste |

**Critérios de aceite:**
- **RN-EC-12, válido:** Dado um projeto pronto para encerrar, quando um supervisor encerra, então o projeto fica encerrado.
- **RN-EC-12, inválido:** Dado o mesmo projeto, quando um gerente de projetos tenta encerrar, então o sistema recusa, e nada muda.
- **RN-EC-15, inválido:** Dado um encerramento ainda não liberado na revisão, quando o supervisor tenta encerrar, então o sistema recusa e diz que falta a liberação.
- **RN-EC-13, inválido:** Dado um encerramento liberado sem aceite final registrado, quando o supervisor tenta encerrar, então o sistema recusa e diz que falta o aceite final.
- **RN-EC-05, inválido:** Dado um projeto sem avaliação final, quando o supervisor tenta encerrar, então o sistema recusa.
- **RN-EC-07, válido:** Dado um checklist sem pendência, quando o supervisor encerra sem justificativa, então o encerramento é aceito.
- **RN-EC-07, inválido:** Dado um checklist com pendência, quando o supervisor encerra sem justificativa, então o sistema recusa e mostra o erro junto do campo.
- **RN-EC-08, válido:** Depois do encerramento, o projeto mostra a situação encerrado e a data de encerramento.

**Fora desta história:** a passagem da equipe para a dissolução (RN-EQ-20, Entrega 3) e o registro do aceite final (RF-EC-07).

---

## RF-EC-04 · Cancelar o projeto

**História:** Como supervisor, quero cancelar um projeto em andamento, com justificativa, para encerrar formalmente um projeto que não vai continuar.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-EC-04 | O sistema deve permitir que um supervisor cancele o projeto em andamento, com justificativa. | Q29, Q63, Q64 | alterado | 1 | teste |
| RN-EC-05 | Encerrar ou cancelar deve exigir a avaliação dos objetivos e dos benefícios em relação ao termo de abertura. | PMBOK 7 p. 47 | confirmado | 1 | teste |
| RN-EC-06 | Cancelar deve exigir justificativa. | Regra do PMO | confirmado | 1 | teste |
| RN-EC-08 | Ao encerrar ou cancelar, o sistema deve gravar a situação e a data de encerramento. | PMBOK 7 p. 166 | confirmado | 1 | teste |
| RN-EC-12 | Somente um supervisor deve encerrar ou cancelar o projeto. | Regra do PMO | novo | 1 | teste |

**Critérios de aceite:**
- **RN-EC-12, válido:** Dado um projeto em andamento, quando um supervisor cancela com justificativa e avaliação, então o projeto fica cancelado.
- **RN-EC-12, inválido:** Dado um projeto em andamento, quando um gerente de projetos tenta cancelar, então o sistema recusa, e nada muda.
- **RN-EC-06, inválido:** Quando o supervisor cancela sem justificativa, então o sistema recusa e mostra o erro junto do campo.
- **RN-EC-05, inválido:** Quando falta a avaliação dos objetivos e dos benefícios, então o sistema recusa.
- **RN-EC-08, válido:** Depois do cancelamento, o projeto mostra a situação cancelado e a data de encerramento.

**Fora desta história:** reabrir o projeto (RF-EC-05) e a passagem da equipe para a dissolução (RN-EQ-20, Entrega 3).

---

## RF-EC-05 · Reabrir o projeto

**História:** Como supervisor, quero reabrir um projeto encerrado ou cancelado, com justificativa, para corrigir um encerramento feito antes da hora.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-EC-05 | O sistema deve permitir que um supervisor reabra o projeto encerrado ou cancelado, com justificativa. | Q29, Q65 | alterado | 1 | teste |
| RN-EC-09 | Somente um supervisor deve reabrir o projeto, com justificativa. | Regra do PMO | alterado | 1 | teste |

**Critérios de aceite:**
- **RN-EC-09, válido:** Dado um projeto encerrado, quando um supervisor reabre com justificativa, então o projeto volta a em andamento, e a justificativa fica no histórico.
- **RN-EC-09, inválido (papel):** Dado o mesmo projeto, quando um gerente de projetos tenta reabrir, então o sistema recusa, e nada muda.
- **RN-EC-09, inválido (justificativa):** Quando o supervisor tenta reabrir sem justificativa, então o sistema recusa e mostra o erro junto do campo.

**Fora desta história:** o link Reabrir na faixa de somente consulta (RNF-USA-02).

---

## RF-EC-06 · Projeto encerrado só para consulta

**História:** Como supervisor do PMO, quero que o projeto encerrado ou cancelado fique só para consulta, inclusive a tela de encerramento, para o registro final não mudar depois.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-EC-06 | O sistema deve manter o projeto encerrado ou cancelado só para consulta, inclusive a tela de encerramento. | Q65 | alterado | 1 | teste |
| RN-EC-10 | A tela de encerramento deve ficar só para consulta depois do encerramento. | Regra do PMO | alterado | 1 | teste |
| RN-PM-23 | O sistema deve recusar gravações num projeto encerrado ou cancelado, exceto a reabertura pelo supervisor e as anonimizações das RF-DA-10 e RF-DA-15. | Regra do PMO | alterado | 1 | teste |

**Critérios de aceite:**
- **RN-PM-23, inválido:** Dado um projeto encerrado, quando alguém tenta gravar um registro de qualquer domínio, então o sistema recusa, e nada muda. Um caso por tela de gravação.
- **RN-PM-23, válido:** Dado um projeto encerrado, quando o supervisor reabre, então a reabertura é aceita.
- **RN-EC-10, inválido:** Dado um projeto encerrado, quando alguém tenta alterar a avaliação final ou o checklist manual, então o sistema recusa.

**Fora desta história:** as anonimizações (RF-DA-10, RF-DA-15), que estão na Entrega 2.

---

## RF-EC-07 · Registrar o aceite final

**História:** Como gerente do projeto, quero registrar o aceite final, com quem aceitou e a data, para o supervisor poder encerrar o projeto.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-EC-07 | O sistema deve permitir registrar o aceite final, com quem aceitou e a data. | Q63, Q109 | novo | 1 | teste |
| RN-EC-14 | O aceite final deve registrar quem aceitou, escolhido entre as partes interessadas (patrocinador, dono do produto ou cliente), e a data. | PMBOK 7 §4.4.3, p. 180 | novo | 1 | teste |

**Entrada:** data do aceite, até a data de hoje (Q224).

**Critérios de aceite:**
- **RN-EC-14, válido:** Dado um encerramento liberado, quando o gerente registra o aceite com uma parte interessada e a data de hoje, então o aceite fica registrado.
- **RN-EC-14, inválido (pessoa):** Quando o gerente tenta registrar o aceite sem escolher quem aceitou, ou com alguém fora das partes interessadas, então o sistema recusa.
- **RN-EC-14, inválido (data):** Quando a data do aceite é amanhã, então o sistema recusa e mostra o erro junto do campo.

**Fora desta história:** o encerramento em si (RF-EC-03).
