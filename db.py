"""Acesso ao SQLite e migrações versionadas.

`schema.sql` é a linha de base (versão 1) e nunca deve ser alterado.
Mudanças de estrutura entram como novas migrações em MIGRACOES; a versão
aplicada fica em `PRAGMA user_version`, então bancos antigos são atualizados
sem perder dados ao abrir uma versão nova do app.
"""
import os
import sqlite3

from flask import current_app, g

MIGRACOES = {
    2: """
        -- v2: domínio de Incerteza
        ALTER TABLE projeto ADD COLUMN limite_risco INTEGER NOT NULL DEFAULT 12;
        ALTER TABLE projeto ADD COLUMN revisao_risco_dias INTEGER NOT NULL DEFAULT 14;
        ALTER TABLE projeto ADD COLUMN reserva_gerenciamento REAL;
        ALTER TABLE projeto ADD COLUMN risco_global TEXT DEFAULT '';
        ALTER TABLE projeto ADD COLUMN risco_global_notas TEXT DEFAULT '';
        ALTER TABLE projeto ADD COLUMN apetite_risco TEXT DEFAULT '';

        CREATE TABLE risco (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            codigo INTEGER NOT NULL,                 -- R-1, R-2... por projeto
            titulo TEXT NOT NULL,
            tipo TEXT NOT NULL DEFAULT 'ameaca',     -- ameaca | oportunidade
            causa TEXT DEFAULT '',
            efeito TEXT DEFAULT '',
            fonte TEXT DEFAULT '',
            probabilidade INTEGER,                   -- 1..5
            impacto INTEGER,                         -- 1..5
            impacto_custo REAL,                      -- R$ estimado se ocorrer (opcional)
            impacto_prazo_dias INTEGER,              -- dias estimados se ocorrer (opcional)
            responsavel TEXT DEFAULT '',
            parte_id INTEGER REFERENCES parte_interessada(id) ON DELETE SET NULL,
            estrategia TEXT DEFAULT '',
            plano_resposta TEXT DEFAULT '',
            gatilho TEXT DEFAULT '',
            plano_contingencia TEXT DEFAULT '',
            reserva_custo REAL,                      -- reserva de contingência (R$)
            reserva_prazo_dias INTEGER,              -- reserva de contingência (dias)
            riscos_secundarios TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'aberto',   -- aberto | em_resposta | ocorreu | encerrado
            identificado_em TEXT NOT NULL DEFAULT (date('now', 'localtime')),
            revisado_em TEXT,
            atualizado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );
        CREATE INDEX idx_risco_projeto ON risco(projeto_id);

        CREATE TABLE risco_revisao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            risco_id INTEGER NOT NULL REFERENCES risco(id) ON DELETE CASCADE,
            data TEXT NOT NULL,
            probabilidade INTEGER,
            impacto INTEGER,
            status TEXT,
            nota TEXT DEFAULT ''
        );

        CREATE TABLE incerteza (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            natureza TEXT NOT NULL,                  -- ambiguidade | complexidade | volatilidade | geral
            descricao TEXT NOT NULL,
            respostas TEXT DEFAULT '',               -- chaves separadas por vírgula
            acoes TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'aberta',   -- aberta | reduzida | resolvida
            criado_em TEXT NOT NULL DEFAULT (date('now', 'localtime')),
            atualizado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );
    """,
    3: """
        -- v3: domínio Trabalho do Projeto
        CREATE TABLE questao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            codigo INTEGER NOT NULL,                  -- Q-1, Q-2... por projeto
            titulo TEXT NOT NULL,
            descricao TEXT DEFAULT '',
            prioridade TEXT NOT NULL DEFAULT 'media', -- alta | media | baixa
            responsavel TEXT DEFAULT '',
            parte_id INTEGER REFERENCES parte_interessada(id) ON DELETE SET NULL,
            risco_id INTEGER REFERENCES risco(id) ON DELETE SET NULL,
            prazo TEXT,
            status TEXT NOT NULL DEFAULT 'aberta',    -- aberta | em_andamento | resolvida
            resolucao TEXT DEFAULT '',
            reserva_usada_custo REAL,
            reserva_usada_dias INTEGER,
            criado_em TEXT NOT NULL DEFAULT (date('now', 'localtime')),
            resolvido_em TEXT,
            atualizado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );
        CREATE INDEX idx_questao_projeto ON questao(projeto_id);

        CREATE TABLE mudanca (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            codigo INTEGER NOT NULL,                  -- M-1, M-2... por projeto
            titulo TEXT NOT NULL,
            descricao TEXT DEFAULT '',
            justificativa TEXT DEFAULT '',
            solicitante TEXT DEFAULT '',
            parte_id INTEGER REFERENCES parte_interessada(id) ON DELETE SET NULL,
            imp_escopo TEXT DEFAULT '',
            imp_cronograma TEXT DEFAULT '',
            imp_custo TEXT DEFAULT '',
            imp_recursos TEXT DEFAULT '',
            imp_partes TEXT DEFAULT '',
            imp_riscos TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'solicitada', -- solicitada | em_analise | aprovada | rejeitada | implementada
            decidido_por TEXT DEFAULT '',
            decidido_em TEXT,
            notas_decisao TEXT DEFAULT '',
            comunicada INTEGER NOT NULL DEFAULT 0,
            criado_em TEXT NOT NULL DEFAULT (date('now', 'localtime')),
            atualizado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );
        CREATE INDEX idx_mudanca_projeto ON mudanca(projeto_id);

        CREATE TABLE licao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            data TEXT NOT NULL,
            tipo TEXT NOT NULL DEFAULT 'manter',      -- manter | melhorar
            descricao TEXT NOT NULL,
            recomendacao TEXT DEFAULT '',
            origem TEXT DEFAULT '',
            dominio TEXT DEFAULT '',
            conhecimento TEXT DEFAULT 'explicito',    -- explicito | tacito
            alcance TEXT DEFAULT 'projeto',           -- projeto | outras_equipes | organizacao
            questao_id INTEGER REFERENCES questao(id) ON DELETE SET NULL,
            criado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );
    """,
    4: """
        -- v4: domínio Entrega e planejamento do escopo
        ALTER TABLE projeto ADD COLUMN definicao_pronto TEXT DEFAULT '';
        ALTER TABLE projeto ADD COLUMN unidade_estimativa TEXT DEFAULT 'pontos';
        ALTER TABLE projeto ADD COLUMN limite_wip INTEGER;

        CREATE TABLE item (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            codigo INTEGER NOT NULL,                  -- I-1, I-2... (requisito rastreável)
            pai_id INTEGER REFERENCES item(id) ON DELETE SET NULL,
            tipo TEXT NOT NULL DEFAULT 'historia',
            titulo TEXT NOT NULL,
            descricao TEXT DEFAULT '',
            criterios_aceite TEXT DEFAULT '',
            ordem INTEGER,
            valor INTEGER,                            -- valor de negócio 1..5
            estimativa REAL,
            q_claro INTEGER NOT NULL DEFAULT 0,
            q_conciso INTEGER NOT NULL DEFAULT 0,
            q_consistente INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'a_fazer',   -- a_fazer | em_andamento | concluido | aceito | cancelado
            dod_ok INTEGER NOT NULL DEFAULT 0,
            responsavel TEXT DEFAULT '',
            parte_id INTEGER REFERENCES parte_interessada(id) ON DELETE SET NULL,
            mudanca_id INTEGER REFERENCES mudanca(id) ON DELETE SET NULL,
            risco_id INTEGER REFERENCES risco(id) ON DELETE SET NULL,
            aceito_por TEXT DEFAULT '',
            criado_em TEXT NOT NULL DEFAULT (date('now', 'localtime')),
            iniciado_em TEXT,
            concluido_em TEXT,
            aceito_em TEXT,
            atualizado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );
        CREATE INDEX idx_item_projeto ON item(projeto_id);

        CREATE TABLE linha_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            criada_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            motivo TEXT DEFAULT '',
            dados_json TEXT NOT NULL DEFAULT '{}'
        );

        CREATE TABLE qualidade_custo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            data TEXT NOT NULL,
            categoria TEXT NOT NULL,                  -- prevencao | avaliacao | falha_interna | falha_externa
            descricao TEXT NOT NULL,
            custo REAL,
            item_id INTEGER REFERENCES item(id) ON DELETE SET NULL,
            resolvido INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE beneficio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            descricao TEXT NOT NULL,
            medida TEXT DEFAULT '',
            meta TEXT DEFAULT '',
            data_prevista TEXT,
            status TEXT NOT NULL DEFAULT 'planejado', -- planejado | parcial | realizado | nao_realizado
            resultado TEXT DEFAULT '',
            atualizado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );
    """,
    5: """
        -- v5: cronograma e orçamento (Planejamento) e domínio Medição
        CREATE TABLE iteracao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            nome TEXT NOT NULL,
            inicio TEXT NOT NULL,
            fim TEXT NOT NULL,
            meta TEXT DEFAULT '',
            capacidade REAL
        );
        ALTER TABLE item ADD COLUMN iteracao_id INTEGER REFERENCES iteracao(id) ON DELETE SET NULL;
        ALTER TABLE item ADD COLUMN inicio_planejado TEXT;
        ALTER TABLE item ADD COLUMN fim_planejado TEXT;
        ALTER TABLE item ADD COLUMN custo_planejado REAL;
        ALTER TABLE item ADD COLUMN custo_real REAL;
        ALTER TABLE projeto ADD COLUMN data_inicio TEXT;
        ALTER TABLE projeto ADD COLUMN data_fim_planejada TEXT;
        ALTER TABLE projeto ADD COLUMN limite_variacao INTEGER NOT NULL DEFAULT 10;
        ALTER TABLE projeto ADD COLUMN plano_excecao TEXT DEFAULT '';

        CREATE TABLE metrica (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL DEFAULT 'resultado',   -- antecedente | resultado
            categoria TEXT DEFAULT '',
            unidade TEXT DEFAULT '',
            direcao TEXT NOT NULL DEFAULT 'maior',    -- maior | menor (é melhor)
            meta REAL,
            limite REAL,
            relevancia TEXT DEFAULT '',
            criado_em TEXT NOT NULL DEFAULT (date('now', 'localtime'))
        );
        CREATE TABLE medicao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metrica_id INTEGER NOT NULL REFERENCES metrica(id) ON DELETE CASCADE,
            data TEXT NOT NULL,
            valor REAL NOT NULL,
            nota TEXT DEFAULT ''
        );
        CREATE TABLE relatorio_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            data TEXT NOT NULL,
            resumo TEXT DEFAULT '',
            realizacoes TEXT DEFAULT '',
            proximos_passos TEXT DEFAULT '',
            dados_json TEXT NOT NULL DEFAULT '{}',
            criado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );
    """,
    6: """
        -- v6: domínio Equipe, ciclo de vida (fases), tailoring e encerramento
        ALTER TABLE projeto ADD COLUMN modelo_lideranca TEXT DEFAULT '';
        ALTER TABLE projeto ADD COLUMN estagio_equipe TEXT DEFAULT '';
        ALTER TABLE projeto ADD COLUMN acordo_valores TEXT DEFAULT '';
        ALTER TABLE projeto ADD COLUMN acordo_comunicacao TEXT DEFAULT '';
        ALTER TABLE projeto ADD COLUMN acordo_decisoes TEXT DEFAULT '';
        ALTER TABLE projeto ADD COLUMN acordo_conflitos TEXT DEFAULT '';
        ALTER TABLE projeto ADD COLUMN acordo_reunioes TEXT DEFAULT '';
        ALTER TABLE projeto ADD COLUMN acordo_atualizado_em TEXT;
        ALTER TABLE projeto ADD COLUMN tailoring_json TEXT DEFAULT '{}';
        ALTER TABLE projeto ADD COLUMN situacao TEXT NOT NULL DEFAULT 'ativo';   -- ativo | encerrado | cancelado
        ALTER TABLE projeto ADD COLUMN encerrado_em TEXT;
        ALTER TABLE projeto ADD COLUMN encerramento_json TEXT DEFAULT '{}';

        CREATE TABLE membro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            nome TEXT NOT NULL,
            papel TEXT DEFAULT '',
            dedicacao TEXT DEFAULT 'integral',        -- integral | parcial
            local TEXT DEFAULT 'presencial',          -- presencial | remoto | hibrido
            habilidades TEXT DEFAULT '',
            lacunas TEXT DEFAULT '',
            plano_desenvolvimento TEXT DEFAULT '',
            motivador TEXT DEFAULT '',
            parte_id INTEGER REFERENCES parte_interessada(id) ON DELETE SET NULL,
            ativo INTEGER NOT NULL DEFAULT 1,
            liberado_em TEXT,
            criado_em TEXT NOT NULL DEFAULT (date('now', 'localtime'))
        );
        CREATE TABLE raci_linha (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            descricao TEXT NOT NULL,
            item_id INTEGER REFERENCES item(id) ON DELETE SET NULL,
            ordem INTEGER
        );
        CREATE TABLE raci_papel (
            linha_id INTEGER NOT NULL REFERENCES raci_linha(id) ON DELETE CASCADE,
            membro_id INTEGER NOT NULL REFERENCES membro(id) ON DELETE CASCADE,
            papel TEXT NOT NULL,                      -- R | A | C | I
            PRIMARY KEY (linha_id, membro_id)
        );
        CREATE TABLE avaliacao_equipe (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            data TEXT NOT NULL,
            notas_json TEXT NOT NULL DEFAULT '{}',
            participantes INTEGER,
            observacoes TEXT DEFAULT ''
        );
        CREATE TABLE fase (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            nome TEXT NOT NULL,
            ordem INTEGER NOT NULL DEFAULT 1,
            inicio TEXT,
            fim TEXT,
            objetivo TEXT DEFAULT '',
            criterios_saida TEXT DEFAULT '',
            criterios_ok TEXT NOT NULL DEFAULT '[]',
            status TEXT NOT NULL DEFAULT 'nao_iniciada', -- nao_iniciada | em_andamento | concluida
            revisao_data TEXT,
            revisao_decisao TEXT DEFAULT '',           -- seguir | seguir_com_ressalvas | repetir | encerrar
            revisao_por TEXT DEFAULT '',
            revisao_notas TEXT DEFAULT ''
        );
        CREATE TABLE decisao_tailoring (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            data TEXT NOT NULL,
            tipo TEXT NOT NULL,                        -- adicionar | remover | ajustar
            elemento TEXT NOT NULL,
            motivo TEXT DEFAULT '',
            origem TEXT DEFAULT ''
        );
    """,
    7: """
        -- v7: cobertura dos 12 princípios
        ALTER TABLE projeto ADD COLUMN bc_necessidade TEXT DEFAULT '';
        ALTER TABLE projeto ADD COLUMN bc_justificativa TEXT DEFAULT '';
        ALTER TABLE projeto ADD COLUMN bc_estrategia TEXT DEFAULT '';
        ALTER TABLE projeto ADD COLUMN bc_alternativas TEXT DEFAULT '';
        ALTER TABLE projeto ADD COLUMN bc_beneficios_nao_financeiros TEXT DEFAULT '';
        ALTER TABLE projeto ADD COLUMN bc_investimento REAL;
        ALTER TABLE projeto ADD COLUMN bc_beneficio_anual REAL;
        ALTER TABLE projeto ADD COLUMN bc_custo_anual REAL;
        ALTER TABLE projeto ADD COLUMN bc_horizonte_anos INTEGER;
        ALTER TABLE projeto ADD COLUMN bc_taxa REAL;
        ALTER TABLE projeto ADD COLUMN bc_revisado_em TEXT;
        ALTER TABLE projeto ADD COLUMN mudanca_estado_atual TEXT DEFAULT '';
        ALTER TABLE projeto ADD COLUMN mudanca_estado_futuro TEXT DEFAULT '';
        ALTER TABLE licao ADD COLUMN aplicada INTEGER NOT NULL DEFAULT 0;
        ALTER TABLE licao ADD COLUMN aplicada_em TEXT;

        CREATE TABLE conformidade (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            area TEXT NOT NULL,
            requisito TEXT NOT NULL,
            como_atender TEXT DEFAULT '',
            responsavel TEXT DEFAULT '',
            prazo TEXT,
            status TEXT NOT NULL DEFAULT 'pendente',  -- pendente | em_andamento | atendido | nao_aplicavel
            evidencia TEXT DEFAULT '',
            atualizado_em TEXT NOT NULL DEFAULT (date('now', 'localtime'))
        );
        CREATE TABLE adocao_grupo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            grupo TEXT NOT NULL,
            parte_id INTEGER REFERENCES parte_interessada(id) ON DELETE SET NULL,
            o_que_muda TEXT DEFAULT '',
            impacto INTEGER,                          -- 1..5
            prontidao INTEGER,                        -- 1..5
            resistencias TEXT DEFAULT '',
            acoes TEXT DEFAULT '',
            meta_adocao REAL,                         -- %
            status TEXT NOT NULL DEFAULT 'nao_iniciado'
        );
        CREATE TABLE adocao_medicao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grupo_id INTEGER NOT NULL REFERENCES adocao_grupo(id) ON DELETE CASCADE,
            data TEXT NOT NULL,
            adocao REAL NOT NULL,
            prontidao INTEGER,
            nota TEXT DEFAULT ''
        );
        CREATE TABLE decisao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            data TEXT NOT NULL,
            titulo TEXT NOT NULL,
            contexto TEXT DEFAULT '',
            alternativas TEXT DEFAULT '',
            decisao TEXT DEFAULT '',
            decidido_por TEXT DEFAULT '',
            envolvidos TEXT DEFAULT '',
            efeitos TEXT DEFAULT '',
            revisar_em TEXT
        );
        CREATE TABLE premissa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            descricao TEXT NOT NULL,
            se_falsa TEXT DEFAULT '',
            como_validar TEXT DEFAULT '',
            validar_ate TEXT,
            status TEXT NOT NULL DEFAULT 'nao_validada', -- nao_validada | validada | invalidada
            atualizado_em TEXT NOT NULL DEFAULT (date('now', 'localtime'))
        );
    """,
    8: """
        -- v8: plano de comunicação (2.4.4), aquisições (2.4.6, 2.5.6) e recursos físicos (2.4.5, 2.5.5)
        ALTER TABLE parte_interessada ADD COLUMN info_necessaria TEXT DEFAULT '';
        ALTER TABLE parte_interessada ADD COLUMN info_responsavel TEXT DEFAULT '';
        CREATE TABLE aquisicao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            codigo INTEGER NOT NULL,
            item TEXT NOT NULL,
            decisao TEXT NOT NULL DEFAULT 'comprar',
            fornecedor TEXT DEFAULT '',
            parte_id INTEGER REFERENCES parte_interessada(id) ON DELETE SET NULL,
            documento TEXT DEFAULT '',
            contrato TEXT DEFAULT '',
            valor REAL,
            necessario_em TEXT,
            entrega_prevista TEXT,
            status TEXT NOT NULL DEFAULT 'planejada',
            criterios TEXT DEFAULT '',
            nota_desempenho INTEGER,
            observacoes TEXT DEFAULT '',
            atualizado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );
        CREATE INDEX idx_aquisicao_projeto ON aquisicao(projeto_id);
        CREATE TABLE recurso_fisico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL DEFAULT 'equipamento',
            quantidade REAL,
            unidade TEXT DEFAULT '',
            usado REAL,
            desperdicio REAL,
            necessario_em TEXT,
            antecedencia_dias INTEGER,
            status TEXT NOT NULL DEFAULT 'planejado',
            armazenamento_descarte TEXT DEFAULT '',
            atualizado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );
        CREATE INDEX idx_recurso_projeto ON recurso_fisico(projeto_id);
    """,
    9: """
        -- v11: usuários e login (necessário para publicar o app na internet)
        CREATE TABLE usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            login TEXT NOT NULL UNIQUE COLLATE NOCASE,
            senha_hash TEXT NOT NULL,
            admin INTEGER NOT NULL DEFAULT 0,
            ativo INTEGER NOT NULL DEFAULT 1,
            criado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );
    """,
    10: """
        -- v13: segurança dos dados
        -- 1) Histórico de alterações (quem, quando, o quê), base da lixeira e da recuperação.
        CREATE TABLE auditoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quando TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            usuario_id INTEGER,
            usuario_nome TEXT DEFAULT '',
            lote TEXT DEFAULT '',
            acao TEXT NOT NULL,
            tabela TEXT NOT NULL,
            registro_id INTEGER,
            projeto_id INTEGER,
            antes TEXT,
            depois TEXT
        );
        CREATE INDEX idx_auditoria_projeto ON auditoria(projeto_id, id);
        CREATE INDEX idx_auditoria_lote ON auditoria(lote);
        CREATE INDEX idx_auditoria_acao ON auditoria(acao, tabela);
        -- 2) Índices nas chaves estrangeiras (exclusões e consultas não varrem tabelas inteiras).
        CREATE INDEX IF NOT EXISTS idx_abertura_projeto_id ON abertura(projeto_id);
        CREATE INDEX IF NOT EXISTS idx_parte_interessada_projeto_id ON parte_interessada(projeto_id);
        CREATE INDEX IF NOT EXISTS idx_interacao_parte_id ON interacao(parte_id);
        CREATE INDEX IF NOT EXISTS idx_historico_engajamento_parte_id ON historico_engajamento(parte_id);
        CREATE INDEX IF NOT EXISTS idx_risco_parte_id ON risco(parte_id);
        CREATE INDEX IF NOT EXISTS idx_risco_revisao_risco_id ON risco_revisao(risco_id);
        CREATE INDEX IF NOT EXISTS idx_incerteza_projeto_id ON incerteza(projeto_id);
        CREATE INDEX IF NOT EXISTS idx_questao_risco_id ON questao(risco_id);
        CREATE INDEX IF NOT EXISTS idx_questao_parte_id ON questao(parte_id);
        CREATE INDEX IF NOT EXISTS idx_mudanca_parte_id ON mudanca(parte_id);
        CREATE INDEX IF NOT EXISTS idx_licao_questao_id ON licao(questao_id);
        CREATE INDEX IF NOT EXISTS idx_licao_projeto_id ON licao(projeto_id);
        CREATE INDEX IF NOT EXISTS idx_item_iteracao_id ON item(iteracao_id);
        CREATE INDEX IF NOT EXISTS idx_item_risco_id ON item(risco_id);
        CREATE INDEX IF NOT EXISTS idx_item_mudanca_id ON item(mudanca_id);
        CREATE INDEX IF NOT EXISTS idx_item_parte_id ON item(parte_id);
        CREATE INDEX IF NOT EXISTS idx_item_pai_id ON item(pai_id);
        CREATE INDEX IF NOT EXISTS idx_linha_base_projeto_id ON linha_base(projeto_id);
        CREATE INDEX IF NOT EXISTS idx_qualidade_custo_item_id ON qualidade_custo(item_id);
        CREATE INDEX IF NOT EXISTS idx_qualidade_custo_projeto_id ON qualidade_custo(projeto_id);
        CREATE INDEX IF NOT EXISTS idx_beneficio_projeto_id ON beneficio(projeto_id);
        CREATE INDEX IF NOT EXISTS idx_iteracao_projeto_id ON iteracao(projeto_id);
        CREATE INDEX IF NOT EXISTS idx_metrica_projeto_id ON metrica(projeto_id);
        CREATE INDEX IF NOT EXISTS idx_medicao_metrica_id ON medicao(metrica_id);
        CREATE INDEX IF NOT EXISTS idx_relatorio_status_projeto_id ON relatorio_status(projeto_id);
        CREATE INDEX IF NOT EXISTS idx_membro_parte_id ON membro(parte_id);
        CREATE INDEX IF NOT EXISTS idx_membro_projeto_id ON membro(projeto_id);
        CREATE INDEX IF NOT EXISTS idx_raci_linha_item_id ON raci_linha(item_id);
        CREATE INDEX IF NOT EXISTS idx_raci_linha_projeto_id ON raci_linha(projeto_id);
        CREATE INDEX IF NOT EXISTS idx_raci_papel_membro_id ON raci_papel(membro_id);
        CREATE INDEX IF NOT EXISTS idx_avaliacao_equipe_projeto_id ON avaliacao_equipe(projeto_id);
        CREATE INDEX IF NOT EXISTS idx_fase_projeto_id ON fase(projeto_id);
        CREATE INDEX IF NOT EXISTS idx_decisao_tailoring_projeto_id ON decisao_tailoring(projeto_id);
        CREATE INDEX IF NOT EXISTS idx_conformidade_projeto_id ON conformidade(projeto_id);
        CREATE INDEX IF NOT EXISTS idx_adocao_grupo_parte_id ON adocao_grupo(parte_id);
        CREATE INDEX IF NOT EXISTS idx_adocao_grupo_projeto_id ON adocao_grupo(projeto_id);
        CREATE INDEX IF NOT EXISTS idx_adocao_medicao_grupo_id ON adocao_medicao(grupo_id);
        CREATE INDEX IF NOT EXISTS idx_decisao_projeto_id ON decisao(projeto_id);
        CREATE INDEX IF NOT EXISTS idx_premissa_projeto_id ON premissa(projeto_id);
        CREATE INDEX IF NOT EXISTS idx_aquisicao_parte_id ON aquisicao(parte_id);
        -- 3) Validações dentro do próprio banco (defesa em profundidade: valem mesmo se o app tiver um defeito).
        CREATE TRIGGER val_risco_escala_i BEFORE INSERT ON risco
        WHEN (NEW.probabilidade IS NOT NULL AND NEW.probabilidade NOT BETWEEN 1 AND 5) OR (NEW.impacto IS NOT NULL AND NEW.impacto NOT BETWEEN 1 AND 5)
        BEGIN SELECT RAISE(ABORT, 'probabilidade e impacto vão de 1 a 5'); END;
        CREATE TRIGGER val_risco_escala_u BEFORE UPDATE ON risco
        WHEN (NEW.probabilidade IS NOT NULL AND NEW.probabilidade NOT BETWEEN 1 AND 5) OR (NEW.impacto IS NOT NULL AND NEW.impacto NOT BETWEEN 1 AND 5)
        BEGIN SELECT RAISE(ABORT, 'probabilidade e impacto vão de 1 a 5'); END;
        CREATE TRIGGER val_aquisicao_i BEFORE INSERT ON aquisicao
        WHEN (NEW.valor IS NOT NULL AND NEW.valor < 0) OR (NEW.nota_desempenho IS NOT NULL AND NEW.nota_desempenho NOT BETWEEN 1 AND 5)
        BEGIN SELECT RAISE(ABORT, 'valor negativo ou nota fora de 1 a 5'); END;
        CREATE TRIGGER val_aquisicao_u BEFORE UPDATE ON aquisicao
        WHEN (NEW.valor IS NOT NULL AND NEW.valor < 0) OR (NEW.nota_desempenho IS NOT NULL AND NEW.nota_desempenho NOT BETWEEN 1 AND 5)
        BEGIN SELECT RAISE(ABORT, 'valor negativo ou nota fora de 1 a 5'); END;
        CREATE TRIGGER val_item_i BEFORE INSERT ON item
        WHEN (NEW.estimativa IS NOT NULL AND NEW.estimativa < 0) OR (NEW.custo_planejado IS NOT NULL AND NEW.custo_planejado < 0) OR (NEW.custo_real IS NOT NULL AND NEW.custo_real < 0) OR (NEW.valor IS NOT NULL AND NEW.valor NOT BETWEEN 1 AND 5)
        BEGIN SELECT RAISE(ABORT, 'estimativa, custo ou valor inválido'); END;
        CREATE TRIGGER val_item_u BEFORE UPDATE ON item
        WHEN (NEW.estimativa IS NOT NULL AND NEW.estimativa < 0) OR (NEW.custo_planejado IS NOT NULL AND NEW.custo_planejado < 0) OR (NEW.custo_real IS NOT NULL AND NEW.custo_real < 0) OR (NEW.valor IS NOT NULL AND NEW.valor NOT BETWEEN 1 AND 5)
        BEGIN SELECT RAISE(ABORT, 'estimativa, custo ou valor inválido'); END;
        CREATE TRIGGER val_iteracao_i BEFORE INSERT ON iteracao
        WHEN NEW.fim < NEW.inicio OR (NEW.capacidade IS NOT NULL AND NEW.capacidade < 0)
        BEGIN SELECT RAISE(ABORT, 'iteração com fim antes do início ou capacidade negativa'); END;
        CREATE TRIGGER val_iteracao_u BEFORE UPDATE ON iteracao
        WHEN NEW.fim < NEW.inicio OR (NEW.capacidade IS NOT NULL AND NEW.capacidade < 0)
        BEGIN SELECT RAISE(ABORT, 'iteração com fim antes do início ou capacidade negativa'); END;
        CREATE TRIGGER val_recurso_i BEFORE INSERT ON recurso_fisico
        WHEN (NEW.quantidade IS NOT NULL AND NEW.quantidade < 0) OR (NEW.usado IS NOT NULL AND NEW.usado < 0) OR (NEW.desperdicio IS NOT NULL AND NEW.desperdicio > COALESCE(NEW.usado, 0))
        BEGIN SELECT RAISE(ABORT, 'quantidade negativa ou desperdício maior que o uso'); END;
        CREATE TRIGGER val_recurso_u BEFORE UPDATE ON recurso_fisico
        WHEN (NEW.quantidade IS NOT NULL AND NEW.quantidade < 0) OR (NEW.usado IS NOT NULL AND NEW.usado < 0) OR (NEW.desperdicio IS NOT NULL AND NEW.desperdicio > COALESCE(NEW.usado, 0))
        BEGIN SELECT RAISE(ABORT, 'quantidade negativa ou desperdício maior que o uso'); END;
        CREATE TRIGGER val_usuario_i BEFORE INSERT ON usuario
        WHEN NEW.admin NOT IN (0, 1) OR NEW.ativo NOT IN (0, 1) OR length(NEW.senha_hash) < 20
        BEGIN SELECT RAISE(ABORT, 'usuário inválido'); END;
        CREATE TRIGGER val_usuario_u BEFORE UPDATE ON usuario
        WHEN NEW.admin NOT IN (0, 1) OR NEW.ativo NOT IN (0, 1) OR length(NEW.senha_hash) < 20
        BEGIN SELECT RAISE(ABORT, 'usuário inválido'); END;
    """,
    11: """
        -- v14: PMO, estagiários e modelos do PMBOK
        CREATE TABLE usuario_projeto (
            usuario_id INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            PRIMARY KEY (usuario_id, projeto_id)
        );
        CREATE INDEX idx_usuario_projeto_projeto ON usuario_projeto(projeto_id);
        -- quem já usava o app continua vendo os projetos que via
        INSERT INTO usuario_projeto (usuario_id, projeto_id) SELECT u.id, p.id FROM usuario u, projeto p WHERE u.admin = 0;
        ALTER TABLE membro ADD COLUMN usuario_id INTEGER REFERENCES usuario(id) ON DELETE SET NULL;
        CREATE INDEX idx_membro_usuario ON membro(usuario_id);
        ALTER TABLE item ADD COLUMN moscow TEXT DEFAULT '';
        CREATE TABLE item_dependencia (
            item_id INTEGER NOT NULL REFERENCES item(id) ON DELETE CASCADE,
            depende_de INTEGER NOT NULL REFERENCES item(id) ON DELETE CASCADE,
            PRIMARY KEY (item_id, depende_de),
            CHECK (item_id != depende_de)
        );
        CREATE INDEX idx_item_dependencia_depende ON item_dependencia(depende_de);
        ALTER TABLE projeto ADD COLUMN modelo TEXT DEFAULT '';
        ALTER TABLE projeto ADD COLUMN cynefin TEXT DEFAULT '';
        ALTER TABLE projeto ADD COLUMN stacey_requisitos INTEGER;
        ALTER TABLE projeto ADD COLUMN stacey_tecnologia INTEGER;
        CREATE TABLE revisao_pmo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL REFERENCES projeto(id) ON DELETE CASCADE,
            tabela TEXT NOT NULL,
            registro_id INTEGER NOT NULL,
            titulo TEXT DEFAULT '',
            link TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'pendente',   -- pendente | aprovada | devolvida
            solicitado_por TEXT DEFAULT '',
            mensagem TEXT DEFAULT '',
            solicitado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            revisor TEXT DEFAULT '',
            comentario TEXT DEFAULT '',
            decidido_em TEXT
        );
        CREATE INDEX idx_revisao_pmo_projeto ON revisao_pmo(projeto_id, status);
        CREATE TABLE configuracao (chave TEXT PRIMARY KEY, valor TEXT);
        INSERT INTO configuracao (chave, valor) VALUES ('nivel_exigencia', 'essencial');
    """,
    12: """
        -- v18: o projeto de exemplo passa a se apresentar como exemplo (não como descrição do Octante)
        UPDATE projeto SET nome = 'Exemplo: AgendaFácil',
            descricao = 'Projeto de demonstração para aprender a usar o Octante. Cenário: uma clínica quer um aplicativo para os pacientes marcarem consultas sem ligar. Explore as telas para ver como cada domínio e princípio do PMBOK 7 fica preenchido.'
        WHERE nome = 'AgendaFácil — app de agendamento';
    """,
}
VERSAO_ATUAL = max(MIGRACOES)


def get_db():
    if "db" not in g:
        # timeout: espera até 10 s se outra requisição estiver gravando (evita "database is locked" com vários usuários)
        g.db = sqlite3.connect(current_app.config["DATABASE"], timeout=10)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
        g.db.execute("PRAGMA busy_timeout = 10000")
        for gancho in current_app.extensions.get("ao_conectar", []):
            gancho(g.db)
    return g.db


def close_db(_exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def migrar(conn):
    """Aplica as migrações pendentes. Cada uma roda em uma transação própria."""
    versao = conn.execute("PRAGMA user_version").fetchone()[0]
    if versao == 0:  # banco novo ou criado pela v1 (que não registrava versão)
        versao = 1
        conn.execute("PRAGMA user_version = 1")
    for alvo in sorted(v for v in MIGRACOES if v > versao):
        try:
            conn.execute("BEGIN")
            for comando in _comandos(MIGRACOES[alvo]):
                conn.execute(comando)
            conn.execute(f"PRAGMA user_version = {alvo}")
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise
    return conn.execute("PRAGMA user_version").fetchone()[0]


def _comandos(script):
    """Divide o script em comandos completos (respeita ';' dentro de strings)."""
    atual, comandos = "", []
    for linha in script.splitlines(keepends=True):
        if linha.strip().startswith("--"):
            continue
        atual += linha
        if sqlite3.complete_statement(atual):
            comandos.append(atual.strip())
            atual = ""
    if atual.strip():
        comandos.append(atual.strip())
    return comandos


def init_db(app):
    path = app.config["DATABASE"]
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    schema = os.path.join(os.path.dirname(__file__), "schema.sql")
    conn = sqlite3.connect(path, isolation_level=None)
    try:
        with open(schema, encoding="utf-8") as f:
            conn.executescript(f.read())
        if callable(app.config.get("ANTES_DE_MIGRAR")) and conn.execute("PRAGMA user_version").fetchone()[0] < VERSAO_ATUAL:
            app.config["ANTES_DE_MIGRAR"](path, conn)
        migrar(conn)
        for gancho in app.extensions.get("ao_iniciar_banco", []):
            gancho(conn)
    finally:
        conn.close()
    app.teardown_appcontext(close_db)
