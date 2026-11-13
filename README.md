# Octante

Aplicação web local para gerenciar projetos seguindo o **PMBOK® Guide 7ª edição**: 12 princípios,
8 domínios de desempenho e *tailoring* da abordagem (preditiva, híbrida ou adaptativa).

Feito para quem está começando num PMO: cada tela explica o conceito do PMBOK que está sendo aplicado e mostra o
que falta preencher.

## Sobre o projeto

Idealizado e conduzido por **Denner Ramiro Ribeiro**, que atuou como dono do produto: definiu o público, os
requisitos e as regras de negócio, priorizou o que entrava em cada versão e validou cada entrega. A implementação
foi feita com o apoio do Claude (IA da Anthropic). O produto passou por 18 versões, com 149 testes automatizados
rodando no GitHub Actions.

## Publicar na internet

Veja **DEPLOY.md** (PythonAnywhere, grátis). O app pede login; o primeiro acesso cria o administrador.

## Como rodar

Requisitos: Python 3.10 ou superior (no Windows, o jeito mais fácil é instalar o **Python 3.13 pela Microsoft Store**).

**Jeito mais fácil:** dê dois cliques em **`iniciar.bat`** (Windows) ou rode `./iniciar.sh` (Linux/macOS). Na primeira vez ele instala
o Flask; depois abre o navegador em **http://localhost:5000** sozinho. Para parar, feche a janela preta (ou `Ctrl+C`).

Pelo terminal, se preferir:

```bash
cd gestor-pmbok7
python -m pip install -r requirements.txt
python app.py
```

> Python da Microsoft Store: se criar um ambiente virtual (`.venv`) e o app disser `No module named 'flask'`, rode sem o `.venv`
> (`deactivate`) ou use os comandos acima, que instalam no Python certo. Opções: `PORTA=5001` muda a porta; `SEM_NAVEGADOR=1` não abre o navegador; `NAVEGADOR=<caminho do .exe>` abre num navegador específico.

Para explorar com dados prontos, clique em **Ver projeto de exemplo** na página inicial (ou rode `python exemplo.py`): ele cria o projeto fictício *AgendaFácil*.

O banco é um arquivo SQLite em `instance/gestor.db`. Para fazer backup, use o link **Baixar uma cópia de segurança** no rodapé da página inicial (ou copie o arquivo com o app fechado). Para zerar tudo, apague-o.

**Atualizando de uma versão anterior:** substitua os arquivos do app e mantenha a pasta `instance/`. Ao iniciar, o app
atualiza a estrutura do banco automaticamente (migrações versionadas), sem perder os dados.

Para ativar o modo de depuração do Flask: `FLASK_DEBUG=1 python app.py` (no Windows: `set FLASK_DEBUG=1` antes).

## O que tem no app

| Domínio de desempenho | Módulo |
|---|---|
| 2.1 Partes interessadas | Ciclo completo da seção 2.1.1: **Identificar → Compreender e analisar → Priorizar → Engajar → Monitorar** |
| 2.2 Equipe | Membros, liderança, estágio de Tuckman, acordo de trabalho, matriz RACI, saúde da equipe |
| 2.3 Abordagem de desenvolvimento e ciclo de vida | Assistente com os 15 fatores da seção 2.3.4, escolha da abordagem e da cadência; fases com critérios de saída e revisão de fase; tailoring com diagnóstico da Tabela 3-1 |
| 2.4 Planejamento | Termo de abertura, declaração de visão, cronograma (iterações, datas) e orçamento (custos planejados e reais) |
| 2.5 Trabalho do projeto | Registro de questões, registro de mudanças com avaliação holística, lições aprendidas, consumo de reservas, **aquisições** (fazer ou comprar, fornecedor, contrato, avaliação) e **recursos físicos** (prazo de pedido, uso, desperdício, descarte) |
| 2.6 Entrega | Escopo e backlog, requisitos, definição de pronto, aceite, quadro de tarefas, linha de base do escopo, custo da qualidade, benefícios |
| 2.7 Medição | Semáforo, valor agregado, burnup, velocidade, fluxo, previsão de término, KPIs, plano de exceção, relatórios de status |
| 2.8 Incerteza | Registro de riscos, matrizes P×I, limites, reservas, EMV, revisões, risco global, ambiguidade, complexidade e volatilidade |
| Todos os domínios | Verificação de resultados com as tabelas 2-2 a 2-10 (status e evidência) e indicadores calculados pelo app |
| Encerramento | Checklist, comparação com o planejado, avaliação final; encerrar, cancelar ou reabrir |

| Princípio (seção 3) | Onde aparece no app |
|---|---|
| 1. Administração | **Conformidade e sustentabilidade** (legal, privacidade, segurança, financeira, ética, pessoas, ambiental, social), termo aprovado, uso das reservas |
| 2. Equipe | Acordo de trabalho, RACI, saúde da equipe, planos de desenvolvimento |
| 3. Partes interessadas | Ciclo completo de partes interessadas |
| 4. Valor | **Business case** (necessidade, justificativa, estratégia, alternativas, VPL, ROI, payback, revisão periódica), benefícios, valor dos itens |
| 5. Pensamento sistêmico | **Registro de decisões** com alternativas e efeitos em outras áreas, **premissas** validadas, avaliação holística de mudanças |
| 6. Liderança | Modelo de liderança, Tuckman, visão, regras de decisão, decisões com envolvidos |
| 7. Tailoring | Assistente de abordagem, tailoring e diagnóstico da Tabela 3-1 |
| 8. Qualidade | Definição de pronto, qualidade dos requisitos, custo da qualidade, aceite |
| 9. Complexidade | Ambiguidade, complexidade, volatilidade, premissas, entrega iterativa |
| 10. Riscos | Registro de riscos, oportunidades, reservas, apetite e risco global |
| 11. Adaptabilidade e resiliência | Plano de exceção, **lições aplicadas**, replanejamento, resiliência da equipe |
| 12. Mudança | **Mudança organizacional**: estados atual e futuro, grupos afetados, prontidão, ações, curva de adoção, saturação |

A página **Autoavaliação dos 12** calcula de 5 a 6 evidências por princípio a partir dos registros (forte ≥ 80%, parcial ≥ 50%, fraco)
e guarda a reflexão da equipe sobre cada um.

Detalhes do ciclo de partes interessadas:

- **Identificar**: registro com papel, organização, categoria (Figura 2-2), interna/externa e status ativo.
- **Compreender e analisar**: poder, interesse, influência, impacto, atitude, proximidade, crenças, expectativas e o Modelo de Saliência (seção 4.2.7.5).
- **Priorizar**: grade poder × interesse, ordem sugerida pela análise e ordem manual confirmada pela equipe.
- **Engajar**: matriz de avaliação do engajamento (atual × desejado) e plano de comunicação (push, pull ou interativa, com tipo formal/informal da Tabela 2-1 e frequência).
- **Monitorar**: registro de interações com feedback e satisfação, histórico de mudanças de nível, tendência de satisfação e alertas.

### Alertas automáticos

- Parte interessada com poder alto (4 ou 5) que se opõe ao projeto.
- Última satisfação registrada ≤ 2.
- Parte no quadrante "Gerenciar de perto" sem interação nos últimos 30 dias.
- Lacuna de 2 ou mais níveis entre o engajamento atual e o desejado.
- Abordagem não definida; termo não aprovado (preditiva); visão não escrita (adaptativa/híbrida).
- Ameaça acima do limite de risco sem estratégia, ou com aceitação passiva (sem plano de contingência).
- Oportunidade com pontuação alta sem estratégia; risco sem responsável; risco sem revisão dentro da cadência; risco que ocorreu.
- Risco global avaliado como alto; reserva de contingência menor que o EMV das ameaças.
- Reserva de contingência ou de gerenciamento usada acima do disponível.
- Questão com prazo vencido, sem responsável ou de prioridade alta sem prazo.
- Mudança aguardando decisão há mais de 7 dias; mudança aprovada ainda não comunicada; risco que ocorreu sem questão.
- Itens fora da linha de base sem mudança aprovada (scope creep); trabalho novo maior que o concluído em 30 dias; WIP acima do limite.
- Item em andamento sem critérios de aceite; item concluído há mais de 14 dias sem aceite; mudança aprovada ainda fora do escopo.
- Benefício com data prevista vencida; custo das falhas maior que o de prevenção e avaliação.
- Indicador além do limite; indicador antecedente piorando duas vezes seguidas; indicador sem medição há 30 dias; dimensão crítica sem plano de exceção.
- Equipe sem acordo de trabalho; linha da RACI sem aprovador ou executor; lacuna de habilidade sem plano; fator de alto desempenho com nota ≤ 2; equipe sem avaliação há 45 dias; equipe adaptativa com mais de 9 pessoas.
- Fase com término vencido; situações da Tabela 3-1 detectadas.
- Business case com VPL negativo; custo previsto acima do investimento; business case sem revisão há 90 dias.
- Requisito de conformidade com prazo vencido; premissa não validada no prazo.
- Grupo de alto impacto com prontidão baixa para a mudança; 4 ou mais grupos em transição ao mesmo tempo; princípios com pouca evidência.

## Referências complementares (não fazem parte do PMBOK 7)

Sinalizadas também na interface:

- Nomes dos níveis de engajamento (Desconhece, Resistente, Neutro, Apoiador, Lidera): PMBOK 6ª ed., 13.2.2.5.
- Nomes dos quadrantes da grade poder × interesse: grade de Mendelow.
- Nomes das 7 classes de saliência: Mitchell, Agle e Wood (1997), modelo citado pelo PMBOK 7.
- Modelo da declaração de visão: *elevator pitch* de Geoffrey Moore.
- Conversão da escala de probabilidade em percentuais (10% a 90%) para o cálculo do EMV: convenção do app.
- Siglas em português do valor agregado (VP, VA, CR, IDP, IDC, ENT, EPT, VNT, IDPT) e a regra 0/100 de valor agregado: prática consolidada do Standard for Earned Value Management, citado pelo guia.
- Nomes dos estágios de Tuckman em português (formação, confronto, normatização, desempenho, dissolução): tradução usual; o modelo está na seção 4.2.6.1 do guia.
- Escala de 1 a 5 para os fatores de alto desempenho e o limite de alerta em 2: convenção do app.
- Faixas do semáforo a partir do limite de variação (atenção abaixo de 1 − limite; crítico abaixo de 1 − 2×limite): convenção do app.

## Estrutura

```
app.py          rotas principais (projetos, abertura, partes interessadas, domínios)
dicas.py        exemplos e orientações de preenchimento de cada campo
suprimentos.py  aquisições e recursos físicos (Blueprint)
incerteza.py    módulo do domínio Incerteza (Blueprint)
trabalho.py     módulo do domínio Trabalho do Projeto (Blueprint)
entrega.py      módulo do domínio Entrega (Blueprint)
medicao.py      módulo do domínio Medição e do cronograma/orçamento (Blueprint)
equipe.py       módulo do domínio Equipe (Blueprint)
ciclo.py        fases do ciclo de vida, tailoring e encerramento (Blueprint)
principios.py   12 princípios: autoavaliação, business case, conformidade, mudança organizacional, decisões e premissas (Blueprint)
partes.py       regras do domínio Partes Interessadas
graficos.py     gráficos em SVG (linhas e colunas)
util.py         funções compartilhadas (conversões, formato de moeda)
pmbok.py        conteúdo do PMBOK 7: domínios, princípios, fatores, classificações
db.py           conexão SQLite e migrações versionadas
schema.sql      estrutura base (v1); mudanças novas entram como migrações em db.py
templates/      telas (Jinja2)
static/         CSS e JS
tests/          testes automatizados (pytest)
exemplo.py      cria um projeto de exemplo
auth.py         login e usuários
auditoria.py    histórico de alterações e lixeira
backup.py       backups automáticos, verificação e restauração
seguranca.py    CSRF, cabeçalhos de segurança, fuso horário
dados.py        telas de histórico, lixeira, backups e LGPD
pmo.py          portfólio, pendências, revisão, busca, agenda, exportação, modelos
metodos.py      MoSCoW, dependências e Gantt, burndown, Cynefin/Stacey, pré-mortem
rotas_partes.py rotas das partes interessadas
wsgi.py         entrada para hospedagem (ver DEPLOY.md)
guia.py         fluxo de 5 fases, glossário e ajuda de cada tela
iniciar.bat     atalho para abrir o app no Windows (iniciar.sh no Linux/macOS)
```

Testes: `pip install pytest` e depois `python -m pytest` (148 testes, incluindo a atualização de bancos criados por versões anteriores).

## Histórico de versões

A versão mais recente vem primeiro. O app foi construído em 14 iterações, cada uma com revisão técnica da anterior.

**v18**: o projeto de exemplo se apresenta como exemplo ("Exemplo: AgendaFácil", cenário fictício de uma clínica), o topo
mostra "PROJETO" antes do nome do projeto aberto, e a página inicial explica o que o Octante faz. Bancos antigos são renomeados sozinhos.

**v17**: o site adotou a paleta da marca. Topo roxo `#3A1D6E` com faixa laranja, ações em roxo `#5B33A8` (8,4:1 com texto
branco), fundo lilás claro. O laranja `#FF9A1F` é só destaque (indicador do menu, próximo passo), nunca texto. Gráficos em
roxo, laranja e ciano, validados para daltonismo. Os status (verde, âmbar, vermelho) não mudaram.

**v16**: cores da marca trocadas para roxo e laranja (escolhidas entre 6 paletas).

**v15** (marca)
- Novo nome: **Octante**. O octante é o instrumento de navegação que mede ângulos com 1/8 de círculo: o nome junta orientar
  o rumo do projeto, medir o desempenho e os 8 domínios do PMBOK 7.
- Logo em SVG (`static/marca/`): círculo dividido em 8 partes (domínios) com 12 marcas no aro (princípios) e um octante laranja
  deslocado para fora (o projeto avançando). Versões para fundo claro e escuro, símbolo e favicon. Cores (v16): roxo `#3A1D6E`,
  laranja `#FF9A1F`, lavanda `#6B5A88`. Nome desenhado com Poppins (licença OFL), convertido em contorno.

**v14** (PMO, estagiários e modelos do PMBOK)
- **Portfólio**: todos os projetos numa tabela com o semáforo de prazo, custo, escopo, riscos, partes e questões, do mais crítico ao mais tranquilo.
- **Acesso por projeto**: administrador vê tudo; os demais veem só os projetos em que foram incluídos (o criador entra sozinho).
- **Minhas pendências**: questões, riscos e itens em que a pessoa é responsável, em todos os projetos (o membro da equipe pode
  ser ligado ao usuário do app para reconhecer apelidos).
- **Revisão do PMO**: o estagiário envia termo, risco, mudança, item, questão ou relatório para revisão; o PMO aprova ou devolve com comentário.
- **Modelos de projeto** (Scrum, híbrido, preditivo) com abordagem, fases, definição de pronto e riscos típicos.
- **Nível de exigência** (essencial ou rigoroso) e **completude** de cada registro ("62% preenchido, falta: causa, efeito").
- **Agenda de prazos** do projeto, com exportação para o calendário (.ics). **Busca** em todos os projetos (tecla /).
  **Exportar para Excel** os registros de riscos, questões, mudanças, partes, backlog e lições (protegido contra injeção de fórmulas).
- Seção 4 do PMBOK: **MoSCoW**, **dependências e Gantt**, **burndown**, **Cynefin e Stacey** (complexidade) e **pré-mortem**.
- "**Ver exemplo preenchido**" em cada tela; rotas de partes interessadas separadas do `app.py`; testes automáticos no GitHub (`.github/workflows`).

**v13** (segurança dos dados)
- **Histórico de alterações** de todo registro (quem, quando, antes e depois), gravado por gatilhos no próprio banco.
- **Lixeira**: projeto ou registro excluído pode ser restaurado pelo administrador, inclusive com todos os registros ligados a ele.
- **Backups automáticos**: um por dia, outro antes de cada atualização do banco e outro antes de cada restauração. Cada cópia
  é verificada (integridade) e assinada (SHA-256). Restauração pela tela **Dados**, também a partir de arquivo enviado.
- **Validações dentro do banco** (probabilidade e impacto de 1 a 5, valores não negativos, datas coerentes) e índices em todas
  as chaves estrangeiras.
- **Segurança web**: token CSRF em todo formulário, cabeçalhos de segurança (CSP, anti-iframe, HSTS em produção), limite de
  tamanho, trocar a senha encerra as outras sessões, bloqueio de tentativas por conta e por máquina.
- **Fuso de Brasília** mesmo em servidor UTC. **LGPD**: anonimizar os dados pessoais de projetos encerrados.

**v12** (revisão de regras, usabilidade e novo design: detalhes em **AVALIACAO.md**)
- 9 regras de negócio corrigidas, entre elas: projeto encerrado só para consulta, aprovação do termo exige quem aprovou, fluxo só
  conta o termo aprovado, mudanças aprovadas não podem ser excluídas, iterações sem sobreposição, partes interessadas sem duplicata
  e exclusão de projeto só pelo administrador.
- Avaliação pelas 10 heurísticas de Nielsen: confirmação em toda exclusão, campos obrigatórios marcados, aviso de alterações não
  salvas, botão "Aguarde…", erros anunciados e focados, "pular para o conteúdo", foco visível e menu recolhível no celular.
- Nova identidade visual: paleta azul-marinho e índigo com contraste AA em variáveis CSS, componentes padronizados e cores de
  gráfico validadas para daltonismo.

**v11** (publicação na internet)
- **Login obrigatório**: primeiro acesso cria o administrador; ele cadastra os usuários (ex.: estagiários), redefine senhas e
  desativa contas. Cada pessoa troca a própria senha. Senhas com hash (Werkzeug), mínimo de 8 caracteres, bloqueio de 5 minutos
  após 5 tentativas erradas, redirecionamento pós-login só para páginas do próprio app, sessão de 12 horas.
- Backup do banco só para administradores. Cookie de sessão `HttpOnly`, `SameSite=Lax` e `Secure` em produção.
- **`wsgi.py`** e **`DEPLOY.md`**: passo a passo para publicar grátis no PythonAnywhere.

**v10** (revisão como engenheiro de software e como gerente de projeto iniciante)
- Primeira abertura: botão **Ver projeto de exemplo** (sem terminal) e texto da página inicial alinhado ao fluxo de 5 fases.
- Projeto novo abre direto no **fluxo**; a visão geral mostra a trilha das 5 fases e um único **Próximo passo** com botão "Fazer agora".
  O guia de 8 passos (v8) foi substituído por esse, para não haver duas listas diferentes.
- Projeto recém-criado vê só o essencial: painéis de situação, domínios e princípios aparecem depois da fase Iniciar, e o alerta
  "princípios com pouca evidência" não aparece antes disso.
- **Modo essencial** no menu (padrão): Compras, Business case, Conformidade, Mudança organizacional, Decisões, Fases, Tailoring e
  Custo da qualidade ficam ocultos até clicar em "Mostrar todas as telas".
- Tela de abordagem com atalho "Primeira vez?" e link direto para a decisão. Menu do topo: "Princípios" virou "Sobre o PMBOK 7".
- Engenharia: **`iniciar.bat` / `iniciar.sh`** (instala o Flask e abre o navegador), aviso de porta em uso, **backup** consistente
  pelo navegador (API de backup do SQLite), dicas calculadas uma vez por tela (cache), imports organizados, correção visual dos
  selos de porcentagem dos princípios.

**v9**
- **Fluxo do projeto**: fluxograma em 5 fases (Iniciar, Planejar, Executar, Acompanhar, Encerrar) com o que já foi feito e o próximo passo.
- **Menu lateral na ordem do trabalho**, com nomes em linguagem simples (o nome do domínio PMBOK aparece em cada etapa do fluxo).
- **Glossário simples** e faixa "Para que serve / O que fazer" no topo de cada tela (some junto com o botão 💡 Dicas).

**v8**
- **Verificação completa contra o PMBOK 7**: nomes, tabelas e seções conferidos; duas referências de seção corrigidas e o texto de "Princípios" alinhado ao Standard (seção 3).
- Lacunas fechadas: **Aquisições e recursos físicos** (2.5.5, 2.5.6) com alertas, indicadores, fornecedor que vira parte interessada e checagem no encerramento; **plano de comunicação** (informação necessária e quem envia) nas partes interessadas.
- **Dicas de preenchimento**: cada campo mostra um exemplo (AgendaFácil) e uma orientação curta; botão 💡 Dicas no topo liga/desliga.
- **Telas mais simples**: guia "Por onde começar" na visão geral (8 passos, com o próximo destacado) e link para Aquisições no domínio Trabalho.

**v7**
- Cobertura dos **12 princípios** integrada aos módulos existentes (novo grupo "Princípios" no menu lateral):
  - **Autoavaliação dos 12**: evidências calculadas para cada princípio, com link para o que falta, gráfico e reflexão da equipe;
  - **Business case e valor** (princípio 4): VPL, ROI, payback, gráfico do valor presente acumulado e comparação com o custo previsto;
  - **Conformidade e sustentabilidade** (princípio 1): requisitos por área, prazo, responsável e evidência obrigatória para marcar como atendido;
  - **Mudança organizacional** (princípio 12): estados atual e futuro, grupos afetados ligados às partes interessadas, prontidão, metas e curva de adoção;
  - **Decisões e premissas** (princípios 5, 6 e 9): registro de decisões com alternativas, envolvidos e efeitos; premissas com prazo de validação.
- Lições aprendidas podem ser marcadas como **aplicadas** (princípio 11).
- Visão geral mostra o nível de evidência de cada princípio; encerramento verifica conformidade e adoção.
- Gráfico de linhas aceita valores negativos; `exemplo.py` virou função reutilizável (`criar(app)`).

**v6**
- Novo módulo do domínio **Equipe** (seção 2.2):
  - membros com papel, dedicação, local, habilidades, lacunas, plano de desenvolvimento e motivador principal;
  - modelo de gestão (centralizada ou distribuída) e estágio da equipe na escada de Tuckman;
  - **acordo de trabalho** (team charter): valores, comunicação, decisões, conflitos e reuniões;
  - **matriz RACI** que exige exatamente um aprovador (A) e pelo menos um executor (R) por linha;
  - **saúde da equipe**: avaliação periódica dos 9 fatores de equipes de alto desempenho, com histórico e gráfico.
- **Ciclo de vida** (2.3.5): fases com critérios de saída e **revisão de fase**. Concluir uma fase exige todos os critérios atendidos e uma decisão registrada; há fases sugeridas para cada abordagem.
- **Tailoring** (seção 3):
  - perguntas sobre produto, equipe e cultura;
  - registro do que foi adicionado, removido ou ajustado;
  - **diagnóstico da Tabela 3-1** a partir dos dados do app, como esperas longas por aprovação, WIP alto, falhas de qualidade e partes interessadas insatisfeitas.
- **Encerramento**: checklist automático (entregas, mudanças, questões, riscos, benefícios, lições, fases, equipe), itens manuais (contratos, arquivo, transição, revisão do business case), comparação com o planejado e avaliação final. O projeto pode ser encerrado, cancelado (com justificativa) ou reaberto.
- Revisão técnica da v5: gráficos de colunas passaram a mostrar todos os rótulos (quebrando em duas linhas) e a aceitar escala fixa.

**v5**
- **Cronograma e orçamento** (Planejamento, 2.4.2.3 e 2.4.2.4): datas do projeto, iterações com meta e capacidade, e por item a iteração, as datas planejadas e os custos planejado e real.
- Novo módulo do domínio **Medição** (seção 2.7):
  - **semáforo** por dimensão (prazo, custo, escopo, riscos, partes interessadas e questões), com ícone e rótulo além da cor;
  - **valor agregado**: VP, VA, CR, variações, IDP, IDC, ENT, EPT, VNT e IDPT, usando os valores da linha de base quando houver, e a curva VP/VA/CR;
  - **burnup**, **velocidade por iteração**, lead time, cycle time, WIP, vazão e **previsão de término** pela velocidade ou pela vazão;
  - **indicadores (KPIs)** antecedentes e de resultado, com meta, limite, histórico e tendência, além dos critérios SMART e das armadilhas de medição;
  - **limite de variação e plano de exceção**, com alerta quando algo fica crítico sem plano;
  - **relatórios de status** que congelam a situação do dia, com sugestões de realizações e próximos passos, prontos para imprimir ou salvar em PDF.
- Gráficos em SVG gerados no próprio app (sem bibliotecas externas), com legenda, rótulos finais e tabela com os dados.
- Revisão técnica da v4: regras de partes interessadas foram para `partes.py`, e os pontos de atenção de todos os domínios passaram a ser reunidos em uma única função (`alertas_do_projeto`).

**v4**
- Novo módulo do domínio **Entrega** (seção 2.6) e do planejamento do escopo (2.4.2.1):
  - **escopo e backlog** em árvore (épicos, funcionalidades, histórias, entregáveis, pacotes de trabalho), com código rastreável, valor de negócio, estimativa e ordem de prioridade;
  - verificação de **requisito bem documentado** (claro, conciso, verificável, consistente, rastreável) por item;
  - **definição de pronto** do projeto: concluir um item exige confirmar que ele a atende;
  - **aceite**: só com critérios de aceite e o nome de quem aceitou;
  - **quadro de tarefas** com limite de trabalho em andamento (WIP);
  - **linha de base do escopo** versionada; refazer exige motivo;
  - detecção de *scope creep* (itens depois da linha de base sem mudança aprovada, nas abordagens preditiva e híbrida) e de backlog que cresce mais rápido do que é concluído (adaptativa);
  - **custo da qualidade** em 4 categorias (prevenção, avaliação, falha interna, falha externa), com defeitos resolvidos;
  - **benefícios** esperados com medida, meta, data prevista e resultado.
- Integrações: mudança aprovada e resposta a risco viram itens do backlog (backlog ajustado ao risco), com aviso quando uma mudança aprovada ainda não foi incorporada ao escopo.
- Revisão técnica da v3: testes passaram a usar apoio compartilhado (`tests/conftest.py`, `tests/ajuda.py`) e deixaram de fixar o número da versão do banco.

**v3**
- Novo módulo do domínio **Trabalho do Projeto** (seção 2.5):
  - **registro de questões** com prioridade, responsável, prazo e resolução obrigatória ao fechar;
  - risco que **ocorre** abre automaticamente uma questão com o plano de contingência, uma única vez;
  - **consumo de reservas**: questões ligadas a riscos usam a contingência e eventos não previstos usam a reserva de gerenciamento, com alerta quando o uso passa do reservado;
  - **registro de mudanças** com fluxo solicitada → em análise → aprovada/rejeitada → implementada;
  - avaliação holística em 6 dimensões (escopo, cronograma, orçamento, recursos, partes interessadas e riscos), obrigatória antes da decisão nas abordagens preditiva e híbrida (*tailoring*);
  - registro de quem decidiu e de quando a mudança foi comunicada às partes interessadas (2.5.7);
  - **lições aprendidas** com tipo (manter/melhorar), conhecimento explícito ou tácito (2.5.8.2), alcance (projeto, outras equipes ou organização) e ligação com a questão de origem;
  - painel do domínio com tempo médio de resolução e pontos de atenção (questão atrasada, mudança parada há mais de 7 dias, mudança aprovada não comunicada).
- Integrações:
  - termo de abertura aprovado aponta para o registro de mudanças;
  - mudanças por parte interessada aparecem como evidência no domínio de Partes Interessadas (Tabela 2-2);
  - riscos mostram as questões abertas a partir deles.
- Revisão técnica da v2:
  - o filtro das listas disparava um aviso falso de "sair da página";
  - a reserva de contingência sumia do total quando o risco ocorria (agora só é liberada quando o risco é encerrado);
  - tipo de risco inválido na URL era aceito;
  - a barra "Salvar" fixa ficou mais legível.

**v2**
- Novo módulo do domínio **Incerteza** (seção 2.8):
  - registro de riscos com ameaças e oportunidades, causa, efeito, fonte, responsável e parte interessada relacionada;
  - probabilidade × impacto e matrizes separadas para ameaças e oportunidades;
  - limite de risco configurável e apetite a risco;
  - estratégias de resposta específicas de cada tipo (2.8.5.1 e 2.8.5.2), gatilho, plano de contingência, riscos secundários e residuais;
  - EMV, reservas de contingência por risco e reserva de gerenciamento do projeto (2.8.5.3);
  - revisões com histórico e cadência configurável (2.8.5.4);
  - avaliação do risco global do projeto;
  - registro de incertezas de ambiguidade, complexidade e volatilidade, com as respostas das seções 2.8.1 a 2.8.4.
- Integração: riscos aparecem na visão geral e nos pontos de atenção, e cada parte interessada mostra seus riscos relacionados.
- Revisão técnica da v1:
  - migrações versionadas do banco;
  - bloqueio de formulários enviados por outros sites (CSRF);
  - chave secreta gerada por instalação e depurador desligado por padrão;
  - interações com data futura rejeitadas;
  - aviso ao alterar um termo de abertura já aprovado;
  - valores em reais no formato brasileiro (`50.000` = cinquenta mil).

**v1**
- Partes interessadas (ciclo completo), abordagem de desenvolvimento, abertura e verificação de resultados dos 8 domínios.

## Possíveis evoluções

Os 8 domínios de desempenho e os 12 princípios já estão cobertos. Melhorias possíveis:
exportação dos registros para planilha, autenticação para uso por mais de uma pessoa e um portfólio com vários projetos lado a lado.
