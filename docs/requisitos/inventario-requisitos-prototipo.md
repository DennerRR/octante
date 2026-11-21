# Inventário de requisitos já implementados no protótipo

Situação atual a confirmar, levantada no commit 626d8fb. As regras de negócio estão em `inventario-regras-prototipo.md` e são citadas aqui pelo ID (PI-xx, PM-xx…).

"Quem pode": **todos** = qualquer usuário logado com acesso ao projeto (PM-07); em projeto encerrado ou cancelado toda gravação é bloqueada (PM-23). **admin** = `auth.exigir_admin()` (403 para os demais).

⚠ = prometido sem código correspondente, garantido só no cliente, ou inconsistente.

## A) Requisitos funcionais

### Projetos e portfólio (PJ)
- RF-PJ-01 | Listar os projetos visíveis, do mais recente ao mais antigo, com o número de partes ativas | `GET /` app.py:279 | todos
- RF-PJ-02 | Criar projeto com nome, descrição, cadência e modelo (em branco, Scrum, híbrido, preditivo) | app.py:326; pmo.py:48 | todos
- RF-PJ-03 | Visão geral: trilha das 5 fases, próximo passo, semáforo, pontos de atenção, resumos, progresso dos domínios e princípios | app.py:347 | todos
- RF-PJ-04 | Editar nome, descrição e cadência | app.py:379 | todos
- RF-PJ-05 | Definir quais usuários (não administradores) acessam o projeto | app.py:392-397 | admin
- RF-PJ-06 | Excluir projeto com confirmação; vai para a lixeira | app.py:405 | admin
- RF-PJ-07 | Portfólio com semáforo, fase, próxima etapa, críticos, atenções e revisões pendentes, por criticidade | pmo.py:140 | todos
- RF-PJ-08 | Checklist dos 8 domínios com progresso | app.py:494 | todos
- RF-PJ-09 | Verificação dos resultados de um domínio (Tabelas 2-2 a 2-10) com indicadores | app.py:499 | todos

### Partes interessadas (PI)
- RF-PI-01 | Registro das partes e resumo do ciclo de 5 etapas | rotas_partes.py:8 | todos
- RF-PI-02 | Cadastrar parte ("salvar e cadastrar outra") | rotas_partes.py:16 | todos
- RF-PI-03 | Detalhe da parte: interações, histórico de engajamento, riscos ligados | rotas_partes.py:47 | todos
- RF-PI-04 | Editar a parte | rotas_partes.py:60 | todos
- RF-PI-05 ⚠ | Excluir a parte — não confere o acesso ao projeto | rotas_partes.py:85 | todos
- RF-PI-06 | Análise em lote: poder, interesse, influência, impacto, atitude, saliência | rotas_partes.py:95 | todos
- RF-PI-07 | Priorização: grade poder × interesse, ordem sugerida, manual ou limpar | rotas_partes.py:124 | todos
- RF-PI-08 | Engajamento: matriz atual × desejado e plano de comunicação | rotas_partes.py:155 | todos
- RF-PI-09 | Monitoramento: registrar interação, últimas 50, mudanças de nível, alertas | rotas_partes.py:187 | todos
- RF-PI-10 ⚠ | Excluir interação — não confere o acesso ao projeto | rotas_partes.py:217 | todos

### Equipe (EQ)
- RF-EQ-01 | Listar e cadastrar membros (papel, dedicação, local, habilidades, lacunas, plano, motivador, parte e usuário ligados) | equipe.py:160 | todos
- RF-EQ-02 | Modelo de liderança e estágio de Tuckman | equipe.py:166 | todos
- RF-EQ-03 | Ver e editar membro com seus papéis RACI | equipe.py:189 | todos
- RF-EQ-04 | Liberar ou reativar membro | equipe.py:203 | todos
- RF-EQ-05 | Excluir membro | equipe.py:198 | todos
- RF-EQ-06 | Acordo de trabalho em 5 seções | equipe.py:225 | todos
- RF-EQ-07 | Matriz RACI: adicionar linha, atribuir R/A/C/I, remover linha | equipe.py:240 | todos
- RF-EQ-08 | Saúde da equipe: 9 fatores, histórico, gráfico, excluir avaliação | equipe.py:284 | todos

### Abordagem, ciclo de vida e tailoring (AB)
- RF-AB-01 | Assistente com 15 fatores: sugestão, escolha, justificativa, cadência | app.py:419 | todos
- RF-AB-02 | Ver fases, aplicar as sugeridas, criar fase | ciclo.py:63 | todos
- RF-AB-03 | Editar fase e fazer revisão de fase para concluí-la | ciclo.py:94 | todos
- RF-AB-04 | Excluir fase | ciclo.py:103 | todos
- RF-AB-05 | Responder às 15 perguntas de tailoring | ciclo.py:198 | todos
- RF-AB-06 | Registrar e excluir decisões de tailoring | ciclo.py:209-219 | todos
- RF-AB-07 | Diagnóstico da Tabela 3-1 calculado dos dados | ciclo.py:152, :225 | todos

### Planejamento (PL)
- RF-PL-01 | Termo de abertura: campos e status (rascunho, em revisão, aprovado) | app.py:452 | todos
- RF-PL-02 | Declaração de visão com texto gerado | app.py:475, :624 | todos
- RF-PL-03 | Datas de início e fim planejado | medicao.py:553 | todos
- RF-PL-04 | Criar iteração (nome, datas, meta, capacidade) | medicao.py:568 | todos
- RF-PL-05 | Excluir iteração (itens voltam ao backlog) | medicao.py:581 | todos
- RF-PL-06 | Planejar itens em lote e ver totais e velocidade | medicao.py:584 | todos

### Trabalho do projeto (TR)
- RF-TR-01 | Painel: resumo, questões, mudanças, lições, alertas | trabalho.py:152 | todos
- RF-TR-02 | Listar questões com filtro | trabalho.py:195 | todos
- RF-TR-03 | Registrar questão | trabalho.py:208 | todos
- RF-TR-04 | Editar questão, resolver, registrar consumo de reserva, ver lições | trabalho.py:235 | todos
- RF-TR-05 | Excluir questão | trabalho.py:247 | todos
- RF-TR-06 | Listar mudanças e mudanças por parte | trabalho.py:307 | todos
- RF-TR-07 | Registrar mudança | trabalho.py:314 | todos
- RF-TR-08 | Editar mudança: 6 impactos, decisão, quem decidiu, comunicada, itens | trabalho.py:343 | todos
- RF-TR-09 | Excluir mudança pendente ou rejeitada | trabalho.py:351 | todos
- RF-TR-10 | Lições aprendidas: listar e registrar | trabalho.py:384 | todos
- RF-TR-11 | Marcar lição como aplicada | trabalho.py:396 | todos
- RF-TR-12 | Excluir lição | trabalho.py:390 | todos

### Entrega (EN)
- RF-EN-01 | Painel: definição de pronto, unidade de estimativa, limite de WIP, alertas | entrega.py:373 | todos
- RF-EN-02 | Definir ou refazer a linha de base do escopo | entrega.py:399 | todos
- RF-EN-03 | Escopo e backlog em árvore, itens fora da linha de base | entrega.py:422 | todos
- RF-EN-04 | Salvar ordem de prioridade | entrega.py:439 | todos
- RF-EN-05 | Criar item (também a partir de mudança ou risco) | entrega.py:465 | todos
- RF-EN-06 | Editar, concluir e aceitar item | entrega.py:503 | todos
- RF-EN-07 | Excluir item | entrega.py:509 | todos
- RF-EN-08 | Quadro de tarefas com 4 colunas | entrega.py:558, :536 | todos
- RF-EN-09 | Custo da qualidade | entrega.py:570 | todos
- RF-EN-10 | Registrar e listar benefícios | entrega.py:622 | todos
- RF-EN-11 | Editar ou excluir benefício | entrega.py:642 | todos

### Medição (ME)
- RF-ME-01 | Painel: semáforo, valor agregado, burnup, velocidade, fluxo, previsão, limite de variação, plano de exceção | medicao.py:377 | todos
- RF-ME-02 | Criar indicador (KPI) e ver histórico | medicao.py:401 | todos
- RF-ME-03 | Registrar e excluir medição; excluir indicador | medicao.py:436 | todos
- RF-ME-04 | Emitir relatório de status que congela os números do dia | medicao.py:508 | todos
- RF-ME-05 | Ver, imprimir/PDF e excluir relatório | medicao.py:534 | todos

### Incerteza (IN)
- RF-IN-01 | Painel: matrizes P×I, EMV e reservas, limite, cadência de revisão, apetite, risco global | incerteza.py:250 | todos
- RF-IN-02 | Listar riscos com filtros | incerteza.py:278 | todos
- RF-IN-03 | Registrar risco | incerteza.py:295 | todos
- RF-IN-04 | Detalhe do risco: revisões, tendência, ligações | incerteza.py:332 | todos
- RF-IN-05 | Editar risco | incerteza.py:344 | todos
- RF-IN-06 | Registrar revisão do risco | incerteza.py:374 | todos
- RF-IN-07 | Excluir risco | incerteza.py:393 | todos
- RF-IN-08 | Registrar ambiguidade, complexidade ou volatilidade | incerteza.py:404 | todos
- RF-IN-09 | Atualizar ou excluir essa incerteza | incerteza.py:431 | todos

### Princípios (PR)
- RF-PR-01 | Autoavaliação dos 12 princípios | principios.py:524 | todos
- RF-PR-02 | Business case: VPL, ROI, payback, gráfico | principios.py:75 | todos
- RF-PR-03 | Conformidade e sustentabilidade | principios.py:108 | todos
- RF-PR-04 | Mudança organizacional: estados, grupos, adoção | principios.py:178 | todos
- RF-PR-05 | Registrar e excluir decisões | principios.py:243 | todos
- RF-PR-06 | Premissas | principios.py:265-285 | todos

### Aquisições e recursos (AQ)
- RF-AQ-01 | Painel "Compras e recursos" | suprimentos.py:131 | todos
- RF-AQ-02 | Registrar ou editar aquisição | suprimentos.py:145 | todos
- RF-AQ-03 | Excluir aquisição | suprimentos.py:178 | todos
- RF-AQ-04 | Cadastrar fornecedor como parte interessada | suprimentos.py:181 | todos
- RF-AQ-05 | Registrar ou editar recurso físico | suprimentos.py:190 | todos
- RF-AQ-06 | Excluir recurso físico | suprimentos.py:213 | todos

### Métodos (MT)
- RF-MT-01 | MoSCoW no item | metodos.py:15 | todos
- RF-MT-02 | Dependências entre itens, ciclos recusados | entrega.py:455; metodos.py:39 | todos
- RF-MT-03 | Gantt | metodos.py:68 | todos
- RF-MT-04 | Burndown | metodos.py:129 | todos
- RF-MT-05 | Cynefin e Stacey | metodos.py:156 | todos
- RF-MT-06 | Pré-mortem (cada linha vira risco) | metodos.py:171 | todos

### PMO (PM)
- RF-PM-01 | Minhas pendências | pmo.py:177 | todos
- RF-PM-02 | Pedir revisão do PMO | pmo.py:210 | todos
- RF-PM-03 | Revisar: aprovar ou devolver com comentário | pmo.py:232 | admin
- RF-PM-04 | Busca global | pmo.py:299 | todos
- RF-PM-05 | Agenda de prazos | pmo.py:359 | todos
- RF-PM-06 | Exportar agenda (.ics) | pmo.py:370 | todos
- RF-PM-07 | Exportar registros para Excel/CSV | pmo.py:411 | todos
- RF-PM-08 | Modelos de projeto na criação | app.py:339; pmo.py:19-60 | todos
- RF-PM-09 | Nível de exigência global | pmo.py:126 | admin

### Ensino (GU)
- RF-GU-01 | Fluxo em 5 fases com próximo passo | app.py:369; guia.py:11 | todos
- RF-GU-02 | Glossário simples | app.py:375 | todos
- RF-GU-03 | Faixa "Para que serve / O que fazer" | guia.py:98 | todos
- RF-GU-04 ⚠ | Dicas por campo, liga/desliga (preferência só no navegador) | dicas.py; app.js:49-101 | todos
- RF-GU-05 | "Ver exemplo preenchido" | pmo.py:262 | todos
- RF-GU-06 | Criar/abrir projeto de exemplo | app.py:289 | todos
- RF-GU-07 | Completude de cada registro | pmo.py:108-118 | todos
- RF-GU-08 | Página "Sobre o PMBOK 7" | app.py:321 | todos
- RF-GU-09 ⚠ | Modo essencial / todas as telas (só no navegador) | app.js:104-116 | todos
- RF-GU-10 | Sugestões de tailoring nas telas | pmbok.py | todos

### Dados (DA)
- RF-DA-01 | Histórico do projeto (últimos 300 eventos) | dados.py:16 | todos
- RF-DA-02 | Painel Dados: backups e lixeira | dados.py:30 | admin
- RF-DA-03 | Fazer backup agora | dados.py:38 | admin
- RF-DA-04 | Restaurar projeto excluído | dados.py:41 | admin
- RF-DA-05 | Restaurar registro avulso | dados.py:44 | admin
- RF-DA-06 | Restaurar backup da lista | dados.py:47 | admin
- RF-DA-07 | Restaurar de arquivo enviado | dados.py:52 | admin
- RF-DA-08 | Baixar backup da lista | dados.py:95 | admin
- RF-DA-09 | Baixar cópia consistente do banco | app.py:306 | admin
- RF-DA-10 | Anonimizar projeto encerrado (LGPD) | dados.py:104 | admin

### Usuários e acesso (US)
- RF-US-01 | Primeiro acesso cria o administrador | auth.py:87 | visitante enquanto não há usuário
- RF-US-02 | Entrar | auth.py:108 | público
- RF-US-03 | Sair | auth.py:132 | todos
- RF-US-04 | Trocar a própria senha | auth.py:139 | todos
- RF-US-05 | Cadastrar usuário | auth.py:167 | admin
- RF-US-06 | Redefinir senha de outro | auth.py:184 | admin
- RF-US-07 | Ativar ou desativar conta | auth.py:191 | admin
- RF-US-08 | Listar usuários | auth.py:198 | admin

### Encerramento (EC)
- RF-EC-01 | Checklist automático (11) e manual (4), comparação com o planejado, objetivos | ciclo.py:286 | todos
- RF-EC-02 | Avaliação final | ciclo.py:297-303 | todos
- RF-EC-03 | Encerrar projeto | ciclo.py:304-320 | todos
- RF-EC-04 | Cancelar projeto com justificativa | ciclo.py:309 | todos
- RF-EC-05 | Reabrir projeto | ciclo.py:294 | todos
- RF-EC-06 | Projeto encerrado somente leitura | app.py:106-118 | todos

## B) Requisitos não funcionais

### Segurança (SEG)
- RNF-SEG-01 | Login obrigatório em todas as rotas (menos entrar, primeiro acesso, estáticos) | auth.py:46-63 | teste: sim
- RNF-SEG-02 | Senha com hash do Werkzeug, ≥ 8 caracteres | auth.py:10-43 | teste: sim
- RNF-SEG-03 ⚠ | Bloqueio de 5 min após 5 erros por IP e conta; contador só na memória do processo e sem ProxyFix (atrás do proxy do PythonAnywhere pode bloquear todos) | auth.py:18-20, :115-128 | teste: sim
- RNF-SEG-04 ⚠ | Cookie HttpOnly, SameSite=Lax, Secure em produção; a sessão expira depois de 12 h sem uso, porque o cookie é renovado a cada requisição (Flask, SESSION_REFRESH_EACH_REQUEST), e não tem limite total enquanto há uso (corrigido em 19/11/2026; antes dizia "12 h; sem expiração por inatividade") | app.py:64-70 | teste: parcial
- RNF-SEG-05 | Trocar senha encerra as outras sessões | auth.py:52-55 | teste: sim
- RNF-SEG-06 | Conta desativada perde acesso na próxima requisição | auth.py:51 | teste: sim
- RNF-SEG-07 | Redirecionamento pós-login só para o próprio app | auth.py:31-35 | teste: sim
- RNF-SEG-08 | CSRF por sessão em todo POST | seguranca.py:21-55 | teste: sim
- RNF-SEG-09 | POST de outra origem recebe 403 | app.py:96-104 | teste: sim
- RNF-SEG-10 | Cabeçalhos de segurança (CSP, nosniff, X-Frame-Options, HSTS, no-store…) | seguranca.py:56-66 | teste: parcial
- RNF-SEG-11 | Autorização de administrador nas telas restritas | auth.py:77-79 e outros | teste: parcial
- RNF-SEG-12 ⚠ | Acesso por projeto (404 sem acesso); **falha**: excluir parte e excluir interação não conferem o acesso | util.py:38-68; rotas_partes.py:85-93, :217-231 | teste: sim, sem cobrir a falha
- RNF-SEG-13 | Isolamento entre projetos nos registros filhos | vários | teste: sim
- RNF-SEG-14 | Limites de requisição (60 MB) e de campo (20.000) | seguranca.py | teste: não
- RNF-SEG-15 | Validação do backup enviado | backup.py | teste: sim
- RNF-SEG-16 | Proteção contra injeção de fórmulas | pmo.py:404-408 | teste: sim
- RNF-SEG-17 ⚠ | Chave secreta por instalação; arquivo criado sem restringir permissões | app.py:146-156 | teste: sim
- RNF-SEG-18 | Depurador desligado; servidor local só em 127.0.0.1 | app.py:659-664 | teste: não
- RNF-SEG-19 | Marca interna não forjável por cabeçalho | exemplo.py:15 | teste: sim
- RNF-SEG-20 | SQL parametrizado; busca escapa curingas | pmo.py:305 | teste: parcial
- RNF-SEG-21 | Autoescape e escape em JSON/SVG | app.py:207 | teste: não
- RNF-SEG-22 | Páginas de erro amigáveis | app.py:536-550 | teste: parcial
- RNF-SEG-23 ⚠ | Primeiro acesso aberto a qualquer um até existir usuário | auth.py:87-105 | teste: sim (que fecha)
- RNF-SEG-24 ⚠ | Confirmação de exclusão só no cliente (exceto projeto) | app.js:153-200 | teste: só projeto

### Privacidade e LGPD (PRV)
- RNF-PRV-01 ⚠ | Anonimização parcial (histórico, lixeira, backups, interações, nomes ficam) | dados.py:104-117 | teste: sim
- RNF-PRV-02 | Hash de senha fora do histórico | auditoria.py:16 | teste: sim
- RNF-PRV-03 | Páginas com dados sem cache (no-store) | seguranca.py:65-66 | teste: não
- RNF-PRV-04 | Permissions-Policy e Referrer-Policy | seguranca.py:61-62 | teste: não
- RNF-PRV-05 | Nenhum recurso de terceiros em execução | seguranca.py:57 | teste: não
- RNF-PRV-06 ⚠ | Sem aviso de privacidade, consentimento, exportação ao titular nem retenção | — | teste: não

### Auditabilidade (AUD)
- RNF-AUD-01 | Gatilhos gravam toda inclusão, alteração e exclusão | auditoria.py:47-99 | teste: sim
- RNF-AUD-02 | Mudar só "atualizado em" não gera evento | auditoria.py:17 | teste: sim
- RNF-AUD-03 | Tela de histórico com nomes legíveis | dados.py:16 | teste: parcial
- RNF-AUD-04 | Quem decidiu fica registrado (termo, mudança, aceite, fase, revisão) | vários | teste: sim
- RNF-AUD-05 ⚠ | Tabela de auditoria sem proteção contra alteração e sem retenção | auditoria.py:3-5 | teste: não
- RNF-AUD-06 ⚠ | Trilha de mudanças contornável (TR-18, TR-20) | trabalho.py | teste: parcial

### Backup e recuperação (BKP)
- RNF-BKP-01 | Backup automático diário (no 1º acesso) | backup.py:119-124 | teste: sim
- RNF-BKP-02 | Backup antes de migração | db.py:673-674 | teste: sim
- RNF-BKP-03 | Backup antes de restauração | backup.py:139 | teste: parcial
- RNF-BKP-04 | Cópia consistente e atômica | backup.py:74-89 | teste: sim
- RNF-BKP-05 | integrity_check e SHA-256 | backup.py:35-61 | teste: sim
- RNF-BKP-06 | Rotação 14/5 | backup.py:107-116 | teste: não
- RNF-BKP-07 | Restaurar migra backup antigo e recusa versão mais nova | backup.py:134-149 | teste: parcial
- RNF-BKP-08 | Download consistente do banco | app.py:306-319 | teste: sim
- RNF-BKP-09 | Falha no backup não derruba o app | app.py:563-566 | teste: não
- RNF-BKP-10 | Lixeira com checagem de órfãos | auditoria.py:129-165 | teste: sim
- RNF-BKP-11 ⚠ | Backups no mesmo disco, sem cópia externa | backup.py:21-24 | teste: não
- RNF-BKP-12 ⚠ | Diálogo diz "não poderá ser recuperado", contradiz a lixeira | app.js:192 | teste: não

### Integridade dos dados (INT)
- RNF-INT-01 | Migrações versionadas e transacionais | db.py:631-662 | teste: sim
- RNF-INT-02 | Chaves estrangeiras ligadas | db.py:618 | teste: parcial
- RNF-INT-03 | Gatilhos de validação no banco | db.py:523-558 | teste: sim
- RNF-INT-04 | Restrições de unicidade e CHECK | schema.sql; db.py | teste: parcial
- RNF-INT-05 | Índices nas chaves estrangeiras | db.py:481-521 | teste: não
- RNF-INT-06 | busy_timeout de 10 s | db.py:616-619 | teste: não
- RNF-INT-07 | Restauração desfeita se deixar órfãos | auditoria.py:159-160 | teste: não
- RNF-INT-08 ⚠ | Códigos sequenciais por projeto sem UNIQUE (podem repetir) | incerteza.py:308 e outros | teste: sim
- RNF-INT-09 | Validação no servidor de listas, faixas e datas | util.py:9-35 | teste: sim
- RNF-INT-10 ⚠ | Ciclos de dependência barrados só no app | metodos.py:39-54 | teste: sim

### Acessibilidade (ACE)
- RNF-ACE-01 | `lang="pt-BR"` | base.html:2 | teste: não
- RNF-ACE-02 | "Pular para o conteúdo" | base.html:12 | teste: sim
- RNF-ACE-03 | Foco visível | style.css | teste: não
- RNF-ACE-04 | `role="alert"` e `role="status"` | base.html:148 | teste: sim
- RNF-ACE-05 ⚠ | Foco automático no erro (só cliente) | app.js:208-210 | teste: não
- RNF-ACE-06 ⚠ | `aria-current` só via JS | app.js:121 | teste: não
- RNF-ACE-07 | Menu com aria-expanded/controls | base.html:34 | teste: sim
- RNF-ACE-08 | Botão de dicas com aria-pressed | base.html:28 | teste: parcial
- RNF-ACE-09 | Gráficos SVG acessíveis com tabela de dados | graficos.py | teste: não
- RNF-ACE-10 | Status com cor + ícone + texto | templates | teste: não
- RNF-ACE-11 ⚠ | Contraste AA afirmado, sem verificação automática | style.css:1-30 | teste: não
- RNF-ACE-12 | prefers-reduced-motion | style.css:726 | teste: não
- RNF-ACE-13 | Alvos de 40 px | style.css | teste: não
- RNF-ACE-14 ⚠ | Diálogo modal com foco em Cancelar (só cliente) | app.js:153-171 | teste: não
- RNF-ACE-15 ⚠ | Asterisco de obrigatório (só cliente) | app.js:130-151 | teste: não
- RNF-ACE-16 | Busca com role="search" e atalho | base.html:16-17 | teste: não
- RNF-ACE-17 | Textos alternativos das imagens | base.html:14 | teste: não

### Usabilidade (USA)
- RNF-USA-01 ⚠ | "Aguarde…" e bloqueio de duplo envio (só cliente) | app.js:202-205 | teste: não
- RNF-USA-02 ⚠ | Faixa "somente consulta" (aparece duas vezes) | base.html:134-141 | teste: sim
- RNF-USA-03 ⚠ | Aviso de alterações não salvas (só cliente, duplicado) | app.js | teste: não
- RNF-USA-04 ⚠ | Confirmação em toda exclusão (só cliente; "remover linha" da RACI não confirma) | app.js; raci.html:25 | teste: não
- RNF-USA-05 ⚠ | Tokens de cor (há rgba() fixos fora de :root; teste só vê hex) | style.css | teste: sim
- RNF-USA-06 ⚠ | Obrigatórios marcados (só cliente) | app.js | teste: não
- RNF-USA-07 ⚠ | "☰ Menu: <tela atual>" (só cliente) | app.js:221-222 | teste: não
- RNF-USA-08 | Cartões com largura mínima e menu recolhível | style.css | teste: não
- RNF-USA-09 ⚠ | Campo inválido em vermelho só na validação do navegador | app.js:211-214 | teste: não
- RNF-USA-10 | Ajuda, dicas e glossário | guia.py | teste: sim
- RNF-USA-11 ⚠ | Mensagem de sucesso some em 4 s (WCAG 2.2.1) | app.js:13-17 | teste: não
- RNF-USA-12 | Modo essencial | app.js:104-116 | teste: sim
- RNF-USA-13 | Projeto novo mostra só o essencial e um "Próximo passo" | app.py:356-360 | teste: sim
- RNF-USA-14 ⚠ | "Funciona sem JavaScript" é falso no celular | app.js:1; style.css:729-732 | teste: não

### Responsividade (RES)
- RNF-RES-01 | Meta viewport | base.html:5 | teste: não
- RNF-RES-02 | Pontos de quebra 600/700/900/1250 px | style.css | teste: não
- RNF-RES-03 ⚠ | Rolagem horizontal de tabelas (via JS) | app.js:123-128 | teste: não
- RNF-RES-04 | Menu recolhível no celular | base.html:34 | teste: parcial
- RNF-RES-05 | Kanban com rolagem horizontal | style.css:409 | teste: não
- RNF-RES-06 | Estilos de impressão | style.css:449, :771 | teste: não

### Desempenho (DES)
- RNF-DES-01 | Dicas em cache | app.py:204-207 | teste: não
- RNF-DES-02 | Índices | db.py:478-521 | teste: não
- RNF-DES-03 | Checagem de backup no máximo de hora em hora | app.py:552-562 | teste: não
- RNF-DES-04 | Limites de leitura (histórico 300, busca 150…) | dados.py; pmo.py | teste: não
- RNF-DES-05 ⚠ | Portfólio recalcula tudo a cada requisição, sem paginação nem meta de desempenho | pmo.py:147-155 | teste: não
- RNF-DES-06 | SQLite para pouca concorrência | db.py:616-619 | teste: não

### Portabilidade e implantação (POR)
- RNF-POR-01 | Python ≥ 3.10; CI em 3.10 e 3.13 | testes.yml | teste: CI
- RNF-POR-02 ⚠ | flask e openpyxl sem versão máxima nem travamento | requirements.txt | teste: CI
- RNF-POR-03 | Sem openpyxl, exporta CSV | pmo.py:442-449 | teste: não
- RNF-POR-04 | iniciar.bat e iniciar.sh | raiz | teste: não
- RNF-POR-05 | Variáveis de ambiente de configuração | app.py; seguranca.py | teste: parcial
- RNF-POR-06 | Avisa porta em uso e abre o navegador | app.py:651-662 | teste: não
- RNF-POR-07 | wsgi.py liga o modo produção | wsgi.py | teste: sim
- RNF-POR-08 ⚠ | DEPLOY.md cita `gestor-pmbok7` em vez de octante | DEPLOY.md; README | teste: não
- RNF-POR-09 | SQLite em arquivo único | app.py:65 | teste: sim
- RNF-POR-10 | Atualização preserva instance/ e migra | db.py:665-680 | teste: sim

### Idioma e fuso (I18)
- RNF-I18-01 | Interface só em pt-BR | templates | teste: não
- RNF-I18-02 ⚠ | Fuso de Brasília (não funciona no Windows: sem tzset) | seguranca.py:14-18 | teste: só a variável
- RNF-I18-03 | Datas dd/mm/aaaa, guardadas em ISO | app.py:125-132 | teste: não
- RNF-I18-04 | Moeda R$ e entrada flexível | util.py | teste: sim
- RNF-I18-05 | .ics com escape RFC 5545 | pmo.py:370-383 | teste: sim
- RNF-I18-06 | CSV com ";" e BOM | pmo.py:444-448 | teste: não
- RNF-I18-07 | Datas do SQLite dependem do TZ do processo | db.py | teste: não

### Manutenibilidade (MAN)
- RNF-MAN-01 ⚠ | 149 testes pytest (README diz 149 e 148) | tests/ | —
- RNF-MAN-02 | CI no GitHub Actions, 3.10/3.13 | testes.yml | teste: sim
- RNF-MAN-03 ⚠ | Teste da regra de tokens (só hex) | tests/test_v12.py:99 | teste: sim
- RNF-MAN-04 | Um blueprint por domínio; conteúdo do PMBOK em pmbok.py | app.py:81-94 | teste: não
- RNF-MAN-05 | schema.sql intocável; mudanças por migração | db.py:1-7 | teste: sim
- RNF-MAN-06 | Alertas reunidos em `alertas_do_projeto` | app.py:187 | teste: não
- RNF-MAN-07 | Sem JS inline (CSP) | app.js:229-235 | teste: não
- RNF-MAN-08 | Documentação (README, AVALIACAO, DEPLOY, CLAUDE.md, docs/) | raiz | teste: não
- RNF-MAN-09 ⚠ | Sem linter, tipos ou cobertura na CI; imports circulares contornados | vários | teste: não
- RNF-MAN-10 ⚠ | Maioria dos testes com login e CSRF desligados | tests/conftest.py:14 | —
- RNF-MAN-11 ⚠ | README desatualizado (14 × 18 iterações; "possíveis evoluções" já feitas) | README.md | —

### Marca (MAR)
- RNF-MAR-01 | Nome e logo em SVG | static/marca | teste: não
- RNF-MAR-02 | Script que gera a marca | static/marca/gerar_marca.py | teste: não
- RNF-MAR-03 | Paleta v17 em tokens | style.css:1-30 | teste: sim
- RNF-MAR-04 | Gráficos em roxo, laranja e ciano | graficos.py:12 | teste: não
- RNF-MAR-05 | Cabeçalho do Excel na cor da marca | pmo.py:431 | teste: parcial
- RNF-MAR-06 | Logo em contornos | static/marca | teste: não
- RNF-MAR-07 ⚠ | AVALIACAO.md descreve a paleta antiga (v12) | AVALIACAO.md:34-38 | —

## Contagem

138 requisitos funcionais (4 com ⚠) e 136 não funcionais (46 com ⚠). Evidência por teste nos RNF: 50 sim, 15 parciais, 63 sem teste, 8 de documentação.
