PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS projeto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT DEFAULT '',
    abordagem TEXT,                 -- preditiva | hibrida | adaptativa
    abordagem_justificativa TEXT DEFAULT '',
    cadencia TEXT,                  -- unica | multiplas | periodica | continua
    fatores_json TEXT DEFAULT '{}', -- respostas do assistente de abordagem
    criado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    atualizado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- Termo de abertura + declaração de visão (artefatos de estratégia, seção 4.6.1)
CREATE TABLE IF NOT EXISTS abertura (
    projeto_id INTEGER PRIMARY KEY REFERENCES projeto(id) ON DELETE CASCADE,
    proposito TEXT DEFAULT '',
    objetivos TEXT DEFAULT '',
    criterios_sucesso TEXT DEFAULT '',
    requisitos_alto_nivel TEXT DEFAULT '',
    premissas TEXT DEFAULT '',
    restricoes TEXT DEFAULT '',
    riscos_alto_nivel TEXT DEFAULT '',
    marcos TEXT DEFAULT '',
    orcamento TEXT DEFAULT '',
    patrocinador TEXT DEFAULT '',
    gerente TEXT DEFAULT '',
    autoridade_gerente TEXT DEFAULT '',
    status TEXT DEFAULT 'rascunho',  -- rascunho | em_revisao | aprovado
    aprovado_por TEXT DEFAULT '',
    aprovado_em TEXT DEFAULT '',
    visao_publico TEXT DEFAULT '',
    visao_necessidade TEXT DEFAULT '',
    visao_produto TEXT DEFAULT '',
    visao_categoria TEXT DEFAULT '',
    visao_beneficio TEXT DEFAULT '',
    visao_alternativa TEXT DEFAULT '',
    visao_diferencial TEXT DEFAULT '',
    visao_texto TEXT DEFAULT '',
    atualizado_em TEXT
);

CREATE TABLE IF NOT EXISTS parte_interessada (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
    -- 1. Identificar
    nome TEXT NOT NULL,
    papel TEXT DEFAULT '',
    organizacao TEXT DEFAULT '',
    categoria TEXT DEFAULT '',
    interna INTEGER DEFAULT 1,
    contato TEXT DEFAULT '',
    ativa INTEGER DEFAULT 1,
    -- 2. Compreender e analisar
    poder INTEGER,          -- 1..5
    interesse INTEGER,      -- 1..5
    influencia INTEGER,     -- 1..5
    impacto INTEGER,        -- 1..5
    atitude TEXT DEFAULT 'desconhecida',
    proximidade TEXT DEFAULT '',
    crencas TEXT DEFAULT '',
    expectativas TEXT DEFAULT '',
    sal_poder INTEGER DEFAULT 0,
    sal_legitimidade INTEGER DEFAULT 0,
    sal_urgencia INTEGER DEFAULT 0,
    -- 3. Priorizar
    prioridade_manual INTEGER,  -- ordem definida pela equipe (opcional)
    -- 4. Engajar
    engajamento_atual INTEGER,     -- 1..5
    engajamento_desejado INTEGER,  -- 1..5
    metodo_comunicacao TEXT DEFAULT '',
    tipo_comunicacao TEXT DEFAULT '',
    frequencia TEXT DEFAULT '',
    estrategia TEXT DEFAULT '',
    criado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    atualizado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- 5. Monitorar: interações (registro de engajamento) e histórico do nível de engajamento
CREATE TABLE IF NOT EXISTS interacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parte_id INTEGER NOT NULL REFERENCES parte_interessada(id) ON DELETE CASCADE,
    data TEXT NOT NULL,
    metodo TEXT DEFAULT '',
    tipo TEXT DEFAULT '',
    resumo TEXT DEFAULT '',
    feedback TEXT DEFAULT '',
    satisfacao INTEGER      -- 1..5 (opcional)
);

CREATE TABLE IF NOT EXISTS historico_engajamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parte_id INTEGER NOT NULL REFERENCES parte_interessada(id) ON DELETE CASCADE,
    data TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    nivel_anterior INTEGER,
    nivel_novo INTEGER
);

-- Verificação de resultados por domínio (Tabelas 2-2 a 2-10)
CREATE TABLE IF NOT EXISTS verificacao (
    projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
    dominio TEXT NOT NULL,
    indice INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'nao_avaliado',
    evidencia TEXT DEFAULT '',
    atualizado_em TEXT,
    PRIMARY KEY (projeto_id, dominio, indice)
);
