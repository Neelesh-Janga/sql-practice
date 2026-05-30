"use strict";

/* ═══════════════════════════════════════════════════════════════
   SQL Practice — frontend application
═══════════════════════════════════════════════════════════════ */

const app = (() => {

  // ── State ──────────────────────────────────────────────────────
  let allQuestions   = [];   // { id, category, title, tables_used }
  let allCategories  = [];
  let allTheory      = [];
  let tablesData     = {};   // keyed by table name
  let currentQid     = null;
  let currentQuestion = null;
  let editor         = null;
  let solutionVisible = false;

  // ── Init ───────────────────────────────────────────────────────
  async function init() {
    initEditor();
    await Promise.all([
      fetchQuestions(),
      fetchTheory(),
      fetchTables(),
    ]);
    buildSidebar();
    showHome();
    attachGlobalKeys();
  }

  // ── CodeMirror ─────────────────────────────────────────────────
  function initEditor() {
    editor = CodeMirror.fromTextArea(document.getElementById("sql-editor"), {
      mode: "text/x-sql",
      theme: "dracula",
      lineNumbers: true,
      matchBrackets: true,
      autoCloseBrackets: true,
      tabSize: 2,
      indentWithTabs: false,
      lineWrapping: false,
      extraKeys: {
        "Ctrl-Enter": runQuery,
        "Cmd-Enter":  runQuery,
        "Ctrl-/":     (cm) => cm.execCommand("toggleComment"),
        "Cmd-/":      (cm) => cm.execCommand("toggleComment"),
      },
    });
  }

  // ── Data fetching ───────────────────────────────────────────────
  async function fetchQuestions() {
    const [cats, qs] = await Promise.all([
      fetch("/api/categories").then(r => r.json()),
      fetch("/api/questions").then(r => r.json()),
    ]);
    allCategories = cats;
    allQuestions  = qs;
    document.getElementById("question-counter").textContent =
      `${qs.length} questions`;
  }

  async function fetchTheory() {
    allTheory = await fetch("/api/theory").then(r => r.json());
  }

  async function fetchTables() {
    tablesData = await fetch("/api/tables").then(r => r.json());
  }

  // ── Sidebar ─────────────────────────────────────────────────────
  function buildSidebar() {
    const nav = document.getElementById("sidebar-nav");
    nav.innerHTML = "";

    // ── Practice section ──
    const practiceHeader = el("div", "nav-section-header", "Practice");
    nav.appendChild(practiceHeader);

    allCategories.forEach(cat => {
      const catQs = allQuestions.filter(q => q.category === cat);

      const catRow = el("div", "nav-category");
      catRow.innerHTML = `
        <span class="caret">&#9654;</span>
        <span>${cat}</span>
        <span class="cat-count">${catQs.length}</span>
      `;
      nav.appendChild(catRow);

      const qList = el("div", "nav-question-list");
      catQs.forEach(q => {
        const qRow = el("div", "nav-question");
        qRow.dataset.qid = q.id;
        qRow.innerHTML = `<span class="q-num">${q.id}</span>
                          <span class="q-title">${q.title}</span>`;
        qRow.addEventListener("click", () => loadQuestion(q.id));
        qList.appendChild(qRow);
      });
      nav.appendChild(qList);

      catRow.addEventListener("click", () => {
        catRow.classList.toggle("open");
        qList.classList.toggle("open");
      });
    });

    // ── Theory section ──
    const theoryHeader = el("div", "nav-section-header", "Theory");
    theoryHeader.style.marginTop = "12px";
    nav.appendChild(theoryHeader);

    allTheory.forEach(page => {
      const row = el("div", "nav-theory-item");
      row.dataset.slug = page.slug;
      row.innerHTML = `<span class="th-icon">${page.icon}</span>${page.title}`;
      row.addEventListener("click", () => showTheoryDetail(page.slug));
      nav.appendChild(row);
    });

    // ── Tables link ──
    const tablesHeader = el("div", "nav-section-header", "Database");
    tablesHeader.style.marginTop = "12px";
    nav.appendChild(tablesHeader);

    const tablesRow = el("div", "nav-theory-item");
    tablesRow.innerHTML = `<span class="th-icon">🗂️</span>Browse Tables`;
    tablesRow.addEventListener("click", showTableViewer);
    nav.appendChild(tablesRow);

    // ── Search filtering ──
    document.getElementById("sidebar-search").addEventListener("input", function() {
      filterSidebar(this.value.trim().toLowerCase());
    });
  }

  function filterSidebar(term) {
    const allQRows = document.querySelectorAll(".nav-question");
    if (!term) {
      // restore normal state — collapse all
      document.querySelectorAll(".nav-category").forEach(c => c.classList.remove("open"));
      document.querySelectorAll(".nav-question-list").forEach(l => {
        l.classList.remove("open");
        l.querySelectorAll(".nav-question").forEach(r => r.style.display = "");
      });
      return;
    }
    allQRows.forEach(row => {
      const title = row.querySelector(".q-title").textContent.toLowerCase();
      const match = title.includes(term);
      row.style.display = match ? "" : "none";
    });
    // Open categories that have visible questions
    document.querySelectorAll(".nav-question-list").forEach(list => {
      const hasVisible = [...list.querySelectorAll(".nav-question")]
        .some(r => r.style.display !== "none");
      list.classList.toggle("open", hasVisible);
      list.previousElementSibling?.classList.toggle("open", hasVisible);
    });
  }

  // ── View management ─────────────────────────────────────────────
  function showView(id) {
    document.querySelectorAll(".view").forEach(v => v.classList.remove("active"));
    document.getElementById(id).classList.add("active");
    // clear active nav items
    document.querySelectorAll(".nav-theory-item, .nav-question").forEach(el =>
      el.classList.remove("active")
    );
  }

  function showHome() {
    showView("view-home");
  }

  function showFirstQuestion() {
    if (allQuestions.length) loadQuestion(allQuestions[0].id);
  }

  function showTheoryList() {
    showView("view-theory-list");
    const grid = document.getElementById("theory-cards-grid");
    if (grid.children.length) return; // already rendered
    grid.innerHTML = "";
    allTheory.forEach(page => {
      const card = el("div", "theory-card");
      card.innerHTML = `
        <div class="theory-card-icon">${page.icon}</div>
        <div class="theory-card-title">${page.title}</div>
        <div class="theory-card-summary">${page.summary}</div>
      `;
      card.addEventListener("click", () => showTheoryDetail(page.slug));
      grid.appendChild(card);
    });
  }

  async function showTheoryDetail(slug) {
    showView("view-theory-detail");
    // highlight sidebar item
    document.querySelectorAll(".nav-theory-item").forEach(el => {
      el.classList.toggle("active", el.dataset.slug === slug);
    });
    const content = document.getElementById("theory-detail-content");
    content.innerHTML = '<div class="placeholder-msg"><span class="spinner"></span> Loading…</div>';
    const page = await fetch(`/api/theory/${slug}`).then(r => r.json());
    content.innerHTML = page.content;
  }

  function showTableViewer() {
    showView("view-tables");
    renderTableBrowser();
  }

  function renderTableBrowser() {
    const tabBar  = document.getElementById("table-browser-tabs");
    const content = document.getElementById("table-browser-content");
    if (tabBar.children.length) return; // already rendered

    const tables = Object.keys(tablesData);
    tables.forEach((name, i) => {
      const btn = el("button", "tab-btn" + (i === 0 ? " active" : ""));
      btn.textContent = name;
      btn.addEventListener("click", () => {
        document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        document.querySelectorAll(".table-panel").forEach(p => p.classList.remove("active"));
        document.getElementById(`panel-${name}`).classList.add("active");
      });
      tabBar.appendChild(btn);

      const panel = el("div", "table-panel" + (i === 0 ? " active" : ""));
      panel.id = `panel-${name}`;
      panel.innerHTML = buildTablePanel(name, tablesData[name]);
      content.appendChild(panel);
    });
  }

  function buildTablePanel(name, data) {
    // Schema
    let schemaHtml = `<h4>Schema — ${name}</h4>
      <table class="schema-table">
        <thead><tr><th>#</th><th>Column</th><th>Type</th><th>Not Null</th><th>Default</th><th>Flags</th></tr></thead>
        <tbody>`;
    data.schema.forEach(col => {
      const flags = [];
      if (col.pk)      flags.push('<span class="pk-tag">PK</span>');
      if (col.notnull) flags.push('<span class="fk-tag">NOT NULL</span>');
      schemaHtml += `<tr>
        <td>${col.cid + 1}</td>
        <td><strong>${col.name}</strong></td>
        <td class="type-tag">${col.type}</td>
        <td>${col.notnull ? "Yes" : "No"}</td>
        <td>${col.dflt_value ?? "—"}</td>
        <td>${flags.join(" ")}</td>
      </tr>`;
    });
    schemaHtml += "</tbody></table>";

    // Sample rows
    let sampleHtml = `<div class="sample-section"><h4>Sample Data (first 5 rows)</h4>
      <div style="overflow-x:auto">
      <table class="schema-table"><thead><tr>`;
    data.columns.forEach(c => sampleHtml += `<th>${c}</th>`);
    sampleHtml += "</tr></thead><tbody>";
    data.sample_rows.forEach(row => {
      sampleHtml += "<tr>" + row.map(v =>
        `<td>${v === null ? '<span style="color:var(--text3);font-style:italic">NULL</span>' : escHtml(String(v))}</td>`
      ).join("") + "</tr>";
    });
    sampleHtml += "</tbody></table></div></div>";

    return schemaHtml + sampleHtml;
  }

  // ── Question loading ─────────────────────────────────────────────
  async function loadQuestion(qid) {
    currentQid = qid;
    solutionVisible = false;
    hideSolution();
    clearResults();

    // highlight in sidebar
    document.querySelectorAll(".nav-question").forEach(el =>
      el.classList.toggle("active", parseInt(el.dataset.qid) === qid)
    );

    const q = await fetch(`/api/question/${qid}`).then(r => r.json());
    currentQuestion = q;

    // open the category in sidebar
    document.querySelectorAll(".nav-question").forEach(row => {
      if (parseInt(row.dataset.qid) === qid) {
        const list = row.parentElement;
        list.classList.add("open");
        list.previousElementSibling?.classList.add("open");
        row.scrollIntoView({ block: "nearest" });
      }
    });

    // Populate question header
    document.getElementById("question-category-badge").textContent = q.category;
    document.getElementById("question-number").textContent = `#${q.id}`;
    document.getElementById("question-title").textContent = q.title;
    document.getElementById("question-description").innerHTML = q.description;

    // Table badges
    const tablesEl = document.getElementById("question-tables-list");
    tablesEl.innerHTML = "";
    if (q.tables_used && q.tables_used.length) {
      q.tables_used.forEach(t => {
        const badge = el("span", "table-badge");
        badge.textContent = t;
        badge.addEventListener("click", () => showTableModal(t));
        tablesEl.appendChild(badge);
      });
      document.getElementById("question-tables").style.display = "";
    } else {
      document.getElementById("question-tables").style.display = "none";
    }

    // Load editor
    editor.setValue(q.starter_sql || "SELECT ");
    editor.focus();

    showView("view-question");
  }

  // ── Run query ───────────────────────────────────────────────────
  async function runQuery() {
    const sql = editor.getValue().trim();
    if (!sql) return;

    const btnRun = document.getElementById("btn-run");
    btnRun.disabled = true;
    btnRun.innerHTML = '<span class="spinner"></span> Running…';

    clearResults();

    try {
      const res = await fetch("/api/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sql }),
      });
      const data = await res.json();
      if (data.error) {
        showError(data.error);
      } else {
        showResultTable(data.columns, data.rows, data.count);
      }
    } catch (err) {
      showError("Network error: " + err.message);
    } finally {
      btnRun.disabled = false;
      btnRun.innerHTML = "&#9654; Run";
    }
  }

  function clearResults() {
    document.getElementById("results-placeholder").classList.remove("hidden");
    document.getElementById("results-error").classList.add("hidden");
    document.getElementById("results-table-wrap").classList.add("hidden");
    document.getElementById("results-count").textContent = "";
  }

  function showError(msg) {
    document.getElementById("results-placeholder").classList.add("hidden");
    const errEl = document.getElementById("results-error");
    errEl.textContent = msg;
    errEl.classList.remove("hidden");
    document.getElementById("results-count").textContent = "";
  }

  function showResultTable(columns, rows, count) {
    document.getElementById("results-placeholder").classList.add("hidden");
    document.getElementById("results-error").classList.add("hidden");

    const table = document.getElementById("results-table");
    table.innerHTML = "";

    // header
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    columns.forEach(col => {
      const th = document.createElement("th");
      th.textContent = col;
      headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // body
    const tbody = document.createElement("tbody");
    rows.forEach(row => {
      const tr = document.createElement("tr");
      row.forEach(val => {
        const td = document.createElement("td");
        if (val === null) {
          td.textContent = "NULL";
          td.classList.add("null-val");
        } else {
          td.textContent = String(val);
        }
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);

    document.getElementById("results-table-wrap").classList.remove("hidden");

    const label = count >= 500 ? `${count}+ rows (capped at 500)` : `${count} row${count !== 1 ? "s" : ""}`;
    document.getElementById("results-count").textContent = label;
  }

  // ── Solution ────────────────────────────────────────────────────
  function toggleSolution() {
    if (solutionVisible) {
      hideSolution();
    } else {
      showSolution();
    }
  }

  function showSolution() {
    if (!currentQuestion) return;
    document.getElementById("solution-sql-display").textContent = currentQuestion.solution_sql;
    document.getElementById("solution-explanation").innerHTML  = currentQuestion.explanation;
    document.getElementById("solution-panel").classList.remove("hidden");
    document.getElementById("btn-solution").textContent = "🔒 Hide Solution";
    solutionVisible = true;
  }

  function hideSolution() {
    document.getElementById("solution-panel").classList.add("hidden");
    document.getElementById("btn-solution").innerHTML = "&#128161; Solution";
    solutionVisible = false;
  }

  function copySolution() {
    const sql = document.getElementById("solution-sql-display").textContent;
    navigator.clipboard.writeText(sql).then(() => {
      const btn = document.getElementById("btn-copy-solution");
      btn.textContent = "Copied!";
      setTimeout(() => btn.textContent = "Copy", 1500);
    });
  }

  function resetEditor() {
    if (!currentQuestion) return;
    editor.setValue(currentQuestion.starter_sql || "SELECT ");
    clearResults();
    hideSolution();
    editor.focus();
  }

  // ── Table modal ─────────────────────────────────────────────────
  function showTableModal(tableName) {
    if (!tablesData[tableName]) return;
    const data = tablesData[tableName];

    document.getElementById("modal-table-name").textContent = tableName;

    // Schema tab
    let schHtml = `<table class="schema-table">
      <thead><tr><th>#</th><th>Column</th><th>Type</th><th>Not Null</th><th>Flags</th></tr></thead><tbody>`;
    data.schema.forEach(col => {
      const flags = [];
      if (col.pk)      flags.push('<span class="pk-tag">PK</span>');
      if (col.notnull) flags.push('<span class="fk-tag">NOT NULL</span>');
      schHtml += `<tr><td>${col.cid+1}</td><td><strong>${col.name}</strong></td>
        <td class="type-tag">${col.type}</td><td>${col.notnull?"Yes":"No"}</td>
        <td>${flags.join(" ") || "—"}</td></tr>`;
    });
    schHtml += "</tbody></table>";
    document.getElementById("modal-schema").innerHTML = schHtml;

    // Sample tab
    let sHtml = `<div style="overflow-x:auto"><table class="schema-table"><thead><tr>`;
    data.columns.forEach(c => sHtml += `<th>${c}</th>`);
    sHtml += "</tr></thead><tbody>";
    data.sample_rows.forEach(row => {
      sHtml += "<tr>" + row.map(v =>
        `<td>${v === null ? '<i style="color:var(--text3)">NULL</i>' : escHtml(String(v))}</td>`
      ).join("") + "</tr>";
    });
    sHtml += "</tbody></table></div>";
    document.getElementById("modal-sample").innerHTML = sHtml;

    // Reset to schema tab
    document.querySelectorAll(".modal-tab").forEach(t => t.classList.remove("active"));
    document.querySelector('[data-tab="schema"]').classList.add("active");
    document.getElementById("modal-schema").classList.remove("hidden");
    document.getElementById("modal-sample").classList.add("hidden");

    document.getElementById("table-modal").classList.remove("hidden");
  }

  function closeTableModal() {
    document.getElementById("table-modal").classList.add("hidden");
  }

  function switchModalTab(tab, btnEl) {
    document.querySelectorAll(".modal-tab").forEach(t => t.classList.remove("active"));
    btnEl.classList.add("active");
    document.getElementById("modal-schema").classList.toggle("hidden", tab !== "schema");
    document.getElementById("modal-sample").classList.toggle("hidden", tab !== "sample");
  }

  // ── Keyboard shortcuts ──────────────────────────────────────────
  function attachGlobalKeys() {
    document.addEventListener("keydown", e => {
      if (e.key === "Escape") closeTableModal();
    });
    document.getElementById("btn-run").addEventListener("click", runQuery);
    document.getElementById("btn-solution").addEventListener("click", toggleSolution);
    document.getElementById("btn-reset").addEventListener("click", resetEditor);
    document.getElementById("btn-close-solution").addEventListener("click", hideSolution);
    document.getElementById("btn-copy-solution").addEventListener("click", copySolution);
  }

  // ── Utilities ───────────────────────────────────────────────────
  function el(tag, cls, text) {
    const e = document.createElement(tag);
    if (cls)  e.className = cls;
    if (text) e.textContent = text;
    return e;
  }

  function escHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  // ── Public API ──────────────────────────────────────────────────
  return {
    init,
    showHome,
    showFirstQuestion,
    showTheoryList,
    showTheoryDetail,
    showTableViewer,
    showTableModal,
    closeTableModal,
    switchModalTab,
    loadQuestion,
  };

})();

document.addEventListener("DOMContentLoaded", app.init);
