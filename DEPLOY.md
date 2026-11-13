# Publicar o Octante na internet (PythonAnywhere, plano grátis)

Resultado: o app fica em `https://SEU_USUARIO.pythonanywhere.com`, com login. Leva uns 15 minutos.
Troque **SEU_USUARIO** pelo nome de usuário que você criar no PythonAnywhere em todos os passos.

## 1. Criar a conta
1. Acesse https://www.pythonanywhere.com e clique em **Pricing & signup** → **Create a Beginner account** (grátis).
2. O nome de usuário vira o endereço do site (ex.: `gestorpmo` → `gestorpmo.pythonanywhere.com`).

## 2. Enviar os arquivos
1. No painel, abra a aba **Files**.
2. Clique em **Upload a file** e envie o `gestor-pmbok7-v18.zip`.
3. Abra a aba **Consoles** → **Bash** e rode, uma linha por vez:

```bash
unzip gestor-pmbok7-v18.zip
cd gestor-pmbok7
python3.13 -m pip install --user -r requirements.txt   # Flask e openpyxl (Excel)
```

## 3. Criar o site
1. Aba **Web** → **Add a new web app** → **Next**.
2. Escolha **Manual configuration** (não escolha "Flask") → **Python 3.13** → **Next**.
3. Ainda na aba **Web**, em **Code**:
   - **Source code**: `/home/SEU_USUARIO/gestor-pmbok7`
   - Clique no link do **WSGI configuration file**, apague todo o conteúdo e cole:

```python
import sys
sys.path.insert(0, "/home/SEU_USUARIO/gestor-pmbok7")
from wsgi import application
```

   Clique em **Save**.
4. Em **Static files**, adicione: URL `/static/` → Directory `/home/SEU_USUARIO/gestor-pmbok7/static`
5. Em **Security**, ligue **Force HTTPS**.
6. Clique no botão verde **Reload** no topo da aba Web.

## 4. Criar o administrador (faça na hora)
Abra `https://SEU_USUARIO.pythonanywhere.com`. A tela **Primeiro acesso** cria a conta de administrador.
Faça isso logo depois do Reload: até existir o primeiro usuário, quem abrir o endereço pode criar essa conta.
Depois, em **Usuários** (no topo), cadastre cada estagiário com uma senha inicial e peça que troquem em "Minha senha".

## Levar os dados do seu computador (opcional)
Antes do passo 3.6, na aba **Files**, entre em `gestor-pmbok7/instance` e envie o seu `gestor.db`
(fica em `gestor-pmbok7\instance` no seu PC). O app atualiza o banco sozinho. Como esse banco ainda não tem usuários,
a tela de Primeiro acesso aparece do mesmo jeito.

## Manutenção
- **Renovar**: no plano grátis o site sai do ar se não for renovado. Entre na aba **Web** e clique em
  **Run until 1 month from today** (o PythonAnywhere manda e-mail antes de expirar).
- **Backup**: logado como administrador, use o link "baixar backup" no rodapé da página de projetos.
- **Atualizar para uma versão nova**: envie o zip novo, rode `unzip -o gestor-pmbok7-vXX.zip` no console Bash
  (a pasta `instance`, com os dados, não é sobrescrita porque não vem no zip) e clique em **Reload**.
- **Erros**: na aba Web, o link **Error log** mostra o que deu errado.

## Limites do plano grátis
1 site, 512 MB de disco, endereço `*.pythonanywhere.com`. Para uma equipe pequena de PMO é suficiente.
