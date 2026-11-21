---
status: accepted
---

# Hospedagem no PythonAnywhere gratuito, com o que isso impõe

O Octante roda no plano gratuito do PythonAnywhere, sem custo. O plano pago (Developer) e um servidor próprio (VPS) foram descartados, embora resolvessem limites reais. O plano gratuito não tem tarefas agendadas, contêineres nem processos sempre ligados, bloqueia e-mail por SMTP e expira todo mês. As consequências foram aceitas assim:

- **Não há notificação por prazo**, porque ela exigiria algo rodando todo dia.
- **E-mail, quando vier, sai por API HTTPS** (Brevo, SendGrid, Resend, Mailgun, Postmark). As mensagens ficam numa fila de saída numa tabela do banco e são enviadas a cada acesso ao sistema, como já acontece com o backup diário. Um RabbitMQ só faz sentido com servidor próprio, e a troca não muda as regras de negócio. A mesma fila serve para qualquer envio futuro a um serviço de fora do Octante. Os módulos não usam fila entre si, porque rodam no mesmo app e gravam no mesmo banco.
- **Docker só no desenvolvimento e na CI.** Kubernetes foi descartado. Prometheus e Grafana ficam para quando houver servidor próprio.
- **Os backups automáticos ficam no mesmo servidor do banco**, então o Administrador baixa uma cópia por semana, e o sistema avisa depois de 7 dias sem download.
- **A renovação mensal do app** é procedimento do Administrador, descrito no `DEPLOY.md`.

Decisões de origem: Q38, Q42, Q44, Q45, Q76 e Q197 em `docs/requisitos/decisoes-elicitacao.md`.
