# Revisão da v12: regras de negócio, heurísticas e design

## 1. Regras de negócio: inconsistências encontradas e corrigidas

| # | Inconsistência | Por que é um problema | Regra nova |
|---|---|---|---|
| R1 | Projeto encerrado ou cancelado continuava editável | O histórico de um projeto fechado podia ser alterado sem registro | Projeto encerrado ou cancelado fica **somente para consulta**: faixa 🔒 em todas as telas; para alterar, é preciso reabrir na tela de encerramento |
| R2 | O termo de abertura podia ser aprovado sem dizer quem aprovou | A aprovação é o que autoriza o projeto (PMBOK, termo de abertura) | **Aprovar exige "Aprovado por"** |
| R3 | O fluxo considerava a fase Iniciar concluída com o termo ainda "em revisão" | Contradiz a regra acima: projeto sem termo aprovado não está autorizado | A etapa virou **"Termo de abertura aprovado"**. Os painéis da visão geral continuam aparecendo com o termo em revisão |
| R4 | Mudanças aprovadas ou implementadas podiam ser excluídas | Quebra a trilha de auditoria do controle de mudanças | **Só mudanças pendentes ou rejeitadas podem ser excluídas.** Para desfazer uma aprovada, registra-se uma nova mudança |
| R5 | Iterações com datas sobrepostas eram aceitas | Iteração é um período fixo (timebox); a sobreposição distorce a velocidade e o cronograma | **Iterações não se sobrepõem** |
| R6 | A mesma parte interessada podia ser cadastrada duas vezes | Duplicava a análise, a priorização e o engajamento | Nome repetido (sem diferenciar maiúsculas) é recusado |
| R7 | Recurso físico aceitava desperdício maior que o uso | Número impossível, que distorce o % de desperdício | **Desperdício ≤ quantidade usada**; uso acima do planejado vira alerta |
| R8 | Fornecedor prometendo entregar depois da data em que o projeto precisa não gerava aviso | O atraso só aparecia quando já tinha acontecido | **Alerta alto** assim que a entrega prometida passa da data em que o projeto precisa |
| R9 | Qualquer usuário podia excluir um projeto inteiro | Com o app publicado, um estagiário apagava o trabalho de todos | **Excluir projeto: só administrador** (o backup já era só do administrador) |

## 2. Avaliação heurística (Nielsen) e correções

| Heurística | Problema encontrado | Correção |
|---|---|---|
| 1. Visibilidade do estado do sistema | Botão sem retorno depois do clique; a situação "encerrado" não aparecia | Botão vira "Aguarde…" ao enviar; faixa "Projeto encerrado: somente consulta"; item ativo do menu marcado (`aria-current`) |
| 2. Correspondência com o mundo real | Termos do PMBOK sem tradução | Mantidos os nomes simples do menu (v9/v10); a etapa do fluxo diz exatamente o que precisa estar pronto ("Termo de abertura **aprovado**") |
| 3. Controle e liberdade | Sair da página perdia o formulário preenchido sem aviso | Aviso ao sair com alterações não salvas; diálogo de exclusão com "Cancelar" em foco |
| 4. Consistência e padrões | Cerca de 60 cores fixas diferentes; botões e campos com alturas variadas | Tokens de cor (variáveis CSS) e componentes únicos: botão primário, secundário e de perigo; campos com 40 px |
| 5. Prevenção de erros | 21 botões "Excluir" sem confirmação; obrigatórios sem marcação; envio duplo | Diálogo de confirmação em toda exclusão; asterisco vermelho e legenda "* campo obrigatório"; botão bloqueado após o 1º clique |
| 6. Reconhecer em vez de lembrar | No celular o menu escondia o conteúdo | Botão "☰ Menu: <tela atual>" mostra onde a pessoa está |
| 7. Flexibilidade e eficiência | Navegação só com o mouse | Link "Pular para o conteúdo" e foco visível em tudo que é clicável |
| 8. Estética e minimalismo | Selo "módulo" repetido em todas as linhas dos domínios; cartões espremidos | Selo removido; cartões de situação com largura mínima de 190 px; menu recolhível no celular |
| 9. Ajudar a reconhecer e corrigir erros | Mensagem de erro não era anunciada | Mensagem de erro com `role="alert"`, foco automático e ícone; campo inválido destacado em vermelho |
| 10. Ajuda e documentação | Já atendia (dicas, glossário, faixa "Para que serve") | Faixa de ajuda recolorida em azul de informação, para não competir com a cor das ações |

## 3. Design (front-end)

**Paleta.** Topo azul-marinho `#121a33`, cor principal índigo `#3a45c4` (6,9:1 com texto branco) e fundo cinza-azulado `#f4f6fb`.
Status: vermelho `#b42d27`, âmbar `#915700`, verde `#1b7343`, azul de informação `#2b62a8`. Cada um tem versões clara, borda
e texto, todas com contraste AA. Status sempre aparece com **cor + ícone + texto**, nunca só com cor.

**Gráficos.** Séries em índigo `#3a45c4`, laranja `#d9741f` e ciano `#1a9bb0`. A combinação foi verificada para luminosidade,
croma, separação para daltonismo (protanopia e tritanopia) e contraste.

**Componentes.** Cartões com raio de 12 px e sombra leve. Menu lateral com indicador da tela atual. Botões e campos com 40 px de
altura (alvo de toque). Tabelas com cabeçalho discreto e rolagem horizontal no celular. Diálogo modal nativo (`<dialog>`) para
confirmações. Respeita "reduzir movimento" do sistema operacional.

**Regra de manutenção.** Nenhuma cor fixa fora de `:root` em `static/style.css`; um teste automático garante isso.
