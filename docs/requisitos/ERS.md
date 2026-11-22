# Especificação de Requisitos de Software (ERS) do Octante

## 0. Identificação

| Campo | Valor |
|---|---|
| Produto | Octante: ferramenta de trabalho de um PMO para gerenciar projetos guiados pelo PMBOK 7 |
| Versão | 1.1, aprovada: a linha de base dos requisitos, com as mudanças da Q219 |
| Data | 22/11/2026 |
| Estado | Aprovada em 20/11/2026 pelo responsável pelo produto. Daqui em diante, cada mudança segue a Q219. |
| Dono dos requisitos | O responsável pelo produto, que aprova a ERS e cada mudança nela (Q216, Q219) |
| Norma | ISO/IEC/IEEE 29148:2018, seção 9.6, com a adaptação declarada na seção 0.2 (Q13, Q214) |
| Decisões | [Registro de decisões](decisoes-elicitacao.md), da Q1 à Q219, e o [resumo confirmado](resumo-para-confirmacao.md) |

**Histórico de versões**

| Versão | Data | O que mudou | Decisões |
|---|---|---|---|
| 0.1 | 20/11/2026 | Parte 1: identificação, introdução, referências, interfaces externas e os domínios Usuários e acesso, PMO, Dados e Projetos. | Q214 a Q219 |
| 0.2 | 20/11/2026 | Parte 1 aprovada. Aplicadas as Q220 a Q222: valores das entradas e nomes dos módulos (seções 1.8, 3.1, 3.2.1 a 3.2.4), exclusão do parecer vencido (RF-PM-18, RN-PM-61, RN-PM-78) e encarregado na página de privacidade (RF-DA-12). | Q220 a Q222 |
| 0.3 | 20/11/2026 | Parte 2: os oito domínios de desempenho (seções 3.2.5 a 3.2.12). | Q214 a Q219, Q223 |
| 0.4 | 20/11/2026 | Parte 3: princípios, aquisições, métodos, guia e encerramento (seções 3.2.13 a 3.2.17), aprovada com a Q224: o custo previsto (RN-PR-03) passa ao domínio Planejamento. | Q214 a Q219, Q224 |
| 0.5 | 20/11/2026 | Parte 4: não funcionais (seções 3.3 a 3.8), verificação (seção 4) e informações de apoio (seção 5). | Q214 a Q219, Q225 |
| 1.0 | 20/11/2026 | ERS aprovada: as quatro partes e as Q220 a Q225. Linha de base dos requisitos. | Q218, Q225 |
| 1.1 | 22/11/2026 | Seção 3.2.1: a RN-PM-79 nova (sessões encerradas quando o Administrador redefine a senha), que a RF-US-06 passa a aplicar; a RN-PM-05 passa a recusar também a lista das contas a quem não é Administrador. | Q230, Q231 |

### 0.1 Sumário

- [0. Identificação](#0-identificação): [0.2 Adaptação da norma](#02-adaptação-da-norma) · [0.3 Como ler os requisitos](#03-como-ler-os-requisitos)
- [1. Introdução](#1-introdução): [1.1 Propósito](#11-propósito) · [1.2 Escopo](#12-escopo) · [1.3 Perspectiva do produto](#13-perspectiva-do-produto) · [1.4 Funções do produto](#14-funções-do-produto) · [1.5 Usuários](#15-usuários) · [1.6 Limitações](#16-limitações) · [1.7 Premissas e dependências](#17-premissas-e-dependências) · [1.8 Divisão dos requisitos](#18-divisão-dos-requisitos) · [1.9 Definições e siglas](#19-definições-e-siglas)
- [2. Referências](#2-referências): [2.1 De conformidade](#21-de-conformidade) · [2.2 De orientação](#22-de-orientação)
- [3. Requisitos](#3-requisitos): [3.1 Interfaces externas](#31-interfaces-externas) · [3.2 Funções e regras de negócio](#32-funções-e-regras-de-negócio)
  - [3.2.1 Usuários e acesso](#321-usuários-e-acesso-us) · [3.2.2 PMO](#322-pmo-pm) · [3.2.3 Dados](#323-dados-da) · [3.2.4 Projetos](#324-projetos-pj)
  - [3.2.5 Partes interessadas](#325-partes-interessadas-pi) · [3.2.6 Equipe](#326-equipe-eq) · [3.2.7 Abordagem](#327-abordagem-ciclo-de-vida-e-tailoring-ab) · [3.2.8 Planejamento](#328-planejamento-pl) · [3.2.9 Trabalho do projeto](#329-trabalho-do-projeto-tr) · [3.2.10 Entrega](#3210-entrega-en) · [3.2.11 Medição](#3211-medição-me) · [3.2.12 Incerteza](#3212-incerteza-in)
  - [3.2.13 Princípios](#3213-princípios-pr) · [3.2.14 Aquisições e recursos físicos](#3214-aquisições-e-recursos-físicos-aq) · [3.2.15 Métodos](#3215-métodos-mt) · [3.2.16 Guia e ensino](#3216-guia-e-ensino-gu) · [3.2.17 Encerramento](#3217-encerramento-ec)
    - [3.3 Usabilidade e acessibilidade](#33-usabilidade-e-acessibilidade) · [3.4 Desempenho](#34-desempenho) · [3.5 Banco de dados lógico](#35-banco-de-dados-lógico) · [3.6 Restrições de projeto](#36-restrições-de-projeto) · [3.7 Conformidade com normas](#37-conformidade-com-normas) · [3.8 Atributos do sistema](#38-atributos-do-sistema)
- [4. Verificação](#4-verificação)
- [5. Informações de apoio](#5-informações-de-apoio): [5.1 Rastreabilidade](#51-rastreabilidade) · [5.2 Códigos que saíram](#52-códigos-que-saíram) · [5.3 Não funcionais que viraram outros requisitos](#53-não-funcionais-do-protótipo-que-viraram-outros-requisitos) · [5.4 Evolução prevista](#54-evolução-prevista) · [5.5 Pontos a confirmar](#55-pontos-a-confirmar)

### 0.2 Adaptação da norma

A Q13 pediu a estrutura da ISO/IEC/IEEE 29148:2018 "simplificada". Pelo anexo C da norma, quem adapta o conteúdo declara as circunstâncias, ouve as partes afetadas e diz o que tirou ou mudou. Esta seção é essa declaração (Q214).

**Circunstâncias:**
- um PMO só, com 1 a 3 supervisores e até uns 15 gerentes de projetos (Q4);
- o protótipo já existe e evolui, sem ser reescrito do zero (Q46, [ADR 0003](../adr/0003-evoluir-o-prototipo-reauditando-as-regras.md));
- o código é escrito pelo Claude, e o responsável pelo produto revisa e faz os commits;
- a hospedagem é o plano gratuito do PythonAnywhere (Q42, [ADR 0002](../adr/0002-hospedagem-no-pythonanywhere-gratuito.md));
- as necessidades, as decisões e as razões de cada uma já estão no registro de decisões e no resumo confirmado.

**Partes ouvidas:** o responsável pelo produto, que aprovou esta adaptação na Q214.

**O que sai ou muda em relação à norma:**
1. Só a especificação de software (seção 9.6) é escrita. As especificações de negócio (9.3), de partes interessadas (9.4) e de sistema (9.5) e os conceitos de operação (anexos A e B) não são produzidos: o registro de decisões e o resumo confirmado já trazem o que eles trariam.
2. As definições (9.2.3) ficam no [GLOSSARY](../../GLOSSARY.md), e a ERS remete a ele.
3. Não há lista de figuras nem de tabelas (9.2.2): o sumário leva a cada seção, e cada tabela fica na seção do seu domínio.
4. A justificativa de cada requisito (5.2.8) fica na pergunta do registro de decisões citada na coluna Origem.
5. Dos atributos de exemplo da 5.2.8, ficam fora das tabelas: a versão de cada requisito, que o histórico de versões mostra pelos códigos mudados; o dono, que é o mesmo para todos e aparece na identificação; o risco e a dificuldade, que vão para o planejamento de cada entrega, nas issues; e o tipo, que já está no código e na seção (Q216).
6. Os critérios de aceite ficam nas histórias de usuário das issues (Q6), e não na ERS.
7. A ordem segue a seção 9.6, que a norma deixa a critério do projeto (9.6.1). As funções ficam por domínio, na ordem do uso (Q214).
8. Um item da norma que não se aplica ao Octante fica na sua seção, com uma linha dizendo por quê.

### 0.3 Como ler os requisitos

- **Requisito:** uma frase com "deve", que diz o que o Octante faz ou a regra que ele cumpre (Q215). A permissão aparece como "o sistema deve permitir que…", e a proibição, como "o sistema deve recusar…". Um texto marcado **A confirmar** depende de uma confirmação, com quem confirma e até qual entrega.
- **Código:** RF- para as funções, RN- para as regras de negócio e RNF- para os não funcionais. O código vem do inventário do protótipo e nunca muda nem é reaproveitado; o requisito novo ganha o próximo número livre do domínio (Q217). As regras ficam no domínio a que mais se ligam, com o código do inventário: por isso as regras de usuários e de projetos têm o código RN-PM.
- **Colunas** (Q216):
  - **Regras:** só nas funções, com as regras de negócio que a função aplica. Uma regra de outro domínio é descrita na seção dele.
  - **Origem:** na regra, a página do PMBOK 7 ou "Regra do PMO", com a pergunta que a decidiu; na função, as perguntas que a decidiram. "Protótipo" quer dizer que a regra veio do protótipo e foi confirmada sem mudança.
  - **Protótipo:** confirmado (entra como estava), alterado (entra reescrito pelas decisões) ou novo (Q6).
  - **Parte:** App (vale para o Octante inteiro, fora de um projeto), Núcleo (sempre presente em todo projeto) ou o nome do módulo opcional (seção 1.8).
  - **Entrega:** 1, 2 ou 3 (seção 1.8). A entrega faz o papel da prioridade.
  - **Verificação:** teste (automático), inspeção (revisão do código ou de um arquivo), demonstração (mostrar funcionando no app) ou análise (medir ou calcular).
- **Quadro de entradas:** cada domínio traz os campos que as pessoas preenchem, com o tipo, se são obrigatórios e os valores válidos. É desse quadro que saem os testes de partição e de valores-limite da Q77.
- Os termos em negrito e os nomes dos papéis seguem o [GLOSSARY](../../GLOSSARY.md).

## 1. Introdução

### 1.1 Propósito

O Octante é a ferramenta de trabalho de um PMO para gerenciar projetos reais seguindo o PMBOK 7, com o ensino embutido no uso, sem um "modo treinamento" (Q1). Esta ERS diz o que a versão nova do Octante deve fazer. Ela parte do protótipo, que evolui (ADR 0003), e das decisões da elicitação, e é a base das issues e dos testes (Q6, Q13).

### 1.2 Escopo

- **Produto:** o Octante, uma aplicação web.
- **O que ele faz:**
  - conduz cada projeto pelos oito domínios de desempenho do PMBOK 7, com um núcleo sempre presente e módulos opcionais que o tailoring do projeto liga (Q18, Q31);
  - leva o trabalho dos gerentes de projetos à revisão do supervisor, que libera ou devolve com comentário (Q14);
  - registra as aprovações dadas por fora, por quem tem autoridade, e gera os documentos que vão aos destinatários (Q11, Q14);
  - mostra alertas, cada um com a origem da regra: a página do PMBOK 7 ou "regra do PMO" (Q153, [ADR 0005](../adr/0005-origem-de-cada-regra-na-tela.md));
  - guarda o histórico, os backups e os pedidos da LGPD (Q51, Q189 a Q195).
- **Para quê:** o gerente de projetos com conhecimento inicial aplica o PMBOK 7 com orientação; o supervisor acompanha e revisa; e o PMO tem um registro auditável dos projetos (Q1, Q19, Q210).
- **O que ele não faz:** enviar e-mail, avisar de prazos fora do app, funcionar no celular e calcular a TIR do business case. O e-mail por API HTTPS e o PMBOK 8 ficam para o futuro (Q41, Q42, Q138, Q200; resumo, seção 8).
- **Especificação de nível acima:** não há. O Octante não faz parte de um sistema maior.

### 1.3 Perspectiva do produto

O Octante é um produto independente: uma instalação por PMO, com um banco próprio.

1. **Interfaces com um sistema maior:** não se aplica, porque o Octante não faz parte de um sistema maior.
2. **Interface com o usuário:** páginas web em português do Brasil, no navegador do computador, com a WCAG 2.1 nível AA (Q38). O Octante não é feito para celular, mas a tela estreita continua para quem usa zoom de até 400% no computador (Q200, Q200b).
3. **Interfaces de hardware:** não se aplica. O Octante só usa o computador e o navegador de quem o abre.
4. **Interfaces com outros softwares:**

   | Software | Para quê | Versão em uso | Onde obter |
   |---|---|---|---|
   | Python | linguagem do app | 3.10 a 3.13, as duas pontas testadas na CI; 3.13 no desenvolvimento | python.org |
   | Flask, com Werkzeug, Jinja2, MarkupSafe, itsdangerous, click e blinker | servidor web e páginas | Flask 3.1 (3.1.3), Werkzeug 3.1 (3.1.9), Jinja2 3.1 (3.1.6) | PyPI oficial |
   | SQLite | banco de dados | a que vem com o Python do servidor; 3.50 no desenvolvimento | sqlite.org |
   | openpyxl, com et-xmlfile | planilha .xlsx exportada | 3.1 (3.1.5) | PyPI oficial |
   | tzdata | fuso horário fora do PythonAnywhere, inclusive no Windows | a mantida mais recente | PyPI oficial (Q206) |
   | Navegador | interface com o usuário | um navegador de computador atual; os testes automáticos usam o Chromium | Q38, Q212 |

   A versão exata de cada biblioteca fica travada no `requirements.txt`, com o hash de cada arquivo, e só entram as bibliotecas aprovadas pelo PMO (Q204, Q204b).
5. **Comunicação:** HTTPS, fornecido pelo PythonAnywhere. O app não carrega recursos de terceiros nem chama serviços de fora (RNF-PRV-05).
6. **Memória e disco:** o banco e os backups ficam no disco do plano gratuito. O Administrador recebe um alerta quando os dois juntos passam de 400 MB (Q195).
7. **Operação:** o uso é interativo. Não há tarefa agendada, porque o plano gratuito não roda nada sozinho (Q42): o backup automático acontece no primeiro acesso depois do intervalo (RN-DA-07). Backup e recuperação: backups automáticos no servidor, uma cópia baixada pelo Administrador toda semana (Q44) e a restauração pela tela Dados.
8. **Ajustes de cada instalação:** o código de instalação, que cria a primeira conta (Q188); a chave secreta própria (RNF-SEG-17); o fuso horário, com o de Brasília como padrão (Q206); os dados da página de privacidade (Q189); e os prazos de guarda dos pareceres e dos projetos (Q25, Q193). A versão nova começa com o banco limpo, sem os dados do protótipo (Q39).
9. **Serviços:** o PythonAnywhere hospeda o app (ADR 0002). O GitHub guarda o código e roda a CI e o Dependabot, só no desenvolvimento (Q204).

### 1.4 Funções do produto

| Domínio | O que o Octante faz | Seção |
|---|---|---|
| Usuários e acesso | contas, tipos de conta, papel de Administrador, primeiro acesso, login, sessão e desligamento | 3.2.1 |
| PMO | pendências, revisão com liberado e devolvido, aprovação registrada, documento gerado, visão do supervisor, parecer, busca, agenda, exportação e modelos de projeto | 3.2.2 |
| Dados | histórico, lixeira, backups, página de privacidade, pedidos do titular, anonimização e prazo de guarda | 3.2.3 |
| Projetos | portfólio, criação pelo supervisor, gerentes do projeto, acesso de consulta, nível de exigência, cadência de relatório, visão geral e projeto de exemplo | 3.2.4 |
| Partes interessadas | identificar, analisar e engajar as partes, plano de comunicação e contatos | parte 2 |
| Equipe | membros, matriz RACI e desenvolvimento da equipe | parte 2 |
| Abordagem, ciclo de vida e tailoring | abordagem de desenvolvimento, fases, critérios de saída e tailoring | parte 2 |
| Planejamento | termo de abertura, visão, cronograma e orçamento | parte 2 |
| Trabalho do projeto | questões, mudanças, lições aprendidas e quadro de tarefas | parte 2 |
| Entrega | itens de escopo, definição de pronto, aceite e iterações | parte 2 |
| Medição | indicadores, semáforo e relatório de status | parte 2 |
| Incerteza | riscos, reservas e risco geral do projeto | parte 2 |
| Princípios | autoavaliação dos 12 princípios | parte 3 |
| Aquisições e recursos | aquisições, fornecedores e recursos físicos | parte 3 |
| Métodos | MoSCoW, dependências, Gantt, burndown, Cynefin e Stacey | parte 3 |
| Guia e ensino | guia das etapas, dicas, exemplos e glossário | parte 3 |
| Encerramento | checklist, avaliação final, aceite final, encerrar, cancelar e reabrir | parte 3 |

### 1.5 Usuários

| Usuário | Quem é | O que faz no Octante |
|---|---|---|
| **Gerente de projetos** | Tipo de conta de quem conduz projetos no PMO, com conhecimento inicial em gerenciamento de projetos (Q207, Q210). Conduz de 1 a 3 projetos (Q4). | Num projeto, é o **gerente do projeto** ou o **gerente de apoio**: preenche os registros, envia para revisão, gera documentos e registra aprovações. |
| **Supervisor** | Tipo de conta de quem revisa o trabalho; não é gerente de projeto (Q2, Q60). O PMO tem de 1 a 3 (Q4). | Cria projetos, revisa, pode editar, concede acesso de consulta, encerra, cancela e reabre projetos, e escreve pareceres (Q9, Q27, Q29, Q34, Q43). |
| **Administrador** | Papel extra, dado só a um supervisor (Q7, Q22). | Cuida das contas, dos backups, da lixeira e dos pedidos da LGPD (Q52, Q190). |
| **Destinatário** | Patrocinador, cliente, equipe ou diretoria, sem conta no Octante (Q3). | Recebe por fora os documentos gerados (Q11). |

O gerente de projetos aprende enquanto trabalha, por isso o Octante mostra a origem de cada regra, dicas e exemplos (Q1, ADR 0005). As páginas seguem a WCAG 2.1 AA, para pessoas com deficiência visual, motora ou cognitiva (Q38).

### 1.6 Limitações

- **Lei:** a LGPD vale para os dados pessoais de contas, partes interessadas e membros da equipe (Q59, Q189 a Q193).
- **Referência única:** o PMBOK 7, edição em inglês, é a única referência das regras de gerenciamento de projetos. Uma regra de outra fonte é não conformidade e sai, mesmo rotulada; onde o PMBOK 7 não trata do assunto, a regra é do PMO, por decisão explícita (Q49, Q113, [ADR 0001](../adr/0001-pmbok-7-como-referencia.md), ADR 0005).
- **Auditoria:** o histórico de alterações é protegido contra alteração (Q194).
- **Segurança:** o endereço no PythonAnywhere é público, então a primeira conta, o login e a sessão têm proteções próprias (Q186 a Q188).
- **Hospedagem:** o plano gratuito não roda tarefas agendadas nem envia e-mail (Q42).
- **Plataforma:** computador e português do Brasil (Q38, Q200).

### 1.7 Premissas e dependências

Se uma destas condições mudar, os requisitos podem mudar junto:
- o plano gratuito do PythonAnywhere continua oferecendo HTTPS, Python, SQLite e o disco de hoje (ADR 0002);
- o PMBOK 7 continua sendo a referência; o PMBOK 8 é evolução prevista (Q30, Q47);
- as pessoas usam o Octante num navegador de computador atual (Q38, Q200);
- o PMO tem o tamanho da Q4: 1 a 3 supervisores e até uns 15 gerentes de projetos, e cada projeto tem no máximo dois gerentes;
- os dados do protótipo não são migrados (Q39).

### 1.8 Divisão dos requisitos

**Por parte do sistema** (coluna Parte). Os nomes dos módulos foram decididos na Q220. Os módulos opcionais são os itens de tailoring da Q31, com os ajustes das Q108, Q172a, Q172b e Q174b, que levaram ao núcleo o registro de contatos, a reserva de contingência, a avaliação do risco geral e o plano de exceção. Um módulo desligado fica inacessível no projeto, com os seus alertas, as etapas do guia e os itens do encerramento, e os dados voltam quando ele é religado (Q57, Q174a).

| Parte | O que reúne | Q31, linha |
|---|---|---|
| App | contas, papéis, PMO, dados, portfólio e o que vale fora de um projeto | 21, 24 |
| Núcleo | o que todo projeto tem | 1, 3, 5, 7, 8, 9, 11, 13, 15, 17, 20, 22, 23 |
| Engajamento das partes | saliência, matriz de engajamento e nota de satisfação dos contatos | 2 |
| Desenvolvimento da equipe | estágios de Tuckman, acordo de trabalho, saúde da equipe e planos de desenvolvimento | 4 |
| Diagnóstico de tailoring | diagnóstico pela Tabela 3-1 do PMBOK 7 | 6 |
| Aquisições e recursos físicos | aquisições, fornecedores e recursos físicos | 10 |
| Escopo, qualidade e benefícios | linha de base do escopo, custo da qualidade e benefícios | 12 |
| Medição avançada | valor agregado, burnup, burndown, velocidade, fluxo e KPIs | 14 |
| Incerteza avançada | valor monetário esperado, ambiguidade, complexidade, volatilidade, Cynefin e Stacey | 16 |
| Business case e governança | business case, conformidade, registro de decisões e mudança organizacional | 18 |
| Princípios e resultados | autoavaliação dos 12 princípios, checklist dos 8 domínios e verificação dos resultados (tabelas 2-2 a 2-10) | 19 |

**Por entrega** (coluna Entrega), pelas Q47 e Q213. A acessibilidade, os testes e o cuidado com as bibliotecas valem desde a Entrega 1.

| Entrega | O que entra |
|---|---|
| 1 | Papéis, criação do projeto pelo supervisor, revisão obrigatória com liberado e devolvido, aprovação separada da revisão, encerramento pelo supervisor, parecer, acesso de consulta e desligamento (Q47). As proteções que valem para o app inteiro: bloqueio de login, sessão, código de instalação, chave secreta, confirmação de exclusão, aviso de privacidade, histórico protegido e backups compactados com alerta de falha. A base de testes da Q205 (Q213). |
| 2 | Núcleo e tailoring, nível de exigência e cadência de relatório por projeto, relatório de status com indicadores congelados, visão do supervisor por gerente de projetos e resumo de alertas (Q47). As mudanças de regras dos domínios do núcleo, o pedido do titular (Q190) e o prazo de guarda (Q193) (Q213). |
| 3 | A revisão das regras de alerta e os ajustes nos módulos opcionais (Q47, Q213). |
| Futuro | E-mail por API HTTPS e PMBOK 8 (Q47). |

Um requisito confirmado, que não muda, entra junto com a parte do sistema a que pertence, para ganhar os testes da Q196 (Q216). As colunas Parte e Entrega de cada tabela formam a tabela cruzada da divisão dos requisitos (9.6.9).

### 1.9 Definições e siglas

As definições estão no [GLOSSARY](../../GLOSSARY.md).

| Sigla | Significado |
|---|---|
| ASVS | Application Security Verification Standard, da OWASP |
| CI | integração contínua: os testes que rodam no GitHub a cada envio de código |
| CSV | arquivo de texto com valores separados por vírgula |
| ERS | especificação de requisitos de software |
| HTTPS | protocolo seguro da web |
| LGPD | Lei Geral de Proteção de Dados Pessoais (Lei nº 13.709/2018) |
| OWASP | Open Worldwide Application Security Project |
| PMBOK 7 | Guia PMBOK, 7.ª edição, com o Padrão de Gerenciamento de Projetos |
| PMO | escritório de gerenciamento de projetos |
| RF, RN, RNF | requisito funcional, regra de negócio e requisito não funcional |
| WCAG | Web Content Accessibility Guidelines, do W3C |

## 2. Referências

Os documentos de conformidade trazem requisitos que a ERS adota ao citá-los. Os de orientação só informam (9.2.4).

### 2.1 De conformidade

| Documento | Versão e data | Editora | Onde obter | Partes que valem |
|---|---|---|---|---|
| A Guide to the Project Management Body of Knowledge (PMBOK® Guide), Seventh Edition, e The Standard for Project Management (ANSI/PMI 99-001-2021) | 7.ª edição, 2021; ISBN 978-1-62825-664-2 | Project Management Institute (PMI) | pmi.org | as seções e as páginas citadas em cada regra, na edição em inglês |
| Lei nº 13.709, de 14 de agosto de 2018 (LGPD) | texto compilado, com as alterações até a Lei nº 15.452, de 2026 | Presidência da República | planalto.gov.br | os artigos citados em cada requisito: 5º, 6º, 7º, 9º, 12, 15, 16, 18, 19, 37, 41 e 46 |
| Web Content Accessibility Guidelines (WCAG) 2.1 | Recomendação do W3C de 06/05/2025 (a primeira é de 05/06/2018) | World Wide Web Consortium (W3C) | w3.org/TR/WCAG21 | os critérios dos níveis A e AA |
| OWASP Application Security Verification Standard (ASVS) | 5.0.0, de 30/05/2025 | OWASP Foundation | asvs.owasp.org | os itens citados nos requisitos de segurança: 6.1.1, 6.3.2 e 6.4.1 |

### 2.2 De orientação

| Documento | Versão e data | Editora | Onde obter |
|---|---|---|---|
| ISO/IEC/IEEE 29148, Systems and software engineering — Life cycle processes — Requirements engineering | 2.ª edição, 2018-11, confirmada em 2024 | ISO, IEC e IEEE | iso.org; IEEE Xplore |
| Guide to the Software Engineering Body of Knowledge (SWEBOK) | V4.0a, agosto de 2026 | IEEE Computer Society | computer.org |
| NASA Systems Engineering Handbook | NASA/SP-2016-6105 Rev2 | NASA | nasa.gov |
| Documentação do Python | da versão em uso | Python Software Foundation | docs.python.org |
| Documentação do Flask, do Werkzeug e do Jinja2 | 3.1 | Pallets | palletsprojects.com |
| Documentação do SQLite | da versão em uso | SQLite | sqlite.org |
| Documentação do openpyxl | 3.1 | projeto openpyxl | openpyxl.readthedocs.io |
| Documentação do pip | atual | Python Packaging Authority | pip.pypa.io |
| GitHub Docs: Actions e Dependabot | atual | GitHub | docs.github.com |
| Playwright para Python e axe-core | da versão travada nos testes | Microsoft e Deque | playwright.dev/python; github.com/dequelabs/axe-core |

## 3. Requisitos

### 3.1 Interfaces externas

As interfaces com o usuário, com outros softwares e com a comunicação estão na seção 1.3. Esta seção diz o que entra e o que sai do Octante.

**Saídas:**

| Saída | Formato | Para quem | Requisitos |
|---|---|---|---|
| Telas | páginas HTML no navegador | contas ativas, pelo papel | seção 3.2 |
| Página de privacidade | página HTML, aberta também sem login | qualquer pessoa | RF-DA-11 |
| Documento gerado | página para imprimir ou salvar em PDF pelo navegador | destinatários, por meio do gerente do projeto | RF-PM-11, RN-PM-45 a RN-PM-47 |
| Documento do parecer | página para imprimir ou salvar em PDF | supervisores | RF-PM-16 |
| Planilha de registros | .xlsx ou .csv | contas para as quais o projeto é visível | RF-PM-07, RN-DA-14, RN-PM-39 |
| Agenda de prazos | .ics, para programas de calendário | contas para as quais os projetos são visíveis | RF-PM-06 |
| Backup | arquivo do banco, compactado, com assinatura SHA-256 | Administrador | RF-DA-03, RF-DA-08, RN-DA-09, RN-DA-10 |
| Cópia do banco | arquivo do banco | Administrador | RF-DA-09 |
| Arquivo do titular | planilha .xlsx, com uma aba por tipo de registro (Q220) | Administrador e supervisor, para entregar ao titular | RF-DA-13, RF-DA-14 |

**Entradas:** os campos de cada domínio estão no quadro de entradas da seção do domínio. As regras que valem para todas as entradas são a RN-DA-11 (tamanho do campo e do arquivo), a RN-DA-15 (validação também no banco) e a RN-DA-30 (campo só com espaços), além dos não funcionais da parte 4, como o erro mostrado junto do campo (Q199) e a proteção contra formulário forjado (RNF-SEG-08).

### 3.2 Funções e regras de negócio

#### 3.2.1 Usuários e acesso (US)

Contas, tipos de conta, papel de Administrador, primeiro acesso, login, sessão e desligamento. As regras deste domínio têm o código RN-PM, do inventário do protótipo.

**Entradas**

| Entrada | Onde | Tipo | Obrigatória | Valores válidos | Origem |
|---|---|---|---|---|---|
| Código de instalação | Primeiro acesso | texto | sim | igual ao código gerado na instalação (RN-PM-25) | Q188 |
| Nome | Primeiro acesso; cadastro e edição de conta | texto | sim | até 20.000 caracteres (RN-DA-11) | Q51 |
| Login | Entrar; Primeiro acesso; cadastro de conta | texto | sim | até 20.000 caracteres; único, sem diferença entre maiúsculas e minúsculas (RN-PM-02) | Q51 |
| E-mail | Primeiro acesso; cadastro e edição de conta | texto | não | um @, com texto antes e um domínio com ponto depois | Q41, Q220 |
| Senha | Entrar | texto oculto | sim | até 20.000 caracteres | Protótipo |
| Senha nova | Primeiro acesso; cadastro de conta; troca e redefinição de senha | texto oculto | sim | de 8 a 20.000 caracteres (RN-PM-29) | Q51 |
| Confirmação da senha | Primeiro acesso; troca da própria senha | texto oculto | sim | igual à senha nova | Protótipo |
| Senha atual | troca da própria senha | texto oculto | sim | igual à senha da conta (RN-PM-33) | Q51 |
| Tipo da conta | cadastro e edição de conta | escolha | sim | gerente de projetos ou supervisor | Q7, Q52, Q210 |
| Papel de Administrador | cadastro e edição de conta | sim ou não | sim | "sim" só no tipo supervisor (RN-PM-06) | Q22, Q52 |
| Situação da conta | lista de contas | ativa ou desativada | sim | a conta de quem faz a mudança não vale para desativar (RN-PM-34) | Q52 |

**Funções**

| Código | Requisito | Regras | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|---|
| RF-US-01 | Enquanto o Octante não tem nenhuma conta, o sistema deve mostrar a tela Primeiro acesso, que cria a primeira conta com o nome, o login, o e-mail e a senha informados. | RN-PM-01, RN-PM-02, RN-PM-25 a RN-PM-29 | Q52, Q188 | alterado | App | 1 | teste |
| RF-US-02 | Quando uma pessoa informa o login e a senha de uma conta ativa e não bloqueada, o sistema deve abrir uma sessão e mostrar as telas que o tipo da conta e o papel dela permitem. | RN-PM-02 a RN-PM-04, RN-PM-30, RN-PM-31 | Q186, Q186b, Q187, Q196 | alterado | App | 1 | teste |
| RF-US-03 | Quando a pessoa pede para sair, o sistema deve encerrar a sessão dela. | — | Protótipo (Q209) | confirmado | App | 1 | teste |
| RF-US-04 | O sistema deve permitir que a pessoa troque a própria senha. | RN-PM-29, RN-PM-32, RN-PM-33 | Q51, Q187 | alterado | App | 1 | teste |
| RF-US-05 | O sistema deve permitir que o Administrador cadastre uma conta com nome, login, e-mail, senha inicial, tipo da conta e papel de Administrador. | RN-PM-02, RN-PM-05, RN-PM-06, RN-PM-29 | Q7, Q22, Q41, Q52, Q210 | alterado | App | 1 | teste |
| RF-US-06 | O sistema deve permitir que o Administrador redefina a senha de outra conta. | RN-PM-05, RN-PM-29, RN-PM-79 | Q52 | alterado | App | 1 | teste |
| RF-US-07 | O sistema deve permitir que o Administrador mude a situação de uma conta entre ativa e desativada. | RN-PM-05, RN-PM-34 a RN-PM-36, RN-PM-38 | Q28, Q32, Q52 | alterado | App | 1 | teste |
| RF-US-08 | O sistema deve mostrar ao Administrador a lista das contas, com o nome, o login, o tipo da conta, o papel de Administrador e a situação de cada uma. | RN-PM-05 | Q52, Q210 | alterado | App | 1 | teste |
| RF-US-09 | O sistema deve permitir que o Administrador edite o nome, o e-mail, o tipo e o papel de Administrador de uma conta. | RN-PM-05, RN-PM-06, RN-PM-35 | Q22, Q41, Q52 | novo | App | 1 | teste |

**Regras de negócio**

| Código | Regra | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RN-PM-01 | A primeira conta criada no Octante deve ter o tipo supervisor e o papel de Administrador. | Regra do PMO (Q52) | alterado | App | 1 | teste |
| RN-PM-02 | O login deve ser único no Octante e reconhecido sem diferença entre maiúsculas e minúsculas. | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-PM-03 | Depois de 5 senhas erradas seguidas para uma conta, vindas da mesma máquina, o sistema deve recusar o login dessa conta, a partir dessa máquina, por 5 minutos. | Regra do PMO (Q186, Q186b, Q220; OWASP ASVS 5.0, 6.1.1) | alterado | App | 1 | teste |
| RN-PM-04 | O sistema deve encerrar a sessão depois de 3 horas sem uso ou 12 horas depois do login, o que vier primeiro. | Regra do PMO (Q187; LGPD, art. 46) | alterado | App | 1 | teste |
| RN-PM-05 | O sistema deve recusar que uma conta sem o papel de Administrador veja a lista das contas, cadastre conta, edite conta, redefina a senha de outra conta ou mude a situação de uma conta. | Regra do PMO (Q52, Q231) | alterado | App | 1 | teste |
| RN-PM-06 | O papel de Administrador deve ficar somente em contas do tipo supervisor. | Regra do PMO (Q22, Q52) | alterado | App | 1 | teste |
| RN-PM-25 | O sistema deve criar a primeira conta somente quando o código de instalação informado for igual ao gerado na instalação. | Regra do PMO (Q188; OWASP ASVS 5.0, 6.3.2) | novo | App | 1 | teste |
| RN-PM-26 | Depois que a primeira conta existe, o sistema deve recusar o acesso à tela Primeiro acesso. | Regra do PMO (Q52, Q188) | novo | App | 1 | teste |
| RN-PM-27 | O código de instalação deve ficar visível somente nos arquivos do servidor ou no terminal do computador onde o Octante roda. | Regra do PMO (Q188) | novo | App | 1 | inspeção |
| RN-PM-28 | O Octante deve ser instalado sem nenhuma conta. | Regra do PMO (Q188; OWASP ASVS 5.0, 6.4.1) | novo | App | 1 | teste |
| RN-PM-29 | A senha deve ter pelo menos 8 caracteres. | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-PM-30 | O sistema deve identificar a máquina pelo endereço real de origem, informado pelo servidor do PythonAnywhere, e não pelo endereço do intermediário. | Regra do PMO (Q186b) | novo | App | 1 | teste |
| RN-PM-31 | A contagem das senhas erradas deve continuar valendo depois que o app reinicia. | Regra do PMO (Q186b) | novo | App | 1 | teste |
| RN-PM-32 | Quando a pessoa troca a própria senha, o sistema deve encerrar as outras sessões abertas da conta dela. | Regra do PMO (Q51, Q187) | confirmado | App | 1 | teste |
| RN-PM-33 | Para trocar a própria senha, a pessoa deve informar a senha atual. | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-PM-34 | O sistema deve recusar que uma pessoa desative a própria conta. | Regra do PMO (Q52) | confirmado | App | 1 | teste |
| RN-PM-35 | O sistema deve recusar a mudança que deixaria o Octante sem nenhum Administrador ativo. | Regra do PMO (Q52) | novo | App | 1 | teste |
| RN-PM-36 | O sistema deve recusar a desativação de uma conta que é o gerente do projeto de um projeto em andamento. | Regra do PMO (Q28, Q32, Q220) | novo | App | 1 | teste |
| RN-PM-37 | O sistema deve mostrar ao Administrador, no portfólio, um alerta médio quando um gerente de projetos ativo já foi gerente do projeto ou gerente de apoio e hoje não é nenhum dos dois em um projeto em andamento, com a ação sugerida de confirmar o desligamento e desativar a conta. | Regra do PMO (Q32, Q153, Q183) | novo | App | 1 | teste |
| RN-PM-38 | O sistema deve manter a conta desativada no Octante, com o nome dela no histórico. | Regra do PMO (Q28) | novo | App | 1 | teste |
| RN-PM-79 | O sistema deve encerrar as sessões abertas de uma conta quando o Administrador redefine a senha dela. | Regra do PMO (Q230) | novo | App | 1 | teste |

Na RN-PM-03, as outras contas e as outras máquinas não são afetadas. Na RN-PM-37, o gerente de projetos que nunca teve projeto não gera alerta (Q183).

Na RN-PM-03, um login certo zera a contagem das senhas erradas daquela conta naquela máquina (Q220).

#### 3.2.2 PMO (PM)

Pendências, revisão, aprovação registrada, documento gerado, visão do supervisor, parecer, busca, agenda, exportação, modelos de projeto e nível de exigência. A RN-PM-12, sobre as telas do Administrador, está na seção 3.2.3.

**Entradas**

| Entrada | Onde | Tipo | Obrigatória | Valores válidos | Origem |
|---|---|---|---|---|---|
| Decisão da revisão | revisar | escolha | sim | liberar ou devolver | Q14 |
| Comentário de devolução | revisar | texto | sim, ao devolver | até 20.000 caracteres | Q14, Q19 |
| Quem aprovou | registrar aprovação | escolha | sim | uma parte interessada do projeto (RN-PM-54) | Q69, Q109 |
| Data da aprovação | registrar aprovação | data | sim | uma data válida, até a data de hoje | Q14, Q220 |
| Pessoa avaliada | parecer | escolha | sim | uma conta do tipo gerente de projetos | Q20, Q210 |
| Texto do parecer | parecer | texto | sim | até 20.000 caracteres | Q20 |
| Prazo de guarda dos pareceres | configuração do Administrador | número inteiro de anos | sim | de 1 a 20; padrão 5 | Q25, Q220 |
| Texto da busca | busca | texto | sim | de 2 a 20.000 caracteres (RN-PM-22) | Q51 |
| Formato da exportação | exportar registros | escolha | sim | .xlsx ou .csv | Protótipo |
| Nível de exigência | configuração do projeto | escolha | sim | essencial ou rigoroso; padrão essencial (RN-PM-13) | Q17 |

**Funções**

| Código | Requisito | Regras | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|---|
| RF-PM-01 | O sistema deve mostrar a cada conta a tela Minhas pendências, com os registros dos projetos em andamento que esperam uma ação dela. | RN-PM-20, RN-PM-52, RN-PM-63 | Q9, Q10, Q14, Q17, Q22, Q27, Q35, Q43, Q51, Q55 | alterado | App | 1 | teste |
| RF-PM-02 | Quando o gerente do projeto ou o gerente de apoio envia um registro para revisão, o sistema deve registrar o pedido e mostrá-lo nas pendências do supervisor designado. | RN-PM-15, RN-PM-16, RN-PM-19, RN-PM-40, RN-PM-42, RN-PM-65 | Q9, Q10, Q14, Q27, Q35, Q43, Q51, Q56 | alterado | App | 1 | teste |
| RF-PM-03 | O sistema deve permitir que um supervisor libere ou devolva com comentário um registro enviado para revisão. | RN-PM-17, RN-PM-18, RN-PM-43, RN-PM-44, RN-PM-48, RN-PM-52 | Q8, Q9, Q10, Q14, Q15, Q17, Q22 | alterado | App | 1 | teste |
| RF-PM-04 | O sistema deve buscar um texto nos registros dos projetos visíveis para a conta e mostrar cada resultado com o projeto e o tipo de registro. | RN-PM-07, RN-PM-22 | Q9, Q27, Q35, Q43 | alterado | App | 1 | teste |
| RF-PM-05 | O sistema deve mostrar a agenda com os prazos dos registros dos projetos visíveis para a conta. | RN-PM-07 | Q9, Q27, Q35, Q43, Q67 | alterado | App | 1 | teste |
| RF-PM-06 | O sistema deve exportar a agenda de prazos num arquivo de calendário .ics. | RN-PM-07 | Q9, Q27, Q35, Q43 | alterado | App | 1 | teste |
| RF-PM-07 | O sistema deve exportar os riscos, as questões, as mudanças, as partes interessadas, o backlog e as lições aprendidas de um projeto numa planilha .xlsx ou num arquivo .csv, à escolha da pessoa. | RN-PM-07, RN-PM-39, RN-DA-14 | Q9, Q27, Q35, Q43, Q104, Q119 | alterado | App | 1 | teste |
| RF-PM-08 | Quando um supervisor cria um projeto a partir de um modelo de projeto, o sistema deve preencher o projeto com a abordagem, a cadência de entrega, a unidade de estimativa, o limite de trabalho em andamento, a definição de pronto e os riscos iniciais do modelo. | RN-PM-08, RN-PM-15 | Q27, Q56, Q127 | alterado | Núcleo | 1 | teste |
| RF-PM-09 | O sistema deve permitir que o supervisor designado defina o nível de exigência de um projeto. | RN-PM-13, RN-PM-14, RN-PM-64 | Q14, Q17, Q22 | alterado | Núcleo | 2 | teste |
| RF-PM-10 | O sistema deve permitir que o gerente do projeto ou o gerente de apoio registre a aprovação de um termo de abertura ou de uma mudança liberados, com quem aprovou e a data. | RN-PM-53, RN-PM-54 | Q14, Q62, Q69, Q109 | novo | App | 1 | teste |
| RF-PM-11 | O sistema deve gerar o documento do termo de abertura, da mudança, do relatório de status e do encerramento, para imprimir ou salvar em PDF. | RN-PM-18, RN-PM-45 a RN-PM-47 | Q11, Q15, Q104, Q119 | novo | App | 1 | teste |
| RF-PM-12 | O sistema deve mostrar ao supervisor o trabalho de cada gerente de projetos: os projetos de que ele é gerente, os registros em revisão e o resumo dos alertas de cada projeto, com os alertas altos em destaque. | RN-PM-07 | Q19, Q36, Q210 | novo | App | 2 | teste |
| RF-PM-13 | O sistema deve permitir que um supervisor escreva, em texto livre, um parecer sobre um gerente de projetos. | RN-PM-57, RN-PM-59, RN-PM-60 | Q19, Q20, Q24 | novo | App | 1 | teste |
| RF-PM-14 | Enquanto o supervisor escreve um parecer, o sistema deve mostrar os indicadores de apoio da pessoa avaliada: as devoluções, os relatórios de status atrasados e as pendências vencidas. | RN-PM-60 | Q23 | novo | App | 2 | teste |
| RF-PM-15 | O sistema deve mostrar ao supervisor os pareceres sobre uma pessoa, com a data e quem escreveu cada um. | RN-PM-55, RN-PM-56 | Q20, Q21, Q211 | novo | App | 1 | teste |
| RF-PM-16 | O sistema deve permitir que um supervisor gere o documento de um parecer, para imprimir ou salvar em PDF. | RN-PM-55, RN-PM-56, RN-PM-59 | Q24 | novo | App | 1 | teste |
| RF-PM-17 | O sistema deve permitir que o Administrador defina o prazo de guarda dos pareceres, em anos, com 5 anos de padrão. | RN-PM-58 | Q25, Q211 | novo | App | 1 | teste |
| RF-PM-18 | Quando o Administrador confirma a exclusão de um parecer com o prazo de guarda vencido, o sistema deve excluí-lo de vez, inclusive do histórico. | RN-PM-61, RN-PM-78, RN-DA-17, RN-DA-18 | Q25, Q59, Q194, Q221 | novo | App | 1 | teste |

**Regras de negócio**

| Código | Regra | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RN-PM-13 | O nível de exigência deve ser definido em cada projeto, com o nível essencial na criação. | Regra do PMO (Q17) | alterado | Núcleo | 2 | teste |
| RN-PM-14 | No nível rigoroso, o sistema deve exigir, para um registro ficar pronto para revisão, também os campos que as regras de cada domínio marcam como exigidos no nível rigoroso. | Regra do PMO (Q70, Q74, Q85, Q103, Q111, Q112) | alterado | Núcleo | 2 | teste |
| RN-PM-15 | O sistema deve mostrar em cada registro o estado pronto para revisão ou a lista dos campos que faltam, pelos campos que o nível de exigência do projeto pede. | Regra do PMO (Q56) | alterado | Núcleo | 2 | teste |
| RN-PM-16 | O termo de abertura, o relatório de status, a mudança, o encerramento e o tailoring devem passar por revisão obrigatória. | Regra do PMO (Q10, Q29, Q33) | alterado | App | 1 | teste |
| RN-PM-17 | A devolução deve ter um comentário. | Regra do PMO (Q14, Q19) | alterado | App | 1 | teste |
| RN-PM-18 | O sistema deve gerar o documento de um registro de revisão obrigatória somente depois que ele for liberado. | Regra do PMO (Q10, Q14, Q15) | alterado | App | 1 | teste |
| RN-PM-19 | O pedido de revisão deve guardar a conta de quem pediu. | Regra do PMO (Q51) | alterado | App | 1 | teste |
| RN-PM-20 | As pendências de uma conta devem trazer as questões não resolvidas, os riscos ativos e os itens de escopo a fazer, em andamento ou concluídos, dos projetos em andamento cujo responsável é o membro da equipe ligado a essa conta. | PMBOK 7 §4.6.2, p. 185 (Q55) | alterado | App | 1 | teste |
| RN-PM-22 | A busca deve exigir pelo menos 2 caracteres. | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-PM-39 | A planilha exportada por quem tem acesso de consulta deve sair sem a análise das partes interessadas e sem os dados pessoais dos membros da equipe. | PMBOK 7 §2.1.1.2, p. 12 (Q104, Q119; confirmação do resumo, 9.2) | novo | App | 1 | teste |
| RN-PM-40 | O sistema deve recusar o envio para revisão de um registro que não está pronto para revisão. | Regra do PMO (Q56) | novo | App | 2 | teste |
| RN-PM-41 | O sistema deve mostrar como "recomendado" o campo que o nível de exigência não pede, sem contá-lo como pendência. | Regra do PMO (Q56) | novo | Núcleo | 2 | teste |
| RN-PM-42 | Um registro deve ter no máximo um pedido de revisão pendente. | Regra do PMO (Q10, Q14) | confirmado | App | 1 | teste |
| RN-PM-43 | O sistema deve recusar a liberação e a devolução feitas por uma conta que não é do tipo supervisor. | Regra do PMO (Q2, Q14) | novo | App | 1 | teste |
| RN-PM-44 | O sistema deve aceitar a liberação ou a devolução feita por um supervisor que não é o designado, como substituto. | Regra do PMO (Q9) | novo | App | 1 | teste |
| RN-PM-45 | O documento gerado deve mostrar quem liberou o registro e a data da liberação. | Regra do PMO (Q15) | novo | App | 1 | teste |
| RN-PM-46 | O documento gerado deve sair sem a análise das partes interessadas e sem os dados pessoais dos membros da equipe. | PMBOK 7 §2.1.1.2, p. 12 (Q104, Q119) | novo | App | 1 | teste |
| RN-PM-47 | No documento gerado, um alerta sobre uma pessoa deve sair sem o nome dela. | Regra do PMO (Q104) | novo | App | 1 | teste |
| RN-PM-48 | Quando o gerente do projeto ou o gerente de apoio altera um registro liberado, o sistema deve tirar a liberação do registro. | Regra do PMO (Q15) | novo | App | 1 | teste |
| RN-PM-49 | Depois da edição feita por um supervisor, o sistema deve manter a liberação e o pedido de revisão do registro. | Regra do PMO (Q40) | novo | App | 1 | teste |
| RN-PM-50 | Quando um supervisor e um gerente do projeto ou gerente de apoio gravam o mesmo registro ao mesmo tempo, o sistema deve manter a versão do supervisor e mostrar ao gerente o que mudou. | Regra do PMO (Q34, Q40) | novo | App | 1 | teste |
| RN-PM-51 | O histórico deve marcar a edição feita por um supervisor como "editado pelo supervisor". | Regra do PMO (Q40) | novo | App | 1 | teste |
| RN-PM-52 | A devolução deve aparecer nas pendências de quem enviou o registro e nas do gerente do projeto. | Regra do PMO (Q8) | novo | App | 1 | teste |
| RN-PM-53 | O sistema deve recusar o registro da aprovação de um termo de abertura ou de uma mudança que não está liberado. | Regra do PMO (Q14) | novo | App | 1 | teste |
| RN-PM-54 | A aprovação deve registrar quem aprovou, escolhido entre as partes interessadas do projeto, e a data. | PMBOK 7 p. 184 e §2.6, p. 87 (Q14, Q69, Q109) | novo | App | 1 | teste |
| RN-PM-55 | O sistema deve mostrar os pareceres somente a contas do tipo supervisor. | Regra do PMO (Q21, Q58) | novo | App | 1 | teste |
| RN-PM-56 | O sistema deve recusar à pessoa avaliada o acesso aos pareceres sobre ela, inclusive depois que ela passa a supervisor. | Regra do PMO (Q21, Q211) | novo | App | 1 | teste |
| RN-PM-57 | A tela do parecer deve avisar a quem escreve que a pessoa avaliada recebe o parecer se pedir os próprios dados e o PMO aceitar o pedido. | Regra do PMO (Q191b; LGPD, arts. 18 e 19) | novo | App | 1 | teste |
| RN-PM-58 | O prazo de guarda de um parecer deve contar da data em que a pessoa avaliada deixa de ser gerente de projetos, pela desativação da conta ou pela mudança para supervisor. | Regra do PMO (Q25, Q211; LGPD) | novo | App | 1 | teste |
| RN-PM-59 | O sistema deve gerar o documento do parecer sem passar por revisão. | Regra do PMO (Q24) | novo | App | 1 | teste |
| RN-PM-60 | O parecer deve guardar só o texto escrito pelo supervisor, sem nota calculada a partir dos indicadores de apoio. | Regra do PMO (Q20, Q23) | novo | App | 1 | teste |
| RN-PM-61 | Quando o prazo de guarda de um parecer vence, o sistema deve mostrar ao Administrador, no portfólio, um alerta alto pedindo a confirmação da exclusão. | Regra do PMO (Q25, Q153, Q193, Q221) | novo | App | 1 | teste |
| RN-PM-62 | O sistema deve permitir que um supervisor edite os registros de um projeto em andamento. | Regra do PMO (Q34) | novo | App | 1 | teste |
| RN-PM-63 | As pendências de um supervisor devem trazer os pedidos de revisão dos projetos de que ele é o supervisor designado. | Regra do PMO (Q9) | novo | App | 1 | teste |
| RN-PM-64 | O sistema deve recusar a mudança do nível de exigência feita por quem não é o supervisor designado do projeto. | Regra do PMO (Q17) | novo | Núcleo | 2 | teste |
| RN-PM-65 | O sistema deve aceitar pedido de revisão opcional para o risco, a questão e o item de escopo. | Regra do PMO (Q10) | alterado | App | 1 | teste |
| RN-PM-78 | A tela de confirmação da exclusão de um parecer vencido deve mostrar de quem é o parecer e quando o prazo venceu, sem o texto do parecer. | Regra do PMO (Q221) | novo | App | 1 | teste |

**A confirmar:** os 5 anos de padrão da RF-PM-17 dependem da confirmação do RH ou do jurídico do PMO, que o responsável pelo produto obtém até a Entrega 1 (Q25). Os indicadores de apoio da RF-PM-14 dependem da cadência de relatório, que entra na Entrega 2. Na RN-PM-54, quem aprova o termo de abertura é o patrocinador, e quem aprova a mudança é a autoridade de mudança registrada no termo; essas regras estão nos domínios Planejamento e Trabalho do projeto, na parte 2 (Q14, Q69).

#### 3.2.3 Dados (DA)

Histórico, lixeira, backups, página de privacidade, pedidos do titular, anonimização e prazo de guarda.

**Entradas**

| Entrada | Onde | Tipo | Obrigatória | Valores válidos | Origem |
|---|---|---|---|---|---|
| Arquivo de backup | restaurar de arquivo | arquivo | sim | até 60 MB (RN-DA-36); um backup válido do Octante (RN-DA-35) | Q51 |
| Controlador | página Privacidade, pelo Administrador | texto | sim | até 20.000 caracteres | Q189 |
| Base legal | página Privacidade, pelo Administrador | escolha | sim | uma das hipóteses do art. 7º da LGPD | Q189, Q220 |
| Encarregado, com o nome e o contato | página Privacidade, pelo Administrador | texto | sim | até 20.000 caracteres | Q222 (LGPD, art. 41) |
| Pessoa do pedido | pedido do titular | escolha | sim | uma conta, uma parte interessada ou um membro da equipe | Q190 |
| Tipo do pedido | pedido do titular | escolha | sim | confirmação, acesso, correção ou eliminação | Q190 |
| Prazo de guarda dos projetos | tela Dados | número inteiro de anos | sim | de 1 a 20; padrão 5 | Q193, Q220 |

**Funções**

| Código | Requisito | Regras | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|---|
| RF-DA-01 | O sistema deve mostrar o histórico de um projeto, com os 300 eventos mais recentes, às contas para as quais o projeto é visível. | RN-DA-02, RN-DA-03, RN-DA-32, RN-PM-07 | Q58, Q191b, Q194, Q211 | alterado | App | 1 | teste |
| RF-DA-02 | O sistema deve mostrar ao Administrador a tela Dados, com os backups, a lixeira e o espaço usado pelo banco e pelos backups. | RN-PM-12 | Q195 | alterado | App | 3 | teste |
| RF-DA-03 | O sistema deve permitir que o Administrador faça um backup na hora. | RN-DA-09, RN-DA-10, RN-DA-22 | Q195 | alterado | App | 1 | teste |
| RF-DA-04 | O sistema deve permitir que o Administrador restaure da lixeira um projeto excluído. | RN-DA-04, RN-DA-05, RN-DA-33 | Protótipo (Q209) | confirmado | App | 1 | teste |
| RF-DA-05 | O sistema deve permitir que o Administrador restaure da lixeira um registro excluído. | RN-DA-04, RN-DA-05, RN-DA-33 | Protótipo (Q209) | confirmado | App | 1 | teste |
| RF-DA-06 | O sistema deve permitir que o Administrador restaure um backup da lista. | RN-DA-19, RN-DA-34, RN-DA-35 | Q194 | alterado | App | 1 | teste |
| RF-DA-07 | O sistema deve permitir que o Administrador restaure um backup a partir de um arquivo enviado. | RN-DA-19, RN-DA-34 a RN-DA-36 | Q194 | alterado | App | 1 | teste |
| RF-DA-08 | O sistema deve permitir que o Administrador baixe um backup da lista. | RN-DA-20, RN-DA-21 | Q44, Q184 | alterado | App | 3 | teste |
| RF-DA-09 | O sistema deve permitir que o Administrador baixe uma cópia consistente do banco. | RN-DA-20, RN-DA-21 | Q44, Q184 | alterado | App | 3 | teste |
| RF-DA-10 | O sistema deve permitir que o Administrador anonimize um projeto encerrado ou cancelado. | RN-DA-12, RN-DA-13, RN-DA-26, RN-DA-27, RN-DA-37 a RN-DA-42 | Q59, Q192, Q193 | alterado | App | 2 | teste |
| RF-DA-11 | O sistema deve mostrar a página Privacidade, também antes do login, com um link na tela Entrar e no rodapé, e com o texto sobre os itens do art. 9º da LGPD. | RN-DA-29 | Q189, Q196 | novo | App | 1 | teste |
| RF-DA-12 | O sistema deve permitir que o Administrador preencha, na página Privacidade, o controlador, o encarregado, com o nome e o contato, e a base legal. | RN-PM-12 | Q189, Q222 | novo | App | 1 | teste |
| RF-DA-13 | O sistema deve permitir que o Administrador gere um arquivo com os dados de uma pessoa (conta, parte interessada ou membro da equipe) em cada projeto em que ela aparece. | — | Q190 | novo | App | 2 | teste |
| RF-DA-14 | O sistema deve permitir que um supervisor gere o arquivo dos dados de uma pessoa somente com os projetos de que ele é o supervisor designado. | — | Q190 (confirmação do resumo, 9.2) | novo | App | 2 | teste |
| RF-DA-15 | Depois de um pedido de eliminação aceito pelo PMO, o sistema deve permitir que o Administrador anonimize uma pessoa, inclusive em projeto em andamento. | RN-DA-26, RN-DA-28 | Q190, Q192 | novo | App | 2 | teste |
| RF-DA-16 | O sistema deve registrar cada pedido do titular atendido, com o tipo, a pessoa e a data. | — | Q190 | novo | App | 2 | teste |
| RF-DA-17 | No pedido de acesso de uma pessoa que é ou foi gerente de projetos, o sistema deve permitir que o Administrador inclua no arquivo os pareceres sobre ela, depois de um aviso. | RN-PM-55, RN-PM-56 | Q191b, Q211 | novo | App | 2 | teste |
| RF-DA-18 | O sistema deve permitir que o Administrador defina o prazo de guarda dos projetos encerrados ou cancelados, em anos, com 5 anos de padrão. | RN-DA-25 | Q193 | novo | App | 2 | teste |
| RF-DA-19 | Antes de excluir um registro ou um projeto, o sistema deve mostrar uma tela de confirmação, gerada pelo servidor, com o que vai ser excluído. | RN-DA-06, RN-DA-31 | Q51, Q198 | novo | App | 1 | teste |

**Regras de negócio**

| Código | Regra | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RN-PM-12 | O sistema deve abrir as telas Usuários, Dados, Lixeira e Backups e a anonimização somente para o Administrador. | Regra do PMO (Q2, Q14, Q17, Q22) | alterado | App | 1 | teste |
| RN-DA-01 | O histórico deve registrar cada inclusão, alteração e exclusão de registro, com quem, quando, o valor anterior, o valor novo e o lote da operação. | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-DA-02 | O histórico deve omitir o hash da senha. | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-DA-03 | O sistema deve mostrar os eventos de histórico de um parecer somente a supervisores que não são a pessoa avaliada. | Regra do PMO (Q58, Q191b, Q211; LGPD) | alterado | App | 1 | teste |
| RN-DA-04 | A lixeira deve restaurar um projeto excluído inteiro, com o lote completo da exclusão, ou um registro avulso. | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-DA-05 | A restauração da lixeira deve ignorar os registros que já existem. | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-DA-06 | A tela de confirmação de exclusão deve informar que o Administrador desfaz a exclusão pela lixeira. | Regra do PMO (Q51, Q198) | alterado | App | 1 | teste |
| RN-DA-07 | O sistema deve fazer o backup automático no primeiro acesso depois de 20 horas do backup automático anterior, conferindo essa condição no máximo uma vez por hora. | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-DA-08 | O sistema deve pular o backup automático quando o banco não tem projetos. | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-DA-09 | Cada backup deve passar pela verificação de integridade do banco e receber uma assinatura SHA-256. | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-DA-10 | O sistema deve guardar os 14 backups automáticos mais recentes e os 5 mais recentes de cada outro motivo. | Regra do PMO (Q51, Q195) | confirmado | App | 1 | teste |
| RN-DA-11 | Cada campo de formulário deve aceitar até 20.000 caracteres. | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-DA-12 | O sistema deve permitir a anonimização de um projeto somente ao Administrador e somente com o projeto encerrado ou cancelado. | Regra do PMO (Q59, Q192; LGPD) | confirmado | App | 2 | teste |
| RN-DA-13 | A anonimização de um projeto deve trocar o nome de cada parte interessada e de cada membro da equipe por um rótulo neutro, como "Parte 1" e "Membro 1". | Regra do PMO (Q192; LGPD, arts. 5º e 12) | alterado | App | 2 | teste |
| RN-DA-14 | Na exportação, o sistema deve pôr um apóstrofo no início de cada célula que começa com =, +, −, @, tabulação ou retorno de linha. | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-DA-15 | O banco deve recusar, além da tela, os valores fora das faixas válidas: probabilidade e impacto de 1 a 5; aquisição com valor maior ou igual a 0 e nota de 1 a 5; item com estimativa e custos maiores ou iguais a 0 e valor de 1 a 5; iteração com o fim igual ao início ou depois dele e capacidade maior ou igual a 0; recurso com quantidade e uso maiores ou iguais a 0 e desperdício até o uso; conta com o papel e a situação em 0 ou 1 e o hash de senha válido. | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-DA-16 | O sistema deve calcular as datas e as horas no fuso configurado, com o de Brasília (America/Sao_Paulo) como padrão, também no Windows. | Regra do PMO (Q51, Q206) | alterado | App | 1 | teste |
| RN-DA-17 | O banco deve recusar a alteração e a exclusão de linhas do histórico, exceto pelas rotinas da anonimização e da exclusão do parecer vencido. | Regra do PMO (Q194; LGPD, arts. 6º, X, e 37) | novo | App | 1 | teste |
| RN-DA-18 | Cada rotina que apaga linhas do histórico deve deixar um evento com o que foi apagado, quando e por quem, sem o conteúdo apagado. | Regra do PMO (Q194) | novo | App | 1 | teste |
| RN-DA-19 | Ao restaurar um backup, o sistema deve gravar no histórico restaurado quem restaurou, quando e de qual arquivo. | Regra do PMO (Q194) | novo | App | 1 | teste |
| RN-DA-20 | O sistema deve registrar a data e a conta de cada download de backup e de cópia do banco. | Regra do PMO (Q184) | novo | App | 3 | teste |
| RN-DA-21 | Quando passam mais de 7 dias sem download de backup ou de cópia do banco, o sistema deve mostrar ao Administrador, no portfólio, um alerta alto; sem nenhum download, os 7 dias contam da criação do primeiro projeto. | Regra do PMO (Q44, Q153, Q184) | novo | App | 3 | teste |
| RN-DA-22 | Os backups devem ser compactados. | Regra do PMO (Q195) | novo | App | 1 | teste |
| RN-DA-23 | Quando o banco e os backups juntos passam de 400 MB, o sistema deve mostrar ao Administrador, no portfólio, um alerta médio. | Regra do PMO (Q153, Q195) | novo | App | 3 | teste |
| RN-DA-24 | Quando um backup automático falha, o sistema deve mostrar ao Administrador, no portfólio, um alerta alto. | Regra do PMO (Q153, Q195) | novo | App | 1 | teste |
| RN-DA-25 | Quando o prazo de guarda de um projeto encerrado ou cancelado vence, o sistema deve mostrar ao Administrador, no portfólio, um alerta alto pedindo a anonimização. | Regra do PMO (Q153, Q193; LGPD, arts. 15 e 16) | novo | App | 2 | teste |
| RN-DA-26 | A anonimização deve acontecer somente por ação do Administrador. | Regra do PMO (Q193) | novo | App | 2 | teste |
| RN-DA-27 | O projeto anonimizado deve continuar disponível para consulta. | Regra do PMO (Q193; LGPD, art. 16, IV) | novo | App | 2 | teste |
| RN-DA-28 | A anonimização de uma pessoa deve aplicar aos registros dela, em cada projeto, o que a anonimização do projeto aplica a cada parte interessada e a cada membro da equipe. | Regra do PMO (Q190, Q192) | novo | App | 2 | teste |
| RN-DA-29 | O sistema deve pedir consentimento somente quando a base legal escolhida pelo PMO for o consentimento. | Regra do PMO (Q189; LGPD, art. 7º) | novo | App | 1 | teste |
| RN-DA-30 | Num campo obrigatório, o sistema deve tratar como vazio o texto feito só de espaços. | Regra do PMO (Q77, Q220) | novo | App | 1 | teste |
| RN-DA-31 | O servidor deve excluir um registro somente depois da confirmação na tela da RF-DA-19, também sem JavaScript e também na linha da matriz RACI. | Regra do PMO (Q198) | novo | App | 1 | teste |
| RN-DA-32 | O histórico deve ignorar a alteração que muda só a data de atualização do registro. | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-DA-33 | O sistema deve desfazer a restauração da lixeira que deixaria um registro sem o seu registro pai. | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-DA-34 | O sistema deve fazer um backup antes de cada migração do banco e antes de cada restauração. | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-DA-35 | A restauração deve recusar o arquivo que não é um banco SQLite, que está corrompido, que não é do Octante, cuja assinatura não confere ou que vem de uma versão mais nova do app. | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-DA-36 | O arquivo de backup enviado deve ter até 60 MB. | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-DA-37 | A anonimização de um projeto deve apagar o contato, as crenças, as expectativas, o e-mail e a análise de cada parte interessada. | Regra do PMO (Q59, Q192; LGPD) | alterado | App | 2 | teste |
| RN-DA-38 | A anonimização de um projeto deve apagar os textos dos contatos com as partes interessadas. | Regra do PMO (Q59) | novo | App | 2 | teste |
| RN-DA-39 | A anonimização de um projeto deve apagar as habilidades, as lacunas, o plano de desenvolvimento e o motivador de cada membro da equipe. | Regra do PMO (Q119) | novo | App | 2 | teste |
| RN-DA-40 | A anonimização de um projeto deve apagar o histórico e a lixeira do projeto. | Regra do PMO (Q59) | novo | App | 2 | teste |
| RN-DA-41 | A anonimização de um projeto deve desfazer a ligação de cada membro da equipe com a conta e com a parte interessada. | Regra do PMO (Q192) | novo | App | 2 | teste |
| RN-DA-42 | A tela de anonimização deve avisar que os textos livres não são varridos e podem citar nomes. | Regra do PMO (Q192) | novo | App | 2 | teste |

As contas não mudam com a anonimização de um projeto (Q192). Os dados apagados pela anonimização continuam nos backups antigos até a rotação da RN-DA-10 descartá-los (Q59). A parte da regra do protótipo sobre restaurar contas excluídas deixou de valer, porque a conta é desativada, e não excluída (RN-PM-38).

**A confirmar:** os 5 anos de padrão da RF-DA-18 dependem da mesma confirmação da RF-PM-17, até a Entrega 2 (Q193).

#### 3.2.4 Projetos (PJ)

Portfólio, criação do projeto pelo supervisor, gerentes do projeto, acesso de consulta, cadência de relatório, visão geral e projeto de exemplo. As regras de projeto têm o código RN-PM, do inventário do protótipo. As regras RN-AB e RN-GU citadas na coluna Regras são descritas na parte 2 (Abordagem) e na parte 3 (Guia).

**Entradas**

| Entrada | Onde | Tipo | Obrigatória | Valores válidos | Origem |
|---|---|---|---|---|---|
| Nome do projeto | criar e editar projeto | texto | sim | até 20.000 caracteres | Protótipo |
| Descrição | criar e editar projeto | texto | não | até 20.000 caracteres | Protótipo |
| Modelo de projeto | criar projeto | escolha | não | em branco, software adaptativo, software híbrido ou implantação e infraestrutura (preditivo) | Q127 |
| Cadência de entrega | criar e editar projeto | escolha | não | entrega única, múltiplas entregas, entregas periódicas ou entrega contínua (PMBOK 7 §2.3.2) | Protótipo |
| Gerente do projeto | gerentes do projeto | escolha | sim | uma conta ativa do tipo gerente de projetos (RN-PM-68) | Q27, Q60 |
| Gerente de apoio | gerentes do projeto | escolha | não | uma conta ativa do tipo gerente de projetos, diferente do gerente do projeto (RN-PM-68) | Q8 |
| Cadência de relatório | configuração do projeto | número inteiro de dias | não | de 1 a 90; sem cadência, não há alerta de relatório atrasado | Q16, Q220 |
| Conta com acesso de consulta | acesso de consulta | escolha | sim | uma conta ativa do tipo gerente de projetos que não é gerente do projeto nem gerente de apoio dele | Q35, Q43 |

**Funções**

| Código | Requisito | Regras | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|---|
| RF-PJ-01 | O sistema deve listar os projetos visíveis para a conta, do mais recente ao mais antigo, com o número de partes interessadas ativas de cada um. | RN-PM-07, RN-PM-10, RN-PM-72 | Q9, Q27, Q35, Q43 | alterado | App | 1 | teste |
| RF-PJ-02 | O sistema deve permitir que um supervisor crie um projeto com nome, descrição, modelo de projeto e cadência de entrega. | RN-PM-08, RN-PM-15, RN-PM-66, RN-AB-02, RN-AB-08 a RN-AB-10, RN-GU-06 | Q27, Q56, Q114, Q122, Q127, Q128 | alterado | Núcleo | 1 | teste |
| RF-PJ-03 | O sistema deve mostrar a visão geral do projeto: o grupo de processos em que ele está, o próximo passo, o semáforo, os pontos de atenção, os resumos dos registros, o progresso dos domínios de desempenho e, quando o módulo Princípios e resultados está ligado, o progresso dos princípios. | RN-PM-07, RN-PM-15, RN-PM-24, RN-AB-01, RN-AB-09 a RN-AB-12, RN-GU-02 a RN-GU-05 | Q9, Q27, Q35, Q43, Q56, Q127, Q128, Q149, Q150, Q174a, Q179 | alterado | Núcleo | 2 | teste |
| RF-PJ-04 | O sistema deve permitir que o gerente do projeto, o gerente de apoio e os supervisores editem o nome, a descrição e a cadência de entrega do projeto. | RN-PM-07, RN-PM-23, RN-PM-71, RN-AB-02 | Q9, Q27, Q34, Q35, Q43, Q122 | alterado | Núcleo | 1 | teste |
| RF-PJ-05 | O sistema deve permitir que o supervisor designado escolha e troque o gerente do projeto e o gerente de apoio. | RN-PM-09, RN-PM-67 a RN-PM-69, RN-PM-77 | Q8, Q27, Q28, Q32, Q114 | alterado | Núcleo | 1 | teste |
| RF-PJ-06 | O sistema deve permitir que o Administrador exclua um projeto criado por engano, depois da tela de confirmação, mandando o projeto para a lixeira. | RN-PM-11, RN-DA-06, RN-DA-31 | Q51, Q54, Q198 | alterado | App | 1 | teste |
| RF-PJ-07 | O sistema deve mostrar o portfólio dos projetos visíveis para a conta, com o semáforo, o grupo de processos, a próxima etapa, os alertas e as revisões pendentes de cada projeto, e, para o Administrador, os alertas do Administrador. | RN-PM-07, RN-PM-21, RN-PM-37, RN-PM-61, RN-DA-21, RN-DA-23 a RN-DA-25, RN-AB-01, RN-GU-02 a RN-GU-04 | Q9, Q17, Q27, Q35, Q36, Q43, Q150, Q183, Q184, Q193, Q195, Q203 | alterado | App | 1 | teste |
| RF-PJ-08 | Quando o módulo Princípios e resultados está ligado no projeto, o sistema deve mostrar o checklist dos 8 domínios de desempenho, com o progresso de cada domínio. | RN-PM-07, RN-PM-24 | Q9, Q27, Q35, Q43, Q174a | alterado | Princípios e resultados | 3 | teste |
| RF-PJ-09 | Quando o módulo Princípios e resultados está ligado no projeto, o sistema deve mostrar a verificação dos resultados de um domínio de desempenho, pelas tabelas 2-2 a 2-10 do PMBOK 7, com os indicadores. | RN-PM-07, RN-PM-24, RN-AB-01 a RN-AB-03, RN-GU-02, RN-GU-04, RN-GU-05 | Q9, Q27, Q35, Q43, Q92, Q122, Q174a | alterado | Princípios e resultados | 3 | teste |
| RF-PJ-10 | O sistema deve permitir que o supervisor designado defina a cadência de relatório do projeto. | RN-PM-76 | Q16 | novo | Núcleo | 2 | teste |
| RF-PJ-11 | O sistema deve permitir que um supervisor conceda e retire o acesso de consulta de um gerente de projetos a um projeto. | RN-PM-70, RN-PM-71 | Q35, Q43 | novo | App | 1 | teste |
| RF-PJ-12 | O sistema deve permitir que o Administrador recrie o projeto de exemplo. | RN-PM-10, RN-PM-73, RN-PM-74 | Q53 | novo | App | 1 | teste |

**Regras de negócio**

| Código | Regra | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RN-PM-07 | O sistema deve mostrar um projeto a uma conta somente quando ela é do tipo supervisor, é o gerente do projeto ou o gerente de apoio dele, ou tem acesso de consulta a ele. | Regra do PMO (Q9, Q27, Q35, Q43) | alterado | App | 1 | teste |
| RN-PM-08 | O supervisor que cria um projeto deve ficar como o supervisor designado dele. | Regra do PMO (Q9, Q27) | alterado | Núcleo | 1 | teste |
| RN-PM-09 | Somente o supervisor designado deve escolher e trocar o gerente do projeto e o gerente de apoio. | Regra do PMO (Q27) | alterado | Núcleo | 1 | teste |
| RN-PM-10 | O Octante deve ter um único projeto de exemplo, visível para cada conta. | Regra do PMO (Q53) | alterado | App | 1 | teste |
| RN-PM-11 | O sistema deve permitir a exclusão de um projeto somente ao Administrador e somente quando o projeto não tem registro liberado nem aprovado. | Regra do PMO (Q54) | alterado | App | 1 | teste |
| RN-PM-21 | O portfólio deve listar primeiro os projetos em andamento e depois os encerrados e os cancelados; em cada grupo, vêm antes os projetos com mais dimensões vermelhas no semáforo, depois os com mais amarelas, e por fim a ordem do nome. | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-PM-23 | O sistema deve recusar gravações num projeto encerrado ou cancelado, exceto a reabertura pelo supervisor e as anonimizações das RF-DA-10 e RF-DA-15. | Regra do PMO (Q29, Q65) | alterado | Núcleo | 1 | teste |
| RN-PM-24 | O sistema deve recusar o acesso às telas de um módulo opcional desligado no projeto, também pelo endereço da tela. | Regra do PMO (Q57, Q174a) | alterado | Núcleo | 2 | teste |
| RN-PM-66 | O sistema deve recusar a criação de projeto por quem não é supervisor. | Regra do PMO (Q27) | novo | Núcleo | 1 | teste |
| RN-PM-67 | Um projeto deve ter exatamente um gerente do projeto e no máximo um gerente de apoio. | Regra do PMO (Q4, Q8) | novo | Núcleo | 1 | teste |
| RN-PM-68 | O gerente do projeto e o gerente de apoio devem ser contas ativas do tipo gerente de projetos, diferentes entre si. | Regra do PMO (Q60, Q210) | novo | Núcleo | 1 | teste |
| RN-PM-69 | O sistema deve incluir o gerente do projeto na equipe com o papel "Gerente do projeto" e o gerente de apoio com o papel "Equipe de gerenciamento do projeto". | PMBOK 7 §2.2, p. 16 (Q114) | novo | Núcleo | 1 | teste |
| RN-PM-70 | Somente um supervisor deve conceder e retirar o acesso de consulta. | Regra do PMO (Q43) | alterado | App | 1 | teste |
| RN-PM-71 | O sistema deve recusar gravações de uma conta que tem só acesso de consulta ao projeto. | Regra do PMO (Q35) | novo | App | 1 | teste |
| RN-PM-72 | Para uma conta à qual o projeto não é visível, o sistema deve responder "não encontrado". | Regra do PMO (Q51) | confirmado | App | 1 | teste |
| RN-PM-73 | Somente o Administrador deve recriar o projeto de exemplo. | Regra do PMO (Q53) | novo | App | 1 | teste |
| RN-PM-74 | O sistema deve recusar gravações no projeto de exemplo, exceto a recriação pelo Administrador. | Regra do PMO (Q53) | novo | App | 1 | teste |
| RN-PM-75 | Quando um módulo opcional é religado no projeto, o sistema deve mostrar de novo os dados que ele tinha. | Regra do PMO (Q57) | novo | Núcleo | 2 | teste |
| RN-PM-76 | O sistema deve recusar a mudança da cadência de relatório feita por quem não é o supervisor designado do projeto. | Regra do PMO (Q16) | novo | Núcleo | 2 | teste |
| RN-PM-77 | Quando o supervisor designado troca o gerente do projeto ou o gerente de apoio, o sistema deve trocar junto o membro da equipe correspondente. | PMBOK 7 §2.2, p. 16 (Q114) | novo | Núcleo | 1 | teste |

Os alertas do portfólio entram na entrega da regra de cada um. O supervisor não entra na equipe do projeto, porque é do PMO (Q114).

#### Domínios de desempenho (parte 2)

As seções 3.2.5 a 3.2.12 seguem os oito domínios de desempenho, na ordem do PMBOK 7. Nelas, valem para cada função as regras de acesso da parte 1: quem grava num projeto são o gerente do projeto, o gerente de apoio e os supervisores (RN-PM-62); quem tem acesso de consulta só lê (RN-PM-71); o projeto encerrado ou cancelado fica só para consulta (RN-PM-23); e a exclusão passa pela tela de confirmação (RF-DA-19, RN-DA-31). Uma função de módulo opcional só aparece com o módulo ligado no projeto (RN-PM-24). Os alertas seguem os níveis da Q153: alto, médio e informativo; o alerta não bloqueia nada e mostra a origem da regra.

#### 3.2.5 Partes interessadas (PI)

Identificar, analisar, priorizar, engajar e monitorar as partes interessadas (PMBOK 7, Figura 2-3, p. 10). O registro, a análise, a priorização, o plano de comunicação e os contatos ficam no núcleo; a saliência, a matriz de engajamento e a nota de satisfação ficam no módulo Engajamento das partes (Q31, Q108).

**Entradas**

| Entrada | Onde | Tipo | Obrigatória | Valores válidos | Origem |
|---|---|---|---|---|---|
| Nome | cadastro e edição da parte | texto | sim | até 20.000 caracteres; único no projeto (RN-PI-02) | Q111 |
| Categoria | cadastro e edição da parte | escolha | sim | a lista da RN-PI-06 | Q170 |
| Papel | cadastro e edição da parte | texto | no nível rigoroso (RN-PI-04) | até 20.000 caracteres | Q17 |
| Interna | cadastro e edição da parte | sim ou não | sim | padrão sim | Q111 |
| Ativa | cadastro e edição da parte | sim ou não | sim | padrão sim | Q110, Q111 |
| E-mail | cadastro e edição da parte | texto | não | um @, com texto antes e um domínio com ponto depois | Q41, Q220 |
| Poder, interesse, influência e impacto | cadastro, edição e análise | número inteiro | não | de 1 a 5 (RN-PI-07) | Q113 |
| Atitude | cadastro, edição e análise | escolha | sim | apoiador, neutro, opositor ou desconhecida; padrão desconhecida (RN-PI-08) | Q113 |
| Proximidade | cadastro e edição da parte | escolha | não | direta, próxima ou distante (RN-PI-09) | Q113 |
| Crenças e expectativas | cadastro e edição da parte | texto | não | até 20.000 caracteres | Q104 |
| Atributos de saliência | análise, no módulo Engajamento das partes | marcar | não | poder de influenciar, legitimidade e urgência | Q107b |
| Nível atual e nível desejado de engajamento | matriz de engajamento, no módulo | número inteiro | não | de 1 a 5 (RN-PI-16) | Q106b |
| Método de comunicação | plano de comunicação | escolha | não | push, pull ou interativo | PMBOK 7 Tabela 2-1 |
| Tipo de comunicação | plano de comunicação | escolha | não | verbal formal, verbal informal, escrito formal ou escrito informal | PMBOK 7 p. 13 |
| Frequência | plano de comunicação | escolha | não | diária, semanal, quinzenal, mensal, por marco ou fase, por iteração ou sob demanda (RN-PI-19) | Q169a |
| Quem conduz a comunicação | plano de comunicação | escolha | não | um membro da equipe do projeto | Q106b |
| Ordem manual | priorização | número inteiro | não | de 1 a 1.000.000 (RN-PI-38) | Protótipo |
| Parte do contato | registrar contato | escolha | sim | uma parte interessada do projeto (RN-PI-22) | Protótipo |
| Data do contato | registrar contato | data | não | até a data de hoje; vazia ou inválida vira hoje (RN-PI-21, RN-PI-40) | Q108 |
| Forma e resumo do contato | registrar contato | texto | não | até 20.000 caracteres | Q108 |
| Nota de satisfação | registrar contato, no módulo | número inteiro | não | de 1 a 5 (RN-PI-41) | Q108 |

**Funções**

| Código | Requisito | Regras | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|---|
| RF-PI-01 | O sistema deve mostrar o registro das partes interessadas do projeto, com o resumo das cinco etapas: identificar, entender e analisar, priorizar, engajar e monitorar. | RN-PI-06, RN-PI-08, RN-PI-10, RN-PI-13, RN-PI-18, RN-PI-23, RN-PI-24, RN-PI-36 | Q104, Q105b, Q106b, Q169a, Q170 | alterado | Núcleo | 2 | teste |
| RF-PI-02 | O sistema deve permitir cadastrar uma parte interessada, com a opção de salvar e cadastrar outra. | RN-PI-01, RN-PI-02, RN-PI-04 a RN-PI-09, RN-PI-34, RN-PI-35 | Q41, Q104, Q105b, Q106b, Q169a, Q170 | alterado | Núcleo | 2 | teste |
| RF-PI-03 | O sistema deve mostrar o detalhe de uma parte interessada, com os contatos, os riscos ligados a ela e, com o módulo Engajamento das partes ligado, o histórico de engajamento. | RN-PI-20, RN-PI-36 | Q104, Q105b, Q106b, Q169a | alterado | Núcleo | 2 | teste |
| RF-PI-04 | O sistema deve permitir editar uma parte interessada, inclusive para inativá-la. | RN-PI-01, RN-PI-03, RN-PI-04, RN-PI-06 a RN-PI-09, RN-PI-24, RN-PI-34, RN-PI-35 | Q41, Q104, Q105b, Q106b, Q110, Q111, Q169a, Q170 | alterado | Núcleo | 2 | teste |
| RF-PI-05 | O sistema deve permitir excluir uma parte interessada sem contatos e sem vínculos. | RN-PI-31, RN-PM-72, RN-DA-31 | Q110, Q198 | alterado | Núcleo | 2 | teste |
| RF-PI-06 | O sistema deve permitir analisar as partes interessadas em lote: poder, interesse, influência, impacto, atitude e, com o módulo Engajamento das partes ligado, os atributos de saliência. | RN-PI-07, RN-PI-08, RN-PI-10, RN-PI-12, RN-PI-34 a RN-PI-36 | Q104, Q105b, Q106b, Q107b | alterado | Núcleo | 2 | teste |
| RF-PI-07 | O sistema deve permitir definir a ordem de prioridade das partes interessadas: gravar a ordem sugerida, ajustar a ordem manual ou limpá-la. | RN-PI-13 a RN-PI-15, RN-PI-37 a RN-PI-39 | Q105b | alterado | Núcleo | 2 | teste |
| RF-PI-08 | O sistema deve permitir registrar o plano de comunicação de cada parte interessada: o método, o tipo, a frequência e quem conduz a comunicação. | RN-PI-18, RN-PI-19 | Q106b, Q169a | alterado | Núcleo | 2 | teste |
| RF-PI-09 | O sistema deve permitir registrar um contato com uma parte interessada, com a data, a forma, o resumo e, com o módulo Engajamento das partes ligado, a nota de satisfação. | RN-PI-21, RN-PI-22, RN-PI-40, RN-PI-41 | Q108 | alterado | Núcleo | 2 | teste |
| RF-PI-10 | O sistema deve permitir excluir um contato. | RN-PI-32, RN-PM-72, RN-DA-31 | Q198 | alterado | Núcleo | 1 | teste |
| RF-PI-11 | O sistema deve mostrar o diagrama de dispersão de poder por interesse das partes analisadas, sem quadrantes e sem nomes de quadrantes. | RN-PI-07, RN-PI-10, RN-PI-24 | Q105b | novo | Núcleo | 2 | teste |
| RF-PI-12 | Com o módulo Engajamento das partes ligado, o sistema deve mostrar a matriz de engajamento, com o nível atual e o desejado de cada parte. | RN-PI-16, RN-PI-17, RN-PI-20 | Q106b | alterado | Engajamento das partes | 3 | teste |
| RF-PI-13 | O sistema deve mostrar o monitoramento das partes: os 50 contatos mais recentes, as mudanças de nível de engajamento, com o módulo ligado, e os alertas do domínio. | RN-PI-23, RN-PI-25 a RN-PI-30, RN-PI-42, RN-PI-43 | Q108, Q163, Q164, Q169a, Q171 | alterado | Núcleo | 3 | teste |

**Regras de negócio**

| Código | Regra | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RN-PI-01 | A parte interessada deve ter nome. | Regra do PMO (Q111) | confirmado | Núcleo | 2 | teste |
| RN-PI-02 | O nome da parte interessada deve ser único no projeto, sem diferença entre maiúsculas e minúsculas. | Regra do PMO (Q111) | confirmado | Núcleo | 2 | teste |
| RN-PI-03 | O sistema deve recusar também na edição o nome de uma parte que já existe no projeto. | Regra do PMO (Q111) | alterado | Núcleo | 2 | teste |
| RN-PI-04 | No nível rigoroso, a parte interessada deve ter o papel preenchido. | Regra do PMO (Q17, Q111) | confirmado | Núcleo | 2 | teste |
| RN-PI-05 | Uma parte interessada nova deve começar interna, ativa e com a atitude desconhecida. | Regra do PMO (Q111) | confirmado | Núcleo | 2 | teste |
| RN-PI-06 | A parte interessada deve ter uma categoria: gerente do projeto, equipe de gerenciamento, equipe do projeto, órgão de governança, PMO, comitê diretor, patrocinador, fornecedor, cliente, usuário final, órgão regulador ou outro. | PMBOK 7 Figura 2-2, p. 9; §4.6.2, p. 185 (Q170) | alterado | Núcleo | 2 | teste |
| RN-PI-07 | Poder, interesse, influência e impacto devem ir de 1 a 5. | PMBOK 7 p. 11; a escala é regra do PMO (Q113) | confirmado | Núcleo | 2 | teste |
| RN-PI-08 | A atitude deve ser apoiador, neutro, opositor ou desconhecida. | PMBOK 7 p. 10; Tabela 2-2, p. 15 (Q113) | confirmado | Núcleo | 2 | teste |
| RN-PI-09 | A proximidade deve ser direta, próxima ou distante. | PMBOK 7 p. 11; os valores são regra do PMO (Q113) | confirmado | Núcleo | 2 | teste |
| RN-PI-10 | A parte interessada deve contar como analisada quando tem poder, interesse e uma atitude diferente de desconhecida. | PMBOK 7 p. 11; os três aspectos são regra do PMO (Q105b, Q113) | confirmado | Núcleo | 2 | teste |
| RN-PI-12 | O sistema deve mostrar quais dos três atributos de saliência a parte tem (poder de influenciar, legitimidade e urgência) e quantos, de 0 a 3. | PMBOK 7 §4.2.7.5, p. 171 (Q107b) | alterado | Engajamento das partes | 3 | teste |
| RN-PI-13 | A ordem de prioridade exibida deve seguir a ordem manual, depois o produto de poder por interesse, do maior para o menor, e por fim o nome. | PMBOK 7 §2.1.1.3, p. 12 (Q105b) | alterado | Núcleo | 2 | teste |
| RN-PI-14 | A ordem sugerida deve seguir o produto de poder por interesse, do maior para o menor, depois a influência, da maior para a menor, e por fim o nome. | PMBOK 7 §2.1.1.3, p. 12 (Q105b) | alterado | Núcleo | 2 | teste |
| RN-PI-15 | Gravar a ordem sugerida deve trocar a ordem manual pela ordem sugerida. | PMBOK 7 §2.1.1.3, p. 12 (Q113) | confirmado | Núcleo | 2 | teste |
| RN-PI-16 | O nível atual e o nível desejado de engajamento devem ir de 1, o menor, a 5, o maior, sem nomes. | PMBOK 7 Tabela 2-2, p. 15; p. 189 (Q106b) | alterado | Engajamento das partes | 3 | teste |
| RN-PI-17 | A lacuna de engajamento deve ser o nível desejado menos o atual, calculada só quando os dois existem. | PMBOK 7 p. 189 | confirmado | Engajamento das partes | 3 | teste |
| RN-PI-18 | A parte interessada deve contar como tendo plano de comunicação quando o plano tem o método, o tipo, a frequência e quem conduz a comunicação. | PMBOK 7 p. 186; Padrão p. 33 (Q106b) | alterado | Núcleo | 2 | teste |
| RN-PI-19 | O prazo de cada frequência do plano deve ser: diária, 1 dia, sem contar sábado e domingo; semanal, 7 dias; quinzenal, 15 dias; mensal, 30 dias; por iteração, a última iteração terminada; por marco ou fase, a última fase concluída; sob demanda, sem prazo. | Regra do PMO (Q169a) | alterado | Núcleo | 2 | teste |
| RN-PI-20 | Cada mudança do nível atual de engajamento deve gerar um registro, com o nível anterior e o novo; no cadastro, o nível inicial fica com o anterior vazio. | PMBOK 7 Tabela 2-2, p. 15 | confirmado | Engajamento das partes | 3 | teste |
| RN-PI-21 | A data de um contato deve ser no máximo a data de hoje. | Regra do PMO (Q108) | confirmado | Núcleo | 2 | teste |
| RN-PI-22 | O contato deve ter a parte interessada escolhida. | Regra do PMO | confirmado | Núcleo | 2 | teste |
| RN-PI-23 | A parte interessada deve contar como monitorada quando teve contato dentro do prazo da frequência do plano (RN-PI-19); sem plano, nos últimos 30 dias; com a frequência sob demanda, quando tem pelo menos um contato. | PMBOK 7 §2.1.1.5, p. 14; p. 186; os prazos são regra do PMO (Q169a) | alterado | Núcleo | 2 | teste |
| RN-PI-24 | As partes inativas devem ficar fora das listas de análise, priorização, engajamento e alertas e dos indicadores, e continuar no registro. | PMBOK 7 p. 14; Padrão p. 32 | confirmado | Núcleo | 2 | teste |
| RN-PI-25 | Sem nenhuma parte interessada no projeto, o sistema deve mostrar um alerta médio. | PMBOK 7 p. 11 (Q166c) | confirmado | Núcleo | 3 | teste |
| RN-PI-26 | Quando uma parte interessada ativa se opõe ao projeto, o sistema deve mostrar um alerta médio, com o poder e o interesse dela. | PMBOK 7 p. 12; Tabela 2-2, p. 15; Padrão p. 32 (Q163) | alterado | Núcleo | 3 | teste |
| RN-PI-27 | Quando a última nota de satisfação de uma parte é 2 ou menos, o sistema deve mostrar um alerta alto. | PMBOK 7 p. 103; o corte é regra do PMO (Q166c) | confirmado | Engajamento das partes | 3 | teste |
| RN-PI-28 | Quando uma parte com plano de comunicação fica sem contato além do prazo da frequência do plano, o sistema deve mostrar um alerta médio. | PMBOK 7 p. 186; os prazos são regra do PMO (Q163, Q169a) | alterado | Núcleo | 3 | teste |
| RN-PI-29 | Quando o nível atual de engajamento de uma parte fica 2 ou mais abaixo do desejado, o sistema deve mostrar um alerta médio. | PMBOK 7 p. 189; o corte é regra do PMO (Q164) | alterado | Engajamento das partes | 3 | teste |
| RN-PI-30 | Quando uma parte ativa ainda não foi analisada, o sistema deve mostrar um alerta médio. | PMBOK 7 p. 11–12 (Q166c) | alterado | Núcleo | 3 | teste |
| RN-PI-31 | O sistema deve permitir excluir uma parte interessada somente quando ela não tem contato registrado nem vínculo com risco, questão, item, mudança, membro, aquisição, aprovação ou aceite. | PMBOK 7 §2.1.1.5, p. 14 (Q110) | alterado | Núcleo | 2 | teste |
| RN-PI-32 | O sistema deve permitir excluir um contato sem outra condição além da tela de confirmação. | Regra do PMO | confirmado | Núcleo | 1 | teste |
| RN-PI-33 | O sistema deve mostrar, como evidência da Tabela 2-2, o número de mudanças pedidas por cada parte interessada. | PMBOK 7 Tabela 2-2, p. 15 | confirmado | Núcleo | 2 | teste |
| RN-PI-34 | Um valor de poder, interesse, influência ou impacto fora da faixa de 1 a 5 deve ficar vazio. | Regra do PMO (Q111) | confirmado | Núcleo | 2 | teste |
| RN-PI-35 | Uma atitude fora da lista da RN-PI-08 deve virar desconhecida. | Regra do PMO (Q111) | confirmado | Núcleo | 2 | teste |
| RN-PI-36 | O sistema deve mostrar a análise individual de cada parte (poder, interesse, influência, impacto, atitude, crenças, expectativas e saliência) somente ao gerente do projeto, ao gerente de apoio e aos supervisores. | PMBOK 7 §2.1.1.2, p. 12 (Q104) | novo | Núcleo | 2 | teste |
| RN-PI-37 | Limpar a ordem deve apagar a ordem manual de cada parte do projeto. | PMBOK 7 §2.1.1.3, p. 12 (Q113) | confirmado | Núcleo | 2 | teste |
| RN-PI-38 | A ordem manual deve aceitar números de 1 a 1.000.000, e o sistema deve renumerá-la de 1 até o número de partes ordenadas. | Regra do PMO (Q111) | confirmado | Núcleo | 2 | teste |
| RN-PI-39 | A parte interessada deve contar como priorizada quando tem ordem manual. | Regra do PMO (Q111) | confirmado | Núcleo | 2 | teste |
| RN-PI-40 | Quando a data do contato fica vazia ou é inválida, o sistema deve usar a data de hoje. | Regra do PMO (Q108) | confirmado | Núcleo | 2 | teste |
| RN-PI-41 | A nota de satisfação do contato deve ser opcional, de 1 a 5. | PMBOK 7 p. 103 (Q108) | confirmado | Engajamento das partes | 3 | teste |
| RN-PI-42 | Quando o nível atual de engajamento de uma parte fica 2 ou mais acima do desejado, o sistema deve mostrar um alerta informativo. | PMBOK 7 p. 189; o corte é regra do PMO (Q164) | novo | Engajamento das partes | 3 | teste |
| RN-PI-43 | Quando uma parte neutra tem influência 4 ou 5, o sistema deve mostrar um alerta informativo, lembrando de engajá-la. | PMBOK 7 Padrão p. 32; p. 12; o corte é regra do PMO (Q171) | novo | Núcleo | 3 | teste |

A regra PI-11 do protótipo, a grade de Mendelow, saiu (Q105b). Nos alertas das RN-PI-26 e RN-PI-28, o documento gerado mostra a parte sem o nome (RN-PM-47). Na RN-PI-19, sem iteração ou fase com datas, as frequências por iteração e por marco ou fase usam os 30 dias (Q169a).

#### 3.2.6 Equipe (EQ)

Membros da equipe, modelo de liderança e matriz RACI, no núcleo; estágio da equipe, acordo de trabalho, saúde da equipe, lacunas e planos de desenvolvimento, no módulo Desenvolvimento da equipe (Q31). O gerente do projeto e o gerente de apoio entram sozinhos na equipe (RN-PM-69, RN-PM-77).

**Entradas**

| Entrada | Onde | Tipo | Obrigatória | Valores válidos | Origem |
|---|---|---|---|---|---|
| Nome do membro | cadastro e edição do membro | texto | sim | até 20.000 caracteres | Q120 |
| Papel e habilidades | cadastro e edição do membro | texto | não | até 20.000 caracteres | Protótipo |
| Dedicação | cadastro e edição do membro | escolha | sim | integral ou parcial; padrão integral | Q120 |
| Local | cadastro e edição do membro | escolha | sim | presencial, híbrido ou remoto; padrão presencial | Q120 |
| Motivador | cadastro e edição do membro | escolha | não | realização, desafio, crença no trabalho, fazer diferença, autonomia, responsabilidade, crescimento pessoal, relacionamento, fazer parte de uma equipe ou recompensa externa (RN-EQ-24) | Q120 |
| Lacunas e plano de desenvolvimento | cadastro e edição do membro, no módulo | texto | não | até 20.000 caracteres | Q119 |
| Conta ligada | cadastro e edição do membro | escolha | não | uma conta ativa | Q55, Q120 |
| Parte interessada ligada | cadastro e edição do membro | escolha | não | uma parte interessada do projeto | Q120 |
| Modelo de liderança | equipe | escolha | não | centralizada ou distribuída | Q120 |
| Estágio da equipe | equipe, no módulo | escolha | não | formação, confronto, normatização, desempenho ou dissolução (RN-EQ-05) | Q120 |
| Seções do acordo de trabalho | acordo de trabalho, no módulo | texto | não | até 20.000 caracteres em cada uma das três seções (RN-EQ-08) | Q116 |
| Descrição da linha da RACI | matriz RACI | texto | sim | até 20.000 caracteres; ligada a um item, o código e o título dele (RN-EQ-09) | Q120 |
| Item ligado à linha | matriz RACI | escolha | não | um item de escopo do projeto | Protótipo |
| Papel na linha | matriz RACI | escolha | não | R, A, C ou I (RN-EQ-10) | Q118, Q121 |
| Data da avaliação de saúde | saúde da equipe, no módulo | data | sim | até a data de hoje (RN-EQ-25) | Q120 |
| Participantes da avaliação | saúde da equipe, no módulo | número inteiro | sim | de 1 a 1.000 | Q120 |
| Nota de cada fator | saúde da equipe, no módulo | número inteiro | pelo menos uma (RN-EQ-12) | de 1 a 5, nos 9 fatores de alto desempenho do PMBOK 7, p. 22 | Q120 |

**Funções**

| Código | Requisito | Regras | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|---|
| RF-EQ-01 | O sistema deve listar os membros da equipe e permitir cadastrar um membro, com papel, dedicação, local, habilidades, motivador, conta e parte interessada ligadas e, com o módulo Desenvolvimento da equipe ligado, lacunas e plano de desenvolvimento. | RN-EQ-01 a RN-EQ-03, RN-EQ-21, RN-EQ-24, RN-PM-69 | Q114, Q117, Q119, Q120, Q165 | alterado | Núcleo | 2 | teste |
| RF-EQ-02 | O sistema deve permitir registrar o modelo de liderança da equipe. | RN-EQ-04 | Q120 | alterado | Núcleo | 2 | teste |
| RF-EQ-03 | O sistema deve mostrar um membro, com os papéis dele na matriz RACI, e permitir editá-lo. | RN-EQ-01 a RN-EQ-03, RN-EQ-21, RN-EQ-24 | Q115, Q119 | alterado | Núcleo | 2 | teste |
| RF-EQ-04 | O sistema deve permitir liberar um membro da equipe e reativá-lo. | RN-EQ-06, RN-EQ-22 | Q115 | alterado | Núcleo | 2 | teste |
| RF-EQ-05 | O sistema deve permitir excluir um membro sem vínculos. | RN-EQ-07, RN-DA-31 | Q115, Q198 | alterado | Núcleo | 2 | teste |
| RF-EQ-06 | O sistema deve permitir registrar o acordo de trabalho da equipe. | RN-EQ-08, RN-EQ-16 | Q116, Q165 | alterado | Desenvolvimento da equipe | 3 | teste |
| RF-EQ-07 | O sistema deve permitir montar a matriz RACI: incluir e excluir linhas e atribuir os papéis R, A, C e I. | RN-EQ-09 a RN-EQ-11, RN-EQ-23, RN-DA-31 | Q117, Q118, Q121, Q198 | alterado | Núcleo | 2 | teste |
| RF-EQ-08 | O sistema deve permitir registrar a avaliação de saúde da equipe pelos 9 fatores de alto desempenho e mostrar o histórico das avaliações, com o gráfico. | RN-EQ-12 a RN-EQ-14, RN-EQ-18, RN-EQ-25 | Q120, Q174a, Q198 | alterado | Desenvolvimento da equipe | 3 | teste |
| RF-EQ-09 | O sistema deve permitir registrar o estágio de desenvolvimento da equipe. | RN-EQ-05, RN-EQ-20 | Q120 | alterado | Desenvolvimento da equipe | 3 | teste |

**Regras de negócio**

| Código | Regra | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RN-EQ-01 | O membro da equipe deve ter nome. | Regra do PMO (Q120) | confirmado | Núcleo | 2 | teste |
| RN-EQ-02 | Um membro novo deve começar com dedicação integral e local presencial. | Regra do PMO (Q120) | confirmado | Núcleo | 2 | teste |
| RN-EQ-03 | O sistema deve permitir ligar o membro a uma conta ativa e a uma parte interessada do mesmo projeto. | Regra do PMO (Q55, Q120) | confirmado | Núcleo | 2 | teste |
| RN-EQ-04 | O modelo de liderança deve ser centralizado ou distribuído. | PMBOK 7 p. 17 (Q120) | confirmado | Núcleo | 2 | teste |
| RN-EQ-05 | O estágio da equipe deve ser formação (forming), confronto (storming), normatização (norming), desempenho (performing) ou dissolução (adjourning), sem ordem obrigatória, porque a equipe vai e volta entre eles. | PMBOK 7 §4.2.6.1, p. 166 (Q120) | confirmado | Desenvolvimento da equipe | 3 | teste |
| RN-EQ-06 | Liberar um membro deve desativá-lo e gravar a data da liberação; reativá-lo deve limpar essa data. | Regra do PMO (Q120) | confirmado | Núcleo | 2 | teste |
| RN-EQ-07 | O sistema deve permitir excluir um membro somente quando ele não é responsável por risco, questão ou item, não tem papel na RACI e não conduz a comunicação com uma parte interessada. | PMBOK 7 §2.2.1.3, p. 18 (Q115) | alterado | Núcleo | 2 | teste |
| RN-EQ-08 | O acordo de trabalho deve ter três seções: valores; acordos e diretrizes de operação; e comportamento esperado. | PMBOK 7 p. 192; §2.2.1.3, p. 19 (Q116) | alterado | Desenvolvimento da equipe | 3 | teste |
| RN-EQ-09 | A linha da RACI deve ter descrição; ligada a um item, a descrição padrão é o código e o título do item. | Regra do PMO (Q120) | confirmado | Núcleo | 2 | teste |
| RN-EQ-10 | Numa linha da RACI, cada pessoa deve ter um só papel, ou os papéis A e R juntos. | PMBOK 7 p. 189 (Q118, Q121) | alterado | Núcleo | 2 | teste |
| RN-EQ-11 | O sistema deve marcar como incompleta a linha da RACI sem A, com mais de um A ou sem R, sem impedir a gravação. | PMBOK 7 p. 189; §2.2.1.1, p. 17; um A por linha é regra do PMO (Q117) | alterado | Núcleo | 2 | teste |
| RN-EQ-12 | A avaliação de saúde da equipe deve ter pelo menos um fator com nota. | PMBOK 7 p. 22 e 104 (Q120) | confirmado | Desenvolvimento da equipe | 3 | teste |
| RN-EQ-13 | A média da avaliação deve ser a média das notas preenchidas. | Regra do PMO (Q120) | confirmado | Desenvolvimento da equipe | 3 | teste |
| RN-EQ-14 | Quando, na última avaliação, um fator fica com nota 2 ou menos, o sistema deve mostrar um alerta médio; o fator sem nota conta como 5. | PMBOK 7 p. 22 e 104; o corte é regra do PMO (Q166c) | confirmado | Desenvolvimento da equipe | 3 | teste |
| RN-EQ-16 | Quando o acordo de trabalho não tem nenhuma das três seções preenchida, o sistema deve mostrar um alerta médio. | PMBOK 7 p. 192 (Q165) | alterado | Desenvolvimento da equipe | 3 | teste |
| RN-EQ-17 | Quando um membro tem lacunas e não tem plano de desenvolvimento, o sistema deve mostrar um alerta informativo. | PMBOK 7 p. 18 (Q166c) | confirmado | Desenvolvimento da equipe | 3 | teste |
| RN-EQ-18 | Quando o projeto não tem avaliação de saúde, ou a última tem mais de 45 dias, o sistema deve mostrar um alerta informativo. | PMBOK 7 p. 103–104; os 45 dias são regra do PMO (Q166c) | confirmado | Desenvolvimento da equipe | 3 | teste |
| RN-EQ-19 | Num projeto de abordagem adaptativa com mais de 9 membros ativos, o sistema deve mostrar um alerta informativo, com a referência de 7 ± 2 membros. | PMBOK 7 p. 41 (Q166c) | confirmado | Núcleo | 3 | teste |
| RN-EQ-20 | Ao encerrar ou cancelar o projeto, o sistema deve passar o estágio da equipe para dissolução. | PMBOK 7 p. 166 (Q120) | confirmado | Desenvolvimento da equipe | 3 | teste |
| RN-EQ-21 | O sistema deve mostrar as habilidades, as lacunas, o plano de desenvolvimento e o motivador de cada membro somente ao gerente do projeto, ao gerente de apoio e aos supervisores. | PMBOK 7 Padrão p. 33; §2.1.1.2, p. 12 (Q119) | novo | Núcleo | 2 | teste |
| RN-EQ-22 | O sistema deve recusar a liberação de um membro que ainda é responsável por risco, questão ou item em aberto. | PMBOK 7 §2.2.1.3, p. 18 (Q115) | novo | Núcleo | 2 | teste |
| RN-EQ-23 | As colunas da RACI devem ser os membros ativos e as partes interessadas ativas que o gerente escolher; o membro ligado a uma parte aparece uma vez só. | PMBOK 7 p. 189 (Q118) | novo | Núcleo | 2 | teste |
| RN-EQ-24 | O motivador deve ser um dos 9 motivadores intrínsecos do PMBOK 7 ou a recompensa externa. | PMBOK 7 p. 24–25 (Q120) | alterado | Núcleo | 2 | teste |
| RN-EQ-25 | A data da avaliação de saúde deve ser no máximo a data de hoje. | Regra do PMO (Q120) | confirmado | Desenvolvimento da equipe | 3 | teste |

A regra EQ-15 do protótipo, alerta de equipe sem membros, saiu (Q165). Na RN-EQ-17, o documento gerado mostra o membro sem o nome (Q119, RN-PM-47).

#### 3.2.7 Abordagem, ciclo de vida e tailoring (AB)

Abordagem de desenvolvimento, cadência de entrega, fases com critérios de saída, revisão de fase e tailoring, no núcleo; o diagnóstico pela Tabela 3-1, no módulo Diagnóstico de tailoring (Q31). A proposta de tailoring passa por revisão obrigatória junto com o termo de abertura (Q33). As regras de Stacey e do Cynefin (RN-AB-06 e RN-AB-07) ficam aqui pelo código; a tela delas é do domínio Métodos, na parte 3.

**Entradas**

| Entrada | Onde | Tipo | Obrigatória | Valores válidos | Origem |
|---|---|---|---|---|---|
| Nota de cada fator de seleção | assistente de abordagem | número inteiro | não | de 1 a 5, em cada um dos 15 fatores (RN-AB-03) | Q123 |
| Abordagem escolhida | assistente de abordagem | escolha | não | preditiva, híbrida ou adaptativa (RN-AB-01) | Q124 |
| Cadência de entrega | assistente de abordagem; criar e editar projeto | escolha | não | entrega única, múltiplas entregas, entregas periódicas ou entrega contínua (RN-AB-02) | Q122 |
| Justificativa da abordagem | assistente de abordagem | texto | quando a escolha é diferente da sugestão (RN-AB-05) | até 20.000 caracteres | Q136 |
| Nome da fase | fases | texto | sim | até 20.000 caracteres (RN-AB-12) | Q135 |
| Início e término da fase | fases | data | não | término igual ao início ou depois dele (RN-AB-13) | Q135 |
| Critérios de saída | fases | texto, um por linha | não | até 20.000 caracteres | Q128, Q129 |
| Situação da fase | fases | escolha | sim | não iniciada, em andamento ou concluída (RN-AB-14) | Q129 |
| Decisão da revisão de fase | revisão de fase | escolha | sim, para concluir | seguir, seguir com modificações, repetir ou estender, ou encerrar o projeto (RN-AB-14) | Q129 |
| Quem decidiu | revisão de fase | escolha | sim, para concluir | uma parte interessada ativa ou um membro da equipe (RN-AB-37) | Q130 |
| Notas da revisão | revisão de fase | texto | com "seguir com modificações" (RN-AB-28) | até 20.000 caracteres | Q179 |
| Respostas de contexto | perguntas de tailoring | texto | não | até 20.000 caracteres em cada uma das 17 perguntas (RN-AB-23) | Q133 |
| Elemento e tipo da decisão de tailoring | decisões de tailoring | texto e escolha | sim | o tipo é adicionar, remover ou ajustar (RN-AB-24) | Q135 |

**Funções**

| Código | Requisito | Regras | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|---|
| RF-AB-01 | O sistema deve permitir propor a abordagem do projeto: dar nota aos 15 fatores de seleção, ver a sugestão, escolher a abordagem e a cadência de entrega e justificar a escolha. | RN-AB-01 a RN-AB-05, RN-AB-26 | Q33, Q122, Q123, Q124, Q136 | alterado | Núcleo | 2 | teste |
| RF-AB-02 | O sistema deve mostrar as fases do ciclo de vida e permitir aplicar as fases sugeridas ou criar uma fase. | RN-AB-10 a RN-AB-12, RN-AB-35, RN-AB-36 | Q128, Q129 | alterado | Núcleo | 2 | teste |
| RF-AB-03 | O sistema deve permitir editar uma fase e fazer a revisão de fase para concluí-la. | RN-AB-13 a RN-AB-19, RN-AB-27 a RN-AB-29, RN-AB-37 | Q129 a Q132, Q137, Q178, Q179 | alterado | Núcleo | 2 | teste |
| RF-AB-04 | O sistema deve permitir excluir uma fase sem revisão registrada. | RN-AB-38, RN-DA-31 | Q132, Q198 | alterado | Núcleo | 2 | teste |
| RF-AB-05 | O sistema deve permitir responder às 17 perguntas de contexto do tailoring. | RN-AB-23 | Q33, Q133 | alterado | Núcleo | 2 | teste |
| RF-AB-06 | O sistema deve permitir registrar e excluir decisões de tailoring. | RN-AB-24, RN-DA-31 | Q133, Q135, Q198 | alterado | Núcleo | 2 | teste |
| RF-AB-07 | O sistema deve mostrar as situações da Tabela 3-1 do PMBOK 7 detectadas nos dados do projeto, com a sugestão de cada uma. | RN-AB-25, RN-AB-39 a RN-AB-44 | Q133, Q134, Q180, Q185 | alterado | Diagnóstico de tailoring | 3 | teste |
| RF-AB-08 | O sistema deve permitir enviar para revisão a proposta de tailoring: a abordagem, a cadência de entrega, as fases, as respostas de contexto e as decisões de tailoring. | RN-PM-16, RN-AB-45 | Q33 | novo | Núcleo | 2 | teste |
| RF-AB-09 | Na revisão da proposta de tailoring, o sistema deve mostrar ao supervisor os fatores que apontam para o outro lado do espectro, os dados do projeto ligados a eles e as decisões de tailoring de outros projetos do PMO com a mesma abordagem. | RN-AB-31 a RN-AB-34 | Q123, Q136 | novo | Núcleo | 2 | teste |

**Regras de negócio**

| Código | Regra | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RN-AB-01 | A abordagem deve ser preditiva, híbrida ou adaptativa; um valor fora da lista vira "não definida". | PMBOK 7 §2.3, p. 33–36; o valor inválido é regra do PMO (Q124, Q135) | confirmado | Núcleo | 2 | teste |
| RN-AB-02 | O servidor deve recusar a cadência de entrega fora da lista (única, múltiplas, periódica ou contínua) ao criar e editar o projeto e na tela de abordagem. | PMBOK 7 §2.3.2, p. 33–34 (Q122) | alterado | Núcleo | 2 | teste |
| RN-AB-03 | Cada um dos 15 fatores de seleção deve ter nota de 1, que favorece a abordagem preditiva, a 5, que favorece a adaptativa; o fator sem nota fica fora da conta. | PMBOK 7 §2.3.4, p. 39–41; a escala é regra do PMO (Q123) | confirmado | Núcleo | 2 | teste |
| RN-AB-04 | A sugestão de abordagem deve vir da média das notas: abaixo de 2,5, preditiva; acima de 3,5, adaptativa; entre esses valores, híbrida; e deve mostrar a média de cada categoria (produto, projeto e organização). | PMBOK 7 §3.4.1, p. 138; a média e os cortes são regra do PMO (Q123) | confirmado | Núcleo | 2 | teste |
| RN-AB-05 | Quando a abordagem escolhida é diferente da sugerida, a justificativa deve ser preenchida. | PMBOK 7 p. 139 (Q136) | alterado | Núcleo | 2 | teste |
| RN-AB-06 | A matriz de Stacey deve usar a incerteza dos requisitos e a incerteza da tecnologia, de 1 (pouca) a 5 (muita), e classificar o projeto pela soma (até 4, simples; até 6, complicado; até 8, complexo; acima de 8, caótico), sem sugerir abordagem. | PMBOK 7 §4.2.5.2, p. 165; a classificação pela soma é regra do PMO (Q126) | alterado | Incerteza avançada | 3 | teste |
| RN-AB-07 | O Cynefin deve ter os 5 contextos do PMBOK 7, com o original em inglês: óbvio (obvious), complicado (complicated), complexo (complex), caótico (chaotic) e desordenado (disordered), com a forma de decidir de cada um e sem ligação com a abordagem. | PMBOK 7 §4.2.5.1, p. 164–165 (Q125) | alterado | Incerteza avançada | 3 | teste |
| RN-AB-08 | O modelo de projeto deve gravar a abordagem, a cadência de entrega, a unidade de estimativa, o limite de trabalho em andamento (3 nos modelos de software; nenhum no preditivo), a definição de pronto, as fases sugeridas e três riscos típicos. | PMBOK 7 p. 35; regra do PMO (Q127) | alterado | Núcleo | 1 | teste |
| RN-AB-09 | Os riscos criados pelo modelo devem usar as fontes da lista oficial e registrar a revisão inicial, como os outros riscos. | PMBOK 7 Tabela 2-10, p. 129 (Q127) | alterado | Núcleo | 1 | teste |
| RN-AB-10 | As fases sugeridas devem seguir a abordagem: 6 fases na preditiva e na híbrida, 3 na adaptativa, cada uma com critérios de saída; sem abordagem definida, valem as da híbrida. | PMBOK 7 p. 42 e 45–47 (Q128) | alterado | Núcleo | 2 | teste |
| RN-AB-11 | As fases sugeridas devem ser aplicadas somente a um ciclo de vida sem fases. | Regra do PMO (Q135) | confirmado | Núcleo | 2 | teste |
| RN-AB-12 | A fase deve ter nome, e a ordem das fases deve ser sequencial e automática, de 1 a 1.000. | Regra do PMO (Q135) | confirmado | Núcleo | 2 | teste |
| RN-AB-13 | O término da fase deve ser igual ao início ou depois dele. | Regra do PMO (Q135) | confirmado | Núcleo | 2 | teste |
| RN-AB-14 | A situação da fase deve ser não iniciada, em andamento ou concluída, e a decisão da revisão de fase, seguir, seguir com modificações, repetir ou estender, ou encerrar o projeto. | PMBOK 7 Glossário (Phase Gate), p. 244; p. 43 (Q129) | alterado | Núcleo | 2 | teste |
| RN-AB-15 | Para concluir a fase, os critérios de saída devem estar marcados e a revisão deve ter a decisão; a fase sem critérios de saída conclui só com a decisão. | PMBOK 7 §2.3.5, p. 42 (Q129) | alterado | Núcleo | 2 | teste |
| RN-AB-16 | Com a decisão repetir ou estender, a fase deve voltar para em andamento, em vez de concluir. | PMBOK 7 p. 43 (Q129) | confirmado | Núcleo | 2 | teste |
| RN-AB-17 | Com a decisão encerrar o projeto, o sistema deve levar à tela de encerramento e avisar que o projeto só encerra pelo supervisor. | PMBOK 7 Glossário (Phase Gate), p. 244 (Q29, Q131) | alterado | Núcleo | 2 | teste |
| RN-AB-18 | A fase concluída deve reabrir somente por uma nova revisão com a decisão repetir ou estender, e a decisão anterior deve ficar no histórico. | PMBOK 7 p. 43 (Q132) | alterado | Núcleo | 2 | teste |
| RN-AB-19 | O sistema deve gravar a data da revisão de fase quando a decisão muda. | Regra do PMO (Q135) | confirmado | Núcleo | 2 | teste |
| RN-AB-20 | Num projeto preditivo ou híbrido sem fases, o sistema deve mostrar um alerta informativo. | PMBOK 7 p. 42 e 45; Tabela 2-5, p. 50 (Q185) | confirmado | Núcleo | 3 | teste |
| RN-AB-21 | Quando uma fase não concluída passa do término sem revisão de fase, o sistema deve mostrar um alerta médio. | PMBOK 7 §2.3.5, p. 42 (Q185) | confirmado | Núcleo | 3 | teste |
| RN-AB-23 | O tailoring deve ter 17 perguntas de contexto, nos grupos produto, equipe e cultura, com o texto alinhado ao PMBOK 7; só as respostas preenchidas são guardadas. | PMBOK 7 §3.4.3, p. 141–143 (Q133) | alterado | Núcleo | 2 | teste |
| RN-AB-24 | A decisão de tailoring deve ter o elemento e o tipo (adicionar, remover ou ajustar) e a data de hoje. | PMBOK 7 §3.4.2, p. 140; Figura 3-6, p. 144; a data é regra do PMO (Q135) | confirmado | Núcleo | 2 | teste |
| RN-AB-25 | Quando o custo das falhas passa do custo de conformidade, o sistema deve mostrar um alerta informativo com a sugestão da Tabela 3-1. | PMBOK 7 Tabela 3-1, p. 151; o critério é regra do PMO (Q134, Q185) | confirmado | Diagnóstico de tailoring | 3 | teste |
| RN-AB-26 | A tela da abordagem deve explicar que a abordagem híbrida inclui o projeto com entregas de abordagens diferentes. | PMBOK 7 p. 36; Tabela 2-4, p. 46 (Q124) | novo | Núcleo | 2 | teste |
| RN-AB-27 | A tela da revisão de fase deve avisar quando a fase não tem critérios de saída. | PMBOK 7 Tabela 2-5, p. 50 (Q129, Q178) | novo | Núcleo | 2 | teste |
| RN-AB-28 | A decisão "seguir com modificações" deve ter as modificações descritas nas notas da revisão. | PMBOK 7 Glossário (Phase Gate), p. 244 (Q179) | novo | Núcleo | 2 | teste |
| RN-AB-29 | A tela da revisão de fase deve lembrar que a fase é o momento de rever o tailoring e, com o módulo Diagnóstico de tailoring ligado, mostrar as situações da Tabela 3-1 detectadas. | PMBOK 7 §3.4.3.4, p. 144; §3.6, p. 151 (Q137) | novo | Núcleo | 2 | teste |
| RN-AB-30 | Quando uma fase em andamento não tem critérios de saída, o sistema deve mostrar um alerta médio. | PMBOK 7 §2.3.5, p. 42; Tabela 2-5, p. 50 (Q178) | novo | Núcleo | 3 | teste |
| RN-AB-31 | A revisão da proposta deve mostrar os fatores que apontam para o outro lado do espectro (nota 1 ou 2 com a escolha adaptativa; 4 ou 5 com a preditiva), cada um com o que o PMBOK 7 diz dele. | PMBOK 7 §2.3.4, p. 39–41 (Q136) | novo | Núcleo | 2 | teste |
| RN-AB-32 | A revisão da proposta deve destacar o projeto com requisitos de segurança rigorosos. | PMBOK 7 p. 139 (Q136) | novo | Núcleo | 2 | teste |
| RN-AB-33 | A revisão da proposta deve mostrar, ao lado dos fatores, os membros ativos e remotos, a cadência escolhida, a aquisição contratada e a classificação de Stacey e do Cynefin, quando preenchidas. | PMBOK 7 p. 33, 40, 41, 139 e 165 (Q136) | novo | Núcleo | 2 | teste |
| RN-AB-34 | O sistema deve mostrar somente ao supervisor as decisões de tailoring de outros projetos do PMO com a mesma abordagem. | Regra do PMO (Q136) | novo | Núcleo | 2 | teste |
| RN-AB-35 | Os critérios de saída sugeridos para a fase de início devem ser: roadmap, necessidades de financiamento, equipe e recursos, cronograma de marcos e estratégia de aquisições. | PMBOK 7 §2.3.5, p. 42 (Q128) | novo | Núcleo | 2 | teste |
| RN-AB-36 | As fases sugeridas da abordagem adaptativa devem ser: definir a visão do projeto e do produto; iterações com feedback e repriorização do backlog; e encerramento. | PMBOK 7 Figura 2-11, p. 45; §2.3.6, p. 46–47 (Q128) | novo | Núcleo | 2 | teste |
| RN-AB-37 | A revisão de fase deve registrar quem decidiu, escolhido entre as partes interessadas ativas e os membros da equipe. | Regra do PMO (Q130) | novo | Núcleo | 2 | teste |
| RN-AB-38 | O sistema deve permitir excluir somente a fase sem revisão registrada. | Regra do PMO (Q132) | alterado | Núcleo | 2 | teste |
| RN-AB-39 | Quando uma mudança aguarda decisão há mais de 7 dias, o sistema deve mostrar um alerta informativo com a sugestão da Tabela 3-1. | PMBOK 7 Tabela 3-1, p. 151; o prazo é regra do PMO (Q134, Q185) | confirmado | Diagnóstico de tailoring | 3 | teste |
| RN-AB-40 | Quando o trabalho em andamento passa do limite, ou, sem limite, chega a 5 ou mais e passa da metade dos itens, o sistema deve mostrar um alerta informativo com a sugestão da Tabela 3-1. | PMBOK 7 Tabela 3-1, p. 151; os cortes são regra do PMO (Q134, Q185) | confirmado | Diagnóstico de tailoring | 3 | teste |
| RN-AB-41 | Quando a satisfação média das partes interessadas fica abaixo de 3, o sistema deve mostrar um alerta informativo com a sugestão da Tabela 3-1. | PMBOK 7 Tabela 3-1, p. 151; o corte é regra do PMO (Q134, Q185) | confirmado | Diagnóstico de tailoring | 3 | teste |
| RN-AB-42 | Quando o projeto tem itens e não tem relatório de status dentro da cadência de relatório nem indicador, o sistema deve mostrar um alerta informativo com a sugestão da Tabela 3-1. | PMBOK 7 Tabela 3-1, p. 151 (Q134, Q180, Q185) | alterado | Diagnóstico de tailoring | 3 | teste |
| RN-AB-43 | Quando há 3 ou mais questões sem risco de origem nos últimos 60 dias, o sistema deve mostrar um alerta informativo com a sugestão da Tabela 3-1. | PMBOK 7 Tabela 3-1, p. 151; os cortes são regra do PMO (Q134, Q185) | confirmado | Diagnóstico de tailoring | 3 | teste |
| RN-AB-44 | Quando o fator "entendimento compartilhado" tem nota 2 ou menos na última avaliação de saúde, o sistema deve mostrar um alerta informativo com a sugestão da Tabela 3-1. | PMBOK 7 Tabela 3-1, p. 151; o corte é regra do PMO (Q134, Q185) | confirmado | Diagnóstico de tailoring | 3 | teste |
| RN-AB-45 | Depois de liberada a proposta de tailoring, mudar a abordagem, as fases ou as decisões de tailoring deve tirar a liberação e exigir nova revisão. | PMBOK 7 §3.4.2, p. 140 (Q33) | novo | Núcleo | 2 | teste |

A regra AB-22 do protótipo, alerta de "seguir com ressalvas" sem notas, saiu (Q179). As situações das RN-AB-25, RN-AB-41 e RN-AB-44 usam dados de módulos opcionais (custo da qualidade, satisfação e saúde da equipe) e só aparecem quando esses dados existem. A regra AB-25 do protótipo foi dividida nas RN-AB-25 e RN-AB-39 a RN-AB-44, uma por situação.

#### 3.2.8 Planejamento (PL)

Termo de abertura, declaração de visão, datas do projeto, iterações, planejamento dos itens e agenda, no núcleo (Q31). O termo segue o fluxo da revisão e da aprovação da parte 1: o gerente prepara, o supervisor libera, o gerente gera o documento, o patrocinador aprova por fora e o gerente registra a aprovação (Q14; RF-PM-02, RF-PM-03, RF-PM-10 e RF-PM-11). Na tela do termo, os campos que vêm do PMBOK 7 aparecem primeiro, e os do PMO num bloco "Campos do PMO" (Q68); essa regra de tela é descrita na parte 4.

**Entradas**

| Entrada | Onde | Tipo | Obrigatória | Valores válidos | Origem |
|---|---|---|---|---|---|
| Propósito, objetivos e critérios de sucesso | termo de abertura | texto | sim, para ficar pronto para revisão (RN-PL-05) | até 20.000 caracteres cada | Q61 |
| Requisitos de alto nível, premissas, restrições, riscos de alto nível, marcos, orçamento e autoridade do gerente | termo de abertura | texto | não | até 20.000 caracteres cada | Protótipo |
| Patrocinador | termo de abertura | escolha | sim, para ficar pronto para revisão | uma parte interessada do projeto (RN-PL-25) | Q61, Q109, Q112 |
| Gerente do projeto | termo de abertura | preenchido pelo sistema | — | o gerente do projeto (RN-PL-24) | Q60 |
| Autoridade de mudança | termo de abertura | escolha | sim | patrocinador, comitê de controle de mudanças ou dono do produto; padrão patrocinador (RN-PL-27) | Q69 |
| Limite de variação | termo de abertura | número inteiro, em % | sim | de 1 a 50; padrão 10 | Q88, Q177 |
| Limite de risco | termo de abertura | número inteiro | sim | de 1 a 25; padrão 12 | Q95, Q177 |
| Declaração de visão | visão | texto | não | até 20.000 caracteres | Q66 |
| Início e término planejado do projeto | datas do projeto | data | não | término igual ao início ou depois dele (RN-PL-13) | Q67 |
| Nome, início e fim da iteração | criar e editar iteração | texto e datas | sim | fim igual ao início ou depois dele; sem sobrepor outra iteração (RN-PL-14, RN-PL-15) | Q67 |
| Meta da iteração | criar e editar iteração | texto | não | até 20.000 caracteres | Protótipo |
| Capacidade da iteração | criar e editar iteração | número | não | maior ou igual a 0 (RN-PL-14) | Q67 |
| Iteração, início, término, custo planejado e custo real de cada item | planejar itens em lote | escolha, datas e números | não | custos maiores ou iguais a 0 (RN-PL-28); iteração do projeto (RN-PL-29) | Q67 |

**Funções**

| Código | Requisito | Regras | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|---|
| RF-PL-01 | O sistema deve permitir preencher o termo de abertura e mostrar a situação dele. | RN-PL-03 a RN-PL-08, RN-PL-24 a RN-PL-27, RN-PL-31, RN-PL-32, RN-PM-16 | Q10, Q14, Q15, Q60, Q61, Q62, Q66, Q68, Q69, Q109, Q112, Q177 | alterado | Núcleo | 1 | teste |
| RF-PL-02 | O sistema deve permitir escrever a declaração de visão do projeto em texto livre. | RN-PL-12 | Q66 | alterado | Núcleo | 2 | teste |
| RF-PL-03 | O sistema deve permitir definir as datas de início e de término planejado do projeto. | RN-PL-13 | Q67 | alterado | Núcleo | 2 | teste |
| RF-PL-04 | O sistema deve permitir criar uma iteração, com nome, início, fim, meta e capacidade. | RN-PL-14, RN-PL-15 | Q67 | alterado | Núcleo | 2 | teste |
| RF-PL-05 | O sistema deve permitir excluir uma iteração. | RN-PL-16, RN-DA-31 | Q67, Q198 | alterado | Núcleo | 2 | teste |
| RF-PL-06 | O sistema deve permitir planejar os itens em lote, com iteração, datas e custos planejados e reais, e mostrar os totais e a velocidade. | RN-PL-17, RN-PL-18, RN-PL-28 a RN-PL-30 | Q67, Q158 | alterado | Núcleo | 2 | teste |
| RF-PL-07 | O sistema deve permitir editar uma iteração. | RN-PL-14, RN-PL-15 | Q67 | novo | Núcleo | 2 | teste |
| RF-PL-08 | O sistema deve guardar as versões do termo de abertura aprovado e mostrar cada versão anterior, com a mudança que a substituiu. | RN-PL-08, RN-PL-31 | Q62 | novo | Núcleo | 1 | teste |

**Regras de negócio**

| Código | Regra | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RN-PL-01 | O projeto deve ter nome. | Regra do PMO (Q67) | confirmado | Núcleo | 1 | teste |
| RN-PL-02 | O projeto de exemplo deve ser reconhecido por uma marca própria, e não pelo nome. | Regra do PMO (Q67) | alterado | App | 1 | teste |
| RN-PL-03 | Ao criar um projeto, o sistema deve criar o termo de abertura dele, vazio e em rascunho. | PMBOK 7 §4.6.1, p. 184; o rascunho é regra do PMO (Q67) | confirmado | Núcleo | 1 | teste |
| RN-PL-04 | A situação do termo de abertura deve ser rascunho, em revisão, liberado, devolvido ou aprovado; aprovado é o termo com a aprovação do patrocinador registrada. | PMBOK 7 §4.6.1, p. 184; a revisão é regra do PMO (Q14, Q15, Q62) | alterado | Núcleo | 1 | teste |
| RN-PL-05 | Para ficar pronto para revisão, o termo de abertura deve ter propósito, objetivos, critérios de sucesso, patrocinador e gerente do projeto, em cada nível de exigência. | PMBOK 7 §4.6.1, p. 184 (patrocinador e gerente); os outros campos são regra do PMO, com apoio nas p. 18 e 96 (Q56, Q61, Q112) | alterado | Núcleo | 2 | teste |
| RN-PL-06 | Quando a aprovação do termo é registrada sem data, a data deve ser a de hoje. | Regra do PMO (Q67) | confirmado | Núcleo | 1 | teste |
| RN-PL-07 | O sistema deve manter na situação aprovado o termo aprovado, sem devolvê-lo ao rascunho. | Regra do PMO (Q112) | alterado | Núcleo | 1 | teste |
| RN-PL-08 | O termo de abertura aprovado deve ficar travado: uma alteração dele só acontece por uma mudança aprovada. | PMBOK 7 §2.6, p. 87; §4.6.1, p. 184 (Q15, Q62) | alterado | Núcleo | 1 | teste |
| RN-PL-10 | Quando a abordagem do projeto não está definida, o sistema deve mostrar um alerta médio. | Regra do PMO (Q154) | confirmado | Núcleo | 3 | teste |
| RN-PL-11 | Quando o termo de abertura não está aprovado, o sistema deve mostrar um alerta médio, em projeto de abordagem preditiva, híbrida ou adaptativa. | PMBOK 7 §4.6.1, p. 184 (Q154) | alterado | Núcleo | 3 | teste |
| RN-PL-12 | Quando o projeto não tem declaração de visão, o sistema deve mostrar um alerta informativo, em projeto de abordagem preditiva, híbrida ou adaptativa. | PMBOK 7 §2.4.1, p. 52; §4.6.1, p. 184 (Q154) | alterado | Núcleo | 3 | teste |
| RN-PL-13 | O término planejado do projeto deve ser igual ao início ou depois dele. | Regra do PMO (Q67) | confirmado | Núcleo | 2 | teste |
| RN-PL-14 | A iteração deve ter nome, início e fim, com o fim igual ao início ou depois dele, e capacidade maior ou igual a 0. | PMBOK 7 Glossário (Iteration), p. 241; a capacidade é regra do PMO (Q67) | confirmado | Núcleo | 2 | teste |
| RN-PL-15 | Duas iterações do mesmo projeto devem ocupar dias diferentes, contando os dias das pontas. | Regra do PMO (Q67) | confirmado | Núcleo | 2 | teste |
| RN-PL-16 | Excluir uma iteração deve devolver os itens dela ao backlog. | Regra do PMO (Q67) | alterado | Núcleo | 2 | teste |
| RN-PL-17 | Quando o término planejado de um item fica antes do início, o sistema deve ignorar as datas desse item e avisar. | Regra do PMO (Q67) | confirmado | Núcleo | 2 | teste |
| RN-PL-18 | Quando o custo planejado dos itens de uma iteração passa da capacidade dela, o sistema deve mostrar um alerta médio. | Regra do PMO (Q67, Q158) | alterado | Núcleo | 3 | teste |
| RN-PL-19 | O sistema deve descartar, com aviso, a dependência de um item com ele mesmo ou que formaria um ciclo de dependências. | PMBOK 7 p. 59–60; barrar ciclos é regra do PMO (Q67) | confirmado | Núcleo | 2 | teste |
| RN-PL-20 | Quando um item começa antes do término do item de que depende, ou no mesmo dia, o sistema deve mostrar um alerta médio de conflito no Gantt. | PMBOK 7 p. 189 (Q67, Q158) | alterado | Núcleo | 3 | teste |
| RN-PL-21 | A agenda deve juntar os prazos de questões, iterações, entregas, compras, premissas, revisões de decisões e benefícios, a próxima revisão de cada risco (a última revisão mais a cadência) e o fim do projeto; atrasado é o evento não feito com data antes de hoje. | Regra do PMO (Q67) | confirmado | App | 1 | teste |
| RN-PL-22 | Na agenda, a premissa não validada deve aparecer como pendente e, com o prazo vencido, como atrasada. | Regra do PMO (Q67) | alterado | App | 1 | teste |
| RN-PL-23 | O arquivo de calendário deve levar só os eventos ainda não feitos. | Regra do PMO (Q67) | confirmado | App | 1 | teste |
| RN-PL-24 | O campo gerente do projeto do termo deve ser preenchido pelo sistema com o gerente do projeto. | PMBOK 7 Padrão §1.2, p. 4; §2.2, p. 16 (Q60) | novo | Núcleo | 1 | teste |
| RN-PL-25 | O patrocinador do termo deve ser uma parte interessada do projeto. | PMBOK 7 §4.6.1, p. 184 (Q109) | novo | Núcleo | 1 | teste |
| RN-PL-26 | Quando o patrocinador registrado no termo ainda não é parte interessada, o sistema deve incluí-lo na lista, com a categoria patrocinador. | Regra do PMO (Q109) | novo | Núcleo | 1 | teste |
| RN-PL-27 | O termo deve registrar a autoridade de mudança do projeto: o patrocinador, que é o padrão, um comitê de controle de mudanças ou o dono do produto. | PMBOK 7 §2.6, p. 87; §2.5.7 (Q69) | novo | Núcleo | 1 | teste |
| RN-PL-28 | Os custos planejado e real de um item devem ser maiores ou iguais a 0. | Regra do PMO (Q67) | confirmado | Núcleo | 2 | teste |
| RN-PL-29 | O item ligado a uma iteração que não existe deve ficar sem iteração. | Regra do PMO (Q67) | confirmado | Núcleo | 2 | teste |
| RN-PL-30 | Quando um item não concluído passa do término planejado, o sistema deve mostrar um alerta alto. | Regra do PMO (Q67, Q158) | alterado | Núcleo | 3 | teste |
| RN-PL-31 | Cada mudança aprovada que altera o termo deve gerar uma nova versão dele, e a versão anterior deve ficar guardada. | Regra do PMO (Q62) | novo | Núcleo | 1 | teste |
| RN-PL-32 | O limite de variação e o limite de risco devem fazer parte do termo e, depois da aprovação, mudar somente por mudança aprovada. | PMBOK 7 §2.7.5, p. 113; §2.8.5, p. 122 (Q88, Q95, Q177) | novo | Núcleo | 2 | teste |
| RN-PR-03 | O custo previsto do projeto deve ser a ENT (EAC) mais as reservas de contingência e de gerenciamento; sem ENT, os custos planejados mais as reservas. | PMBOK 7 §2.4.2.4, Figura 2-18, p. 62–63 (Q144, Q224) | confirmado | Núcleo | 2 | teste |

O custo previsto (RN-PR-03) fica neste domínio, junto do orçamento, como no PMBOK 7 (Q224); o business case só usa o valor. A reserva de gerenciamento entra no cálculo quando o módulo Incerteza avançada está ligado. A regra PL-09 do protótipo, o gerador da visão no formato de Moore, saiu (Q66). Quem aprova o termo é o patrocinador (PMBOK 7 p. 184), e a aprovação é registrada pela RF-PM-10. As telas de dependências e do Gantt são do domínio Métodos, na parte 3.

#### 3.2.9 Trabalho do projeto (TR)

Questões, mudanças e lições aprendidas, no núcleo (Q31). A mudança é de revisão obrigatória (RN-PM-16) e segue o fluxo da Q72: o gerente prepara, o supervisor libera, o documento vai à autoridade de mudança e a decisão é registrada. O uso das reservas nas questões está no domínio Incerteza.

**Entradas**

| Entrada | Onde | Tipo | Obrigatória | Valores válidos | Origem |
|---|---|---|---|---|---|
| Título da questão | registrar e editar questão | texto | sim | até 20.000 caracteres | Q75 |
| Descrição da questão | registrar e editar questão | texto | não | até 20.000 caracteres | Protótipo |
| Prioridade | registrar e editar questão | escolha | sim | alta, média ou baixa; padrão média (RN-TR-02) | Q75 |
| Situação da questão | registrar e editar questão | escolha | sim | aberta, em andamento, resolvida ou cancelada; padrão aberta | Q73, Q75 |
| Responsável | registrar e editar questão | escolha | sim | um membro da equipe (RN-TR-03) | Q74 |
| Prazo | registrar e editar questão | data | no nível rigoroso (RN-TR-33) | uma data válida; a inválida fica vazia (RN-TR-30) | Q74 |
| Parte interessada e risco ligados | registrar e editar questão | escolha | não | do mesmo projeto (RN-TR-31) | Q75 |
| Resolução | resolver questão | texto | sim, ao resolver (RN-TR-04) | até 20.000 caracteres | Q112 |
| Justificativa do cancelamento | cancelar questão | texto | sim (RN-TR-32) | até 20.000 caracteres | Q73 |
| Título da mudança | registrar e editar mudança | texto | sim | até 20.000 caracteres | Q75 |
| Solicitante | registrar e editar mudança | escolha | sim, para ficar pronta (RN-TR-16) | uma parte interessada ou um membro da equipe (RN-TR-22) | Q70, Q176 |
| Valor esperado | registrar e editar mudança | texto | sim, para ficar pronta | até 20.000 caracteres | Q70, Q112 |
| Impacto no escopo, no cronograma, no orçamento, nos recursos, nas partes interessadas e nos riscos | registrar e editar mudança | texto | sim, para ficar pronta | até 20.000 caracteres cada; aceita "sem impacto" | Q70 |
| Riscos novos | registrar e editar mudança | texto | sim, para ficar pronta | até 20.000 caracteres | Q70 |
| Quem decidiu | decisão da mudança | escolha | sim, ao aprovar, rejeitar ou implementar (RN-TR-15) | uma parte interessada ou um membro da equipe | Q69, Q176 |
| Comunicada às partes | editar mudança | sim ou não | não | — | Q155 |
| Itens ligados | editar mudança | escolha | não | itens de escopo do projeto | Protótipo |
| Descrição da lição | registrar lição | texto | sim | até 20.000 caracteres | Q75 |
| Data da lição | registrar lição | data | não | até a data de hoje (RN-TR-39) | Q75 |
| Tipo da lição | registrar lição | escolha | sim | melhorar ou manter; padrão melhorar (RN-TR-27) | Q75 |
| Conhecimento | registrar lição | escolha | sim | explícito ou tácito; padrão explícito | Q75 |
| Alcance | registrar lição | escolha | sim | projeto, outras equipes ou organização; padrão projeto | Q75 |
| Origem, domínio e questão de origem | registrar lição | texto e escolhas | não | a questão de origem é do mesmo projeto (RN-TR-40) | Q75 |

**Funções**

| Código | Requisito | Regras | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|---|
| RF-TR-01 | O sistema deve mostrar o painel do trabalho do projeto, com o resumo das questões, das mudanças e das lições e os alertas do domínio. | RN-TR-07, RN-TR-08, RN-TR-10, RN-TR-12, RN-TR-23, RN-TR-24, RN-TR-35 | Q72, Q112, Q167 | alterado | Núcleo | 2 | teste |
| RF-TR-02 | O sistema deve listar as questões do projeto, com filtro. | RN-TR-07 | Protótipo (Q209) | confirmado | Núcleo | 2 | teste |
| RF-TR-03 | O sistema deve permitir registrar uma questão. | RN-TR-01 a RN-TR-03, RN-TR-05, RN-TR-30, RN-TR-31, RN-TR-33 | Q74, Q75 | alterado | Núcleo | 2 | teste |
| RF-TR-04 | O sistema deve permitir editar e resolver uma questão e mostrar as lições ligadas a ela. | RN-TR-01 a RN-TR-04, RN-TR-06, RN-TR-07, RN-TR-30, RN-TR-31, RN-TR-33 | Q73, Q74, Q75, Q112, Q168 | alterado | Núcleo | 2 | teste |
| RF-TR-05 | O sistema deve permitir excluir uma questão cadastrada por engano. | RN-TR-11, RN-DA-31 | Q73, Q168, Q198 | alterado | Núcleo | 2 | teste |
| RF-TR-06 | O sistema deve listar as mudanças do projeto e as mudanças pedidas por cada parte interessada. | RN-TR-14, RN-TR-35 | Q70, Q71, Q72, Q112 | alterado | Núcleo | 1 | teste |
| RF-TR-07 | O sistema deve permitir registrar uma mudança, em rascunho. | RN-TR-13, RN-TR-14, RN-TR-16, RN-TR-22, RN-TR-37 | Q10, Q69, Q70, Q71, Q72, Q112, Q176 | alterado | Núcleo | 1 | teste |
| RF-TR-08 | O sistema deve permitir editar uma mudança e registrar a decisão da autoridade de mudança, com quem decidiu, a comunicação às partes e os itens ligados. | RN-TR-14 a RN-TR-21, RN-TR-36, RN-TR-38, RN-PL-31 | Q62, Q69, Q70, Q71, Q72, Q73b, Q112, Q176 | alterado | Núcleo | 1 | teste |
| RF-TR-09 | O sistema deve permitir excluir uma mudança em rascunho. | RN-TR-19, RN-DA-31 | Q72, Q73b, Q198 | alterado | Núcleo | 1 | teste |
| RF-TR-10 | O sistema deve listar as lições aprendidas e permitir registrar uma lição. | RN-TR-26, RN-TR-27, RN-TR-39, RN-TR-40 | Q73, Q75 | alterado | Núcleo | 2 | teste |
| RF-TR-11 | O sistema deve permitir marcar e desmarcar uma lição como aplicada. | RN-TR-28 | Q73, Q75 | alterado | Núcleo | 2 | teste |
| RF-TR-12 | O sistema deve permitir excluir uma lição, que vai para a lixeira. | RN-TR-29, RN-DA-31 | Q73, Q198 | alterado | Núcleo | 2 | teste |
| RF-TR-13 | O sistema deve permitir cancelar uma questão, com justificativa. | RN-TR-32 | Q73, Q168 | novo | Núcleo | 2 | teste |

**Regras de negócio**

| Código | Regra | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RN-TR-01 | A questão deve ter título. | Regra do PMO (Q75) | confirmado | Núcleo | 2 | teste |
| RN-TR-02 | Uma questão nova deve começar com prioridade média e situação aberta. | PMBOK 7 §4.6.2, p. 185; os valores são regra do PMO (Q75) | confirmado | Núcleo | 2 | teste |
| RN-TR-03 | A questão deve ter responsável, escolhido entre os membros da equipe. | PMBOK 7 §4.6.2, p. 185 (Q74) | alterado | Núcleo | 2 | teste |
| RN-TR-04 | Para resolver uma questão, a resolução deve estar descrita; sem ela, o sistema deve recusar a gravação com a mensagem de erro, sem mudar a situação. | PMBOK 7 p. 185; exigir a resolução é regra do PMO (Q112) | alterado | Núcleo | 2 | teste |
| RN-TR-05 | A exigência da resolução deve valer também no cadastro de uma questão já resolvida. | Regra do PMO (Q75) | alterado | Núcleo | 2 | teste |
| RN-TR-06 | O sistema deve gravar a data de resolução ao resolver a questão, mantendo a primeira data, e apagá-la ao reabrir. | Regra do PMO (Q75) | confirmado | Núcleo | 2 | teste |
| RN-TR-07 | A questão atrasada deve ser a não resolvida com prazo antes de hoje. | Regra do PMO (Q75) | confirmado | Núcleo | 2 | teste |
| RN-TR-08 | Quando uma questão está atrasada, o sistema deve mostrar um alerta alto. | PMBOK 7 p. 185; o prazo é regra do PMO (Q74, Q159, Q166c) | confirmado | Núcleo | 3 | teste |
| RN-TR-10 | Quando uma questão de prioridade alta não tem prazo, o sistema deve mostrar um alerta médio. | Regra do PMO (Q159) | confirmado | Núcleo | 3 | teste |
| RN-TR-11 | O sistema deve permitir excluir somente a questão aberta que continua na situação em que foi registrada, que não foi aberta pelo sistema a partir de um risco e que não tem reserva usada. | Regra do PMO (Q73, Q168) | alterado | Núcleo | 2 | teste |
| RN-TR-12 | O sistema deve mostrar o tempo médio de resolução: a média dos dias em aberto das questões resolvidas. | Regra do PMO (Q75) | confirmado | Núcleo | 2 | teste |
| RN-TR-13 | A mudança deve ter título. | Regra do PMO (Q75) | confirmado | Núcleo | 1 | teste |
| RN-TR-14 | A situação da mudança deve seguir o fluxo rascunho, em revisão, liberada, aguardando decisão, aprovada ou rejeitada, e implementada; a devolução leva de volta a rascunho. | PMBOK 7 §4.6.2, p. 185; o fluxo é regra do PMO (Q72) | alterado | Núcleo | 1 | teste |
| RN-TR-15 | Aprovar, rejeitar ou implementar a mudança deve registrar quem decidiu, escolhido entre as partes interessadas e os membros da equipe, em nome da autoridade de mudança do termo. | PMBOK 7 p. 77 e 87 (Q69, Q176) | alterado | Núcleo | 1 | teste |
| RN-TR-16 | Para ficar pronta para revisão, a mudança deve ter solicitante, valor esperado, os 6 impactos (escopo, cronograma, orçamento, recursos, partes interessadas e riscos, aceitando "sem impacto") e os riscos novos, em cada nível de exigência. | PMBOK 7 §2.5.7; §2.6, p. 87; Tabela 2-7, p. 79 (Q62, Q70, Q112) | alterado | Núcleo | 2 | teste |
| RN-TR-17 | O sistema deve permitir passar a implementada somente a mudança aprovada. | PMBOK 7 p. 77 (Q75) | confirmado | Núcleo | 1 | teste |
| RN-TR-18 | O sistema deve recusar a mudança de situação fora do fluxo da RN-TR-14. | Regra do PMO (Q72) | alterado | Núcleo | 1 | teste |
| RN-TR-19 | O sistema deve permitir excluir a mudança somente na situação rascunho, inclusive depois de uma devolução. | PMBOK 7 §4.6.2, p. 185 (Q73b) | alterado | Núcleo | 1 | teste |
| RN-TR-20 | O sistema deve recusar a edição e a exclusão de mudança aprovada, rejeitada ou implementada; alterar o que foi aprovado exige uma nova mudança. | PMBOK 7 §4.6.2, p. 185 (Q72, Q73b) | alterado | Núcleo | 1 | teste |
| RN-TR-21 | O sistema deve gravar a data da decisão quando a mudança passa a aprovada ou rejeitada. | Regra do PMO (Q75) | alterado | Núcleo | 1 | teste |
| RN-TR-22 | O solicitante da mudança deve ser escolhido entre as partes interessadas e os membros da equipe. | PMBOK 7 p. 77 (Q70, Q176) | alterado | Núcleo | 2 | teste |
| RN-TR-23 | Quando uma mudança pendente foi criada há mais de 7 dias, o sistema deve mostrar um alerta médio. | Regra do PMO (Q155) | confirmado | Núcleo | 3 | teste |
| RN-TR-24 | Quando uma mudança aprovada ou implementada ainda não foi comunicada às partes interessadas, o sistema deve mostrar um alerta médio. | PMBOK 7 §2.5.7, p. 77 (Q155) | confirmado | Núcleo | 3 | teste |
| RN-TR-25 | O sistema deve mostrar quantas mudanças decididas tiveram a avaliação completa dos 6 impactos. | PMBOK 7 Tabela 2-7, p. 79 (Q75) | confirmado | Núcleo | 2 | teste |
| RN-TR-26 | A lição aprendida deve ter descrição. | PMBOK 7 p. 185; a descrição obrigatória é regra do PMO (Q75) | confirmado | Núcleo | 2 | teste |
| RN-TR-27 | Uma lição nova deve começar com o tipo melhorar, o conhecimento explícito e o alcance projeto. | PMBOK 7 §2.5.8, p. 77–78; os padrões são regra do PMO (Q75) | alterado | Núcleo | 2 | teste |
| RN-TR-28 | Marcar a lição como aplicada deve gravar a data; desmarcar deve apagá-la. | PMBOK 7 p. 185 (Q75) | confirmado | Núcleo | 2 | teste |
| RN-TR-29 | Excluir uma lição deve mandá-la para a lixeira. | Regra do PMO (Q73) | alterado | Núcleo | 2 | teste |
| RN-TR-30 | Um prazo de questão inválido deve ficar vazio. | Regra do PMO (Q75) | confirmado | Núcleo | 2 | teste |
| RN-TR-31 | O risco ligado à questão deve ser do mesmo projeto. | Regra do PMO (Q75) | confirmado | Núcleo | 2 | teste |
| RN-TR-32 | Cancelar uma questão deve exigir justificativa. | Regra do PMO (Q73, Q168) | novo | Núcleo | 2 | teste |
| RN-TR-33 | No nível rigoroso, a questão deve ter prazo. | Regra do PMO (Q74) | confirmado | Núcleo | 2 | teste |
| RN-TR-34 | Os dias em aberto de uma questão devem ser a data de resolução, ou a de hoje, menos a data de criação. | Regra do PMO (Q75) | confirmado | Núcleo | 2 | teste |
| RN-TR-35 | As mudanças pendentes devem ser as em revisão e as aguardando decisão. | Regra do PMO (Q112) | alterado | Núcleo | 1 | teste |
| RN-TR-36 | A rejeição da mudança deve ser definitiva; a ideia volta como uma nova mudança, que cita a anterior. | Regra do PMO (Q72) | novo | Núcleo | 1 | teste |
| RN-TR-37 | A tela de mudança deve explicar que, em projeto adaptativo, o trabalho novo entra como item do backlog e a mudança formal só altera o termo ou a linha de base de custo e de prazo; e que, em projeto híbrido, só a parte preditiva passa por mudança formal. | PMBOK 7 §2.5.7, p. 76–77 (Q71) | novo | Núcleo | 2 | teste |
| RN-TR-38 | Editar uma mudança liberada ou aguardando decisão deve devolvê-la a rascunho e tirar a liberação. | Regra do PMO (Q15, Q73b) | novo | Núcleo | 1 | teste |
| RN-TR-39 | A data da lição deve ser no máximo a data de hoje. | Regra do PMO (Q75) | confirmado | Núcleo | 2 | teste |
| RN-TR-40 | A questão de origem da lição deve ser do mesmo projeto. | Regra do PMO (Q75) | confirmado | Núcleo | 2 | teste |

A regra TR-09 do protótipo, alerta de questão sem responsável nem parte ligada, saiu (Q167). Na RN-TR-15, quem decidiu pode ser uma parte interessada ou um membro da equipe (Q176), o que vale para a mudança no lugar da RN-PM-54. Quando a mudança aprovada altera o termo, nasce uma nova versão dele (RN-PL-31).

#### 3.2.10 Entrega (EN)

Itens de escopo e backlog, requisitos, definição de pronto, aceite e quadro de tarefas, no núcleo; linha de base do escopo, custo da qualidade e benefícios, no módulo Escopo, qualidade e benefícios (Q31).

**Entradas**

| Entrada | Onde | Tipo | Obrigatória | Valores válidos | Origem |
|---|---|---|---|---|---|
| Título do item | criar e editar item | texto | sim | até 20.000 caracteres | Q85 |
| Tipo do item | criar e editar item | escolha | sim | épico, funcionalidade, história, entregável, pacote de trabalho ou requisito (RN-EN-02) | Q85 |
| Item pai | criar e editar item | escolha | não | item do mesmo projeto, diferente dele e dos descendentes dele (RN-EN-03) | Q85 |
| Ordem, valor de negócio e estimativa | criar e editar item | números | não | ordem de 1 a 1.000.000; valor de 1 a 5; estimativa maior ou igual a 0 (RN-EN-04) | Q85 |
| Classificação MoSCoW | criar e editar item | escolha | não | deve, deveria, poderia ou não terá agora | Q85 |
| Critérios de aceite | criar e editar item | texto | para aceitar; no nível rigoroso, para começar (RN-EN-09, RN-EN-10) | até 20.000 caracteres | Q82 |
| Situação do item | editar item; quadro de tarefas | escolha | sim | a fazer, em andamento, concluído, aceito ou cancelado (RN-EN-07) | Q80 |
| Quem aceitou | aceitar item | escolha | sim, ao aceitar | uma parte interessada do projeto (RN-EN-09) | Q82 |
| Motivo do cancelamento | cancelar item | texto | sim (RN-EN-33) | até 20.000 caracteres | Q80, Q81 |
| Definição de pronto | painel da entrega | texto | não | até 20.000 caracteres | Protótipo |
| Unidade de estimativa | painel da entrega | escolha | sim | pontos, horas ou dias; padrão pontos (RN-EN-05) | Q85 |
| Limite de trabalho em andamento | painel da entrega | número inteiro | não | de 1 a 1.000, ou sem limite (RN-EN-05) | Q83 |
| Resposta de completude do conjunto | escopo | sim ou não | não | — | Q84b |
| Mudança ligada à nova linha de base | refazer linha de base, no módulo | escolha | sim (RN-EN-17) | uma mudança aprovada do projeto | Q79 |
| Categoria, descrição, data, custo e defeito resolvido | custo da qualidade, no módulo | escolha, texto, data, número e marca | categoria e descrição | categoria de prevenção, avaliação, falha interna ou falha externa; data até hoje; custo maior ou igual a 0 (RN-EN-26, RN-EN-38) | Q85 |
| Descrição, situação, data prevista e resultado medido do benefício | benefícios, no módulo | texto, escolha, data e texto | descrição; resultado quando realizado ou parcial | situação planejado, parcial, realizado ou não realizado (RN-EN-28, RN-EN-29) | Q85 |

**Funções**

| Código | Requisito | Regras | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|---|
| RF-EN-01 | O sistema deve mostrar o painel da entrega, com a definição de pronto, a unidade de estimativa, o limite de trabalho em andamento e os alertas do domínio. | RN-EN-05, RN-EN-15, RN-EN-19 a RN-EN-24, RN-EN-27 | Q80, Q83, Q155, Q156, Q159 | alterado | Núcleo | 2 | teste |
| RF-EN-02 | O sistema deve permitir gravar a linha de base do escopo e refazê-la ligada a uma mudança aprovada. | RN-EN-16, RN-EN-17, RN-EN-32, RN-EN-36 | Q79, Q80, Q84b | alterado | Escopo, qualidade e benefícios | 3 | teste |
| RF-EN-03 | O sistema deve mostrar o escopo e o backlog em árvore, com os itens fora da linha de base marcados. | RN-EN-02, RN-EN-07, RN-EN-15, RN-EN-32 | Q80, Q84b | alterado | Núcleo | 2 | teste |
| RF-EN-04 | O sistema deve permitir gravar a ordem de prioridade dos itens. | — | Protótipo (Q209) | confirmado | Núcleo | 2 | teste |
| RF-EN-05 | O sistema deve permitir criar um item, também a partir de uma mudança ou de um risco. | RN-EN-01 a RN-EN-04, RN-EN-06, RN-EN-31 | Q80, Q82 | alterado | Núcleo | 2 | teste |
| RF-EN-06 | O sistema deve permitir editar, concluir e aceitar um item. | RN-EN-06 a RN-EN-12, RN-EN-34 | Q80, Q81, Q82, Q84 | alterado | Núcleo | 2 | teste |
| RF-EN-07 | O sistema deve permitir excluir um item criado por engano. | RN-EN-14, RN-DA-31 | Q81, Q198 | alterado | Núcleo | 2 | teste |
| RF-EN-08 | O sistema deve mostrar o quadro de tarefas, com as colunas a fazer, em andamento, concluído e aceito. | RN-EN-07 a RN-EN-13, RN-EN-20 | Q80, Q82, Q83 | alterado | Núcleo | 2 | teste |
| RF-EN-09 | O sistema deve permitir registrar o custo da qualidade e mostrar a conformidade e a não conformidade. | RN-EN-25 a RN-EN-27, RN-EN-38 | Q80, Q159 | alterado | Escopo, qualidade e benefícios | 3 | teste |
| RF-EN-10 | O sistema deve permitir registrar e listar os benefícios do projeto. | RN-EN-28 a RN-EN-30 | Q85 | alterado | Escopo, qualidade e benefícios | 3 | teste |
| RF-EN-11 | O sistema deve permitir editar e excluir um benefício. | RN-EN-28, RN-EN-29, RN-DA-31 | Q85, Q198 | alterado | Escopo, qualidade e benefícios | 3 | teste |
| RF-EN-12 | O sistema deve permitir cancelar um item, com motivo. | RN-EN-33, RN-EN-35 | Q80, Q81 | novo | Núcleo | 2 | teste |

**Regras de negócio**

| Código | Regra | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RN-EN-01 | O item deve ter título. | Regra do PMO (Q85) | confirmado | Núcleo | 2 | teste |
| RN-EN-02 | O tipo padrão de um item novo deve ser entregável nos projetos preditivos e história nos outros. | PMBOK 7 p. 83–84 (Q85) | confirmado | Núcleo | 2 | teste |
| RN-EN-03 | O item pai deve ser do mesmo projeto, diferente do próprio item e dos descendentes dele. | PMBOK 7 p. 84; barrar ciclos é regra do PMO (Q85) | confirmado | Núcleo | 2 | teste |
| RN-EN-04 | A ordem do item deve ir de 1 a 1.000.000, o valor de negócio de 1 a 5, e a estimativa deve ser maior ou igual a 0. | PMBOK 7 p. 181 (MoSCoW); as faixas são regra do PMO (Q85) | confirmado | Núcleo | 2 | teste |
| RN-EN-05 | A unidade de estimativa padrão deve ser pontos, e o limite de trabalho em andamento deve ir de 1 a 1.000 ou ficar sem limite. | PMBOK 7 p. 57–58, 99 e 109; as faixas são regra do PMO (Q85) | confirmado | Núcleo | 2 | teste |
| RN-EN-06 | A tela do requisito deve mostrar os 6 critérios de requisito bem documentado: claro, conciso e consistente, marcados à mão; verificável, quando tem critérios de aceite; rastreável, pelo código; e completo, com a resposta do conjunto. | PMBOK 7 §2.6.2.1, p. 83 (Q84, Q84b) | alterado | Núcleo | 2 | teste |
| RN-EN-07 | A situação do item deve ser a fazer, em andamento, concluído, aceito ou cancelado; "feito" é o item concluído ou aceito. | PMBOK 7 p. 85 e 109 (Q80) | alterado | Núcleo | 2 | teste |
| RN-EN-08 | Quando o projeto tem definição de pronto, concluir ou aceitar um item deve exigir a confirmação dela. | PMBOK 7 §2.6.2.2, p. 85 (Q85) | confirmado | Núcleo | 2 | teste |
| RN-EN-09 | Aceitar um item deve exigir critérios de aceite e quem aceitou, escolhido entre as partes interessadas do projeto. | PMBOK 7 Glossário (Acceptance Criteria), p. 235; p. 85 (Q82) | alterado | Núcleo | 2 | teste |
| RN-EN-10 | No nível rigoroso, passar um item para em andamento deve exigir critérios de aceite. | PMBOK 7 p. 179; a exigência é regra do PMO (Q85, Q166c) | confirmado | Núcleo | 2 | teste |
| RN-EN-11 | O sistema deve ajustar as datas do item pela situação: a fazer apaga início, conclusão e aceite; em andamento grava o início e apaga conclusão e aceite; concluído grava início e conclusão e apaga o aceite; aceito grava as três; uma data que já existia é mantida. | Regra do PMO (Q85) | confirmado | Núcleo | 2 | teste |
| RN-EN-12 | A situação do item deve seguir o fluxo a fazer, em andamento, concluído e aceito; o sistema deve permitir voltar de em andamento para a fazer e de concluído para em andamento, e manter o aceito como definitivo. | PMBOK 7 §2.6.2.2, p. 85; p. 109 (Q80) | alterado | Núcleo | 2 | teste |
| RN-EN-13 | No quadro de tarefas, o item deve mudar de coluna pelas mesmas regras da tela do item; quando falta algo, o sistema deve levar à página do item. | PMBOK 7 p. 109 (Q85) | confirmado | Núcleo | 2 | teste |
| RN-EN-14 | O sistema deve permitir excluir somente o item a fazer, fora da linha de base e sem aceite registrado. | PMBOK 7 §4.6.5, p. 188 (Q81) | alterado | Núcleo | 2 | teste |
| RN-EN-15 | Os itens de trabalho devem ser os itens sem filhos e não cancelados; os percentuais de concluído e de aceito devem usar a soma das estimativas quando cada item de trabalho tem estimativa e, nos outros casos, a contagem de itens. | Regra do PMO (Q85) | confirmado | Núcleo | 2 | teste |
| RN-EN-16 | A linha de base do escopo deve exigir pelo menos um item de trabalho e gravar o título, a estimativa, o custo planejado e as datas de cada item; a versão é o número de linhas de base gravadas. | PMBOK 7 p. 188 (Q79) | confirmado | Escopo, qualidade e benefícios | 3 | teste |
| RN-EN-17 | Refazer a linha de base do escopo deve exigir uma mudança aprovada ligada. | PMBOK 7 §4.6.5, p. 188; §2.6.2.3, p. 87 (Q79) | alterado | Escopo, qualidade e benefícios | 3 | teste |
| RN-EN-18 | Num projeto que não é adaptativo, quando um item de trabalho fica fora da linha de base atual sem mudança aprovada ou implementada ligada, o sistema deve mostrar um alerta alto e marcar o escopo como crítico no semáforo. | PMBOK 7 p. 87 (Q156) | confirmado | Escopo, qualidade e benefícios | 3 | teste |
| RN-EN-19 | Num projeto adaptativo, quando, nos últimos 30 dias, entrou trabalho novo em quantidade igual ou maior que a concluída, o sistema deve mostrar um alerta médio; com linha de base, novo é o item fora dela, e, sem linha de base, só conta o projeto que já tinha itens antes desses 30 dias. | PMBOK 7 p. 76; os 30 dias são regra do PMO (Q156) | alterado | Núcleo | 3 | teste |
| RN-EN-20 | Com o limite de trabalho em andamento atingido, o sistema deve recusar passar mais um item para em andamento. | PMBOK 7 §2.7.2.2, p. 99; p. 109 (Q83) | alterado | Núcleo | 2 | teste |
| RN-EN-21 | Quando um item em andamento não tem critérios de aceite, o sistema deve mostrar um alerta médio. | PMBOK 7 p. 84 e 179 (Q159, Q166c) | confirmado | Núcleo | 3 | teste |
| RN-EN-22 | Quando um item está concluído há mais de 14 dias e ainda não foi aceito, o sistema deve mostrar um alerta médio. | Regra do PMO (Q159) | confirmado | Núcleo | 3 | teste |
| RN-EN-23 | Quando uma mudança aprovada ou implementada não tem item de escopo ligado, o sistema deve mostrar um alerta informativo. | PMBOK 7 p. 77 (Q155) | alterado | Núcleo | 3 | teste |
| RN-EN-24 | Num projeto adaptativo ou híbrido com itens e sem definição de pronto, o sistema deve mostrar um alerta informativo. | PMBOK 7 p. 85 (Q159) | confirmado | Núcleo | 3 | teste |
| RN-EN-25 | O custo da qualidade deve ter 4 categorias: prevenção e avaliação, que contam como conformidade, e falha interna e falha externa, que contam como não conformidade. | PMBOK 7 p. 88 (Q85) | confirmado | Escopo, qualidade e benefícios | 3 | teste |
| RN-EN-26 | O registro de custo da qualidade deve ter categoria e descrição e custo maior ou igual a 0. | Regra do PMO (Q85) | confirmado | Escopo, qualidade e benefícios | 3 | teste |
| RN-EN-27 | Quando o custo das falhas passa do custo de prevenção e avaliação e é maior que zero, o sistema deve mostrar um alerta informativo, citando o equilíbrio do custo da qualidade. | PMBOK 7 p. 88; o critério é regra do PMO (Q159) | alterado | Escopo, qualidade e benefícios | 3 | teste |
| RN-EN-28 | O benefício deve ter descrição, e a situação dele deve ser planejado, parcial, realizado ou não realizado. | PMBOK 7 p. 82 e 184; as situações são regra do PMO (Q85) | confirmado | Escopo, qualidade e benefícios | 3 | teste |
| RN-EN-29 | O benefício realizado ou parcial deve ter o resultado medido, também no cadastro. | Regra do PMO (Q85) | alterado | Escopo, qualidade e benefícios | 3 | teste |
| RN-EN-30 | Quando um benefício planejado ou parcial passa da data prevista, o sistema deve mostrar um alerta médio. | Regra do PMO (Q159) | confirmado | Escopo, qualidade e benefícios | 3 | teste |
| RN-EN-31 | Ao criar um item a partir de uma mudança ou de um risco, o sistema deve preencher o vínculo, o título e a descrição. | PMBOK 7 p. 185 (Q85) | confirmado | Núcleo | 2 | teste |
| RN-EN-32 | A completude do conjunto de requisitos deve ser respondida na tela do escopo e conferida ao gravar a linha de base. | PMBOK 7 §2.6.2.1, p. 83 (Q84b) | novo | Núcleo | 2 | teste |
| RN-EN-33 | Cancelar um item deve exigir motivo. | Regra do PMO (Q80) | novo | Núcleo | 2 | teste |
| RN-EN-34 | Um defeito achado depois do aceite deve virar um item novo, ligado ao original. | PMBOK 7 p. 85 (Q80) | novo | Núcleo | 2 | teste |
| RN-EN-35 | O sistema deve permitir cancelar um item da linha de base somente com uma mudança aprovada ligada. | PMBOK 7 §4.6.5, p. 188 (Q81) | novo | Escopo, qualidade e benefícios | 3 | teste |
| RN-EN-36 | A primeira linha de base do escopo deve ser liberada junto com o termo de abertura. | PMBOK 7 §4.6.5, p. 188 (Q79) | novo | Escopo, qualidade e benefícios | 3 | teste |
| RN-EN-37 | A mudança do limite de trabalho em andamento deve ficar registrada no histórico. | Regra do PMO (Q83) | novo | Núcleo | 2 | teste |
| RN-EN-38 | A data do registro de custo da qualidade deve ser no máximo a data de hoje. | Regra do PMO (Q85) | confirmado | Escopo, qualidade e benefícios | 3 | teste |

#### 3.2.11 Medição (ME)

Semáforo, limite de variação, plano de exceção e relatório de status, no núcleo; valor agregado, burnup, burndown, velocidade, fluxo, previsão e indicadores (KPIs), no módulo Medição avançada (Q31, Q174b). O relatório de status é de revisão obrigatória (RN-PM-16). Os termos do valor agregado mostram a sigla original em inglês entre parênteses (Q113).

**Entradas**

| Entrada | Onde | Tipo | Obrigatória | Valores válidos | Origem |
|---|---|---|---|---|---|
| Plano de exceção | painel da medição | texto | não | até 20.000 caracteres | Q174b |
| Nome do indicador | criar indicador, no módulo | texto | sim | até 20.000 caracteres (RN-ME-18) | Q94 |
| Tipo do indicador | criar indicador, no módulo | escolha | sim | antecedente ou de resultado; padrão de resultado (RN-ME-32) | Q94 |
| Direção | criar indicador, no módulo | escolha | sim | maior é melhor ou menor é melhor; padrão maior | Q94 |
| Meta e limite | criar indicador, no módulo | número | não | aceitam valores negativos | Q94 |
| Categoria do indicador | criar indicador, no módulo | escolha | não | uma das 7 categorias do PMO | Q94 |
| Valor e data da medição | registrar medição, no módulo | número e data | valor | data até hoje (RN-ME-19) | Q94 |
| Data do relatório | relatório de status | data | sim | até a data de hoje (RN-ME-34) | Q94 |
| Análise, próximos passos e pedidos de apoio | relatório de status | texto | não | até 20.000 caracteres cada | Q37 |
| Explicação de cada dimensão em vermelho | relatório de status | texto | sim, para ficar pronto (RN-ME-35) | até 20.000 caracteres | Q89 |

**Funções**

| Código | Requisito | Regras | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|---|
| RF-ME-01 | O sistema deve mostrar o painel da medição, com o semáforo, o limite de variação e o plano de exceção, e permitir registrar o plano de exceção. | RN-ME-06 a RN-ME-13, RN-ME-25 | Q88, Q90, Q174b, Q177 | alterado | Núcleo | 2 | teste |
| RF-ME-02 | O sistema deve permitir criar um indicador e mostrar o histórico de medições dele. | RN-ME-18, RN-ME-20, RN-ME-21, RN-ME-32, RN-ME-36 | Q93, Q94 | alterado | Medição avançada | 3 | teste |
| RF-ME-03 | O sistema deve permitir registrar e excluir uma medição e excluir um indicador. | RN-ME-19, RN-DA-31 | Q94, Q198 | alterado | Medição avançada | 3 | teste |
| RF-ME-04 | O sistema deve permitir preparar o relatório de status: o sistema monta os indicadores, e o gerente completa com a análise, os próximos passos e os pedidos de apoio. | RN-ME-26, RN-ME-27, RN-ME-33 a RN-ME-35, RN-ME-39, RN-PM-16 | Q10, Q16, Q37, Q87, Q89, Q91, Q104 | alterado | Núcleo | 2 | teste |
| RF-ME-05 | O sistema deve mostrar o relatório de status e permitir excluí-lo enquanto está em rascunho. | RN-ME-28, RN-ME-37, RN-DA-31 | Q11, Q91, Q198 | alterado | Núcleo | 2 | teste |
| RF-ME-06 | O sistema deve mostrar o valor agregado, o burnup, o burndown da iteração, a velocidade, o fluxo e a previsão de término. | RN-ME-01 a RN-ME-05, RN-ME-14 a RN-ME-17 | Q86, Q87, Q94 | alterado | Medição avançada | 3 | teste |

**Regras de negócio**

| Código | Regra | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RN-ME-01 | O valor agregado deve seguir a regra 0/100: o item agrega valor só quando está concluído ou aceito. | PMBOK 7 §2.7.2.3, p. 100; a regra 0/100 é regra do PMO (Q86) | confirmado | Medição avançada | 3 | teste |
| RN-ME-02 | O valor planejado deve crescer de forma linear pelos dias do item, contando o início e o fim: 0 antes do início e 100% no término; o item sem data entra no orçamento no término e fica fora do valor planejado. | Regra do PMO (Q86) | confirmado | Medição avançada | 3 | teste |
| RN-ME-03 | Os valores da linha de base (custo e datas) devem valer antes dos atuais do item, e só devem entrar os itens de trabalho com custo planejado. | PMBOK 7 p. 100 (Q94) | confirmado | Medição avançada | 3 | teste |
| RN-ME-04 | As fórmulas devem ser: ONP (BAC), a soma dos custos planejados; VA (EV), a soma dos custos dos itens feitos; CR (AC), a soma dos custos reais; IDP (SPI) = VA ÷ VP (PV); IDC (CPI) = VA ÷ CR; ENT (EAC) = ONP ÷ IDC; EPT (ETC) = ENT − CR; VNT (VAC) = ONP − ENT; IDPT (TCPI) = (ONP − VA) ÷ (ONP − CR), só quando ONP passa de CR; variação de prazo (SV) = VA − VP; variação de custo (CV) = VA − CR. | PMBOK 7 p. 100–105 (Q94, Q113) | alterado | Medição avançada | 3 | teste |
| RN-ME-05 | O custo real deve somar só os itens que entram no valor agregado e no valor planejado. | PMBOK 7 §2.7.2.3, p. 100 (Q87) | alterado | Medição avançada | 3 | teste |
| RN-ME-06 | O limite de variação deve ser o registrado no termo do projeto, com 10% de padrão, de 1% a 50%. | PMBOK 7 §2.7.5, p. 113 (Q88, Q177) | alterado | Núcleo | 2 | teste |
| RN-ME-07 | As faixas do semáforo por índice devem ser: verde, no rumo, a partir de 1 menos o limite; amarelo, atenção, a partir de 1 menos 2 vezes o limite; vermelho, crítico, abaixo disso; e "sem dados" sem índice. | PMBOK 7 p. 106; as faixas são regra do PMO (Q94) | confirmado | Núcleo | 2 | teste |
| RN-ME-08 | O semáforo de prazo deve usar, nesta ordem: o IDP, se existe; senão, a previsão de término contra o fim planejado (sem atraso, verde; atraso até o limite de variação aplicado à duração planejada, amarelo; acima, vermelho); senão, verde com o escopo inteiro concluído; senão, "sem dados". | PMBOK 7 p. 100; a ordem e as faixas são regra do PMO (Q94) | confirmado | Núcleo | 2 | teste |
| RN-ME-09 | O semáforo de custo deve usar o IDC e, sem IDC, mostrar "sem dados". | PMBOK 7 p. 100 (Q94) | confirmado | Núcleo | 2 | teste |
| RN-ME-10 | O semáforo de escopo deve ser: sem itens, "sem dados"; com escopo crescendo sem controle num projeto que não é adaptativo, vermelho; com o backlog de um projeto adaptativo crescendo, amarelo; nos outros casos, verde. | PMBOK 7 p. 76 e 87; as cores são regra do PMO (Q94, Q156) | confirmado | Núcleo | 2 | teste |
| RN-ME-11 | O semáforo de riscos deve ser: sem riscos ativos, "sem dados"; com ameaça alta sem resposta ativa, vermelho; com ameaça alta ou risco geral alto, amarelo; nos outros casos, verde. | Regra do PMO (Q94) | confirmado | Núcleo | 2 | teste |
| RN-ME-12 | O semáforo das partes interessadas deve usar a média da última nota de satisfação de cada parte (a partir de 3,5, verde; a partir de 2,5, amarelo; abaixo, vermelho) e, sem notas, mostrar "sem dados". | PMBOK 7 p. 103; as faixas são regra do PMO (Q94, Q108) | alterado | Núcleo | 2 | teste |
| RN-ME-13 | O semáforo de questões deve ser: sem questões, "sem dados"; com questão atrasada, vermelho; com questão aberta, amarelo; nos outros casos, verde. | Regra do PMO (Q90) | alterado | Núcleo | 2 | teste |
| RN-ME-14 | A velocidade deve ser a média do concluído nas últimas 3 iterações encerradas, contando o concluído até o fim de cada iteração. | PMBOK 7 p. 109; Glossário, p. 252; as 3 iterações são regra do PMO (Q94) | confirmado | Medição avançada | 3 | teste |
| RN-ME-15 | A previsão de término deve usar a velocidade (iterações restantes = restante ÷ velocidade, arredondado para cima; data = hoje mais as iterações vezes a duração média delas) e, sem velocidade, a vazão dos últimos 30 dias. | PMBOK 7 §2.7.2.7, p. 105; o cálculo é regra do PMO (Q94) | confirmado | Medição avançada | 3 | teste |
| RN-ME-16 | O fluxo deve mostrar o lead time (conclusão menos criação), o cycle time (conclusão menos início), dos itens dos últimos 90 dias, a vazão dos últimos 30 dias, o trabalho em andamento e a fila. | PMBOK 7 p. 99; Glossário, p. 251; as janelas são regra do PMO (Q94) | confirmado | Medição avançada | 3 | teste |
| RN-ME-17 | O burnup deve comparar o escopo e o concluído por semana, e o burndown da iteração, a linha ideal e o restante. | PMBOK 7 p. 109; Figura 2-30, p. 111 (Q94) | confirmado | Medição avançada | 3 | teste |
| RN-ME-18 | O indicador deve ter nome. | PMBOK 7 p. 95–96 (Q94) | confirmado | Medição avançada | 3 | teste |
| RN-ME-19 | A medição deve ter valor e data até a de hoje. | Regra do PMO (Q94) | confirmado | Medição avançada | 3 | teste |
| RN-ME-20 | A situação do indicador pela última medição deve ser: crítico, quando passa do limite (igual ao limite não é crítico); ok, sem meta ou com a meta atingida; atenção, nos outros casos; e "sem dados", sem medição. | PMBOK 7 Glossário (Threshold), p. 251; "atenção" é regra do PMO (Q94) | confirmado | Medição avançada | 3 | teste |
| RN-ME-21 | A tendência deve comparar as duas últimas medições, e a piora seguida deve ser a piora nas duas últimas variações, com pelo menos 3 medições. | Regra do PMO (Q94) | confirmado | Medição avançada | 3 | teste |
| RN-ME-22 | Quando um indicador passa do limite, o sistema deve mostrar um alerta alto. | PMBOK 7 p. 113 (Q157) | confirmado | Medição avançada | 3 | teste |
| RN-ME-23 | Quando um indicador antecedente tem piora seguida e ainda não está crítico, o sistema deve mostrar um alerta médio. | PMBOK 7 p. 96 e 113 (Q157) | confirmado | Medição avançada | 3 | teste |
| RN-ME-24 | Quando um indicador está há mais de 30 dias sem medição, o sistema deve mostrar um alerta informativo. | Regra do PMO (Q157) | confirmado | Medição avançada | 3 | teste |
| RN-ME-25 | Quando uma dimensão do semáforo fica em vermelho e o projeto não tem plano de exceção, o sistema deve mostrar um alerta alto. | PMBOK 7 §2.7.5, p. 113–114 (Q157, Q174b) | confirmado | Núcleo | 3 | teste |
| RN-ME-26 | O relatório de status deve congelar o semáforo, o escopo, o valor agregado, a previsão, os 5 principais riscos ativos, as 5 principais questões abertas e até 8 alertas altos. | PMBOK 7 §4.6.7, p. 190 (Q37) | alterado | Núcleo | 2 | teste |
| RN-ME-27 | O relatório deve sugerir os itens concluídos desde o último relatório, os itens em andamento e os próximos 3 a fazer, pela ordem. | PMBOK 7 p. 190 (Q94) | confirmado | Núcleo | 2 | teste |
| RN-ME-28 | O sistema deve permitir excluir o relatório de status somente em rascunho. | Regra do PMO (Q91) | alterado | Núcleo | 2 | teste |
| RN-ME-29 | O progresso de um domínio na verificação de resultados deve ser (atendidos + 0,5 × parciais) ÷ total, com cada resultado não avaliado, atendido, parcial ou não atendido. | PMBOK 7 Tabelas 2-2 a 2-10 (Q94) | confirmado | Princípios e resultados | 3 | teste |
| RN-ME-30 | Marcar um resultado de domínio como atendido ou parcial deve exigir evidência em texto. | PMBOK 7 Tabelas 2-2 a 2-10 (Q92) | alterado | Princípios e resultados | 3 | teste |
| RN-ME-31 | Quando um item tem custo real e não tem custo planejado, o sistema deve mostrar um alerta médio. | PMBOK 7 §2.7.2.3, p. 100 (Q87, Q158) | novo | Núcleo | 3 | teste |
| RN-ME-32 | Um indicador novo deve começar com o tipo de resultado e a direção que favorece os valores maiores. | Regra do PMO (Q94) | confirmado | Medição avançada | 3 | teste |
| RN-ME-33 | O relatório deve congelar os números ao ser enviado para revisão e congelar de novo no reenvio depois de uma devolução. | Regra do PMO (Q91) | novo | Núcleo | 2 | teste |
| RN-ME-34 | A data do relatório de status deve ser no máximo a data de hoje. | Regra do PMO (Q94) | confirmado | Núcleo | 2 | teste |
| RN-ME-35 | Para ficar pronto para revisão, o relatório deve ter uma explicação para cada dimensão em vermelho. | PMBOK 7 §2.7.3.1, p. 106 (Q89) | novo | Núcleo | 2 | teste |
| RN-ME-36 | O cadastro do indicador deve mostrar os critérios SMART (específico, significativo, atingível, relevante e oportuno) como apoio, sem bloquear a gravação. | PMBOK 7 §2.7.1.2, p. 97 (Q93) | novo | Medição avançada | 3 | teste |
| RN-ME-37 | O sistema deve recusar a alteração e a exclusão do relatório de status liberado. | Regra do PMO (Q15, Q91) | novo | Núcleo | 2 | teste |
| RN-ME-38 | Quando o último relatório de status passa da cadência de relatório do projeto, o sistema deve mostrar ao gerente do projeto e ao supervisor um alerta médio. | Regra do PMO (Q16, Q158) | novo | Núcleo | 3 | teste |
| RN-ME-39 | O relatório de status deve mostrar das partes interessadas só o semáforo agregado. | PMBOK 7 §2.1.1.2, p. 12 (Q104) | novo | Núcleo | 2 | teste |

A tela da verificação de resultados (RN-ME-29 e RN-ME-30) é a RF-PJ-09, do módulo Princípios e resultados.

#### 3.2.12 Incerteza (IN)

Registro de riscos, matriz de probabilidade e impacto, limite de risco, cadência de revisão, reserva de contingência e avaliação do risco geral, no núcleo; valor monetário esperado (EMV), reserva de gerenciamento e as outras incertezas (ambiguidade, complexidade e volatilidade), no módulo Incerteza avançada (Q31, Q172a, Q172b). O limite de risco faz parte do termo (RN-PL-32).

**Entradas**

| Entrada | Onde | Tipo | Obrigatória | Valores válidos | Origem |
|---|---|---|---|---|---|
| Título do risco | registrar e editar risco | texto | sim | até 20.000 caracteres | Q103 |
| Tipo | registrar e editar risco | escolha | sim | ameaça ou oportunidade; padrão ameaça (RN-IN-02) | Q103 |
| Fonte | registrar e editar risco | escolha | não | técnico, social, político, mercado, econômico, regulatório, organizacional, partes interessadas ou equipe (RN-IN-04) | Q103 |
| Probabilidade e impacto | registrar e editar risco | número inteiro | para passar a em resposta (RN-IN-39) | de 1 a 5 (RN-IN-05) | Q103, Q166b |
| Impacto em custo e reserva em R$ | registrar e editar risco | número | não | maior ou igual a 0 | Q103 |
| Impacto em prazo e reserva em dias | registrar e editar risco | número inteiro | não | de 0 a 100.000 | Q103 |
| Estratégia | registrar e editar risco | escolha | para passar a em resposta | a da lista do tipo (RN-IN-03) | Q103, Q166b |
| Responsável | registrar e editar risco | escolha | para passar a em resposta | um membro da equipe | Q166b |
| Plano de contingência | registrar e editar risco | texto | não | até 20.000 caracteres | Q161 |
| Risco residual e riscos secundários | registrar e editar risco | texto | na ameaça acima do limite, para passar a em resposta (RN-IN-40) | até 20.000 caracteres; aceita "nenhum" | Q101, Q173 |
| A quem foi escalado e quando | registrar e editar risco | escolha e data | com a estratégia escalar (RN-IN-35) | uma parte interessada do projeto | Q100 |
| Situação do risco | editar risco | escolha | sim | aberto, em resposta, ocorreu ou encerrado (RN-IN-11) | Q97 |
| Motivo do encerramento | encerrar risco | escolha | sim, ao encerrar (RN-IN-37) | não ocorreu, resposta eficaz ou deixou de existir | Q97 |
| Justificativa da reabertura | reabrir risco | texto | sim (RN-IN-38) | até 20.000 caracteres | Q97 |
| Ganho obtido | oportunidade que ocorreu | texto | sim (RN-IN-16) | até 20.000 caracteres | Q98, Q160 |
| Cadência de revisão dos riscos | painel da incerteza | número inteiro de dias | sim | de 1 a 365; padrão 14 (RN-IN-36) | Q95 |
| Avaliação do risco geral | painel da incerteza | escolha | não | baixo, médio ou alto | Q172b |
| Reserva de gerenciamento | painel, no módulo | número | não | maior ou igual a 0 | Q172a |
| Natureza, descrição e situação de outra incerteza | outras incertezas, no módulo | escolha, texto e escolha | natureza e descrição | natureza geral, ambiguidade, complexidade ou volatilidade; situação aberta, reduzida ou resolvida (RN-IN-33) | Q103 |

**Funções**

| Código | Requisito | Regras | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|---|
| RF-IN-01 | O sistema deve mostrar o painel da incerteza, com a matriz de probabilidade e impacto, o limite de risco, a cadência de revisão, a reserva de contingência e o uso dela, e permitir avaliar o risco geral do projeto. | RN-IN-06 a RN-IN-08, RN-IN-18 a RN-IN-20, RN-IN-22, RN-IN-36, RN-IN-43 | Q95, Q160, Q172a, Q172b, Q177 | alterado | Núcleo | 2 | teste |
| RF-IN-02 | O sistema deve listar os riscos do projeto, com filtros. | RN-IN-02, RN-IN-04, RN-IN-08, RN-IN-11, RN-IN-14 | Q97, Q103 | alterado | Núcleo | 2 | teste |
| RF-IN-03 | O sistema deve permitir registrar um risco, inclusive só com o título. | RN-IN-01 a RN-IN-05, RN-IN-13, RN-IN-17, RN-IN-44 | Q97, Q98, Q103, Q166b | alterado | Núcleo | 2 | teste |
| RF-IN-04 | O sistema deve mostrar o detalhe de um risco, com as revisões, a tendência e as ligações. | RN-IN-06, RN-IN-08, RN-IN-14 | Q97, Q103 | alterado | Núcleo | 2 | teste |
| RF-IN-05 | O sistema deve permitir editar um risco e mudar a situação dele. | RN-IN-01 a RN-IN-05, RN-IN-11 a RN-IN-17, RN-IN-35, RN-IN-37 a RN-IN-40, RN-IN-44 | Q97, Q98, Q100, Q101, Q103, Q166b, Q167, Q173 | alterado | Núcleo | 2 | teste |
| RF-IN-06 | O sistema deve permitir registrar uma revisão do risco. | RN-IN-13, RN-IN-14 | Q97, Q98 | alterado | Núcleo | 2 | teste |
| RF-IN-07 | O sistema deve permitir excluir um risco cadastrado por engano. | RN-IN-32, RN-DA-31 | Q97, Q99, Q198 | alterado | Núcleo | 2 | teste |
| RF-IN-08 | O sistema deve permitir registrar uma ambiguidade, uma complexidade ou uma volatilidade. | RN-IN-33 | Protótipo (Q209) | confirmado | Incerteza avançada | 3 | teste |
| RF-IN-09 | O sistema deve permitir atualizar e excluir uma dessas incertezas. | RN-IN-33, RN-DA-31 | Q198 | alterado | Incerteza avançada | 3 | teste |
| RF-IN-10 | O sistema deve mostrar o valor monetário esperado (EMV) das ameaças e das oportunidades e a reserva de gerenciamento, com o uso dela. | RN-IN-09, RN-IN-10, RN-IN-21, RN-IN-31, RN-IN-41 | Q96, Q162, Q172a | alterado | Incerteza avançada | 3 | teste |
| RF-IN-11 | O sistema deve permitir encerrar um risco, com o motivo. | RN-IN-37 | Q97, Q99 | novo | Núcleo | 2 | teste |

**Regras de negócio**

| Código | Regra | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RN-IN-01 | O risco deve ter título. | Regra do PMO (Q103) | confirmado | Núcleo | 2 | teste |
| RN-IN-02 | O tipo do risco deve ser ameaça ou oportunidade, com ameaça como padrão; um tipo inválido vira ameaça. | PMBOK 7 p. 122 (Q103) | confirmado | Núcleo | 2 | teste |
| RN-IN-03 | A estratégia deve pertencer ao tipo: para a ameaça, evitar, escalar, transferir, mitigar ou aceitar; para a oportunidade, explorar, escalar, compartilhar, melhorar ou aceitar; a estratégia de outro tipo fica vazia. | PMBOK 7 §2.8.5.1 e §2.8.5.2, p. 123–125 (Q103) | confirmado | Núcleo | 2 | teste |
| RN-IN-04 | A fonte do risco deve ser técnica, social, política, mercado, econômica, regulatória, organizacional, partes interessadas ou equipe. | PMBOK 7 Tabela 2-10, p. 129 (as cinco primeiras); as outras são regra do PMO (Q103) | alterado | Núcleo | 2 | teste |
| RN-IN-05 | Probabilidade e impacto devem ir de 1 a 5; o impacto em custo e a reserva em R$, ser maiores ou iguais a 0; e o impacto em prazo e a reserva em dias, ir de 0 a 100.000. | PMBOK 7 p. 122; a escala é regra do PMO (Q103) | confirmado | Núcleo | 2 | teste |
| RN-IN-06 | A pontuação do risco deve ser a probabilidade vezes o impacto. | PMBOK 7 Figura 2-33, p. 124; p. 176 (Q103) | confirmado | Núcleo | 2 | teste |
| RN-IN-07 | O limite de risco deve ser o registrado no termo do projeto, de 1 a 25, com 12 de padrão. | PMBOK 7 §2.8.5, p. 122; os valores são regra do PMO (Q95, Q177) | alterado | Núcleo | 2 | teste |
| RN-IN-08 | O nível do risco deve ser alto quando a pontuação chega ao limite, médio quando o dobro da pontuação chega ao limite, e baixo nos outros casos. | PMBOK 7 p. 122; a faixa média é regra do PMO (Q103) | confirmado | Núcleo | 2 | teste |
| RN-IN-09 | O sistema deve converter a probabilidade para o EMV como 1 = 10%, 2 = 30%, 3 = 50%, 4 = 70% e 5 = 90%, e mostrar essa conversão na tela. | Regra do PMO (Q96) | confirmado | Incerteza avançada | 3 | teste |
| RN-IN-10 | O EMV deve ser a probabilidade em percentual vezes o impacto em custo, negativo na ameaça e positivo na oportunidade, com totais separados por tipo, só dos riscos ativos. | PMBOK 7 p. 126 e 176 (Q103) | confirmado | Incerteza avançada | 3 | teste |
| RN-IN-11 | A situação do risco deve ser aberto, em resposta, ocorreu ou encerrado, e os riscos ativos devem ser os abertos e os em resposta. | PMBOK 7 §2.8.5.1, p. 124; regra do PMO (Q97) | alterado | Núcleo | 2 | teste |
| RN-IN-12 | A situação do risco deve seguir o fluxo: de aberto para em resposta, ocorreu ou encerrado; de em resposta para ocorreu ou encerrado; e de ocorreu para encerrado. | PMBOK 7 p. 124; o fluxo é regra do PMO (Q97, Q166b) | alterado | Núcleo | 2 | teste |
| RN-IN-13 | O sistema deve registrar a revisão "Identificação" ao cadastrar o risco e uma revisão quando a probabilidade, o impacto ou a situação mudam; a revisão feita pela pessoa deve atualizar a data de revisão. | PMBOK 7 p. 127 (Q103) | confirmado | Núcleo | 2 | teste |
| RN-IN-14 | A revisão atrasada deve ser a de um risco ativo cuja última revisão passou da cadência de revisão. | PMBOK 7 p. 127; a cadência é regra do PMO (Q95, Q103) | confirmado | Núcleo | 2 | teste |
| RN-IN-15 | Quando uma ameaça passa a ocorreu, o sistema deve abrir uma questão, uma única vez por risco, com prioridade alta, com o plano de contingência na descrição e com o responsável do risco ou, sem ele, o gerente do projeto. | PMBOK 7 §4.6.2, p. 185 (Q98, Q167) | alterado | Núcleo | 2 | teste |
| RN-IN-16 | Quando uma oportunidade passa a ocorreu, o sistema deve pedir o ganho obtido e oferecer o registro de uma lição aprendida, sem abrir questão. | PMBOK 7 §4.6.2, p. 185; §2.8.5.2 (Q98) | alterado | Núcleo | 2 | teste |
| RN-IN-17 | No nível rigoroso, o risco com pontuação igual ou acima do limite deve ter responsável e estratégia. | Regra do PMO (Q103) | confirmado | Núcleo | 2 | teste |
| RN-IN-18 | A reserva de contingência deve ser a soma das reservas em R$ e em dias das ameaças não encerradas, e continuar comprometida depois que o risco ocorre. | PMBOK 7 p. 62 e 127 (Q103, Q172a) | confirmado | Núcleo | 2 | teste |
| RN-IN-19 | O uso da contingência deve ser a reserva usada nas questões ligadas a riscos. | PMBOK 7 p. 127 (Q103, Q172a) | confirmado | Núcleo | 2 | teste |
| RN-IN-20 | Quando a contingência usada passa da reservada, o sistema deve mostrar um alerta alto. | Regra do PMO (Q162, Q172a) | confirmado | Núcleo | 3 | teste |
| RN-IN-21 | Quando a reserva de gerenciamento usada passa da disponível, o sistema deve mostrar um alerta alto; sem reserva definida, o primeiro uso já gera o alerta. | Regra do PMO (Q162) | confirmado | Incerteza avançada | 3 | teste |
| RN-IN-22 | Quando o risco geral do projeto é avaliado como alto, o sistema deve mostrar um alerta alto. | PMBOK 7 p. 123; Padrão p. 54 (Q160, Q172b) | confirmado | Núcleo | 3 | teste |
| RN-IN-23 | Quando o projeto não tem nenhum risco identificado, o sistema deve mostrar um alerta médio. | PMBOK 7 p. 122 (Q166c) | alterado | Núcleo | 3 | teste |
| RN-IN-24 | Quando uma ameaça ocorreu e não tem questão ligada, o sistema deve mostrar um alerta médio. | Regra do PMO (Q98, Q160) | alterado | Núcleo | 3 | teste |
| RN-IN-25 | Quando uma ameaça ativa de nível alto não tem estratégia, o sistema deve mostrar um alerta alto, citando a p. 125. | PMBOK 7 §2.8.5.2, p. 125 (Q161) | confirmado | Núcleo | 3 | teste |
| RN-IN-26 | Quando uma ameaça ativa de nível alto tem a estratégia aceitar e não tem plano de contingência, o sistema deve mostrar um alerta alto, explicando que aceitar é válido abaixo do limite. | PMBOK 7 p. 123 e 125 (Q161) | alterado | Núcleo | 3 | teste |
| RN-IN-27 | Quando uma oportunidade ativa de nível alto não tem estratégia, o sistema deve mostrar um alerta médio. | Regra do PMO (Q161) | confirmado | Núcleo | 3 | teste |
| RN-IN-28 | Quando um risco ativo não tem probabilidade e impacto avaliados, o sistema deve mostrar um alerta médio. | PMBOK 7 p. 122, 125 e 176 (Q166b) | alterado | Núcleo | 3 | teste |
| RN-IN-29 | Quando um risco ativo não tem responsável, o sistema deve mostrar um alerta médio. | PMBOK 7 p. 185 (Q166c, Q176) | alterado | Núcleo | 3 | teste |
| RN-IN-30 | Quando a revisão de um risco está atrasada, o sistema deve mostrar um alerta médio. | PMBOK 7 p. 127 (Q166c) | confirmado | Núcleo | 3 | teste |
| RN-IN-31 | Quando a reserva de contingência é menor que o EMV das ameaças, o sistema deve mostrar um alerta informativo. | PMBOK 7 p. 126–127; regra do PMO (Q162) | alterado | Incerteza avançada | 3 | teste |
| RN-IN-32 | O sistema deve permitir excluir somente o risco aberto, sem revisão além da identificação, sem questão ou item ligado e sem reserva usada. | Regra do PMO (Q99) | alterado | Núcleo | 2 | teste |
| RN-IN-33 | A outra incerteza deve ter natureza (geral, ambiguidade, complexidade ou volatilidade) e descrição; só valem as respostas da natureza escolhida; e a situação deve ser aberta, reduzida ou resolvida. | PMBOK 7 §2.8.1 a §2.8.4, p. 119–122 (Q103) | confirmado | Incerteza avançada | 3 | teste |
| RN-IN-35 | A estratégia escalar deve registrar a parte interessada a quem o risco foi escalado e a data. | PMBOK 7 §2.8.5.1, p. 123; Glossário (Risk Escalation) (Q100) | novo | Núcleo | 2 | teste |
| RN-IN-36 | A cadência de revisão dos riscos deve ser definida por projeto, de 1 a 365 dias, com 14 de padrão, e o sistema deve permitir mudá-la também depois da aprovação do termo, com registro no histórico. | PMBOK 7 §2.8.5.4, p. 127; os valores são regra do PMO (Q95, Q177) | alterado | Núcleo | 2 | teste |
| RN-IN-37 | Encerrar um risco deve exigir o motivo: não ocorreu, resposta eficaz ou deixou de existir. | PMBOK 7 §2.8.5.1, p. 124 (Q97) | novo | Núcleo | 2 | teste |
| RN-IN-38 | Reabrir um risco encerrado deve exigir justificativa. | Regra do PMO (Q97) | novo | Núcleo | 2 | teste |
| RN-IN-39 | Para passar a em resposta, o risco deve ter probabilidade, impacto, estratégia e responsável. | PMBOK 7 p. 122, 125 e 185 (Q166b) | novo | Núcleo | 2 | teste |
| RN-IN-40 | Para passar a em resposta, a ameaça acima do limite deve ter o risco residual e os riscos secundários, que aceitam "nenhum", em cada nível de exigência. | PMBOK 7 §2.8.5.2, p. 125 (Q101, Q173) | novo | Núcleo | 2 | teste |
| RN-IN-41 | O uso da reserva de gerenciamento deve ser a reserva usada nas questões sem risco ligado. | PMBOK 7 p. 127 (Q103, Q172a) | confirmado | Incerteza avançada | 3 | teste |
| RN-IN-42 | Quando uma oportunidade ocorreu sem o ganho registrado, o sistema deve mostrar um alerta informativo. | Regra do PMO (Q160) | novo | Núcleo | 3 | teste |
| RN-IN-43 | Quando o orçamento não tem reserva de contingência e há ameaça ativa, o sistema deve mostrar um alerta médio. | PMBOK 7 §2.4.2.4, p. 62; §2.8.5.3, p. 127 (Q172a) | novo | Núcleo | 3 | teste |
| RN-IN-44 | A tela de riscos deve mostrar o limite de variação do projeto como referência para a nota de impacto. | PMBOK 7 §2.8.5, p. 122 (Q95) | novo | Núcleo | 2 | teste |

A regra IN-34 do protótipo, o pré-mortem, saiu (Q102), junto com a RF-MT-06. O código dela não é reaproveitado (Q217).

---

#### Princípios, aquisições, métodos, guia e encerramento (parte 3)

As seções 3.2.13 a 3.2.17 seguem as mesmas regras de acesso, de exclusão e de módulo da abertura da parte 2.

#### 3.2.13 Princípios (PR)

Premissas e restrições, no núcleo; business case, conformidade, registro de decisões e mudança organizacional, no módulo Business case e governança; autoavaliação dos 12 princípios, no módulo Princípios e resultados (Q31). Os princípios mostram o título original em inglês (Q144).

**Entradas**

| Entrada | Onde | Tipo | Obrigatória | Valores válidos | Origem |
|---|---|---|---|---|---|
| Investimento | business case, no módulo | número | sim, para calcular | maior que 0 (RN-PR-01) | Q138 |
| Benefício anual e custo anual | business case, no módulo | número | o benefício, para calcular | maiores ou iguais a 0 | Q138 |
| Horizonte | business case, no módulo | número inteiro de anos | sim, para calcular | de 1 a 50 | Q138 |
| Taxa de desconto | business case, no módulo | número, em % | não | maior ou igual a 0 | Q138 |
| Benefícios não financeiros | business case, no módulo | texto | não | até 20.000 caracteres | Q181 |
| "Revisei, sem mudanças" | business case, no módulo | marca | não | — | Q139 |
| Área da conformidade | conformidade, no módulo | escolha | sim | legal, privacidade, segurança, financeira, ética, pessoas, ambiental ou social (RN-PR-07) | Q144 |
| Requisito, prazo e evidência da conformidade | conformidade, no módulo | texto e data | o requisito; a evidência, para atendido (RN-PR-09) | até 20.000 caracteres | Q144 |
| Responsável pela conformidade | conformidade, no módulo | escolha | não | um membro da equipe (RN-PR-24) | Q176 |
| Situação da conformidade | conformidade, no módulo | escolha | sim | pendente, em andamento, atendido ou não se aplica; padrão pendente (RN-PR-08) | Q144 |
| Grupo afetado | mudança organizacional, no módulo | texto | sim | até 20.000 caracteres | Q144 |
| Impacto e capacidade de absorção | mudança organizacional, no módulo | número inteiro | não | de 1 a 5 (RN-PR-11) | Q140 |
| Meta de adoção | mudança organizacional, no módulo | número, em % | não | de 0 a 100 | Q144 |
| Situação do grupo | mudança organizacional, no módulo | escolha | sim | não iniciado, preparando, em transição ou adotado; padrão não iniciado | Q140 |
| Adoção medida e data | medição de adoção, no módulo | número e data | a adoção | adoção de 0 a 100%; data até hoje (RN-PR-12) | Q144 |
| Título, data e "revisar em" da decisão | registro de decisões, no módulo | texto e datas | o título | data até hoje (RN-PR-15) | Q142 |
| Decidido por | registro de decisões, no módulo | escolha | não | uma parte interessada ativa ou um membro da equipe (RN-PR-26) | Q142 |
| Tipo e descrição | premissas e restrições | escolha e texto | sim | premissa ou restrição (RN-PR-27) | Q141 |
| Situação e "validar até" da premissa | premissas e restrições | escolha e data | a situação | não validada, validada ou invalidada; padrão não validada (RN-PR-16) | Q141 |
| Situação e reflexão de cada princípio | autoavaliação, no módulo | escolha e texto | a reflexão, para atendido ou parcial (RN-PR-21) | não avaliado, atendido, parcial ou não atendido (Q224) | Q143 |

**Funções**

| Código | Requisito | Regras | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|---|
| RF-PR-01 | O sistema deve permitir a autoavaliação dos 12 princípios pela equipe, com a situação e a reflexão de cada um, e mostrar os sinais no projeto calculados dos dados. | RN-PR-18, RN-PR-21 | Q143, Q144 | alterado | Princípios e resultados | 3 | teste |
| RF-PR-02 | O sistema deve permitir registrar o business case e mostrar o VPL, o ROI, a razão benefício-custo, o payback e o gráfico. | RN-PR-01 a RN-PR-06, RN-PR-22, RN-PR-23 | Q138, Q139, Q181, Q182 | alterado | Business case e governança | 3 | teste |
| RF-PR-03 | O sistema deve permitir registrar os requisitos de conformidade e de sustentabilidade. | RN-PR-07 a RN-PR-10, RN-PR-24 | Q144, Q176 | alterado | Business case e governança | 3 | teste |
| RF-PR-04 | O sistema deve permitir registrar a mudança organizacional: os grupos afetados, a situação de cada um e as medições de adoção. | RN-PR-11 a RN-PR-14, RN-PR-25 | Q140, Q144 | alterado | Business case e governança | 3 | teste |
| RF-PR-05 | O sistema deve permitir registrar e excluir decisões no registro de decisões. | RN-PR-15, RN-PR-26, RN-DA-31 | Q142, Q198 | alterado | Business case e governança | 3 | teste |
| RF-PR-06 | O sistema deve permitir registrar as premissas e as restrições do projeto e mostrar, como referência, as escritas no termo de abertura. | RN-PR-16, RN-PR-17, RN-PR-27 a RN-PR-29 | Q141, Q142, Q198 | alterado | Núcleo | 2 | teste |

**Regras de negócio**

| Código | Regra | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RN-PR-01 | O business case deve ser calculado somente com investimento maior que 0, benefício anual informado, horizonte de 1 a 50 anos e taxa maior ou igual a 0%. | Regra do PMO (Q138) | confirmado | Business case e governança | 3 | teste |
| RN-PR-02 | A data de revisão do business case deve mudar quando o conteúdo muda ou quando a pessoa marca "revisei, sem mudanças". | PMBOK 7 §4.6.1, p. 184; Padrão §3.4, p. 35 (Q139) | alterado | Business case e governança | 3 | teste |
| RN-PR-04 | Quando a razão benefício-custo fica abaixo de 1,0 e não há benefícios não financeiros registrados, o sistema deve mostrar um alerta alto, com a leitura do PMBOK 7. | PMBOK 7 §2.7.2.5, p. 102; Glossário (Business Case), p. 236 (Q181) | alterado | Business case e governança | 3 | teste |
| RN-PR-05 | Quando o custo previsto passa do investimento do business case em mais que o limite de variação, o sistema deve mostrar um alerta alto, pedindo para reavaliar o valor ou atualizar o business case. | PMBOK 7 §2.7.5, p. 113; Padrão §3.4, p. 35 (Q182) | alterado | Business case e governança | 3 | teste |
| RN-PR-06 | Quando o business case já salvo está há mais de 90 dias sem revisão, o sistema deve mostrar um alerta informativo. | Padrão p. 35; os 90 dias são regra do PMO (Q185) | confirmado | Business case e governança | 3 | teste |
| RN-PR-07 | O requisito de conformidade deve ter a área (legal, privacidade, segurança, financeira, ética, pessoas, ambiental ou social) e o texto do requisito; a área segurança deve explicar os dois sentidos, da informação (security) e das pessoas (safety). | Padrão §3.1, p. 24–27; "segurança" é regra do PMO (Q144) | confirmado | Business case e governança | 3 | teste |
| RN-PR-08 | A situação da conformidade deve ser pendente, em andamento, atendido ou não se aplica, com pendente como padrão. | Regra do PMO (Q144) | confirmado | Business case e governança | 3 | teste |
| RN-PR-09 | Para marcar a conformidade como atendida, a evidência deve estar registrada. | Regra do PMO (Q92, Q144) | confirmado | Business case e governança | 3 | teste |
| RN-PR-10 | Quando um requisito de conformidade pendente ou em andamento passa do prazo, o sistema deve mostrar um alerta alto. | Padrão §3.1, p. 24–27; o prazo é regra do PMO (Q185) | confirmado | Business case e governança | 3 | teste |
| RN-PR-11 | O grupo afetado pela mudança organizacional deve ter nome; o impacto e a capacidade de absorção devem ir de 1 (baixa) a 5 (alta); e a meta de adoção, até 100%. | Padrão §3.12, p. 58–59; a escala é regra do PMO (Q140, Q144) | alterado | Business case e governança | 3 | teste |
| RN-PR-12 | A medição de adoção deve ter a adoção, de 0 a 100%, e a data até a de hoje; a capacidade de absorção informada na medição deve atualizar a do grupo. | Regra do PMO (Q140, Q144) | alterado | Business case e governança | 3 | teste |
| RN-PR-13 | Quando um grupo tem impacto 4 ou 5 e capacidade de absorção 2 ou menos, o sistema deve mostrar um alerta médio; sem capacidade informada, ela conta como 5. | Padrão §3.12, p. 58–59; os cortes são regra do PMO (Q140, Q185) | alterado | Business case e governança | 3 | teste |
| RN-PR-14 | Quando 4 ou mais grupos estão preparando ou em transição ao mesmo tempo, o sistema deve mostrar um alerta informativo de saturação de mudanças. | Padrão p. 59; o número 4 é regra do PMO (Q185) | confirmado | Business case e governança | 3 | teste |
| RN-PR-15 | A decisão deve ter título e data até a de hoje; com "revisar em" preenchido e vencido, a tela deve mostrá-la como a revisar. | Regra do PMO (Q142) | alterado | Business case e governança | 3 | teste |
| RN-PR-16 | A situação da premissa deve ser não validada, validada ou invalidada, com não validada como padrão, e só a premissa tem situação. | PMBOK 7 p. 185; Padrão p. 39 (Q141) | alterado | Núcleo | 2 | teste |
| RN-PR-17 | Quando uma premissa não validada passa da data de "validar até", o sistema deve mostrar um alerta médio. | PMBOK 7 p. 185 (Q141, Q185) | alterado | Núcleo | 3 | teste |
| RN-PR-18 | A autoavaliação deve mostrar, para cada princípio, os sinais no projeto calculados dos dados, só como informação, sem nível e sem alerta, com os sinais refeitos pelas decisões: o acordo de trabalho com 3 seções, a estratégia de engajamento de cada parte que não apoia, o contato dentro da frequência do plano, as perguntas de tailoring contadas sobre 17, a capacidade de absorção e a justificativa da abordagem. | Padrão §3, p. 21; os limiares são regra do PMO (Q143) | alterado | Princípios e resultados | 3 | teste |
| RN-PR-21 | Marcar um princípio como atendido ou parcial deve exigir a reflexão da equipe em texto. | Padrão §3, p. 21 (Q92, Q143) | alterado | Princípios e resultados | 3 | teste |
| RN-PR-22 | O business case deve calcular o ROI como (benefício anual − custo anual) ÷ investimento, a razão benefício-custo como o valor presente dos benefícios ÷ o valor presente dos custos, o VPL e o payback simples. | PMBOK 7 §2.7.2.5, p. 102; §4.4.1, p. 175 (Q138) | alterado | Business case e governança | 3 | teste |
| RN-PR-23 | Com benefícios não financeiros registrados, a tela do business case deve mostrar a leitura do PMBOK 7 sobre a razão benefício-custo abaixo de 1,0, sem alerta. | PMBOK 7 §2.7.2.5, p. 102 (Q181) | novo | Business case e governança | 3 | teste |
| RN-PR-24 | O responsável pelo requisito de conformidade deve ser escolhido entre os membros da equipe. | PMBOK 7 p. 185 (Q55, Q176) | novo | Business case e governança | 3 | teste |
| RN-PR-25 | Ao marcar o grupo como adotado, a tela deve lembrar que o PMBOK 7 pede reforço e que as medições de adoção mostram se o grupo volta ao estado anterior. | Padrão §3.12, p. 58–59; §4.2.4.1, p. 161 (Q140) | novo | Business case e governança | 3 | teste |
| RN-PR-26 | O "decidido por" deve ser escolhido entre as partes interessadas ativas e os membros da equipe. | PMBOK 7 §4.6.2, p. 185–186 (Q142) | novo | Business case e governança | 3 | teste |
| RN-PR-27 | O registro de premissas e restrições deve ter o tipo, premissa ou restrição, e a descrição. | PMBOK 7 §4.6.2, p. 185; Glossário (Assumption Log) (Q141) | alterado | Núcleo | 2 | teste |
| RN-PR-28 | Ao invalidar uma premissa, o sistema deve avisar para avaliar se ela vira risco, questão ou mudança, sem criar nenhum deles. | PMBOK 7 p. 185; Padrão §3.5, p. 39 (Q141) | confirmado | Núcleo | 2 | teste |
| RN-PR-29 | A tela de premissas e restrições deve mostrar, como referência, as premissas e as restrições escritas no termo de abertura. | PMBOK 7 §4.6.2, p. 185 (Q141) | novo | Núcleo | 2 | teste |

As regras PR-19 e PR-20 do protótipo, o nível calculado dos princípios e o alerta de princípios fracos, saíram (Q143). A TIR fica de fora do business case por ora (Q138).

#### 3.2.14 Aquisições e recursos físicos (AQ)

Aquisições, fornecedores e recursos físicos, no módulo Aquisições e recursos físicos (Q31). O fornecedor contratado entra sozinho na lista de partes interessadas (Q147).

**Entradas**

| Entrada | Onde | Tipo | Obrigatória | Valores válidos | Origem |
|---|---|---|---|---|---|
| Item da aquisição | registrar e editar aquisição | texto | sim | até 20.000 caracteres | Q148 |
| Fazer ou comprar | registrar e editar aquisição | escolha | sim | comprar ou fazer; padrão comprar (RN-AQ-01) | Q148 |
| Situação da aquisição | editar aquisição | escolha | sim | planejada, em licitação ou cotação, contratada, entregue, encerrada ou cancelada (RN-AQ-17) | Q145 |
| Documento de licitação e tipo de contrato | registrar e editar aquisição | escolha | não | nenhum, RFI, RFP ou RFQ; preço fixo, custo reembolsável, tempo e material, IDIQ ou outro (RN-AQ-02) | Q148 |
| Valor | registrar e editar aquisição | número | não | maior ou igual a 0 (RN-AQ-05) | Q148 |
| Fornecedor | registrar e editar aquisição | escolha | para contratada, entregue e encerrada na compra (RN-AQ-03) | uma parte interessada do projeto | Q147 |
| Concorrentes da licitação | registrar e editar aquisição | texto | não | até 20.000 caracteres | Q147 |
| Critérios de seleção | registrar e editar aquisição | texto | para passar de em licitação a contratada (RN-AQ-18) | até 20.000 caracteres | Q175 |
| Datas de necessidade e de entrega prevista e prometida | registrar e editar aquisição | data | não | datas válidas | Q185 |
| Nota do fornecedor | encerrar compra | número inteiro | sim, para encerrar a compra (RN-AQ-04) | de 1 a 5 | Q146 |
| Motivo do cancelamento | cancelar aquisição | texto | sim (RN-AQ-22) | até 20.000 caracteres | Q145 |
| Nome do recurso físico | registrar e editar recurso | texto | sim | até 20.000 caracteres | Q148 |
| Tipo do recurso | registrar e editar recurso | escolha | sim | material, equipamento, software, ambiente ou outro; padrão equipamento (RN-AQ-12) | Q148 |
| Situação do recurso | registrar e editar recurso | escolha | sim | planejado, pedido, recebido, em uso, devolvido ou descartado; padrão planejado | Q148 |
| Antecedência | registrar e editar recurso | número inteiro de dias | não | de 0 a 730 | Q148 |
| Quantidade, uso e desperdício | registrar e editar recurso | número | não | maiores ou iguais a 0; desperdício até o uso (RN-AQ-13) | Q148 |

**Funções**

| Código | Requisito | Regras | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|---|
| RF-AQ-01 | O sistema deve mostrar o painel de compras e recursos, com as aquisições, os recursos físicos e os alertas do domínio. | RN-AQ-07 a RN-AQ-10, RN-AQ-14 a RN-AQ-16, RN-AQ-23, RN-AQ-25 | Q145 a Q148, Q175, Q185 | alterado | Aquisições e recursos físicos | 3 | teste |
| RF-AQ-02 | O sistema deve permitir registrar e editar uma aquisição. | RN-AQ-01 a RN-AQ-05, RN-AQ-17 a RN-AQ-21 | Q145 a Q148, Q175 | alterado | Aquisições e recursos físicos | 3 | teste |
| RF-AQ-03 | O sistema deve permitir excluir uma aquisição cadastrada por engano. | RN-AQ-06, RN-DA-31 | Q145, Q198 | alterado | Aquisições e recursos físicos | 3 | teste |
| RF-AQ-05 | O sistema deve permitir registrar e editar um recurso físico. | RN-AQ-12 a RN-AQ-14 | Q148 | alterado | Aquisições e recursos físicos | 3 | teste |
| RF-AQ-06 | O sistema deve permitir excluir um recurso físico ainda planejado. | RN-AQ-24, RN-DA-31 | Q148, Q198 | alterado | Aquisições e recursos físicos | 3 | teste |
| RF-AQ-07 | O sistema deve permitir cancelar uma aquisição, com motivo. | RN-AQ-22 | Q145 | novo | Aquisições e recursos físicos | 3 | teste |

**Regras de negócio**

| Código | Regra | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RN-AQ-01 | A aquisição deve ter o item e a decisão de fazer ou comprar, com comprar como padrão; as aquisições ativas são as planejadas, em licitação ou cotação e contratadas. | PMBOK 7 p. 65 e 74–76 (Q145, Q148) | alterado | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-02 | O documento de licitação deve ser nenhum, RFI, RFP ou RFQ, e o contrato, preço fixo, custo reembolsável, tempo e material, IDIQ ou outro. | PMBOK 7 p. 75; §4.6.8, p. 191 (Q148) | confirmado | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-03 | A compra contratada, entregue ou encerrada deve ter o fornecedor, escolhido entre as partes interessadas. | PMBOK 7 p. 75–76 (Q147) | alterado | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-04 | Encerrar uma compra deve exigir a nota do fornecedor, de 1 a 5, e a tela deve mostrar os critérios de seleção registrados. | PMBOK 7 §2.5.6.1, p. 75; p. 76; Tabela 2-7, p. 79; a escala é regra do PMO (Q146) | alterado | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-05 | O valor da aquisição deve ser maior ou igual a 0. | Regra do PMO (Q148) | confirmado | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-06 | O sistema deve permitir excluir somente a aquisição planejada, sem contrato e sem vínculo. | Regra do PMO (Q145) | alterado | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-07 | Quando uma compra planejada ou em licitação é necessária em até 30 dias e ainda não foi contratada, o sistema deve mostrar um alerta médio. | PMBOK 7 p. 65; os 30 dias são regra do PMO (Q185) | confirmado | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-08 | Quando uma aquisição contratada passa da entrega prevista, o sistema deve mostrar um alerta alto. | PMBOK 7 p. 76 (Q185) | confirmado | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-09 | Quando a entrega prometida pelo fornecedor é depois da data de necessidade do projeto e a aquisição não está entregue, encerrada ou cancelada, o sistema deve mostrar um alerta alto. | PMBOK 7 p. 65 e 76 (Q185) | confirmado | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-10 | Quando o fornecedor de uma aquisição contratada ou entregue tem nota 2 ou menos, o sistema deve mostrar um alerta médio. | Regra do PMO (Q146, Q185) | alterado | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-12 | O recurso físico deve ter nome, o tipo material, equipamento, software, ambiente ou outro, com equipamento como padrão, e antecedência de 0 a 730 dias. | PMBOK 7 p. 65; nome e antecedência são regra do PMO (Q148) | alterado | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-13 | O desperdício deve ser no máximo o total usado, e a quantidade e o uso devem ser maiores ou iguais a 0. | PMBOK 7 p. 74; Tabela 2-7, p. 79; os limites são regra do PMO (Q148) | confirmado | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-14 | A data para pedir o recurso deve ser a data de necessidade menos a antecedência. | PMBOK 7 p. 65 (Q148) | confirmado | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-15 | Quando o uso de um recurso passa da quantidade planejada, o sistema deve mostrar um alerta médio. | PMBOK 7 p. 74; Tabela 2-7, p. 79 (Q185) | confirmado | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-16 | O percentual de desperdício deve ser o desperdício dividido pelo uso, e a partir de 15% o sistema deve mostrar um alerta informativo. | PMBOK 7 p. 74; os 15% são regra do PMO (Q185) | confirmado | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-17 | A situação da compra deve seguir o fluxo planejada, em licitação ou cotação, contratada, entregue e encerrada, com a passagem direta de planejada a contratada quando não há licitação; a decisão de fazer segue planejada, entregue e encerrada. | PMBOK 7 §2.4.5 e §2.4.6, p. 65; §2.5.6, p. 74–76 (Q145) | novo | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-18 | Passar de em licitação ou cotação a contratada deve exigir os critérios de seleção registrados; a contratação direta, sem licitação, não exige. | PMBOK 7 §2.5.6.1, p. 75 (Q175) | novo | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-19 | Quando o fornecedor escolhido ainda não é parte interessada, o sistema deve incluí-lo na lista, com a categoria fornecedor, externo e ativo. | PMBOK 7 §2.5.6.2, p. 76 (Q147) | novo | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-20 | Ao marcar a compra como contratada, a tela deve lembrar de atualizar o cronograma, os custos, a qualidade e os riscos. | PMBOK 7 §2.5.6.2, p. 76 (Q147) | novo | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-21 | Durante a licitação, os concorrentes devem ficar em texto livre, fora da lista de partes interessadas. | Regra do PMO (Q147) | novo | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-22 | Cancelar uma aquisição planejada, em licitação ou contratada deve exigir motivo. | Regra do PMO (Q145) | novo | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-23 | Quando a data de necessidade de uma compra planejada ou em licitação já passou e ela não foi contratada, o sistema deve mostrar um alerta alto. | PMBOK 7 p. 65 (Q185) | confirmado | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-24 | O sistema deve permitir excluir o recurso físico somente enquanto ele está planejado; depois do pedido, ele termina como devolvido ou descartado. | Regra do PMO (Q148) | novo | Aquisições e recursos físicos | 3 | teste |
| RN-AQ-25 | Quando um recurso planejado passa da data para pedir, o sistema deve mostrar um alerta alto; faltando até 7 dias, um alerta médio. | PMBOK 7 p. 65; os 7 dias são regra do PMO (Q185) | confirmado | Aquisições e recursos físicos | 3 | teste |

A função RF-AQ-04, o botão que cadastrava o fornecedor como parte interessada, e a regra AQ-11 do protótipo, o alerta dela, saíram (Q147).

#### 3.2.15 Métodos (MT)

Telas de métodos que usam regras de outros domínios: MoSCoW, dependências e Gantt, no núcleo; burndown, no módulo Medição avançada; Cynefin e Stacey, no módulo Incerteza avançada (Q31). O domínio não tem regras próprias: as regras estão em Planejamento (RN-PL-19, RN-PL-20), Entrega, Medição (RN-ME-17) e Abordagem (RN-AB-06, RN-AB-07).

**Entradas**

| Entrada | Onde | Tipo | Obrigatória | Valores válidos | Origem |
|---|---|---|---|---|---|
| Item de que depende | dependências | escolha | não | outro item do mesmo projeto, sem formar ciclo (RN-PL-19) | Q67 |
| Incerteza dos requisitos e incerteza da tecnologia | Stacey, no módulo | número inteiro | não | de 1 (pouca) a 5 (muita) (RN-AB-06) | Q126 |
| Contexto do Cynefin | Cynefin, no módulo | escolha | não | óbvio, complicado, complexo, caótico ou desordenado (RN-AB-07) | Q125 |

**Funções**

| Código | Requisito | Regras | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|---|
| RF-MT-01 | O sistema deve permitir classificar cada item pela técnica MoSCoW. | RN-EN-04 | Protótipo (Q209) | confirmado | Núcleo | 2 | teste |
| RF-MT-02 | O sistema deve permitir registrar as dependências entre os itens. | RN-PL-19 | Protótipo (Q209) | confirmado | Núcleo | 2 | teste |
| RF-MT-03 | O sistema deve mostrar o gráfico de Gantt dos itens com datas, com as dependências e os conflitos marcados. | RN-PL-20, RN-EN-07, RN-EN-15, RN-EN-16 | Q67, Q80, Q158 | alterado | Núcleo | 2 | teste |
| RF-MT-04 | O sistema deve mostrar o burndown da iteração. | RN-EN-07, RN-EN-15, RN-ME-17 | Q80 | alterado | Medição avançada | 3 | teste |
| RF-MT-05 | O sistema deve permitir classificar o projeto pela matriz de Stacey e pelo Cynefin. | RN-AB-06, RN-AB-07 | Q125, Q126 | alterado | Incerteza avançada | 3 | teste |

A função RF-MT-06, o pré-mortem, saiu (Q102).

#### 3.2.16 Guia e ensino (GU)

Guia das etapas, glossário, ajuda das telas, dicas, exemplo preenchido, projeto de exemplo, pronto para revisão, página sobre o PMBOK 7 e sugestões de tailoring, no núcleo (Q31). Os textos de ensino seguem o GLOSSARY e as decisões, e só dizem o que o PMBOK 7 diz, com a página (Q151).

**Entradas**

| Entrada | Onde | Tipo | Obrigatória | Valores válidos | Origem |
|---|---|---|---|---|---|
| Dicas | preferências da conta | ligadas ou desligadas | sim | padrão ligadas (RN-GU-13) | Q202 |
| Modo do menu | preferências da conta | escolha | sim | essencial ou completo; padrão essencial (RN-GU-13) | Q202 |

**Funções**

| Código | Requisito | Regras | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|---|
| RF-GU-01 | O sistema deve mostrar o guia do projeto, com as etapas nos cinco grupos de processos e o próximo passo. | RN-GU-01 a RN-GU-05, RN-GU-09 a RN-GU-12 | Q149, Q150, Q169b, Q169c, Q169d, Q174a | alterado | Núcleo | 2 | teste |
| RF-GU-02 | O sistema deve mostrar o glossário, com os termos e as definições do GLOSSARY, em linguagem simples, com o original em inglês e a página do PMBOK 7. | RN-GU-07 | Q113, Q151 | alterado | Núcleo | 2 | inspeção |
| RF-GU-03 | O sistema deve mostrar em cada tela a faixa "Para que serve / O que fazer", com o texto alinhado às decisões. | RN-GU-07 | Q151 | alterado | Núcleo | 2 | inspeção |
| RF-GU-04 | O sistema deve mostrar as dicas de cada campo e permitir ligá-las e desligá-las na conta da pessoa. | RN-GU-13 | Q202 | alterado | Núcleo | 2 | teste |
| RF-GU-05 | O sistema deve mostrar, em cada tela de registro, o exemplo preenchido. | — | Protótipo (Q209) | confirmado | Núcleo | 2 | teste |
| RF-GU-06 | O sistema deve permitir abrir o projeto de exemplo. | RN-GU-06, RN-PM-10 | Q53, Q151 | alterado | App | 1 | teste |
| RF-GU-07 | O sistema deve mostrar em cada registro se ele está pronto para revisão ou o que falta. | RN-PM-15, RN-PM-41 | Q56 | alterado | Núcleo | 2 | teste |
| RF-GU-08 | O sistema deve mostrar a página "Sobre o PMBOK 7", com o texto alinhado às decisões. | RN-GU-07 | Q151 | alterado | Núcleo | 2 | inspeção |
| RF-GU-09 | O sistema deve permitir escolher, na conta da pessoa, o menu no modo essencial ou no modo completo. | RN-GU-13, RN-GU-14 | Q57, Q202 | alterado | Núcleo | 2 | teste |
| RF-GU-10 | O sistema deve mostrar, nas telas, as sugestões de tailoring da abordagem do projeto. | RN-GU-08 | Q151, Q152 | alterado | Núcleo | 2 | inspeção |

**Regras de negócio**

| Código | Regra | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RN-GU-01 | O guia deve organizar as etapas nos cinco grupos de processos, com o original em inglês: Iniciação (Initiating), com abordagem, termo aprovado e partes; Planejamento (Planning), com equipe, escopo, riscos, prazo e orçamento e compras, opcional; Execução (Executing), com quadro, engajar as pessoas e questões e mudanças, opcional; Monitoramento e controle (Monitoring and Controlling), com acompanhamento, checklist dos domínios e princípios; e Encerramento (Closing), com lições e encerramento; e a tela deve dizer que os grupos não são fases e se repetem em cada fase. | PMBOK 7 §4.2.7.4, p. 170–171; a lista de etapas é regra do PMO (Q149) | alterado | Núcleo | 2 | teste |
| RN-GU-02 | A etapa da Iniciação deve contar como feita só com o termo de abertura aprovado. | Regra do PMO (Q152) | confirmado | Núcleo | 2 | teste |
| RN-GU-03 | A etapa "Prazo e orçamento" deve contar como feita com uma iteração, ou com itens ou fases com datas. | PMBOK 7 §2.4.2.3, p. 58–61 (Q150) | alterado | Núcleo | 2 | teste |
| RN-GU-04 | O próximo passo deve ser a primeira etapa obrigatória ainda não feita, e o grupo deve contar como completo quando as etapas obrigatórias dele estão feitas. | Regra do PMO (Q152) | confirmado | Núcleo | 2 | teste |
| RN-GU-05 | Os painéis completos da visão geral devem aparecer quando a Iniciação tem abordagem, propósito, objetivos e pelo menos uma parte interessada. | Regra do PMO (Q149, Q152) | confirmado | Núcleo | 2 | teste |
| RN-GU-06 | O projeto novo deve abrir direto no guia, e o projeto de exemplo deve ser reaproveitado quando já existe. | Regra do PMO (Q53, Q152) | confirmado | Núcleo | 2 | teste |
| RN-GU-07 | O glossário, a ajuda das telas e a página sobre o PMBOK 7 devem ser textos de ensino, sem efeito nos dados, com os termos do GLOSSARY e o texto alinhado às decisões. | GLOSSARY.md (Q151) | alterado | Núcleo | 2 | inspeção |
| RN-GU-08 | As sugestões de tailoring devem dizer só o que o PMBOK 7 diz, com a página: incerteza conforme a abordagem (p. 128), monitoramento por revisões (p. 14), trabalho novo no backlog (p. 76), escopo por EAP ou por épicos, funcionalidades e histórias (p. 84), cronograma (p. 58–61) e medição (p. 104); as sugestões de abertura são reescritas. | PMBOK 7 p. 14, 58–61, 76, 84, 104 e 128 (Q151, Q152) | alterado | Núcleo | 2 | inspeção |
| RN-GU-09 | A etapa "Engajar as pessoas" deve contar como feita com pelo menos uma parte ativa com plano de comunicação completo. | PMBOK 7 Figura 2-3, p. 10; p. 186 (Q169b) | novo | Núcleo | 2 | teste |
| RN-GU-10 | A etapa "Equipe" deve contar como feita com pelo menos uma linha completa na matriz RACI, com um A e pelo menos um R, e ter o texto "Quem faz o trabalho e quem responde por cada atividade ou entrega". | PMBOK 7 §2.2.1.3, p. 18; p. 189 (Q169c) | novo | Núcleo | 2 | teste |
| RN-GU-11 | A etapa "Riscos" deve contar como feita com pelo menos um risco com probabilidade e impacto avaliados. | PMBOK 7 p. 176; Figura 2-33, p. 124 (Q169d) | novo | Núcleo | 2 | teste |
| RN-GU-12 | As etapas de um módulo opcional desligado não devem aparecer no guia. | Regra do PMO (Q174a) | novo | Núcleo | 2 | teste |
| RN-GU-13 | As preferências de dicas e de modo do menu devem ficar na conta da pessoa, com as dicas ligadas e o modo essencial como padrão. | Regra do PMO (Q202) | alterado | Núcleo | 2 | teste |
| RN-GU-14 | O modo essencial deve só esconder telas do menu, sem mudar o acesso a elas. | Regra do PMO (Q57, Q202) | alterado | Núcleo | 2 | teste |

#### 3.2.17 Encerramento (EC)

Checklist, avaliação final, aceite final e o encerramento, o cancelamento e a reabertura do projeto, no núcleo (Q31). O gerente prepara o encerramento, que passa por revisão obrigatória; o aceite final é registrado; e só o supervisor encerra, cancela ou reabre (Q29, Q63).

**Entradas**

| Entrada | Onde | Tipo | Obrigatória | Valores válidos | Origem |
|---|---|---|---|---|---|
| Avaliação dos objetivos e benefícios em relação ao termo | avaliação final | texto | sim, para encerrar ou cancelar (RN-EC-05) | até 20.000 caracteres | Q64 |
| Itens do checklist manual | encerramento | marcas | não | os itens da RN-EC-03 | Q64, Q174a |
| Justificativa do encerramento com pendências | encerrar | texto | com pendência no checklist (RN-EC-07) | até 20.000 caracteres | Q64 |
| Justificativa do cancelamento e da reabertura | cancelar e reabrir | texto | sim (RN-EC-06, RN-EC-09) | até 20.000 caracteres | Q29, Q65 |
| Quem deu o aceite final | aceite final | escolha | sim, para encerrar | uma parte interessada do projeto: patrocinador, dono do produto ou cliente (RN-EC-14) | Q63, Q109 |
| Data do aceite final | aceite final | data | sim, para encerrar | até a data de hoje (Q224) | Q63 |

**Funções**

| Código | Requisito | Regras | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|---|
| RF-EC-01 | O sistema deve mostrar o encerramento do projeto: o checklist automático, o checklist manual, a comparação com o planejado e os objetivos do termo. | RN-EC-02 a RN-EC-04, RN-EC-11 | Q64, Q65, Q112, Q174a | alterado | Núcleo | 1 | teste |
| RF-EC-02 | O sistema deve permitir registrar a avaliação final do projeto. | RN-EC-05 | Q64, Q65 | alterado | Núcleo | 1 | teste |
| RF-EC-03 | O sistema deve permitir que um supervisor encerre o projeto em andamento. | RN-EC-05, RN-EC-07, RN-EC-08, RN-EC-12, RN-EC-13, RN-EC-15 | Q29, Q63, Q64, Q65 | alterado | Núcleo | 1 | teste |
| RF-EC-04 | O sistema deve permitir que um supervisor cancele o projeto em andamento, com justificativa. | RN-EC-05, RN-EC-06, RN-EC-08, RN-EC-12 | Q29, Q63, Q64 | alterado | Núcleo | 1 | teste |
| RF-EC-05 | O sistema deve permitir que um supervisor reabra o projeto encerrado ou cancelado, com justificativa. | RN-EC-09 | Q29, Q65 | alterado | Núcleo | 1 | teste |
| RF-EC-06 | O sistema deve manter o projeto encerrado ou cancelado só para consulta, inclusive a tela de encerramento. | RN-EC-10, RN-PM-23 | Q65 | alterado | Núcleo | 1 | teste |
| RF-EC-07 | O sistema deve permitir registrar o aceite final, com quem aceitou e a data. | RN-EC-14 | Q63, Q109 | novo | Núcleo | 1 | teste |

**Regras de negócio**

| Código | Regra | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RN-EC-01 | A situação do projeto deve ser em andamento, que é o padrão, encerrado ou cancelado. | PMBOK 7 p. 123; regra do PMO (Q112) | confirmado | Núcleo | 1 | teste |
| RN-EC-02 | O checklist automático deve conferir: entregas aceitas ou canceladas; mudanças rejeitadas ou implementadas; questões resolvidas; riscos encerrados; nenhum benefício só planejado; pelo menos uma lição; fases concluídas, exceto a fase chamada Encerramento; aquisições fora das ativas; conformidade sem pendente nem em andamento; grupos de mudança organizacional adotados; e nenhum membro ativo. | PMBOK 7 §2.3.5 e §4.6; regra do PMO (Q72, Q80, Q97, Q112) | alterado | Núcleo | 1 | teste |
| RN-EC-03 | O checklist manual deve ter 4 itens: contratos encerrados, conhecimento arquivado, transição para a operação e termo e business case revisados; o item de um módulo desligado não aparece, e, sem o módulo do business case, o último item fica "termo revisado". | PMBOK 7 p. 47; Padrão p. 14; p. 42, 77–78 e 180; "contratos encerrados" é regra do PMO (Q64, Q174a) | alterado | Núcleo | 2 | teste |
| RN-EC-04 | O encerramento deve comparar o escopo total com o aceito, o orçamento no término com o custo real e mostrar o fim planejado. | PMBOK 7 p. 47 (Q64, Q112) | confirmado | Núcleo | 1 | teste |
| RN-EC-05 | Encerrar ou cancelar deve exigir a avaliação dos objetivos e dos benefícios em relação ao termo de abertura. | PMBOK 7 p. 47 (Q64) | confirmado | Núcleo | 1 | teste |
| RN-EC-06 | Cancelar deve exigir justificativa. | Regra do PMO (Q64) | confirmado | Núcleo | 1 | teste |
| RN-EC-07 | Encerrar com pendência no checklist automático ou manual deve exigir justificativa. | Regra do PMO (Q64) | confirmado | Núcleo | 1 | teste |
| RN-EC-08 | Ao encerrar ou cancelar, o sistema deve gravar a situação e a data de encerramento. | PMBOK 7 p. 166 (Q64) | confirmado | Núcleo | 1 | teste |
| RN-EC-09 | Somente um supervisor deve reabrir o projeto, com justificativa. | Regra do PMO (Q29, Q65) | alterado | Núcleo | 1 | teste |
| RN-EC-10 | A tela de encerramento deve ficar só para consulta depois do encerramento. | Regra do PMO (Q65) | alterado | Núcleo | 1 | teste |
| RN-EC-11 | As lições com alcance outras equipes ou organização devem aparecer em destaque no encerramento. | PMBOK 7 §2.5.8.1, p. 77 (Q64) | confirmado | Núcleo | 1 | teste |
| RN-EC-12 | Somente um supervisor deve encerrar ou cancelar o projeto. | Regra do PMO (Q29) | novo | Núcleo | 1 | teste |
| RN-EC-13 | Encerrar deve exigir o aceite final registrado; cancelar não exige. | PMBOK 7 §4.4.3, p. 180 (Q63) | novo | Núcleo | 1 | teste |
| RN-EC-14 | O aceite final deve registrar quem aceitou, escolhido entre as partes interessadas (patrocinador, dono do produto ou cliente), e a data. | PMBOK 7 §4.4.3, p. 180 (Q63, Q109) | novo | Núcleo | 1 | teste |
| RN-EC-15 | Encerrar deve exigir o encerramento, com o checklist e a avaliação final, liberado na revisão. | Regra do PMO (Q29, Q63) | novo | Núcleo | 1 | teste |

A passagem da equipe para o estágio de dissolução ao encerrar ou cancelar está na RN-EQ-20.

### 3.3 Usabilidade e acessibilidade

As páginas seguem a WCAG 2.1, níveis A e AA (Q38). O Octante não é feito para celular, mas a tela estreita serve a quem usa zoom de até 400% no computador (Q200, Q200b).

| Código | Requisito | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RNF-ACE-01 | Cada página deve declarar o idioma pt-BR. | WCAG 2.1, 3.1.1 (Q208) | confirmado | App | 1 | teste |
| RNF-ACE-02 | Cada página deve ter o link "Pular para o conteúdo". | WCAG 2.1, 2.4.1 (Q208) | confirmado | App | 1 | teste |
| RNF-ACE-03 | O elemento com o foco do teclado deve ficar visível. | WCAG 2.1, 2.4.7 (Q208) | confirmado | App | 1 | teste |
| RNF-ACE-04 | As mensagens de erro e de situação devem chegar aos leitores de tela sem receber o foco. | WCAG 2.1, 4.1.3 (Q208) | confirmado | App | 1 | teste |
| RNF-ACE-05 | Quando o servidor recusa um envio, a página deve voltar com o que foi digitado, com a mensagem junto do campo e o campo marcado como inválido para os leitores de tela, também sem JavaScript. | WCAG 2.1, 3.3.1 e 3.3.2 (Q199) | alterado | App | 1 | teste |
| RNF-ACE-06 | A marca da tela atual (aria-current) e o nome dela no botão do menu devem vir do servidor. | WCAG 2.1, 1.3.1 (Q200b) | alterado | App | 1 | teste |
| RNF-ACE-07 | O menu deve informar aos leitores de tela se está aberto e o que controla. | WCAG 2.1, 4.1.2 (Q208) | confirmado | App | 1 | teste |
| RNF-ACE-08 | O botão de dicas deve informar aos leitores de tela se está ligado. | WCAG 2.1, 4.1.2 (Q208) | confirmado | App | 1 | teste |
| RNF-ACE-09 | Cada gráfico deve ter uma descrição acessível e uma tabela com os dados. | WCAG 2.1, 1.1.1 (Q208) | confirmado | App | 1 | teste |
| RNF-ACE-10 | Cada situação mostrada por cor deve ter também ícone e texto. | WCAG 2.1, 1.4.1 (Q208) | confirmado | App | 1 | teste |
| RNF-ACE-11 | As cores da paleta devem ter contraste de pelo menos 4,5:1 no texto normal e 3:1 no texto grande, conferido por teste automático. | WCAG 2.1, 1.4.3 (Q208) | alterado | App | 1 | teste |
| RNF-ACE-12 | Com a preferência do sistema por menos movimento, as animações devem parar. | Regra do PMO, além do nível AA (WCAG 2.1, 2.3.3, nível AAA) (Q208) | confirmado | App | 1 | teste |
| RNF-ACE-13 | Os alvos de clique devem ter pelo menos 40 px. | Regra do PMO (Q208) | confirmado | App | 1 | teste |
| RNF-ACE-14 | O asterisco dos campos obrigatórios deve vir do servidor, no rótulo do campo. | WCAG 2.1, 3.3.2 (Q199) | alterado | App | 1 | teste |
| RNF-ACE-16 | A busca deve ser marcada como região de busca e ter um atalho de teclado. | WCAG 2.1, 1.3.1 e 2.1.1 (Q208) | confirmado | App | 1 | teste |
| RNF-ACE-17 | Cada imagem deve ter texto alternativo. | WCAG 2.1, 1.1.1 (Q208) | confirmado | App | 1 | teste |
| RNF-USA-01 | O aviso "Aguarde…", o bloqueio de duplo envio e o foco na mensagem de erro devem funcionar no navegador como ajuda, sem ser a única proteção. | Regra do PMO (Q198, Q199) | alterado | App | 1 | teste |
| RNF-USA-02 | O projeto encerrado ou cancelado deve mostrar uma única faixa de "somente consulta", com o link para o encerramento, e o link Reabrir só para o supervisor. | Regra do PMO (Q29, Q208) | alterado | App | 1 | teste |
| RNF-USA-03 | O aviso de alterações não salvas deve funcionar no navegador como ajuda. | Regra do PMO (Q198) | alterado | App | 1 | teste |
| RNF-USA-05 | As cores devem vir só dos tokens da paleta, inclusive as transparências, e o teste deve conferir também esse formato. | Regra do PMO (Q208) | alterado | App | 1 | teste |
| RNF-USA-07 | O menu recolhido da tela estreita deve abrir sem JavaScript. | WCAG 2.1, 1.4.10 (Q200b) | alterado | App | 1 | teste |
| RNF-USA-08 | Os cartões devem ter largura mínima, e o menu deve recolher na tela estreita. | WCAG 2.1, 1.4.10 (Q208) | confirmado | App | 1 | teste |
| RNF-USA-11 | A mensagem de sucesso deve ficar na tela até a pessoa fechá-la ou mudar de página. | WCAG 2.1, 2.2.1 e 4.1.3 (Q201) | alterado | App | 1 | teste |
| RNF-USA-13 | O projeto novo deve mostrar só o essencial e o próximo passo do guia. | Regra do PMO (Q208) | confirmado | Núcleo | 2 | teste |
| RNF-USA-15 | Em cada tela, os campos que vêm do PMBOK 7 devem aparecer primeiro, com a seção citada, e os do PMO num bloco "Campos do PMO". | Regra do PMO (Q68) | novo | App | 2 | teste |
| RNF-RES-01 | Cada página deve declarar a área de visualização para a largura do dispositivo. | WCAG 2.1, 1.4.10 (Q208) | confirmado | App | 1 | teste |
| RNF-RES-02 | O layout deve se ajustar nas larguras de 600, 700, 900 e 1.250 px. | WCAG 2.1, 1.4.10 (Q208) | confirmado | App | 1 | teste |
| RNF-RES-03 | As tabelas largas, os gráficos e o quadro de tarefas devem rolar para o lado pelo CSS, sem JavaScript, e o resto da página deve caber numa largura de 320 px, que é a janela de 1.280 px com zoom de 400%. | WCAG 2.1, 1.4.4 e 1.4.10 (Q200b) | alterado | App | 1 | teste |
| RNF-RES-06 | As páginas devem ter estilos de impressão. | Regra do PMO (Q208) | confirmado | App | 1 | demonstração |
| RNF-MAR-01 | O Octante deve usar o nome e o logo em SVG da marca. | Regra do PMO (Q208) | confirmado | App | 1 | inspeção |
| RNF-MAR-02 | O repositório deve ter o script que gera os arquivos da marca. | Regra do PMO (Q208) | confirmado | App | 1 | inspeção |
| RNF-MAR-03 | A paleta da marca deve estar em tokens. | Regra do PMO (Q208) | confirmado | App | 1 | teste |
| RNF-MAR-04 | Os gráficos devem usar as cores roxo, laranja e ciano da marca. | Regra do PMO (Q208) | confirmado | App | 1 | inspeção |
| RNF-MAR-05 | O cabeçalho da planilha exportada deve usar a cor da marca. | Regra do PMO (Q208) | confirmado | App | 1 | teste |
| RNF-MAR-06 | O logo deve existir também em contornos. | Regra do PMO (Q208) | confirmado | App | 1 | inspeção |

### 3.4 Desempenho

O Octante atende um PMO de 1 a 3 supervisores e até uns 15 gerentes de projetos, com 1 a 3 projetos cada (Q4).

| Código | Requisito | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RNF-DES-01 | As dicas devem ficar em cache depois da primeira leitura. | Regra do PMO (Q208) | confirmado | App | 1 | teste |
| RNF-DES-02 | O banco deve ter índice em cada chave estrangeira. | Regra do PMO (Q208) | confirmado | App | 1 | teste |
| RNF-DES-03 | A condição do backup automático deve ser conferida no máximo uma vez por hora. | Regra do PMO (Q208) | confirmado | App | 1 | teste |
| RNF-DES-04 | As leituras longas devem ter limite: o histórico mostra 300 eventos, e a busca, 150 resultados. | Regra do PMO (Q208) | confirmado | App | 1 | teste |
| RNF-DES-05 | O portfólio deve abrir em até 1 segundo com 50 projetos, conferido por teste automático. | Regra do PMO (Q203) | alterado | App | 1 | teste |
| RNF-DES-06 | O banco deve atender ao uso de um PMO, com pouca escrita ao mesmo tempo. | Regra do PMO (Q208) | confirmado | App | 1 | análise |

Se a meta da RNF-DES-05 for passada, o PMO decide entre cache e paginação (Q203).

### 3.5 Banco de dados lógico

**Informações guardadas:** contas e preferências; projetos, com o termo e as versões dele; partes interessadas, contatos e planos de comunicação; membros, matriz RACI e saúde da equipe; abordagem, fases e tailoring; iterações e itens de escopo; questões, mudanças e lições; riscos, reservas e outras incertezas; indicadores, medições e relatórios de status; business case, conformidade, decisões, premissas e mudança organizacional; aquisições e recursos físicos; revisões, aprovações, aceites e pareceres; histórico, lixeira, backups e pedidos do titular. **Acesso:** pelas regras de papel e de projeto (RN-PM-05, RN-PM-07, RN-PM-12, RN-PM-55, RN-PM-71). **Segurança e guarda:** histórico protegido (RN-DA-17), prazos de guarda (RF-PM-17, RF-DA-18) e anonimização (RN-DA-12 a RN-DA-13, RN-DA-37 a RN-DA-42).

| Código | Requisito | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RNF-INT-01 | As migrações do banco devem ser numeradas e feitas dentro de uma transação. | Regra do PMO (Q196) | confirmado | App | 1 | teste |
| RNF-INT-02 | O banco deve conferir as chaves estrangeiras. | Regra do PMO (Q196) | confirmado | App | 1 | teste |
| RNF-INT-03 | O banco deve ter gatilhos que validam as faixas da RN-DA-15. | Regra do PMO (Q196) | confirmado | App | 1 | teste |
| RNF-INT-04 | O banco deve ter as restrições de unicidade e de verificação dos valores válidos. | Regra do PMO (Q196) | confirmado | App | 1 | teste |
| RNF-INT-05 | O banco deve ter índice em cada chave estrangeira usada nas consultas. | Regra do PMO (Q196) | confirmado | App | 1 | teste |
| RNF-INT-06 | O banco deve esperar até 10 segundos por um registro travado antes de falhar. | Regra do PMO (Q196) | confirmado | App | 1 | teste |
| RNF-INT-08 | O código sequencial de cada registro deve ser único no projeto, garantido pelo banco. | Regra do PMO (Q196) | alterado | App | 1 | teste |
| RNF-INT-09 | O servidor deve validar as listas, as faixas e as datas de cada entrada. | Regra do PMO (Q196) | confirmado | App | 1 | teste |

### 3.6 Restrições de projeto

| Código | Requisito | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RNF-POR-01 | O Octante deve rodar em Python 3.10 ou mais novo, com a CI testando o 3.10 e o 3.13. | Regra do PMO (Q208) | confirmado | App | 1 | teste |
| RNF-POR-02 | O requirements.txt deve travar a versão exata e o hash SHA-256 de cada biblioteca, inclusive das que o Flask traz, e o pip deve recusar o arquivo que não bate. | pip (hash-checking mode) (Q204, Q204b) | alterado | App | 1 | inspeção |
| RNF-POR-03 | Sem a biblioteca de planilha, a exportação deve sair em CSV. | Regra do PMO (Q208) | confirmado | App | 1 | teste |
| RNF-POR-04 | O repositório deve ter scripts de início para Windows e para Linux. | Regra do PMO (Q208) | confirmado | App | 1 | demonstração |
| RNF-POR-05 | A configuração do servidor deve vir de variáveis de ambiente. | Regra do PMO (Q208) | confirmado | App | 1 | teste |
| RNF-POR-06 | No computador local, o Octante deve avisar quando a porta está em uso e abrir o navegador. | Regra do PMO (Q208) | confirmado | App | 1 | demonstração |
| RNF-POR-07 | O Octante deve ter o ponto de entrada WSGI para o PythonAnywhere. | Regra do PMO (Q42, Q208) | confirmado | App | 1 | teste |
| RNF-POR-08 | O DEPLOY.md deve usar o nome octante. | Regra do PMO (Q208) | alterado | App | 1 | inspeção |
| RNF-POR-09 | O banco deve ser um arquivo SQLite único. | Regra do PMO (Q42, Q208) | confirmado | App | 1 | teste |
| RNF-POR-10 | A atualização do Octante deve preservar a pasta instance e migrar o banco. | Regra do PMO (Q208) | confirmado | App | 1 | teste |
| RNF-POR-11 | O app deve usar só as bibliotecas aprovadas pelo PMO, baixadas do PyPI oficial: Flask e openpyxl, com as que eles trazem, e a tzdata; no desenvolvimento e na CI, também pytest, pytest-cov, ruff, mutmut, pip-tools, pip-audit, playwright e pytest-playwright. | Regra do PMO (Q204b, Q212) | novo | App | 1 | inspeção |
| RNF-POR-12 | Antes de instalar uma biblioteca, o nome deve ser conferido na página oficial do projeto, e a biblioteca nova deve ter decisão do PMO. | Regra do PMO (Q204b) | novo | App | 1 | inspeção |
| RNF-POR-13 | O Dependabot deve propor cada atualização num pull request próprio, 7 dias depois da versão nova, exceto nas correções de segurança. | GitHub Docs (cooldown) (Q204, Q204b) | novo | App | 1 | inspeção |
| RNF-POR-14 | A CI deve rodar o pip-audit e reprovar a versão com falha conhecida. | Regra do PMO (Q78, Q204b) | novo | App | 1 | teste |
| RNF-POR-15 | As actions da CI devem ficar presas pelo SHA completo do commit. | GitHub Docs (Q204b) | novo | App | 1 | inspeção |
| RNF-POR-16 | Um pull request de dependência deve entrar só com a CI aprovada e a revisão do responsável pelo produto. | Regra do PMO (Q204, Q204b) | novo | App | 1 | inspeção |
| RNF-POR-17 | Os testes de tela devem usar o Playwright só com o Chromium e o axe-core num arquivo guardado com os testes, com a versão, o hash e o aviso da licença MPL-2.0. | Regra do PMO (Q212) | novo | App | 1 | inspeção |
| RNF-POR-18 | O Docker deve ser usado só no desenvolvimento e na CI. | Regra do PMO (Q76) | novo | App | 1 | inspeção |
| RNF-I18-01 | A interface deve estar só em português do Brasil. | Regra do PMO (Q38, Q208) | confirmado | App | 1 | inspeção |
| RNF-I18-03 | As datas devem aparecer como dd/mm/aaaa e ser guardadas no formato ISO. | Regra do PMO (Q208) | confirmado | App | 1 | teste |
| RNF-I18-04 | Os valores em dinheiro devem aparecer em R$ e aceitar a entrada com ou sem separador de milhar. | Regra do PMO (Q208) | confirmado | App | 1 | teste |
| RNF-I18-05 | O arquivo .ics deve escapar os textos como manda a RFC 5545. | RFC 5545 (Q208) | confirmado | App | 1 | teste |
| RNF-I18-06 | O CSV deve usar ponto e vírgula como separador e começar com o BOM, para abrir certo nas planilhas em português. | Regra do PMO (Q208) | confirmado | App | 1 | teste |

### 3.7 Conformidade com normas

| Código | Requisito | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RNF-USA-16 | Cada regra e cada alerta devem mostrar a origem: a página do PMBOK 7 ou "regra do PMO". | ADR 0005 (Q49, Q153) | novo | App | 2 | teste |
| RNF-USA-17 | Cada termo do PMBOK 7 traduzido deve mostrar o original em inglês entre parênteses. | Regra do PMO (Q113) | novo | App | 2 | inspeção |
| RNF-AUD-03 | A tela de histórico deve mostrar nomes legíveis para as tabelas e os campos. | Regra do PMO (Q196) | confirmado | App | 1 | teste |
| RNF-AUD-04 | O Octante deve registrar quem decidiu em cada decisão do projeto: termo, mudança, aceite, revisão de fase e revisão. | PMBOK 7 p. 87 e 180 (Q196) | confirmado | App | 1 | teste |

A trilha de auditoria (histórico com o valor anterior e o novo, protegido contra alteração) está nas RN-DA-01, RN-DA-17 e RN-DA-18; a LGPD, nas seções 3.2.3 e 3.8; e a WCAG 2.1, na seção 3.3.

### 3.8 Atributos do sistema

**Segurança**

| Código | Requisito | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RNF-SEG-01 | Cada tela deve exigir login, exceto Entrar, Primeiro acesso, Privacidade e os arquivos estáticos. | Regra do PMO (Q189, Q196) | alterado | App | 1 | teste |
| RNF-SEG-02 | A senha deve ser guardada só como hash, com a função de hash do Werkzeug. | OWASP ASVS 5.0 (Q196) | confirmado | App | 1 | teste |
| RNF-SEG-04 | O cookie de sessão deve ter HttpOnly e SameSite=Lax e, em produção, Secure. | OWASP ASVS 5.0 (Q187, Q196) | alterado | App | 1 | teste |
| RNF-SEG-06 | A conta desativada deve perder o acesso na requisição seguinte. | Regra do PMO (Q196) | confirmado | App | 1 | teste |
| RNF-SEG-07 | O redirecionamento depois do login deve levar só a uma página do próprio Octante. | OWASP ASVS 5.0 (Q196) | confirmado | App | 1 | teste |
| RNF-SEG-08 | Cada envio de formulário deve ter o token anti-CSRF da sessão. | OWASP ASVS 5.0 (Q196) | confirmado | App | 1 | teste |
| RNF-SEG-09 | O servidor deve recusar, com o código 403, o envio que vem de outra origem. | OWASP ASVS 5.0 (Q196) | confirmado | App | 1 | teste |
| RNF-SEG-10 | As respostas devem levar os cabeçalhos de segurança: política de conteúdo (CSP), nosniff, proibição de moldura, HSTS e no-store. | OWASP ASVS 5.0 (Q196) | confirmado | App | 1 | teste |
| RNF-SEG-13 | Um registro de um projeto deve ficar fora do alcance de outro projeto, também nos registros filhos. | Regra do PMO (Q196) | confirmado | App | 1 | teste |
| RNF-SEG-17 | A chave secreta deve ser própria de cada instalação, num arquivo com permissão só para o dono. | OWASP ASVS 5.0 (Q196) | alterado | App | 1 | teste |
| RNF-SEG-18 | Em produção, o depurador deve ficar desligado, e o servidor local deve ouvir só em 127.0.0.1. | OWASP ASVS 5.0 (Q196) | confirmado | App | 1 | teste |
| RNF-SEG-19 | A marca interna do projeto de exemplo não deve poder ser forjada por um cabeçalho. | Regra do PMO (Q196) | confirmado | App | 1 | teste |
| RNF-SEG-20 | As consultas ao banco devem ser parametrizadas, e a busca deve escapar os curingas. | OWASP ASVS 5.0 (Q196) | confirmado | App | 1 | teste |
| RNF-SEG-21 | As páginas devem escapar o texto automaticamente, também dentro de JSON e de SVG. | OWASP ASVS 5.0 (Q196) | confirmado | App | 1 | teste |
| RNF-SEG-22 | Os erros devem mostrar uma página com explicação em linguagem simples, sem detalhes técnicos. | OWASP ASVS 5.0 (Q196) | confirmado | App | 1 | teste |

**Privacidade**

| Código | Requisito | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RNF-PRV-03 | As páginas com dados não devem ficar em cache (no-store). | LGPD, art. 46 (Q196) | confirmado | App | 1 | teste |
| RNF-PRV-04 | As respostas devem levar a Permissions-Policy e a Referrer-Policy. | LGPD, art. 46 (Q196) | confirmado | App | 1 | teste |
| RNF-PRV-05 | As páginas devem funcionar sem nenhum recurso de terceiros. | LGPD, art. 46 (Q196) | confirmado | App | 1 | teste |

**Confiabilidade e disponibilidade**

| Código | Requisito | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RNF-BKP-04 | O backup deve ser uma cópia consistente do banco, gravada de uma vez. | Regra do PMO (Q196) | confirmado | App | 1 | teste |
| RNF-BKP-07 | A restauração de um backup de versão anterior deve migrar o banco. | Regra do PMO (Q196) | confirmado | App | 1 | teste |
| RNF-BKP-08 | O download do banco deve ser uma cópia consistente. | Regra do PMO (Q196) | confirmado | App | 1 | teste |
| RNF-BKP-09 | A falha de um backup deve deixar o Octante funcionando. | Regra do PMO (Q196) | confirmado | App | 1 | teste |

**Manutenibilidade**

| Código | Requisito | Origem | Protótipo | Parte | Entrega | Verificação |
|---|---|---|---|---|---|---|
| RNF-MAN-02 | A CI deve rodar os testes no GitHub Actions, no Python 3.10 e no 3.13. | Regra do PMO (Q208) | confirmado | App | 1 | teste |
| RNF-MAN-03 | O teste da regra de tokens de cor deve conferir também as cores escritas em rgba. | Regra do PMO (Q208) | alterado | App | 1 | teste |
| RNF-MAN-04 | O código deve ter um blueprint por domínio, e o conteúdo do PMBOK 7 deve ficar num módulo próprio. | Regra do PMO (Q208) | confirmado | App | 1 | inspeção |
| RNF-MAN-05 | O módulo do banco deve explicar no topo as convenções que segue. | Regra do PMO (Q208) | confirmado | App | 1 | inspeção |
| RNF-MAN-06 | Os alertas de um projeto devem ser reunidos por uma única função. | Regra do PMO (Q208) | confirmado | App | 1 | inspeção |
| RNF-MAN-07 | As páginas devem funcionar sem JavaScript escrito dentro do HTML, como pede a política de conteúdo. | OWASP ASVS 5.0 (Q208) | confirmado | App | 1 | teste |
| RNF-MAN-08 | A documentação do repositório (README, DEPLOY, AVALIACAO e docs) deve estar de acordo com a versão atual. | Regra do PMO (Q208) | confirmado | App | 1 | inspeção |
| RNF-MAN-10 | Os testes devem rodar com o login e o CSRF ligados, como em produção, com cada teste entrando com o papel que o caso testado exige. | Regra do PMO (Q205) | alterado | App | 1 | inspeção |
| RNF-MAN-12 | A cobertura dos testes deve ser de pelo menos 95% das linhas e das ramificações, e a CI deve reprovar abaixo disso. | Regra do PMO (Q77) | novo | App | 1 | teste |
| RNF-MAN-13 | As regras de revisão, de mudança e de encerramento devem ter testes de mutação. | Regra do PMO (Q77) | novo | App | 1 | teste |
| RNF-MAN-14 | Cada regra de negócio deve ter teste do caminho válido e do inválido, com o código da regra no teste. | Regra do PMO (Q77) | novo | App | 1 | inspeção |
| RNF-MAN-15 | Cada entrada (campo, parâmetro e arquivo) deve ter testes por partição de equivalência e valores-limite: válido, vazio, ausente, só espaços, no limite, um acima e um abaixo, tipo errado, texto longo demais, caracteres especiais e tentativas de injeção de HTML, JavaScript e SQL. | Regra do PMO (Q77) | novo | App | 1 | inspeção |
| RNF-MAN-16 | Cada tela deve ter teste de acesso com um papel que ela aceita e com um papel que ela recusa. | Regra do PMO (Q205) | novo | App | 1 | inspeção |
| RNF-MAN-17 | A CI deve conferir o estilo com o ruff e reprovar o erro. | Regra do PMO (Q78b, Q205) | novo | App | 1 | teste |
| RNF-MAN-18 | Os logs devem ser estruturados, com a biblioteca de logs do próprio Python. | Regra do PMO (Q78, Q212) | novo | App | 1 | inspeção |
| RNF-MAN-19 | As telas devem ter testes de acessibilidade com o Playwright e o axe. | WCAG 2.1 (Q78, Q212) | novo | App | 1 | teste |
| RNF-MAN-20 | Os testes do protótipo devem ser refeitos, e os requisitos sem teste ou com teste parcial devem ganhar teste. | Regra do PMO (Q196, Q205, Q208) | novo | App | 1 | inspeção |

**Portabilidade:** o Octante roda no PythonAnywhere e no computador local, no Windows e no Linux (RNF-POR-01 a RNF-POR-10), com o fuso configurado valendo em qualquer sistema (RN-DA-16).

## 4. Verificação

Cada requisito traz o método de verificação na coluna Verificação (Q216). Os métodos são:

- **Teste:** teste automático, que roda na CI a cada envio de código. As funções e as regras são testadas pelo pytest, com o login e o CSRF ligados (RNF-MAN-10); as telas e a acessibilidade, pelo Playwright com o axe (RNF-MAN-19). Cada regra tem o teste do caminho válido e do inválido, com o código no teste (RNF-MAN-14), e cada entrada, os testes de partição e de valores-limite (RNF-MAN-15). As regras de revisão, de mudança e de encerramento têm testes de mutação (RNF-MAN-13), e a cobertura mínima é de 95% (RNF-MAN-12).
- **Inspeção:** revisão de um arquivo, do código ou de um texto, feita pelo Claude antes de cada entrega e pelo responsável pelo produto no pull request.
- **Demonstração:** mostrar funcionando no app, como a impressão e os scripts de início.
- **Análise:** medição ou cálculo, como a carga que o banco atende.

A CI só aprova um pull request com os testes passando, a cobertura mínima, o ruff sem erro e o pip-audit sem falha conhecida (RNF-MAN-12, RNF-MAN-17, RNF-POR-14). Os critérios de aceite de cada história ficam nas issues (Q6).

## 5. Informações de apoio

Nada nesta seção é requisito: ela só ajuda a ler a ERS (9.6.20).

### 5.1 Rastreabilidade

- **Requisito → regras:** a coluna Regras de cada função.
- **Requisito → decisões:** a coluna Origem, com as perguntas do [registro de decisões](decisoes-elicitacao.md), que guarda a justificativa de cada uma.
- **Regra → PMBOK 7:** a coluna Origem, com a seção e a página, conferidas na [origem das regras](origem-das-regras.md).
- **Protótipo → ERS:** a coluna Protótipo e a [tabela das funções](rf-regras-decisoes.md), que liga cada função do protótipo às regras e às decisões.
- **ERS → issues e testes:** cada issue e cada teste citam o código do requisito (Q13, RNF-MAN-14).

### 5.2 Códigos que saíram

| Código | O que era | Decisão |
|---|---|---|
| RF-MT-06 | Pré-mortem | Q102 |
| RF-AQ-04 | Botão que cadastrava o fornecedor como parte interessada | Q147 |
| PI-11 | Grade poder × interesse de Mendelow | Q105b |
| EQ-15 | Alerta de equipe sem membros | Q165 |
| AB-22 | Alerta de "seguir com ressalvas" sem notas | Q179 |
| PL-09 | Gerador da visão no formato de Moore | Q66 |
| TR-09 | Alerta de questão sem responsável nem parte | Q167 |
| IN-34 | Pré-mortem | Q102 |
| PR-19, PR-20 | Nível calculado dos princípios e alerta de princípios fracos | Q143 |
| AQ-11 | Alerta do fornecedor que não é parte interessada | Q147 |

Os códigos que saíram não são reaproveitados (Q217).

### 5.3 Não funcionais do protótipo que viraram outros requisitos

Estes não funcionais do inventário não têm linha própria, porque o que eles diziam está em outro requisito, para não ser escrito duas vezes (Q214).

| Código do protótipo | Onde está agora |
|---|---|
| RNF-SEG-03 | RN-PM-03, RN-PM-30, RN-PM-31 |
| RNF-SEG-05 | RN-PM-32 |
| RNF-SEG-11 | RN-PM-05, RN-PM-12 |
| RNF-SEG-12 | RN-PM-07, RN-PM-72 |
| RNF-SEG-14 | RN-DA-11, RN-DA-36 |
| RNF-SEG-15 | RN-DA-35 |
| RNF-SEG-16 | RN-DA-14 |
| RNF-SEG-23 | RN-PM-25 a RN-PM-28 |
| RNF-SEG-24, RNF-USA-04 | RF-DA-19, RN-DA-31 |
| RNF-PRV-01 | RN-DA-13, RN-DA-37 a RN-DA-42 |
| RNF-PRV-02 | RN-DA-02 |
| RNF-PRV-06 | RF-DA-11 a RF-DA-17 |
| RNF-AUD-01, RNF-AUD-02, RNF-AUD-05 | RN-DA-01, RN-DA-32, RN-DA-17 |
| RNF-AUD-06 | RN-TR-14, RN-TR-18 |
| RNF-BKP-01 a RNF-BKP-03, RNF-BKP-05, RNF-BKP-06 | RN-DA-07, RN-DA-34, RN-DA-09, RN-DA-10 |
| RNF-BKP-10, RNF-INT-07 | RN-DA-04, RN-DA-33 |
| RNF-BKP-11 | RN-DA-20, RN-DA-21 |
| RNF-BKP-12 | RN-DA-06 |
| RNF-INT-10 | RN-PL-19 |
| RNF-ACE-15, RNF-USA-06, RNF-USA-09 | RNF-ACE-05, RNF-ACE-14 |
| RNF-USA-10 | RF-GU-02 a RF-GU-04 |
| RNF-USA-12 | RF-GU-09, RN-GU-14 |
| RNF-USA-14 | RNF-USA-07, RNF-RES-03 |
| RNF-RES-04, RNF-RES-05 | RNF-USA-07, RNF-RES-03 |
| RNF-I18-02, RNF-I18-07 | RN-DA-16 |
| RNF-MAN-01, RNF-MAN-09, RNF-MAN-11 | RNF-MAN-08, RNF-MAN-12, RNF-MAN-17, RNF-MAN-20 |
| RNF-MAR-07 | RNF-MAN-08 |

### 5.4 Evolução prevista

- E-mail por API HTTPS, com as mensagens numa fila de saída no banco (Q41, Q42, Q76, Q197). O e-mail para gente de fora pede base legal e opção de descadastro (Q41).
- Troca da fila de saída pelo RabbitMQ, e Prometheus e Grafana, se um dia houver servidor próprio (Q76, Q197).
- Cache ou paginação do portfólio, se a meta da RNF-DES-05 for passada (Q203).
- Adaptação ao PMBOK 8 (Q30, Q47).

**Fora do escopo:** notificação por prazo (Q42), versão para celular (Q200), TIR no business case, por ora (Q138), formalidades de estágio (Q207) e filas entre os módulos (Q197).

### 5.5 Pontos a confirmar

| Ponto | Requisitos | Quem confirma | Até quando |
|---|---|---|---|
| Os 5 anos de padrão do prazo de guarda dos pareceres | RF-PM-17 | o responsável pelo produto, com o RH ou o jurídico do PMO (Q25) | Entrega 1 |
| Os 5 anos de padrão do prazo de guarda dos projetos | RF-DA-18 | o responsável pelo produto, com o RH ou o jurídico do PMO (Q193) | Entrega 2 |

Os dados da página de privacidade (controlador, encarregado e base legal) não são requisitos: o Administrador os preenche em cada instalação (RF-DA-12).

---

**Fim da ERS.** Versão 1.1, a linha de base dos requisitos (Q218), com as mudanças da Q219.
