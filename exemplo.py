"""Cria um projeto de exemplo (AgendaFácil) para explorar o app.

Uso:  python exemplo.py
"""
from datetime import date, timedelta

import pmbok
from app import create_app


def criar(app=None):
    """Cria o projeto AgendaFácil e devolve o id."""
    app = app or create_app()
    c = app.test_client()
    c.environ_base["gestor.interno"] = True  # requisição interna: dispensa login e CSRF
    r = c.post("/projetos/novo", data={"nome": "Exemplo: AgendaFácil", "descricao": "Projeto de demonstração para aprender a usar o Octante. Cenário: uma clínica quer um aplicativo para os pacientes marcarem consultas sem ligar. Explore as telas para ver como cada domínio e princípio do PMBOK 7 fica preenchido.", "cadencia": "periodica"})
    pid = int(r.headers["Location"].split("/p/")[1].split("/")[0])
    f = {k: v for k, v in zip([x[0] for x in pmbok.FATORES_ABORDAGEM], [4,5,4,4,5,3,4,2,4,5,4,4,4,3,5])}
    f.update(acao="salvar", abordagem="adaptativa", cadencia="periodica", justificativa="Requisitos devem evoluir com o feedback dos pacientes; LGPD exige documentação mínima.")
    c.post(f"/p/{pid}/abordagem", data={k: str(v) for k, v in f.items()})
    c.post(f"/p/{pid}/abertura", data={"status":"em_revisao","proposito":"Reduzir a fila de ligações da recepção e permitir agendamento 24h.","objetivos":"Agendamento em menos de 2 minutos\n40% das consultas marcadas online em 6 meses","criterios_sucesso":"Meta de adoção atingida; satisfação dos pacientes ≥ 4/5","patrocinador":"Dra. Lúcia Prado","gerente":"Denner Ribeiro","marcos":"MVP em março; release 1.0 em junho",
     "visao_publico":"pacientes da clínica","visao_necessidade":"precisam marcar consultas sem ligar","visao_produto":"AgendaFácil","visao_categoria":"aplicativo web de agendamento","visao_beneficio":"permite agendar em menos de 2 minutos","visao_alternativa":"o agendamento por telefone","visao_diferencial":"funciona 24 horas e confirma por WhatsApp","gerar_visao":"1"})
    pessoas = [
     ("Dra. Lúcia Prado","Diretora clínica","Patrocinador",5,5,"apoiador",(1,1,1),4,5,"interativa","Semanal"),
     ("Carlos Mendes","Gerente de TI","Equipe de gerenciamento do projeto",4,3,"opositor",(1,1,0),2,4,"interativa","Quinzenal"),
     ("Recepção","Equipe de atendimento","Usuário final",2,5,"apoiador",(0,1,1),4,5,"interativa","Por iteração"),
     ("Pacientes","Usuários do app","Cliente",3,4,"neutro",(0,1,0),1,4,"push","Mensal"),
     ("Encarregado LGPD","DPO","Órgão de governança",4,2,"neutro",(1,1,0),3,4,"push","Por marco/fase"),
     ("Fornecedor de SMS","Integração WhatsApp","Fornecedor",1,2,"desconhecida",(0,0,0),None,None,"",""),
    ]
    ids=[]
    for nome,papel,cat,po,inte,at,sal,ea,ed,met,fr in pessoas:
        d={"nome":nome,"papel":papel,"categoria":cat,"interna":"1" if cat not in("Cliente","Fornecedor") else "0","ativa":"1","atitude":at,
           "poder":str(po),"interesse":str(inte),"influencia":str(po),"impacto":str(inte),"metodo_comunicacao":met,"frequencia":fr,
           "engajamento_atual":str(ea or ""),"engajamento_desejado":str(ed or "")}
        for k,v in zip(("sal_poder","sal_legitimidade","sal_urgencia"),sal):
            if v: d[k]="1"
        r=c.post(f"/p/{pid}/partes/nova",data=d); ids.append(int(r.headers["Location"].split("/")[-1]))
    c.post(f"/p/{pid}/partes/priorizacao", data={"acao":"sugerida"})
    hoje=date.today()
    for sid,dias,res,sat in [(ids[0],40,"Kickoff do projeto",4),(ids[0],12,"Demo da sprint 1",4),(ids[0],3,"Demo da sprint 2",5),(ids[2],5,"Teste do protótipo com recepcionistas",4),(ids[2],20,"Entrevista de requisitos",3),(ids[1],50,"Reunião sobre infraestrutura",2)]:
        c.post(f"/p/{pid}/partes/monitoramento",data={"parte_id":str(sid),"data":(hoje-timedelta(days=dias)).isoformat(),"metodo":"interativa","tipo":"verbal_formal","resumo":res,"satisfacao":str(sat)})
    c.post(f"/p/{pid}/partes/engajamento", data={**{f"atual_{s}":v for s,v in zip(ids,[5,2,4,2,3,""])}, **{f"desejado_{s}":v for s,v in zip(ids,[5,4,5,4,4,""])}, **{f"metodo_{s}":v for s,v in zip(ids,["interativa","interativa","interativa","push","push",""])}, **{f"frequencia_{s}":v for s,v in zip(ids,["Semanal","Quinzenal","Por iteração","Mensal","Por marco/fase",""])}})
    c.post(f"/p/{pid}/dominios/partes-interessadas", data={"status_0":"atendido","evidencia_0":"Patrocinadora e recepção avançaram no contínuo de engajamento.","status_1":"parcial","evidencia_1":"TI ainda questiona o escopo de integração.","status_2":"nao_avaliado"})
    c.post(f"/p/{pid}/dominios/abordagem", data={"status_0":"atendido","status_1":"parcial","status_2":"nao_avaliado"})


    # Incerteza (v2)
    c.post(f"/p/{pid}/incerteza", data={"limite_risco": "12", "revisao_risco_dias": "14", "reserva_gerenciamento": "8.000",
           "apetite_risco": "Aceitamos até 2 semanas de atraso no MVP; nenhum risco à conformidade com a LGPD.",
           "risco_global": "medio", "risco_global_notas": "Integrações com sistemas legados e requisitos ainda em evolução."})
    riscos = [
        dict(titulo="Vazamento de dados de pacientes", tipo="ameaca", fonte="regulatorio", probabilidade="2", impacto="5",
             impacto_custo="50.000", estrategia_ameaca="mitigar", responsavel="Encarregado LGPD", parte_id=str(ids[4]),
             plano_resposta="Revisão de segurança a cada release; criptografia dos dados sensíveis.", reserva_custo="10.000"),
        dict(titulo="TI bloquear a integração com o sistema da clínica", tipo="ameaca", fonte="partes", probabilidade="4", impacto="4",
             impacto_prazo_dias="20", parte_id=str(ids[1]), causa="Gerente de TI vê o app como risco à infraestrutura."),
        dict(titulo="Mudança de preço da API do WhatsApp", tipo="ameaca", fonte="mercado", probabilidade="3", impacto="3",
             impacto_custo="6.000", estrategia_ameaca="aceitar", plano_contingencia="Usar SMS como canal alternativo",
             responsavel="Denner", reserva_custo="3.000"),
        dict(titulo="Recepção adotar o app antes do previsto", tipo="oportunidade", fonte="partes", probabilidade="4", impacto="3",
             estrategia_oportunidade="melhorar", responsavel="Denner", parte_id=str(ids[2]),
             plano_resposta="Treinamento antecipado e material de apoio no balcão."),
        dict(titulo="Reaproveitar componente de agenda open source", tipo="oportunidade", fonte="tecnico", probabilidade="3", impacto="4",
             impacto_custo="12.000", estrategia_oportunidade="explorar", responsavel="Equipe de desenvolvimento"),
    ]
    for rk in riscos:
        rk.setdefault("status", "aberto")
        c.post(f"/p/{pid}/incerteza/riscos/novo", data=rk)
    c.post(f"/p/{pid}/incerteza/riscos/1/revisar", data={"probabilidade": "2", "impacto": "4", "status": "em_resposta",
           "nota": "Criptografia implementada na sprint 2"})
    c.post(f"/p/{pid}/incerteza/outras", data={"natureza": "ambiguidade", "descricao": "Recepção e médicos entendem “consulta confirmada” de formas diferentes",
           "respostas": ["definicoes", "prototipos"], "acoes": "Glossário validado com a diretora clínica"})
    c.post(f"/p/{pid}/incerteza/outras", data={"natureza": "complexidade", "descricao": "Integração com 3 sistemas legados que se afetam entre si",
           "respostas": ["desacoplamento", "iterar"], "acoes": "Integrar um sistema por release"})
    c.post(f"/p/{pid}/incerteza/outras", data={"natureza": "volatilidade", "descricao": "Rotatividade de desenvolvedores no mercado de SJC",
           "respostas": ["alternativas"]})

    # Trabalho do projeto (v3)
    c.post(f"/p/{pid}/incerteza/riscos/3/revisar", data={"status": "ocorreu", "nota": "Fornecedor anunciou reajuste de 40%"})
    c.post(f"/p/{pid}/trabalho/questoes/1", data={"titulo": "Mudança de preço da API do WhatsApp", "prioridade": "alta",
           "status": "em_andamento", "risco_id": "3", "responsavel": "Denner", "prazo": (hoje + timedelta(days=5)).isoformat(),
           "descricao": "Risco R-3 ocorreu. Plano de contingência: usar SMS como canal alternativo.", "reserva_usada_custo": "1.800"})
    c.post(f"/p/{pid}/trabalho/questoes/nova", data={"titulo": "Servidor de homologação instável", "prioridade": "alta",
           "status": "aberta", "responsavel": "Carlos Mendes", "parte_id": str(ids[1]), "prazo": (hoje - timedelta(days=2)).isoformat()})
    c.post(f"/p/{pid}/trabalho/questoes/nova", data={"titulo": "Deploy da sprint 2 falhou em produção", "prioridade": "media",
           "status": "resolvida", "responsavel": "Denner", "resolucao": "Faltava a variável de ambiente do gateway de SMS no servidor."})
    c.post(f"/p/{pid}/trabalho/licoes", data={"descricao": "Deploy falhou por variável de ambiente ausente.", "tipo": "melhorar",
           "recomendacao": "Checklist de deploy com validação automática das variáveis antes de publicar.", "origem": "questao",
           "questao_id": "3", "dominio": "trabalho", "conhecimento": "explicito", "alcance": "outras_equipes"})
    c.post(f"/p/{pid}/trabalho/licoes", data={"descricao": "Demonstrar o protótipo para a recepção a cada sprint antecipou ajustes de usabilidade.",
           "tipo": "manter", "recomendacao": "Manter a demo quinzenal com quem usa o sistema no balcão.", "origem": "retrospectiva",
           "dominio": "partes-interessadas", "conhecimento": "tacito", "alcance": "organizacao"})
    impactos = {"imp_escopo": "Nova tela de pagamento e integração com gateway.", "imp_cronograma": "+1 sprint antes da release 1.0.",
                "imp_custo": "Taxa do gateway por transação; sem custo fixo.", "imp_recursos": "Sem mudança na equipe.",
                "imp_partes": "Pacientes e financeiro da clínica.", "imp_riscos": "Novo risco de conformidade (PCI) com dados de cartão."}
    c.post(f"/p/{pid}/trabalho/mudancas/nova", data={"titulo": "Pagamento online da consulta", "parte_id": str(ids[0]),
           "justificativa": "Reduzir faltas: consultas pagas antecipadamente têm menos ausências.", "status": "aprovada",
           "decidido_por": "Dra. Lúcia Prado", "comunicada": "1", "notas_decisao": "Aprovada para a release 1.0.", **impactos})
    c.post(f"/p/{pid}/trabalho/mudancas/nova", data={"titulo": "Trocar o banco de dados para o da TI corporativa",
           "parte_id": str(ids[1]), "justificativa": "Padronização da infraestrutura.", "status": "em_analise",
           "imp_escopo": "Reescrever a camada de persistência.", "imp_cronograma": "+2 sprints."})

    # Entrega (v4)
    c.post(f"/p/{pid}/entrega", data={"definicao_pronto": "Código revisado por outra pessoa\nTestes automatizados passando\nPublicado em homologação",
           "unidade_estimativa": "pontos", "limite_wip": "2"})


    def novo_item(**campos):
        campos.setdefault("tipo", "historia")
        campos.setdefault("status", "a_fazer")
        campos.setdefault("q_claro", "1")
        campos.setdefault("q_consistente", "1")
        r = c.post(f"/p/{pid}/entrega/itens/novo", data=campos)
        return r.headers["Location"].split("/")[-1]


    pronto = {"dod_ok": "1"}
    aceite = {"dod_ok": "1", "aceito_por": "Dra. Lúcia Prado"}
    ep1 = novo_item(titulo="Agendamento online", tipo="epico", valor="5", ordem="1")
    novo_item(titulo="Marcar consulta pelo celular", pai_id=ep1, estimativa="5", valor="5", status="aceito", q_conciso="1",
              criterios_aceite="Paciente agenda em menos de 2 minutos\nHorários ocupados não aparecem", parte_id=str(ids[3]), **aceite)
    novo_item(titulo="Receber confirmação por WhatsApp", pai_id=ep1, estimativa="3", valor="4", status="concluido", q_conciso="1",
              criterios_aceite="Mensagem enviada em até 1 minuto após o agendamento", **pronto)
    novo_item(titulo="Remarcar ou cancelar consulta", pai_id=ep1, estimativa="5", valor="4", status="em_andamento",
              criterios_aceite="Paciente remarca até 2 horas antes", responsavel="Denner")
    novo_item(titulo="Entrar na lista de espera", pai_id=ep1, estimativa="8", valor="2")
    ep2 = novo_item(titulo="Painel da recepção", tipo="epico", valor="4", ordem="2")
    novo_item(titulo="Ver a agenda do dia", pai_id=ep2, estimativa="3", valor="5", status="aceito", q_conciso="1",
              criterios_aceite="Mostra todas as consultas do dia por médico", parte_id=str(ids[2]), **aceite)
    novo_item(titulo="Bloquear horários de um médico", pai_id=ep2, estimativa="2", valor="3", status="em_andamento",
              criterios_aceite="Horário bloqueado some do app do paciente", responsavel="Denner")
    c.post(f"/p/{pid}/entrega/linha-base", data={"motivo": "Escopo do MVP aprovado pela patrocinadora"})
    novo_item(titulo="Pagamento online da consulta", estimativa="8", valor="4", mudanca_id="1", ordem="3", q_conciso="1",
              criterios_aceite="Pagamento por cartão aprovado em até 10 segundos")
    novo_item(titulo="Criptografar dados sensíveis dos pacientes", tipo="requisito", estimativa="3", valor="5", risco_id="1", ordem="4",
              status="concluido", criterios_aceite="Dados pessoais criptografados no banco", **pronto)
    for cat, desc, custo in [("prevencao", "Revisão de código em pares nas sprints 1 e 2", "1.200"),
                             ("avaliacao", "Teste do protótipo com as recepcionistas", "800"),
                             ("falha_interna", "Retrabalho no fluxo de remarcação após o teste", "600")]:
        c.post(f"/p/{pid}/entrega/qualidade", data={"categoria": cat, "descricao": desc, "custo": custo})
    c.post(f"/p/{pid}/entrega/qualidade", data={"acao": "resolver", "registro_id": "3"})
    c.post(f"/p/{pid}/entrega/beneficios", data={"descricao": "Menos ligações de agendamento para a recepção",
           "medida": "Ligações de agendamento por semana", "meta": "Reduzir 40%", "data_prevista": (hoje + timedelta(days=120)).isoformat()})
    c.post(f"/p/{pid}/entrega/beneficios", data={"descricao": "Agendamento disponível 24 horas", "medida": "Consultas marcadas fora do horário comercial",
           "meta": "Pelo menos 15% das consultas"})

    # Cronograma, orçamento e medição (v5)
    def dia(n):
        return (hoje + timedelta(days=n)).isoformat()


    url = f"/p/{pid}/medicao/cronograma"
    c.post(url, data={"acao": "datas", "data_inicio": dia(-42), "data_fim_planejada": dia(60)})
    for n, (ini, fim) in enumerate([(-42, -29), (-28, -15), (-14, -1), (0, 13), (14, 27)], start=1):
        c.post(url, data={"acao": "iteracao", "nome": f"Sprint {n}", "inicio": dia(ini), "fim": dia(fim), "capacidade": "8",
                          "meta": ["Agendar pelo celular", "Painel da recepção", "Segurança dos dados", "Remarcação", "Lista de espera e pagamento"][n - 1]})
    # código do item: (sprint, início, fim, custo planejado, custo real, criado, iniciado, concluído)
    plano = {2: (1, -42, -29, "4.000", "4.400", -42, -40, -30), 3: (2, -28, -15, "2.500", "2.600", -42, -27, -16),
             7: (2, -28, -15, "2.500", "2.300", -42, -26, -18), 10: (3, -14, -1, "2.500", "2.600", -20, -12, -4),
             4: (4, -8, 5, "4.000", "1.500", -42, -5, None), 8: (4, 0, 13, "1.500", "300", -42, -2, None),
             5: (5, 14, 27, "6.000", "", -42, None, None), 9: (5, 28, 41, "6.000", "", -10, None, None)}
    with app.app_context():
        from db import get_db
        db = get_db()
        por_codigo = {r["codigo"]: r["id"] for r in db.execute("SELECT id, codigo FROM item WHERE projeto_id = ?", (pid,))}
        dados = {"acao": "itens"}
        for cod, (sp, ini, fim, cp, cr, *_resto) in plano.items():
            k = por_codigo[cod]
            dados.update({f"iteracao_{k}": str(sp), f"inicio_{k}": dia(ini), f"fim_{k}": dia(fim),
                          f"custo_planejado_{k}": cp, f"custo_real_{k}": cr})
        c.post(url, data=dados)
        for cod, (*_x, criado, iniciado, concluido) in plano.items():
            db.execute("UPDATE item SET criado_em = ?, iniciado_em = COALESCE(?, iniciado_em), concluido_em = COALESCE(?, concluido_em), "
                       "aceito_em = CASE WHEN aceito_em IS NOT NULL THEN COALESCE(?, aceito_em) END WHERE id = ?",
                       (dia(criado), dia(iniciado) if iniciado is not None else None, dia(concluido) if concluido is not None else None,
                        dia(concluido + 1) if concluido is not None else None, por_codigo[cod]))
        for cod in (1, 6):
            db.execute("UPDATE item SET criado_em = ? WHERE id = ?", (dia(-42), por_codigo[cod]))
        db.execute("UPDATE linha_base SET criada_em = ? WHERE projeto_id = ?", (dia(-35) + " 10:00:00", pid))
        db.commit()

    c.post(f"/p/{pid}/medicao", data={"limite_variacao": "10", "plano_excecao":
           "Se prazo ou custo ficarem críticos: reunião com a Dra. Lúcia em até 3 dias para decidir entre reduzir o escopo da release 1.0, "
           "adiar a lista de espera ou usar a reserva de gerenciamento."})
    mi = f"/p/{pid}/medicao/indicadores"
    c.post(mi, data={"nome": "Defeitos abertos", "tipo": "antecedente", "categoria": "entrega", "unidade": "defeitos", "direcao": "menor",
                     "meta": "2", "limite": "5", "relevancia": "Muitos defeitos abertos antecipam atraso e retrabalho na release 1.0."})
    c.post(mi, data={"nome": "Moral da equipe", "tipo": "antecedente", "categoria": "partes", "unidade": "pontos (1 a 5)", "direcao": "maior",
                     "meta": "4", "limite": "3", "relevancia": "Pesquisa rápida na retrospectiva (seção 2.7.2.6)."})
    c.post(mi, data={"nome": "Consultas agendadas online", "tipo": "resultado", "categoria": "valor", "unidade": "%", "direcao": "maior",
                     "meta": "40", "relevancia": "Objetivo do termo de abertura: 40% das consultas online em 6 meses."})
    for mid, valores in [(1, [(-35, 1), (-21, 2), (-7, 3), (-1, 4)]), (2, [(-29, 4.5), (-15, 4), (-1, 4.2)]), (3, [(-14, 6), (-7, 9), (-1, 13)])]:
        for n, v in valores:
            c.post(f"{mi}/{mid}", data={"valor": str(v).replace(".", ","), "data": dia(n)})
    c.post(f"/p/{pid}/medicao/relatorios", data={"resumo": "MVP avançando: agendamento pelo celular e agenda da recepção aceitos. "
           "Prazo e custo em atenção; integração com a TI ainda bloqueada.",
           "realizacoes": "I-2 Marcar consulta pelo celular (aceito)\nI-7 Ver a agenda do dia (aceito)\nI-10 Criptografia dos dados (concluído)",
           "proximos_passos": "Concluir I-4 Remarcar ou cancelar consulta\nResolver Q-2 Servidor de homologação\nDecisão sobre M-2 (banco de dados da TI)"})

    # Equipe, ciclo de vida e tailoring (v6)
    eq = f"/p/{pid}/equipe"
    for nome, papel, local, hab, lac, plano, mot in [
            ("Denner Ribeiro", "Gerente do projeto e product owner", "presencial", "Scrum, Jira, levantamento de requisitos", "", "", "Responsabilidade"),
            ("Ana Souza", "Desenvolvedora back-end", "remoto", "Python, Flask, SQL", "Testes automatizados", "Mentoria com o Bruno nas sprints 4 e 5", "Desafio"),
            ("Bruno Lima", "Desenvolvedor front-end", "presencial", "JavaScript, acessibilidade, testes", "", "", "Crescimento pessoal"),
            ("Carla Dias", "Designer de UX", "hibrido", "Pesquisa com usuários, protótipos", "Integração com WhatsApp", "", "Fazer diferença")]:
        c.post(eq, data={"nome": nome, "papel": papel, "local": local, "habilidades": hab, "lacunas": lac,
                         "plano_desenvolvimento": plano, "motivador": mot, "dedicacao": "integral" if nome != "Carla Dias" else "parcial"})
    c.post(eq, data={"acao": "lideranca", "modelo_lideranca": "distribuida", "estagio_equipe": "normatizacao"})
    c.post(f"{eq}/acordo", data={
        "acordo_valores": "Transparência sobre problemas e atrasos; respeito às opiniões; discordar é bem-vindo, com argumentos.",
        "acordo_comunicacao": "Slack para o dia a dia, resposta em até 4 horas úteis; decisões importantes registradas no app.",
        "acordo_decisoes": "Técnicas: a equipe decide por punho de cinco. Escopo e prazo: o product owner, ouvindo a equipe. Orçamento: a patrocinadora.",
        "acordo_conflitos": "Focar no problema, não na pessoa; conversar em particular primeiro; se não resolver, levar à retrospectiva.",
        "acordo_reunioes": "Daily às 9h15 (15 min); planejamento e revisão quinzenais; quarta à tarde sem reuniões."})
    for desc in ["Priorizar o backlog", "Aprovar mudanças de escopo", "Publicar em produção", "Comunicar a recepção sobre novidades"]:
        c.post(f"{eq}/raci", data={"acao": "linha", "descricao": desc})
    with app.app_context():
        from db import get_db
        m = {r["nome"].split()[0]: r["id"] for r in get_db().execute("SELECT id, nome FROM membro WHERE projeto_id = ?", (pid,))}
    raci_papeis = {1: {"Denner": "A", "Ana": "C", "Bruno": "C", "Carla": "R"}, 2: {"Denner": "R", "Ana": "C", "Bruno": "I"},
                   3: {"Denner": "A", "Ana": "R", "Bruno": "R", "Carla": "I"}, 4: {"Denner": "A", "Carla": "R", "Ana": "I", "Bruno": "I"}}
    dados = {"acao": "salvar"}
    for linha, papeis in raci_papeis.items():
        for nome, papel in papeis.items():
            dados[f"p_{linha}_{m[nome]}"] = papel
    c.post(f"{eq}/raci", data=dados)
    for dias, notas, obs in [(-15, dict(comunicacao=4, entendimento=4, propriedade=3, confianca=3, colaboracao=4, adaptabilidade=3,
                                         resiliencia=3, empoderamento=4, reconhecimento=3), "Retrospectiva da sprint 2"),
                             (-1, dict(comunicacao=4, entendimento=5, propriedade=4, confianca=4, colaboracao=4, adaptabilidade=4,
                                        resiliencia=3, empoderamento=4, reconhecimento=2), "Retrospectiva da sprint 3")]:
        c.post(f"{eq}/saude", data={"data": dia(dias), "participantes": "4", "observacoes": obs, **{k: str(v) for k, v in notas.items()}})
    c.post(f"/p/{pid}/fases", data={"acao": "sugeridas"})
    c.post(f"/p/{pid}/fases/1", data={"nome": "Início", "inicio": dia(-49), "fim": dia(-43), "status": "concluida",
           "objetivo": "Visão do produto, equipe e backlog inicial.", "criterios_saida": "Declaração de visão escrita\nBacklog inicial priorizado",
           "criterio_ok": ["0", "1"], "revisao_decisao": "seguir", "revisao_por": "Dra. Lúcia Prado", "revisao_notas": "Visão validada com a recepção."})
    c.post(f"/p/{pid}/fases/2", data={"nome": "Iterações e releases", "inicio": dia(-42), "fim": dia(60), "status": "em_andamento",
           "objetivo": "Iterações com revisão do cliente ao fim de cada uma e repriorização do backlog.",
           "criterios_saida": "Itens de maior prioridade entregues\nPartes interessadas satisfeitas com as entregas", "criterio_ok": ["1"]})
    tl = f"/p/{pid}/tailoring"
    for tipo, elemento, motivo, origem in [
            ("remover", "Relatório de status semanal por e-mail", "A demo quinzenal com a patrocinadora já cumpre esse papel", "Retrospectiva da sprint 1"),
            ("adicionar", "Revisão de segurança a cada release", "Dados de saúde dos pacientes (LGPD)", "Exigência da organização"),
            ("ajustar", "Limite de 2 itens em andamento no quadro", "Itens ficavam parados esperando revisão", "Retrospectiva da sprint 3")]:
        c.post(tl, data={"acao": "decisao", "tipo": tipo, "elemento": elemento, "motivo": motivo, "origem": origem})
    c.post(tl, data={"acao": "respostas", "criticidade": "Média: dados de saúde exigem cuidado com a LGPD", "tecnologia": "Estável (web)",
                     "requisitos": "Mudam com o feedback da recepção e dos pacientes", "incremental": "Sim, a cada sprint",
                     "tamanho": "4 pessoas, 1 em tempo parcial", "geografia": "Uma pessoa remota", "cliente": "Sim: demo quinzenal com a recepção",
                     "adesao": "Alta na clínica; a TI ainda resiste"})


    # Princípios (v7)
    pr = f"/p/{pid}"
    c.post(f"{pr}/partes/engajamento", data={f"atual_{ids[1]}": "2", f"desejado_{ids[1]}": "4", f"metodo_{ids[1]}": "interativa",
           f"frequencia_{ids[1]}": "Quinzenal", f"estrategia_{ids[1]}": "Envolver a TI na decisão de arquitetura e mostrar o plano de segurança antes de cada integração."})
    for sid, dias, res, sat in [(ids[1], 6, "Revisão conjunta da arquitetura de integração", 3), (ids[4], 9, "Validação do fluxo de consentimento", 4)]:
        c.post(f"{pr}/partes/monitoramento", data={"parte_id": str(sid), "data": (hoje - timedelta(days=dias)).isoformat(), "metodo": "interativa",
               "tipo": "verbal_formal", "resumo": res, "satisfacao": str(sat)})
    c.post(f"{pr}/business-case", data={
        "bc_necessidade": "A recepção atende 600 ligações por semana só para agendar; 18% dos pacientes faltam sem avisar.",
        "bc_justificativa": "Cada falta custa em média R$ 180 em horário ocioso. Sem agendamento online, a clínica perde pacientes para concorrentes que já oferecem.",
        "bc_estrategia": "Plano estratégico 2026 da clínica: atendimento digital e redução de custos administrativos.",
        "bc_alternativas": "Contratar mais uma recepcionista (resolve a fila, não as faltas); comprar um sistema pronto (não integra com o prontuário); não fazer nada.",
        "bc_beneficios_nao_financeiros": "Pacientes satisfeitos; recepção com mais tempo para atendimento presencial; dados para planejar a agenda.",
        "bc_investimento": "50.000", "bc_beneficio_anual": "30.000", "bc_custo_anual": "6.000", "bc_horizonte_anos": "3", "bc_taxa": "12"})
    conf = f"{pr}/conformidade"
    for area, req, como, resp, prazo, status, evid in [
            ("privacidade", "Consentimento do paciente para lembretes por WhatsApp (LGPD)", "Termo de consentimento no cadastro, com opção de revogar",
             "Encarregado LGPD", dia(-10), "atendido", "Tela de consentimento aprovada pelo DPO na sprint 2"),
            ("seguranca", "Dados de saúde criptografados em repouso e em trânsito", "Criptografia no banco e HTTPS obrigatório", "Ana",
             dia(-3), "atendido", "Relatório da revisão de segurança da release 0.3"),
            ("legal", "Termos de uso e política de privacidade publicados", "Redação com o jurídico da clínica", "Denner", dia(20), "em_andamento", ""),
            ("etica", "Lista de espera sem favorecimento", "Ordem de chegada, com prioridade só para casos clínicos definidos pela diretoria",
             "Dra. Lúcia Prado", dia(35), "pendente", ""),
            ("pessoas", "Recepção não perde postos de trabalho", "Realocar tempo para atendimento presencial; combinado com a diretoria",
             "Dra. Lúcia Prado", None, "atendido", "Ata da reunião de diretoria"),
            ("ambiental", "Fim das fichas de papel de agendamento", "Menos impressão; descarte seguro das fichas antigas", "Recepção",
             dia(60), "pendente", ""),
            ("social", "Acessibilidade para pacientes idosos e com deficiência", "Contraste, fonte grande e leitor de tela; agendamento por telefone continua",
             "Bruno", dia(30), "em_andamento", ""),
            ("financeira", "Notas fiscais do fornecedor de mensagens", "Não se aplica: a clínica já tem contrato corporativo", "", None, "nao_aplicavel", "")]:
        c.post(conf, data={"area": area, "requisito": req, "como_atender": como, "responsavel": resp, "prazo": prazo or "",
                           "status": "pendente" if status == "atendido" else status})
        if status == "atendido":
            with app.app_context():
                rid = get_db().execute("SELECT MAX(id) FROM conformidade WHERE projeto_id = ?", (pid,)).fetchone()[0]
            c.post(conf, data={"registro_id": rid, "area": area, "requisito": req, "como_atender": como, "responsavel": resp,
                               "prazo": prazo or "", "status": "atendido", "evidencia": evid})
    dec = f"{pr}/decisoes"
    for d in [
            dict(data=dia(-35), titulo="WhatsApp em vez de SMS para lembretes", contexto="Lembretes reduzem faltas; pacientes ignoram SMS.",
                 alternativas="SMS; e-mail; ligação automática", decisao="WhatsApp, com SMS como contingência (risco R-3).",
                 decidido_por="Dra. Lúcia Prado", envolvidos="Equipe, recepção e Encarregado LGPD",
                 efeitos="Custo mensal da API; novo requisito de consentimento (LGPD); dependência de fornecedor."),
            dict(data=dia(-20), titulo="Integrar um sistema legado por release", contexto="Três sistemas legados se afetam entre si.",
                 alternativas="Integrar tudo no MVP; integrar por release", decisao="Por release, começando pela agenda.",
                 decidido_por="Equipe (punho de cinco)", envolvidos="Carlos Mendes (TI)",
                 efeitos="MVP sai antes; pagamento online fica para a release 2; TI participa de cada integração.", revisar_em=dia(25))]:
        c.post(dec, data={"acao": "decisao", **d})
    for desc, falsa, como, ate in [
            ("A maioria dos pacientes usa WhatsApp", "Lembretes não chegam e as faltas não caem", "Pesquisa no balcão com 50 pacientes", dia(-12)),
            ("A recepção terá 2 horas por semana para treinamento", "A adoção atrasa e o benefício demora", "Confirmar escala com a diretoria", dia(-5)),
            ("O sistema de prontuário tem API documentada", "A integração vira um projeto à parte", "Prova de conceito na sprint 4", dia(10))]:
        c.post(dec, data={"acao": "premissa", "descricao": desc, "se_falsa": falsa, "como_validar": como, "validar_ate": ate})
    c.post(dec, data={"acao": "status_premissa", "registro_id": "1", "status": "validada"})
    c.post(dec, data={"acao": "status_premissa", "registro_id": "2", "status": "validada"})
    with app.app_context():
        lid = get_db().execute("SELECT MIN(id) FROM licao WHERE projeto_id = ?", (pid,)).fetchone()[0]
    c.post(f"{pr}/trabalho/licoes", data={"acao": "aplicar", "licao_id": str(lid), "aplicada": "1"})
    ad = f"{pr}/mudanca-organizacional"
    c.post(ad, data={"acao": "estados", "mudanca_estado_atual": "Agendamento só por telefone, em fichas de papel; confirmação manual na véspera.",
                     "mudanca_estado_futuro": "Pacientes agendam pelo app; a recepção acompanha o painel e só trata exceções; lembretes automáticos."})
    grupos = [
        ("Recepcionistas", ids[2], "Deixam de anotar em fichas e passam a usar o painel do app.", 5, 3, "Medo de perder o controle da agenda",
         "Treinamento de 2 h por sprint; recepcionista-referência; manual impresso no balcão", 90, "em_transicao", [(-14, 30), (-7, 55), (-1, 70)]),
        ("Pacientes", ids[3], "Agendam e remarcam pelo celular.", 3, 3, "Pacientes idosos preferem ligar",
         "Cartaz e QR code na recepção; telefone continua disponível; mensagem de boas-vindas", 40, "preparando", [(-7, 8), (-1, 14)]),
        ("Médicos", None, "Veem a agenda do dia no app em vez da lista impressa.", 2, 4, "", "Demonstração na reunião clínica mensal", 80, "nao_iniciado", []),
    ]
    for nome, parte, muda, imp, pront, resist, acoes, meta, status, medicoes in grupos:
        c.post(ad, data={"grupo": nome, "parte_id": str(parte or ""), "o_que_muda": muda, "impacto": str(imp), "prontidao": str(pront),
                         "resistencias": resist, "acoes": acoes, "meta_adocao": str(meta)})
        with app.app_context():
            gid = get_db().execute("SELECT MAX(id) FROM adocao_grupo WHERE projeto_id = ?", (pid,)).fetchone()[0]
        c.post(ad, data={"grupo_id": str(gid), "grupo": nome, "parte_id": str(parte or ""), "o_que_muda": muda, "impacto": str(imp),
                         "prontidao": str(pront), "resistencias": resist, "acoes": acoes, "meta_adocao": str(meta), "status": status})
        for d_, v in medicoes:
            c.post(ad, data={"acao": "medir", "grupo_id": str(gid), "data": dia(d_), "adocao": str(v)})
    c.post(f"{pr}/principios", data={"status_0": "parcial", "reflexao_0": "Conformidade bem cuidada; ainda falta fechar os termos de uso e o impacto ambiental.",
                                      "status_11": "parcial", "reflexao_11": "A recepção está avançando; pacientes idosos precisam de mais apoio."})
    # v8: aquisições, recursos físicos e plano de comunicação (informação necessária)
    sup = f"{pr}/suprimentos"
    c.post(sup, data={"acao": "aquisicao", "item": "API de mensagens por WhatsApp", "decisao": "comprar", "fornecedor": "Zap Mensagens Ltda.",
                      "documento": "rfq", "contrato": "preco_fixo", "valor": "4.800", "necessario_em": dia(20), "status": "contratada",
                      "criterios": "Preço, prazo, 99,5% de disponibilidade"})
    c.post(sup, data={"acao": "aquisicao", "item": "Módulo de lembretes", "decisao": "fazer", "status": "planejada"})
    c.post(sup, data={"acao": "recurso", "nome": "Servidor de homologação", "tipo": "equipamento", "quantidade": "1", "unidade": "un.",
                      "necessario_em": dia(25), "antecedencia_dias": "30", "status": "planejado"})
    # v14: complexidade, MoSCoW, dependências e datas para o Gantt
    c.post(f"/p/{pid}/complexidade", data={"cynefin": "complexo", "stacey_requisitos": "3", "stacey_tecnologia": "3"})
    with app.app_context():
        from datetime import date as _date, timedelta as _td
        from db import get_db as _gdb
        db = _gdb()
        itens = db.execute("SELECT id, codigo FROM item WHERE projeto_id = ? ORDER BY codigo", (pid,)).fetchall()
        moscow = ["must", "must", "should", "must", "could", "should", "wont", "could", "should", "must"]
        for n, it in enumerate(itens):
            db.execute("UPDATE item SET moscow = ? WHERE id = ?", (moscow[n % len(moscow)], it["id"]))
        folhas_ = [r["id"] for r in db.execute("SELECT id FROM item WHERE projeto_id = ? AND id NOT IN (SELECT pai_id FROM item WHERE pai_id IS NOT NULL) ORDER BY codigo", (pid,))]
        hoje = _date.today()
        for n, iid in enumerate(folhas_):
            ini = hoje + _td(days=-14 + 7 * n)
            db.execute("UPDATE item SET inicio_planejado = COALESCE(inicio_planejado, ?), fim_planejado = COALESCE(fim_planejado, ?) WHERE id = ?",
                       (ini.isoformat(), (ini + _td(days=9)).isoformat(), iid))
        for a, b in zip(folhas_, folhas_[1:3]):
            db.execute("INSERT OR IGNORE INTO item_dependencia (item_id, depende_de) VALUES (?, ?)", (b, a))
        db.commit()
    return pid


if __name__ == "__main__":
    pid = criar()
    print(f"Projeto de exemplo criado: http://localhost:5000/p/{pid}")
