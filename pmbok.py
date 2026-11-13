"""Conteúdo de referência do PMBOK Guide 7ª edição usado pelo aplicativo.

Textos traduzidos e resumidos livremente a partir do guia. Itens marcados com
`fonte_complementar` vêm de outras referências consolidadas e não do PMBOK 7.
"""

# --------------------------------------------------------------------------
# 12 princípios (The Standard for Project Management, seção 3)
# --------------------------------------------------------------------------
PRINCIPIOS = [
    ("Administração (stewardship)", "Seja um administrador diligente, respeitoso e cuidadoso: integridade, cuidado, confiabilidade e conformidade."),
    ("Equipe", "Crie um ambiente colaborativo para a equipe do projeto."),
    ("Partes interessadas", "Envolva-se efetivamente com as partes interessadas."),
    ("Valor", "Foque no valor."),
    ("Pensamento sistêmico", "Reconheça, avalie e responda às interações do sistema."),
    ("Liderança", "Demonstre comportamentos de liderança."),
    ("Tailoring", "Faça o tailoring (adaptação) com base no contexto."),
    ("Qualidade", "Incorpore a qualidade nos processos e nas entregas."),
    ("Complexidade", "Navegue pela complexidade."),
    ("Risco", "Otimize as respostas aos riscos."),
    ("Adaptabilidade e resiliência", "Adote a adaptabilidade e a resiliência."),
    ("Mudança", "Habilite a mudança para alcançar o estado futuro previsto."),
]

# --------------------------------------------------------------------------
# 8 domínios de desempenho e suas tabelas de "Verificação de resultados"
# (Tabelas 2-2, 2-3, 2-5, 2-6, 2-7, 2-8, 2-9 e 2-10)
# Cada resultado: (resultado desejado, como verificar)
# --------------------------------------------------------------------------
DOMINIOS = [
    {
        "chave": "partes-interessadas",
        "nome": "Partes Interessadas",
        "secao": "2.1",
        "tabela": "2-2",
        "resumo": "Atividades e funções associadas às partes interessadas: trabalhar com elas para manter o alinhamento e engajá-las para promover relações positivas e satisfação.",
        "modulo": "partes",
        "resultados": [
            ("Relacionamento de trabalho produtivo com as partes interessadas ao longo do projeto.",
             "Relações produtivas podem ser observadas; o movimento das partes interessadas ao longo de um contínuo de engajamento indica o nível relativo de satisfação."),
            ("Concordância das partes interessadas com os objetivos do projeto.",
             "Um número elevado de mudanças nos requisitos e no escopo pode indicar que as partes interessadas não estão engajadas ou alinhadas aos objetivos."),
            ("Beneficiários apoiam e estão satisfeitos; quem se opõe ao projeto não impacta negativamente os resultados.",
             "O comportamento das partes interessadas, pesquisas, entrevistas e grupos focais indicam apoio ou oposição. Revisar os registros de questões e de riscos ajuda a identificar desafios com partes interessadas específicas."),
        ],
    },
    {
        "chave": "equipe",
        "nome": "Equipe",
        "secao": "2.2",
        "tabela": "2-3",
        "resumo": "Atividades e funções associadas às pessoas responsáveis por produzir as entregas que realizam os resultados do negócio.",
        "modulo": "equipe",
        "resultados": [
            ("Propriedade compartilhada.",
             "Todos conhecem a visão e os objetivos; a equipe é dona das entregas e dos resultados do projeto."),
            ("Equipe de alto desempenho.",
             "Os membros confiam uns nos outros e colaboram, se adaptam a mudanças, são resilientes e se sentem empoderados e reconhecidos."),
            ("Habilidades de liderança e interpessoais demonstradas por todos os membros.",
             "Os membros aplicam pensamento crítico e habilidades interpessoais; os estilos de liderança são adequados ao contexto do projeto."),
        ],
    },
    {
        "chave": "abordagem",
        "nome": "Abordagem de Desenvolvimento e Ciclo de Vida",
        "secao": "2.3",
        "tabela": "2-5",
        "resumo": "Estabelecer a abordagem de desenvolvimento, a cadência de entrega e o ciclo de vida necessários para otimizar os resultados do projeto.",
        "modulo": "abordagem",
        "resultados": [
            ("Abordagens de desenvolvimento consistentes com as entregas do projeto.",
             "A abordagem (preditiva, híbrida ou adaptativa) reflete as variáveis do produto e é adequada às variáveis do projeto e da organização."),
            ("Ciclo de vida com fases que conectam a entrega de valor ao negócio e às partes interessadas do início ao fim.",
             "O trabalho, do lançamento ao encerramento, está representado nas fases, e as fases têm critérios de saída adequados."),
            ("Fases do ciclo de vida que facilitam a cadência de entrega e a abordagem necessárias.",
             "A cadência de desenvolvimento, teste e implantação está representada nas fases; entregas com cadências diferentes aparecem como fases sobrepostas ou repetidas."),
        ],
    },
    {
        "chave": "planejamento",
        "nome": "Planejamento",
        "secao": "2.4",
        "tabela": "2-6",
        "resumo": "Organizar, elaborar e coordenar o trabalho do projeto ao longo de todo o projeto.",
        "modulo": "abertura",
        "resultados": [
            ("O projeto progride de forma organizada, coordenada e deliberada.",
             "A comparação dos resultados com as linhas de base e outras métricas mostra que o projeto avança como planejado, com variações dentro dos limites."),
            ("Há uma abordagem holística para entregar os resultados do projeto.",
             "Cronograma de entrega, financiamento, disponibilidade de recursos e aquisições estão planejados de forma integrada, sem lacunas ou desalinhamentos."),
            ("Informações em evolução são elaboradas para produzir as entregas e os resultados.",
             "Comparar as informações iniciais com as atuais mostra elaboração adequada; comparar com o business case indica que o projeto produzirá o que motivou sua criação."),
            ("O tempo gasto planejando é adequado à situação.",
             "Planos e documentos mostram que o nível de planejamento é apropriado ao projeto."),
            ("As informações de planejamento são suficientes para gerenciar as expectativas das partes interessadas.",
             "O plano de comunicações e as informações das partes interessadas indicam comunicação suficiente para gerenciar expectativas."),
            ("Há um processo para adaptar os planos conforme necessidades e condições mudam.",
             "Projetos com backlog mostram a adaptação dos planos ao longo do projeto."),
        ],
    },
    {
        "chave": "trabalho",
        "nome": "Trabalho do Projeto",
        "secao": "2.5",
        "tabela": "2-7",
        "resumo": "Estabelecer os processos e executar o trabalho que permite à equipe produzir as entregas e os resultados esperados.",
        "modulo": "trabalho",
        "resultados": [
            ("Desempenho eficiente e eficaz do projeto.",
             "Os relatórios de status mostram que o trabalho é eficiente e eficaz."),
            ("Processos adequados ao projeto e ao ambiente.",
             "Há evidências de tailoring dos processos; auditorias e garantia da qualidade mostram que os processos são relevantes e usados de forma eficaz."),
            ("Comunicação e engajamento apropriados com as partes interessadas.",
             "Os artefatos de comunicação mostram que o planejado está sendo entregue; há poucos pedidos ad hoc de informação ou mal-entendidos."),
            ("Gestão eficiente dos recursos físicos.",
             "A quantidade de material usado, descarte e retrabalho indica uso eficiente dos recursos."),
            ("Gestão eficaz das aquisições.",
             "Uma auditoria de aquisições mostra que os processos foram suficientes e que o fornecedor cumpre o planejado."),
            ("Tratamento eficaz das mudanças.",
             "Preditivo: o registro de mudanças mostra avaliação holística (escopo, cronograma, custo, recursos, partes interessadas, riscos). Adaptativo: o backlog mostra o ritmo de conclusão e de inclusão de escopo."),
            ("Capacidade aprimorada por aprendizado contínuo e melhoria de processos.",
             "Os relatórios da equipe mostram menos erros e retrabalho, com aumento da velocidade."),
        ],
    },
    {
        "chave": "entrega",
        "nome": "Entrega",
        "secao": "2.6",
        "tabela": "2-8",
        "resumo": "Entregar o escopo e a qualidade que o projeto foi criado para alcançar, gerando os resultados pretendidos.",
        "modulo": "entrega",
        "resultados": [
            ("Os projetos contribuem para os objetivos de negócio e o avanço da estratégia.",
             "Plano de negócio, plano estratégico e documentos de autorização mostram alinhamento entre entregas e objetivos."),
            ("Os projetos realizam os resultados que motivaram sua criação.",
             "O business case e seus dados indicam que o projeto continua no caminho para realizar os resultados pretendidos."),
            ("Os benefícios são realizados no prazo planejado.",
             "O plano de realização de benefícios, o business case e/ou o cronograma mostram métricas financeiras e entregas sendo cumpridas."),
            ("A equipe entende claramente os requisitos.",
             "No preditivo, pouca mudança nos requisitos iniciais reflete entendimento; quando os requisitos evoluem, o entendimento pleno pode vir mais tarde."),
            ("As partes interessadas aceitam e estão satisfeitas com as entregas.",
             "Entrevistas, observação e feedback de usuários finais indicam satisfação; reclamações e devoluções também servem de indicador."),
        ],
    },
    {
        "chave": "medicao",
        "nome": "Medição",
        "secao": "2.7",
        "tabela": "2-9",
        "resumo": "Avaliar o desempenho do projeto e implementar respostas adequadas para manter o desempenho ideal.",
        "modulo": "medicao",
        "resultados": [
            ("Entendimento confiável do status do projeto.",
             "Auditorias das medições e dos relatórios demonstram se os dados são confiáveis."),
            ("Dados acionáveis para apoiar a tomada de decisão.",
             "As medições indicam se o projeto está como esperado ou se há variações."),
            ("Ações oportunas e adequadas para manter o desempenho nos trilhos.",
             "Indicadores antecedentes e/ou o status atual levam a decisões e ações oportunas."),
            ("Metas atingidas e valor gerado com decisões baseadas em previsões confiáveis.",
             "Comparar previsões passadas com o desempenho atual e o realizado com o planejado mostra a probabilidade de alcançar o valor pretendido."),
        ],
    },
    {
        "chave": "incerteza",
        "nome": "Incerteza",
        "secao": "2.8",
        "tabela": "2-10",
        "resumo": "Atividades e funções associadas a riscos e incertezas: ambiguidade, complexidade, volatilidade e risco.",
        "modulo": "incerteza",
        "resultados": [
            ("Consciência do ambiente do projeto (técnico, social, político, de mercado e econômico).",
             "A equipe considera o ambiente ao avaliar incertezas, riscos e respostas."),
            ("Exploração e resposta proativas à incerteza.",
             "As respostas aos riscos estão alinhadas à priorização das restrições (orçamento, cronograma, desempenho)."),
            ("Consciência da interdependência de múltiplas variáveis no projeto.",
             "As ações para lidar com complexidade, ambiguidade e volatilidade são adequadas ao projeto."),
            ("Capacidade de antecipar ameaças e oportunidades e entender as consequências de questões.",
             "Os sistemas para identificar, registrar e responder a riscos são suficientemente robustos."),
            ("Entrega com pouco ou nenhum impacto negativo de eventos imprevistos.",
             "As datas de entrega são cumpridas e o desempenho do orçamento está dentro do limite de variação."),
            ("Oportunidades realizadas para melhorar desempenho e resultados.",
             "A equipe usa mecanismos estabelecidos para identificar e aproveitar oportunidades."),
            ("Reservas de custo e cronograma usadas de forma eficaz.",
             "A equipe previne ameaças de forma proativa, limitando o uso das reservas."),
        ],
    },
]

DOMINIOS_POR_CHAVE = {d["chave"]: d for d in DOMINIOS}

STATUS_VERIFICACAO = [
    ("nao_avaliado", "Não avaliado"),
    ("atendido", "Atendido"),
    ("parcial", "Parcial"),
    ("nao_atendido", "Não atendido"),
]

# --------------------------------------------------------------------------
# Abordagem de desenvolvimento (seção 2.3)
# --------------------------------------------------------------------------
ABORDAGENS = [
    ("preditiva", "Preditiva"),
    ("hibrida", "Híbrida"),
    ("adaptativa", "Adaptativa"),
]

# Cadência de entrega (seção 2.3.2)
CADENCIAS = [
    ("unica", "Entrega única (ao final do projeto)"),
    ("multiplas", "Múltiplas entregas"),
    ("periodica", "Entregas periódicas (ex.: releases mensais)"),
    ("continua", "Entrega contínua"),
]

# Fatores para seleção da abordagem (seção 2.3.4). Escala 1..5:
# 1 = favorece preditiva, 5 = favorece adaptativa.
FATORES_ABORDAGEM = [
    # (chave, categoria, nome, rótulo do lado preditivo, rótulo do lado adaptativo)
    ("inovacao", "Produto", "Grau de inovação",
     "Entrega conhecida, equipe já fez algo parecido", "Alta inovação ou equipe sem experiência"),
    ("requisitos", "Produto", "Certeza dos requisitos",
     "Requisitos bem conhecidos e fáceis de definir", "Requisitos incertos, voláteis ou complexos"),
    ("escopo", "Produto", "Estabilidade do escopo",
     "Escopo estável, pouca chance de mudar", "Muitas mudanças esperadas no escopo"),
    ("facilidade_mudanca", "Produto", "Facilidade de mudança",
     "Difícil incorporar mudanças na entrega", "A entrega se adapta facilmente a mudanças"),
    ("opcoes_entrega", "Produto", "Opções de entrega",
     "Só faz sentido entregar tudo de uma vez", "Pode ser desenvolvida/entregue em partes"),
    ("risco", "Produto", "Risco",
     "Alto risco que exige planejamento antecipado rigoroso", "Risco reduzido construindo de forma modular e aprendendo"),
    ("seguranca", "Produto", "Requisitos de segurança (safety)",
     "Requisitos de segurança rigorosos", "Sem requisitos de segurança críticos"),
    ("regulacao", "Produto", "Regulação",
     "Forte supervisão regulatória e documentação exigida", "Pouca ou nenhuma regulação"),
    ("stakeholders", "Projeto", "Envolvimento das partes interessadas",
     "Partes interessadas pouco disponíveis durante o projeto", "Envolvimento contínuo (ex.: product owner presente)"),
    ("prazo", "Projeto", "Restrições de cronograma",
     "Não há necessidade de entregar algo cedo", "Precisa entregar algo cedo, mesmo incompleto"),
    ("financiamento", "Projeto", "Disponibilidade de financiamento",
     "Financiamento garantido e estável", "Financiamento incerto (MVP com investimento mínimo)"),
    ("estrutura", "Organização", "Estrutura organizacional",
     "Muitos níveis, hierarquia rígida, burocracia", "Estrutura plana, equipes auto-organizadas"),
    ("cultura", "Organização", "Cultura",
     "Cultura de gerenciar e dirigir, medir contra linhas de base", "Cultura de autogestão da equipe"),
    ("capacidade", "Organização", "Capacidade organizacional",
     "Políticas e mentalidade alinhadas a métodos preditivos", "Executivos e políticas alinhados a métodos adaptativos"),
    ("equipe", "Organização", "Tamanho e localização da equipe",
     "Equipe grande e/ou majoritariamente remota", "Equipe de 7 ± 2 pessoas no mesmo espaço"),
]


def recomendar_abordagem(respostas):
    """Recebe {chave_fator: 1..5} e devolve (media, abordagem_sugerida, medias_por_categoria)."""
    valores = [v for v in respostas.values() if v]
    if not valores:
        return None, None, {}
    media = sum(valores) / len(valores)
    if media < 2.5:
        sugestao = "preditiva"
    elif media > 3.5:
        sugestao = "adaptativa"
    else:
        sugestao = "hibrida"
    por_cat = {}
    for chave, cat, *_ in FATORES_ABORDAGEM:
        if respostas.get(chave):
            por_cat.setdefault(cat, []).append(respostas[chave])
    medias_cat = {c: sum(v) / len(v) for c, v in por_cat.items()}
    return media, sugestao, medias_cat


# Sugestões de tailoring por abordagem, usadas nas telas de abertura e monitoramento.
TAILORING = {
    "preditiva": {
        "incerteza": "Com escopo relativamente estável, use reservas de cronograma e de orçamento para responder aos riscos (seção 2.8.6).",
        "abertura": "Na abordagem preditiva, o termo de abertura costuma ser formal e aprovado pelo patrocinador antes do planejamento detalhado. Preencha todos os campos e registre a aprovação.",
        "monitoramento": "Obtenha feedback em revisões de fase (stage gates), relatórios de status e reuniões de revisão do projeto.",
    },
    "hibrida": {
        "incerteza": "Use reservas para as partes preditivas e inclua respostas a riscos no backlog das partes adaptativas.",
        "abertura": "Na abordagem híbrida, combine um termo de abertura enxuto (autorização, objetivos, restrições) com uma visão de produto clara para orientar as partes adaptativas.",
        "monitoramento": "Combine revisões de fase para as partes preditivas com revisões de iteração e demonstrações para as partes adaptativas.",
    },
    "adaptativa": {
        "incerteza": "Ajuste os planos conforme o entendimento evolui e inclua ações de resposta a riscos no backlog (backlog ajustado ao risco); reservas podem compensar riscos que se concretizarem (seção 2.8.6).",
        "abertura": "Na abordagem adaptativa, a declaração de visão é o artefato central para alinhar a equipe; o termo de abertura pode ser leve, focado em autorização, objetivos e restrições.",
        "monitoramento": "Use revisões de iteração, demonstrações frequentes do produto e retrospectivas para medir a satisfação das partes interessadas.",
    },
}

# --------------------------------------------------------------------------
# Partes interessadas (seção 2.1)
# --------------------------------------------------------------------------
ETAPAS_ENGAJAMENTO = [
    ("identificar", "Identificar", "Identificação de alto nível no início e elaboração progressiva e contínua ao longo do projeto."),
    ("analisar", "Compreender e analisar", "Entender sentimentos, crenças e valores; analisar poder, impacto, atitude, expectativas, influência, proximidade e interesse."),
    ("priorizar", "Priorizar", "Focar o engajamento nas partes com mais poder e interesse e repriorizar conforme o cenário muda."),
    ("engajar", "Engajar", "Trabalhar de forma colaborativa: apresentar o projeto, levantar requisitos, gerenciar expectativas, resolver questões e negociar."),
    ("monitorar", "Monitorar", "Acompanhar mudanças nas partes interessadas e avaliar se a estratégia de engajamento é eficaz."),
]

# Exemplos de partes interessadas (Figura 2-2)
CATEGORIAS_PARTES = [
    "Gerente do projeto", "Equipe de gerenciamento do projeto", "Equipe do projeto",
    "Órgão de governança", "PMO", "Comitê diretor", "Patrocinador", "Fornecedor",
    "Cliente", "Usuário final", "Órgão regulador", "Outro",
]

ATITUDES = [
    ("apoiador", "Apoiador"),
    ("neutro", "Neutro"),
    ("opositor", "Opositor"),
    ("desconhecida", "Desconhecida"),
]

PROXIMIDADE = [
    ("direta", "Trabalha diretamente no projeto"),
    ("proxima", "Próxima (interage com frequência)"),
    ("distante", "Distante (impactada indiretamente)"),
]

# Níveis de engajamento da matriz de avaliação do engajamento.
# fonte_complementar: o PMBOK 7 cita a matriz (seção 4.6.6) mas os nomes dos
# níveis vêm do PMBOK 6ª ed. (seção 13.2.2.5).
NIVEIS_ENGAJAMENTO = [
    (1, "Desconhece"),
    (2, "Resistente"),
    (3, "Neutro"),
    (4, "Apoiador"),
    (5, "Lidera"),
]
NIVEIS_ENGAJAMENTO_DICT = dict(NIVEIS_ENGAJAMENTO)

# Métodos de comunicação (seção 2.1.1.4)
METODOS_COMUNICACAO = [
    ("push", "Push (enviada: e-mails, memorandos, relatórios)"),
    ("pull", "Pull (buscada: intranet, repositórios)"),
    ("interativa", "Interativa (conversas, reuniões, demos)"),
]
METODOS_COMUNICACAO_CURTO = {"push": "Push", "pull": "Pull", "interativa": "Interativa"}

# Tipos de comunicação (Tabela 2-1)
TIPOS_COMUNICACAO = [
    ("verbal_formal", "Verbal formal (apresentações, revisões, demos)"),
    ("verbal_informal", "Verbal informal (conversas, discussões ad hoc)"),
    ("escrita_formal", "Escrita formal (relatórios, documentos do projeto)"),
    ("escrita_informal", "Escrita informal (e-mail, mensagens, notas)"),
]
TIPOS_COMUNICACAO_CURTO = {
    "verbal_formal": "Verbal formal", "verbal_informal": "Verbal informal",
    "escrita_formal": "Escrita formal", "escrita_informal": "Escrita informal",
}

FREQUENCIAS = ["Diária", "Semanal", "Quinzenal", "Mensal", "Por marco/fase", "Por iteração", "Sob demanda"]


def classificar_salience(poder, legitimidade, urgencia):
    """Modelo de Saliência (seção 4.2.7.5), tipologia de Mitchell, Agle e Wood."""
    chave = (bool(poder), bool(legitimidade), bool(urgencia))
    tabela = {
        (True, True, True): ("Definitiva", "definitiva"),
        (True, True, False): ("Dominante", "expectante"),
        (True, False, True): ("Perigosa", "expectante"),
        (False, True, True): ("Dependente", "expectante"),
        (True, False, False): ("Adormecida", "latente"),
        (False, True, False): ("Discricionária", "latente"),
        (False, False, True): ("Exigente", "latente"),
        (False, False, False): ("Sem saliência", "nenhuma"),
    }
    return tabela[chave]


def quadrante_poder_interesse(poder, interesse):
    """Grade poder × interesse. Alto = 4 ou 5 na escala 1..5.

    fonte_complementar: os nomes dos quadrantes seguem a prática consolidada
    (grade de Mendelow); o PMBOK 7 orienta priorizar quem tem mais poder e interesse.
    """
    if poder is None or interesse is None:
        return None
    alto_p, alto_i = poder >= 4, interesse >= 4
    if alto_p and alto_i:
        return "Gerenciar de perto"
    if alto_p:
        return "Manter satisfeita"
    if alto_i:
        return "Manter informada"
    return "Monitorar"


ORDEM_QUADRANTE = {"Gerenciar de perto": 0, "Manter satisfeita": 1, "Manter informada": 2, "Monitorar": 3, None: 4}


# --------------------------------------------------------------------------
# Incerteza (seção 2.8)
# --------------------------------------------------------------------------
TIPOS_RISCO = [("ameaca", "Ameaça"), ("oportunidade", "Oportunidade")]

# Estratégias de resposta (2.8.5.1 e 2.8.5.2)
ESTRATEGIAS = {
    "ameaca": [
        ("evitar", "Evitar", "Agir para eliminar a ameaça ou proteger o projeto do seu impacto."),
        ("escalar", "Escalar", "A ameaça está fora do escopo do projeto ou a resposta excede a autoridade do gerente."),
        ("transferir", "Transferir", "Passar a responsabilidade e o impacto para um terceiro (ex.: seguro, contrato)."),
        ("mitigar", "Mitigar", "Reduzir a probabilidade e/ou o impacto. Agir cedo costuma ser mais eficaz."),
        ("aceitar", "Aceitar", "Reconhecer a ameaça sem ação proativa; ativamente, com plano de contingência, ou passivamente."),
    ],
    "oportunidade": [
        ("explorar", "Explorar", "Agir para garantir que a oportunidade aconteça."),
        ("escalar", "Escalar", "A oportunidade está fora do escopo do projeto ou a resposta excede a autoridade do gerente."),
        ("compartilhar", "Compartilhar", "Alocar a oportunidade a um terceiro mais capaz de capturar o benefício."),
        ("melhorar", "Melhorar", "Aumentar a probabilidade ou o impacto. Agir cedo costuma ser mais eficaz."),
        ("aceitar", "Aceitar", "Reconhecer a oportunidade sem ação proativa planejada."),
    ],
}
ESTRATEGIAS_NOME = {t: {k: n for k, n, _ in lst} for t, lst in ESTRATEGIAS.items()}

# Fontes: ambientes citados nos resultados do domínio (Tabela 2-10) + internas do projeto
FONTES_RISCO = [
    ("tecnico", "Técnico"), ("social", "Social"), ("politico", "Político"),
    ("mercado", "Mercado"), ("economico", "Econômico"), ("regulatorio", "Regulatório / legal"),
    ("organizacional", "Organizacional"), ("partes", "Partes interessadas"), ("equipe", "Equipe / recursos"),
]

STATUS_RISCO = [
    ("aberto", "Aberto"),
    ("em_resposta", "Resposta em execução"),
    ("ocorreu", "Ocorreu"),
    ("encerrado", "Encerrado"),
]
STATUS_RISCO_ATIVOS = ("aberto", "em_resposta")

# Escalas. A conversão de probabilidade para % é usada no cálculo do valor
# monetário esperado (EMV); os rótulos são uma convenção do app.
ESCALA_PROBABILIDADE = [(1, "Muito baixa", 0.1), (2, "Baixa", 0.3), (3, "Média", 0.5), (4, "Alta", 0.7), (5, "Muito alta", 0.9)]
ESCALA_IMPACTO = [(1, "Muito baixo"), (2, "Baixo"), (3, "Médio"), (4, "Alto"), (5, "Muito alto")]
PROB_PERCENTUAL = {n: p for n, _, p in ESCALA_PROBABILIDADE}

RISCO_GLOBAL = [("baixo", "Baixo"), ("medio", "Médio"), ("alto", "Alto")]
NIVEIS_RISCO_NOME = dict(RISCO_GLOBAL)


def nivel_risco(pontuacao, limite):
    """Classifica P×I pelo limite de risco do projeto (2.8.5: limites refletem o apetite a risco)."""
    if pontuacao is None:
        return None
    if pontuacao >= limite:
        return "alto"
    if pontuacao * 2 >= limite:
        return "medio"
    return "baixo"


# Naturezas de incerteza além do risco e respostas sugeridas pelo guia
NATUREZAS_INCERTEZA = [
    {
        "chave": "geral", "nome": "Incerteza geral", "secao": "2.8.1",
        "definicao": "Falta de entendimento sobre questões, eventos, caminhos ou soluções.",
        "respostas": [
            ("coletar_info", "Coletar informações", "Pesquisa, especialistas, análise de mercado (até o ponto em que o custo compensa)."),
            ("multiplos_resultados", "Preparar-se para múltiplos resultados", "Solução principal mais planos alternativos para os resultados possíveis."),
            ("set_based", "Design baseado em conjuntos", "Investigar várias alternativas cedo e descartar as menos eficazes."),
            ("resiliencia", "Incorporar resiliência", "Equipe e processos capazes de aprender e se adaptar rapidamente."),
        ],
    },
    {
        "chave": "ambiguidade", "nome": "Ambiguidade", "secao": "2.8.2",
        "definicao": "Falta de clareza: termos usados de formas diferentes (conceitual) ou vários resultados possíveis (situacional).",
        "respostas": [
            ("definicoes", "Definir regras e termos comuns", "Reduz a ambiguidade conceitual (ex.: o que significa “no prazo”)."),
            ("elaboracao_progressiva", "Elaboração progressiva", "Detalhar o plano à medida que surgem informações e estimativas melhores."),
            ("experimentos", "Experimentos", "Identificar relações de causa e efeito."),
            ("prototipos", "Protótipos", "Distinguir as relações entre variáveis diferentes."),
        ],
    },
    {
        "chave": "complexidade", "nome": "Complexidade", "secao": "2.8.3",
        "definicao": "Muitas influências interconectadas (comportamento humano, de sistemas, ambiguidade) tornam as previsões imprecisas.",
        "respostas": [
            ("desacoplamento", "Desacoplamento", "Separar partes do sistema para reduzir variáveis conectadas (baseado em sistemas)."),
            ("simulacao", "Simulação", "Usar cenários análogos para simular componentes (baseado em sistemas)."),
            ("diversidade", "Diversidade de perspectivas", "Brainstorming, processos tipo Delphi (reenquadramento)."),
            ("equilibrio", "Equilíbrio de dados", "Combinar indicadores antecedentes e de resultado (reenquadramento)."),
            ("iterar", "Iterar", "Construir de forma iterativa ou incremental e aprender a cada ciclo (processo)."),
            ("engajar", "Engajar", "Criar oportunidades de envolvimento das partes interessadas (processo)."),
            ("fail_safe", "À prova de falhas", "Redundância ou degradação controlada em elementos críticos (processo)."),
        ],
    },
    {
        "chave": "volatilidade", "nome": "Volatilidade", "secao": "2.8.4",
        "definicao": "Ambiente sujeito a mudanças rápidas e imprevisíveis, geralmente afetando custo e prazo.",
        "respostas": [
            ("alternativas", "Análise de alternativas", "Outra combinação de habilidades, resequenciar ou terceirizar o trabalho."),
            ("reserva", "Reserva", "Reserva de custo ou de cronograma para absorver a variação."),
        ],
    },
]
NATUREZAS_POR_CHAVE = {n["chave"]: n for n in NATUREZAS_INCERTEZA}
STATUS_INCERTEZA = [("aberta", "Aberta"), ("reduzida", "Reduzida"), ("resolvida", "Resolvida")]


# --------------------------------------------------------------------------
# Trabalho do Projeto (seção 2.5)
# --------------------------------------------------------------------------
PRIORIDADES = [("alta", "Alta"), ("media", "Média"), ("baixa", "Baixa")]
STATUS_QUESTAO = [("aberta", "Aberta"), ("em_andamento", "Em andamento"), ("resolvida", "Resolvida")]

STATUS_MUDANCA = [
    ("solicitada", "Solicitada"),
    ("em_analise", "Em análise"),
    ("aprovada", "Aprovada"),
    ("rejeitada", "Rejeitada"),
    ("implementada", "Implementada"),
]
STATUS_MUDANCA_PENDENTES = ("solicitada", "em_analise")

# Avaliação holística da mudança (Tabela 2-7: escopo, cronograma, orçamento,
# recursos, partes interessadas e riscos; 2.5.7: mudanças podem trazer novos riscos).
IMPACTOS_MUDANCA = [
    ("imp_escopo", "Escopo", "O que entra, sai ou muda nas entregas e no backlog?"),
    ("imp_cronograma", "Cronograma", "Efeito em marcos, sprints e data de entrega."),
    ("imp_custo", "Orçamento", "Custo adicional ou economia estimada."),
    ("imp_recursos", "Recursos", "Pessoas, habilidades, ferramentas e infraestrutura."),
    ("imp_partes", "Partes interessadas", "Quem é afetado e precisa ser comunicado?"),
    ("imp_riscos", "Riscos", "Novos riscos introduzidos ou riscos alterados pela mudança."),
]

TIPOS_LICAO = [("manter", "O que funcionou (manter)"), ("melhorar", "O que melhorar")]
ORIGENS_LICAO = [
    ("retrospectiva", "Retrospectiva"), ("revisao_fase", "Revisão de fase / marco"),
    ("questao", "Questão resolvida"), ("risco", "Risco"), ("mudanca", "Mudança"), ("outro", "Outro"),
]
# Conhecimento explícito x tácito (2.5.8.2)
TIPOS_CONHECIMENTO = [
    ("explicito", "Explícito (pode ser documentado: passos, regras, números)"),
    ("tacito", "Tácito (experiência; compartilhado conectando pessoas)"),
]
# Gestão do conhecimento (2.5.8.1): aprendizado do projeto, de outras equipes ou da organização
ALCANCES_LICAO = [("projeto", "Este projeto"), ("outras_equipes", "Outras equipes"), ("organizacao", "Toda a organização")]

TAILORING["preditiva"]["mudancas"] = "Na abordagem preditiva, só mudanças aprovadas entram na linha de base do escopo. O app exige a avaliação de todos os impactos antes da decisão."
TAILORING["hibrida"]["mudancas"] = "Na abordagem híbrida, use o controle formal para as partes preditivas; mudanças no escopo adaptativo podem ir direto para o backlog priorizado. O app exige a avaliação de todos os impactos antes da decisão."
TAILORING["adaptativa"]["mudancas"] = "Na abordagem adaptativa, trabalho novo normalmente entra no backlog e o product owner prioriza. Use este registro para mudanças que afetam orçamento, prazo ou acordos; se entrar mais trabalho do que sai, o projeto não termina."


# --------------------------------------------------------------------------
# Entrega (seção 2.6) e planejamento do escopo (2.4.2.1)
# --------------------------------------------------------------------------
# Decomposição do escopo (2.6.2.2): EAP no preditivo; épicos, funcionalidades e histórias no adaptativo.
TIPOS_ITEM = [
    ("epico", "Épico"),
    ("funcionalidade", "Funcionalidade"),
    ("historia", "História de usuário"),
    ("entregavel", "Entregável"),
    ("pacote", "Pacote de trabalho"),
    ("requisito", "Requisito"),
]
STATUS_ITEM = [
    ("a_fazer", "A fazer"),
    ("em_andamento", "Em andamento"),
    ("concluido", "Concluído"),
    ("aceito", "Aceito"),
    ("cancelado", "Cancelado"),
]
COLUNAS_QUADRO = ["a_fazer", "em_andamento", "concluido", "aceito"]
UNIDADES_ESTIMATIVA = [
    ("pontos", "Pontos de história (estimativa relativa)"),
    ("horas", "Horas (estimativa absoluta)"),
    ("dias", "Dias (estimativa absoluta)"),
]

# Requisitos bem documentados (2.6.2.1). "Completo" vale para o conjunto de requisitos, não para um item.
QUALIDADE_REQUISITO = [
    ("claro", "Claro", "Só há uma forma de interpretar."),
    ("conciso", "Conciso", "Dito com o mínimo de palavras."),
    ("verificavel", "Verificável", "Há critérios de aceite para verificar se foi atendido."),
    ("consistente", "Consistente", "Não contradiz outros requisitos."),
    ("rastreavel", "Rastreável", "Tem identificador único (o código do item)."),
]

# Custo da qualidade (2.6.3.1)
CUSTO_QUALIDADE = [
    ("prevencao", "Prevenção", "conformidade", "Evitar defeitos: especificações, planejamento e garantia da qualidade, treinamento."),
    ("avaliacao", "Avaliação", "conformidade", "Medir a conformidade: verificação, testes, auditorias, avaliação de fornecedores."),
    ("falha_interna", "Falha interna", "nao_conformidade", "Defeito encontrado antes de chegar ao cliente: retrabalho, desperdício, análise de falhas."),
    ("falha_externa", "Falha externa", "nao_conformidade", "Defeito encontrado pelo cliente: reparos, garantia, reclamações, devoluções, reputação."),
]
CUSTO_QUALIDADE_NOME = {k: n for k, n, *_ in CUSTO_QUALIDADE}
# Curva do custo da mudança de Boehm (Figura 2-22)
CUSTO_MUDANCA = [("Requisitos", "1x"), ("Design", "5x"), ("Construção", "20x"), ("Teste", "50x"), ("Produção", "150x")]

STATUS_BENEFICIO = [
    ("planejado", "Planejado"),
    ("parcial", "Parcialmente realizado"),
    ("realizado", "Realizado"),
    ("nao_realizado", "Não realizado"),
]

TAILORING["preditiva"]["entrega"] = "Na abordagem preditiva, decomponha o escopo em entregáveis e pacotes de trabalho (EAP), cada um com critérios de aceite, e defina a linha de base do escopo. Depois dela, itens novos devem vir de mudanças aprovadas."
TAILORING["hibrida"]["entrega"] = "Na abordagem híbrida, use entregáveis com linha de base para as partes preditivas e épicos, funcionalidades e histórias para as partes adaptativas."
TAILORING["adaptativa"]["entrega"] = "Na abordagem adaptativa, organize o backlog em épicos, funcionalidades e histórias, detalhe as histórias no último momento responsável e use a definição de pronto para decidir quando um item está concluído."


# --------------------------------------------------------------------------
# Medição (seção 2.7) e cronograma/orçamento (2.4.2.3, 2.4.2.4)
# --------------------------------------------------------------------------
TIPOS_INDICADOR = [
    ("antecedente", "Antecedente (prevê tendências; permite agir antes)"),
    ("resultado", "De resultado (mede o que já aconteceu)"),
]
# Categorias do que medir (2.7.2)
CATEGORIAS_METRICA = [
    ("entrega", "Entregas (defeitos, desempenho técnico)"),
    ("fluxo", "Fluxo de trabalho (WIP, lead time, cycle time)"),
    ("linha_base", "Desempenho em relação à linha de base (prazo e custo)"),
    ("recursos", "Recursos"),
    ("valor", "Valor de negócio"),
    ("partes", "Partes interessadas (satisfação, moral da equipe)"),
    ("previsao", "Previsões"),
]
DIRECOES_METRICA = [("maior", "Quanto maior, melhor"), ("menor", "Quanto menor, melhor")]
# Métricas eficazes: critérios SMART na formulação do guia (2.7.1.2)
SMART = [
    ("Específica", "Diz exatamente o que medir."),
    ("Significativa", "Ligada ao business case, às linhas de base ou aos requisitos."),
    ("Alcançável", "A meta é possível com as pessoas, a tecnologia e o ambiente."),
    ("Relevante", "Gera informação que permite agir."),
    ("Oportuna", "Informação recente; tendências ajudam mais que dados antigos."),
]
# Armadilhas de medição (2.7.4)
ARMADILHAS_MEDICAO = [
    ("Efeito Hawthorne", "Medir algo muda o comportamento. Medir só a quantidade de entregas incentiva volume, e não satisfação do cliente."),
    ("Métrica de vaidade", "Mostra dados, mas não ajuda a decidir (ex.: visualizações de página em vez de novos usuários)."),
    ("Desmoralização", "Metas inalcançáveis derrubam o moral da equipe."),
    ("Uso indevido", "Focar nas métricas menos importantes, no curto prazo ou em tarefas fáceis só para melhorar o indicador."),
    ("Viés de confirmação", "Tendemos a ver nos dados o que confirma o que já pensávamos."),
    ("Correlação não é causa", "Duas variáveis que andam juntas não significam que uma causa a outra."),
]
STATUS_SEMAFORO = {
    "ok": ("No rumo", "✓"),
    "atencao": ("Atenção", "!"),
    "critico": ("Crítico", "✕"),
    "sem_dados": ("Sem dados", "–"),
}
TAILORING["preditiva"]["cronograma"] = "Na abordagem preditiva, o cronograma vem de decompor o escopo em atividades, sequenciar, estimar e alocar. Informe datas e custos planejados por item: eles formam a linha de base usada no valor agregado."
TAILORING["hibrida"]["cronograma"] = "Na abordagem híbrida, use datas e custos planejados nas partes preditivas e iterações com backlog priorizado nas partes adaptativas."
TAILORING["adaptativa"]["cronograma"] = "Na abordagem adaptativa, o planejamento é incremental: um plano de release de alto nível e iterações (timeboxes) com o trabalho tirado do backlog priorizado. O detalhe das próximas releases fica para depois."
TAILORING["preditiva"]["medicao"] = "Na abordagem preditiva, acompanhe o desempenho em relação às linhas de base de prazo e custo (valor agregado: SPI, CPI e previsões)."
TAILORING["hibrida"]["medicao"] = "Na abordagem híbrida, combine valor agregado nas partes preditivas com velocidade e burnup nas partes adaptativas."
TAILORING["adaptativa"]["medicao"] = "Na abordagem adaptativa, use velocidade, burnup, lead time, cycle time e trabalho em andamento. As previsões de valor agregado são usadas principalmente em ambientes preditivos."


# --------------------------------------------------------------------------
# Equipe (seção 2.2)
# --------------------------------------------------------------------------
MODELOS_LIDERANCA = [
    ("centralizada", "Centralizada: a responsabilidade é de uma pessoa, como o gerente do projeto (2.2.1.1)"),
    ("distribuida", "Distribuída: compartilhada pela equipe, que pode se auto-organizar com um facilitador (2.2.1.2)"),
]
# Escada de Tuckman (seção 4.2.6.1)
ESTAGIOS_EQUIPE = [
    ("formacao", "Formação", "A equipe se reúne e os membros se conhecem: nomes, papéis, habilidades (ex.: reunião de kickoff)."),
    ("confronto", "Confronto", "Personalidades, forças e fraquezas aparecem; pode haver conflito enquanto descobrem como trabalhar juntos."),
    ("normatizacao", "Normatização", "A equipe passa a funcionar como um grupo; os problemas são resolvidos rápido."),
    ("desempenho", "Desempenho", "Equipe madura e eficiente, com sinergia e produto de alta qualidade."),
    ("dissolucao", "Dissolução", "O trabalho termina e a equipe se desfaz para outras atividades."),
]
DEDICACOES = [("integral", "Tempo integral"), ("parcial", "Tempo parcial")]
LOCAIS = [("presencial", "Presencial"), ("hibrido", "Híbrido"), ("remoto", "Remoto")]
# Fatores de motivação intrínseca (2.2.4.3)
MOTIVADORES = ["Realização", "Desafio", "Crença no trabalho", "Fazer diferença", "Autonomia", "Responsabilidade",
               "Crescimento pessoal", "Relacionamento", "Fazer parte de uma equipe"]
# Fatores de equipes de alto desempenho (2.2.3)
FATORES_ALTO_DESEMPENHO = [
    ("comunicacao", "Comunicação aberta", "Ambiente seguro para falar, debater ideias e resolver problemas."),
    ("entendimento", "Entendimento compartilhado", "O propósito do projeto e seus benefícios são conhecidos por todos."),
    ("propriedade", "Propriedade compartilhada", "Os membros se sentem donos dos resultados."),
    ("confianca", "Confiança", "Os membros confiam uns nos outros, no gerente e na organização."),
    ("colaboracao", "Colaboração", "Trabalham juntos em vez de em silos ou competindo."),
    ("adaptabilidade", "Adaptabilidade", "Adaptam a forma de trabalhar à situação."),
    ("resiliencia", "Resiliência", "Recuperam-se rápido de problemas e falhas."),
    ("empoderamento", "Empoderamento", "Decidem sobre a forma de trabalhar, sem microgerenciamento."),
    ("reconhecimento", "Reconhecimento", "O trabalho e o desempenho são reconhecidos."),
]
PAPEIS_RACI = [("R", "Responsável (executa)"), ("A", "Aprovador (presta contas)"), ("C", "Consultado"), ("I", "Informado")]

# --------------------------------------------------------------------------
# Ciclo de vida e fases (seção 2.3.5) e tailoring (Guia, seção 3)
# --------------------------------------------------------------------------
STATUS_FASE = [("nao_iniciada", "Não iniciada"), ("em_andamento", "Em andamento"), ("concluida", "Concluída")]
DECISOES_PORTAO = [
    ("seguir", "Seguir para a próxima fase"),
    ("seguir_com_ressalvas", "Seguir com ressalvas"),
    ("repetir", "Repetir ou estender a fase"),
    ("encerrar", "Encerrar o projeto"),
]
# Fases de exemplo: 2.3.5 (preditivo) e 2.3.6 (exemplo do centro comunitário, que mistura abordagens)
FASES_SUGERIDAS = {
    "preditiva": [
        ("Viabilidade", "Determinar se o business case é válido e se a organização tem capacidade de entregar o resultado.",
         "Business case aprovado\nTermo de abertura aprovado"),
        ("Design", "Planejamento e análise levam ao design da entrega.", "Requisitos documentados e aprovados\nLinha de base do escopo definida"),
        ("Construção", "Construção da entrega com garantia da qualidade integrada.", "Itens do escopo concluídos\nDefinição de pronto atendida"),
        ("Teste", "Revisão final da qualidade e inspeção antes da transição ou do aceite.", "Critérios de aceite verificados\nDefeitos críticos resolvidos"),
        ("Implantação", "Entregas em uso e atividades de transição para sustentação e realização dos benefícios.",
         "Entregas aceitas pelo cliente\nOperação treinada"),
        ("Encerramento", "Projeto encerrado, conhecimento arquivado, equipe liberada e contratos fechados.",
         "Lições aprendidas registradas\nContratos encerrados\nEquipe liberada"),
    ],
    "hibrida": [
        ("Início", "Roadmap, financiamento inicial, equipe, cronograma de marcos e estratégia de aquisições.",
         "Business case aprovado\nTermo de abertura autorizado\nRoadmap de alto nível definido"),
        ("Planejamento", "Detalhar o planejamento das partes preditivas e preparar o backlog das adaptativas.",
         "Linha de base das partes preditivas definida\nBacklog inicial priorizado"),
        ("Desenvolvimento", "Entregas com cadências diferentes, sobrepostas a teste e implantação.", "Entregas planejadas concluídas"),
        ("Teste", "Testes adequados a cada tipo de entrega.", "Critérios de aceite verificados"),
        ("Implantação", "Entregas colocadas em uso, de forma iterativa.", "Entregas aceitas e em uso"),
        ("Encerramento", "Liberar equipe, registrar lições e comparar o desempenho com as linhas de base.",
         "Lições aprendidas registradas\nBenefícios avaliados contra o business case"),
    ],
    "adaptativa": [
        ("Início", "Visão do produto, equipe e backlog inicial.", "Declaração de visão escrita\nBacklog inicial priorizado"),
        ("Iterações e releases", "Iterações com revisão do cliente ao fim de cada uma e repriorização do backlog.",
         "Itens de maior prioridade entregues\nPartes interessadas satisfeitas com as entregas"),
        ("Encerramento", "Encerrar quando os itens de maior prioridade forem entregues ou o valor restante não compensar.",
         "Lições aprendidas registradas\nEquipe liberada"),
    ],
}
# Atributos do tailoring para o projeto (3.4.3)
PERGUNTAS_TAILORING = [
    ("Produto", "criticidade", "Conformidade e criticidade", "Quanto rigor de processo e garantia da qualidade é adequado?"),
    ("Produto", "mercado", "Mercado", "O mercado é muito regulado, muda rápido ou evolui devagar?"),
    ("Produto", "tecnologia", "Tecnologia", "A tecnologia é estável ou muda rápido, com risco de obsolescência?"),
    ("Produto", "prazo", "Horizonte de tempo", "O projeto dura semanas, meses ou anos?"),
    ("Produto", "requisitos", "Estabilidade dos requisitos", "Qual a chance de mudanças nos requisitos principais?"),
    ("Produto", "seguranca", "Sigilo", "Há elementos confidenciais ou sigilosos?"),
    ("Produto", "incremental", "Entrega incremental", "É possível entregar aos poucos e receber feedback?"),
    ("Equipe", "tamanho", "Tamanho da equipe", "Quantas pessoas em tempo integral e parcial?"),
    ("Equipe", "geografia", "Localização", "A equipe trabalha no mesmo lugar ou está distribuída?"),
    ("Equipe", "experiencia", "Experiência", "A equipe tem experiência no setor, na organização e trabalhando junta?"),
    ("Equipe", "cliente", "Acesso ao cliente", "É viável obter feedback frequente do cliente?"),
    ("Cultura", "adesao", "Adesão", "Há aceitação e entusiasmo pela abordagem proposta?"),
    ("Cultura", "confianca", "Confiança", "Há confiança de que a equipe é capaz e comprometida?"),
    ("Cultura", "empoderamento", "Empoderamento", "A equipe é encorajada a definir seu ambiente, acordos e decisões?"),
    ("Cultura", "cultura_org", "Cultura organizacional", "Os valores da organização combinam com a abordagem do projeto?"),
]
TIPOS_DECISAO_TAILORING = [("adicionar", "Adicionar"), ("remover", "Remover"), ("ajustar", "Ajustar")]
SITUACOES_PROJETO = [("ativo", "Ativo"), ("encerrado", "Encerrado"), ("cancelado", "Cancelado")]


# --------------------------------------------------------------------------
# Princípios (The Standard for Project Management, seção 3) — v7
# --------------------------------------------------------------------------
# Áreas de responsabilidade do administrador (3.1): dentro e fora da organização
AREAS_CONFORMIDADE = [
    ("legal", "Legal e regulatória"),
    ("privacidade", "Privacidade e proteção de dados"),
    ("seguranca", "Segurança"),
    ("financeira", "Financeira (uso de recursos)"),
    ("etica", "Ética e conduta"),
    ("pessoas", "Pessoas (tratamento justo da equipe)"),
    ("ambiental", "Ambiental e sustentabilidade"),
    ("social", "Impacto social e na comunidade"),
]
STATUS_CONFORMIDADE = [("pendente", "Pendente"), ("em_andamento", "Em andamento"), ("atendido", "Atendido"), ("nao_aplicavel", "Não se aplica")]
STATUS_ADOCAO = [("nao_iniciado", "Não iniciado"), ("preparando", "Preparando"), ("em_transicao", "Em transição"), ("adotado", "Adotado")]
STATUS_PREMISSA = [("nao_validada", "Não validada"), ("validada", "Validada"), ("invalidada", "Invalidada")]
NIVEIS_PRINCIPIO = [("forte", "Forte"), ("parcial", "Parcial"), ("fraco", "Fraco")]


# --------------------------------------------------------------------------
# Aquisições (2.4.6, 2.5.6, 4.6.8) e recursos físicos (2.4.5, 2.5.5) — v8
# --------------------------------------------------------------------------
DECISOES_FAZER_COMPRAR = [("comprar", "Comprar de fora"), ("fazer", "Fazer internamente")]
DOCUMENTOS_LICITACAO = [
    ("", "Nenhum"),
    ("rfi", "RFI: pedido de informações (sondar o mercado)"),
    ("rfp", "RFP: pedido de proposta (escopo complexo, o fornecedor propõe a solução)"),
    ("rfq", "RFQ: pedido de cotação (o preço decide, solução pronta)"),
]
TIPOS_CONTRATO = [
    ("", "Ainda não definido"),
    ("preco_fixo", "Preço fixo (escopo bem definido)"),
    ("custo_reembolsavel", "Custo reembolsável (escopo incerto ou mutável)"),
    ("tempo_material", "Tempo e material (reforço de equipe, consultoria)"),
    ("idiq", "Entrega indefinida, quantidade indefinida (IDIQ)"),
    ("outro", "Outro acordo (SLA, MOU, pedido-base)"),
]
STATUS_AQUISICAO = [
    ("planejada", "Planejada"), ("em_licitacao", "Em licitação ou cotação"), ("contratada", "Contratada"),
    ("entregue", "Entregue"), ("encerrada", "Encerrada"), ("cancelada", "Cancelada"),
]
STATUS_AQUISICAO_ATIVOS = ("planejada", "em_licitacao", "contratada")
TIPOS_RECURSO = [
    ("material", "Material ou insumo"), ("equipamento", "Equipamento"), ("software", "Software ou licença"),
    ("ambiente", "Ambiente de testes ou infraestrutura"), ("outro", "Outro"),
]
STATUS_RECURSO = [
    ("planejado", "Planejado"), ("pedido", "Pedido feito"), ("recebido", "Recebido"),
    ("em_uso", "Em uso"), ("devolvido", "Devolvido ou descartado"),
]
STATUS_RECURSO_PENDENTES = ("planejado",)
