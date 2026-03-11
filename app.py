import streamlit as st
import pandas as pd
import unicodedata
import smtplib
import imaplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

st.set_page_config(page_title="MailForge", page_icon="📮", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.stApp { background: #0a0a0f; color: #e8e8f0; }
.main .block-container { max-width: 820px; padding: 2.5rem 2rem 5rem; }
header[data-testid="stHeader"],
.stAppHeader,
[data-testid="stDecoration"],
[data-testid="stToolbar"] { display: none !important; }

/* ── Header ── */
.mf-header { display: flex; align-items: center; gap: 18px; margin-bottom: 48px; }
.mf-logo {
  width: 56px; height: 56px; border-radius: 16px; flex-shrink: 0;
  background: linear-gradient(145deg, #c471ed, #7b5ea7, #4776e6);
  display: flex; align-items: center; justify-content: center; font-size: 26px;
  box-shadow: 0 8px 32px rgba(196,113,237,0.35);
}
.mf-title { font-size: 2.8rem; font-weight: 800; letter-spacing: -0.04em; line-height: 1; margin: 0;
  background: linear-gradient(90deg, #c471ed, #7b5ea7, #4776e6);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.mf-sub { font-family: 'DM Mono', monospace; font-size: 0.72rem; color: #6b6b88; margin-top: 6px; letter-spacing: 0.06em; }

/* ── Cards ── */
.card { background: #12121a; border: 1px solid #1e1e2e; border-radius: 16px; padding: 26px 28px; margin-bottom: 16px; }
.card-accent { border-color: rgba(196,113,237,0.4); background: linear-gradient(135deg, rgba(196,113,237,0.04), rgba(71,118,230,0.03)); }
.card-label { font-family: 'DM Mono', monospace; font-size: 0.65rem; color: #7b5ea7; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 3px; }
.card-title { font-size: 1rem; font-weight: 700; color: #e8e8f0; margin-bottom: 18px; }

/* ── Variable chips ── */
.var-row { display: flex; gap: 8px; margin-bottom: 14px; }
.var-chip {
  background: rgba(196,113,237,0.12); border: 1px solid rgba(196,113,237,0.3);
  color: #c471ed; border-radius: 6px; padding: 4px 12px;
  font-family: 'DM Mono', monospace; font-size: 0.75rem;
  cursor: pointer; transition: all 0.15s; user-select: none;
}
.var-chip:hover { background: rgba(196,113,237,0.25); border-color: rgba(196,113,237,0.6); }

/* ── Badges ── */
.badge-ok  { display:inline-flex; align-items:center; gap:6px; background:rgba(74,222,128,0.1); border:1px solid rgba(74,222,128,0.3); color:#4ade80; border-radius:6px; padding:4px 12px; font-family:'DM Mono',monospace; font-size:0.74rem; }
.badge-warn{ display:inline-flex; align-items:center; gap:6px; background:rgba(250,204,21,0.1); border:1px solid rgba(250,204,21,0.3); color:#facc15; border-radius:6px; padding:4px 12px; font-family:'DM Mono',monospace; font-size:0.74rem; }

/* ── Example line ── */
.example-line { font-family:'DM Mono',monospace; font-size:0.78rem; color:#6b6b88; margin-top:10px; padding:10px 14px; background:#0e0e18; border-radius:8px; border-left:3px solid #7b5ea7; }
.example-line span { color:#c471ed; }

/* ── Preview card ── */
.prev-card { background:#0e0e18; border:1px solid #1e1e2e; border-radius:10px; padding:14px 18px; margin-bottom:10px; }
.prev-to { font-family:'DM Mono',monospace; font-size:0.7rem; color:#7b5ea7; margin-bottom:4px; letter-spacing:0.04em; }
.prev-subj { font-size:0.9rem; font-weight:600; margin-bottom:8px; }
.prev-body { font-family:'DM Mono',monospace; font-size:0.74rem; color:#6b6b88; border-top:1px solid #1e1e2e; padding-top:8px; white-space:pre-wrap; line-height:1.6; }

/* ── Hint ── */
.hint { background:#0e0e18; border:1px solid #1e1e2e; border-radius:8px; padding:12px 16px; font-family:'DM Mono',monospace; font-size:0.74rem; color:#6b6b88; line-height:1.7; margin-bottom:14px; }
.hint a { color:#c471ed; }
.hint code { background:rgba(196,113,237,0.12); color:#c471ed; padding:1px 6px; border-radius:4px; }
.hint strong { color:#e8e8f0; }

/* ── Logs ── */
.log-ok  { color:#4ade80; font-family:'DM Mono',monospace; font-size:0.76rem; }
.log-err { color:#ff6584; font-family:'DM Mono',monospace; font-size:0.76rem; }
.log-info{ color:#7b5ea7; font-family:'DM Mono',monospace; font-size:0.76rem; }

/* ── Streamlit overrides ── */
.stTextInput>div>div>input,
.stTextArea>div>div>textarea {
  background:#0e0e18 !important; border:1px solid #1e1e2e !important;
  border-radius:10px !important; color:#e8e8f0 !important;
  font-family:'DM Mono',monospace !important; font-size:0.86rem !important;
}
.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus { border-color:rgba(196,113,237,0.6) !important; box-shadow:none !important; }
.stSelectbox>div>div { background:#0e0e18 !important; border-color:#1e1e2e !important; color:#e8e8f0 !important; }
label { color:#6b6b88 !important; font-family:'DM Mono',monospace !important; font-size:0.7rem !important; letter-spacing:0.08em !important; text-transform:uppercase !important; }
/* Variable chip buttons */
[data-testid="stHorizontalBlock"] .stButton>button {
  background: rgba(196,113,237,0.12) !important;
  color: #c471ed !important;
  border: 1px solid rgba(196,113,237,0.35) !important;
  border-radius: 6px !important;
  font-family: 'DM Mono', monospace !important;
  font-weight: 400 !important;
  font-size: 0.78rem !important;
  padding: 0.25rem 0.8rem !important;
  box-shadow: none !important;
  transition: all 0.15s !important;
}
[data-testid="stHorizontalBlock"] .stButton>button:hover {
  background: rgba(196,113,237,0.25) !important;
  border-color: rgba(196,113,237,0.6) !important;
  transform: none !important;
  box-shadow: none !important;
}
/* Main CTA buttons — full gradient */
div[data-testid="stVerticalBlock"] > div > div > .stButton>button,
section.main .stButton>button {
  background:linear-gradient(135deg,#c471ed,#7b5ea7,#4776e6) !important;
  color:white !important; border:none !important; border-radius:10px !important;
  font-family:'Syne',sans-serif !important; font-weight:700 !important;
  padding:0.55rem 1.4rem !important; transition:all 0.2s !important;
}
div[data-testid="stVerticalBlock"] > div > div > .stButton>button:hover {
  transform:translateY(-1px); box-shadow:0 8px 24px rgba(196,113,237,0.35) !important;
}
.stButton>button:disabled { opacity:0.35 !important; transform:none !important; }

/* var-chips : force row layout + pill style */
.var-chips + div [data-testid="stHorizontalBlock"],
.var-chips [data-testid="stHorizontalBlock"] {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  gap: 8px !important;
  flex-wrap: nowrap !important;
  width: auto !important;
}
.var-chips [data-testid="column"] {
  flex: 0 0 auto !important;
  width: auto !important;
  min-width: 0 !important;
  padding: 0 !important;
}
.var-chips [data-testid="column"] > div { width: auto !important; }
.var-chips [data-testid="column"] button {
  background: rgba(196,113,237,0.15) !important;
  color: #c471ed !important;
  border: 1px solid rgba(196,113,237,0.4) !important;
  font-family: 'DM Mono', monospace !important;
  font-size: 0.72rem !important;
  font-weight: 400 !important;
  padding: 2px 24px !important;
  height: 26px !important;
  min-height: 0 !important;
  width: auto !important;
  min-width: 0 !important;
  border-radius: 20px !important;
  box-shadow: none !important;
  white-space: nowrap !important;
  line-height: 1 !important;
}
.var-chips [data-testid="column"] button:hover {
  background: rgba(196,113,237,0.28) !important;
  transform: none !important;
  box-shadow: none !important;
}
.stFileUploader { background:#0e0e18 !important; border:2px dashed #1e1e2e !important; border-radius:12px !important; }
.stProgress>div>div { background:linear-gradient(90deg,#c471ed,#4776e6) !important; }
[data-testid="stDataFrame"] { border-radius:10px; overflow:hidden; }
</style>

<script>
function insertVar(fieldId, val) {
  const el = window.parent.document.querySelector(`[data-testid="${fieldId}"] textarea`) ||
             window.parent.document.querySelector(`[data-testid="${fieldId}"] input`);
  if (!el) return;
  const s = el.selectionStart, e = el.selectionEnd;
  el.value = el.value.slice(0,s) + val + el.value.slice(e);
  el.selectionStart = el.selectionEnd = s + val.length;
  el.dispatchEvent(new Event('input', {bubbles:true}));
  el.focus();
}
</script>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown("""
<div class="mf-header">
  <div class="mf-logo">✉</div>
  <div>
    <div class="mf-title">MailForge</div>
    <div class="mf-sub">// automatisation de campagnes email personnalisées</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Session state ──
for k, v in {"contacts":[], "prenom_col":None, "nom_col":None, "pdfs":[],
             "gmail":"", "pwd":"", "connected":False}.items():
    if k not in st.session_state: st.session_state[k] = v

# ── Helpers ──
def norm(s):
    s = s.lower().strip()
    return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn').replace(' ','.')

def resolve_addr(c, pat, pc, nc):
    return pat.lower().replace('{prenom}', norm(c.get(pc,''))).replace('{nom}', norm(c.get(nc,'')))

def resolve_txt(c, txt, pc, nc):
    return txt.replace('{prenom}', c.get(pc,'')).replace('{nom}', c.get(nc,''))

def build_msg(frm, to, subj, body, atts):
    msg = MIMEMultipart()
    msg["From"] = frm; msg["To"] = to; msg["Subject"] = subj
    msg.attach(MIMEText(body,"plain","utf-8"))
    for a in atts:
        p = MIMEBase("application","pdf"); p.set_payload(a["data"]); encoders.encode_base64(p)
        p.add_header("Content-Disposition", f'attachment; filename="{a["name"]}"'); msg.attach(p)
    return msg

def test_conn(addr, pwd):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=8) as s: s.login(addr, pwd)

def save_draft(addr, pwd, msg):
    with imaplib.IMAP4_SSL("imap.gmail.com") as M:
        M.login(addr, pwd)
        for f in ['[Gmail]/Drafts','[Gmail]/Brouillons','Drafts','Brouillons']:
            try:
                if M.append(f, '\\Draft', None, msg.as_bytes())[0] == 'OK': return
            except: continue
        raise Exception("Dossier Brouillons introuvable")


# ════════════════════════════════════════════════
# 01 — CSV
# ════════════════════════════════════════════════
st.markdown('<div class="card card-accent"><div class="card-label">Étape 01</div><div class="card-title">📋 Importer les contacts</div>', unsafe_allow_html=True)

csv_file = st.file_uploader("Fichier CSV", type=["csv"], label_visibility="collapsed")
if csv_file:
    try:
        try:
            df = pd.read_csv(csv_file, sep=';', encoding='utf-8')
            if len(df.columns)==1: csv_file.seek(0); df = pd.read_csv(csv_file, sep=',', encoding='utf-8')
        except:
            csv_file.seek(0); df = pd.read_csv(csv_file, sep=',', encoding='latin-1')
        df.columns = df.columns.str.strip()
        st.session_state.contacts = df.to_dict('records')
        cols  = list(df.columns)
        lower = [c.lower() for c in cols]
        dp = next((cols[i] for i,c in enumerate(lower) if 'prenom' in c or 'prénom' in c or 'first' in c), cols[0])
        dn = next((cols[i] for i,c in enumerate(lower) if c=='nom' or 'last' in c), cols[min(1,len(cols)-1)])
        st.markdown(f'<div class="badge-ok" style="margin:10px 0 16px">✓ {len(st.session_state.contacts)} contacts chargés</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: st.session_state.prenom_col = st.selectbox("Colonne → Prénom", cols, index=cols.index(dp))
        with c2: st.session_state.nom_col    = st.selectbox("Colonne → Nom",    cols, index=cols.index(dn))
        st.dataframe(df[[st.session_state.prenom_col, st.session_state.nom_col]].head(5), use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Erreur CSV : {e}")

st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════
# 02 — Pattern email
# ════════════════════════════════════════════════
st.markdown('<div class="card"><div class="card-label">Étape 02</div><div class="card-title">📧 Format de l\'adresse email</div>', unsafe_allow_html=True)

if "ep" not in st.session_state: st.session_state.ep = ""
if "ep_inject" not in st.session_state: st.session_state.ep_inject = ""
if st.session_state.ep_inject:
    st.session_state.ep += st.session_state.ep_inject
    st.session_state.ep_inject = ""

st.markdown('<div class="var-chips">', unsafe_allow_html=True)
c1, c2, _ = st.columns([2,2,6])
with c1: st.button("{prenom}", key="ep_p", on_click=lambda: st.session_state.update(ep_inject="{prenom}"))
with c2: st.button("{nom}",    key="ep_n", on_click=lambda: st.session_state.update(ep_inject="{nom}"))
st.markdown('</div>', unsafe_allow_html=True)

email_pattern = st.text_input("Format", key="ep", placeholder="{prenom}.{nom}@natixis.com", label_visibility="collapsed")

if email_pattern and st.session_state.contacts and st.session_state.prenom_col:
    ex = resolve_addr(st.session_state.contacts[0], email_pattern, st.session_state.prenom_col, st.session_state.nom_col)
    st.markdown(f'<div class="example-line">→ <span>{ex}</span></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════
# 03 — Contenu
# ════════════════════════════════════════════════
st.markdown('<div class="card"><div class="card-label">Étape 03</div><div class="card-title">✍️ Contenu du mail</div>', unsafe_allow_html=True)

st.markdown('<p style="font-family:DM Mono,monospace;font-size:0.7rem;color:#6b6b88;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:4px">Objet</p>', unsafe_allow_html=True)
mail_subject = st.text_input("Objet", key="ms", placeholder="ex: Candidature — Développeur Full Stack", label_visibility="collapsed")

st.markdown('<p style="font-family:DM Mono,monospace;font-size:0.7rem;color:#6b6b88;letter-spacing:0.08em;text-transform:uppercase;margin:12px 0 4px">Corps</p>', unsafe_allow_html=True)

if "mb" not in st.session_state: st.session_state.mb = ""
if "mb_inject" not in st.session_state: st.session_state.mb_inject = ""
if st.session_state.mb_inject:
    st.session_state.mb += st.session_state.mb_inject
    st.session_state.mb_inject = ""

st.markdown('<div class="var-chips">', unsafe_allow_html=True)
c1, c2, _ = st.columns([2,2,6])
with c1: st.button("{prenom}", key="mb_p", on_click=lambda: st.session_state.update(mb_inject="{prenom}"))
with c2: st.button("{nom}",    key="mb_n", on_click=lambda: st.session_state.update(mb_inject="{nom}"))
st.markdown('</div>', unsafe_allow_html=True)

mail_body = st.text_area("Corps", key="mb", placeholder="Bonjour {prenom} {nom},\n\nJe me permets de vous contacter...\n\nCordialement,", height=200, label_visibility="collapsed")

st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════
# 04 — PDF
# ════════════════════════════════════════════════
st.markdown('<div class="card"><div class="card-label">Étape 04</div><div class="card-title">📎 Pièces jointes</div>', unsafe_allow_html=True)

pdfs = st.file_uploader("PDF (CV, lettre…)", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed")
if pdfs:
    st.session_state.pdfs = [{"name": f.name, "data": f.read()} for f in pdfs]
    for a in st.session_state.pdfs:
        st.markdown(f'<div class="badge-ok" style="margin-bottom:6px">📄 {a["name"]} — {len(a["data"])//1024} KB</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════
# 05 — Preview
# ════════════════════════════════════════════════
st.markdown('<div class="card"><div class="card-label">Étape 05</div><div class="card-title">🔍 Prévisualisation</div>', unsafe_allow_html=True)

if st.button("Générer la prévisualisation"):
    if not st.session_state.contacts: st.warning("Importe d'abord un CSV.")
    elif not email_pattern: st.warning("Remplis le pattern d'adresse.")
    else:
        for c in st.session_state.contacts[:5]:
            to   = resolve_addr(c, email_pattern, st.session_state.prenom_col, st.session_state.nom_col)
            subj = resolve_txt(c, mail_subject, st.session_state.prenom_col, st.session_state.nom_col)
            body = resolve_txt(c, mail_body,    st.session_state.prenom_col, st.session_state.nom_col)
            st.markdown(f'<div class="prev-card"><div class="prev-to">À → {to}</div><div class="prev-subj">{subj or "(objet vide)"}</div><div class="prev-body">{body or "(corps vide)"}</div></div>', unsafe_allow_html=True)
        if len(st.session_state.contacts) > 5:
            st.markdown(f'<p style="font-family:DM Mono,monospace;font-size:0.74rem;color:#6b6b88;text-align:center;margin-top:4px">+ {len(st.session_state.contacts)-5} autres…</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════
# 06 — Connexion Gmail
# ════════════════════════════════════════════════
st.markdown('<div class="card card-accent"><div class="card-label">Étape 06</div><div class="card-title">📬 Connexion Gmail</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hint">
  Utilise un <strong>mot de passe d'application Gmail</strong> — pas ton vrai mot de passe.<br>
  <strong>1.</strong> <a href="https://myaccount.google.com/security" target="_blank">myaccount.google.com/security</a> → active la validation en 2 étapes<br>
  <strong>2.</strong> Cherche <strong>"Mots de passe des applications"</strong> → crée-en un → copie le code à 16 caractères
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1: gmail_in = st.text_input("Adresse Gmail", placeholder="toi@gmail.com", value=st.session_state.gmail)
with c2: pwd_in   = st.text_input("Mot de passe d'app", placeholder="xxxx xxxx xxxx xxxx", type="password", value=st.session_state.pwd)

if gmail_in: st.session_state.gmail = gmail_in
if pwd_in:   st.session_state.pwd   = pwd_in

if st.session_state.gmail and st.session_state.pwd and not st.session_state.connected:
    if st.button("🔌 Tester la connexion"):
        try:
            test_conn(st.session_state.gmail, st.session_state.pwd.replace(" ",""))
            st.session_state.connected = True
            st.rerun()
        except Exception as e:
            st.error(f"Connexion échouée : {e}")

if st.session_state.connected:
    st.markdown(f'<div class="badge-ok" style="margin-top:10px">✓ Connecté : {st.session_state.gmail}</div>', unsafe_allow_html=True)
    if st.button("🔓 Déconnecter"):
        st.session_state.connected = False; st.session_state.pwd = ""; st.rerun()

st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════
# 07 — Envoi
# ════════════════════════════════════════════════
st.markdown('<div class="card"><div class="card-label">Étape 07</div><div class="card-title">🚀 Créer les brouillons</div>', unsafe_allow_html=True)

ready = st.session_state.contacts and email_pattern and mail_body and st.session_state.connected
if not ready:
    missing = [x for x, ok in [("CSV", st.session_state.contacts), ("Pattern email", email_pattern), ("Corps du mail", mail_body), ("Connexion Gmail", st.session_state.connected)] if not ok]
    st.markdown(f'<div class="badge-warn">⚠ En attente : {" · ".join(missing)}</div>', unsafe_allow_html=True)

n = len(st.session_state.contacts)
if st.button(f"✉ Créer {n} brouillon{'s' if n>1 else ''} dans Gmail", disabled=not ready):
    prog = st.progress(0); status = st.empty(); logs = st.empty()
    lines = []; ok = 0; err = 0
    pwd = st.session_state.pwd.replace(" ","")
    for i, c in enumerate(st.session_state.contacts):
        to   = resolve_addr(c, email_pattern, st.session_state.prenom_col, st.session_state.nom_col)
        subj = resolve_txt(c, mail_subject, st.session_state.prenom_col, st.session_state.nom_col)
        body = resolve_txt(c, mail_body,    st.session_state.prenom_col, st.session_state.nom_col)
        try:
            save_draft(st.session_state.gmail, pwd, build_msg(st.session_state.gmail, to, subj, body, st.session_state.pdfs))
            ok += 1; lines.append(f'<div class="log-ok">✓ {to}</div>')
        except Exception as e:
            err += 1; lines.append(f'<div class="log-err">✗ {to} — {e}</div>')
        prog.progress((i+1)/len(st.session_state.contacts))
        status.markdown(f'<div class="log-info">{i+1}/{len(st.session_state.contacts)}</div>', unsafe_allow_html=True)
        logs.markdown('\n'.join(lines[-8:]), unsafe_allow_html=True)
    status.empty()
    if err == 0: st.success(f"✅ {ok} brouillons créés dans Gmail !")
    else: st.warning(f"✅ {ok} créés · ⚠️ {err} erreur(s)")
    logs.markdown('\n'.join(lines), unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
