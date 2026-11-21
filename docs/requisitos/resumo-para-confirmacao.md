# Resumo da elicitação, para confirmação

Este resumo junta o que a elicitação decidiu, da Q1 à Q211, para o responsável pelo produto confirmar antes da ERS. Ele não decide nada novo: cada item cita a pergunta do [registro de decisões](decisoes-elicitacao.md), e é o registro que vale. Se algum item parecer diferente do que foi decidido, o registro prevalece e o resumo é corrigido. A ligação de cada requisito funcional às regras e às decisões está em [rf-regras-decisoes.md](rf-regras-decisoes.md) (Q209). As perguntas que surgiram ao montar o resumo estão na seção 9.

**Confirmado em 20/11/2026:** o responsável pelo produto confirmou este resumo, as interpretações da seção 9.2 e as propostas das Q212 e Q213 com "Sim".

Os nomes dos papéis seguem a Q210: gerente de projetos, gerente do projeto e gerente de apoio. Nas decisões anteriores à Q210, eles aparecem como estagiário, estagiário responsável e estagiário de apoio.

## 1. O que é o Octante

- Uma ferramenta de trabalho de um PMO para gerenciar projetos reais seguindo o PMBOK 7. O ensino vem embutido no uso, sem "modo treinamento" (Q1).
- Os projetos são, na maioria, internos de TI e de melhoria de processos, em abordagem híbrida (Q12).
- Um PMO só, com 1 a 3 supervisores e até uns 15 gerentes de projetos. Cada gerente de projetos conduz de 1 a 3 projetos, e um projeto tem no máximo dois: o gerente do projeto e um gerente de apoio (Q4, Q8, Q210).
- A única referência é o PMBOK 7, edição em inglês (Q5, Q30; [ADR 0001](../adr/0001-pmbok-7-como-referencia.md)). Regra de outra fonte é não conformidade e sai, mesmo rotulada (Q49, Q113; [ADR 0005](../adr/0005-origem-de-cada-regra-na-tela.md)). Onde o PMBOK 7 não trata do assunto, a regra é do PMO, por decisão explícita, e pode se apoiar numa lei ou norma, como a LGPD e a WCAG 2.1 (Q38, Q49, Q113).
- Cada regra mostra a origem na tela: a página do PMBOK 7 ou "regra do PMO" (ADR 0005; Q153). Os campos do PMBOK aparecem primeiro, e os do PMO num bloco "Campos do PMO" (Q68). Os termos traduzidos mostram o original em inglês (Q113).
- A elicitação produz a ERS e as histórias de usuário com critérios de aceite, como issues no GitHub, além do glossário e das regras. Cada funcionalidade do protótipo é marcada como confirmada, alterada ou descartada (Q6, Q13).
- O protótipo evolui, e não é reescrito do zero, mas nenhuma regra vale só por já estar escrita e testada (Q46). A versão nova começa com o banco limpo (Q39).

## 2. Pessoas, papéis e acesso

- Só gerentes de projetos e supervisores entram no sistema. Patrocinador, cliente, equipe e diretoria são **destinatários**: recebem os documentos gerados, sem login (Q3).
- **Gerente do projeto:** o gerente de projetos que responde pelo projeto ao supervisor. Todo projeto tem um, e ele entra sozinho na equipe do projeto (Q8, Q60, Q114, Q210).
- **Gerente de apoio:** opcional; edita tudo, mas não responde pelo projeto (Q8, Q114).
- **Supervisor:** revisa o trabalho e não é o gerente do projeto (Q2, Q60). O **supervisor designado** cria o projeto e recebe as revisões; os outros supervisores veem todos os projetos e revisam como substitutos (Q9, Q27).
- **Administrador:** papel extra, dado só a um supervisor, que cuida de usuários, backups, lixeira e LGPD. Sempre há pelo menos um ativo (Q7, Q22, Q52; [ADR 0004](../adr/0004-administrador-somente-supervisor.md)).
- O gerente de projetos vê os próprios projetos, o projeto de exemplo e os projetos com acesso de consulta, que o supervisor designado ou outro supervisor concede, só para leitura (Q35, Q43).
- O supervisor também pode editar. Na edição simultânea, fica a versão dele, o gerente é avisado e vê o que mudou, e o histórico marca a edição. A edição do supervisor não anula uma liberação (Q34, Q40).
- O Administrador cria e desativa usuários, muda o tipo da conta e dá ou tira o papel de Administrador. Ninguém desativa a própria conta (Q52).
- **Primeiro acesso:** a tela pede o código de instalação, que só quem tem acesso ao servidor vê. O primeiro usuário nasce supervisor, com o papel de Administrador (Q52, Q188).
- **Login:** senha de 8 ou mais caracteres (Q51). Cinco senhas erradas trancam a conta só naquela máquina, por 5 minutos, pelo endereço real, com a contagem no banco (Q186, Q186b). A sessão termina com 3 horas sem uso ou 12 horas depois da entrada, e trocar a senha encerra as outras sessões (Q51, Q187). A pessoa entra uma vez por sessão e vê as telas do seu papel (Q196).
- **Desligamento:** os projetos em andamento passam antes a outro gerente, e desativar a conta é obrigatório. O Administrador recebe um alerta pelo gerente de projetos ativo que já teve projeto e hoje não tem nenhum (Q28, Q32, Q183, Q210).
- **Projeto de exemplo:** um só, somente consulta para todos, que só o Administrador recria (Q53).

## 3. Como o trabalho flui

- O supervisor cria o projeto, vira o supervisor designado e escolhe o gerente do projeto e, se quiser, um gerente de apoio. O gerente de projetos não cria projetos (Q27).
- **Revisão não é aprovação.** O supervisor revisa e libera ou devolve com comentário. A aprovação é de quem tem autoridade, como o patrocinador ou a autoridade de mudança do projeto; é dada por fora e registrada no Octante, com quem e quando (Q14, Q69).
- **Revisão obrigatória** para o termo de abertura, o relatório de status, a mudança, o encerramento e o tailoring. Para os outros registros, a revisão é opcional (Q10, Q29, Q33). Só vai para revisão o que está "pronto para revisão", com os campos que o nível de exigência pede (Q56).
- Alterar o que foi liberado exige nova revisão, e o documento gerado mostra quem liberou e quando (Q15). A devolução vai para quem enviou, com cópia ao gerente do projeto, e o comentário de devolução é o canal de feedback (Q8, Q19).
- O Octante gera o documento (PDF ou impressão), e o gerente entrega por fora (Q11). O e-mail fica para o futuro (Q41, Q42).
- O termo aprovado trava e só muda por mudança aprovada, que gera uma nova versão e guarda a anterior (Q62). O limite de variação e o limite de risco fazem parte do termo (Q177).
- O **nível de exigência** é por projeto, decidido pelo supervisor designado, e o gerente não pode reduzi-lo (Q17). A **cadência de relatório** também é por projeto, e o atraso gera alerta (Q16, Q158).
- **Núcleo e módulos opcionais:** um núcleo sempre presente e módulos que o tailoring liga (Q18, Q31). O módulo desligado fica inacessível, com os seus alertas, as suas etapas do guia e os seus itens do encerramento; ligado de novo, os dados voltam (Q57, Q174a). Ajustes ao núcleo da Q31: entraram o registro de contatos (Q108), a reserva de contingência (Q172a), a avaliação do risco geral (Q172b) e o plano de exceção (Q174b); o pré-mortem saiu (Q102).
- **Tailoring:** o gerente propõe pelo assistente de abordagem, e o supervisor revisa junto com o termo. Mudar depois exige nova revisão (Q33).
- **Encerramento:** o gerente prepara o checklist e a avaliação final, que passam por revisão. O aceite final é registrado, com quem aceitou, escolhido entre as partes interessadas, e quando. Só o supervisor encerra, cancela ou reabre, e cancelar e reabrir exigem justificativa (Q29, Q63, Q65, Q109). O projeto encerrado fica só para consulta, inclusive a tela de encerramento (Q65).
- **Excluir projeto:** só o Administrador, e só o projeto criado por engano. O projeto real é cancelado (Q54).
- O supervisor vê o trabalho por gerente de projetos e o resumo dos alertas de cada projeto, com os altos em destaque (Q19, Q36).
- **Parecer do supervisor:** texto livre, escrito quando o supervisor quiser (Q20). Todos os supervisores leem, menos a própria pessoa avaliada, mesmo depois de passar a supervisor (Q21, Q211). Ao escrever, o supervisor vê indicadores de apoio, que não viram nota (Q23). O parecer sai como documento gerado, só por supervisor (Q24), e fica até 5 anos depois que a pessoa deixa de ser gerente de projetos, com o prazo configurável (Q25, Q211). Num pedido do titular, o Administrador pode entregá-lo à pessoa, depois de um aviso (Q191b).

## 4. Decisões por área

### 4.1 Partes interessadas

- As cinco etapas do PMBOK 7: identificar, analisar, priorizar, engajar e monitorar (Q104 a Q113).
- A categoria da parte (Figura 2-2 do PMBOK) passa a ser obrigatória, e o nome repetido é barrado também na edição (Q111, Q170). A parte ganha o campo de e-mail (Q41).
- A análise de cada parte é sigilosa: só o gerente do projeto, o gerente de apoio e os supervisores a veem, e ela fica fora do acesso de consulta e dos documentos gerados (Q104).
- A priorização usa o diagrama de dispersão poder × interesse, sem os quadrantes e os nomes de Mendelow, e a ordem é a que o gerente define, com uma sugestão do app (Q105b).
- O engajamento atual e o desejado vão de 1 a 5, sem nomes, na matriz de engajamento, que é opcional. No núcleo, o plano de comunicação diz como, com que frequência e por quem (Q106b).
- A saliência mostra quantos dos três atributos do PMBOK a parte tem, sem as sete categorias (Q107b).
- O registro de contatos fica no núcleo, e a nota de satisfação continua opcional (Q108). A parte conta como monitorada quando tem contato dentro do prazo da frequência do seu plano (Q169a).
- O patrocinador e quem dá o aceite são escolhidos na lista de partes, e o patrocinador do termo entra sozinho na lista (Q109).
- Só se exclui a parte sem contato e sem vínculo; nos outros casos, ela é inativada (Q110).

### 4.2 Equipe

- O gerente do projeto entra sozinho na equipe, com o papel "Gerente do projeto", e o gerente de apoio com o papel "Equipe de gerenciamento do projeto". O supervisor não entra na equipe (Q114).
- Só se exclui o membro sem vínculo; nos outros casos, ele é liberado, depois de passar as suas pendências a outro membro (Q115).
- O acordo de trabalho tem as três partes do PMBOK 7: valores, acordos e diretrizes de operação, e comportamento esperado (Q116).
- A matriz RACI avisa a linha incompleta, sem impedir a gravação: cada linha tem exatamente um A e pelo menos um R, e a mesma pessoa pode ser A e R (Q117, Q121). As colunas aceitam também partes interessadas (Q118).
- Habilidades, lacunas, plano de desenvolvimento e motivador dos membros são sigilosos e entram na anonimização (Q119).
- Os estágios de Tuckman mostram o original em inglês, e a equipe escolhe o estágio livremente (Q120).

### 4.3 Abordagem, ciclo de vida e tailoring

- A cadência é conferida pelo servidor (Q122). Os 15 fatores de seleção continuam; a escala, a média e os cortes são regras do PMO; a sugestão de abordagem é informativa (Q123). Escolher uma abordagem diferente da sugerida exige justificativa, e a revisão mostra os fatores e os dados do projeto que apontam para o outro lado (Q136).
- Uma abordagem por projeto, e "híbrida" inclui o projeto cujas entregas usam abordagens diferentes (Q124).
- O Cynefin tem os cinco contextos do PMBOK 7, e o Stacey usa a incerteza dos requisitos e a da tecnologia, sem sugerir abordagem (Q125, Q126).
- Nos modelos de projeto, "Software ágil (Scrum)" vira "Software adaptativo", e as fontes de risco seguem a lista oficial (Q127). As fases sugeridas foram corrigidas pelo PMBOK (Q128).
- A revisão de fase decide seguir, seguir com modificações (que exige descrever as modificações), encerrar ou repetir. Quem decidiu é escolhido numa lista; a fase concluída só reabre com "repetir"; só se exclui a fase sem revisão (Q129, Q130, Q132, Q179). A fase em andamento sem critérios de saída gera alerta (Q178), e a revisão de fase lembra de rever o tailoring (Q137).
- O tailoring tem as 17 perguntas do PMBOK 7 (Q133). O diagnóstico da Tabela 3-1 continua, com os limiares do PMO e a cadência de relatório (Q134, Q180).

### 4.4 Planejamento

- No termo de abertura, o gerente vem sozinho, e o patrocinador e o gerente aparecem primeiro, antes de propósito, objetivos e critérios de sucesso (Q60, Q61, Q68). O patrocinador é exigido em todos os níveis, e o termo registra a autoridade de mudança (Q69, Q112).
- A declaração de visão é texto livre, sem o gerador no formato de Moore (Q66).
- A iteração ganha tela de edição, e a premissa atrasada aparece na agenda. Capacidade estourada, item com prazo vencido e conflito no Gantt viram alertas (Q67, Q158).
- Termo não aprovado gera alerta médio, e projeto sem declaração de visão gera alerta informativo, em qualquer abordagem (Q154).

### 4.5 Trabalho do projeto

- A mudança fica pronta para revisão com solicitante, valor esperado, os seis impactos e os riscos novos (Q70, Q112). O fluxo é fixo: rascunho, em revisão, liberada, aguardando decisão, aprovada ou rejeitada e implementada; a rejeitada é definitiva; editar e excluir só em rascunho (Q72, Q73b). Quem decidiu e o solicitante vêm da lista de partes e membros (Q176). No adaptativo, o trabalho novo vira item do backlog (Q71).
- A questão tem responsável obrigatório, escolhido entre os membros, e prazo obrigatório no nível rigoroso (Q74). Resolver exige a descrição da resolução (Q112). Só se exclui a questão aberta que nunca mudou de status e não veio de um risco; nos outros casos, resolve-se ou cancela-se com justificativa (Q73, Q168). A questão que o app abre quando uma ameaça ocorre herda o responsável do risco ou, sem ele, o gerente do projeto (Q167).
- A lição aprendida pode ir para a lixeira (Q73).

### 4.6 Entrega

- A linha de base do escopo só muda por mudança aprovada (Q79).
- O item vai de a fazer a em andamento, concluído e aceito; o aceito é definitivo, e o defeito depois do aceite vira item novo. Cancelar exige motivo; só se exclui o item a fazer, fora da linha de base e nunca aceito (Q80, Q81). Quem aceitou é escolhido entre as partes (Q82).
- Com o limite de trabalho em andamento atingido, o app impede mover mais um item (Q83).
- O requisito mostra os seis critérios do PMBOK, e "completo" vale para o conjunto, conferido ao gravar a linha de base (Q84, Q84b).
- O benefício realizado exige o resultado medido (Q85).

### 4.7 Medição

- A regra 0/100 e o valor planejado linear ficam como regras do PMO (Q86). O custo real soma só os itens que entram no valor agregado e no planejado (Q87).
- O limite de variação é por projeto, com 10% por padrão (Q88).
- No relatório de status, cada dimensão em vermelho exige explicação; os indicadores congelam ao enviar para revisão; depois de liberado, o relatório nunca muda (Q89, Q91). Sem questões registradas, a dimensão mostra "sem dados" (Q90).
- Marcar um resultado como atendido exige evidência (Q92). O indicador mostra os critérios SMART como apoio (Q93).
- O plano de exceção fica no núcleo, junto do semáforo (Q174b).

### 4.8 Incerteza

- O limite de risco e a cadência de revisão são por projeto (Q95), e a conversão da probabilidade em percentual aparece na tela (Q96).
- O risco pode nascer só com o título. Para passar a "em resposta", precisa de probabilidade, impacto, estratégia e responsável; acima do limite, também do risco residual e dos riscos secundários (Q97, Q166b, Q173).
- A oportunidade que ocorreu registra o ganho, sem virar questão (Q98). Só se exclui o risco aberto, sem histórico nem vínculos (Q99). Escalar exige dizer a quem e quando (Q100).
- O pré-mortem sai (Q102). A reserva de contingência e a avaliação do risco geral ficam no núcleo (Q172a, Q172b).

### 4.9 Princípios e valor

- O business case calcula o ROI pela definição do PMBOK e a razão benefício-custo, no lugar do selo "viável" (Q138). A data de revisão só muda quando o conteúdo muda ou com a marca "revisei, sem mudanças" (Q139).
- "Prontidão" vira "capacidade de absorção" (Q140).
- O registro de premissas guarda premissas e restrições (Q141). O registro de decisões fica como regra do PMO (Q142).
- A autoavaliação dos princípios não tem nível calculado nem alerta: os sinais do projeto são só informação, e "atendido" exige reflexão (Q143).
- Razão benefício-custo abaixo de 1,0 sem benefícios não financeiros e custo previsto acima do investimento além do limite de variação geram alertas altos (Q181, Q182).

### 4.10 Aquisições e recursos físicos

- A compra segue planejada, em licitação ou cotação, contratada, entregue e encerrada; fazer internamente segue planejada, entregue e encerrada. Cancelar exige motivo, e só se exclui a aquisição planejada sem vínculo (Q145).
- A nota do fornecedor só é exigida na compra (Q146), e contratar depois de uma licitação exige os critérios de seleção (Q175).
- O fornecedor contratado entra sozinho como parte interessada (Q147).
- O recurso físico só se exclui enquanto está planejado (Q148).

### 4.11 Guia e ensino

- Os blocos do guia são os cinco grupos de processos do PMBOK 7, que não são fases (Q149).
- As etapas "Prazo e orçamento", "Engajar as pessoas", "Equipe" e "Riscos" contam como feitas pelos critérios corrigidos (Q150, Q169b, Q169c, Q169d).
- O glossário do app, a ajuda das telas e as sugestões de tailoring seguem o GLOSSARY e o PMBOK 7 (Q151, Q152).
- A completude vira "pronto para revisão" ou "falta: …" (Q56).
- As preferências de dicas e de modo essencial ficam na conta do usuário (Q202).

### 4.12 Dados, histórico e backup

- O histórico guarda tudo, menos a senha; há lixeira; os backups têm rotação (Q51). O banco recusa alterar ou apagar o histórico, salvo nas rotinas permitidas, e a restauração de um backup fica registrada (Q194).
- Os backups são compactados; a tela Dados mostra o espaço usado; há alerta de espaço e de backup que falhou (Q195). O Administrador baixa uma cópia por semana, e o app registra quem baixou e quando (Q44, Q184).
- A anonimização vale para o projeto encerrado ou cancelado e é feita pelo Administrador. Ela troca os nomes das partes e dos membros por rótulos neutros e apaga o contato, as crenças, as expectativas, o e-mail e a análise das partes, os textos dos contatos, os dados pessoais dos membros, o histórico e a lixeira. Os textos livres não são varridos, e a tela avisa disso (Q59, Q192). O prazo de guarda é de 5 anos por padrão, com alerta para o Administrador (Q193).

## 5. Alertas

- Cada alerta é um limite com uma ação sugerida, em três níveis: **alto**, o limite foi ultrapassado ou o dano já acontece; **médio**, o limite está perto ou falta algo que uma regra exige; **informativo**, lembrete sem prazo. O alerta não bloqueia nada e mostra a origem (Q153).
- O alerta aparece no projeto; o supervisor vê o resumo por projeto, com os altos em destaque (Q36); os alertas do Administrador aparecem no portfólio (Q183, Q184, Q193, Q195). Em documento gerado, o alerta sobre uma pessoa sai sem o nome (Q104). Com o módulo desligado, os alertas dele não aparecem (Q174a).
- Das regras do protótipo, 49 têm o nível de alerta decidido nas rodadas 13 a 15, uma por uma, na [origem das regras](origem-das-regras.md).
- Alertas novos: relatório de status atrasado, capacidade da iteração estourada, item com prazo vencido, conflito no Gantt e custo real sem custo planejado (Q158); oportunidade que ocorreu sem o ganho registrado (Q160); engajamento acima do desejado (Q164); parte neutra de influência alta (Q171); orçamento sem reserva de contingência com ameaça ativa (Q172a); fase em andamento sem critérios de saída (Q178); gerente de projetos sem projeto (Q183); cópia de segurança sem download (Q184); prazo de guarda vencido (Q193); espaço em disco e backup que falhou (Q195).
- Alertas que saem: princípios fracos (Q143), projeto sem membro (Q165), questão sem responsável (Q167), "seguir com modificações" sem notas (Q179) e fornecedor a cadastrar como parte (Q147).

## 6. Requisitos não funcionais

- **Plataforma:** web, no navegador do computador; o Octante não é feito para celular, mas a tela estreita continua para quem usa zoom de até 400% no computador (Q38, Q200, Q200b). Só português do Brasil (Q38). Roda no plano gratuito do PythonAnywhere, sem notificação por prazo (Q42; [ADR 0002](../adr/0002-hospedagem-no-pythonanywhere-gratuito.md)).
- **Acessibilidade:** WCAG 2.1 AA (Q38). O erro aparece junto do campo, também sem JavaScript (Q199); a mensagem de sucesso fica até a pessoa fechá-la ou mudar de página (Q201); o contraste das cores é testado (Q208); os testes usam o Playwright com o axe (Q78).
- **Usabilidade:** toda exclusão passa por uma tela de confirmação do servidor, inclusive a da linha da RACI (Q198). O "Aguarde…" e o aviso de alterações não salvas ficam no navegador, como ajuda (Q198).
- **Segurança:** login, sessão, primeiro acesso e bloqueio (seção 2); proteção contra formulário forjado, cabeçalhos de segurança, autorização pelos papéis, isolamento entre projetos, limites de tamanho e as demais proteções do protótipo continuam (Q196). Correções: o arquivo da chave secreta só para o dono, e os códigos de cada projeto sem repetição no banco (Q196).
- **Privacidade e LGPD:** página de privacidade, com o controlador, o contato e a base legal (Q189); pedido do titular, com o arquivo dos dados de uma pessoa, a anonimização de uma pessoa e o registro dos pedidos; o Administrador atende qualquer pessoa, e o supervisor, só com os dados dos projetos de que é o supervisor designado (Q190, Q191b); anonimização e prazo de guarda (seção 4.12); sigilo da análise das partes e dos dados dos membros (Q104, Q119). E-mail para gente de fora pede base legal e opção de descadastro (Q41).
- **Desempenho:** o portfólio abre em até 1 segundo com 50 projetos, conferido por teste (Q203).
- **Fuso:** o fuso configurado, com o de Brasília como padrão, vale em qualquer sistema, inclusive no Windows (Q206).
- **Bibliotecas:** versões e hashes travados; atualização pelo Dependabot, que espera 7 dias, menos nas correções de segurança; o pip-audit na CI; as actions presas pelo commit; só as bibliotecas aprovadas; nenhuma atualização entra sem revisão (Q204, Q204b; Q78).
- **Qualidade:** cobertura mínima de 95% de linhas e de ramificações, com a CI reprovando abaixo disso; testes de mutação nas regras de revisão, mudança e encerramento; toda entrada testada por partição de equivalência e valores-limite (Q77). Os testes rodam com o login e a proteção de formulário ligados, por papel, e os testes que já existem são refeitos (Q196, Q205). O ruff confere o código na CI, e os logs são estruturados (Q78, Q78b, Q205).
- **Infraestrutura:** Docker só no desenvolvimento e na CI; sem Kubernetes; Prometheus e Grafana só com servidor próprio (Q76).
- **Correções de documentação e de tela:** uma faixa só para o projeto encerrado, as cores fixas na paleta, o nome octante no DEPLOY.md e a paleta atual no AVALIACAO.md (Q208).

## 7. Entregas

A Q47 definiu, antes da auditoria:

- **Entrega 1:** papéis, criação do projeto pelo supervisor, revisão obrigatória com liberado e devolvido, aprovação separada da revisão, encerramento pelo supervisor, parecer, acesso de consulta e desligamento.
- **Entrega 2:** núcleo e tailoring, nível de exigência e cadência de relatório por projeto, relatório de status com indicadores congelados, visão do supervisor por gerente de projetos e resumo de alertas.
- **Entrega 3:** revisão das regras de alerta e ajustes nos módulos de tailoring.
- **Futuro:** e-mail por API HTTPS e PMBOK 8.

As decisões da auditoria e das rodadas 16 e 17 ainda não estão em nenhuma entrega. A Q213, na seção 9, propõe onde cada uma entra.

## 8. Fora do escopo e evolução prevista

- O e-mail por API HTTPS, com as mensagens numa fila de saída no banco (Q41, Q42, Q76, Q197).
- O PMBOK 8 (Q30, Q47).
- Um servidor próprio, com RabbitMQ, Prometheus e Grafana (Q76).
- Fora do escopo: notificação por prazo (Q42), versão para celular (Q200), a TIR no business case, por ora (Q138), e formalidades de estágio (Q207).

## 9. Para confirmar

### 9.1 Perguntas novas (decididas com "Sim" em 20/11/2026)

- **Q212:** os pacotes do Playwright e do axe, aprovados na Q78, ficaram fora da lista de bibliotecas da Q204b, e o axe não está no PyPI.
- **Q213:** em que entrega entram as decisões da auditoria e das rodadas 16 e 17.

### 9.2 Como entendi três respostas (confirmadas em 20/11/2026)

- **Exportação para Excel (Q104, Q119):** segue o mesmo sigilo das telas. Para quem tem acesso de consulta, ela sai sem a análise das partes e sem os dados pessoais dos membros.
- **"Projetos que estão atribuídos" (Q190):** são os projetos de que o supervisor é o supervisor designado.
- **"Fazer o login uma única vez" (Q196):** é uma vez por sessão, com os prazos da Q187.

### 9.3 O que depende do responsável pelo produto, fora do Octante

- Confirmar com o RH ou o jurídico os 5 anos do parecer e do prazo de guarda (Q25, Q193).
- Escolher a base legal e informar o controlador e o contato da página de privacidade (Q189).
- Configurar o autor do git neste computador e fazer os commits da elicitação e das correções das issues #1 e #2, que estão nas suas branches.
