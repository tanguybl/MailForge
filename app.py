import streamlit as st
import pandas as pd
import base64
import json
import urllib.request
import urllib.parse
import urllib.error
import unicodedata
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import io

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

.mailforge-header {
    display: flex; align-items: center; gap: 16px; margin-bottom: 40px;
}
.logo { 
    width: 52px; height: 52px; border-radius: 12px;
    background: linear-gradient(135deg, #6c63ff, #ff6584);
    display: flex; align-items: center; justify-content: center;
    font-size: 26px; flex-shrink: 0;
}
.header-text h1 { 
    font-size: 2.6rem; font-weight: 800; line-height: 1; margin: 0;
    background: linear-gradient(90deg, #6c63ff, #ff6584);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.header-text p { 
    font-family: 'DM Mono', monospace; font-size: 0.75rem; 
    color: #6b6b88; margin: 6px 0 0; letter-spacing: 0.05em;
}

.step-card {
    background: #12121a; border: 1px solid #2a2a3d; border-radius: 16px;
    padding: 24px 28px; margin-bottom: 20px;
}
.step-card.highlighted { border-color: #6c63ff; }

.step-label {
    font-family: 'DM Mono', monospace; font-size: 0.68rem; 
    color: #6c63ff; letter-spacing: 0.1em; text-transform: uppercase; 
    margin-bottom: 4px;
}
.step-title { font-size: 1rem; font-weight: 700; margin-bottom: 16px; color: #e8e8f0; }

.badge-success {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.3);
    color: #4ade80; border-radius: 6px; padding: 4px 12px;
    font-family: 'DM Mono', monospace; font-size: 0.75rem;
}
.badge-warn {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(250,204,21,0.1); border: 1px solid rgba(250,204,21,0.3);
    color: #facc15; border-radius: 6px; padding: 4px 12px;
    font-family: 'DM Mono', monospace; font-size: 0.75rem;
}
.badge-err {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(255,101,132,0.1); border: 1px solid rgba(255,101,132,0.3);
    color: #ff6584; border-radius: 6px; padding: 4px 12px;
    font-family: 'DM Mono', monospace; font-size: 0.75rem;
}

.preview-card {
    background: #1a1a26; border: 1px solid #2a2a3d; border-radius: 10px;
    padding: 14px 18px; margin-bottom: 10px;
}
.preview-to { font-family: 'DM Mono', monospace; font-size: 0.72rem; color: #6c63ff; margin-bottom: 4px; }
.preview-subject { font-size: 0.88rem; font-weight: 600; margin-bottom: 6px; }
.preview-body { 
    font-family: 'DM Mono', monospace; font-size: 0.75rem; color: #6b6b88; 
    border-top: 1px solid #2a2a3d; padding-top: 8px; white-space: pre-wrap; line-height: 1.6;
}

.hint-box {
    background: #1a1a26; border: 1px solid #2a2a3d; border-radius: 8px;
    padding: 12px 16px; font-family: 'DM Mono', monospace; font-size: 0.75rem;
    color: #6b6b88; margin-top: 8px; line-height: 1.7;
}
.hint-box a { color: #6c63ff; }
.hint-box code { 
    background: rgba(108,99,255,0.15); color: #a09dff; 
    padding: 2px 6px; border-radius: 4px; font-size: 0.72rem;
}

.log-line-ok  { color: #4ade80; font-family: 'DM Mono', monospace; font-size: 0.78rem; }
.log-line-err { color: #ff6584; font-family: 'DM Mono', monospace; font-size: 0.78rem; }
.log-line-info{ color: #6c63ff; font-family: 'DM Mono', monospace; font-size: 0.78rem; }

/* Streamlit overrides */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #1a1a26 !important; border: 1px solid #2a2a3d !important;
    border-radius: 10px !important; color: #e8e8f0 !important;
    font-family: 'DM Mono', monospace !important; font-size: 0.88rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6c63ff !important; box-shadow: none !important;
}
.stSelectbox > div > div { 
    background: #1a1a26 !important; border-color: #2a2a3d !important; color: #e8e8f0 !important;
}
label { color: #6b6b88 !important; font-family: 'DM Mono', monospace !important; font-size: 0.72rem !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; }
.stButton > button {
    background: linear-gradient(135deg, #6c63ff, #9b59f5) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
    padding: 0.6rem 1.4rem !important; transition: all 0.2s !important;
}
.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(108,99,255,0.4) !important; }
.stFileUploader { background: #1a1a26 !important; border: 2px dashed #2a2a3d !important; border-radius: 12px !important; }
.stProgress > div > div { background: linear-gradient(90deg, #6c63ff, #ff6584) !important; }
div[data-testid="stExpander"] { background: #12121a !important; border: 1px solid #2a2a3d !important; border-radius: 12px !important; }
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

def build_raw_email(to, subject, body, attachments):
    msg = MIMEMultipart()
    msg["To"]      = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))
    for att in attachments:
        part = MIMEBase("application", "pdf")
        part.set_payload(att["data"])
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{att["name"]}"')
        msg.attach(part)
    return base64.urlsafe_b64encode(msg.as_bytes()).decode()

def create_gmail_draft(access_token, raw):
    body = json.dumps({"message": {"raw": raw}}).encode()
    req  = urllib.request.Request(
        "https://gmail.googleapis.com/gmail/v1/users/me/drafts",
        data=body,
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def get_new_access_token(client_id, client_secret, refresh_token):
    data = urllib.parse.urlencode({
        "client_id":     client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type":    "refresh_token",
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, method="POST")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["access_token"]

def exchange_code(client_id, client_secret, code, redirect_uri):
    data = urllib.parse.urlencode({
        "code":          code,
        "client_id":     client_id,
        "client_secret": client_secret,
        "redirect_uri":  redirect_uri,
        "grant_type":    "authorization_code",
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, method="POST")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def get_user_email(access_token):
    req = urllib.request.Request(
        "https://www.googleapis.com/gmail/v1/users/me/profile",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["emailAddress"]


# ─── Session state init ────────────────────────────────────────────────────────
for k, v in {
    "contacts": [], "prenom_col": None, "nom_col": None,
    "pdf_attachments": [],
    "access_token": None, "refresh_token": None, "gmail_email": None,
    "client_id": "", "client_secret": "",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════════════
# ÉTAPE 1 — CSV
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="step-card highlighted">', unsafe_allow_html=True)
st.markdown('<div class="step-label">Étape 01</div><div class="step-title">📋 Importer les contacts (CSV)</div>', unsafe_allow_html=True)

csv_file = st.file_uploader("Fichier CSV (colonnes : nom, prenom ou similaire)", type=["csv"], key="csv_upload")

if csv_file:
    try:
        # Try different separators
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

        st.markdown(f'<div class="badge-success">✓ {len(st.session_state.contacts)} contacts chargés</div>', unsafe_allow_html=True)
        st.write("")

        cols = list(df.columns)
        lower = [c.lower() for c in cols]

        # Auto-detect
        default_prenom = next((cols[i] for i, c in enumerate(lower) if 'prenom' in c or 'prénom' in c or 'first' in c), cols[0])
        default_nom    = next((cols[i] for i, c in enumerate(lower) if c == 'nom' or 'last' in c), cols[min(1, len(cols)-1)])

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

email_pattern = st.text_input("Format de l'adresse", placeholder="{prenom}.{nom}@natixis.com", help="Utilise {prenom} et {nom} comme variables")

if email_pattern and st.session_state.contacts and st.session_state.prenom_col:
    sample = st.session_state.contacts[0]
    example = resolve_email(sample, email_pattern, st.session_state.prenom_col, st.session_state.nom_col)
    st.markdown(f'<div class="hint-box">→ Exemple : <code>{example}</code></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ÉTAPE 3 — Contenu du mail
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="step-card">', unsafe_allow_html=True)
st.markdown('<div class="step-label">Étape 03</div><div class="step-title">✍️ Contenu du mail</div>', unsafe_allow_html=True)

st.markdown('<div class="hint-box">Variables disponibles : <code>{prenom}</code> &nbsp; <code>{nom}</code></div>', unsafe_allow_html=True)
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
# ÉTAPE 6 — Connexion Gmail
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="step-card highlighted">', unsafe_allow_html=True)
st.markdown('<div class="step-label">Étape 06</div><div class="step-title">📬 Connexion Gmail (OAuth)</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hint-box">
  Renseigne tes credentials Google Cloud. Ils ne sont <strong style="color:#e8e8f0">jamais stockés</strong> — utilisés uniquement pour cette session.<br><br>
  Tu n'as pas encore de credentials ? → <a href="https://console.cloud.google.com/apis/credentials" target="_blank">Google Cloud Console</a><br>
  <code>APIs & Services</code> → <code>Identifiants</code> → <code>Créer un ID client OAuth</code> → <code>Application Web</code><br>
  URI de redirection : <code>urn:ietf:wg:oauth:2.0:oob</code>
</div>
""", unsafe_allow_html=True)
st.write("")

col1, col2 = st.columns(2)
with col1:
    client_id = st.text_input("Client ID", value=st.session_state.client_id, placeholder="934056...apps.googleusercontent.com", type="password")
with col2:
    client_secret = st.text_input("Client Secret", value=st.session_state.client_secret, placeholder="GOCSPX-...", type="password")

if client_id: st.session_state.client_id = client_id
if client_secret: st.session_state.client_secret = client_secret

# Auth flow
if client_id and client_secret:
    REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
    params = {
        "client_id":     client_id,
        "redirect_uri":  REDIRECT_URI,
        "response_type": "code",
        "scope":         "https://mail.google.com/",
        "access_type":   "offline",
        "prompt":        "consent",
    }
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)

    if not st.session_state.access_token:
        st.markdown(f"""
        <div class="hint-box" style="margin-top:12px">
          <strong style="color:#e8e8f0">1.</strong> Clique sur ce lien pour autoriser l'accès Gmail :<br>
          <a href="{auth_url}" target="_blank">🔗 Ouvrir la page d'autorisation Google</a><br><br>
          <strong style="color:#e8e8f0">2.</strong> Connecte-toi, accepte, puis <strong style="color:#e8e8f0">copie le code</strong> affiché par Google<br>
          <strong style="color:#e8e8f0">3.</strong> Colle-le ci-dessous
        </div>
        """, unsafe_allow_html=True)
        st.write("")

        auth_code = st.text_input("Code d'autorisation Google", placeholder="4/0AX4XfWh...")
        if st.button("✅ Valider le code") and auth_code:
            try:
                tokens = exchange_code(client_id, client_secret, auth_code.strip(), REDIRECT_URI)
                st.session_state.access_token  = tokens["access_token"]
                st.session_state.refresh_token = tokens.get("refresh_token")
                st.session_state.gmail_email   = get_user_email(tokens["access_token"])
                st.success(f"✓ Connecté : {st.session_state.gmail_email}")
                st.rerun()
            except Exception as e:
                st.error(f"Erreur d'authentification : {e}")
    else:
        st.markdown(f'<div class="badge-success" style="margin-top:8px">✓ Connecté : {st.session_state.gmail_email}</div>', unsafe_allow_html=True)
        if st.button("🔓 Se déconnecter"):
            st.session_state.access_token = None
            st.session_state.refresh_token = None
            st.session_state.gmail_email = None
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ÉTAPE 7 — Envoi
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="step-card">', unsafe_allow_html=True)
st.markdown('<div class="step-label">Étape 07</div><div class="step-title">🚀 Créer les brouillons Gmail</div>', unsafe_allow_html=True)

ready = (
    st.session_state.contacts and
    email_pattern and
    mail_body and
    st.session_state.access_token
)

if not ready:
    missing = []
    if not st.session_state.contacts: missing.append("CSV")
    if not email_pattern: missing.append("Pattern email")
    if not mail_body: missing.append("Corps du mail")
    if not st.session_state.access_token: missing.append("Connexion Gmail")
    st.markdown(f'<div class="badge-warn">⚠ En attente : {" · ".join(missing)}</div>', unsafe_allow_html=True)

if st.button(f"✉ Créer {len(st.session_state.contacts)} brouillon(s) dans Gmail", disabled=not ready):
    progress = st.progress(0)
    status   = st.empty()
    logs     = st.empty()

    log_lines = []
    ok_count  = 0
    err_count = 0
    token     = st.session_state.access_token

    for i, contact in enumerate(st.session_state.contacts):
        to      = resolve_email(contact, email_pattern, st.session_state.prenom_col, st.session_state.nom_col)
        subject = resolve_text(contact, mail_subject, st.session_state.prenom_col, st.session_state.nom_col)
        body    = resolve_text(contact, mail_body,    st.session_state.prenom_col, st.session_state.nom_col)

        try:
            raw = build_raw_email(to, subject, body, st.session_state.pdf_attachments)
            create_gmail_draft(token, raw)
            ok_count += 1
            log_lines.append(f'<div class="log-line-ok">✓ Draft créé → {to}</div>')
        except urllib.error.HTTPError as e:
            if e.code == 401 and st.session_state.refresh_token:
                try:
                    token = get_new_access_token(client_id, client_secret, st.session_state.refresh_token)
                    st.session_state.access_token = token
                    raw = build_raw_email(to, subject, body, st.session_state.pdf_attachments)
                    create_gmail_draft(token, raw)
                    ok_count += 1
                    log_lines.append(f'<div class="log-line-ok">✓ Draft créé → {to}</div>')
                except Exception as e2:
                    err_count += 1
                    log_lines.append(f'<div class="log-line-err">✗ {to} : {e2}</div>')
            else:
                err_count += 1
                log_lines.append(f'<div class="log-line-err">✗ {to} : {e}</div>')
        except Exception as e:
            err_count += 1
            log_lines.append(f'<div class="log-line-err">✗ {to} : {e}</div>')

        pct = (i + 1) / len(st.session_state.contacts)
        progress.progress(pct)
        status.markdown(f'<div class="log-line-info">{i+1} / {len(st.session_state.contacts)} traités…</div>', unsafe_allow_html=True)
        logs.markdown('\n'.join(log_lines[-10:]), unsafe_allow_html=True)

    status.empty()
    if err_count == 0:
        st.success(f"✅ {ok_count} brouillons créés avec succès dans Gmail !")
    else:
        st.warning(f"✅ {ok_count} brouillons créés · ⚠️ {err_count} erreur(s)")

    logs.markdown('\n'.join(log_lines), unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
