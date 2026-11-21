# Octante

Ferramenta de trabalho de um PMO para gerenciar projetos reais (sobretudo internos de TI e de melhoria de processos, em abordagem híbrida) seguindo o PMBOK 7, usada por gerentes de projetos, em geral iniciantes, sob a revisão de um supervisor. O ensino do PMBOK vem embutido no uso.

## Pessoas e papéis

**PMO**:
O escritório de projetos que usa o Octante: um único PMO, com seus supervisores e gerentes de projetos.
_Avoid_: Escritório, departamento

**Gerente de projetos**:
Tipo de conta de quem conduz projetos no Octante, como gerente do projeto ou gerente de apoio, sob a revisão de um supervisor. Em geral tem conhecimento de gerenciamento de projetos de nível inicial, e o Octante ensina o PMBOK 7 durante o uso. Pode conduzir mais de um projeto.
_Avoid_: Estagiário, usuário comum, aluno, membro

**Gerente do projeto**:
No sentido do PMBOK 7, a pessoa designada pela organização para liderar a equipe responsável pelos objetivos do projeto. No Octante, é o gerente de projetos que responde ao supervisor por aquele projeto. Todo projeto tem exatamente um.
_Avoid_: Estagiário responsável, dono, supervisor, coordenador

**Gerente de apoio**:
Segundo gerente de projetos, opcional, que trabalha num projeto com os mesmos poderes de edição do gerente do projeto, mas sem responder por ele.
_Avoid_: Estagiário de apoio, auxiliar, colaborador

**Supervisor**:
Pessoa do PMO que revisa o trabalho dos gerentes de projetos, exercendo o papel de supervisão que o PMBOK 7 atribui ao PMO. Não é o gerente do projeto.
_Avoid_: Admin, PMO (como pessoa), revisor

**Supervisor designado**:
O supervisor que recebe as revisões de um projeto. Outro supervisor pode atuar como substituto.
_Avoid_: Supervisor do projeto, orientador

**Administrador**:
Papel extra, dado somente a um Supervisor, que dá poder sobre usuários, backups e dados. Ninguém é só Administrador.
_Avoid_: Admin, supervisor

**Código de instalação**:
Código secreto que o Octante gera enquanto não existe nenhum usuário. A tela Primeiro acesso o pede para criar o primeiro Administrador. Só quem tem acesso ao servidor o vê, e ele serve uma só vez.
_Avoid_: Senha inicial, chave de ativação

**Desligamento**:
Saída de uma pessoa do PMO. A conta é desativada, e não excluída, e o histórico mantém o nome dela.
_Avoid_: Fim do estágio, exclusão do usuário

**Destinatário**:
Pessoa de fora do Octante que recebe o que ele produz (por exemplo, o termo aprovado ou o relatório de status). Não tem acesso ao sistema.
_Avoid_: Usuário externo, leitor

## Projetos

**Projeto**:
Um projeto real do PMO, conduzido no Octante por um gerente do projeto e, se houver, um gerente de apoio.
_Avoid_: Exercício, caso

**Acesso de consulta**:
Permissão, dada por um supervisor, para um gerente de projetos ver um projeto do qual não participa, sem poder alterar nada.
_Avoid_: Modo visualização, acesso de leitura

**Encerramento**:
Fechamento de um projeto, concluído ou cancelado. O gerente do projeto prepara, o supervisor revisa e só o supervisor encerra, cancela ou reabre. Encerrar exige o aceite final; cancelar e reabrir exigem justificativa.
_Avoid_: Finalização, arquivamento

**Parte interessada**:
Pessoa, grupo ou organização que pode afetar o projeto, ser afetada por ele ou se perceber afetada. Fica registrada no projeto e pode ou não ter conta no Octante. Quando deixa de ser parte, é inativada. A análise de cada uma só é vista pelo gerente do projeto, pelo gerente de apoio e pelos supervisores.
_Avoid_: Stakeholder, envolvido, interessado

**Patrocinador**:
Parte interessada que fornece recursos e apoio ao projeto e responde por viabilizar o sucesso dele. Emite o termo de abertura e, por padrão, é a autoridade de mudança. É escolhido na lista de partes interessadas.
_Avoid_: Cliente, dono do projeto, demandante

**Contato**:
Registro de uma comunicação com uma parte interessada: data, forma e resumo, com nota de satisfação opcional.
_Avoid_: Interação, atendimento

**Membro da equipe**:
Pessoa que trabalha no projeto, com ou sem conta no Octante. Pode ser ligado a um usuário.
_Avoid_: Colaborador, recurso

**Responsável**:
O membro da equipe encarregado de um risco, questão ou item do projeto. É sempre escolhido entre os membros da equipe.
_Avoid_: Dono, encarregado

**Projeto de exemplo**:
Projeto fictício, único e já preenchido, somente para consulta de todos. Não é trabalho do PMO.
_Avoid_: Projeto de treinamento, demo

**Nível de exigência**:
O grau de rigor (essencial ou rigoroso) cobrado no preenchimento de um projeto, definido pelo supervisor designado.
_Avoid_: Modo, configuração de rigor

**Núcleo**:
O conjunto de funcionalidades sempre presente em todo projeto. O resto só aparece quando o tailoring do projeto o ativa.
_Avoid_: Básico, MVP

**Módulo opcional**:
Parte do Octante que fica fora do núcleo e só aparece num projeto quando o tailoring desse projeto a liga, como a matriz de engajamento ou a saúde da equipe.
_Avoid_: Módulo (sozinho), recurso extra, funcionalidade avançada

**Cadência de relatório**:
Intervalo esperado entre dois relatórios de status de um projeto, definido pelo supervisor designado.
_Avoid_: Frequência, periodicidade, cadência (sozinho)

## Abordagem, ciclo de vida e tailoring

**Abordagem de desenvolvimento**:
Forma de criar e evoluir o produto do projeto: preditiva, híbrida ou adaptativa. Cada projeto tem uma; é híbrida quando partes do projeto usam abordagens diferentes.
_Avoid_: Metodologia, método, modelo de gestão

**Sugestão de abordagem**:
Abordagem indicada pelas notas dadas aos 15 fatores de seleção do PMBOK; é o que o PMBOK chama de filtro de adequação. É só informativa: a equipe escolhe a abordagem, justifica quando ela é diferente da sugerida, e o supervisor revisa a escolha junto com o tailoring.
_Avoid_: Recomendação, abordagem calculada

**Cadência de entrega**:
Ritmo das entregas do projeto: entrega única, múltiplas entregas, entregas periódicas ou entrega contínua.
_Avoid_: Cadência (sozinho), frequência de entrega

**Ciclo de vida**:
Série de fases pelas quais o projeto passa, do início ao fim.
_Avoid_: Roadmap, cronograma de fases

**Fase**:
Conjunto de atividades relacionadas do projeto que termina com a conclusão de uma ou mais entregas. Cada fase fecha numa revisão de fase.
_Avoid_: Etapa, estágio

**Grupo de processos**:
Um dos cinco agrupamentos do trabalho de gerenciamento: Iniciação (Initiating), Planejamento (Planning), Execução (Executing), Monitoramento e controle (Monitoring and Controlling) e Encerramento (Closing). Não é fase: os grupos se repetem dentro de cada fase do ciclo de vida.
_Avoid_: Fase, etapa do projeto

**Critério de saída**:
Condição que precisa estar atendida na revisão de fase para que a fase conclua.
_Avoid_: Critério de aceite da fase, pré-requisito

**Revisão de fase**:
Revisão no fim de uma fase em que se decide seguir, seguir com modificações, repetir a fase ou encerrar o projeto. Quem decide é uma parte interessada ou um membro da equipe; não é a revisão do supervisor.
_Avoid_: Portão, gate, revisão (sozinho)

**Tailoring**:
Adaptação deliberada da abordagem, da governança e dos processos ao projeto: o que entra, sai ou muda além do núcleo. O gerente do projeto propõe e o supervisor revisa.
_Avoid_: Personalização, configuração, adaptação (sozinho)

**Modelo de projeto**:
Conjunto de valores iniciais que o PMO oferece ao criar um projeto, como abordagem, cadência, fases e riscos típicos. Não é um dos modelos da Seção 4 do PMBOK, como o Cynefin, que são formas de pensar.
_Avoid_: Template, projeto-base

## Escopo e entrega

**Item de escopo**:
Unidade do escopo do projeto: épico, funcionalidade, história, entregável, pacote de trabalho ou requisito. Os itens formam uma hierarquia.
_Avoid_: Tarefa, atividade, card

**Critérios de aceite**:
Condições que um item precisa cumprir antes de ser aceito por quem o recebe.
_Avoid_: Requisitos de teste, checklist

**Definição de pronto**:
Lista, única por projeto, do que todo item precisa cumprir para ser considerado pronto para uso do cliente. Usada sobretudo na parte adaptativa.
_Avoid_: DoD, critério de conclusão

**Linha de base do escopo**:
Versão aprovada do escopo, usada para comparar com o que foi realizado. Só muda por controle formal de mudanças.
_Avoid_: Escopo congelado, snapshot

**Aceite do item**:
Registro de que um item concluído foi aceito por quem o recebe, conforme seus critérios de aceite. Diferente do aceite final, que vale para o projeto inteiro.
_Avoid_: Homologação, aprovação do item

## Aquisições e recursos físicos

**Aquisição**:
Bem ou serviço de que o projeto precisa, com a decisão de comprá-lo de fora ou fazê-lo internamente, acompanhado do planejamento ao encerramento.
_Avoid_: Compra (sozinho), suprimento, pedido

**Fornecedor**:
Organização ou pessoa de fora contratada numa aquisição. A partir do contrato, é uma parte interessada do projeto.
_Avoid_: Vendedor, terceiro, prestador

**Recurso físico**:
Tudo o que o projeto usa e não é pessoa: material, equipamento, software ou licença, ambiente de testes.
_Avoid_: Insumo, recurso (sozinho)

## Medição e incerteza

**Limite de variação**:
Variação aceitável em torno de um objetivo do projeto (prazo, custo), combinada com o patrocinador e registrada no termo de abertura. Depois do termo aprovado, só muda por mudança aprovada. Passar dele aciona o plano de exceção.
_Avoid_: Tolerância (sozinho), margem

**Plano de exceção**:
Conjunto de ações combinadas para quando um limite de variação é ultrapassado ou está previsto para ser.
_Avoid_: Plano B, plano de contingência

**Risco**:
Evento ou condição incerta que, se ocorrer, afeta um ou mais objetivos do projeto. Ameaça, se o efeito for negativo; oportunidade, se for positivo.
_Avoid_: Problema, questão

**Limite de risco**:
Pontuação de risco (probabilidade × impacto) a partir da qual uma ameaça precisa de resposta. É registrado no termo de abertura e, depois do termo aprovado, só muda por mudança aprovada.
_Avoid_: Apetite a risco, tolerância

**Risco residual**:
O risco que ainda resta depois de executada a resposta planejada (residual risk).
_Avoid_: Risco restante, sobra

**Risco secundário**:
Risco novo que a própria resposta planejada cria (secondary risk).
_Avoid_: Risco derivado, efeito colateral

**Risco geral do projeto**:
Efeito da incerteza no projeto como um todo, vindo de todas as fontes de incerteza, inclusive dos riscos individuais (overall project risk). É avaliado como baixo, médio ou alto.
_Avoid_: Risco global, risco total

**Reserva de contingência**:
Tempo ou dinheiro separado para os riscos identificados, caso ocorram.
_Avoid_: Folga, colchão

**Reserva de gerenciamento**:
Tempo ou dinheiro separado para imprevistos dentro do escopo, que não vieram de um risco identificado.
_Avoid_: Reserva geral

## Valor e princípios

**Business case**:
Proposta de valor do projeto: a necessidade, a justificativa (com a análise de custo-benefício e as premissas), a estratégia e os benefícios financeiros e não financeiros. Pode ser revisto ao longo do projeto.
_Avoid_: Caso de negócio, estudo de viabilidade, justificativa (sozinho)

**ROI**:
Retorno sobre o investimento, como o PMBOK 7 define: a média dos benefícios líquidos por período dividida pelo investimento inicial.
_Avoid_: Retorno total, ROI acumulado

**Razão benefício-custo**:
Valor presente dos benefícios dividido pelo valor presente dos custos. Acima de 1,0, o projeto deve ser considerado; abaixo, só por razões regulatórias, sociais ou outras.
_Avoid_: Viabilidade, selo "viável"

**Custo previsto**:
Quanto o projeto deve custar ao fim, já com as reservas de contingência e de gerenciamento. É o valor comparado com o investimento do business case.
_Avoid_: Orçamento, custo total

**Premissa**:
Fator considerado verdadeiro sem prova, registrado para ser validado ao longo do projeto.
_Avoid_: Suposição, hipótese

**Restrição**:
Fator que limita as opções do projeto, como prazo, orçamento, lei ou tecnologia. É um limite, e não se valida.
_Avoid_: Limitação, condição

**Registro de decisões**:
Lista das decisões do projeto, com o contexto, as alternativas, quem decidiu e os efeitos. É regra do PMO: o PMBOK 7 não tem esse artefato.
_Avoid_: Ata, log de decisões

**Sinais no projeto**:
Verificações calculadas a partir dos registros do projeto que mostram como ele se relaciona com cada um dos 12 princípios. São só informação: a avaliação do princípio é a reflexão da equipe.
_Avoid_: Nível do princípio, nota, evidência (sozinho)

## Revisão e aprovação

**Revisão**:
Análise de um registro pelo supervisor antes que ele saia do Octante ou comprometa o projeto. Termina em liberado ou devolvido.
_Avoid_: Aprovação, validação

**Revisão obrigatória**:
Revisão sem a qual o registro não pode gerar documento nem seguir adiante: vale para termo de abertura, tailoring, relatório de status, mudança e encerramento.
_Avoid_: Revisão exigida

**Pronto para revisão**:
Estado de um registro cujos campos exigidos pelo nível de exigência estão todos preenchidos. Só um registro pronto pode ser enviado para revisão.
_Avoid_: Completo, 100% preenchido

**Questão**:
Situação atual que pode afetar os objetivos do projeto, atribuída a um responsável até ser resolvida. Diferente do risco, que é incerto e futuro.
_Avoid_: Problema, issue, pendência, impedimento

**Lição aprendida**:
Conhecimento obtido durante o projeto, registrado para melhorar o desempenho futuro do projeto, de outras equipes ou da organização.
_Avoid_: Retrospectiva, aprendizado

**Mudança**:
Pedido para alterar algo já aprovado, como o termo, a linha de base do escopo, o custo ou o prazo. Leva o solicitante, o valor esperado, os seis impactos e os riscos novos. O supervisor revisa, e a autoridade de mudança do projeto aprova ou rejeita.
_Avoid_: Alteração, ajuste, solicitação

**Autoridade de mudança**:
Quem decide sobre as mudanças de um projeto: o patrocinador (padrão), um comitê de controle de mudanças ou o dono do produto. Fica registrada no termo de abertura.
_Avoid_: Aprovador, comitê (sozinho)

**Mudança organizacional**:
Transição de pessoas, grupos ou da organização do estado atual para o estado futuro que o projeto cria, até a adoção. Não é a mudança, que é um pedido para alterar o que já foi aprovado no projeto.
_Avoid_: Gestão da mudança, mudança (sozinho)

**Capacidade de absorção**:
Quanto um grupo afetado consegue absorver da mudança organizacional sem fadiga nem resistência.
_Avoid_: Prontidão, readiness

**Liberado**:
Resultado da revisão em que o supervisor aceita o registro. Perde a validade se o gerente do projeto ou o gerente de apoio alterar o registro depois; a edição feita pelo próprio supervisor não a anula.
_Avoid_: Aprovado, aceito

**Devolvido**:
Resultado da revisão em que o supervisor pede correções, com comentário. O comentário de devolução é o canal de feedback ao gerente do projeto.
_Avoid_: Rejeitado, reprovado

**Aprovação**:
Decisão do próprio projeto tomada por quem tem autoridade para ela, como o patrocinador que autoriza o termo ou quem decide sobre uma mudança. Não é feita pelo supervisor.
_Avoid_: Liberação, revisão

**Aceite final**:
Aprovação, dada por uma parte interessada com essa autoridade (patrocinador, dono do produto ou cliente), de que o escopo entregue está completo. É condição para encerrar o projeto.
_Avoid_: Homologação, aceite do supervisor

**Parecer do supervisor**:
Avaliação formal do desempenho de um gerente de projetos, em texto livre, escrita por um supervisor quando quiser. Todos os supervisores leem, menos a própria pessoa avaliada, mesmo depois de ela passar a supervisor. Ela pode receber o parecer num pedido do titular sobre os próprios dados.
_Avoid_: Avaliação, feedback, nota

**Documento gerado**:
Versão para impressão ou PDF de um registro, feita para o gerente do projeto entregar a um Destinatário por fora do Octante.
_Avoid_: Envio, notificação

## Dados pessoais e privacidade

**Dado pessoal**:
Informação ligada a uma pessoa identificada ou que se possa identificar, como o nome, o contato, a análise de uma parte interessada ou o parecer sobre um gerente de projetos.
_Avoid_: Dado sensível, informação privada

**Titular**:
A pessoa a quem os dados pessoais se referem: um usuário, uma parte interessada ou um membro da equipe.
_Avoid_: Dono dos dados, usuário

**Controlador**:
Quem decide sobre os dados pessoais guardados no Octante: o PMO ou a organização dele.
_Avoid_: Administrador, responsável pelos dados

**Aviso de privacidade**:
Texto aberto a todos, mesmo antes de entrar, que diz quais dados pessoais o Octante guarda, para quê, por quanto tempo, quem é o controlador e como fazer um pedido.
_Avoid_: Termo de uso, política de cookies

**Pedido do titular**:
Pedido de um titular para confirmar que há dados dele, acessá-los, corrigi-los, anonimizá-los ou eliminá-los.
_Avoid_: Solicitação LGPD, requisição

**Anonimização**:
Troca ou apagamento dos dados pessoais de um projeto, ou de uma pessoa, de modo que não se possa mais saber a quem se referiam. Não se desfaz.
_Avoid_: Exclusão, limpeza

**Prazo de guarda**:
Tempo, depois do encerramento ou do cancelamento do projeto, em que os dados pessoais dele ficam no Octante antes da anonimização.
_Avoid_: Retenção, validade
