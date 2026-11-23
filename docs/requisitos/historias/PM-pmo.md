# Histórias da Entrega 1: PMO (épico #5)

Rascunho para a revisão do responsável pelo produto, antes de criar as issues (Q228). Cada história sai da [ERS 1.1](../ERS.md), seção 3.2.2. Marco: Entrega 1. Rótulos: `enhancement`, `needs-triage`. Testes exigidos em cada uma: RNF-MAN-14 (válido e inválido de cada regra, com o código no teste), RNF-MAN-15 (valores-limite de cada entrada) e RNF-MAN-16 (acesso, com o papel aceito e o recusado).

Ficam para a Entrega 2, fora deste arquivo: RF-PM-09 (nível de exigência), RF-PM-12 (visão do supervisor por gerente de projetos) e RF-PM-14 (indicadores de apoio do parecer), com as regras RN-PM-13 a 15, RN-PM-40, RN-PM-41 e RN-PM-64. Quando uma história da Entrega 1 aplica uma regra de outro domínio, a regra aparece na tabela com a seção dela na ERS.

---

## RF-PM-01 · Ver as minhas pendências

**História:** Como gerente de projetos ou supervisor, quero ver numa só tela os registros que esperam uma ação minha, para não deixar nada parado nos projetos em andamento.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-PM-01 | O sistema deve mostrar a cada conta a tela Minhas pendências, com os registros dos projetos em andamento que esperam uma ação dela. | Q9, Q10, Q14, Q17, Q22, Q27, Q35, Q43, Q51, Q55 | alterado | 1 | teste |
| RN-PM-20 | As pendências de uma conta devem trazer as questões não resolvidas, os riscos ativos e os itens de escopo a fazer, em andamento ou concluídos, dos projetos em andamento cujo responsável é o membro da equipe ligado a essa conta. | PMBOK 7 §4.6.2, p. 185 (Q55) | alterado | 1 | teste |
| RN-PM-52 | A devolução deve aparecer nas pendências de quem enviou o registro e nas do gerente do projeto. | Regra do PMO (Q8) | novo | 1 | teste |
| RN-PM-63 | As pendências de um supervisor devem trazer os pedidos de revisão dos projetos de que ele é o supervisor designado. | Regra do PMO (Q9) | novo | 1 | teste |

**Critérios de aceite:**
- **RF-PM-01, válido:** Dado uma conta com registros que esperam uma ação dela, quando ela abre Minhas pendências, então vê cada registro com o projeto a que pertence.
- **RF-PM-01, inválido:** Dado um projeto encerrado ou cancelado, com uma questão não resolvida da conta, quando ela abre Minhas pendências, então a questão não aparece.
- **RN-PM-20, válido:** Dado um membro da equipe ligado à conta e responsável por uma questão não resolvida, um risco ativo e um item de escopo em andamento, quando a conta abre as pendências, então os três aparecem.
- **RN-PM-20, inválido:** Dado uma questão resolvida, um risco encerrado, ou um registro cujo responsável é um membro com o mesmo nome da pessoa, mas não ligado à conta dela, quando a conta abre as pendências, então eles não aparecem (Q55: o vínculo vale, o nome não).
- **RN-PM-52, válido:** Dado um registro enviado pelo gerente de apoio e devolvido, quando o gerente de apoio e o gerente do projeto abrem as pendências, então a devolução aparece para os dois.
- **RN-PM-52, inválido:** Dado a mesma devolução, quando outro gerente de projetos, sem ligação com o projeto, abre as pendências, então ela não aparece.
- **RN-PM-63, válido:** Dado um pedido de revisão num projeto de que o supervisor é o designado, quando ele abre as pendências, então o pedido aparece.
- **RN-PM-63, inválido:** Dado um pedido de revisão num projeto de outro supervisor designado, quando ele abre as pendências, então o pedido não aparece ali (ele pode revisar como substituto pelo projeto, pela RN-PM-44).

---

## RF-PM-02 · Enviar um registro para revisão

**História:** Como gerente do projeto ou gerente de apoio, quero enviar um registro para a revisão do supervisor designado, para que ele seja liberado antes de sair do projeto.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-PM-02 | Quando o gerente do projeto ou o gerente de apoio envia um registro para revisão, o sistema deve registrar o pedido e mostrá-lo nas pendências do supervisor designado. | Q9, Q10, Q14, Q27, Q35, Q43, Q51, Q56 | alterado | 1 | teste |
| RN-PM-16 | O termo de abertura, o relatório de status, a mudança, o encerramento e o tailoring devem passar por revisão obrigatória. | Regra do PMO (Q10, Q29, Q33) | alterado | 1 | teste |
| RN-PM-19 | O pedido de revisão deve guardar a conta de quem pediu. | Regra do PMO (Q51) | alterado | 1 | teste |
| RN-PM-42 | Um registro deve ter no máximo um pedido de revisão pendente. | Regra do PMO (Q10, Q14) | confirmado | 1 | teste |
| RN-PM-65 | O sistema deve aceitar pedido de revisão opcional para o risco, a questão e o item de escopo. | Regra do PMO (Q10) | alterado | 1 | teste |

**Critérios de aceite:**
- **RF-PM-02, válido:** Dado um termo de abertura, quando o gerente do projeto o envia para revisão, então o pedido fica registrado e aparece nas pendências do supervisor designado.
- **RF-PM-02, inválido:** Dado um gerente de projetos que não é o gerente do projeto nem o gerente de apoio, quando ele tenta enviar um registro do projeto para revisão, mesmo direto ao servidor, então o sistema recusa.
- **RN-PM-16, válido:** O termo de abertura, o relatório de status, a mudança, o encerramento e o tailoring oferecem o envio para revisão, e o registro só fica liberado por uma revisão.
- **RN-PM-16, inválido:** Dado um desses registros sem liberação, quando alguém tenta gerar o documento dele, então o sistema recusa (RN-PM-18, na RF-PM-11).
- **RN-PM-19, válido:** Dado um pedido enviado pelo gerente de apoio, quando o supervisor abre o pedido, então vê a conta de quem pediu.
- **RN-PM-19, inválido:** O pedido de revisão não é gravado sem a conta de quem pediu: um pedido sem sessão é recusado.
- **RN-PM-42, válido:** Dado um registro sem pedido pendente, quando o gerente o envia, então o pedido é aceito.
- **RN-PM-42, inválido:** Dado um registro com um pedido pendente, quando alguém o envia de novo, então o sistema recusa e mantém um só pedido.
- **RN-PM-65, válido:** Dado um risco, uma questão ou um item de escopo, quando o gerente o envia para revisão, então o pedido é aceito; sem o envio, o registro continua valendo.
- **RN-PM-65, inválido:** Dado um risco que nunca foi enviado para revisão, então ele não aparece nas pendências de nenhum supervisor, e nada no projeto fica bloqueado por isso.

**Fora desta história:** a conferência do estado "pronto para revisão" e a recusa do envio do que não está pronto (RN-PM-15 e RN-PM-40, Entrega 2).

---

## RF-PM-03 · Liberar ou devolver um registro

**História:** Como supervisor, quero liberar ou devolver com comentário um registro enviado para revisão, e editar os registros quando precisar, para garantir a qualidade do que sai dos projetos.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-PM-03 | O sistema deve permitir que um supervisor libere ou devolva com comentário um registro enviado para revisão. | Q8, Q9, Q10, Q14, Q15, Q17, Q22 | alterado | 1 | teste |
| RN-PM-17 | A devolução deve ter um comentário. | Regra do PMO (Q14, Q19) | alterado | 1 | teste |
| RN-PM-18 | O sistema deve gerar o documento de um registro de revisão obrigatória somente depois que ele for liberado. | Regra do PMO (Q10, Q14, Q15) | alterado | 1 | teste |
| RN-PM-43 | O sistema deve recusar a liberação e a devolução feitas por uma conta que não é do tipo supervisor. | Regra do PMO (Q2, Q14) | novo | 1 | teste |
| RN-PM-44 | O sistema deve aceitar a liberação ou a devolução feita por um supervisor que não é o designado, como substituto. | Regra do PMO (Q9) | novo | 1 | teste |
| RN-PM-48 | Quando o gerente do projeto ou o gerente de apoio altera um registro liberado, o sistema deve tirar a liberação do registro. | Regra do PMO (Q15) | novo | 1 | teste |
| RN-PM-52 | A devolução deve aparecer nas pendências de quem enviou o registro e nas do gerente do projeto. | Regra do PMO (Q8) | novo | 1 | teste |
| RN-PM-49 | Depois da edição feita por um supervisor, o sistema deve manter a liberação e o pedido de revisão do registro. | Regra do PMO (Q40) | novo | 1 | teste |
| RN-PM-50 | Quando um supervisor e um gerente do projeto ou gerente de apoio gravam o mesmo registro ao mesmo tempo, o sistema deve manter a versão do supervisor e mostrar ao gerente o que mudou. | Regra do PMO (Q34, Q40) | novo | 1 | teste |
| RN-PM-51 | O histórico deve marcar a edição feita por um supervisor como "editado pelo supervisor". | Regra do PMO (Q40) | novo | 1 | teste |
| RN-PM-62 | O sistema deve permitir que um supervisor edite os registros de um projeto em andamento. | Regra do PMO (Q34) | novo | 1 | teste |

**Entradas:** decisão da revisão (liberar ou devolver, obrigatória); comentário de devolução (obrigatório ao devolver, até 20.000 caracteres; só espaços conta como vazio, RN-DA-30).

**Critérios de aceite:**
- **RF-PM-03, válido:** Dado um registro com pedido de revisão, quando o supervisor designado o libera, então o registro fica liberado, com quem liberou e a data, e o pedido sai das pendências dele.
- **RN-PM-17, válido:** Quando o supervisor devolve com um comentário, então o registro fica devolvido, com o comentário.
- **RN-PM-17, inválido:** Quando o supervisor devolve sem comentário, ou só com espaços, então o sistema recusa e mostra o erro junto do campo.
- **RN-PM-18, válido:** Dado um termo de abertura liberado, quando o gerente gera o documento, então o documento sai.
- **RN-PM-18, inválido:** Dado um termo de abertura devolvido ou ainda sem revisão, quando o gerente tenta gerar o documento, então o sistema recusa.
- **RN-PM-43, inválido:** Dado um gerente de projetos, mesmo o gerente do projeto, quando ele tenta liberar ou devolver, mesmo direto ao servidor, então o sistema recusa.
- **RN-PM-44, válido:** Dado um supervisor que não é o designado do projeto, quando ele libera o registro, então a liberação é aceita e fica registrada em nome dele.
- **RN-PM-44, inválido:** Dado um registro sem pedido de revisão pendente, quando um supervisor tenta liberá-lo ou devolvê-lo, então o sistema recusa.
- **RN-PM-48, válido:** Dado um registro liberado, quando o gerente do projeto o altera, então a liberação sai e o registro volta a precisar de revisão.
- **RN-PM-48, inválido:** Dado um registro liberado, quando o gerente só o abre, sem gravar mudança, então a liberação continua.
- **RN-PM-52, válido:** Dado um registro devolvido, então a devolução aparece nas pendências de quem enviou e nas do gerente do projeto (os casos estão na RF-PM-01).
- **RN-PM-52, inválido:** A devolução não aparece nas pendências do supervisor que devolveu.
- **RN-PM-62, válido:** Dado um projeto em andamento, quando um supervisor edita um registro dele, então a edição é gravada.
- **RN-PM-62, inválido:** Dado um projeto encerrado ou cancelado, quando um supervisor tenta editar um registro dele, então o sistema recusa (o projeto fica só para consulta, RF-EC-06).
- **RN-PM-49, válido:** Dado um registro liberado, ou com pedido pendente, quando um supervisor o edita, então a liberação e o pedido continuam.
- **RN-PM-49, inválido:** Dado o mesmo registro, quando quem edita é o gerente do projeto, então vale a RN-PM-48: a liberação sai.
- **RN-PM-50, válido:** Dado um supervisor e o gerente do projeto com o mesmo registro aberto, quando os dois gravam, então fica a versão do supervisor, e o gerente vê o aviso com o que mudou.
- **RN-PM-50, inválido:** Dado só o gerente do projeto editando o registro, sem edição do supervisor no meio, quando ele grava, então a versão dele fica, sem aviso.
- **RN-PM-51, válido:** Quando um supervisor edita um registro, então o histórico mostra a linha como "editado pelo supervisor".
- **RN-PM-51, inválido:** Quando o gerente do projeto edita, então a linha do histórico não tem essa marca.

**Fora desta história:** gerar o documento (RF-PM-11). A edição pelo supervisor (RN-PM-49 a 51 e RN-PM-62) não tem função própria na ERS e ficou nesta história, que trata do trabalho do supervisor sobre os registros.

---

## RF-PM-04 · Buscar nos registros

**História:** Como pessoa com conta no Octante, quero buscar um texto nos registros dos projetos que eu posso ver, para achar uma informação sem abrir projeto por projeto.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-PM-04 | O sistema deve buscar um texto nos registros dos projetos visíveis para a conta e mostrar cada resultado com o projeto e o tipo de registro. | Q9, Q27, Q35, Q43 | alterado | 1 | teste |
| RN-PM-07 | O sistema deve mostrar um projeto a uma conta somente quando ela é do tipo supervisor, é o gerente do projeto ou o gerente de apoio dele, ou tem acesso de consulta a ele. | Regra do PMO (Q9, Q27, Q35, Q43) | alterado | 1 | teste |
| RN-PM-22 | A busca deve exigir pelo menos 2 caracteres. | Regra do PMO (Q51) | confirmado | 1 | teste |

A RN-PM-07 é do domínio Projetos (seção 3.2.4).

**Entradas:** texto da busca, de 2 a 20.000 caracteres.

**Critérios de aceite:**
- **RF-PM-04, válido:** Dado um risco com a palavra "fornecedor" num projeto visível, quando a pessoa busca "fornecedor", então o risco aparece, com o projeto e o tipo de registro.
- **RF-PM-04, inválido:** Quando a busca não acha nada, então a tela diz que não há resultados, sem erro.
- **RN-PM-07, válido:** Dado um gerente de projetos que é gerente de apoio do projeto A, quando ele busca um texto que está no projeto A, então o resultado aparece; um supervisor acha o texto em qualquer projeto.
- **RN-PM-07, inválido:** Dado o mesmo texto no projeto B, de que esse gerente não participa nem tem acesso de consulta, quando ele busca, então o resultado do projeto B não aparece.
- **RN-PM-22, válido:** Quando a busca tem 2 caracteres, então ela roda.
- **RN-PM-22, inválido:** Quando a busca tem 1 caractere, está vazia ou só tem espaços, então o sistema recusa e mostra o erro junto do campo.

---

## RF-PM-05 · Ver a agenda de prazos

**História:** Como pessoa com conta no Octante, quero ver numa agenda os prazos dos registros dos projetos que eu posso ver, para me organizar.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-PM-05 | O sistema deve mostrar a agenda com os prazos dos registros dos projetos visíveis para a conta. | Q9, Q27, Q35, Q43, Q67 | alterado | 1 | teste |
| RN-PM-07 | O sistema deve mostrar um projeto a uma conta somente quando ela é do tipo supervisor, é o gerente do projeto ou o gerente de apoio dele, ou tem acesso de consulta a ele. | Regra do PMO (Q9, Q27, Q35, Q43) | alterado | 1 | teste |

A RN-PM-07 é do domínio Projetos (seção 3.2.4).

**Critérios de aceite:**
- **RF-PM-05, válido:** Dado registros com prazo em projetos visíveis, quando a pessoa abre a agenda, então vê cada prazo, com a data no fuso configurado (RN-DA-16), o registro e o projeto.
- **RF-PM-05, inválido:** Dado um registro sem prazo, quando a pessoa abre a agenda, então ele não aparece, e a agenda sem nenhum prazo mostra a lista vazia, sem erro.
- **RN-PM-07, válido:** Dado uma conta com acesso de consulta ao projeto A, quando ela abre a agenda, então vê os prazos do projeto A.
- **RN-PM-07, inválido:** Dado o projeto B, de que a conta não participa, quando ela abre a agenda, então os prazos do projeto B não aparecem.

---

## RF-PM-06 · Exportar a agenda para o calendário

**História:** Como pessoa com conta no Octante, quero baixar a agenda de prazos num arquivo de calendário, para ver os prazos no meu calendário de costume.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-PM-06 | O sistema deve exportar a agenda de prazos num arquivo de calendário .ics. | Q9, Q27, Q35, Q43 | alterado | 1 | teste |
| RN-PM-07 | O sistema deve mostrar um projeto a uma conta somente quando ela é do tipo supervisor, é o gerente do projeto ou o gerente de apoio dele, ou tem acesso de consulta a ele. | Regra do PMO (Q9, Q27, Q35, Q43) | alterado | 1 | teste |

A RN-PM-07 é do domínio Projetos (seção 3.2.4).

**Critérios de aceite:**
- **RF-PM-06, válido:** Quando a pessoa exporta a agenda, então recebe um arquivo .ics válido, com um evento para cada prazo da agenda dela.
- **RF-PM-06, inválido:** Dado uma agenda sem prazos, quando a pessoa exporta, então recebe um .ics válido, sem eventos, e não um erro.
- **RN-PM-07, válido:** O arquivo traz os prazos dos projetos visíveis para a conta.
- **RN-PM-07, inválido:** O arquivo não traz nenhum prazo de projeto que a conta não pode ver.

---

## RF-PM-07 · Exportar os registros do projeto

**História:** Como pessoa que pode ver um projeto, quero exportar os riscos, as questões, as mudanças, as partes interessadas, o backlog e as lições numa planilha, para trabalhar com eles fora do Octante.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-PM-07 | O sistema deve exportar os riscos, as questões, as mudanças, as partes interessadas, o backlog e as lições aprendidas de um projeto numa planilha .xlsx ou num arquivo .csv, à escolha da pessoa. | Q9, Q27, Q35, Q43, Q104, Q119 | alterado | 1 | teste |
| RN-PM-07 | O sistema deve mostrar um projeto a uma conta somente quando ela é do tipo supervisor, é o gerente do projeto ou o gerente de apoio dele, ou tem acesso de consulta a ele. | Regra do PMO (Q9, Q27, Q35, Q43) | alterado | 1 | teste |
| RN-PM-39 | A planilha exportada por quem tem acesso de consulta deve sair sem a análise das partes interessadas e sem os dados pessoais dos membros da equipe. | PMBOK 7 §2.1.1.2, p. 12 (Q104, Q119; confirmação do resumo, 9.2) | novo | 1 | teste |
| RN-DA-14 | Na exportação, o sistema deve pôr um apóstrofo no início de cada célula que começa com =, +, −, @, tabulação ou retorno de linha. | Regra do PMO (Q51) | confirmado | 1 | teste |

A RN-PM-07 é do domínio Projetos (seção 3.2.4), e a RN-DA-14, do domínio Dados (seção 3.2.3).

**Entradas:** formato da exportação, .xlsx ou .csv.

**Critérios de aceite:**
- **RF-PM-07, válido:** Dado um projeto com registros dos seis tipos, quando o gerente do projeto exporta em .xlsx, e depois em .csv, então cada arquivo traz os seis tipos de registro.
- **RF-PM-07, inválido:** Quando o formato pedido não é .xlsx nem .csv, então o sistema recusa.
- **RN-PM-07, inválido:** Dado um projeto que a conta não pode ver, quando ela pede a exportação dele, mesmo direto ao servidor, então o sistema recusa.
- **RN-PM-39, válido:** Dado uma conta com acesso de consulta, quando ela exporta, então o arquivo sai sem a análise das partes interessadas e sem os dados pessoais dos membros da equipe.
- **RN-PM-39, inválido:** Dado o gerente do projeto, quando ele exporta, então o arquivo traz a análise das partes interessadas e os dados da equipe.
- **RN-DA-14, válido:** Dado um risco com o título "=SOMA(A1)", quando ele é exportado, então a célula sai como "'=SOMA(A1)", e o mesmo vale para +, −, @, tabulação e retorno de linha.
- **RN-DA-14, inválido:** Dado um título que começa com uma letra, quando ele é exportado, então a célula sai sem apóstrofo.

---

## RF-PM-08 · Criar um projeto a partir de um modelo

**História:** Como supervisor, quero criar um projeto a partir de um modelo de projeto, para começar com a abordagem, a cadência e os riscos iniciais já preenchidos.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-PM-08 | Quando um supervisor cria um projeto a partir de um modelo de projeto, o sistema deve preencher o projeto com a abordagem, a cadência de entrega, a unidade de estimativa, o limite de trabalho em andamento, a definição de pronto e os riscos iniciais do modelo. | Q27, Q56, Q127 | alterado | 1 | teste |
| RN-PM-08 | O supervisor que cria um projeto deve ficar como o supervisor designado dele. | Regra do PMO (Q9, Q27) | alterado | 1 | teste |

A RN-PM-08 é do domínio Projetos (seção 3.2.4).

**Critérios de aceite:**
- **RF-PM-08, válido:** Dado o modelo "Software adaptativo", quando o supervisor cria um projeto com ele, então o projeto nasce com a abordagem, a cadência de entrega, a unidade de estimativa, o limite de trabalho em andamento, a definição de pronto e os riscos iniciais do modelo.
- **RF-PM-08, inválido:** Dado um gerente de projetos, quando ele tenta criar um projeto, com ou sem modelo, mesmo direto ao servidor, então o sistema recusa (só o supervisor cria projeto, Q27); e um modelo que não existe é recusado.
- **RN-PM-08, válido:** Quando o supervisor cria o projeto, então ele fica como o supervisor designado.
- **RN-PM-08, inválido:** Dado o projeto criado pelo supervisor A, então o supervisor B não fica como designado e não recebe os pedidos de revisão do projeto nas pendências dele (RN-PM-63).

**Fora desta história:** o estado "pronto para revisão" dos campos preenchidos pelo modelo (RN-PM-15, Entrega 2) e a criação do projeto sem modelo (Projetos, #7).

---

## RF-PM-10 · Registrar a aprovação do termo ou da mudança

**História:** Como gerente do projeto ou gerente de apoio, quero registrar quem aprovou o termo de abertura ou a mudança, e quando, depois que o supervisor liberou e a pessoa com autoridade assinou, para que a aprovação fique no projeto.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-PM-10 | O sistema deve permitir que o gerente do projeto ou o gerente de apoio registre a aprovação de um termo de abertura ou de uma mudança liberados, com quem aprovou e a data. | Q14, Q62, Q69, Q109 | novo | 1 | teste |
| RN-PM-53 | O sistema deve recusar o registro da aprovação de um termo de abertura ou de uma mudança que não está liberado. | Regra do PMO (Q14) | novo | 1 | teste |
| RN-PM-54 | A aprovação deve registrar quem aprovou, escolhido entre as partes interessadas do projeto, e a data. | PMBOK 7 p. 184 e §2.6, p. 87 (Q14, Q69, Q109) | novo | 1 | teste |

**Entradas:** quem aprovou (uma parte interessada do projeto, obrigatória); data da aprovação (obrigatória, uma data válida, até a data de hoje).

**Critérios de aceite:**
- **RF-PM-10, válido:** Dado um termo de abertura liberado, quando o gerente do projeto registra a aprovação com o patrocinador e a data de hoje, então a aprovação fica registrada no termo.
- **RF-PM-10, inválido:** Dado um gerente de projetos de fora do projeto, quando ele tenta registrar a aprovação, mesmo direto ao servidor, então o sistema recusa.
- **RN-PM-53, válido:** Dado uma mudança liberada, quando o gerente registra a aprovação, então ela é aceita.
- **RN-PM-53, inválido:** Dado um termo ou uma mudança devolvidos, ou ainda sem revisão, quando o gerente tenta registrar a aprovação, então o sistema recusa.
- **RN-PM-54, válido:** Quando o gerente escolhe uma parte interessada do projeto e uma data até hoje, então a aprovação é aceita.
- **RN-PM-54, inválido (pessoa):** Quando ninguém é escolhido, ou a pessoa é parte interessada de outro projeto, então o sistema recusa.
- **RN-PM-54, inválido (data):** Quando a data é amanhã, ou não é uma data válida, então o sistema recusa e mostra o erro junto do campo.

**Fora desta história:** quem tem a autoridade para aprovar, o patrocinador no termo e a autoridade de mudança na mudança, que são regras dos domínios Planejamento e Trabalho do projeto (Q14, Q69).

---

## RF-PM-11 · Gerar o documento de um registro liberado

**História:** Como gerente do projeto, quero gerar o documento do termo de abertura, da mudança, do relatório de status e do encerramento, para imprimir ou salvar em PDF e levar à assinatura ou aos destinatários.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-PM-11 | O sistema deve gerar o documento do termo de abertura, da mudança, do relatório de status e do encerramento, para imprimir ou salvar em PDF. | Q11, Q15, Q104, Q119 | novo | 1 | teste |
| RN-PM-18 | O sistema deve gerar o documento de um registro de revisão obrigatória somente depois que ele for liberado. | Regra do PMO (Q10, Q14, Q15) | alterado | 1 | teste |
| RN-PM-45 | O documento gerado deve mostrar quem liberou o registro e a data da liberação. | Regra do PMO (Q15) | novo | 1 | teste |
| RN-PM-46 | O documento gerado deve sair sem a análise das partes interessadas e sem os dados pessoais dos membros da equipe. | PMBOK 7 §2.1.1.2, p. 12 (Q104, Q119) | novo | 1 | teste |
| RN-PM-47 | No documento gerado, um alerta sobre uma pessoa deve sair sem o nome dela. | Regra do PMO (Q104) | novo | 1 | teste |

**Critérios de aceite:**
- **RF-PM-11, válido:** Dado um termo, uma mudança, um relatório de status e um encerramento liberados, quando o gerente gera o documento de cada um, então sai uma página pronta para imprimir ou salvar em PDF pelo navegador.
- **RF-PM-11, inválido:** Dado uma conta que não pode ver o projeto, quando ela pede o documento, mesmo direto ao servidor, então o sistema recusa.
- **RN-PM-18, válido:** Dado o registro liberado, então o documento sai.
- **RN-PM-18, inválido:** Dado o registro devolvido, sem revisão, ou alterado depois da liberação (RN-PM-48), então o sistema recusa gerar o documento.
- **RN-PM-45, válido:** O documento mostra o nome de quem liberou e a data da liberação.
- **RN-PM-45, inválido:** Dado um registro liberado por um substituto (RN-PM-44), o documento mostra o substituto, e não o supervisor designado.
- **RN-PM-46, válido:** Dado um projeto com análise das partes interessadas e dados pessoais da equipe, quando o documento é gerado, então nenhum desses dados aparece nele.
- **RN-PM-46, inválido:** Os mesmos dados continuam aparecendo nas telas do projeto para o gerente do projeto; a regra vale só para o documento.
- **RN-PM-47, válido:** Dado um alerta sobre um membro da equipe, quando o documento é gerado, então o alerta sai sem o nome da pessoa.
- **RN-PM-47, inválido:** Dado um alerta que não é sobre uma pessoa, então ele sai como está.

---

## RF-PM-13 · Escrever um parecer sobre um gerente de projetos

**História:** Como supervisor, quero escrever, quando quiser e em texto livre, um parecer sobre um gerente de projetos, para registrar como ele está se desenvolvendo.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-PM-13 | O sistema deve permitir que um supervisor escreva, em texto livre, um parecer sobre um gerente de projetos. | Q19, Q20, Q24 | novo | 1 | teste |
| RN-PM-57 | A tela do parecer deve avisar a quem escreve que a pessoa avaliada recebe o parecer se pedir os próprios dados e o PMO aceitar o pedido. | Regra do PMO (Q191b; LGPD, arts. 18 e 19) | novo | 1 | teste |
| RN-PM-59 | O sistema deve gerar o documento do parecer sem passar por revisão. | Regra do PMO (Q24) | novo | 1 | teste |
| RN-PM-60 | O parecer deve guardar só o texto escrito pelo supervisor, sem nota calculada a partir dos indicadores de apoio. | Regra do PMO (Q20, Q23) | novo | 1 | teste |

**Entradas:** pessoa avaliada (uma conta do tipo gerente de projetos, obrigatória); texto do parecer (obrigatório, até 20.000 caracteres).

**Critérios de aceite:**
- **RF-PM-13, válido:** Dado um supervisor, quando ele escreve um parecer sobre um gerente de projetos, então o parecer fica gravado com a data e o nome de quem escreveu.
- **RF-PM-13, inválido:** Dado um gerente de projetos, quando ele tenta abrir a tela do parecer ou gravar um parecer, mesmo direto ao servidor, então o sistema recusa; e um parecer sobre uma conta do tipo supervisor, ou com o texto vazio ou com 20.001 caracteres, é recusado.
- **RN-PM-57, válido:** Quando o supervisor abre a tela do parecer, então vê o aviso de que a pessoa avaliada recebe o parecer se pedir os próprios dados e o PMO aceitar.
- **RN-PM-57, inválido:** O aviso aparece em cada abertura da tela, e não só na primeira: não há opção de dispensá-lo.
- **RN-PM-59, válido:** Dado um parecer gravado, então o documento dele pode ser gerado na hora (RF-PM-16), sem pedido de revisão.
- **RN-PM-59, inválido:** O parecer não oferece o envio para revisão, e um pedido de revisão de parecer enviado direto ao servidor é recusado.
- **RN-PM-60, válido:** O parecer gravado tem só o texto, a pessoa avaliada, a data e quem escreveu.
- **RN-PM-60, inválido:** O parecer não tem campo de nota, e nenhuma nota é calculada nem gravada a partir dos indicadores.

**Fora desta história:** os indicadores de apoio mostrados enquanto o supervisor escreve (RF-PM-14, Entrega 2).

---

## RF-PM-15 · Ver os pareceres sobre uma pessoa

**História:** Como supervisor, quero ver os pareceres escritos sobre um gerente de projetos, com a data e quem escreveu cada um, para acompanhar o desenvolvimento dele.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-PM-15 | O sistema deve mostrar ao supervisor os pareceres sobre uma pessoa, com a data e quem escreveu cada um. | Q20, Q21, Q211 | novo | 1 | teste |
| RN-PM-55 | O sistema deve mostrar os pareceres somente a contas do tipo supervisor. | Regra do PMO (Q21, Q58) | novo | 1 | teste |
| RN-PM-56 | O sistema deve recusar à pessoa avaliada o acesso aos pareceres sobre ela, inclusive depois que ela passa a supervisor. | Regra do PMO (Q21, Q211) | novo | 1 | teste |

**Critérios de aceite:**
- **RF-PM-15, válido:** Dado três pareceres sobre uma pessoa, escritos por dois supervisores, quando um supervisor os abre, então vê os três, cada um com a data e quem escreveu.
- **RF-PM-15, inválido:** Dado uma pessoa sem parecer, quando o supervisor abre os pareceres dela, então a tela diz que não há pareceres, sem erro.
- **RN-PM-55, válido:** Dado qualquer conta do tipo supervisor, com ou sem o papel de Administrador, quando ela abre os pareceres, então os vê.
- **RN-PM-55, inválido:** Dado uma conta do tipo gerente de projetos, quando ela tenta abrir os pareceres de qualquer pessoa, mesmo direto ao servidor, então o sistema recusa.
- **RN-PM-56, válido:** Dado um supervisor que nunca foi avaliado, quando ele abre os pareceres de outra pessoa, então os vê.
- **RN-PM-56, inválido:** Dado um gerente de projetos que passou a supervisor e tem pareceres sobre ele, quando ele tenta abrir os próprios pareceres, ou o documento de um deles, então o sistema recusa; os pareceres sobre os outros continuam abertos para ele.

**Fora desta história:** o parecer entregue num pedido do titular, que é do Administrador (Q191b, Dados, #6).

---

## RF-PM-16 · Gerar o documento de um parecer

**História:** Como supervisor, quero gerar o documento de um parecer, para imprimir ou salvar em PDF quando o PMO precisar.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-PM-16 | O sistema deve permitir que um supervisor gere o documento de um parecer, para imprimir ou salvar em PDF. | Q24 | novo | 1 | teste |
| RN-PM-55 | O sistema deve mostrar os pareceres somente a contas do tipo supervisor. | Regra do PMO (Q21, Q58) | novo | 1 | teste |
| RN-PM-56 | O sistema deve recusar à pessoa avaliada o acesso aos pareceres sobre ela, inclusive depois que ela passa a supervisor. | Regra do PMO (Q21, Q211) | novo | 1 | teste |
| RN-PM-59 | O sistema deve gerar o documento do parecer sem passar por revisão. | Regra do PMO (Q24) | novo | 1 | teste |

**Critérios de aceite:**
- **RF-PM-16, válido:** Dado um parecer, quando um supervisor gera o documento, então sai uma página pronta para imprimir ou salvar em PDF, com o texto, a pessoa avaliada, a data e quem escreveu.
- **RN-PM-55, inválido:** Dado um gerente de projetos, quando ele pede o documento de um parecer, mesmo direto ao servidor, então o sistema recusa.
- **RN-PM-56, inválido:** Dado a pessoa avaliada, já supervisor, quando ela pede o documento de um parecer sobre ela, então o sistema recusa.
- **RN-PM-55 e RN-PM-56, válido:** Dado um supervisor que não é a pessoa avaliada, quando ele pede o documento, então o documento sai.
- **RN-PM-59, válido:** Dado um parecer recém-gravado, sem nenhuma revisão, quando o supervisor gera o documento, então ele sai.
- **RN-PM-59, inválido:** O documento do parecer não mostra campos de revisão (quem liberou e quando), porque o parecer não passa por revisão.

---

## RF-PM-17 · Definir o prazo de guarda dos pareceres

**História:** Como Administrador, quero definir por quantos anos os pareceres ficam guardados depois que a pessoa deixa de ser gerente de projetos, para cumprir o prazo que o RH ou o jurídico do PMO definir.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-PM-17 | O sistema deve permitir que o Administrador defina o prazo de guarda dos pareceres, em anos, com 5 anos de padrão. | Q25, Q211 | novo | 1 | teste |
| RN-PM-58 | O prazo de guarda de um parecer deve contar da data em que a pessoa avaliada deixa de ser gerente de projetos, pela desativação da conta ou pela mudança para supervisor. | Regra do PMO (Q25, Q211; LGPD) | novo | 1 | teste |

**Entradas:** prazo de guarda, número inteiro de anos, de 1 a 20; padrão 5.

**Ponto a confirmar:** os 5 anos de padrão dependem da confirmação do RH ou do jurídico do PMO, que o responsável pelo produto obtém até a Entrega 1 (ERS, seção 5.5). A história pode ser construída com o padrão de 5 anos; se o número mudar, muda só o padrão.

**Critérios de aceite:**
- **RF-PM-17, válido:** Dado uma instalação nova, quando o Administrador abre a configuração, então o prazo é 5 anos; quando ele grava 1 ou 20, então o prazo novo vale.
- **RF-PM-17, inválido:** Quando o prazo é 0, 21, vazio, com casa decimal ou com letras, então o sistema recusa e mostra o erro junto do campo; e uma conta sem o papel de Administrador não abre nem grava a configuração.
- **RN-PM-58, válido (desativação):** Dado um gerente de projetos desativado em 01/03/2027 e o prazo de 5 anos, então o prazo dos pareceres dele vence em 01/03/2032.
- **RN-PM-58, válido (passou a supervisor):** Dado um gerente de projetos que passou a supervisor em 01/03/2027, então o prazo conta dessa data.
- **RN-PM-58, inválido:** Dado um gerente de projetos ativo, então os pareceres dele não têm prazo correndo e não aparecem como vencidos.

---

## RF-PM-18 · Excluir o parecer com o prazo vencido

**História:** Como Administrador, quero ser avisado quando o prazo de guarda de um parecer vence e confirmar a exclusão dele, para que o parecer não fique guardado além do prazo.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-PM-18 | Quando o Administrador confirma a exclusão de um parecer com o prazo de guarda vencido, o sistema deve excluí-lo de vez, inclusive do histórico. | Q25, Q59, Q194, Q221 | novo | 1 | teste |
| RN-PM-61 | Quando o prazo de guarda de um parecer vence, o sistema deve mostrar ao Administrador, no portfólio, um alerta alto pedindo a confirmação da exclusão. | Regra do PMO (Q25, Q153, Q193, Q221) | novo | 1 | teste |
| RN-PM-78 | A tela de confirmação da exclusão de um parecer vencido deve mostrar de quem é o parecer e quando o prazo venceu, sem o texto do parecer. | Regra do PMO (Q221) | novo | 1 | teste |
| RN-DA-17 | O banco deve recusar a alteração e a exclusão de linhas do histórico, exceto pelas rotinas da anonimização e da exclusão do parecer vencido. | Regra do PMO (Q194; LGPD, arts. 6º, X, e 37) | novo | 1 | teste |
| RN-DA-18 | Cada rotina que apaga linhas do histórico deve deixar um evento com o que foi apagado, quando e por quem, sem o conteúdo apagado. | Regra do PMO (Q194) | novo | 1 | teste |

As RN-DA-17 e RN-DA-18 são do domínio Dados (seção 3.2.3).

**Critérios de aceite:**
- **RF-PM-18, válido:** Dado um parecer vencido, quando o Administrador confirma a exclusão, então o parecer some das telas, do banco e do histórico.
- **RF-PM-18, inválido:** Dado um parecer ainda no prazo, quando alguém pede a exclusão, mesmo direto ao servidor, então o sistema recusa; e um supervisor sem o papel de Administrador não exclui nenhum parecer.
- **RN-PM-61, válido:** Dado um parecer cujo prazo venceu hoje, quando o Administrador abre o portfólio, então vê o alerta alto, que leva à tela de confirmação.
- **RN-PM-61, inválido:** Dado um parecer com o prazo vencendo amanhã, então o alerta não aparece; e um supervisor sem o papel de Administrador não vê o alerta.
- **RN-PM-78, válido:** A tela de confirmação mostra o nome da pessoa avaliada e a data em que o prazo venceu.
- **RN-PM-78, inválido:** A tela de confirmação não mostra o texto do parecer.
- **RN-DA-17, válido:** A rotina da exclusão do parecer vencido apaga as linhas do histórico ligadas ao parecer.
- **RN-DA-17, inválido:** Uma alteração ou exclusão de linha do histórico feita fora dessa rotina e da anonimização é recusada pelo próprio banco.
- **RN-DA-18, válido:** Depois da exclusão, o histórico tem um evento dizendo que um parecer foi apagado, quando e por qual Administrador.
- **RN-DA-18, inválido:** O evento não traz o texto do parecer.

**Fora desta história:** a contagem do prazo (RF-PM-17) e os backups antigos, que guardam o parecer até a rotação deles (RN-DA-10, Dados, #6).
