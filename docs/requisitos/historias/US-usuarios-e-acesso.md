# Histórias da Entrega 1: Usuários e acesso (épico #4)

Rascunho para a revisão do responsável pelo produto, antes de criar as issues (Q228). Cada história sai da [ERS 1.1](../ERS.md), seção 3.2.1. Marco: Entrega 1. Rótulos: `enhancement`, `needs-triage`. Testes exigidos em cada uma: RNF-MAN-14 (válido e inválido de cada regra, com o código no teste), RNF-MAN-15 (valores-limite de cada entrada) e RNF-MAN-16 (acesso, com o papel aceito e o recusado).

As regras deste domínio têm o código RN-PM, do inventário do protótipo.

---

## RF-US-01 · Criar a primeira conta

**História:** Como a pessoa que instalou o Octante, quero criar a primeira conta com o código de instalação, para começar a usar o sistema sem que mais ninguém consiga tomar o lugar do Administrador.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-US-01 | Enquanto o Octante não tem nenhuma conta, o sistema deve mostrar a tela Primeiro acesso, que cria a primeira conta com o nome, o login, o e-mail e a senha informados. | Q52, Q188 | alterado | 1 | teste |
| RN-PM-01 | A primeira conta criada no Octante deve ter o tipo supervisor e o papel de Administrador. | Regra do PMO (Q52) | alterado | 1 | teste |
| RN-PM-02 | O login deve ser único no Octante e reconhecido sem diferença entre maiúsculas e minúsculas. | Regra do PMO (Q51) | confirmado | 1 | teste |
| RN-PM-25 | O sistema deve criar a primeira conta somente quando o código de instalação informado for igual ao gerado na instalação. | Regra do PMO (Q188; OWASP ASVS 5.0, 6.3.2) | novo | 1 | teste |
| RN-PM-26 | Depois que a primeira conta existe, o sistema deve recusar o acesso à tela Primeiro acesso. | Regra do PMO (Q52, Q188) | novo | 1 | teste |
| RN-PM-27 | O código de instalação deve ficar visível somente nos arquivos do servidor ou no terminal do computador onde o Octante roda. | Regra do PMO (Q188) | novo | 1 | inspeção |
| RN-PM-28 | O Octante deve ser instalado sem nenhuma conta. | Regra do PMO (Q188; OWASP ASVS 5.0, 6.4.1) | novo | 1 | teste |
| RN-PM-29 | A senha deve ter pelo menos 8 caracteres. | Regra do PMO (Q51) | confirmado | 1 | teste |

**Entradas:** código de instalação (obrigatório); nome (obrigatório, até 20.000 caracteres); login (obrigatório, até 20.000); e-mail (opcional: um @, com texto antes e um domínio com ponto depois, Q220); senha nova (de 8 a 20.000) e a confirmação, igual à senha. Campo só com espaços conta como vazio (Q220).

**Critérios de aceite:**
- **RF-US-01, válido:** Dado um Octante sem contas, quando a pessoa abre o endereço, então aparece a tela Primeiro acesso.
- **RN-PM-01, válido:** Dado um Octante sem contas e o código certo, quando a pessoa cria a conta, então ela nasce supervisor e Administrador, e a sessão abre.
- **RN-PM-25, válido:** Quando o código informado é igual ao gerado na instalação, então a conta é criada e o arquivo do código é apagado: o mesmo código não serve uma segunda vez (Q188).
- **RN-PM-25, inválido:** Quando o código está errado ou vazio, então o sistema recusa, não cria a conta e mostra o erro junto do campo.
- **RN-PM-26, válido:** Dado um Octante sem contas, quando a pessoa abre o Primeiro acesso, então a tela aparece.
- **RN-PM-26, inválido:** Dado um Octante com uma conta, quando alguém abre o endereço do Primeiro acesso, então o sistema recusa e leva ao login.
- **RN-PM-27 (inspeção):** O código aparece no arquivo da pasta `instance` e, no computador local, no terminal; não aparece em nenhuma página, resposta do servidor ou registro do histórico.
- **RN-PM-28, válido:** Dado uma instalação nova, quando o banco é criado, então ele não tem nenhuma conta, nem conta padrão.
- **RN-PM-02, válido:** Quando a pessoa usa um login novo, então a conta é criada.
- **RN-PM-02, inválido:** Esta regra se testa no cadastro (RF-US-05), porque aqui ainda não há outro login.
- **RN-PM-29, válido:** Quando a senha tem 8 caracteres, então a conta é criada.
- **RN-PM-29, inválido:** Quando a senha tem 7 caracteres, ou a confirmação é diferente, então o sistema recusa e mostra o erro junto do campo.
- **Entradas, inválido:** nome ou login vazios ou só com espaços, e-mail sem @ ou sem domínio com ponto, e qualquer campo com 20.001 caracteres são recusados, cada um com o erro junto do campo.

**Fora desta história:** o aviso de privacidade na primeira tela (RF-DA-11, Dados).

---

## RF-US-02 · Entrar no Octante

**História:** Como pessoa com conta no Octante, quero entrar com o meu login e a minha senha, para ver as telas que o meu tipo de conta e o meu papel permitem.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-US-02 | Quando uma pessoa informa o login e a senha de uma conta ativa e não bloqueada, o sistema deve abrir uma sessão e mostrar as telas que o tipo da conta e o papel dela permitem. | Q186, Q186b, Q187, Q196 | alterado | 1 | teste |
| RN-PM-02 | O login deve ser único no Octante e reconhecido sem diferença entre maiúsculas e minúsculas. | Regra do PMO (Q51) | confirmado | 1 | teste |
| RN-PM-03 | Depois de 5 senhas erradas seguidas para uma conta, vindas da mesma máquina, o sistema deve recusar o login dessa conta, a partir dessa máquina, por 5 minutos. | Regra do PMO (Q186, Q186b, Q220; OWASP ASVS 5.0, 6.1.1) | alterado | 1 | teste |
| RN-PM-04 | O sistema deve encerrar a sessão depois de 3 horas sem uso ou 12 horas depois do login, o que vier primeiro. | Regra do PMO (Q187; LGPD, art. 46) | alterado | 1 | teste |
| RN-PM-30 | O sistema deve identificar a máquina pelo endereço real de origem, informado pelo servidor do PythonAnywhere, e não pelo endereço do intermediário. | Regra do PMO (Q186b) | novo | 1 | teste |
| RN-PM-31 | A contagem das senhas erradas deve continuar valendo depois que o app reinicia. | Regra do PMO (Q186b) | novo | 1 | teste |

**Entradas:** login e senha, os dois obrigatórios, até 20.000 caracteres.

**Critérios de aceite:**
- **RF-US-02, válido:** Dado uma conta ativa de gerente de projetos, quando a pessoa entra com o login e a senha certos, então a sessão abre e ela vê só as telas do gerente de projetos; com uma conta de supervisor Administrador, vê também as telas do Administrador.
- **RF-US-02, inválido:** Dado uma conta desativada, quando a pessoa entra com a senha certa, então o sistema recusa e não abre a sessão.
- **RN-PM-02, válido:** Dado a conta "Ana", quando a pessoa entra como "ANA" com a senha certa, então a sessão abre.
- **RN-PM-03, válido:** Dado 4 senhas erradas seguidas, quando a pessoa erra a 5.ª, então o login dessa conta, nessa máquina, fica recusado por 5 minutos; passados os 5 minutos, a senha certa abre a sessão.
- **RN-PM-03, inválido (outras contas e máquinas):** Dado uma conta bloqueada na máquina A, quando a mesma conta entra pela máquina B, ou outra conta entra pela máquina A, então o login funciona.
- **RN-PM-03 (login certo zera):** Dado 4 senhas erradas, quando a pessoa acerta a senha, então a contagem zera, e um novo erro conta como o 1.º (Q220).
- **RN-PM-03, inválido (bloqueado):** Dado uma conta bloqueada nessa máquina, quando a pessoa informa a senha certa antes dos 5 minutos, então o sistema recusa.
- **RN-PM-04, válido:** Dado uma sessão usada há 2 h 59 min, quando a pessoa abre uma tela, então a sessão continua.
- **RN-PM-04, inválido (sem uso):** Dado uma sessão sem uso há 3 h, quando a pessoa abre uma tela, então a sessão acabou e o sistema leva ao login.
- **RN-PM-04, inválido (máximo):** Dado uma sessão aberta há 12 h e usada o tempo todo, quando a pessoa abre uma tela, então a sessão acabou.
- **RN-PM-30, válido:** Dado uma requisição com o endereço real informado pelo servidor do PythonAnywhere, quando a pessoa erra a senha, então a contagem fica com esse endereço; no computador local, com o endereço da conexão.
- **RN-PM-30, inválido:** Dado duas pessoas em máquinas diferentes, atrás do mesmo intermediário, quando uma delas é bloqueada, então a outra continua entrando.
- **RN-PM-31, válido:** Dado 5 senhas erradas, quando o app reinicia dentro dos 5 minutos, então o login continua recusado.
- **Acesso, inválido:** sem sessão, cada tela, exceto Entrar, Primeiro acesso, Privacidade e os arquivos estáticos, leva ao login (RNF-SEG-01).

**Fora desta história:** a proteção do cookie da sessão e o registro das tentativas, que estão nos não funcionais de segurança (#21).

---

## RF-US-03 · Sair do Octante

**História:** Como pessoa com sessão aberta, quero sair do Octante, para que ninguém use a minha sessão neste computador.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-US-03 | Quando a pessoa pede para sair, o sistema deve encerrar a sessão dela. | Protótipo (Q209) | confirmado | 1 | teste |

**Critérios de aceite:**
- **RF-US-03, válido:** Dado uma sessão aberta, quando a pessoa sai, então a sessão acaba e o sistema leva ao login.
- **RF-US-03, inválido:** Dado uma pessoa que saiu, quando ela volta pelo navegador a uma tela que estava aberta, então o sistema leva ao login, e não mostra a tela.
- **Acesso:** sair só funciona por um formulário com o token anti-CSRF da sessão; um pedido sem ele é recusado (RNF-SEG-08).

---

## RF-US-04 · Trocar a própria senha

**História:** Como pessoa com conta no Octante, quero trocar a minha senha, para manter o meu acesso seguro.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-US-04 | O sistema deve permitir que a pessoa troque a própria senha. | Q51, Q187 | alterado | 1 | teste |
| RN-PM-29 | A senha deve ter pelo menos 8 caracteres. | Regra do PMO (Q51) | confirmado | 1 | teste |
| RN-PM-32 | Quando a pessoa troca a própria senha, o sistema deve encerrar as outras sessões abertas da conta dela. | Regra do PMO (Q51, Q187) | confirmado | 1 | teste |
| RN-PM-33 | Para trocar a própria senha, a pessoa deve informar a senha atual. | Regra do PMO (Q51) | confirmado | 1 | teste |

**Entradas:** senha atual (obrigatória); senha nova (de 8 a 20.000 caracteres); confirmação, igual à senha nova.

**Critérios de aceite:**
- **RF-US-04, válido:** Dado uma pessoa com sessão aberta, quando ela informa a senha atual certa e uma senha nova válida, então a senha muda, e o próximo login só aceita a nova.
- **RN-PM-29, válido:** Quando a senha nova tem 8 caracteres, então a troca é aceita.
- **RN-PM-29, inválido:** Quando a senha nova tem 7 caracteres, ou a confirmação é diferente, então o sistema recusa e mostra o erro junto do campo.
- **RN-PM-32, válido:** Dado a mesma conta aberta em dois navegadores, quando a pessoa troca a senha num deles, então a sessão dele continua e a do outro acaba.
- **RN-PM-33, inválido:** Quando a senha atual está errada ou vazia, então o sistema recusa e a senha não muda.
- **Acesso:** a pessoa troca só a própria senha; trocar a de outra conta é a RF-US-06, do Administrador.

---

## RF-US-05 · Cadastrar uma conta

**História:** Como Administrador, quero cadastrar uma conta de gerente de projetos ou de supervisor, para que a pessoa possa entrar no Octante.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-US-05 | O sistema deve permitir que o Administrador cadastre uma conta com nome, login, e-mail, senha inicial, tipo da conta e papel de Administrador. | Q7, Q22, Q41, Q52, Q210 | alterado | 1 | teste |
| RN-PM-02 | O login deve ser único no Octante e reconhecido sem diferença entre maiúsculas e minúsculas. | Regra do PMO (Q51) | confirmado | 1 | teste |
| RN-PM-05 | O sistema deve recusar que uma conta sem o papel de Administrador veja a lista das contas, cadastre conta, edite conta, redefina a senha de outra conta ou mude a situação de uma conta. | Regra do PMO (Q52, Q231) | alterado | 1 | teste |
| RN-PM-06 | O papel de Administrador deve ficar somente em contas do tipo supervisor. | Regra do PMO (Q22, Q52) | alterado | 1 | teste |
| RN-PM-29 | A senha deve ter pelo menos 8 caracteres. | Regra do PMO (Q51) | confirmado | 1 | teste |

**Entradas:** nome e login (obrigatórios, até 20.000 caracteres); e-mail (opcional, como no Primeiro acesso); senha inicial (de 8 a 20.000); tipo da conta (gerente de projetos ou supervisor); papel de Administrador (sim ou não).

**Critérios de aceite:**
- **RF-US-05, válido:** Dado um Administrador, quando ele cadastra uma conta de gerente de projetos com os campos válidos, então a conta é criada, ativa, e aparece na lista de contas.
- **RN-PM-02, inválido:** Dado a conta "ana", quando o Administrador cadastra outra com o login "Ana", então o sistema recusa e mostra o erro junto do campo.
- **RN-PM-05, válido:** Dado um supervisor Administrador, quando ele abre o cadastro de conta, então a tela aparece.
- **RN-PM-05, inválido:** Dado um supervisor sem o papel de Administrador, ou um gerente de projetos, quando ele abre o cadastro ou envia o formulário direto ao servidor, então o sistema recusa.
- **RN-PM-06, válido:** Quando o Administrador cadastra um supervisor com o papel de Administrador, então a conta é criada com o papel.
- **RN-PM-06, inválido:** Quando o Administrador cadastra um gerente de projetos com o papel de Administrador, então o sistema recusa e mostra o erro.
- **RN-PM-29, inválido:** Quando a senha inicial tem 7 caracteres, então o sistema recusa.
- **Entradas, inválido:** nome ou login vazios, e-mail inválido e campos com 20.001 caracteres são recusados.

---

## RF-US-06 · Redefinir a senha de outra conta

**História:** Como Administrador, quero redefinir a senha de outra conta, para devolver o acesso a quem esqueceu a senha.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-US-06 | O sistema deve permitir que o Administrador redefina a senha de outra conta. | Q52 | alterado | 1 | teste |
| RN-PM-05 | O sistema deve recusar que uma conta sem o papel de Administrador veja a lista das contas, cadastre conta, edite conta, redefina a senha de outra conta ou mude a situação de uma conta. | Regra do PMO (Q52, Q231) | alterado | 1 | teste |
| RN-PM-29 | A senha deve ter pelo menos 8 caracteres. | Regra do PMO (Q51) | confirmado | 1 | teste |
| RN-PM-79 | O sistema deve encerrar as sessões abertas de uma conta quando o Administrador redefine a senha dela. | Regra do PMO (Q230) | novo | 1 | teste |

**Entradas:** senha nova, de 8 a 20.000 caracteres.

**Critérios de aceite:**
- **RF-US-06, válido:** Dado um Administrador, quando ele redefine a senha de outra conta, então a senha muda, e o próximo login dessa conta só aceita a nova.
- **RN-PM-05, inválido:** Dado uma conta sem o papel de Administrador, quando ela tenta redefinir a senha de outra, mesmo enviando o formulário direto ao servidor, então o sistema recusa.
- **RN-PM-29, inválido:** Quando a senha nova tem 7 caracteres, então o sistema recusa.
- **RN-PM-79, válido:** Dado a conta aberta em dois navegadores, quando o Administrador redefine a senha dela, então as duas sessões acabam na requisição seguinte, e só a senha nova abre uma sessão.
- **RN-PM-79, inválido:** Dado uma redefinição recusada (senha com 7 caracteres, ou pedida por quem não é Administrador), quando a pessoa usa a sessão aberta, então ela continua.
- **Acesso:** o Administrador troca a própria senha pela RF-US-04, que pede a senha atual.


---

## RF-US-07 · Ativar ou desativar uma conta

**História:** Como Administrador, quero desativar a conta de quem saiu do PMO, e reativá-la se a pessoa voltar, para que só quem trabalha no PMO entre no Octante, sem perder o histórico.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-US-07 | O sistema deve permitir que o Administrador mude a situação de uma conta entre ativa e desativada. | Q28, Q32, Q52 | alterado | 1 | teste |
| RN-PM-05 | O sistema deve recusar que uma conta sem o papel de Administrador veja a lista das contas, cadastre conta, edite conta, redefina a senha de outra conta ou mude a situação de uma conta. | Regra do PMO (Q52, Q231) | alterado | 1 | teste |
| RN-PM-34 | O sistema deve recusar que uma pessoa desative a própria conta. | Regra do PMO (Q52) | confirmado | 1 | teste |
| RN-PM-35 | O sistema deve recusar a mudança que deixaria o Octante sem nenhum Administrador ativo. | Regra do PMO (Q52) | novo | 1 | teste |
| RN-PM-36 | O sistema deve recusar a desativação de uma conta que é o gerente do projeto de um projeto em andamento. | Regra do PMO (Q28, Q32, Q220) | novo | 1 | teste |
| RN-PM-37 | O sistema deve mostrar ao Administrador, no portfólio, um alerta médio quando um gerente de projetos ativo já foi gerente do projeto ou gerente de apoio e hoje não é nenhum dos dois em um projeto em andamento, com a ação sugerida de confirmar o desligamento e desativar a conta. | Regra do PMO (Q32, Q153, Q183) | novo | 1 | teste |
| RN-PM-38 | O sistema deve manter a conta desativada no Octante, com o nome dela no histórico. | Regra do PMO (Q28) | novo | 1 | teste |

**Critérios de aceite:**
- **RF-US-07, válido:** Dado uma conta ativa sem projeto em andamento, quando o Administrador a desativa, então ela não entra mais, e uma sessão já aberta perde o acesso na requisição seguinte (RNF-SEG-06); quando ele a reativa, ela volta a entrar.
- **RN-PM-05, inválido:** Dado uma conta sem o papel de Administrador, quando ela tenta mudar a situação de uma conta, então o sistema recusa.
- **RN-PM-34, inválido:** Quando o Administrador tenta desativar a própria conta, então o sistema recusa.
- **RN-PM-35, válido:** Dado dois Administradores ativos, quando um desativa o outro, então a mudança é aceita.
- **RN-PM-35, inválido:** Dado um só Administrador ativo, quando alguém tenta tirar dele a condição de Administrador ativo, então o sistema recusa. (A desativação da própria conta já é recusada pela RN-PM-34; a edição está na RF-US-09.)
- **RN-PM-36, válido:** Dado um gerente de projetos que só é gerente do projeto de projetos encerrados ou cancelados, quando o Administrador o desativa, então a mudança é aceita.
- **RN-PM-36, inválido:** Dado um gerente do projeto de um projeto em andamento, quando o Administrador tenta desativá-lo, então o sistema recusa e diz o projeto que precisa passar a outro gerente antes.
- **RN-PM-37, válido:** Dado um gerente de projetos ativo que foi gerente de apoio de um projeto já encerrado e não está em nenhum projeto em andamento, quando o Administrador abre o portfólio, então aparece o alerta médio, com a ação de confirmar o desligamento e desativar a conta.
- **RN-PM-37, inválido:** Dado um gerente de projetos que nunca teve projeto, ou que está num projeto em andamento, quando o Administrador abre o portfólio, então o alerta não aparece; e um supervisor sem o papel de Administrador não vê o alerta.
- **RN-PM-38, válido:** Dado uma conta desativada, quando alguém abre o histórico de um projeto dela, então o nome dela continua lá; a conta continua na lista de contas, como desativada.
- **RN-PM-38, inválido:** Não há exclusão de conta: o sistema não oferece a ação, e um pedido de exclusão enviado direto ao servidor é recusado.

**Fora desta história:** passar o projeto a outro gerente (Projetos, #7); o resumo dos alertas do Administrador (Entrega 2).

---

## RF-US-08 · Ver a lista das contas

**História:** Como Administrador, quero ver todas as contas, com o tipo, o papel e a situação de cada uma, para saber quem tem acesso ao Octante.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-US-08 | O sistema deve mostrar ao Administrador a lista das contas, com o nome, o login, o tipo da conta, o papel de Administrador e a situação de cada uma. | Q52, Q210 | alterado | 1 | teste |
| RN-PM-05 | O sistema deve recusar que uma conta sem o papel de Administrador veja a lista das contas, cadastre conta, edite conta, redefina a senha de outra conta ou mude a situação de uma conta. | Regra do PMO (Q52, Q231) | alterado | 1 | teste |

**Critérios de aceite:**
- **RF-US-08, válido:** Dado contas ativas e desativadas dos dois tipos, quando o Administrador abre a lista, então vê cada conta com o nome, o login, o tipo (gerente de projetos ou supervisor), o papel de Administrador e a situação.
- **RN-PM-05, válido:** Dado um Administrador, quando ele abre a lista, então cada conta mostra as ações de editar, redefinir a senha e mudar a situação.
- **RN-PM-05, inválido (Q231):** Dado um supervisor sem o papel de Administrador, ou um gerente de projetos, quando ele abre o endereço da lista, então o sistema recusa.
- **Dados:** a lista não mostra a senha nem o resumo (hash) dela.

---

## RF-US-09 · Editar uma conta

**História:** Como Administrador, quero editar o nome, o e-mail, o tipo e o papel de Administrador de uma conta, para corrigir dados ou promover um gerente de projetos a supervisor.

| Código | Requisito | Origem | Protótipo | Entrega | Verificação |
|---|---|---|---|---|---|
| RF-US-09 | O sistema deve permitir que o Administrador edite o nome, o e-mail, o tipo e o papel de Administrador de uma conta. | Q22, Q41, Q52 | novo | 1 | teste |
| RN-PM-05 | O sistema deve recusar que uma conta sem o papel de Administrador veja a lista das contas, cadastre conta, edite conta, redefina a senha de outra conta ou mude a situação de uma conta. | Regra do PMO (Q52, Q231) | alterado | 1 | teste |
| RN-PM-06 | O papel de Administrador deve ficar somente em contas do tipo supervisor. | Regra do PMO (Q22, Q52) | alterado | 1 | teste |
| RN-PM-35 | O sistema deve recusar a mudança que deixaria o Octante sem nenhum Administrador ativo. | Regra do PMO (Q52) | novo | 1 | teste |

**Entradas:** nome (obrigatório, até 20.000 caracteres); e-mail (opcional); tipo da conta; papel de Administrador. O login não muda.

**Critérios de aceite:**
- **RF-US-09, válido:** Dado um Administrador, quando ele muda o nome e o e-mail de uma conta, então os dados novos aparecem na lista e nas telas.
- **RN-PM-05, inválido:** Dado uma conta sem o papel de Administrador, quando ela tenta editar uma conta, mesmo enviando o formulário direto ao servidor, então o sistema recusa.
- **RN-PM-06, válido:** Quando o Administrador muda um gerente de projetos para supervisor e lhe dá o papel de Administrador, então a mudança é aceita.
- **RN-PM-06, inválido:** Quando o Administrador dá o papel de Administrador a um gerente de projetos, ou muda para gerente de projetos um supervisor que é Administrador, sem tirar o papel, então o sistema recusa.
- **RN-PM-35, válido:** Dado dois Administradores ativos, quando um tira o papel do outro, então a mudança é aceita.
- **RN-PM-35, inválido:** Dado um só Administrador ativo, quando ele tenta tirar o próprio papel ou mudar o próprio tipo, então o sistema recusa.
- **Entradas, inválido:** nome vazio, e-mail inválido e nome com 20.001 caracteres são recusados.

**Fora desta história:** o que acontece com os projetos de quem muda de tipo, que é a regra dos projetos (Projetos, #7), e o parecer de quem passa a supervisor (Q211, PMO, #5).
