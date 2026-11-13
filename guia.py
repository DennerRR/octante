"""Guia para iniciantes (v9): fluxo do projeto em 5 fases, glossário em linguagem simples e ajuda por página."""
from flask import url_for

from db import get_db


def _n(db, sql, *args):
    return db.execute(sql, args).fetchone()[0]


def fluxo_do_projeto(p, partes, abertura):
    """Fases e etapas do fluxo, com o que já foi feito. Cada etapa: titulo, simples, link, feito, opcional."""
    db = get_db()
    pid = p["id"]
    u = lambda ep: url_for(ep, projeto_id=pid)  # noqa: E731

    def tab(t):
        return _n(db, f"SELECT COUNT(*) FROM {t} WHERE projeto_id = ?", pid)

    def e(titulo, simples, ep, feito, opcional=False, dominio=""):
        return {"titulo": titulo, "simples": simples, "link": u(ep), "feito": bool(feito), "opcional": opcional, "dominio": dominio}

    fases = [
        ("1", "Iniciar", "Dar nome, motivo e rumo ao projeto.", [
            e("Como vamos trabalhar", "Escolha o jeito de trabalhar: plano fechado, por etapas curtas ou misto.", "abordagem", p["abordagem"], dominio="Abordagem e ciclo de vida"),
            e("Termo de abertura aprovado", "Documento que autoriza o projeto: por que existe, objetivos e quem patrocina. Só vale depois de aprovado.", "abertura", abertura["status"] == "aprovado", dominio="Planejamento"),
            e("Pessoas envolvidas", "Liste quem é afetado ou pode influenciar o projeto (as partes interessadas).", "partes_registro", len(partes) > 0, dominio="Partes interessadas"),
        ]),
        ("2", "Planejar", "Decidir o que, quem, quando, quanto e o que pode dar errado.", [
            e("Equipe", "Quem faz o trabalho e como a equipe combina de trabalhar.", "equipe.membros", tab("membro") > 0, dominio="Equipe"),
            e("Escopo e entregas", "Lista do que será entregue (backlog) e como o cliente aceita.", "entrega.itens", tab("item") > 0, dominio="Entrega"),
            e("Riscos", "Coisas que podem dar errado (ou certo) e o que fazer a respeito.", "incerteza.riscos", tab("risco") > 0, dominio="Incerteza"),
            e("Prazo e orçamento", "Datas das etapas e quanto cada uma deve custar.", "medicao.cronograma", tab("iteracao") > 0, dominio="Planejamento"),
            e("Compras e recursos", "O que precisa ser comprado ou contratado de fora.", "suprimentos.painel", tab("aquisicao") + tab("recurso_fisico") > 0, True, "Trabalho do projeto"),
        ]),
        ("3", "Executar", "Fazer o trabalho e cuidar do dia a dia.", [
            e("Quadro de tarefas", "Mova os itens: a fazer, em andamento, concluído.", "entrega.quadro", _n(db, "SELECT COUNT(*) FROM item WHERE projeto_id = ? AND status != 'a_fazer'", pid) > 0, dominio="Entrega"),
            e("Engajar as pessoas", "Combine como e com que frequência vai falar com cada parte interessada.", "partes_engajamento", _n(db, "SELECT COUNT(*) FROM parte_interessada WHERE projeto_id = ? AND ativa = 1 AND engajamento_desejado IS NOT NULL", pid) > 0, dominio="Partes interessadas"),
            e("Questões e mudanças", "Registre problemas que surgem e pedidos de mudança.", "trabalho.painel", tab("questao") + tab("mudanca") > 0, True, "Trabalho do projeto"),
        ]),
        ("4", "Acompanhar", "Ver se o projeto está no rumo e corrigir cedo.", [
            e("Acompanhamento", "Painel de prazo, custo e escopo; relatório de status.", "medicao.painel", tab("relatorio_status") > 0 or tab("metrica") > 0, dominio="Medição"),
            e("Checklist dos 8 domínios", "Marque se os resultados esperados de cada área já foram atingidos.", "dominios", _n(db, "SELECT COUNT(*) FROM verificacao WHERE projeto_id = ? AND dominio != 'principios' AND status != 'nao_avaliado'", pid) > 0, dominio="Todos"),
            e("Os 12 princípios", "Autoavaliação: o projeto segue os princípios do PMBOK?", "principios.autoavaliacao", _n(db, "SELECT COUNT(*) FROM verificacao WHERE projeto_id = ? AND dominio = 'principios' AND status != 'nao_avaliado'", pid) > 0, dominio="Princípios"),
        ]),
        ("5", "Encerrar", "Fechar o projeto e deixar aprendizado.", [
            e("Lições aprendidas", "O que deu certo e o que fazer diferente na próxima vez.", "trabalho.licoes", tab("licao") > 0, dominio="Trabalho do projeto"),
            e("Encerramento", "Confira pendências, avalie o resultado e encerre.", "ciclo.encerramento", p["situacao"] and p["situacao"] != "ativo", dominio="Todos"),
        ]),
    ]
    resultado, achou = [], False
    for num, nome, resumo, etapas in fases:
        for et in etapas:
            et["proximo"] = False
            if not achou and not et["feito"] and not et["opcional"]:
                et["proximo"] = achou = True
        feitas = sum(1 for et in etapas if et["feito"])
        obrig = [et for et in etapas if not et["opcional"]]
        resultado.append({"num": num, "nome": nome, "resumo": resumo, "etapas": etapas, "feitas": feitas, "total": len(etapas),
                          "completa": all(et["feito"] for et in obrig)})
    return resultado


GLOSSARIO = [
    ("Abordagem preditiva / adaptativa / híbrida", "Preditiva: planeja tudo antes e segue o plano. Adaptativa (ágil): entrega em partes e ajusta com o feedback. Híbrida: mistura das duas."),
    ("Aceite", "O cliente confirma que a entrega está como combinado."),
    ("Backlog", "Lista priorizada de tudo que ainda precisa ser feito."),
    ("Baseline (linha de base)", "Versão aprovada do escopo, prazo ou custo, usada para comparar com o que de fato acontece."),
    ("Business case", "Justificativa financeira e estratégica: vale a pena gastar nesse projeto?"),
    ("Cadência", "De quanto em quanto tempo o projeto entrega algo (a cada 2 semanas, por exemplo)."),
    ("Critério de aceite", "Condição que a entrega precisa cumprir para ser aceita."),
    ("Definição de pronto", "Lista de condições para um item ser considerado terminado (testado, revisado etc.)."),
    ("Domínio de desempenho", "Cada uma das 8 áreas do PMBOK 7: partes interessadas, equipe, abordagem, planejamento, trabalho, entrega, medição e incerteza."),
    ("EMV (valor monetário esperado)", "Probabilidade do risco × quanto ele custaria. Ajuda a decidir quanto reservar."),
    ("Escopo", "Tudo o que o projeto vai entregar (e o que não vai)."),
    ("Iteração / sprint", "Período curto e fixo (1 a 4 semanas) em que a equipe entrega um pedaço do produto."),
    ("KPI (indicador)", "Número que mostra como o projeto está indo."),
    ("Lição aprendida", "Aprendizado registrado para não repetir erros e repetir acertos."),
    ("MVP", "Primeira versão mínima do produto, suficiente para testar com usuários."),
    ("Parte interessada (stakeholder)", "Qualquer pessoa ou grupo afetado pelo projeto ou que pode influenciá-lo."),
    ("Patrocinador", "Quem libera dinheiro e apoio e decide nas questões grandes."),
    ("PMO", "Escritório de projetos: apoia e padroniza o gerenciamento de projetos na organização."),
    ("Premissa", "Algo que você assume como verdadeiro sem ter provado ainda. Precisa ser validado."),
    ("Princípios (12)", "Orientações de comportamento do PMBOK 7, como administração, foco em valor e qualidade."),
    ("Probabilidade × impacto", "As duas notas de um risco: chance de acontecer e tamanho do estrago."),
    ("RACI", "Matriz que diz quem é Responsável, quem Aprova, quem é Consultado e quem é Informado em cada atividade."),
    ("Reserva", "Dinheiro ou prazo guardado para imprevistos."),
    ("Restrição", "Limite que não dá para mudar: prazo, orçamento, lei, tecnologia."),
    ("Risco", "Evento incerto que pode afetar o projeto. Pode ser ameaça (ruim) ou oportunidade (boa)."),
    ("Tailoring (adaptação)", "Ajustar processos e documentos ao tamanho e ao contexto do projeto, em vez de seguir tudo igual."),
    ("Termo de abertura", "Documento que autoriza o projeto e dá autoridade ao gerente."),
    ("Valor agregado (EVM)", "Método que compara o que foi planejado, o que foi feito e o que foi gasto, para ver prazo e custo."),
    ("Velocidade", "Quantos pontos ou itens a equipe entrega por iteração. Serve para prever prazos."),
    ("WIP (trabalho em andamento)", "Itens começados e não terminados. Limitar o WIP evita travar o fluxo."),
]

# endpoint -> (para que serve, o que fazer aqui)
AJUDA_PAGINA = {
    "abordagem": ("Escolhe o jeito de trabalhar do projeto.", "Dê notas de 1 a 5 aos fatores; o app sugere preditiva, adaptativa ou híbrida. Você pode discordar e justificar."),
    "abertura": ("O termo de abertura autoriza o projeto.", "Preencha propósito, objetivos, critérios de sucesso, patrocinador e gerente. Só então marque como aprovado."),
    "partes_registro": ("Lista de quem é afetado pelo projeto ou pode influenciá-lo.", "Cadastre pessoas e grupos. Para cada um, informe o papel e (se souber) a atitude: apoia, neutro ou opõe."),
    "partes_analise": ("Entender cada parte interessada.", "Dê notas de poder, interesse, influência e impacto. Isso define quem exige mais atenção."),
    "partes_priorizacao": ("Decidir com quem gastar mais energia.", "Veja a matriz poder × interesse e ajuste a prioridade sugerida."),
    "partes_engajamento": ("Plano para levar cada parte do nível atual ao desejado.", "Defina onde cada um está, onde precisa estar e como e com que frequência vai se comunicar."),
    "partes_monitoramento": ("Registrar as conversas e medir a satisfação.", "Anote cada contato (data, o que foi tratado) e, se possível, uma nota de satisfação."),
    "equipe.membros": ("Quem trabalha no projeto.", "Cadastre os membros com papel e habilidades; aponte lacunas para planejar desenvolvimento."),
    "equipe.acordo": ("Regras da equipe, escritas por todos.", "Combine valores, comunicação, decisões, conflitos e reuniões."),
    "equipe.matriz": ("Quem faz o quê em cada atividade.", "Marque R (responsável), A (aprova), C (consultado) ou I (informado)."),
    "equipe.saude": ("Termômetro da equipe.", "Faça a avaliação a cada iteração ou retrospectiva e acompanhe a tendência."),
    "entrega.itens": ("Escopo e backlog: o que será entregue.", "Cadastre épicos, histórias e requisitos com critérios de aceite; ordene por valor."),
    "entrega.quadro": ("Quadro de tarefas.", "Mova os itens entre as colunas conforme o andamento; respeite o limite de trabalho em andamento."),
    "entrega.qualidade": ("Custo da qualidade.", "Registre o que gastou prevenindo defeitos e o que gastou corrigindo."),
    "entrega.beneficios": ("Benefícios esperados do projeto.", "Defina o que será medido e a meta; depois registre o resultado real."),
    "incerteza.riscos": ("Registro de riscos.", "Descreva o risco, dê probabilidade e impacto, escolha a resposta e um responsável."),
    "incerteza.painel": ("Visão geral e limites dos riscos.", "Ajuste o limite de risco alto e a reserva de gerenciamento."),
    "incerteza.outras": ("Outras incertezas além do risco.", "Registre ambiguidade, complexidade e volatilidade e como vai tratá-las."),
    "medicao.cronograma": ("Prazo e orçamento por iteração ou item.", "Informe datas e custos planejados; depois atualize com o custo real."),
    "medicao.painel": ("Painel de desempenho.", "Leia o semáforo: verde no rumo, amarelo atenção, vermelho ação."),
    "medicao.indicadores": ("Indicadores (KPIs) do projeto.", "Defina o que medir, a meta e registre os valores periodicamente."),
    "medicao.relatorios": ("Relatórios de status.", "Escreva um resumo curto: situação, o que foi feito, próximos passos."),
    "trabalho.painel": ("Dia a dia: questões, mudanças e lições.", "Use os atalhos para registrar problemas e pedidos de mudança."),
    "trabalho.questoes": ("Questões são problemas que já aconteceram.", "Registre, atribua responsável e prazo, e resolva."),
    "trabalho.mudancas": ("Pedidos de mudança.", "Avalie o impacto em escopo, prazo, custo, recursos, partes e riscos antes de decidir."),
    "trabalho.licoes": ("Lições aprendidas.", "Registre durante o projeto, não só no fim."),
    "suprimentos.painel": ("Compras, contratos e recursos físicos.", "Decida fazer ou comprar; para comprar, registre fornecedor, contrato e prazos."),
    "principios.autoavaliacao": ("Os 12 princípios do PMBOK 7.", "Marque o status de cada evidência e escreva uma reflexão da equipe."),
    "principios.business_case": ("Justificativa financeira.", "Informe investimento, benefício e custo anual para ver VPL, ROI e payback."),
    "principios.conformidade": ("Obrigações legais e éticas.", "Liste cada requisito, quem cuida e a evidência de que foi atendido."),
    "principios.adocao": ("Mudança organizacional.", "Para cada grupo afetado, avalie impacto, prontidão e meta de adoção."),
    "principios.decisoes": ("Decisões e premissas.", "Registre decisões importantes e valide as premissas antes que virem problema."),
    "dominios": ("Checklist dos 8 domínios.", "Escolha uma área e marque se cada resultado esperado foi atingido, com evidência."),
    "parte_nova": ("Cadastrar uma parte interessada.", "Nome e papel bastam para começar; refine depois nas etapas de análise."),
    "parte_editar": ("Editar uma parte interessada.", "Atualize papel, atitude e notas conforme você a conhece melhor."),
    "incerteza.risco_novo": ("Novo risco.", "Escreva como evento (\"pode acontecer X\"), com causa e efeito. Dê probabilidade e impacto de 1 a 5."),
    "incerteza.risco_editar": ("Editar risco.", "Atualize notas, resposta e responsável a cada revisão."),
    "entrega.item_novo": ("Novo item de escopo.", "Dê um título claro, o valor para o negócio e critérios de aceite."),
    "entrega.item": ("Editar item de escopo.", "Mantenha status e estimativa atualizados."),
    "entrega.painel": ("Resumo da entrega.", "Veja quanto do escopo já foi aceito e o que está pendente."),
    "trabalho.questao_nova": ("Nova questão.", "Descreva o problema, a prioridade e quem resolve."),
    "trabalho.mudanca_nova": ("Novo pedido de mudança.", "Preencha o impacto em cada área antes de pedir a decisão."),
    "dominio": ("Resultados esperados de uma área.", "Marque atendido, parcial ou não atendido e escreva a evidência."),
    "medicao.relatorio": ("Relatório de status.", "Resumo curto da situação, realizações e próximos passos."),
    "ciclo.fases": ("Fases do ciclo de vida.", "Defina fases com critérios de saída e faça revisão ao fim de cada uma."),
    "ciclo.tailoring": ("Adaptar o processo ao projeto.", "Responda o diagnóstico e registre o que adicionou, removeu ou ajustou."),
    "ciclo.encerramento": ("Fechar o projeto.", "Resolva as pendências do checklist, avalie os objetivos e encerre."),
}
