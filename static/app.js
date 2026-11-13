// Pequenas melhorias de usabilidade. O app funciona sem JavaScript.
(function () {
  // Avisa antes de sair de um formulário com alterações não salvas.
  let alterado = false;
  document.querySelectorAll("form[method=post]").forEach(function (form) {
    form.addEventListener("input", function () { alterado = true; });
    form.addEventListener("submit", function () { alterado = false; });
  });
  window.addEventListener("beforeunload", function (e) {
    if (alterado) { e.preventDefault(); e.returnValue = ""; }
  });

  // Some com as mensagens de sucesso depois de alguns segundos.
  document.querySelectorAll(".flash-ok").forEach(function (el) {
    setTimeout(function () { el.style.transition = "opacity .4s"; el.style.opacity = "0"; }, 4000);
    setTimeout(function () { el.remove(); }, 4500);
  });
})();

// Formulário de risco: mostra só as estratégias do tipo escolhido (ameaça ou oportunidade).
(function () {
  const form = document.getElementById("form-risco");
  if (!form) return;
  function atualizar() {
    const marcado = form.querySelector("input[name=tipo]:checked");
    const tipo = marcado ? marcado.value : "ameaca";
    form.querySelectorAll("[data-estrategias]").forEach(function (fs) {
      fs.hidden = fs.dataset.estrategias !== tipo;
    });
  }
  form.querySelectorAll("input[name=tipo]").forEach(function (el) { el.addEventListener("change", atualizar); });
  atualizar();
})();

// Formulário de mudança: contador de impactos avaliados.
(function () {
  const contador = document.getElementById("contador-impactos");
  if (!contador) return;
  const campos = document.querySelectorAll("[data-impacto]");
  function contar() {
    const n = Array.prototype.filter.call(campos, function (c) { return c.value.trim() !== ""; }).length;
    contador.textContent = n + "/" + campos.length + " avaliados";
  }
  campos.forEach(function (c) { c.addEventListener("input", contar); });
  contar();
})();

// Dicas de preenchimento: exemplo no campo vazio (placeholder) e orientação em letra pequena.
(function () {
  const el = document.getElementById("dicas-dados");
  if (!el) return;
  let dicas = {};
  try { dicas = JSON.parse(el.textContent) || {}; } catch (e) { return; }
  const botao = document.getElementById("alternar-dicas");
  function ligado() { try { return localStorage.getItem("dicas") !== "off"; } catch (e) { return true; } }
  function achar(nome) {
    if (dicas[nome]) return dicas[nome];
    const base = nome.replace(/\d+$/, "");
    if (base !== nome) {
      if (dicas[base]) return dicas[base];
      if (dicas[base.replace(/_$/, "")]) return dicas[base.replace(/_$/, "")];
    }
    return null;
  }
  const guardados = [];
  document.querySelectorAll("form[method=post] [name]").forEach(function (campo) {
    if (campo.type === "hidden" || campo.type === "submit" || campo.type === "checkbox" || campo.type === "radio") return;
    const d = achar(campo.name);
    if (!d) return;
    const exemplo = d[0], ajuda = d[1];
    if (exemplo && !campo.placeholder && (campo.tagName === "TEXTAREA" || campo.type === "text" || campo.type === "number" || campo.type === "")) {
      campo.placeholder = exemplo;
    }
    let nota = null;
    const rotulo = campo.closest("label");
    const jaTemAjuda = rotulo && rotulo.querySelector(".ajuda, small");
    if (ajuda && !jaTemAjuda && !campo.closest("td") && campo.type !== "date") {
      nota = document.createElement("small");
      nota.className = "dica-campo";
      nota.textContent = ajuda;
      campo.insertAdjacentElement("afterend", nota);
    } else if (ajuda && !campo.title) {
      campo.title = ajuda;
    }
    guardados.push({ campo: campo, exemplo: exemplo, nota: nota, original: campo.getAttribute("placeholder") });
  });
  function aplicar() {
    const on = ligado();
    guardados.forEach(function (g) {
      if (g.nota) g.nota.hidden = !on;
    });
    const ap = document.getElementById("ajuda-pagina");
    if (ap) ap.hidden = !on;
    if (botao) { botao.setAttribute("aria-pressed", on ? "true" : "false"); botao.classList.toggle("desligado", !on); }
  }
  if (botao) botao.addEventListener("click", function () {
    try { localStorage.setItem("dicas", ligado() ? "off" : "on"); } catch (e) {}
    aplicar();
  });
  aplicar();
})();

// Modo essencial (padrão) x modo completo: esconde telas avançadas do menu lateral.
(function () {
  const botao = document.getElementById("alternar-modo");
  function completo() { try { return localStorage.getItem("modo") === "completo"; } catch (e) { return false; } }
  function aplicar() {
    document.body.classList.toggle("modo-completo", completo());
    if (botao) botao.textContent = completo() ? "Voltar ao modo essencial" : "Mostrar todas as telas";
  }
  if (botao) botao.addEventListener("click", function () {
    try { localStorage.setItem("modo", completo() ? "essencial" : "completo"); } catch (e) {}
    aplicar();
  });
  aplicar();
})();

// ---------------------------------------------------------------- v12: usabilidade (heurísticas de Nielsen)
(function () {
  // Marca menu ativo para leitores de tela (H1: visibilidade do estado).
  document.querySelectorAll(".lateral a.ativo").forEach(function (a) { a.setAttribute("aria-current", "page"); });

  // Tabelas largas rolam dentro do cartão no celular, em vez de estourar a página.
  document.querySelectorAll("main table").forEach(function (t) {
    if (t.parentElement.classList.contains("rolagem-tabela")) return;
    const w = document.createElement("div"); w.className = "rolagem-tabela";
    t.parentNode.insertBefore(w, t); w.appendChild(t);
  });

  // Campos obrigatórios com asterisco + legenda (H5: prevenção de erros).
  document.querySelectorAll("form[method=post]").forEach(function (form) {
    let tem = false;
    form.querySelectorAll("[required]").forEach(function (campo) {
      const rot = campo.closest("label");
      if (!rot || rot.querySelector(".obrig")) return;
      const no = Array.from(rot.childNodes).find(function (n) { return n.nodeType === 3 && n.textContent.trim(); });
      if (!no) return;
      // Junta texto e asterisco num só elemento para não quebrar o layout do rótulo.
      const texto = document.createElement("span");
      texto.textContent = no.textContent.replace(/\s*\*\s*$/, "").trimEnd();
      const marca = document.createElement("span");
      marca.className = "obrig"; marca.textContent = "*"; marca.setAttribute("aria-hidden", "true");
      texto.appendChild(marca);
      no.replaceWith(texto);
      tem = true;
    });
    if (tem && form.querySelectorAll("[required]").length > 1 && !form.querySelector(".legenda-obrig")) {
      const p = document.createElement("p"); p.className = "legenda-obrig"; p.textContent = "* campo obrigatório";
      form.prepend(p);
    }
  });

  // Diálogo de confirmação para ações destrutivas (H3 controle do usuário, H5 prevenção de erros).
  let dialogo = null;
  function confirmar(texto, aoConfirmar) {
    if (!window.HTMLDialogElement) { if (window.confirm(texto)) aoConfirmar(); return; }
    if (!dialogo) {
      dialogo = document.createElement("dialog");
      dialogo.className = "confirmar";
      dialogo.innerHTML = '<h2>Tem certeza?</h2><p class="texto"></p><div class="acoes">' +
        '<button type="button" class="botao botao-sec" value="nao">Cancelar</button>' +
        '<button type="button" class="botao botao-perigo" value="sim">Excluir</button></div>';
      document.body.appendChild(dialogo);
    }
    dialogo.querySelector(".texto").textContent = texto;
    dialogo.querySelectorAll("button").forEach(function (b) {
      b.onclick = function () { dialogo.close(); if (b.value === "sim") aoConfirmar(); };
    });
    dialogo.showModal();
    dialogo.querySelector("button[value=nao]").focus();
  }
  function destrutivo(form, botao) {
    const valor = (botao && botao.value) || "";
    const acao = form.getAttribute("action") || "";
    return /^excluir/.test(valor) || /\/excluir$/.test(acao) || (botao && botao.hasAttribute("data-confirmar"));
  }

  // Formulário alterado e não salvo (H3: evita perder trabalho sem querer).
  let sujo = false;
  document.querySelectorAll("form[method=post]").forEach(function (form) {
    if (form.closest(".topo")) return;
    form.addEventListener("input", function () { sujo = true; });
    form.addEventListener("change", function () { sujo = true; });
  });
  window.addEventListener("beforeunload", function (e) { if (sujo) { e.preventDefault(); e.returnValue = ""; } });

  document.addEventListener("submit", function (e) {
    const form = e.target;
    const botao = e.submitter;
    if (form.dataset.confirmado !== "1" && destrutivo(form, botao)) {
      e.preventDefault();
      const texto = (botao && botao.getAttribute("data-confirmar")) || "Este registro será excluído e não poderá ser recuperado.";
      confirmar(texto, function () {
        form.dataset.confirmado = "1";
        if (botao && botao.name) { const h = document.createElement("input"); h.type = "hidden"; h.name = botao.name; h.value = botao.value; form.appendChild(h); }
        sujo = false;
        form.submit();
      });
      return;
    }
    sujo = false;
    // Estado de ocupado e proteção contra duplo envio (H1 + H5).
    if (botao && botao.classList.contains("botao")) {
      setTimeout(function () { botao.disabled = true; botao.classList.add("ocupado"); botao.dataset.rotulo = botao.textContent; botao.textContent = "Aguarde…"; }, 0);
    }
  });

  // Erro: leva o foco à mensagem e destaca campos obrigatórios vazios (H9: ajudar a reconhecer e corrigir erros).
  const erro = document.querySelector(".flash-erro");
  if (erro) { erro.setAttribute("tabindex", "-1"); erro.focus({ preventScroll: false }); }
  document.querySelectorAll("[required]").forEach(function (campo) {
    campo.addEventListener("invalid", function () { campo.classList.add("campo-invalido"); });
    campo.addEventListener("input", function () { campo.classList.remove("campo-invalido"); });
  });
})();

// Menu lateral recolhível no celular (H8: o conteúdo vem primeiro).
(function () {
  const b = document.getElementById("abrir-menu"), m = document.getElementById("menu-lateral");
  if (!b || !m) return;
  const atual = m.querySelector("a.ativo:last-of-type") || m.querySelector("a.ativo");
  if (atual) b.textContent = "☰ Menu: " + atual.textContent.trim();
  b.addEventListener("click", function () {
    const aberto = m.classList.toggle("aberta");
    b.setAttribute("aria-expanded", aberto ? "true" : "false");
  });
})();

// v13: sem JavaScript embutido no HTML (permite a política de segurança de conteúdo).
document.querySelectorAll("[data-enviar-ao-mudar]").forEach(function (el) {
  el.addEventListener("change", function () { el.form && el.form.submit(); });
});
document.querySelectorAll("[data-imprimir]").forEach(function (el) {
  el.addEventListener("click", function () { window.print(); });
});
// Token CSRF em todo formulário que envia dados.
(function () {
  const meta = document.querySelector('meta[name="csrf-token"]');
  if (!meta) return;
  document.querySelectorAll("form[method=post], form[method=POST]").forEach(function (f) {
    if (f.querySelector("input[name=_csrf]")) return;
    const h = document.createElement("input"); h.type = "hidden"; h.name = "_csrf"; h.value = meta.content; f.appendChild(h);
  });
})();

// v14: "/" foca a busca (atalho de teclado, heurística 7).
document.addEventListener("keydown", function (e) {
  const alvo = e.target.tagName;
  if (e.key === "/" && !/INPUT|TEXTAREA|SELECT/.test(alvo) && !e.target.isContentEditable) {
    const b = document.getElementById("busca-global");
    if (b) { e.preventDefault(); b.focus(); }
  }
});
