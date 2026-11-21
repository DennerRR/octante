# Inventário de regras de negócio do Octante

Os caminhos abaixo partem da raiz do repositório e as linhas se referem ao protótipo no commit 626d8fb.

**Como ler a origem declarada:**
- "PMBOK 7 §x" quando o código, a docstring ou o README citam a seção.
- "PMBOK 6 / outra fonte" quando o README trata a regra como referência complementar. Na auditoria, essas regras são não conformidades, porque o PMBOK 7 é a única referência (Q49).
- "convenção do app" quando o README diz isso ou quando nenhuma fonte é citada.

**Marcação ⚠:** regra inconsistente, contraditória com outra, ou que só existe no template/JS (o servidor não garante).

---

## 1. Partes interessadas (PI)

- PI-01 | O nome da parte interessada é obrigatório, ao cadastrar e ao editar. | rotas_partes.py:22, :66 | convenção do app
- PI-02 | Não pode haver duas partes com o mesmo nome no mesmo projeto (comparação sem diferenciar maiúsculas). | rotas_partes.py:24-26 | convenção do app (AVALIACAO R6)
- PI-03 ⚠ | A checagem de nome duplicado só roda no cadastro. Ao editar, dá para renomear para um nome que já existe. O botão "fornecedor vira parte interessada" também cria a parte sem checar duplicata. | rotas_partes.py:65-69; suprimentos.py:187 | convenção do app
- PI-04 | No nível "rigoroso", o papel da parte é obrigatório. | pmo.py:88-89; rotas_partes.py:23, :66 | convenção do app
- PI-05 | Valores padrão de uma parte nova: interna = sim, ativa = sim, atitude = "desconhecida". | rotas_partes.py:44; schema.sql:52-60 | convenção do app
- PI-06 | Categorias possíveis (exemplos da Figura 2-2): Gerente do projeto, Equipe de gerenciamento, Equipe do projeto, Órgão de governança, PMO, Comitê diretor, Patrocinador, Fornecedor, Cliente, Usuário final, Órgão regulador, Outro. | pmbok.py:303-307 | PMBOK 7 Fig. 2-2
- PI-07 | Poder, interesse, influência e impacto vão de 1 a 5. Valor fora da faixa vira vazio. | app.py:581-584; util.py:9-14 | PMBOK 7 §2.1
- PI-08 | A atitude é uma de quatro: apoiador, neutro, opositor ou desconhecida. Qualquer outro valor vira "desconhecida". | pmbok.py:309-314; app.py:585 | PMBOK 7 §2.1
- PI-09 | A proximidade é uma de três: direta, próxima ou distante. | pmbok.py:316-320 | PMBOK 7 §2.1.1.2
- PI-10 | A parte conta como "analisada" quando tem poder, interesse e uma atitude diferente de "desconhecida". | partes.py:31 | convenção do app
- PI-11 | Grade poder × interesse: nota 4 ou 5 é "alto". Os quadrantes são: alto/alto = "Gerenciar de perto"; só poder alto = "Manter satisfeita"; só interesse alto = "Manter informada"; nenhum alto = "Monitorar". | pmbok.py:373-388 | PMBOK 6 / outra fonte (grade de Mendelow)
- PI-12 | Modelo de saliência, com os marcadores poder, legitimidade e urgência:
  - os três = Definitiva;
  - poder + legitimidade = Dominante;
  - poder + urgência = Perigosa;
  - legitimidade + urgência = Dependente;
  - só poder = Adormecida;
  - só legitimidade = Discricionária;
  - só urgência = Exigente;
  - nenhum = Sem saliência. | pmbok.py:357-370 | PMBOK 7 §4.2.7.5 (nomes: Mitchell, Agle e Wood)
- PI-13 | Ordem de prioridade exibida: primeiro a ordem manual; depois o quadrante (Gerenciar de perto → Manter satisfeita → Manter informada → Monitorar → sem análise); depois poder × interesse, do maior para o menor; por fim o nome. | partes.py:70-77; pmbok.py:391 | convenção do app
- PI-14 | Ordem sugerida, que ignora a ordem manual: quadrante, depois poder × interesse (decrescente), depois influência (decrescente), depois nome. | partes.py:80-90 | PMBOK 7 §2.1.1.3
- PI-15 | Na priorização há três ações:
  - "sugerida" grava a ordem da análise;
  - "limpar" apaga a ordem manual;
  - a ordem manual aceita de 1 a 1.000.000 e é renumerada em 1..n.

  A parte conta como "priorizada" quando tem ordem manual. | rotas_partes.py:128-151; partes.py:32 | convenção do app
- PI-16 | Níveis de engajamento de 1 a 5: Desconhece, Resistente, Neutro, Apoiador, Lidera. | pmbok.py:325-331 | PMBOK 6 / outra fonte (PMBOK 6 §13.2.2.5)
- PI-17 | Lacuna de engajamento = nível desejado − nível atual. Só é calculada quando os dois existem. | partes.py:36-39 | PMBOK 7 §4.6.6
- PI-18 | A parte tem "plano de engajamento" quando há nível atual, nível desejado e método de comunicação. | partes.py:33-35 | convenção do app
- PI-19 | Métodos de comunicação: push, pull ou interativa. Tipos: verbal formal, verbal informal, escrita formal, escrita informal. Frequências: Diária, Semanal, Quinzenal, Mensal, Por marco/fase, Por iteração, Sob demanda. | pmbok.py:335-354 | PMBOK 7 §2.1.1.4 e Tabela 2-1
- PI-20 | Toda mudança do nível atual de engajamento gera um registro no histórico (nível anterior → novo). No cadastro, o nível inicial é registrado com "anterior" vazio. | rotas_partes.py:35-37, :76-78, :176-178 | convenção do app
- PI-21 | Uma interação não pode ter data futura. Data vazia ou inválida vira hoje. A satisfação (1 a 5) é opcional. | app.py:604-617 | convenção do app (README v2)
- PI-22 | Para registrar uma interação é preciso escolher a parte interessada. | rotas_partes.py:191-194 | convenção do app
- PI-23 | A parte conta como "monitorada" quando teve interação nos últimos 30 dias. | partes.py:13, :44-45 | convenção do app
- PI-24 | Partes inativas saem das listas de análise, priorização, engajamento e alertas e dos indicadores. O registro mostra todas. | partes.py:51-56; rotas_partes.py:11 | convenção do app
- PI-25 | Alerta médio: nenhuma parte interessada identificada. | partes.py:130-132 | convenção do app
- PI-26 | Alerta alto: opositor com poder ≥ 4. | partes.py:135-136 | convenção do app
- PI-27 | Alerta alto: a última satisfação registrada é ≤ 2. | partes.py:137-138 | convenção do app
- PI-28 | Alerta alto: parte em "Gerenciar de perto" sem interação nos últimos 30 dias. | partes.py:139-141 | convenção do app
- PI-29 ⚠ | Alerta médio: lacuna de engajamento ≥ 2. Quando o nível atual está acima do desejado (lacuna negativa), não há alerta. | partes.py:142-143 | convenção do app
- PI-30 | Alerta informativo: parte ainda não analisada. | partes.py:144-145 | convenção do app
- PI-31 | Uma parte pode ser excluída sem restrição. Interações e histórico vão junto; riscos, questões, itens, mudanças, membros e aquisições ligados a ela perdem o vínculo. | rotas_partes.py:85-93; db.py:37, :84, :105, :161, :282 | convenção do app
- PI-32 | Uma interação pode ser excluída sem restrição. | rotas_partes.py:217-231 | convenção do app
- PI-33 | Evidência para a Tabela 2-2: número de mudanças solicitadas por parte interessada (muitas podem indicar desalinhamento). | trabalho.py:141-146; app.py:239-242 | PMBOK 7 Tabela 2-2

## 2. Equipe (EQ)

- EQ-01 | O nome do membro é obrigatório. | equipe.py:174-176, :210-212 | convenção do app
- EQ-02 | Valores padrão do membro: dedicação "integral" (ou "parcial"), local "presencial" (ou "híbrido"/"remoto"). O motivador só pode ser um dos 9 da lista. | equipe.py:151-155; pmbok.py:668-672 | PMBOK 7 §2.2.4.3
- EQ-03 | O membro pode ser ligado a um usuário ativo do app (para "Minhas pendências") e a uma parte interessada do mesmo projeto. | equipe.py:131-135, :145-147 | convenção do app (README v14)
- EQ-04 | Modelo de liderança: centralizada ou distribuída. | pmbok.py:656-659; equipe.py:166-170 | PMBOK 7 §2.2.1.1-2
- EQ-05 | Estágios de Tuckman: formação, confronto, normatização, desempenho, dissolução. | pmbok.py:661-667 | PMBOK 7 §4.2.6.1 (nomes em PT: tradução usual)
- EQ-06 | Liberar um membro o desativa e grava a data; reativar limpa a data. | equipe.py:203-207 | convenção do app
- EQ-07 | Um membro pode ser excluído sem restrição; os papéis RACI dele vão junto. | equipe.py:198-202; db.py:296 | convenção do app
- EQ-08 | O acordo de trabalho tem 5 seções: valores, comunicação, decisões, conflitos e reuniões. | equipe.py:18, :225-237 | PMBOK 7 §2.2 (team charter)
- EQ-09 | Uma linha da RACI precisa de descrição. Se estiver ligada a um item, a descrição padrão é "I-n título". | equipe.py:248-261 | convenção do app
- EQ-10 | Na RACI, cada membro tem no máximo um papel por linha (R, A, C ou I). Só membros ativos aparecem. | equipe.py:244, :266-276; db.py:298 | convenção do app
- EQ-11 ⚠ | A RACI deve ter exatamente um A e pelo menos um R por linha. Isso só gera alerta médio, não impede salvar. O README v6 diz que a matriz "exige". | equipe.py:43-50, :98-99 | convenção do app
- EQ-12 | Fatores de alto desempenho: 9, com nota de 1 a 5. A avaliação precisa de pelo menos um fator com nota. A data não pode ser futura. Participantes: 1 a 1000. | equipe.py:294-304; pmbok.py:674-684 | PMBOK 7 §2.2.3; escala 1-5: convenção do app
- EQ-13 | Média da avaliação = média das notas preenchidas. | equipe.py:60-61 | convenção do app
- EQ-14 | Alerta médio: na última avaliação, algum fator ficou ≤ 2 (fator sem nota conta como 5). | equipe.py:72, :103-105 | convenção do app (README)
- EQ-15 | Alerta informativo: nenhum membro cadastrado. Com zero membros, os outros alertas de equipe não aparecem. | equipe.py:92-94 | convenção do app
- EQ-16 | Alerta médio: acordo de trabalho sem nenhuma seção preenchida. | equipe.py:95-97 | convenção do app
- EQ-17 | Alerta informativo: membro com lacunas de habilidade e sem plano de desenvolvimento. | equipe.py:78, :100-102 | convenção do app
- EQ-18 | Alerta informativo: nenhuma avaliação de saúde, ou a última tem mais de 45 dias. | equipe.py:19, :106-108 | convenção do app
- EQ-19 | Alerta informativo: projeto adaptativo com mais de 9 membros ativos (referência 7 ± 2). | equipe.py:20, :109-111 | PMBOK 7 §2.3.4.3
- EQ-20 | Ao encerrar ou cancelar o projeto, o estágio da equipe passa para "dissolução". | ciclo.py:318 | PMBOK 7 §4.2.6.1

## 3. Abordagem, ciclo de vida e tailoring (AB)

- AB-01 | A abordagem é preditiva, híbrida ou adaptativa. Qualquer outro valor vira "não definida". | pmbok.py:201-205; app.py:429-431 | PMBOK 7 §2.3
- AB-02 ⚠ | Cadência possível: única, múltiplas, periódica ou contínua. O servidor não confere o valor recebido em criar, editar ou abordagem. | pmbok.py:208-213; app.py:336, :390, :437 | PMBOK 7 §2.3.2
- AB-03 | Há 15 fatores de seleção, cada um com nota de 1 (favorece preditiva) a 5 (favorece adaptativa). Fator sem nota é ignorado. | pmbok.py:217-249; app.py:425-428 | PMBOK 7 §2.3.4
- AB-04 | Sugestão de abordagem pela média dos fatores: abaixo de 2,5 = preditiva; acima de 3,5 = adaptativa; senão híbrida. Também mostra a média por categoria (Produto, Projeto, Organização). | pmbok.py:252-269 | convenção do app
- AB-05 | A sugestão é só informativa: a equipe escolhe outra abordagem sem precisar justificar. | app.py:429-444; templates/abordagem.html:8 | convenção do app
- AB-06 | Matriz de Stacey (acordo sobre requisitos + certeza tecnológica, cada um de 1 a 5): soma ≤ 4 = Simples/preditiva; ≤ 6 = Complicado/híbrida; ≤ 8 = Complexo/adaptativa; acima = Caótico/adaptativa. | metodos.py:142-153, :163 | convenção do app (README cita a seção 4)
- AB-07 | Cynefin tem 4 domínios: claro, complicado, complexo e caótico. | metodos.py:17-22, :160 | PMBOK 7 §4
- AB-08 | Modelos de projeto (Em branco, Scrum ágil, Híbrido, Preditivo) já gravam abordagem, cadência, unidade de estimativa, WIP (3, 3 ou nenhum), definição de pronto, fases sugeridas e 3 riscos típicos. | pmo.py:19-60; app.py:339 | convenção do app
- AB-09 ⚠ | Os riscos criados pelo modelo usam fontes ("Mercado/cliente", "Equipe", "Fornecedor", "Técnico") que não estão na lista oficial. Eles também não registram a revisão inicial. | pmo.py:25-43, :58-60; pmbok.py:419-423 | convenção do app
- AB-10 | Fases sugeridas por abordagem: preditiva com 6 fases, híbrida com 6, adaptativa com 3, cada uma com critérios de saída. Sem abordagem definida, usa as da híbrida. | pmbok.py:698-728; ciclo.py:74 | PMBOK 7 §2.3.5 e §2.3.6
- AB-11 | As fases sugeridas só podem ser aplicadas a um ciclo de vida vazio. | ciclo.py:70-72 | convenção do app
- AB-12 | O nome da fase é obrigatório. A ordem é sequencial e automática (de 1 a 1000). | ciclo.py:80-86, :137 | convenção do app
- AB-13 | O término da fase não pode ser antes do início. | ciclo.py:109-111 | convenção do app
- AB-14 | Status da fase: não iniciada, em andamento ou concluída. Decisões possíveis na revisão de fase: seguir, seguir com ressalvas, repetir/estender, encerrar o projeto. | pmbok.py:690-696 | PMBOK 7 §2.3.5
- AB-15 | Para concluir a fase, todos os critérios de saída precisam estar marcados e é preciso registrar a decisão e quem decidiu. Fase sem critérios conclui só com a decisão. | ciclo.py:118-125 | PMBOK 7 §2.3.5
- AB-16 | Se a decisão for "repetir/estender", a fase volta para "em andamento" em vez de concluir. | ciclo.py:126-128 | PMBOK 7 §2.3.5
- AB-17 ⚠ | A decisão "encerrar" só leva à tela de encerramento; o projeto não é encerrado. | ciclo.py:141-143 | convenção do app
- AB-18 ⚠ | Uma fase concluída pode voltar para outro status sem regra nenhuma. Fases podem ser excluídas sem restrição. | ciclo.py:103-107, :115 | convenção do app
- AB-19 | A data da revisão de fase é gravada quando a decisão muda. | ciclo.py:129-131 | convenção do app
- AB-20 | Alerta informativo: projeto preditivo ou híbrido sem fases. | ciclo.py:51-52 | convenção do app
- AB-21 | Alerta médio: fase não concluída com término vencido. | ciclo.py:36, :54-55 | convenção do app (README)
- AB-22 | Alerta informativo: fase concluída "com ressalvas" sem notas registradas. | ciclo.py:56-57 | convenção do app
- AB-23 | Tailoring: 15 perguntas de contexto (Produto, Equipe, Cultura); só as respostas preenchidas são guardadas. | pmbok.py:730-746; ciclo.py:205-208 | PMBOK 7 §3.4.3
- AB-24 | Uma decisão de tailoring exige o elemento e o tipo (adicionar, remover ou ajustar). A data é sempre hoje. | ciclo.py:209-216 | PMBOK 7 §3
- AB-25 | Diagnóstico pela Tabela 3-1, com 7 situações detectadas a partir dos dados:
  - (a) custo das falhas maior que o de conformidade;
  - (b) mudança aguardando decisão há mais de 7 dias;
  - (c) WIP acima do limite, ou, sem limite, WIP ≥ 5 e maior que metade dos itens;
  - (d) satisfação média das partes abaixo de 3;
  - (e) itens existentes, nenhum relatório de status nos últimos 30 dias e nenhum indicador;
  - (f) 3 ou mais questões sem risco de origem nos últimos 60 dias;
  - (g) "entendimento compartilhado" com nota ≤ 2 na última avaliação.

  Cada situação gera um alerta informativo. | ciclo.py:152-195, :58-59 | PMBOK 7 Tabela 3-1; limiares: convenção do app

## 4. Planejamento (PL)

- PL-01 | O nome do projeto é obrigatório ao criar e ao editar. | app.py:329-332, :383-386 | convenção do app
- PL-02 ⚠ | O nome do projeto não precisa ser único. O projeto de exemplo é reconhecido por conter "AgendaFácil" no nome, então um projeto real com esse nome seria tratado como exemplo. | app.py:292; pmo.py:268 | convenção do app
- PL-03 | Ao criar um projeto, ele já nasce com um termo de abertura vazio (rascunho). | app.py:338; schema.sql:30 | convenção do app
- PL-04 | Status do termo de abertura: rascunho, em revisão ou aprovado. Qualquer outro valor vira rascunho. | app.py:458-459 | PMBOK 7 §4.6.1
- PL-05 | Para aprovar o termo é preciso propósito, objetivos, critérios de sucesso, patrocinador, gerente e "aprovado por". Se faltar algo, o status volta ao anterior; se o anterior era "aprovado", vira "em revisão". | app.py:54, :464-468 | PMBOK 7 (AVALIACAO R2)
- PL-06 | Se o termo for aprovado sem data, a data de aprovação é hoje. | app.py:469-470 | convenção do app
- PL-07 | No nível "rigoroso", qualquer status diferente de rascunho exige patrocinador. Se faltar, o termo é salvo como rascunho, mesmo que já estivesse aprovado. | app.py:460-463; pmo.py:90-91 | convenção do app
- PL-08 ⚠ | Alterar um termo já aprovado só gera um aviso para registrar a mudança. Não bloqueia nem cria a mudança automaticamente. | app.py:471-474 | convenção do app (README v2)
- PL-09 | A declaração de visão é gerada automaticamente quando o texto está vazio e os 5 campos (público, necessidade, produto, categoria, benefício) estão preenchidos, ou quando o usuário pede. Formato: "Para… que… o… é um(a)… que…". | app.py:55, :475-476, :624-635 | PMBOK 6 / outra fonte (elevator pitch de G. Moore)
- PL-10 | Alerta médio: abordagem não definida. | app.py:172-174 | convenção do app
- PL-11 | Alerta médio: projeto preditivo com termo não aprovado. | app.py:176-178 | PMBOK 7 §4.6.1
- PL-12 | Alerta médio: projeto adaptativo ou híbrido sem declaração de visão. | app.py:179-181 | PMBOK 7 §4.6.1
- PL-13 | Datas do projeto: o término planejado não pode ser antes do início. | medicao.py:561-567 | convenção do app
- PL-14 | Uma iteração exige nome, início e fim, com fim ≥ início. O banco também garante isso e capacidade ≥ 0. | medicao.py:569-574; db.py:541-546 | PMBOK 7 §2.4.2.3
- PL-15 | Iterações não podem se sobrepor. A comparação inclui as pontas: duas iterações que compartilham um dia já conflitam. | medicao.py:570-576 | convenção do app (AVALIACAO R5)
- PL-16 ⚠ | Não existe tela para editar uma iteração: só criar ou excluir. Excluir devolve os itens dela ao backlog. | medicao.py:581-583; db.py:215 | convenção do app
- PL-17 | Datas planejadas de um item: término antes do início faz o app ignorar as datas daquele item (e avisar). Custos planejado e real ≥ 0. Iteração inexistente vira "sem iteração". | medicao.py:591-602; db.py:535-540 | convenção do app
- PL-18 ⚠ | Item com custo planejado acima da capacidade da iteração, ou com término planejado vencido, só aparece como selo na tela de cronograma. Não vira alerta. | templates/cronograma.html:47, :66 | convenção do app
- PL-19 | Dependências entre itens: um item não pode depender de si mesmo nem formar ciclo. As dependências que criariam ciclo são descartadas com aviso. | metodos.py:39-54; db.py:577; entrega.py:455-462 | PMBOK 7 §4
- PL-20 ⚠ | Conflito de dependência no Gantt (item começa antes ou no dia em que o predecessor termina) só aparece na tela do Gantt. Não vira alerta nem impede salvar. | metodos.py:80-84 | convenção do app
- PL-21 | Agenda: junta prazos de questões, iterações, entregas, compras, premissas, revisões de decisões, benefícios, próxima revisão de cada risco (última revisão + cadência) e fim do projeto. Evento atrasado = não feito com data antes de hoje. | pmo.py:323-356 | convenção do app
- PL-22 ⚠ | Na agenda, uma premissa conta como "feita" quando o status é diferente de "a_validar", status que não existe (o real é "nao_validada"). Resultado: toda premissa aparece como feita e nunca atrasada. | pmo.py:341 | convenção do app
- PL-23 | O arquivo de calendário (.ics) leva só os eventos ainda não feitos. | pmo.py:375-377 | convenção do app

## 5. Trabalho do projeto (TR)

- TR-01 | O título da questão é obrigatório. | trabalho.py:214, :254 | convenção do app
- TR-02 | Questão: prioridade padrão "média" (alta, média, baixa); status padrão "aberta" (aberta, em andamento, resolvida). Prazo inválido vira vazio. O risco ligado precisa ser do mesmo projeto. | trabalho.py:168-188 | PMBOK 7 §2.5
- TR-03 | No nível "rigoroso", a questão exige responsável e prazo. | pmo.py:75-76 | convenção do app
- TR-04 | Para marcar uma questão como resolvida é preciso descrever a resolução. Se faltar, o status volta ao anterior; se já estava resolvida, vira "em andamento". | trabalho.py:258-260 | convenção do app (README v3)
- TR-05 ⚠ | Essa exigência de resolução não vale no cadastro: dá para criar uma questão já "resolvida" sem descrever a resolução. | trabalho.py:219-220 | convenção do app
- TR-06 | A data de resolução é gravada ao resolver (a primeira data é mantida) e apagada ao reabrir. | trabalho.py:261-264 | convenção do app
- TR-07 | Questão atrasada = não resolvida com prazo antes de hoje. Dias em aberto = (data de resolução ou hoje) − data de criação. | trabalho.py:39-43 | convenção do app
- TR-08 | Alerta alto: questão atrasada. | trabalho.py:111-112 | convenção do app
- TR-09 | Alerta médio: questão sem responsável e sem parte interessada ligada. | trabalho.py:113-114 | convenção do app
- TR-10 | Alerta médio: questão de prioridade alta sem prazo. | trabalho.py:115-116 | convenção do app
- TR-11 | Uma questão pode ser excluída sem restrição. | trabalho.py:247-251 | convenção do app
- TR-12 | Indicador: tempo médio de resolução (média dos dias em aberto das questões resolvidas). | trabalho.py:95 | convenção do app
- TR-13 | O título da mudança é obrigatório. | trabalho.py:320, :361 | convenção do app
- TR-14 | Status da mudança: solicitada, em análise, aprovada, rejeitada, implementada. "Pendentes" = solicitada e em análise. Padrão: solicitada. | pmbok.py:508-515; trabalho.py:287 | PMBOK 7 §2.5.7
- TR-15 | Aprovar, rejeitar ou implementar exige informar quem decidiu. | trabalho.py:295-296 | PMBOK 7 §2.5.7
- TR-16 | Em projetos preditivos, híbridos ou sem abordagem, aprovar ou rejeitar exige os 6 impactos preenchidos: escopo, cronograma, orçamento, recursos, partes interessadas e riscos (pode ser "sem impacto"). Em projetos adaptativos não há essa exigência. | trabalho.py:297-301; pmbok.py:519-526 | PMBOK 7 Tabela 2-7, §2.5.7
- TR-17 | Só uma mudança aprovada (ou já implementada) pode passar a "implementada". Não dá para criar uma mudança já implementada. | trabalho.py:302-303 | PMBOK 7 §2.5.7
- TR-18 ⚠ | Fora a TR-17, qualquer transição é permitida, inclusive aprovada → solicitada e rejeitada → aprovada. O fluxo descrito no README (solicitada → em análise → aprovada/rejeitada → implementada) não é obrigatório. | trabalho.py:292-304 | convenção do app
- TR-19 | Mudanças aprovadas ou implementadas não podem ser excluídas; só as pendentes ou rejeitadas. | trabalho.py:352-356 | convenção do app (AVALIACAO R4)
- TR-20 ⚠ | Por causa da TR-18, dá para contornar a TR-19: volta-se a mudança aprovada para "solicitada" e depois ela pode ser excluída. | trabalho.py:351-362 | convenção do app
- TR-21 | Data de decisão: no cadastro, é gravada para aprovada, rejeitada ou implementada; na edição, só quando o status muda para aprovada ou rejeitada. | trabalho.py:326-327, :368-369 | convenção do app
- TR-22 ⚠ | No nível "rigoroso", a mudança exige solicitante e justificativa. Isso só é conferido no cadastro, não na edição. | pmo.py:83-84; trabalho.py:321 vs :362 | convenção do app
- TR-23 | Alerta médio: mudança pendente criada há mais de 7 dias. | trabalho.py:16, :66-67, :119-120 | convenção do app (README)
- TR-24 | Alerta médio: mudança aprovada ou implementada ainda não comunicada às partes interessadas. | trabalho.py:121-122 | PMBOK 7 §2.5.7
- TR-25 | Indicador: quantas mudanças decididas tiveram avaliação completa dos 6 impactos. | trabalho.py:133-136 | PMBOK 7 Tabela 2-7
- TR-26 | A descrição da lição aprendida é obrigatória. A data não pode ser futura. | trabalho.py:406-417 | convenção do app
- TR-27 ⚠ | Lição: o tipo padrão no formulário é "melhorar", mas no banco é "manter". Também tem origem, domínio, conhecimento (padrão explícito; ou tácito), alcance (padrão projeto; ou outras equipes ou organização) e a questão de origem, que precisa ser do mesmo projeto. | trabalho.py:418-426; db.py:126 | PMBOK 7 §2.5.8.1-2
- TR-28 | Uma lição pode ser marcada como aplicada (grava a data) ou desmarcada (apaga a data). | trabalho.py:396-405 | PMBOK 7 princípio 11
- TR-29 | Uma lição pode ser excluída sem restrição. | trabalho.py:390-395 | convenção do app

## 6. Entrega (EN)

- EN-01 | O título do item é obrigatório. | entrega.py:471, :516 | convenção do app
- EN-02 | Tipos de item: épico, funcionalidade, história (padrão), entregável, pacote de trabalho, requisito. No formulário de item novo, o padrão é "entregável" para projetos preditivos e "história" para os demais. | pmbok.py:550-557; entrega.py:300, :488 | PMBOK 7 §2.6.2.2
- EN-03 | O item pai precisa ser do mesmo projeto e não pode ser o próprio item nem um descendente dele. | entrega.py:278-290 | convenção do app
- EN-04 | Ordem de 1 a 1.000.000. Valor de negócio de 1 a 5 (o banco também garante). Estimativa ≥ 0 (banco também). Classificação MoSCoW: deve, deveria, poderia, não terá agora. | entrega.py:302-315; db.py:535-540; metodos.py:15 | PMBOK 7 §4 (MoSCoW)
- EN-05 | Unidade de estimativa: pontos (padrão), horas ou dias. Limite de WIP: de 1 a 1000, ou sem limite. | entrega.py:380-383; db.py:140 | convenção do app
- EN-06 | Requisito bem documentado = 5 critérios:
  - claro, conciso e consistente: marcados à mão;
  - verificável: tem critérios de aceite;
  - rastreável: sempre verdadeiro (pelo código do item). | entrega.py:28-37; pmbok.py:573-579 | PMBOK 7 §2.6.2.1
- EN-07 | Status do item: a fazer, em andamento, concluído, aceito, cancelado. "Feito" = concluído ou aceito. | pmbok.py:558-564; entrega.py:38 | convenção do app
- EN-08 | Concluir ou aceitar exige confirmar a definição de pronto, mas só quando o projeto tem uma escrita. | entrega.py:334-335 | PMBOK 7 §2.6.2.2
- EN-09 | Aceitar exige critérios de aceite e o nome de quem aceitou. | entrega.py:336-340 | PMBOK 7 §2.6.2.2
- EN-10 | No nível "rigoroso", começar um item ("em andamento") exige critérios de aceite. | pmo.py:85-87; entrega.py:328-331 | convenção do app
- EN-11 | Datas automáticas do item:
  - a fazer apaga início, conclusão e aceite;
  - em andamento grava o início e apaga conclusão e aceite;
  - concluído grava início e conclusão e apaga o aceite;
  - aceito grava as três.

  Datas que já existiam são mantidas. | entrega.py:341-353 | convenção do app
- EN-12 ⚠ | Não há ordem obrigatória entre status: dá para ir de "a fazer" direto para "aceito", ou de "aceito" de volta para "a fazer". Cancelar não pede motivo. | entrega.py:319-354 | convenção do app
- EN-13 | No quadro, os itens só se movem entre 4 colunas (a fazer, em andamento, concluído, aceito), com as mesmas regras. Se faltar algo, o app leva à página do item. | entrega.py:536-555; pmbok.py:565 | convenção do app
- EN-14 ⚠ | Um item pode ser excluído sem restrição, mesmo aceito ou dentro da linha de base. | entrega.py:509-514 | convenção do app
- EN-15 | Itens de trabalho = itens sem filhos e não cancelados. Os percentuais (concluído, aceito) usam a soma das estimativas, mas só quando todos esses itens têm estimativa; senão contam itens. | entrega.py:99-101, :156-159, :185-186 | convenção do app
- EN-16 | Linha de base do escopo: exige pelo menos um item de trabalho. Grava título, estimativa, custo planejado e datas de cada item. A versão é o número de linhas de base gravadas. | entrega.py:393-416, :118 | PMBOK 7 §2.4.2.1
- EN-17 | Refazer a linha de base exige motivo. | entrega.py:407-409 | convenção do app (README v4)
- EN-18 | Scope creep = item de trabalho fora da linha de base atual sem mudança aprovada ou implementada ligada. Em projetos não adaptativos gera alerta alto e deixa o escopo "crítico" no semáforo. | entrega.py:122-128, :214-217; medicao.py:264-265 | PMBOK 7 §2.6 / Tabela 2-7
- EN-19 | Projeto adaptativo: alerta médio se, nos últimos 30 dias, entrou mais trabalho novo do que foi concluído. Com linha de base, "novo" = fora dela; sem linha de base, só conta se o projeto já tinha itens antes desses 30 dias. | entrega.py:18, :167-176, :218-221 | PMBOK 7 Tabela 2-7
- EN-20 ⚠ | Alerta médio: itens em andamento acima do limite de WIP. Isso não impede mover mais itens para "em andamento", embora a ajuda da tela diga "respeite o limite". | entrega.py:222-224; guia.py:111 | convenção do app
- EN-21 | Alerta médio: item em andamento sem critérios de aceite. | entrega.py:226-227 | convenção do app
- EN-22 | Alerta médio: item concluído há mais de 14 dias e ainda não aceito. | entrega.py:17, :228-229 | convenção do app
- EN-23 ⚠ | Alerta informativo: mudança aprovada sem item de escopo ligado. Só vale para "aprovada"; as "implementadas" ficam de fora. | entrega.py:233-239 | convenção do app
- EN-24 | Alerta informativo: projeto adaptativo ou híbrido com itens e sem definição de pronto. | entrega.py:244-245 | convenção do app
- EN-25 | Custo da qualidade: 4 categorias. Prevenção e avaliação contam como conformidade; falha interna e externa, como não conformidade. | pmbok.py:582-588; entrega.py:131-149 | PMBOK 7 §2.6.3.1
- EN-26 | Um registro de custo da qualidade exige categoria e descrição. Data não futura; custo ≥ 0. Defeito resolvido = marca alternável. | entrega.py:577-595 | convenção do app
- EN-27 | Alerta médio: custo das falhas maior que o investido em prevenção e avaliação (e maior que zero). | entrega.py:241-243 | PMBOK 7 §2.6.3.1
- EN-28 | A descrição do benefício é obrigatória. Status: planejado, parcial, realizado ou não realizado. | entrega.py:607-637; pmbok.py:592-597 | PMBOK 7 §2.6
- EN-29 ⚠ | Marcar um benefício como realizado ou parcial exige o resultado medido, mas só na edição. No cadastro dá para criar um benefício já "realizado" sem resultado. | entrega.py:656-658 vs :627-636 | convenção do app
- EN-30 | Alerta médio: benefício planejado ou parcial com data prevista vencida. | entrega.py:199, :230-232 | convenção do app
- EN-31 | Ao abrir um item a partir de uma mudança ou de um risco, o formulário já vem preenchido com o vínculo, o título ("Resposta ao risco R-n") e a descrição. | entrega.py:490-498 | PMBOK 7 §2.8.6 (backlog ajustado ao risco)

## 7. Medição (ME)

- ME-01 | Valor agregado pela regra 0/100: o item só agrega valor quando está concluído ou aceito. | medicao.py:79-89 | PMBOK 6 / outra fonte (Standard for EVM)
- ME-02 | O valor planejado (VP) cresce de forma linear pelos dias do item, contando início e fim: 0 antes do início, 100% no término. Itens sem data entram no orçamento total mas não no VP. | medicao.py:51-58, :86-87 | outra fonte (EVM)
- ME-03 | Os valores da linha de base (custo e datas) têm prioridade sobre os atuais do item. Só entram itens de trabalho com custo planejado. | medicao.py:61-76 | PMBOK 7 §2.7.2.3
- ME-04 | Fórmulas:
  - ONP (orçamento no término) = soma dos custos planejados;
  - VA = soma dos custos dos itens feitos;
  - CR = soma dos custos reais;
  - IDP = VA ÷ VP;
  - IDC = VA ÷ CR;
  - ENT = ONP ÷ IDC;
  - EPT = ENT − CR;
  - VNT = ONP − ENT;
  - IDPT = (ONP − VA) ÷ (ONP − CR), só quando ONP > CR;
  - variação de prazo = VA − VP; variação de custo = VA − CR. | medicao.py:85-97 | PMBOK 7 §2.7.2.3; siglas PT: outra fonte
- ME-05 ⚠ | O custo real (CR) soma todos os itens de trabalho, inclusive os sem custo planejado, enquanto VA e VP só usam os que têm. Isso distorce o IDC. | medicao.py:88-89 | convenção do app
- ME-06 | Limite de variação: padrão 10%, de 1% a 50%. | db.py:222; medicao.py:383 | convenção do app
- ME-07 | Faixas do semáforo por índice: verde (no rumo) se ≥ 1 − limite; amarelo (atenção) se ≥ 1 − 2 × limite; vermelho (crítico) abaixo; "sem dados" se não há índice. | medicao.py:224-229 | convenção do app (README)
- ME-08 | Semáforo de prazo, na ordem:
  - IDP, se existir;
  - senão, previsão de término × fim planejado: sem atraso = verde; atraso até limite% da duração planejada = amarelo; acima = vermelho;
  - senão, todo o escopo concluído = verde;
  - senão, "sem dados". | medicao.py:240-252 | convenção do app
- ME-09 | Semáforo de custo: pelo IDC; sem IDC, "sem dados". | medicao.py:255-258 | convenção do app
- ME-10 | Semáforo de escopo: sem itens = sem dados; scope creep (não adaptativo) = vermelho; adaptativo com backlog crescendo = amarelo; senão verde. | medicao.py:261-268 | convenção do app
- ME-11 | Semáforo de riscos: sem riscos ativos = sem dados; ameaça alta sem resposta ativa = vermelho; ameaça alta ou risco global alto = amarelo; senão verde. | medicao.py:271-278 | convenção do app
- ME-12 | Semáforo das partes interessadas, pela média da última satisfação de cada parte: ≥ 3,5 = verde; ≥ 2,5 = amarelo; abaixo = vermelho. | medicao.py:281-287 | convenção do app
- ME-13 ⚠ | Semáforo de questões: alguma atrasada = vermelho; alguma aberta = amarelo; senão verde. Mesmo sem nenhuma questão registrada aparece verde, nunca "sem dados" (diferente das outras dimensões). | medicao.py:290-292 | convenção do app
- ME-14 | Velocidade = média do concluído nas últimas 3 iterações encerradas. Conta o que foi concluído até o fim de cada iteração. | medicao.py:152-176 | PMBOK 7 §2.7.2
- ME-15 | Previsão de término:
  - com velocidade: iterações restantes = restante ÷ velocidade, arredondado para cima; data = hoje + iterações × duração média das iterações;
  - sem velocidade: usa a vazão dos últimos 30 dias (restante ÷ ritmo diário). | medicao.py:196-218 | PMBOK 7 §2.7.2.7
- ME-16 | Fluxo: lead time = conclusão − criação; cycle time = conclusão − início (itens dos últimos 90 dias); vazão = itens concluídos em 30 dias; WIP; fila. | medicao.py:179-193 | PMBOK 7 §2.7.2
- ME-17 | Burnup (escopo × concluído por semana) e burndown da iteração (linha ideal linear × restante). | medicao.py:129-145; metodos.py:104-126 | PMBOK 7 §2.7
- ME-18 | Indicador (KPI): o nome é obrigatório. Tipo: antecedente ou de resultado (padrão). Direção: maior ou menor é melhor (padrão: maior). Meta e limite podem ser negativos. Há 7 categorias. | medicao.py:406-417; pmbok.py:607-621 | PMBOK 7 §2.7.1-2.7.2
- ME-19 | Uma medição exige valor e não pode ter data futura. | medicao.py:450-457 | convenção do app
- ME-20 | Status do KPI pela última medição:
  - crítico se passou do limite (igual ao limite não é crítico);
  - ok se não tem meta ou atingiu a meta;
  - atenção caso contrário;
  - sem dados se não tem medição. | medicao.py:300-315 | convenção do app
- ME-21 | Tendência = comparação das duas últimas medições. "Piora seguida" = as duas últimas variações pioraram (precisa de pelo menos 3 medições). | medicao.py:316-320 | convenção do app
- ME-22 | Alerta alto: KPI passou do limite. | medicao.py:340-341 | convenção do app
- ME-23 | Alerta médio: indicador antecedente com piora seguida (só quando ainda não está crítico). | medicao.py:342-343 | PMBOK 7 §2.7.1
- ME-24 | Alerta informativo: indicador sem medição há mais de 30 dias. | medicao.py:23, :321, :344-345 | convenção do app
- ME-25 | Alerta alto: alguma dimensão do semáforo em vermelho e o projeto sem plano de exceção. | medicao.py:347-350 | convenção do app
- ME-26 | Relatório de status: data não futura. Congela o semáforo, o escopo, o valor agregado, a previsão, os 5 principais riscos ativos, as 5 principais questões abertas e até 8 alertas altos. | medicao.py:469-490, :514-519 | PMBOK 7 §4.6.7
- ME-27 | Sugestões do relatório: itens concluídos desde o último relatório; itens em andamento; os próximos 3 a fazer, pela ordem. | medicao.py:493-505 | convenção do app
- ME-28 ⚠ | Um relatório "congelado" pode ser excluído por qualquer usuário com acesso ao projeto. | medicao.py:541-545 | convenção do app
- ME-29 | Verificação de resultados dos 8 domínios (Tabelas 2-2 a 2-10): cada resultado é não avaliado, atendido, parcial ou não atendido. Progresso do domínio = (atendidos + 0,5 × parciais) ÷ total. | app.py:210-221, :507-518; pmbok.py:191-196 | PMBOK 7 Tabelas 2-2 a 2-10
- ME-30 ⚠ | Marcar um resultado de domínio como "atendido" não exige evidência. Já a conformidade exige (PR-12). | app.py:507-518 | convenção do app

## 8. Incerteza (IN)

- IN-01 | O título do risco é obrigatório. | incerteza.py:302, :352 | convenção do app
- IN-02 | Tipo do risco: ameaça (padrão) ou oportunidade. Tipo inválido vira ameaça. | incerteza.py:180; pmbok.py:397 | PMBOK 7 §2.8
- IN-03 | Estratégias por tipo:
  - ameaça: evitar, escalar, transferir, mitigar, aceitar;
  - oportunidade: explorar, escalar, compartilhar, melhorar, aceitar.

  Estratégia que não pertence ao tipo vira vazia. | pmbok.py:400-415; incerteza.py:181-183 | PMBOK 7 §2.8.5.1-2
- IN-04 | Fontes de risco: técnico, social, político, mercado, econômico, regulatório, organizacional, partes interessadas, equipe. | pmbok.py:419-423; incerteza.py:185 | PMBOK 7 Tabela 2-10
- IN-05 | Probabilidade e impacto vão de 1 a 5, garantido também pelo banco. Impacto em custo ≥ 0. Impacto em prazo e reserva em dias: de 0 a 100.000. Reserva em R$ ≥ 0. | incerteza.py:189-194; db.py:523-528 | convenção do app (escala)
- IN-06 | Pontuação = probabilidade × impacto. | incerteza.py:28 | PMBOK 7 §2.8
- IN-07 | Limite de risco: padrão 12, de 1 a 25. Cadência de revisão: padrão 14 dias, de 1 a 365. | db.py:16-17; incerteza.py:259-260 | PMBOK 7 §2.8.5; valores: convenção do app
- IN-08 | Nível do risco: pontuação ≥ limite = alto; pontuação × 2 ≥ limite = médio; senão baixo. | pmbok.py:443-451 | PMBOK 7 §2.8.5; faixas: convenção do app
- IN-09 | Conversão de probabilidade para o EMV: 1 = 10%, 2 = 30%, 3 = 50%, 4 = 70%, 5 = 90%. | pmbok.py:435-437 | convenção do app (README)
- IN-10 | EMV = probabilidade (%) × impacto em custo. É negativo para ameaça e positivo para oportunidade. Totais separados por tipo, só de riscos ativos. | incerteza.py:33-35, :81-82 | PMBOK 7 §2.8.5.3
- IN-11 | Status do risco: aberto, em resposta, ocorreu, encerrado. "Ativos" = aberto e em resposta. | pmbok.py:425-431 | convenção do app
- IN-12 ⚠ | Qualquer transição de status é permitida, e encerrar não pede nada. | incerteza.py:184, :380 | convenção do app
- IN-13 | Ao cadastrar, o risco ganha uma revisão "Identificação". Na edição, uma revisão é registrada quando probabilidade, impacto ou status mudam. A revisão explícita sempre registra e atualiza a data de revisão. | incerteza.py:239-244, :314, :362-363, :384 | PMBOK 7 §2.8.5.4
- IN-14 | Revisão atrasada = risco ativo cuja última revisão (ou identificação) tem mais dias que a cadência. | incerteza.py:36-38 | PMBOK 7 §2.8.5.4
- IN-15 | Quando um risco passa a "ocorreu", o app abre automaticamente uma questão, uma única vez por risco. Prioridade alta se for ameaça, média se for oportunidade. A descrição leva o plano de contingência. | incerteza.py:212-231 | PMBOK 7 §2.5 / §4.6.2
- IN-16 ⚠ | Também uma oportunidade que "ocorreu" vira questão (um problema), o que conceitualmente é discutível. | incerteza.py:222 | convenção do app
- IN-17 | No nível "rigoroso", risco com pontuação ≥ limite exige responsável e estratégia. | pmo.py:77-82 | convenção do app
- IN-18 | Reserva de contingência = soma das reservas em R$ e em dias das ameaças não encerradas. A reserva continua comprometida depois que o risco ocorre. | incerteza.py:83-86, :103 | PMBOK 7 §2.8.5.3 (README v3)
- IN-19 | Uso da contingência = reserva usada em questões ligadas a riscos. Uso da reserva de gerenciamento = reserva usada em questões sem risco. | incerteza.py:87-91 | PMBOK 7 §2.8.5.3
- IN-20 | Alerta alto: contingência usada acima da reservada. | incerteza.py:127-129 | convenção do app
- IN-21 | Alerta alto: reserva de gerenciamento usada acima da disponível (se não houver reserva definida, qualquer uso já dispara). | incerteza.py:130-132 | convenção do app
- IN-22 | Alerta alto: risco global avaliado como alto. A avaliação é baixo, médio ou alto. | incerteza.py:118-120; pmbok.py:439 | PMBOK 7 §2.8
- IN-23 | Alerta informativo: nenhum risco identificado. | incerteza.py:121-123 | convenção do app
- IN-24 | Alerta médio: risco "ocorreu" sem questão ligada. | incerteza.py:134-135 | convenção do app
- IN-25 | Alerta alto: ameaça ativa no nível alto sem estratégia. | incerteza.py:139-141 | convenção do app
- IN-26 | Alerta alto: ameaça ativa no nível alto com estratégia "aceitar" e sem plano de contingência (aceitação passiva). | incerteza.py:142-143 | PMBOK 7 §2.8.5.1
- IN-27 | Alerta médio: oportunidade ativa no nível alto sem estratégia. | incerteza.py:144-145 | convenção do app
- IN-28 | Alerta informativo: risco ativo sem probabilidade e impacto avaliados. | incerteza.py:146-147 | convenção do app
- IN-29 | Alerta médio: risco ativo sem responsável e sem parte interessada ligada. | incerteza.py:148-149 | convenção do app
- IN-30 | Alerta médio: revisão do risco atrasada. | incerteza.py:150-151 | convenção do app
- IN-31 ⚠ | "Reserva de contingência menor que o EMV das ameaças" está no README como alerta automático, mas só aparece como texto na tela do painel de Incerteza. Não entra nos pontos de atenção. | templates/incerteza_painel.html:63-65; README.md:97 | convenção do app
- IN-32 ⚠ | Um risco pode ser excluído sem restrição, mesmo depois de ocorrido ou com reserva usada. As questões ligadas perdem o vínculo. | incerteza.py:393-401 | convenção do app
- IN-33 | Outras incertezas: a natureza (geral, ambiguidade, complexidade, volatilidade) e a descrição são obrigatórias. Só valem as respostas da natureza escolhida. Status: aberta, reduzida ou resolvida. | incerteza.py:409-417, :438-447; pmbok.py:455-499 | PMBOK 7 §2.8.1-2.8.4
- IN-34 ⚠ | Pré-mortem: cada linha vira um risco "aberto" (até 30 riscos, títulos de até 300 caracteres). A fonte gravada é "Pré-mortem", que não está na lista oficial. Não passa pela revisão inicial nem pelo nível rigoroso. | metodos.py:175-186 | PMBOK 7 §4

## 9. Princípios (PR)

- PR-01 | Análise financeira do business case. Só calcula com investimento > 0, benefício anual informado e horizonte de 1 a 50 anos. Taxa ≥ 0%.
  - fluxo anual = benefício − custo anual;
  - VPL = −investimento + Σ fluxo ÷ (1 + taxa)^t;
  - ROI = (fluxo × anos − investimento) ÷ investimento, sem desconto;
  - payback simples = investimento ÷ fluxo (só com fluxo > 0);
  - viável quando VPL ≥ 0. | principios.py:40-55, :88 | PMBOK 7 princípio 4; fórmulas: convenção do app
- PR-02 ⚠ | Todo salvamento do business case marca "revisado hoje", mesmo sem nenhuma alteração. | principios.py:84 | convenção do app
- PR-03 | Custo previsto do projeto = ENT do valor agregado + reservas (contingência + gerenciamento). Sem ENT: custos planejados + reservas. | principios.py:58-72 | convenção do app
- PR-04 | Alerta alto: VPL negativo. | principios.py:492-494 | PMBOK 7 princípio 4
- PR-05 | Alerta alto: custo previsto acima do investimento do business case. | principios.py:495-498 | PMBOK 7 princípio 4
- PR-06 | Alerta informativo: business case sem revisão há mais de 90 dias. Só vale se ele já foi salvo alguma vez. | principios.py:21, :499-501 | convenção do app
- PR-07 | Conformidade: a área (uma de 8: legal, privacidade, segurança, financeira, ética, pessoas, ambiental, social) e o requisito são obrigatórios. | principios.py:119-124; pmbok.py:755-764 | PMBOK 7 §3.1
- PR-08 | Status da conformidade: pendente (padrão), em andamento, atendido ou não se aplica. | pmbok.py:765 | convenção do app
- PR-09 | Para marcar como "atendido" é preciso registrar a evidência. | principios.py:125-127 | PMBOK 7 §3.1 (README v7)
- PR-10 | Alerta alto: requisito pendente ou em andamento com prazo vencido. | principios.py:153, :502-504 | convenção do app
- PR-11 | Mudança organizacional: o grupo afetado é obrigatório. Impacto e prontidão de 1 a 5. Meta de adoção limitada a 100%. Status: não iniciado (padrão), preparando, em transição, adotado. | principios.py:206-216; pmbok.py:766 | PMBOK 7 princípio 12
- PR-12 | Medição de adoção: de 0 a 100%, obrigatória. Data não futura. A prontidão informada na medição atualiza a do grupo. | principios.py:193-201 | convenção do app
- PR-13 | Risco de resistência = impacto ≥ 4 e prontidão ≤ 2 (sem prontidão informada, conta como 5). Gera alerta médio. | principios.py:173, :505-508 | PMBOK 7 §3.12
- PR-14 | Alerta informativo: 4 ou mais grupos "preparando" ou "em transição" ao mesmo tempo (saturação de mudanças). | principios.py:509-512; templates/adocao.html:19 | PMBOK 7 §3.12
- PR-15 | O título da decisão é obrigatório. Data não futura. "Revisar em" opcional; decisão a revisar = data de revisão ≤ hoje (só exibida na tela). | principios.py:251-262, :291 | PMBOK 7 princípios 5 e 6
- PR-16 | A descrição da premissa é obrigatória. Status: não validada (padrão), validada, invalidada. Ao invalidar, o app avisa para avaliar se ela vira risco, questão ou mudança, mas não cria nada sozinho. | principios.py:266-283 | PMBOK 7 princípios 5 e 9
- PR-17 | Alerta médio: premissa não validada com "validar até" vencido. | principios.py:514-516 | convenção do app
- PR-18 | Autoavaliação: cada princípio tem de 5 a 6 evidências calculadas, com estes limiares:
  - analisadas ≥ 80%;
  - plano de engajamento ≥ 80%;
  - pelo menos metade das partes monitoradas;
  - itens com valor de negócio ≥ 80%;
  - premissas validadas ≥ 50%;
  - fatores de abordagem ≥ 10 de 15;
  - perguntas de tailoring ≥ 5;
  - itens a fazer bem documentados ≥ 70%;
  - defeitos resolvidos ≥ 80%;
  - acordo de trabalho ≥ 3 seções;
  - fatores de equipe com nota ≥ 3;
  - saúde da equipe avaliada nos últimos 45 dias;
  - business case revisado nos últimos 90 dias. | principios.py:303-472 | PMBOK 7 §3; limiares: convenção do app
- PR-19 | Nível do princípio: forte ≥ 80% das evidências; parcial ≥ 50%; fraco abaixo. | principios.py:476-478 | convenção do app (README)
- PR-20 | Alerta informativo: princípios fracos. Fica oculto até a fase Iniciar ter abordagem, propósito, objetivos e pelo menos uma parte. | principios.py:517-520; app.py:357-360 | convenção do app (README v10)
- PR-21 ⚠ | O status manual do princípio e a reflexão da equipe são independentes do nível calculado: dá para marcar "atendido" um princípio "fraco". | principios.py:524-543 | convenção do app

## 10. Aquisições e recursos físicos (AQ)

- AQ-01 | Aquisição: o item é obrigatório. Decisão: comprar (padrão) ou fazer. Status: planejada (padrão), em licitação, contratada, entregue, encerrada, cancelada. "Ativas" = planejada, em licitação e contratada. | suprimentos.py:148-156; pmbok.py:774-793 | PMBOK 7 §2.4.6, §2.5.6
- AQ-02 | Documento de licitação: nenhum, RFI, RFP ou RFQ. Contrato: preço fixo, custo reembolsável, tempo e material, IDIQ, outro. | pmbok.py:775-788 | PMBOK 7 §4.6.8
- AQ-03 | Compra externa marcada como contratada, entregue ou encerrada exige fornecedor. | suprimentos.py:157-158 | convenção do app
- AQ-04 | Encerrar uma aquisição exige avaliar o fornecedor (nota de 1 a 5; o banco também garante). | suprimentos.py:159-160; db.py:529-534 | PMBOK 7 §2.5.6
- AQ-05 | Valor da aquisição ≥ 0 (garantido pelo banco). | db.py:529-534 | convenção do app
- AQ-06 ⚠ | Fora a AQ-03 e a AQ-04, qualquer transição de status é permitida. A aquisição pode ser excluída sem restrição. | suprimentos.py:151, :179-181 | convenção do app
- AQ-07 | Alerta médio: compra externa planejada ou em licitação necessária em até 30 dias e ainda não contratada. Vira alerta alto se a data de necessidade já passou. | suprimentos.py:17, :49-51, :81-84 | convenção do app
- AQ-08 | Alerta alto: aquisição contratada com entrega prevista vencida. | suprimentos.py:52, :85-86 | convenção do app
- AQ-09 | Alerta alto: entrega prometida pelo fornecedor depois da data em que o projeto precisa (enquanto não estiver entregue, encerrada ou cancelada). | suprimentos.py:89-92 | convenção do app (AVALIACAO R8)
- AQ-10 | Alerta médio: fornecedor com nota ≤ 2 (aquisição não cancelada). | suprimentos.py:93-94 | convenção do app
- AQ-11 | Alerta informativo: compra contratada ou entregue cujo fornecedor ainda não é parte interessada. Há um botão que cadastra o fornecedor como parte (categoria Fornecedor, externa, ativa); exige o nome do fornecedor. | suprimentos.py:87-88, :182-190 | PMBOK 7 §2.5.6.2
- AQ-12 | Recurso físico: o nome é obrigatório. Tipo: material, equipamento (padrão), software, ambiente, outro. Status: planejado (padrão), pedido, recebido, em uso, devolvido. Antecedência de 0 a 730 dias. | suprimentos.py:192-204; pmbok.py:794-802 | PMBOK 7 §2.4.5, §2.5.5
- AQ-13 | O desperdício não pode passar do total usado. Quantidade e uso ≥ 0. O banco também garante. | suprimentos.py:196-199; db.py:547-552 | convenção do app (AVALIACAO R7)
- AQ-14 | Data para pedir = data de necessidade − antecedência. Alerta alto se o recurso planejado já passou dessa data. Alerta médio se faltam até 7 dias. | suprimentos.py:18, :65-68, :96-99 | convenção do app
- AQ-15 | Alerta médio: uso acima da quantidade planejada. | suprimentos.py:100-101 | convenção do app (AVALIACAO R7)
- AQ-16 | Percentual de desperdício = desperdício ÷ uso. Alerta informativo a partir de 15%. | suprimentos.py:69-70, :102-103 | convenção do app

## 11. PMO, revisão e permissões (PM)

- PM-01 | Com login obrigatório, o primeiro acesso cria o administrador; depois disso, a tela de primeiro acesso não funciona mais. | auth.py:87-105 | convenção do app (README v11)
- PM-02 | O login é único (sem diferenciar maiúsculas) e guardado em minúsculas. Nome e login são obrigatórios. Senha com pelo menos 8 caracteres. | auth.py:17, :38-43, :168-173; db.py:455 | convenção do app
- PM-03 | Bloqueio de 5 minutos depois de 5 tentativas erradas, contado por máquina (IP) e por conta. | auth.py:18-19, :115-128 | convenção do app
- PM-04 | A sessão expira depois de 12 horas sem uso, porque é renovada a cada página, e não tem limite total enquanto há uso (corrigido em 19/11/2026; antes dizia "a sessão dura 12 horas"). Trocar a senha encerra as outras sessões. Trocar a própria senha exige a senha atual. | app.py:69; auth.py:52-55, :145-153 | convenção do app
- PM-05 | Só o administrador cria usuários, redefine senhas e ativa ou desativa contas. Ninguém desativa a própria conta. | auth.py:161, :180-197 | convenção do app
- PM-06 ⚠ | O perfil de administrador só é escolhido ao criar o usuário; não há como promover ou rebaixar depois. | auth.py:175-176 | convenção do app
- PM-07 | O administrador vê todos os projetos. Os demais usuários veem só os projetos em que foram incluídos. Projeto sem acesso responde "não encontrado". | util.py:38-68 | convenção do app (README v14)
- PM-08 | Quem cria um projeto (não administrador) passa a ter acesso a ele automaticamente. | app.py:340-341 | convenção do app
- PM-09 | Só o administrador define a lista de acesso do projeto; administradores não entram nessa lista. | app.py:392-397 | convenção do app
- PM-10 ⚠ | Qualquer usuário que clicar em "Ver projeto de exemplo" ganha acesso ao projeto de exemplo que já existir, mesmo que tenha sido criado por outra pessoa. | app.py:289-300 | convenção do app
- PM-11 | Excluir um projeto: só administrador, e só marcando a confirmação. Vale também para projeto encerrado. | app.py:405-416, :111 | convenção do app (AVALIACAO R9)
- PM-12 | Backup, Dados/Lixeira/restauração, Revisões do PMO, Usuários, nível de exigência e anonimização: só administrador. | app.py:309; dados.py:32, :97, :107; pmo.py:128, :234 | convenção do app
- PM-13 ⚠ | O nível de exigência (essencial, que é o padrão, ou rigoroso) vale para todos os projetos de uma vez; não pode ser escolhido por projeto. | pmo.py:64-66; db.py:601 | convenção do app
- PM-14 | Regras extras do nível "rigoroso":
  - questão exige responsável e prazo;
  - risco alto exige responsável e estratégia;
  - mudança exige solicitante e justificativa;
  - item em andamento exige critérios de aceite;
  - parte interessada exige papel;
  - termo fora de rascunho exige patrocinador. | pmo.py:69-92 | convenção do app
- PM-15 | Completude de cada registro = campos preenchidos ÷ campos considerados (risco 8, questão 4, mudança 6, item 5, parte 8; atitude "desconhecida" conta como vazia). Cores da barra: 100% verde, ≥ 50% médio, abaixo baixo. | pmo.py:95-118; templates/_macros.html:123 | convenção do app
- PM-16 | Pedido de revisão do PMO: vale para termo, risco, mudança, item, relatório de status e questão. Só um pedido pendente por registro. | pmo.py:215-221 | convenção do app (README v14)
- PM-17 | O revisor (administrador) aprova ou devolve. Devolver exige comentário. | pmo.py:240-248 | convenção do app
- PM-18 ⚠ | A aprovação ou devolução do PMO é só informativa: não muda o status do registro nem impede que ele siga sem revisão. | pmo.py:245-247 | convenção do app
- PM-19 ⚠ | O pedido de revisão guarda o nome de quem pediu, não o identificador do usuário. A tela de pendências procura respostas por esse nome, o que falha se houver nomes repetidos ou se o nome mudar. | pmo.py:226, :203-205 | convenção do app
- PM-20 | Minhas pendências: questões não resolvidas, riscos ativos e itens a fazer, em andamento ou concluídos, só de projetos ativos. São "meus" quando o campo responsável bate com o nome, o login, o primeiro nome ou o nome do membro ligado ao usuário (ignorando o texto entre parênteses). | pmo.py:162-206 | convenção do app
- PM-21 | Portfólio: ativos primeiro, depois encerrados e cancelados; dentro de cada grupo, mais dimensões vermelhas, depois mais amarelas, depois nome. | pmo.py:156-157 | convenção do app
- PM-22 | A busca exige pelo menos 2 caracteres e respeita os projetos visíveis ao usuário. | pmo.py:303-304 | convenção do app
- PM-23 | Projeto encerrado ou cancelado fica só para consulta: qualquer gravação é bloqueada. As exceções são a tela de encerramento, a exclusão do projeto e a anonimização. | app.py:106-118 | convenção do app (AVALIACAO R1)
- PM-24 ⚠ | "Modo essencial" esconde 8 telas do menu (Fases, Tailoring, Custo da qualidade, Compras, Business case, Conformidade, Mudança organizacional, Decisões). É só preferência do navegador, não uma permissão: as telas continuam acessíveis. | static/app.js:104-116; templates/base.html:44-123 | convenção do app

## 12. Dados, auditoria e backup (DA)

- DA-01 | O histórico grava toda inclusão, alteração e exclusão em todas as tabelas, com quem, quando, o antes e o depois e o lote da operação. | auditoria.py:47-76 | convenção do app (README v13)
- DA-02 | O hash da senha nunca entra no histórico. Alteração só do "atualizado em" não é registrada. | auditoria.py:16-17, :73 | convenção do app
- DA-03 | O histórico do projeto pode ser consultado por qualquer usuário com acesso a ele (últimos 300 eventos). | dados.py:16-27 | convenção do app
- DA-04 | A lixeira restaura um projeto excluído inteiro (todo o lote) ou um registro avulso. Só o administrador restaura. | auditoria.py:129-137; dados.py:41-46 | convenção do app
- DA-05 | Usuários excluídos nunca são restaurados. Registros que já existem são ignorados. A restauração é desfeita se deixar algum registro sem o registro pai. | auditoria.py:146-160 | convenção do app
- DA-06 ⚠ | A confirmação de exclusão diz "não poderá ser recuperado", mas o administrador consegue restaurar pela Lixeira. | static/app.js:192; app.py:415 | convenção do app
- DA-07 | Backup automático: no máximo um a cada 20 horas, checado no máximo uma vez por hora. Também há backup antes de cada migração, antes de cada restauração e o manual. | backup.py:119-124; app.py:554-567; db.py:673-674 | convenção do app
- DA-08 | Não se faz backup de banco sem projetos, exceto o manual. | backup.py:70-73 | convenção do app
- DA-09 | Cada backup passa pela verificação de integridade e recebe uma assinatura SHA-256. Restaurar recusa arquivo que não é SQLite, que está corrompido, que não é do Octante, cuja assinatura não confere ou que vem de uma versão mais nova do app. | backup.py:35-61, :81-87 | convenção do app
- DA-10 | Ficam guardados os 14 backups automáticos mais recentes e os 5 mais recentes de cada outro motivo. | backup.py:17-18, :107-116 | convenção do app
- DA-11 | Upload de backup de até 60 MB. Campo de formulário de até 20.000 caracteres. | seguranca.py:10, :28, :35-37 | convenção do app
- DA-12 | Anonimização (LGPD): só administrador, só para projeto encerrado ou cancelado. Apaga contato, crenças e expectativas das partes interessadas. | dados.py:104-117 | convenção do app (README v13)
- DA-13 ⚠ | A anonimização deixa intactos o resumo e o feedback das interações e o histórico de alterações (que guarda os valores antigos). A Lixeira também pode trazer os dados de volta. | dados.py:113-114; auditoria.py:72-75 | convenção do app
- DA-14 | Exportar para Excel/CSV: riscos, questões, mudanças, partes, backlog e lições. Células que começam com =, +, −, @, tab ou retorno ganham um apóstrofo (proteção contra injeção de fórmulas). | pmo.py:387-449 | convenção do app
- DA-15 | Validações também dentro do banco: probabilidade e impacto de 1 a 5; aquisição com valor ≥ 0 e nota de 1 a 5; item com estimativa e custos ≥ 0 e valor de 1 a 5; iteração com fim ≥ início e capacidade ≥ 0; recurso com quantidade e uso ≥ 0 e desperdício ≤ uso; usuário com admin e ativo em 0/1 e hash de senha válido. | db.py:523-558 | convenção do app
- DA-16 | O app trabalha no fuso de Brasília (America/Sao_Paulo), mesmo em servidor UTC. | seguranca.py:14-18 | convenção do app

## 13. Guia e ensino (GU)

- GU-01 | Fluxo do projeto em 5 fases:
  - Iniciar: abordagem, termo aprovado, partes;
  - Planejar: equipe, escopo, riscos, prazo e orçamento, compras (opcional);
  - Executar: quadro, engajamento, questões e mudanças (opcional);
  - Acompanhar: acompanhamento, checklist dos domínios, princípios;
  - Encerrar: lições, encerramento. | guia.py:11-50 | convenção do app (README v9/v10)
- GU-02 | A etapa "Iniciar" só conta como concluída com o termo aprovado; termo em revisão não basta. | guia.py:26 | convenção do app (AVALIACAO R3)
- GU-03 ⚠ | A etapa "Prazo e orçamento" só conta como concluída com pelo menos uma iteração. Projeto preditivo que só usa datas e custos por item nunca a conclui. | guia.py:33 | convenção do app
- GU-04 | Próximo passo = a primeira etapa obrigatória ainda não feita. Uma fase está completa quando todas as etapas obrigatórias estão feitas. | guia.py:51-60 | convenção do app
- GU-05 | Os painéis completos da visão geral aparecem quando a fase Iniciar tem abordagem, propósito, objetivos e pelo menos uma parte (o termo pode estar em revisão). | app.py:356-360 | convenção do app (README v10)
- GU-06 | Projeto novo abre direto no fluxo; o projeto de exemplo é reaproveitado se já existir. | app.py:289-304, :343-344 | convenção do app
- GU-07 | Glossário de 30 termos e ajuda "Para que serve / O que fazer" em cada tela. São textos de ensino, sem efeito nos dados. | guia.py:64-146 | convenção do app
- GU-08 | Sugestões de tailoring por abordagem para abertura, incerteza, monitoramento, mudanças, entrega, cronograma e medição. São textos de orientação. | pmbok.py:273-289, :541-543, :599-601, :645-650 | PMBOK 7 §2.8.6 e outras

## 14. Encerramento (EC)

- EC-01 | Situação do projeto: ativo (padrão), encerrado ou cancelado. | db.py:267; pmbok.py:748 | convenção do app
- EC-02 | Checklist automático com 11 verificações:
  - entregas aceitas ou canceladas;
  - mudanças decididas e implementadas ("aprovada" ainda conta como pendente);
  - questões resolvidas;
  - riscos encerrados ("ocorreu" conta como aberto);
  - nenhum benefício só "planejado" (parcial é aceito);
  - pelo menos uma lição;
  - fases concluídas (a fase chamada "Encerramento" não entra);
  - aquisições não ativas;
  - conformidade sem pendente ou em andamento;
  - todos os grupos de mudança organizacional "adotados";
  - nenhum membro ativo. | ciclo.py:231-267 | PMBOK 7 §2.3.5 / §4.6
- EC-03 | Checklist manual com 4 itens: contratos encerrados, conhecimento arquivado, transição para a operação, termo e business case revisados. | ciclo.py:268-273, :298 | convenção do app
- EC-04 | Comparação com o planejado: escopo total × aceito, orçamento (ONP) × custo real, fim planejado. | ciclo.py:274-282 | convenção do app
- EC-05 | Encerrar ou cancelar exige a avaliação dos objetivos e benefícios em relação ao termo de abertura. | ciclo.py:311-312 | convenção do app
- EC-06 | Cancelar exige justificativa. | ciclo.py:309-310 | convenção do app
- EC-07 | Encerrar com pendências no checklist (automático ou manual) exige justificativa. Sem pendências, não exige. | ciclo.py:313-315 | convenção do app
- EC-08 | Ao encerrar ou cancelar, o app grava a situação, a data de encerramento e o estágio da equipe "dissolução". | ciclo.py:316-320 | convenção do app
- EC-09 ⚠ | Reabrir um projeto não exige justificativa nem administrador: qualquer usuário com acesso reabre, e depois pode editar tudo. Isso contrasta com a trava de somente leitura (PM-23). | ciclo.py:294-296 | convenção do app
- EC-10 ⚠ | A tela de encerramento escapa da trava de somente leitura, então a avaliação final e o checklist manual de um projeto encerrado continuam editáveis. | app.py:111; ciclo.py:297-303 | convenção do app
- EC-11 | As lições com alcance "outras equipes" ou "organização" aparecem destacadas no encerramento. | ciclo.py:326 | PMBOK 7 §2.5.8.1

---

## Destaques das ⚠ (as mais relevantes para o dono do produto)

1. **A trilha de auditoria das mudanças pode ser contornada.** O fluxo de status das mudanças não é obrigatório, então uma mudança aprovada pode voltar a "solicitada" e ser excluída (TR-18, TR-20).
2. **Regras que só valem na edição, não no cadastro:**
   - resolução da questão (TR-05);
   - resultado do benefício (EN-29);
   - nome duplicado da parte interessada (PI-03);
   - nível rigoroso da mudança (TR-22).
3. **Regras descritas como obrigatórias que só geram alerta:** RACI com 1 A e pelo menos 1 R (EQ-11); limite de WIP (EN-20).
4. **Regras que só aparecem numa tela, fora dos pontos de atenção:** EMV × reserva de contingência (IN-31, citado no README como alerta); capacidade da iteração e item com término vencido (PL-18); conflitos de dependência no Gantt (PL-20).
5. **Defeito na agenda:** as premissas nunca aparecem atrasadas (PL-22).
6. **A anonimização LGPD não é completa:** o histórico e a Lixeira guardam os dados antigos (DA-13).
7. **Encerramento:** qualquer usuário reabre o projeto sem justificativa (EC-09). A tela de encerramento continua editável num projeto encerrado (EC-10).
8. **Exclusões sem restrição em registros importantes:** itens aceitos (EN-14), riscos ocorridos (IN-32), relatórios congelados (ME-28), fases concluídas (AB-18).
9. **Valores fora das listas oficiais:** a cadência não é conferida pelo servidor (AB-02); as fontes de risco dos modelos e do pré-mortem não estão na lista (AB-09, IN-34).

## Contagem por domínio

| Domínio | Regras | Com ⚠ |
|---|---|---|
| Partes interessadas (PI) | 33 | 2 |
| Equipe (EQ) | 20 | 1 |
| Abordagem, ciclo de vida e tailoring (AB) | 25 | 4 |
| Planejamento (PL) | 23 | 6 |
| Trabalho (TR) | 29 | 5 |
| Entrega (EN) | 31 | 4 |
| Medição (ME) | 30 | 4 |
| Incerteza (IN) | 34 | 5 |
| Princípios (PR) | 21 | 2 |
| Aquisições e recursos (AQ) | 16 | 1 |
| PMO, revisão e permissões (PM) | 24 | 6 |
| Dados, auditoria e backup (DA) | 16 | 2 |
| Guia e ensino (GU) | 8 | 1 |
| Encerramento (EC) | 11 | 2 |
| **Total** | **321** | **45** |
