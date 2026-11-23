<h1 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="static/marca/octante-logo-negativo.svg">
    <img src="static/marca/octante-logo.svg" alt="Octante" width="304">
  </picture>
</h1>

[![testes](https://github.com/DennerRR/octante/actions/workflows/testes.yml/badge.svg?branch=develop)](https://github.com/DennerRR/octante/actions/workflows/testes.yml)

Sistema web para o PMO conduzir os seus projetos reais com base no **PMBOK® Guide – Sétima Edição**. O ensino vem junto com o uso: cada tela explica o conceito do PMBOK que está sendo aplicado e mostra o que falta preencher.

O nome vem do octante, instrumento de navegação que mede ângulos com 1/8 de círculo: orientar o rumo do projeto, medir o desempenho e os 8 domínios de desempenho do PMBOK 7.

> **Situação em novembro de 2026:** o código deste repositório é um **protótipo feito com vibe coding**. Os requisitos estão sendo especificados agora, e o protótipo ainda não segue as decisões já tomadas. Veja a [situação do projeto](#situação-do-projeto).

## Para quem é

- **PMO** de 1 a 3 supervisores e até uns 15 gerentes de projetos. Cada gerente de projetos conduz de 1 a 3 projetos, e um projeto tem no máximo dois: o gerente do projeto e um gerente de apoio.
- **Projetos** reais, na maioria internos de TI e de melhoria de processos, em abordagem híbrida.
- **Quem entra no sistema:** só os gerentes de projetos e os supervisores. Patrocinador, cliente e equipe recebem os documentos gerados, sem login.

| Papel | O que faz |
|---|---|
| Gerente do projeto | Conduz o projeto e responde por ele ao supervisor. Em geral, tem conhecimento de nível inicial. |
| Gerente de apoio | Opcional. Trabalha no projeto com os mesmos poderes de edição, sem responder por ele. |
| Supervisor designado | Cria o projeto e revisa o que o gerente do projeto envia, como o termo de abertura, o relatório de status, as mudanças e o encerramento. Outro supervisor pode substituí-lo. |
| Administrador | Papel extra de um supervisor, com poder sobre usuários, backups e dados. |
| Destinatário | Patrocinador, cliente ou equipe. Recebe os documentos gerados, sem acesso ao sistema. |

Esses papéis foram decididos na elicitação e chegam na Entrega 1. Hoje o protótipo só distingue o administrador dos demais usuários.

## O que o protótipo faz hoje

- **Portfólio do PMO:** todos os projetos com o semáforo de prazo, custo, escopo, riscos, partes interessadas e questões. Também tem minhas pendências, busca, agenda de prazos com exportação para o calendário (.ics) e exportação para Excel.
- **Guia do projeto:** mostra a próxima etapa a fazer, com glossário, ajuda e exemplo de preenchimento em cada tela, e um projeto de exemplo para consulta.
- **Os 8 domínios de desempenho:**
  - partes interessadas: identificar, analisar, priorizar, engajar e monitorar;
  - equipe: membros, matriz RACI, acordo de trabalho e saúde da equipe;
  - abordagem e ciclo de vida: os 15 fatores de escolha da abordagem, fases com revisão de fase e tailoring;
  - planejamento: termo de abertura, declaração de visão, cronograma, orçamento e Gantt com dependências;
  - trabalho do projeto: questões, mudanças, lições aprendidas, aquisições e recursos físicos;
  - entrega: backlog, requisitos, definição de pronto, aceite, quadro de tarefas, linha de base do escopo, custo da qualidade e benefícios;
  - medição: valor agregado, burnup e burndown, velocidade, fluxo, indicadores, plano de exceção e relatórios de status;
  - incerteza: registro de riscos com probabilidade e impacto, reservas, valor monetário esperado e risco geral do projeto.
- **Os 12 princípios:** autoavaliação, business case (VPL, ROI e payback), conformidade, mudança organizacional, registro de decisões e premissas.
- **Revisão do PMO:** o usuário envia um registro para revisão, e o administrador aprova ou devolve com comentário. Há também nível de exigência (essencial ou rigoroso), modelos de projeto e a completude de cada registro.
- **Alertas automáticos** em todos os domínios, reunidos nos pontos de atenção de cada projeto.
- **Encerramento:** checklist, comparação com o planejado e avaliação final, com as opções de encerrar, cancelar ou reabrir o projeto.
- **Dados e segurança:** login, histórico de todas as alterações, lixeira com restauração, backups automáticos verificados e assinados, e anonimização de dados pessoais (LGPD).

Muitas dessas telas vão mudar, porque a auditoria achou regras a corrigir em todas as áreas. O que cada tela faz hoje está nos [inventários do protótipo](#documentação).

## Situação do projeto

### Como o protótipo foi feito

O protótipo foi desenvolvido com *vibe coding*: o código foi gerado pelo Claude, IA da Anthropic, a partir de pedidos em linguagem natural, sem conceitos de engenharia de software. Não houve requisitos especificados, arquitetura planejada nem conferência de cada regra contra a referência. O resultado funciona e tem testes automatizados, mas as regras de negócio foram sendo criadas pelo caminho.

### O que a auditoria encontrou

Na conferência contra o PMBOK 7, apareceram:

- regras de outras fontes apresentadas como se fossem do PMBOK 7, como a grade de Mendelow e os níveis de engajamento do PMBOK 6;
- regras que contrariam o PMBOK 7, como o guia que chamava de fases os grupos de processos, que o PMBOK diz que se repetem dentro de cada fase;
- regras que nunca disparam, ou que dependem de uma tela que pode estar desligada;
- textos que prometem o que o código não faz, como a matriz RACI que "exigia" um aprovador, mas só avisava.

### O que está sendo feito

A elicitação especifica os requisitos do sistema que já existe ([issue #3](https://github.com/DennerRR/octante/issues/3)). Cada regra do protótipo é conferida contra o PMBOK 7, a única referência ([ADR 0001](docs/adr/0001-pmbok-7-como-referencia.md)), e recebe um de três veredictos:

1. **De acordo com o PMBOK 7:** entra, com seção e página.
2. **Não conforme:** é defeito, e a regra passa a seguir o PMBOK 7.
3. **O PMBOK 7 não trata:** só fica por decisão explícita do PMO, marcada como "regra do PMO".

O inventário do protótipo tem 321 regras de negócio, 138 requisitos funcionais e 136 não funcionais. A auditoria das regras e a revisão dos requisitos funcionais e não funcionais terminaram. O [resumo para confirmação](docs/requisitos/resumo-para-confirmacao.md) foi confirmado, e a [especificação](docs/requisitos/ERS.md) foi aprovada na versão 1.0, com 789 requisitos (173 funcionais, 501 regras de negócio e 115 não funcionais), hoje na versão 1.1. Agora as histórias de usuário da Entrega 1 viram [issues](https://github.com/DennerRR/octante/issues), um domínio por vez: o Encerramento, Usuários e acesso e o PMO estão prontos.

### Próximos passos

1. Terminar as histórias de usuário da Entrega 1, com os critérios de aceite, a partir da [ERS](docs/requisitos/ERS.md) aprovada: um épico por domínio e uma issue por requisito, no [marco Entrega 1](https://github.com/DennerRR/octante/milestone/1).
2. Juntar a elicitação à `develop`, pelo PR da issue #3.
3. Evoluir o protótipo até cumprir a especificação ([ADR 0003](docs/adr/0003-evoluir-o-prototipo-reauditando-as-regras.md)), em entregas:
   - **Entrega 1:** papéis, criação do projeto pelo supervisor, revisão obrigatória, aprovação separada da revisão, encerramento pelo supervisor, parecer, acesso de consulta e desligamento.
   - **Entrega 2:** núcleo e tailoring, nível de exigência e cadência de relatório por projeto, relatório de status com indicadores congelados, visão do supervisor por gerente de projetos e resumo dos alertas.
   - **Entrega 3:** as regras de alerta e os módulos de tailoring.
   - **Depois:** envio de e-mail e a adaptação ao PMBOK 8.

## Requisitos já decididos (amostra)

Uma amostra do que a elicitação decidiu, para dar uma ideia do sistema. Nada disso está implementado ainda. A lista completa está nos [documentos da elicitação](#documentação) e vai para a especificação.

"p." é página do Guia do PMBOK 7, edição em inglês. "Qn" é a pergunta do [registro de decisões](docs/requisitos/decisoes-elicitacao.md) em que a decisão foi tomada.

### Funcionais

- O supervisor cria o projeto e escolhe o gerente do projeto e, se quiser, um gerente de apoio. O gerente do projeto entra sozinho na equipe do projeto. (Q27, Q114)
- O termo de abertura passa pela revisão do supervisor e pela aprovação do patrocinador. Depois de aprovado, só muda por mudança aprovada. (Q10, Q15, Q62)
- As partes interessadas seguem as cinco etapas do PMBOK 7: identificar, analisar, priorizar, engajar e monitorar. Cada parte tem plano de comunicação (como, com que frequência e por quem) e registro de contatos. (p. 10–14 e 186; Q105b, Q106b, Q108)
- Cada projeto tem um núcleo, sempre presente, e módulos opcionais que o tailoring liga. O gerente do projeto propõe, e o supervisor revisa. Um módulo desligado some do projeto, com os seus alertas. (Q18, Q31, Q57, Q174a)
- O guia do projeto segue os cinco grupos de processos, de Iniciação a Encerramento, e deixa claro que eles não são fases. (p. 170–171; Q149)
- Os alertas têm três níveis (alto, médio e informativo), e cada um mostra a sua origem: a página do PMBOK 7 ou "regra do PMO". (Q153; [ADR 0005](docs/adr/0005-origem-de-cada-regra-na-tela.md))

### Não funcionais

- Hospedagem gratuita no PythonAnywhere. ([ADR 0002](docs/adr/0002-hospedagem-no-pythonanywhere-gratuito.md))
- Login com senha de 8 ou mais caracteres, bloqueio de 5 minutos depois de 5 tentativas erradas e sessão de 12 horas. (Q51)
- Cobertura de testes de no mínimo 95% de linhas e de ramificações, com a CI reprovando abaixo disso. Cada regra de negócio tem teste do caminho válido e do inválido. (Q77)
- O administrador baixa uma cópia de segurança pelo menos uma vez por semana, porque os backups automáticos ficam no mesmo servidor do banco. (Q44)
- LGPD: o administrador pode anonimizar os dados pessoais de um projeto encerrado ou cancelado, inclusive no histórico, na lixeira e nos textos dos contatos. (Q59)

### Regras de negócio

- Toda parte interessada tem uma categoria da Figura 2-2, e o fornecedor contratado entra sozinho como parte interessada. (p. 9, 76 e 185; Q147, Q170)
- Cada linha da matriz RACI tem um único responsável pelo resultado (A) e pelo menos um executor (R). A linha incompleta aparece marcada, sem impedir a gravação. (p. 17 e 189; "um único A" é regra do PMO; Q117)
- O risco pode ser cadastrado só com o título, mas só passa a "em resposta" com probabilidade, impacto, estratégia e responsável. (p. 122, 125 e 185; Q166b)
- Projeto com ameaça ativa e orçamento sem reserva de contingência gera alerta, porque o orçamento deve incluir essa reserva. (p. 62; Q172a)
- O limite de variação e o limite de risco ficam no termo de abertura e, depois da aprovação, só mudam por mudança aprovada. (p. 113 e 122; Q177)
- Só o supervisor encerra, cancela ou reabre um projeto. O gerente do projeto prepara o encerramento, que passa por revisão obrigatória. (regra do PMO; Q29)

## Como rodar o protótipo

Precisa do Python 3.10 ou mais novo; os testes rodam no 3.10 e no 3.13. No Windows, o jeito mais fácil é instalar o Python 3.13 pela Microsoft Store.

**Jeito mais fácil:** dê dois cliques em `iniciar.bat` (Windows) ou rode `./iniciar.sh` (Linux e macOS). Na primeira vez, ele instala as dependências; depois, abre o navegador em http://localhost:5000. Para parar, feche a janela ou use `Ctrl+C`.

**Pelo terminal:**

```bash
git clone https://github.com/DennerRR/octante.git
cd octante
python -m pip install -r requirements.txt
python app.py
```

### Primeiros passos

1. No primeiro acesso, o app pede para criar o administrador.
2. O administrador cadastra os demais usuários na tela **Usuários**.
3. Crie um projeto, ou abra o **projeto de exemplo** pela página inicial. Pelo terminal, `python exemplo.py` também cria o exemplo.
4. Siga o guia do projeto, que mostra a próxima etapa a fazer.

### Dados e opções

- O banco é o arquivo SQLite `instance/gestor.db`. Para guardar uma cópia, o administrador usa o link **baixar backup** da página inicial. Para começar do zero, apague o arquivo com o app fechado.
- Ao atualizar o código, mantenha a pasta `instance/`: o app atualiza a estrutura do banco sozinho, sem perder os dados.
- Opções: `PORTA=5001` muda a porta; `SEM_NAVEGADOR=1` não abre o navegador; `NAVEGADOR=<caminho do .exe>` escolhe o navegador; `FLASK_DEBUG=1` liga o modo de depuração; `GESTOR_FUSO` troca o fuso horário, que por padrão é `America/Sao_Paulo`.
- Python da Microsoft Store: se, dentro de um ambiente virtual (`.venv`), o app disser `No module named 'flask'`, rode sem o `.venv` ou use os comandos acima.
- Para publicar na internet, siga o [DEPLOY.md](DEPLOY.md).

## Testes

```bash
python -m pip install pytest pytest-cov
python -m pytest
python -m pytest --cov=. --cov-branch
```

O último comando mostra a cobertura de linhas e de ramificações. A meta decidida é de 95% (Q77), e a CI ainda não cobra essa meta. Os testes rodam no GitHub Actions a cada envio e a cada pull request.

## Tecnologias e arquitetura

- **Python 3.10+ e Flask 3**, com as telas montadas no servidor (Jinja2) e CSS e JavaScript próprios, sem framework de front-end.
- **SQLite**, num único arquivo em `instance/`, com migrações versionadas em `db.py`. O histórico de alterações é gravado por gatilhos no próprio banco.
- **Gráficos em SVG** gerados em Python (`graficos.py`), sem bibliotecas externas, e **openpyxl** para exportar para Excel.
- **pytest** nos testes, rodando no GitHub Actions com Python 3.10 e 3.13.
- **PythonAnywhere** na hospedagem, pela entrada `wsgi.py`. Ela liga o modo de produção (`GESTOR_PRODUCAO=1`), em que o cookie de sessão só trafega por HTTPS.

O código é um monólito Flask, organizado em módulos por área do PMBOK, a maioria como Blueprint. Os nomes no código, nas telas e nos documentos estão em português.

### Estrutura do código

```
app.py           rotas principais (projetos, abertura, domínios)
rotas_partes.py  rotas das partes interessadas
partes.py        regras das partes interessadas
equipe.py        equipe, acordo de trabalho, RACI e saúde da equipe
ciclo.py         fases do ciclo de vida, tailoring e encerramento
medicao.py       medição, cronograma e orçamento
trabalho.py      questões, mudanças e lições aprendidas
entrega.py       escopo, backlog, aceite e qualidade
incerteza.py     riscos e outras incertezas
suprimentos.py   aquisições e recursos físicos
principios.py    princípios, business case, conformidade, mudança organizacional, decisões e premissas
metodos.py       MoSCoW, dependências e Gantt, burndown, Cynefin e Stacey, pré-mortem
pmo.py           portfólio, pendências, revisão, busca, agenda, exportação e modelos
guia.py          guia do projeto, glossário e ajuda de cada tela
dicas.py         exemplos e orientações de preenchimento
pmbok.py         conteúdo do PMBOK usado nas telas
graficos.py      gráficos em SVG
auth.py          login e usuários
auditoria.py     histórico de alterações e lixeira
backup.py        backups automáticos, verificação e restauração
dados.py         telas de histórico, lixeira, backups e LGPD
seguranca.py     CSRF, cabeçalhos de segurança e fuso horário
db.py            conexão SQLite e migrações
schema.sql       estrutura inicial do banco
util.py          funções compartilhadas
exemplo.py       cria o projeto de exemplo
wsgi.py          entrada para a hospedagem (ver DEPLOY.md)
templates/       telas (Jinja2)
static/          CSS, JavaScript e marca
tests/           testes automatizados (pytest)
```

## Limitações conhecidas

- As regras de negócio ainda são as do protótipo, porque as decisões da elicitação não foram implementadas.
- O bloqueio de tentativas de login fica na memória e zera quando o app reinicia. A contagem é por endereço IP, e no PythonAnywhere todos podem aparecer com o mesmo IP e ficar bloqueados juntos. A correção foi decidida nas Q186 e Q186b.
- Algumas garantias só existem no navegador: a confirmação de exclusão, o bloqueio de duplo envio, a marca de campo obrigatório e o aviso de alterações não salvas.
- Na tela estreita, o menu depende de JavaScript.
- O ajuste para o fuso de Brasília não tem efeito no Windows.

As decisões sobre os outros pontos estão nas Q198 (confirmação numa tela do servidor), Q200 e Q200b (o Octante não é feito para celular, mas a tela estreita continua para quem usa zoom no computador) e Q206 (o fuso vale também no Windows). Os defeitos abertos estão nas [issues com o rótulo bug](https://github.com/DennerRR/octante/issues?q=is%3Aissue+is%3Aopen+label%3Abug).

## Documentação

| Documento | O que tem |
|---|---|
| [Especificação de requisitos (ERS)](docs/requisitos/ERS.md) | O que o Octante deve fazer, requisito por requisito; rascunho, com a parte 1 de 4 |
| [Resumo para confirmação](docs/requisitos/resumo-para-confirmacao.md) | O que a elicitação decidiu, por área, com o número de cada pergunta |
| [Requisitos funcionais: regras e decisões](docs/requisitos/rf-regras-decisoes.md) | Cada requisito funcional do protótipo, as regras que aplica e as decisões que o mudam |
| [Registro de decisões](docs/requisitos/decisoes-elicitacao.md) | Cada pergunta da elicitação, a decisão e a origem |
| [Origem das regras](docs/requisitos/origem-das-regras.md) | A origem conferida de cada uma das 321 regras |
| [Regras do protótipo](docs/requisitos/inventario-regras-prototipo.md) | As regras de negócio como o protótipo faz hoje |
| [Requisitos do protótipo](docs/requisitos/inventario-requisitos-prototipo.md) | Os requisitos funcionais e não funcionais como estão hoje |
| [Glossário](GLOSSARY.md) | Os termos do domínio e os que se deve evitar |
| [ADRs](docs/adr/) | As decisões de arquitetura |
| [DEPLOY.md](DEPLOY.md) | Como publicar no PythonAnywhere |

As páginas citadas são da edição em inglês do PMBOK 7. O livro não fica no repositório, por direitos autorais.

## Como o trabalho é organizado

- As tarefas são [issues no GitHub](https://github.com/DennerRR/octante/issues).
- Cada issue tem a sua branch, criada a partir da `develop`, com o nome `<tipo>/<número-da-issue>-<descrição-curta>`, como `fix/1-gatilhos-da-auditoria`. Os tipos são `feature`, `fix`, `hotfix`, `docs`, `refactor`, `test` e `chore`.
- As mensagens de commit são em português, com o verbo no presente ("Corrige…", "Registra…"), e citam a issue.
- O trabalho entra na `develop` por pull request, e os testes rodam em cada um. A `main` guarda as versões publicadas.
- O projeto usa o Claude Code como assistente. As convenções para os agentes estão no [CLAUDE.md](CLAUDE.md) e em [docs/agents/](docs/agents/).

## Licença

[MIT](LICENSE): qualquer pessoa pode usar, copiar, modificar e distribuir o código, desde que mantenha o aviso de direitos autorais e o texto da licença. O software vem sem garantia. A licença vale para o conteúdo deste repositório; o PMBOK® Guide não faz parte dele.

## Autoria

Idealizado e conduzido por **Denner Ramiro Ribeiro**, responsável pelo produto. O código do protótipo foi gerado com o Claude (Anthropic).

PMBOK® é marca registrada do Project Management Institute, Inc. O Octante não tem vínculo com o PMI.
