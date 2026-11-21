# Requisitos funcionais: regras e decisões

Esta tabela acompanha o [resumo para confirmação](resumo-para-confirmacao.md), como decidido na Q209. Para cada requisito funcional do [inventário](inventario-requisitos-prototipo.md), ela mostra as regras de negócio que a tela aplica ou mostra, as decisões da elicitação que mudam o requisito e como ele entra na ERS.

**Como ler:**
- **Regras:** as do [inventário de regras](inventario-regras-prototipo.md) do mesmo domínio que o código da tela usa: a rota, as funções que ela chama, os templates e as listas do `pmbok.py`. A ligação foi feita pelo código do protótipo e conferida domínio por domínio. Os alertas ficam fora desta coluna e estão na seção 5 do resumo.
- **Decisões que mudam:** as perguntas do [registro de decisões](decisoes-elicitacao.md) que alteram uma dessas regras ("Muda" ou "Sai" na [origem das regras](origem-das-regras.md)) ou o próprio requisito, como as de papéis, revisão, LGPD e não funcionais. O detalhe de cada mudança está na pergunta citada.
- **Na ERS**, nos termos da Q6: **confirmado** (entra como está), **alterado** (entra reescrito pelas decisões) ou **descartado**.

## Projetos e portfólio (PJ)

| RF | O que faz no protótipo | Regras | Decisões que mudam | Na ERS |
|---|---|---|---|---|
| RF-PJ-01 | Listar os projetos visíveis, do mais recente ao mais antigo, com o número de partes ativas | AB-01, PM-07 | Q9, Q27, Q35, Q43 | Alterado |
| RF-PJ-02 | Criar projeto com nome, descrição, cadência e modelo (em branco, Scrum, híbrido, preditivo) | AB-02, AB-08, AB-09, AB-10, GU-06, PM-08, PM-15 | Q27, Q56, Q114, Q122, Q127, Q128 | Alterado |
| RF-PJ-03 | Visão geral: trilha das 5 fases, próximo passo, semáforo, pontos de atenção, resumos, progresso dos domínios e princípios | AB-01, AB-09, AB-10, AB-11, AB-12, AB-22, GU-02, GU-03, GU-04, GU-05, PM-07, PM-15 | Q9, Q27, Q35, Q43, Q56, Q127, Q128, Q149, Q150, Q179 | Alterado |
| RF-PJ-04 | Editar nome, descrição e cadência | AB-02, PM-07, PM-09, PM-15 | Q9, Q27, Q35, Q43, Q56, Q122 | Alterado |
| RF-PJ-05 | Definir quais usuários (não administradores) acessam o projeto | AB-02, PM-07, PM-09, PM-15 | Q9, Q27, Q35, Q43, Q56, Q122 | Alterado: quem escolhe os gerentes do projeto é o supervisor designado, e o acesso de consulta também é dele (Q27 e Q43) |
| RF-PJ-06 | Excluir projeto com confirmação; vai para a lixeira | DA-06, PM-07, PM-11 | Q9, Q27, Q35, Q43, Q51, Q54, Q198 | Alterado |
| RF-PJ-07 | Portfólio com semáforo, fase, próxima etapa, críticos, atenções e revisões pendentes, por criticidade | AB-01, GU-02, GU-03, GU-04, PM-07, PM-13, PM-21 | Q9, Q17, Q27, Q35, Q36, Q43, Q150, Q183, Q184, Q193, Q195, Q203 | Alterado |
| RF-PJ-08 | Checklist dos 8 domínios com progresso | PM-07 | Q9, Q27, Q35, Q43, Q174a | Alterado |
| RF-PJ-09 | Verificação dos resultados de um domínio (Tabelas 2-2 a 2-10) com indicadores | AB-01, AB-02, AB-03, GU-02, GU-04, GU-05, PM-07 | Q9, Q27, Q35, Q43, Q92, Q122, Q174a | Alterado |

## Partes interessadas (PI)

| RF | O que faz no protótipo | Regras | Decisões que mudam | Na ERS |
|---|---|---|---|---|
| RF-PI-01 | Registro das partes e resumo do ciclo de 5 etapas | PI-06, PI-08, PI-10, PI-11, PI-13, PI-16, PI-17, PI-18, PI-23, PI-24 | Q104, Q105b, Q106b, Q169a, Q170 | Alterado |
| RF-PI-02 | Cadastrar parte ("salvar e cadastrar outra") | PI-01, PI-02, PI-04, PI-05, PI-06, PI-07, PI-08, PI-09, PI-13, PI-16, PI-19, PI-20 | Q41, Q104, Q105b, Q106b, Q169a, Q170 | Alterado |
| RF-PI-03 | Detalhe da parte: interações, histórico de engajamento, riscos ligados | PI-08, PI-09, PI-10, PI-11, PI-13, PI-16, PI-17, PI-18, PI-23 | Q104, Q105b, Q106b, Q169a | Alterado |
| RF-PI-04 | Editar a parte | PI-01, PI-03, PI-04, PI-06, PI-07, PI-08, PI-09, PI-13, PI-16, PI-19, PI-20 | Q41, Q104, Q105b, Q106b, Q111, Q169a, Q170 | Alterado |
| RF-PI-05 | Excluir a parte — não confere o acesso ao projeto | PI-31 | Q110, Q198 | Alterado: correção da issue #2 |
| RF-PI-06 | Análise em lote: poder, interesse, influência, impacto, atitude, saliência | PI-07, PI-08, PI-10, PI-11, PI-13, PI-16, PI-17, PI-18, PI-23, PI-24 | Q104, Q105b, Q106b, Q107b, Q169a | Alterado |
| RF-PI-07 | Priorização: grade poder × interesse, ordem sugerida, manual ou limpar | PI-07, PI-08, PI-10, PI-11, PI-13, PI-14, PI-16, PI-17, PI-18, PI-23, PI-24 | Q105b, Q106b, Q169a | Alterado |
| RF-PI-08 | Engajamento: matriz atual × desejado e plano de comunicação | PI-07, PI-08, PI-10, PI-11, PI-13, PI-16, PI-17, PI-18, PI-19, PI-20, PI-23, PI-24 | Q105b, Q106b, Q169a | Alterado |
| RF-PI-09 | Monitoramento: registrar interação, últimas 50, mudanças de nível, alertas | PI-04, PI-07, PI-08, PI-13, PI-16, PI-21, PI-22, PI-23, PI-26, PI-28, PI-29 | Q105b, Q106b, Q108, Q163, Q164, Q169a | Alterado |
| RF-PI-10 | Excluir interação — não confere o acesso ao projeto | PI-32 | Q198 | Alterado: correção da issue #2 |

## Equipe (EQ)

| RF | O que faz no protótipo | Regras | Decisões que mudam | Na ERS |
|---|---|---|---|---|
| RF-EQ-01 | Listar e cadastrar membros (papel, dedicação, local, habilidades, lacunas, plano, motivador, parte e usuário ligados) | EQ-01, EQ-02, EQ-03, EQ-04, EQ-05, EQ-08, EQ-11, EQ-12, EQ-13, EQ-15, EQ-16 | Q114, Q116, Q117, Q119, Q165 | Alterado |
| RF-EQ-02 | Modelo de liderança e estágio de Tuckman | EQ-01, EQ-02, EQ-03, EQ-04, EQ-05, EQ-08, EQ-11, EQ-12, EQ-13, EQ-15, EQ-16 | Q116, Q117, Q120, Q165 | Alterado |
| RF-EQ-03 | Ver e editar membro com seus papéis RACI | EQ-01, EQ-02, EQ-03, EQ-06, EQ-07 | Q115, Q119 | Alterado |
| RF-EQ-04 | Liberar ou reativar membro | EQ-01, EQ-02, EQ-03, EQ-06, EQ-07 | Q115 | Alterado |
| RF-EQ-05 | Excluir membro | EQ-01, EQ-02, EQ-03, EQ-06, EQ-07 | Q115, Q198 | Alterado |
| RF-EQ-06 | Acordo de trabalho em 5 seções | EQ-08 | Q116 | Alterado |
| RF-EQ-07 | Matriz RACI: adicionar linha, atribuir R/A/C/I, remover linha | EQ-09, EQ-10, EQ-11 | Q117, Q118, Q121, Q198 | Alterado |
| RF-EQ-08 | Saúde da equipe: 9 fatores, histórico, gráfico, excluir avaliação | EQ-12, EQ-13 | Q174a, Q198 | Alterado |

## Abordagem, ciclo de vida e tailoring (AB)

| RF | O que faz no protótipo | Regras | Decisões que mudam | Na ERS |
|---|---|---|---|---|
| RF-AB-01 | Assistente com 15 fatores: sugestão, escolha, justificativa, cadência | AB-01, AB-02, AB-03, AB-04, AB-05 | Q33, Q122, Q123, Q136 | Alterado |
| RF-AB-02 | Ver fases, aplicar as sugeridas, criar fase | AB-01, AB-10, AB-11, AB-12, AB-14 | Q128, Q129 | Alterado |
| RF-AB-03 | Editar fase e fazer revisão de fase para concluí-la | AB-12, AB-13, AB-14, AB-15, AB-16, AB-17, AB-18, AB-19 | Q129, Q130, Q131, Q132, Q137, Q179 | Alterado |
| RF-AB-04 | Excluir fase | AB-12, AB-13, AB-14, AB-15, AB-16, AB-17, AB-18, AB-19 | Q129, Q130, Q131, Q132, Q198 | Alterado |
| RF-AB-05 | Responder às 15 perguntas de tailoring | AB-23, AB-24 | Q33, Q133 | Alterado |
| RF-AB-06 | Registrar e excluir decisões de tailoring | AB-23, AB-24 | Q133, Q198 | Alterado |
| RF-AB-07 | Diagnóstico da Tabela 3-1 calculado dos dados | AB-23, AB-24 | Q133, Q134, Q180 | Alterado |

## Planejamento (PL)

| RF | O que faz no protótipo | Regras | Decisões que mudam | Na ERS |
|---|---|---|---|---|
| RF-PL-01 | Termo de abertura: campos e status (rascunho, em revisão, aprovado) | PL-04, PL-05, PL-06, PL-07, PL-08, PL-09 | Q10, Q14, Q15, Q60, Q61, Q62, Q66, Q69, Q109, Q112, Q177 | Alterado |
| RF-PL-02 | Declaração de visão com texto gerado | PL-04, PL-05, PL-06, PL-07, PL-08, PL-09 | Q14, Q15, Q61, Q62, Q66, Q109, Q112 | Alterado: a visão passa a ser texto livre, sem o gerador (Q66) |
| RF-PL-03 | Datas de início e fim planejado | PL-13, PL-14, PL-15, PL-16, PL-17, PL-18 | Q67, Q158 | Alterado |
| RF-PL-04 | Criar iteração (nome, datas, meta, capacidade) | PL-13, PL-14, PL-15, PL-16, PL-17, PL-18 | Q67, Q158 | Alterado |
| RF-PL-05 | Excluir iteração (itens voltam ao backlog) | PL-13, PL-14, PL-15, PL-16, PL-17, PL-18 | Q67, Q158, Q198 | Alterado |
| RF-PL-06 | Planejar itens em lote e ver totais e velocidade | PL-13, PL-14, PL-15, PL-16, PL-17, PL-18 | Q67, Q158 | Alterado |

## Trabalho do projeto (TR)

| RF | O que faz no protótipo | Regras | Decisões que mudam | Na ERS |
|---|---|---|---|---|
| RF-TR-01 | Painel: resumo, questões, mudanças, lições, alertas | TR-07, TR-09, TR-12, TR-14 | Q72, Q112, Q167 | Alterado |
| RF-TR-02 | Listar questões com filtro | TR-07 | — | Confirmado |
| RF-TR-03 | Registrar questão | TR-01, TR-02, TR-03, TR-05 | Q74, Q75 | Alterado |
| RF-TR-04 | Editar questão, resolver, registrar consumo de reserva, ver lições | TR-01, TR-02, TR-03, TR-04, TR-06, TR-07, TR-11, TR-26, TR-27, TR-28, TR-29 | Q73, Q74, Q75, Q112, Q168 | Alterado |
| RF-TR-05 | Excluir questão | TR-01, TR-02, TR-03, TR-04, TR-06, TR-07, TR-11, TR-27 | Q73, Q74, Q75, Q112, Q168, Q198 | Alterado |
| RF-TR-06 | Listar mudanças e mudanças por parte | TR-14, TR-16 | Q70, Q71, Q72, Q112 | Alterado |
| RF-TR-07 | Registrar mudança | TR-13, TR-14, TR-15, TR-16, TR-17, TR-21, TR-22 | Q10, Q69, Q70, Q71, Q72, Q112, Q176 | Alterado |
| RF-TR-08 | Editar mudança: 6 impactos, decisão, quem decidiu, comunicada, itens | TR-13, TR-14, TR-15, TR-16, TR-17, TR-19, TR-20, TR-21, TR-22 | Q69, Q70, Q71, Q72, Q73b, Q112, Q176 | Alterado |
| RF-TR-09 | Excluir mudança pendente ou rejeitada | TR-13, TR-14, TR-15, TR-16, TR-17, TR-19, TR-20, TR-21, TR-22 | Q69, Q70, Q71, Q72, Q73b, Q112, Q176, Q198 | Alterado |
| RF-TR-10 | Lições aprendidas: listar e registrar | TR-26, TR-27, TR-28, TR-29 | Q73, Q75 | Alterado |
| RF-TR-11 | Marcar lição como aplicada | TR-26, TR-27, TR-28, TR-29 | Q73, Q75 | Alterado |
| RF-TR-12 | Excluir lição | TR-26, TR-27, TR-28, TR-29 | Q73, Q75, Q198 | Alterado |

## Entrega (EN)

| RF | O que faz no protótipo | Regras | Decisões que mudam | Na ERS |
|---|---|---|---|---|
| RF-EN-01 | Painel: definição de pronto, unidade de estimativa, limite de WIP, alertas | EN-02, EN-05, EN-07, EN-15, EN-16, EN-19, EN-20, EN-23, EN-25, EN-27 | Q80, Q83, Q155, Q156, Q159 | Alterado |
| RF-EN-02 | Definir ou refazer a linha de base do escopo | EN-02, EN-07, EN-15, EN-16, EN-17 | Q79, Q80 | Alterado |
| RF-EN-03 | Escopo e backlog em árvore, itens fora da linha de base | EN-02, EN-07, EN-15, EN-16 | Q80, Q84b | Alterado |
| RF-EN-04 | Salvar ordem de prioridade | — | — | Confirmado |
| RF-EN-05 | Criar item (também a partir de mudança ou risco) | EN-01, EN-02, EN-03, EN-04, EN-07, EN-08, EN-09, EN-10, EN-12, EN-31 | Q80, Q82 | Alterado |
| RF-EN-06 | Editar, concluir e aceitar item | EN-01, EN-02, EN-03, EN-04, EN-07, EN-08, EN-09, EN-10, EN-12, EN-14 | Q80, Q81, Q82, Q84 | Alterado |
| RF-EN-07 | Excluir item | EN-01, EN-02, EN-03, EN-04, EN-07, EN-08, EN-09, EN-10, EN-12, EN-14 | Q80, Q81, Q82, Q198 | Alterado |
| RF-EN-08 | Quadro de tarefas com 4 colunas | EN-02, EN-07, EN-08, EN-09, EN-10, EN-12, EN-13, EN-15, EN-16 | Q80, Q82, Q83 | Alterado |
| RF-EN-09 | Custo da qualidade | EN-02, EN-07, EN-25, EN-26 | Q80 | Alterado |
| RF-EN-10 | Registrar e listar benefícios | EN-28, EN-29 | Q85 | Alterado |
| RF-EN-11 | Editar ou excluir benefício | EN-28, EN-29 | Q85, Q198 | Alterado |

## Medição (ME)

| RF | O que faz no protótipo | Regras | Decisões que mudam | Na ERS |
|---|---|---|---|---|
| RF-ME-01 | Painel: semáforo, valor agregado, burnup, velocidade, fluxo, previsão, limite de variação, plano de exceção | ME-01, ME-02, ME-03, ME-05, ME-06, ME-07, ME-09, ME-10, ME-11, ME-12, ME-13, ME-14, ME-16, ME-17, ME-21 | Q87, Q88, Q90, Q174b, Q177 | Alterado |
| RF-ME-02 | Criar indicador (KPI) e ver histórico | ME-18, ME-21 | Q93 | Alterado |
| RF-ME-03 | Registrar e excluir medição; excluir indicador | ME-19 | Q198 | Alterado |
| RF-ME-04 | Emitir relatório de status que congela os números do dia | ME-01, ME-02, ME-05, ME-07, ME-09, ME-11, ME-12, ME-26, ME-27 | Q10, Q16, Q37, Q87, Q89, Q91, Q104 | Alterado |
| RF-ME-05 | Ver, imprimir/PDF e excluir relatório | ME-28 | Q11, Q91, Q198 | Alterado |

## Incerteza (IN)

| RF | O que faz no protótipo | Regras | Decisões que mudam | Na ERS |
|---|---|---|---|---|
| RF-IN-01 | Painel: matrizes P×I, EMV e reservas, limite, cadência de revisão, apetite, risco global | IN-02, IN-04, IN-07, IN-08, IN-10, IN-11, IN-18, IN-19, IN-24, IN-31 | Q95, Q97, Q103, Q160, Q162, Q172a, Q172b, Q177 | Alterado |
| RF-IN-02 | Listar riscos com filtros | IN-02, IN-04, IN-06, IN-08, IN-09, IN-10, IN-11, IN-14 | Q97, Q103 | Alterado |
| RF-IN-03 | Registrar risco | IN-01, IN-02, IN-04, IN-05, IN-09, IN-11, IN-12, IN-13, IN-15, IN-16, IN-17 | Q97, Q98, Q103, Q166b | Alterado |
| RF-IN-04 | Detalhe do risco: revisões, tendência, ligações | IN-02, IN-04, IN-06, IN-08, IN-09, IN-10, IN-11, IN-14 | Q97, Q103 | Alterado |
| RF-IN-05 | Editar risco | IN-01, IN-02, IN-04, IN-05, IN-06, IN-08, IN-09, IN-10, IN-11, IN-12, IN-13, IN-14, IN-15, IN-16, IN-17 | Q97, Q98, Q100, Q101, Q103, Q166b, Q173 | Alterado |
| RF-IN-06 | Registrar revisão do risco | IN-06, IN-08, IN-09, IN-10, IN-11, IN-12, IN-13, IN-14, IN-15, IN-16 | Q97, Q98 | Alterado |
| RF-IN-07 | Excluir risco | IN-06, IN-08, IN-09, IN-10, IN-11, IN-14, IN-32 | Q97, Q99, Q198 | Alterado |
| RF-IN-08 | Registrar ambiguidade, complexidade ou volatilidade | IN-33 | — | Confirmado |
| RF-IN-09 | Atualizar ou excluir essa incerteza | IN-33 | Q198 | Alterado |

## Princípios (PR)

| RF | O que faz no protótipo | Regras | Decisões que mudam | Na ERS |
|---|---|---|---|---|
| RF-PR-01 | Autoavaliação dos 12 princípios | PR-03, PR-19, PR-21 | Q143 | Alterado |
| RF-PR-02 | Business case: VPL, ROI, payback, gráfico | PR-02, PR-03 | Q138, Q139, Q181, Q182 | Alterado |
| RF-PR-03 | Conformidade e sustentabilidade | PR-07, PR-08, PR-09 | Q144, Q176 | Alterado |
| RF-PR-04 | Mudança organizacional: estados, grupos, adoção | PR-11, PR-12 | Q140 | Alterado |
| RF-PR-05 | Registrar e excluir decisões | PR-15 | Q142, Q198 | Alterado |
| RF-PR-06 | Premissas | PR-15, PR-16 | Q141, Q142, Q198 | Alterado |

## Aquisições e recursos (AQ)

| RF | O que faz no protótipo | Regras | Decisões que mudam | Na ERS |
|---|---|---|---|---|
| RF-AQ-01 | Painel "Compras e recursos" | AQ-01, AQ-02, AQ-03, AQ-04, AQ-06, AQ-11, AQ-13, AQ-14 | Q145, Q146, Q147, Q148, Q175 | Alterado |
| RF-AQ-02 | Registrar ou editar aquisição | AQ-01, AQ-02, AQ-03, AQ-04, AQ-06, AQ-11, AQ-13, AQ-14 | Q145, Q146, Q147, Q148, Q175 | Alterado |
| RF-AQ-03 | Excluir aquisição | AQ-01, AQ-02, AQ-03, AQ-04, AQ-06, AQ-11, AQ-13, AQ-14 | Q145, Q146, Q147, Q148, Q175, Q198 | Alterado |
| RF-AQ-04 | Cadastrar fornecedor como parte interessada | AQ-01, AQ-02, AQ-03, AQ-04, AQ-06, AQ-11, AQ-13, AQ-14 | Q145, Q146, Q147, Q148, Q175 | Descartado: o fornecedor contratado entra sozinho como parte interessada, e o botão sai (Q147) |
| RF-AQ-05 | Registrar ou editar recurso físico | AQ-12, AQ-13, AQ-14 | Q148 | Alterado |
| RF-AQ-06 | Excluir recurso físico | AQ-12, AQ-13, AQ-14 | Q148, Q198 | Alterado |

## Métodos (MT)

| RF | O que faz no protótipo | Regras | Decisões que mudam | Na ERS |
|---|---|---|---|---|
| RF-MT-01 | MoSCoW no item | — | — | Confirmado |
| RF-MT-02 | Dependências entre itens, ciclos recusados | PL-19 | — | Confirmado |
| RF-MT-03 | Gantt | EN-02, EN-07, EN-15, EN-16, PL-20 | Q67, Q80, Q158 | Alterado |
| RF-MT-04 | Burndown | EN-07, EN-15, ME-17 | Q80 | Alterado |
| RF-MT-05 | Cynefin e Stacey | AB-06, AB-07 | Q125, Q126 | Alterado |
| RF-MT-06 | Pré-mortem (cada linha vira risco) | IN-34 | Q102 | Descartado: o pré-mortem sai (Q102) |

## PMO (PM)

| RF | O que faz no protótipo | Regras | Decisões que mudam | Na ERS |
|---|---|---|---|---|
| RF-PM-01 | Minhas pendências | PM-07, PM-12, PM-17, PM-18, PM-19, PM-20 | Q9, Q10, Q14, Q17, Q22, Q27, Q35, Q43, Q51, Q55 | Alterado |
| RF-PM-02 | Pedir revisão do PMO | PM-07, PM-16, PM-19 | Q9, Q10, Q14, Q27, Q35, Q43, Q51, Q56 | Alterado |
| RF-PM-03 | Revisar: aprovar ou devolver com comentário | PM-12, PM-17, PM-18 | Q8, Q9, Q10, Q14, Q15, Q17, Q22 | Alterado |
| RF-PM-04 | Busca global | PM-07, PM-22 | Q9, Q27, Q35, Q43 | Alterado |
| RF-PM-05 | Agenda de prazos | PM-07 | Q9, Q27, Q35, Q43, Q67 | Alterado |
| RF-PM-06 | Exportar agenda (.ics) | PM-07 | Q9, Q27, Q35, Q43 | Alterado |
| RF-PM-07 | Exportar registros para Excel/CSV | PM-07 | Q9, Q27, Q35, Q43, Q104, Q119 | Alterado |
| RF-PM-08 | Modelos de projeto na criação | PM-08, PM-15 | Q27, Q56, Q127 | Alterado |
| RF-PM-09 | Nível de exigência global | PM-12 | Q14, Q17, Q22 | Alterado: o nível passa a ser por projeto, decidido pelo supervisor designado (Q17) |

## Ensino (GU)

| RF | O que faz no protótipo | Regras | Decisões que mudam | Na ERS |
|---|---|---|---|---|
| RF-GU-01 | Fluxo em 5 fases com próximo passo | GU-02, GU-03, GU-04 | Q149, Q150, Q169b, Q169c, Q169d | Alterado |
| RF-GU-02 | Glossário simples | GU-07 | Q151 | Alterado |
| RF-GU-03 | Faixa "Para que serve / O que fazer" | — | Q151 | Alterado |
| RF-GU-04 | Dicas por campo, liga/desliga (preferência só no navegador) | — | Q202 | Alterado: a preferência fica na conta do usuário (Q202) |
| RF-GU-05 | "Ver exemplo preenchido" | — | — | Confirmado |
| RF-GU-06 | Criar/abrir projeto de exemplo | GU-06, GU-07 | Q53, Q151 | Alterado |
| RF-GU-07 | Completude de cada registro | — | Q56 | Alterado |
| RF-GU-08 | Página "Sobre o PMBOK 7" | — | Q151 | Alterado |
| RF-GU-09 | Modo essencial / todas as telas (só no navegador) | — | Q202 | Alterado: a preferência fica na conta do usuário (Q202) |
| RF-GU-10 | Sugestões de tailoring nas telas | — | Q151, Q152 | Alterado |

## Dados (DA)

| RF | O que faz no protótipo | Regras | Decisões que mudam | Na ERS |
|---|---|---|---|---|
| RF-DA-01 | Histórico do projeto (últimos 300 eventos) | DA-02, DA-03 | Q58, Q191b, Q194, Q211 | Alterado |
| RF-DA-02 | Painel Dados: backups e lixeira | DA-02, DA-04, DA-05, DA-08, DA-09, DA-15 | Q195 | Alterado |
| RF-DA-03 | Fazer backup agora | DA-02, DA-04, DA-05, DA-08, DA-09, DA-15 | Q195 | Alterado |
| RF-DA-04 | Restaurar projeto excluído | DA-02, DA-04, DA-05, DA-08, DA-09, DA-15 | — | Confirmado |
| RF-DA-05 | Restaurar registro avulso | DA-02, DA-04, DA-05, DA-08, DA-09, DA-15 | — | Confirmado |
| RF-DA-06 | Restaurar backup da lista | DA-02, DA-04, DA-05, DA-08, DA-09, DA-15 | Q194 | Alterado |
| RF-DA-07 | Restaurar de arquivo enviado | DA-02, DA-04, DA-05, DA-08, DA-09, DA-15 | Q194 | Alterado |
| RF-DA-08 | Baixar backup da lista | — | Q184 | Alterado |
| RF-DA-09 | Baixar cópia consistente do banco | — | Q184 | Alterado |
| RF-DA-10 | Anonimizar projeto encerrado (LGPD) | DA-12, DA-13 | Q59, Q192, Q193 | Alterado |

## Usuários e acesso (US)

| RF | O que faz no protótipo | Regras | Decisões que mudam | Na ERS |
|---|---|---|---|---|
| RF-US-01 | Primeiro acesso cria o administrador | PM-01, PM-02 | Q52, Q188 | Alterado: a tela pede o código de instalação (Q188) |
| RF-US-02 | Entrar | PM-03 | Q186, Q186b, Q187 | Alterado |
| RF-US-03 | Sair | — | — | Confirmado |
| RF-US-04 | Trocar a própria senha | PM-02, PM-04 | Q187 | Alterado |
| RF-US-05 | Cadastrar usuário | PM-02, PM-05, PM-06 | Q41, Q52 | Alterado |
| RF-US-06 | Redefinir senha de outro | PM-02, PM-05, PM-06 | Q52 | Alterado |
| RF-US-07 | Ativar ou desativar conta | PM-02, PM-05, PM-06 | Q32, Q52 | Alterado |
| RF-US-08 | Listar usuários | PM-02, PM-05, PM-06 | Q52 | Alterado |

## Encerramento (EC)

| RF | O que faz no protótipo | Regras | Decisões que mudam | Na ERS |
|---|---|---|---|---|
| RF-EC-01 | Checklist automático (11) e manual (4), comparação com o planejado, objetivos | EC-03, EC-04, EC-05, EC-06, EC-07, EC-08, EC-09, EC-10, EC-11 | Q64, Q65, Q112, Q174a | Alterado |
| RF-EC-02 | Avaliação final | EC-03, EC-04, EC-05, EC-06, EC-07, EC-08, EC-09, EC-10, EC-11 | Q64, Q65, Q174a | Alterado |
| RF-EC-03 | Encerrar projeto | EC-03, EC-04, EC-05, EC-06, EC-07, EC-08, EC-09, EC-10, EC-11 | Q29, Q63, Q64, Q65, Q174a | Alterado |
| RF-EC-04 | Cancelar projeto com justificativa | EC-03, EC-04, EC-05, EC-06, EC-07, EC-08, EC-09, EC-10, EC-11 | Q29, Q64, Q65, Q174a | Alterado |
| RF-EC-05 | Reabrir projeto | EC-03, EC-04, EC-05, EC-06, EC-07, EC-08, EC-09, EC-10, EC-11 | Q29, Q64, Q65, Q174a | Alterado |
| RF-EC-06 | Projeto encerrado somente leitura | EC-10 | Q65 | Alterado |

## Requisitos funcionais novos

Funções que o protótipo não tem e que as decisões criaram. Na ERS, cada uma ganha o seu código RF.

| Função nova | Decisões |
|---|---|
| Escolher o gerente do projeto e o gerente de apoio, e trocá-los quando alguém sai | Q27, Q28, Q32, Q114 |
| Definir a cadência de relatório e o nível de exigência de cada projeto | Q16, Q17 |
| Conceder e retirar o acesso de consulta | Q35, Q43 |
| Propor o tailoring e mandar para a revisão do supervisor | Q33 |
| Liberar ou devolver com comentário, e reenviar depois da devolução | Q10, Q14, Q15, Q56 |
| Registrar a aprovação do patrocinador ou da autoridade de mudança, com quem e quando | Q14, Q69 |
| Gerar o documento (PDF ou impressão) do termo, da mudança, do relatório de status e do encerramento, com quem liberou e quando | Q11, Q15 |
| Guardar as versões do termo aprovado e do que uma mudança altera | Q62 |
| Registrar o aceite final, com quem aceitou e quando | Q63, Q109 |
| Ver o trabalho por gerente de projetos (visão do supervisor) | Q19, Q36 |
| Escrever e ler o parecer do supervisor, com os indicadores de apoio; gerar o documento; excluir no fim do prazo | Q20 a Q25, Q211 |
| Editar a iteração | Q67 |
| Cancelar com motivo o item, a questão, o risco e a aquisição, no lugar de excluir | Q81, Q97, Q145, Q168 |
| Tela de confirmação de exclusão, servida pelo servidor | Q198 |
| Página de privacidade, com o controlador, o contato e a base legal preenchidos pelo Administrador | Q189 |
| Arquivo com os dados de uma pessoa, anonimização de uma pessoa e registro dos pedidos do titular | Q190, Q191b |
| Prazo de guarda dos projetos encerrados ou cancelados, configurável | Q193 |
| Espaço do banco e dos backups na tela Dados | Q195 |
| Registro de quem baixou cada cópia de segurança, e quando | Q184 |

**Contagem:** 9 confirmados, 127 alterados e 2 descartados, de 138 requisitos funcionais do protótipo; mais 19 funções novas.
