import streamlit as st
import pandas as pd
import unicodedata
import smtplib
import imaplib
import email as email_lib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# ─── Config page ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MailForge",
    page_icon="✉️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.stApp { background: #0a0a0f; color: #e8e8f0; }
.main .block-container { max-width: 860px; padding: 2rem 2rem 4rem; }
h1, h2, h3 { font-family: 'Syne', sans-serif !important; letter-spacing: -0.03em; }
header[data-testid="stHeader"] { display: none !important; }
.stAppHeader { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

.mailforge-header { display: flex; align-items: center; gap: 16px; margin-bottom: 40px; }
.logo { width: 52px; height: 52px; border-radius: 12px; background: linear-gradient(135deg, #6c63ff, #ff6584); display: flex; align-items: center; justify-content: center; font-size: 26px; flex-shrink: 0; }
.header-text h1 { font-size: 2.6rem; font-weight: 800; line-height: 1; margin: 0; background: linear-gradient(90deg, #6c63ff, #ff6584); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.header-text p { font-family: 'DM Mono', monospace; font-size: 0.75rem; color: #6b6b88; margin: 6px 0 0; letter-spacing: 0.05em; }

.step-card { background: #12121a; border: 1px solid #2a2a3d; border-radius: 16px; padding: 24px 28px; margin-bottom: 20px; }
.step-card.highlighted { border-color: #6c63ff; }
.step-label { font-family: 'DM Mono', monospace; font-size: 0.68rem; color: #6c63ff; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 4px; }
.step-title { font-size: 1rem; font-weight: 700; margin-bottom: 16px; color: #e8e8f0; }

.badge-success { display: inline-flex; align-items: center; gap: 6px; background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.3); color: #4ade80; border-radius: 6px; padding: 4px 12px; font-family: 'DM Mono', monospace; font-size: 0.75rem; }
.badge-warn { display: inline-flex; align-items: center; gap: 6px; background: rgba(250,204,21,0.1); border: 1px solid rgba(250,204,21,0.3); color: #facc15; border-radius: 6px; padding: 4px 12px; font-family: 'DM Mono', monospace; font-size: 0.75rem; }

.preview-card { background: #1a1a26; border: 1px solid #2a2a3d; border-radius: 10px; padding: 14px 18px; margin-bottom: 10px; }
.preview-to { font-family: 'DM Mono', monospace; font-size: 0.72rem; color: #6c63ff; margin-bottom: 4px; }
.preview-subject { font-size: 0.88rem; font-weight: 600; margin-bottom: 6px; }
.preview-body { font-family: 'DM Mono', monospace; font-size: 0.75rem; color: #6b6b88; border-top: 1px solid #2a2a3d; padding-top: 8px; white-space: pre-wrap; line-height: 1.6; }

.hint-box { background: #1a1a26; border: 1px solid #2a2a3d; border-radius: 8px; padding: 12px 16px; font-family: 'DM Mono', monospace; font-size: 0.75rem; color: #6b6b88; margin-top: 8px; line-height: 1.7; }
.hint-box a { color: #6c63ff; }
.hint-box code { background: rgba(108,99,255,0.15); color: #a09dff; padding: 2px 6px; border-radius: 4px; font-size: 0.72rem; }

.log-line-ok  { color: #4ade80; font-family: 'DM Mono', monospace; font-size: 0.78rem; }
.log-line-err { color: #ff6584; font-family: 'DM Mono', monospace; font-size: 0.78rem; }
.log-line-info{ color: #6c63ff; font-family: 'DM Mono', monospace; font-size: 0.78rem; }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #1a1a26 !important; border: 1px solid #2a2a3d !important;
    border-radius: 10px !important; color: #e8e8f0 !important;
    font-family: 'DM Mono', monospace !important; font-size: 0.88rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus { border-color: #6c63ff !important; box-shadow: none !important; }
.stSelectbox > div > div { background: #1a1a26 !important; border-color: #2a2a3d !important; color: #e8e8f0 !important; }
label { color: #6b6b88 !important; font-family: 'DM Mono', monospace !important; font-size: 0.72rem !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; }
.stButton > button { background: linear-gradient(135deg, #6c63ff, #9b59f5) !important; color: white !important; border: none !important; border-radius: 10px !important; font-family: 'Syne', sans-serif !important; font-weight: 700 !important; padding: 0.6rem 1.4rem !important; }
.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(108,99,255,0.4) !important; }
.stFileUploader { background: #1a1a26 !important; border: 2px dashed #2a2a3d !important; border-radius: 12px !important; }
.stProgress > div > div { background: linear-gradient(90deg, #6c63ff, #ff6584) !important; }
</style>
""", unsafe_allow_html=True)

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="mailforge-header">
  <div class="logo">✉</div>
  <div class="header-text">
    <h1>MailForge</h1>
    <p>// automatisation de campagnes email personnalisées</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Helpers ───────────────────────────────────────────────────────────────────
def normalize(s):
    s = s.lower().strip()
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return s.replace(' ', '.')

def resolve_email(contact, pattern, prenom_col, nom_col):
    prenom = normalize(contact.get(prenom_col, ''))
    nom    = normalize(contact.get(nom_col, ''))
    return pattern.lower().replace('{prenom}', prenom).replace('{nom}', nom)

def resolve_text(contact, text, prenom_col, nom_col):
    prenom = contact.get(prenom_col, '')
    nom    = contact.get(nom_col, '')
    return text.replace('{prenom}', prenom).replace('{nom}', nom)

def build_email(from_addr, to, subject, body, attachments):
    msg = MIMEMultipart()
    msg["From"]    = from_addr
    msg["To"]      = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))
    for att in attachments:
        part = MIMEBase("application", "pdf")
        part.set_payload(att["data"])
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{att["name"]}"')
        msg.attach(part)
    return msg

def test_gmail_connection(gmail_addr, app_password):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=8) as s:
        s.login(gmail_addr, app_password)
    return True

def save_draft_imap(gmail_addr, app_password, msg):
    """Save email as draft via IMAP."""
    with imaplib.IMAP4_SSL("imap.gmail.com") as M:
        M.login(gmail_addr, app_password)
        raw = msg.as_bytes()
        # Append to [Gmail]/Drafts folder
        for folder in ['[Gmail]/Drafts', '[Gmail]/Brouillons', 'Drafts', 'Brouillons']:
            try:
                result = M.append(folder, '\\Draft', None, raw)
                if result[0] == 'OK':
                    return True
            except:
                continue
        raise Exception("Dossier Brouillons introuvable")

# ─── Session state ─────────────────────────────────────────────────────────────
for k, v in {
    "contacts": [], "prenom_col": None, "nom_col": None,
    "pdf_attachments": [],
    "gmail_addr": "", "app_password": "", "gmail_connected": False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════════════
# ÉTAPE 1 — CSV
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="step-card highlighted">', unsafe_allow_html=True)
st.markdown('<div class="step-label">Étape 01</div><div class="step-title">📋 Importer les contacts (CSV)</div>', unsafe_allow_html=True)

csv_file = st.file_uploader("Fichier CSV (colonnes : nom, prenom ou similaire)", type=["csv"])

if csv_file:
    try:
        try:
            df = pd.read_csv(csv_file, sep=';', encoding='utf-8')
            if len(df.columns) == 1:
                csv_file.seek(0)
                df = pd.read_csv(csv_file, sep=',', encoding='utf-8')
        except:
            csv_file.seek(0)
            df = pd.read_csv(csv_file, sep=',', encoding='latin-1')

        df.columns = df.columns.str.strip()
        st.session_state.contacts = df.to_dict('records')
        cols  = list(df.columns)
        lower = [c.lower() for c in cols]

        default_prenom = next((cols[i] for i, c in enumerate(lower) if 'prenom' in c or 'prénom' in c or 'first' in c), cols[0])
        default_nom    = next((cols[i] for i, c in enumerate(lower) if c == 'nom' or 'last' in c), cols[min(1, len(cols)-1)])

        st.markdown(f'<div class="badge-success">✓ {len(st.session_state.contacts)} contacts chargés</div>', unsafe_allow_html=True)
        st.write("")

        col1, col2 = st.columns(2)
        with col1:
            st.session_state.prenom_col = st.selectbox("Colonne → Prénom", cols, index=cols.index(default_prenom))
        with col2:
            st.session_state.nom_col = st.selectbox("Colonne → Nom", cols, index=cols.index(default_nom))

        st.dataframe(df.head(5), use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Erreur lecture CSV : {e}")

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ÉTAPE 2 — Pattern email
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="step-card">', unsafe_allow_html=True)
st.markdown('<div class="step-label">Étape 02</div><div class="step-title">📧 Structure de l\'adresse email</div>', unsafe_allow_html=True)

st.markdown('<div class="hint-box">Utilise <code>{prenom}</code> et <code>{nom}</code> comme variables</div>', unsafe_allow_html=True)
st.write("")

email_pattern = st.text_input("Format de l'adresse", placeholder="{prenom}.{nom}@natixis.com")

if email_pattern and st.session_state.contacts and st.session_state.prenom_col:
    sample  = st.session_state.contacts[0]
    example = resolve_email(sample, email_pattern, st.session_state.prenom_col, st.session_state.nom_col)
    st.markdown(f'<div class="hint-box">→ Exemple généré : <code>{example}</code></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ÉTAPE 3 — Contenu
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="step-card">', unsafe_allow_html=True)
st.markdown('<div class="step-label">Étape 03</div><div class="step-title">✍️ Contenu du mail</div>', unsafe_allow_html=True)

st.markdown('<div class="hint-box">💡 Utilise <code>{prenom}</code> et <code>{nom}</code> dans ton texte — remplacés automatiquement pour chaque contact</div>', unsafe_allow_html=True)
st.write("")

mail_subject = st.text_input("Objet du mail", placeholder="ex: Candidature — Développeur Full Stack")
mail_body    = st.text_area("Corps du mail", placeholder="Bonjour {prenom} {nom},\n\nJe me permets de vous contacter...\n\nCordialement,", height=200)

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ÉTAPE 4 — Pièces jointes
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="step-card">', unsafe_allow_html=True)
st.markdown('<div class="step-label">Étape 04</div><div class="step-title">📎 Pièces jointes (PDF)</div>', unsafe_allow_html=True)

pdf_files = st.file_uploader("Ajouter des PDF (CV, lettre de motivation…)", type=["pdf"], accept_multiple_files=True)
if pdf_files:
    st.session_state.pdf_attachments = []
    for f in pdf_files:
        data = f.read()
        st.session_state.pdf_attachments.append({"name": f.name, "data": data})
        st.markdown(f'<div class="badge-success" style="margin-bottom:6px">📄 {f.name} — {len(data)//1024} KB</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ÉTAPE 5 — Prévisualisation
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="step-card">', unsafe_allow_html=True)
st.markdown('<div class="step-label">Étape 05</div><div class="step-title">🔍 Prévisualisation</div>', unsafe_allow_html=True)

if st.button("Générer la prévisualisation"):
    if not st.session_state.contacts:
        st.warning("Importe d'abord un CSV.")
    elif not email_pattern:
        st.warning("Remplis le pattern d'adresse email.")
    else:
        for c in st.session_state.contacts[:5]:
            to   = resolve_email(c, email_pattern, st.session_state.prenom_col, st.session_state.nom_col)
            subj = resolve_text(c, mail_subject, st.session_state.prenom_col, st.session_state.nom_col)
            body = resolve_text(c, mail_body,    st.session_state.prenom_col, st.session_state.nom_col)
            st.markdown(f"""
            <div class="preview-card">
              <div class="preview-to">À → {to}</div>
              <div class="preview-subject">{subj or "(objet vide)"}</div>
              <div class="preview-body">{body or "(corps vide)"}</div>
            </div>""", unsafe_allow_html=True)
        if len(st.session_state.contacts) > 5:
            st.markdown(f'<div style="font-family:DM Mono,monospace;font-size:0.75rem;color:#6b6b88;text-align:center;padding:8px">+ {len(st.session_state.contacts)-5} autres emails…</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ÉTAPE 6 — Connexion Gmail (App Password)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="step-card highlighted">', unsafe_allow_html=True)
st.markdown('<div class="step-label">Étape 06</div><div class="step-title">📬 Connexion Gmail</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hint-box">
  Utilise un <strong style="color:#e8e8f0">mot de passe d'application Gmail</strong> — plus simple que OAuth, aucune config Google Cloud nécessaire.<br><br>
  <strong style="color:#e8e8f0">Comment obtenir ton mot de passe d'application :</strong><br>
  1. Va sur <a href="https://myaccount.google.com/security" target="_blank">myaccount.google.com/security</a><br>
  2. Active la <strong style="color:#e8e8f0">validation en 2 étapes</strong> si ce n'est pas fait<br>
  3. Cherche <strong style="color:#e8e8f0">"Mots de passe des applications"</strong> → crée un mot de passe pour <code>Mail</code><br>
  4. Google te donne un code à 16 caractères → colle-le ci-dessous
</div>
""", unsafe_allow_html=True)
st.write("")

col1, col2 = st.columns(2)
with col1:
    gmail_input = st.text_input("Adresse Gmail", placeholder="tonemail@gmail.com", value=st.session_state.gmail_addr)
with col2:
    password_input = st.text_input("Mot de passe d'application", placeholder="xxxx xxxx xxxx xxxx", type="password", value=st.session_state.app_password)

if gmail_input:  st.session_state.gmail_addr    = gmail_input
if password_input: st.session_state.app_password = password_input

if st.session_state.gmail_addr and st.session_state.app_password:
    if not st.session_state.gmail_connected:
        if st.button("🔌 Tester la connexion"):
            try:
                test_gmail_connection(st.session_state.gmail_addr, st.session_state.app_password.replace(" ", ""))
                st.session_state.gmail_connected = True
                st.rerun()
            except Exception as e:
                st.error(f"Connexion échouée : {e}")

if st.session_state.gmail_connected:
    st.markdown(f'<div class="badge-success" style="margin-top:8px">✓ Connecté : {st.session_state.gmail_addr}</div>', unsafe_allow_html=True)
    if st.button("🔓 Se déconnecter"):
        st.session_state.gmail_connected = False
        st.session_state.app_password    = ""
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ÉTAPE 7 — Créer les brouillons
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="step-card">', unsafe_allow_html=True)
st.markdown('<div class="step-label">Étape 07</div><div class="step-title">🚀 Créer les brouillons Gmail</div>', unsafe_allow_html=True)

ready = (
    st.session_state.contacts and
    email_pattern and
    mail_body and
    st.session_state.gmail_connected
)

if not ready:
    missing = []
    if not st.session_state.contacts:       missing.append("CSV")
    if not email_pattern:                   missing.append("Pattern email")
    if not mail_body:                       missing.append("Corps du mail")
    if not st.session_state.gmail_connected: missing.append("Connexion Gmail")
    st.markdown(f'<div class="badge-warn">⚠ En attente : {" · ".join(missing)}</div>', unsafe_allow_html=True)

if st.button(f"✉ Créer {len(st.session_state.contacts)} brouillon(s) dans Gmail", disabled=not ready):
    progress  = st.progress(0)
    status    = st.empty()
    logs      = st.empty()
    log_lines = []
    ok_count  = 0
    err_count = 0

    clean_password = st.session_state.app_password.replace(" ", "")

    for i, contact in enumerate(st.session_state.contacts):
        to      = resolve_email(contact, email_pattern, st.session_state.prenom_col, st.session_state.nom_col)
        subject = resolve_text(contact, mail_subject, st.session_state.prenom_col, st.session_state.nom_col)
        body    = resolve_text(contact, mail_body,    st.session_state.prenom_col, st.session_state.nom_col)

        try:
            msg = build_email(st.session_state.gmail_addr, to, subject, body, st.session_state.pdf_attachments)
            save_draft_imap(st.session_state.gmail_addr, clean_password, msg)
            ok_count += 1
            log_lines.append(f'<div class="log-line-ok">✓ Brouillon créé → {to}</div>')
        except Exception as e:
            err_count += 1
            log_lines.append(f'<div class="log-line-err">✗ {to} : {e}</div>')

        progress.progress((i + 1) / len(st.session_state.contacts))
        status.markdown(f'<div class="log-line-info">{i+1} / {len(st.session_state.contacts)} traités…</div>', unsafe_allow_html=True)
        logs.markdown('\n'.join(log_lines[-10:]), unsafe_allow_html=True)

    status.empty()
    if err_count == 0:
        st.success(f"✅ {ok_count} brouillons créés avec succès dans Gmail !")
    else:
        st.warning(f"✅ {ok_count} brouillons créés · ⚠️ {err_count} erreur(s)")
    logs.markdown('\n'.join(log_lines), unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
