<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Skill Test — Transcription</title>
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Source+Sans+3:wght@300;400;600&family=Courier+Prime:wght@400;700&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  /* ── LIGHT ───────────────────────────────── */
  [data-theme="light"] {
    --bg:           #f0f2f8;
    --topbar-bg:    #ffffff;
    --topbar-border:#e2e6f0;
    --card-bg:      #ffffff;
    --card-border:  #e2e6f0;
    --text:         #1a1f36;
    --text-muted:   #6b7280;
    --textarea-bg:  #fafbfd;
    --textarea-border:#d1d5e0;
    --textarea-focus:#2563eb;
    --textarea-text:#1a1f36;
    --placeholder:  #9ca3af;
    --accent:       #2563eb;
    --accent-text:  #ffffff;
    --btn-reset-bg: #f3f4f6;
    --btn-reset-text:#374151;
    --btn-reset-border:#d1d5e0;
    --timer-bg:     rgba(37,99,235,.08);
    --timer-border: rgba(37,99,235,.25);
    --timer-color:  #2563eb;
    --toggle-bg:    #f3f4f6;
    --toggle-border:#d1d5e0;
    --toggle-text:  #374151;
    --shadow:       0 2px 16px rgba(0,0,0,.07);
  }

  /* ── DARK ────────────────────────────────── */
  [data-theme="dark"] {
    --bg:           #0d1117;
    --topbar-bg:    rgba(0,0,0,.4);
    --topbar-border:rgba(255,255,255,.08);
    --card-bg:      rgba(255,255,255,.04);
    --card-border:  rgba(255,255,255,.1);
    --text:         #f1f5f9;
    --text-muted:   rgba(255,255,255,.45);
    --textarea-bg:  transparent;
    --textarea-border:rgba(255,255,255,.12);
    --textarea-focus:#f0a500;
    --textarea-text:#f1f5f9;
    --placeholder:  rgba(255,255,255,.2);
    --accent:       #f0a500;
    --accent-text:  #0d1117;
    --btn-reset-bg: transparent;
    --btn-reset-text:rgba(255,255,255,.6);
    --btn-reset-border:rgba(255,255,255,.18);
    --timer-bg:     rgba(240,165,0,.12);
    --timer-border: rgba(240,165,0,.35);
    --timer-color:  #f0a500;
    --toggle-bg:    rgba(255,255,255,.08);
    --toggle-border:rgba(255,255,255,.15);
    --toggle-text:  #f1f5f9;
    --shadow:       none;
  }

  html, body {
    height: 100%;
  }

  body {
    font-family: 'Source Sans 3', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    transition: background .3s, color .3s;
    position: relative;
  }

  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
      none;
    pointer-events: none;
    z-index: 0;
  }

  /* ── TOPBAR ──────────────────────────────── */
  .topbar {
    position: sticky;
    top: 0;
    z-index: 50;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 28px;
    height: 58px;
    background: var(--topbar-bg);
    border-bottom: 1px solid var(--topbar-border);
    box-shadow: var(--shadow);
    transition: background .3s, border-color .3s;
  }

  .topbar-left {
    display: flex;
    align-items: center;
    gap: 20px;
  }

  .brand {
    font-family: 'Rajdhani', sans-serif;
    font-size: 17px;
    font-weight: 700;
    letter-spacing: 2px;
    color: var(--accent);
    transition: color .3s;
  }

  .meta-item {
    font-size: 13px;
    color: var(--text-muted);
    transition: color .3s;
  }

  .meta-item strong {
    color: var(--text);
    font-weight: 600;
    transition: color .3s;
  }

  .topbar-right {
    display: flex;
    align-items: center;
    gap: 14px;
  }

  /* Timer */
  .timer-wrap {
    display: flex;
    align-items: center;
    gap: 7px;
    background: var(--timer-bg);
    border: 1px solid var(--timer-border);
    border-radius: 6px;
    padding: 5px 14px;
    transition: background .3s, border-color .3s;
  }

  .timer-wrap svg {
    width: 14px; height: 14px;
    color: var(--timer-color);
    flex-shrink: 0;
    transition: color .3s;
  }

  #timer {
    font-family: 'Rajdhani', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: var(--timer-color);
    min-width: 52px;
    text-align: center;
    transition: color .3s;
  }

  /* Theme toggle */
  .theme-toggle {
    display: flex;
    align-items: center;
    gap: 6px;
    background: var(--toggle-bg);
    border: 1px solid var(--toggle-border);
    border-radius: 999px;
    padding: 6px 14px 6px 10px;
    cursor: pointer;
    transition: background .3s, border-color .3s;
    outline: none;
  }

  .theme-toggle:hover { opacity: .8; }

  .theme-toggle svg {
    width: 15px; height: 15px;
    color: var(--toggle-text);
    transition: color .3s;
  }

  .theme-toggle .lbl {
    font-family: 'Rajdhani', sans-serif;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1px;
    color: var(--toggle-text);
    transition: color .3s;
  }

  /* ── MAIN ────────────────────────────────── */
  .main {
    position: relative;
    z-index: 1;
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 32px 20px 40px;
    gap: 20px;
    max-width: 860px;
    width: 100%;
    margin: 0 auto;
  }

  /* ── TYPING CARD ─────────────────────────── */
  .typing-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 10px;
    width: 100%;
    overflow: hidden;
    box-shadow: var(--shadow);
    transition: background .3s, border-color .3s;
  }

  .typing-card-header {
    padding: 11px 20px;
    border-bottom: 1px solid var(--card-border);
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-muted);
    transition: border-color .3s, color .3s;
  }

  #typingBox {
    width: 100%;
    height: 420px;
    background: var(--textarea-bg);
    border: none;
    outline: none;
    padding: 22px 24px;
    font-family: 'Courier Prime', monospace;
    font-size: 17px;
    line-height: 1.9;
    color: var(--textarea-text);
    resize: none;
    caret-color: var(--accent);
    transition: background .3s, color .3s;
  }

  #typingBox::placeholder { color: var(--placeholder); }

  /* ── ACTIONS ─────────────────────────────── */
  .actions {
    display: flex;
    gap: 12px;
    width: 100%;
    justify-content: flex-end;
  }

  .btn {
    padding: 11px 28px;
    border-radius: 6px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    border: none;
    cursor: pointer;
    transition: opacity .2s, transform .1s, background .3s, color .3s;
  }

  .btn:active { transform: scale(.97); }
  .btn:hover  { opacity: .84; }

  .btn-primary {
    background: var(--accent);
    color: var(--accent-text);
  }

  .btn-secondary {
    background: var(--btn-reset-bg);
    color: var(--btn-reset-text);
    border: 1px solid var(--btn-reset-border);
  }

  /* ── SUBMIT OVERLAY ──────────────────────── */
  .overlay {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,.6);
    backdrop-filter: blur(6px);
    align-items: center;
    justify-content: center;
    z-index: 200;
  }

  .overlay.show { display: flex; }

  .overlay-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 10px;
    padding: 40px 44px;
    text-align: center;
    max-width: 340px;
    width: 90%;
    box-shadow: 0 8px 40px rgba(0,0,0,.3);
  }

  .overlay-card h3 {
    font-family: 'Rajdhani', sans-serif;
    font-size: 22px;
    color: var(--text);
    margin-bottom: 8px;
  }

  .overlay-card p {
    font-size: 13px;
    color: var(--text-muted);
  }

  .spinner {
    width: 36px; height: 36px;
    border: 3px solid color-mix(in srgb, var(--accent) 25%, transparent);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin .7s linear infinite;
    margin: 0 auto 20px;
  }

  @keyframes spin { to { transform: rotate(360deg); } }
</style>
</head>
<body>

<!-- ── TOPBAR ─────────────────────────────── -->
<div class="topbar">
  <div class="topbar-left">
    <div class="brand">Steno &nbsp;·&nbsp; SKILL TEST</div>
    <div class="meta-item">{{ student_name }} &nbsp;·&nbsp; Code: <strong>{{ code }}</strong></div>
  </div>
  <div class="topbar-right">
    <div class="timer-wrap">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
      </svg>
      <div id="timer">00:00</div>
    </div>

    <button class="theme-toggle" onclick="toggleTheme()">
      <svg id="iconMoon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
      </svg>
      <svg id="iconSun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:none">
        <circle cx="12" cy="12" r="5"/>
        <line x1="12" y1="1"  x2="12" y2="3"/>  <line x1="12" y1="21" x2="12" y2="23"/>
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>  <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
        <line x1="1" y1="12" x2="3" y2="12"/>   <line x1="21" y1="12" x2="23" y2="12"/>
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>  <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
      </svg>
      <span class="lbl" id="themeLabel">Dark</span>
    </button>
  </div>
</div>

<!-- ── MAIN ──────────────────────────────── -->
<div class="main">

  <div class="typing-card">
    <div class="typing-card-header">Type your transcription below</div>
    <textarea id="typingBox"
      placeholder="Begin typing here — timer starts automatically on first keystroke…"
      spellcheck="false" autocorrect="off" autocapitalize="off"></textarea>
  </div>

  <div class="actions">
    <button class="btn btn-secondary" onclick="resetTest()">Reset</button>
    <button class="btn btn-primary"   onclick="confirmSubmit()">Submit Test</button>
  </div>

</div>

<!-- ── OVERLAY ────────────────────────────── -->
<div class="overlay" id="overlay">
  <div class="overlay-card">
    <div class="spinner"></div>
    <h3>Evaluating…</h3>
    <p>Please wait while your transcription is being assessed.</p>
  </div>
</div>

<script>
  /* ── Theme ─────────────────────────────── */
  const html      = document.documentElement;
  const iconSun   = document.getElementById("iconSun");
  const iconMoon  = document.getElementById("iconMoon");
  const themeLabel = document.getElementById("themeLabel");

  applyTheme(localStorage.getItem("ssc-theme") || "light");

  function applyTheme(theme) {
    html.setAttribute("data-theme", theme);
    localStorage.setItem("ssc-theme", theme);
    const dark = theme === "dark";
    iconSun.style.display  = dark ? "block" : "none";
    iconMoon.style.display = dark ? "none"  : "block";
    themeLabel.textContent = dark ? "Light" : "Dark";
  }

  function toggleTheme() {
    applyTheme(html.getAttribute("data-theme") === "dark" ? "light" : "dark");
  }

  /* ── Timer ─────────────────────────────── */
  let startTime = null, timerInterval = null;
  const typingBox = document.getElementById("typingBox");
  const timerEl   = document.getElementById("timer");

  typingBox.addEventListener("input", () => {
    if (!startTime) {
      startTime = Date.now();
      timerInterval = setInterval(tick, 1000);
    }
  });

  function tick() {
    const s = Math.floor((Date.now() - startTime) / 1000);
    timerEl.textContent = pad(Math.floor(s / 60)) + ":" + pad(s % 60);
  }

  function pad(n) { return String(n).padStart(2, "0"); }

  /* ── Submit ─────────────────────────────── */
  function confirmSubmit() {
    if (!typingBox.value.trim()) { alert("Please type something before submitting."); return; }
    submitTest();
  }

  async function submitTest() {
    const typedText   = typingBox.value.trim();
    const passageCode = "{{ code }}";
    const elapsed     = startTime ? Math.floor((Date.now() - startTime) / 1000) : 0;
    const studentId   = new URLSearchParams(window.location.search).get("student") || "";

    document.getElementById("overlay").classList.add("show");

    try {
      const res  = await fetch("/submit-test", {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify({ typed_text: typedText, passage_code: passageCode, time_taken: elapsed, student_id: studentId })
      });
      const data = await res.json();
      if (data.status === "ok") {
        window.location = "/results";
      } else {
        document.getElementById("overlay").classList.remove("show");
        alert("Error: " + (data.message || "Submission failed."));
      }
    } catch (err) {
      document.getElementById("overlay").classList.remove("show");
      alert("Submission failed. Please try again.");
    }
  }

  /* ── Reset ──────────────────────────────── */
  function resetTest() {
    if (!confirm("Reset the test? All typed text will be lost.")) return;
    typingBox.value = "";
    startTime = null;
    clearInterval(timerInterval);
    timerEl.textContent = "00:00";
  }

  /* ── Security ───────────────────────────── */
  typingBox.addEventListener("paste",       e => e.preventDefault());
  typingBox.addEventListener("contextmenu", e => e.preventDefault());
  document.addEventListener("keydown", e => {
    if (e.ctrlKey && ["v","V","c","C"].includes(e.key)) e.preventDefault();
  });
</script>

</body>
</html>
