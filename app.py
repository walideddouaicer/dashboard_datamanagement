#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
University Data Warehouse Dashboard — with authentication
Professor Dashboard + Student Dashboard
"""

import hashlib
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
from datetime import date

# ─────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Tableau de Bord Universitaire",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════
#  DESIGN SYSTEM
# ══════════════════════════════════════════════

_CSS = """
<style>
/* ── Streamlit chrome ── */
#MainMenu, header, footer { visibility: hidden; }
.stDeployButton { display: none !important; }

/* ── App canvas ── */
.stApp { background-color: #F4F6F8; }
.main .block-container {
    padding: 1.5rem 2.5rem 3rem 2.5rem;
    max-width: 1440px;
}

/* ── KPI Cards ── */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 20px 24px 16px;
    box-shadow: 0 1px 3px rgba(15,23,42,.05), 0 1px 2px rgba(15,23,42,.03);
    transition: box-shadow .18s ease, transform .18s ease;
}
[data-testid="stMetric"]:hover {
    box-shadow: 0 6px 22px rgba(15,23,42,.10);
    transform: translateY(-2px);
}
[data-testid="stMetricLabel"] > div {
    font-size: .70rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: #94A3B8 !important;
}
[data-testid="stMetricValue"] > div {
    font-size: 1.65rem !important;
    font-weight: 700 !important;
    color: #1E293B !important;
    line-height: 1.2;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E2E8F0 !important;
}
[data-testid="stSidebar"] .block-container {
    padding-top: 1.25rem !important;
    padding-bottom: 2rem !important;
}

/* ── Sidebar selectbox / slider labels ── */
[data-testid="stSidebar"] label {
    font-size: .8rem !important;
    font-weight: 600 !important;
    color: #475569 !important;
}

/* ── Tabs ── */
button[data-baseweb="tab"] {
    font-size: .82rem !important;
    font-weight: 600 !important;
    color: #64748B !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #1E293B !important;
}
[data-testid="stTabsContent"] {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-top: none;
    border-radius: 0 0 10px 10px;
    padding: 16px;
}

/* ── Expanders ── */
[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 10px !important;
    margin-bottom: 8px;
    overflow: hidden;
}
[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    font-size: .88rem !important;
    color: #334155 !important;
}

/* ── Dataframes ── */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* ── Radio buttons ── */
[data-testid="stRadio"] label {
    font-size: .84rem !important;
    color: #475569 !important;
}

/* ── Section headings ── */
.sec-head {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 32px 0 20px;
    padding-bottom: 11px;
    border-bottom: 2px solid #E2E8F0;
    font-size: 1.05rem;
    font-weight: 700;
    color: #1E293B;
    letter-spacing: .01em;
}

/* ══ LOGIN PAGE ══ */
/* Dark gradient when login marker is present */
body:has(span#login-marker) [data-testid="stAppViewContainer"],
body:has(span#login-marker) [data-testid="stMain"],
body:has(span#login-marker) .stApp {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 55%, #334155 100%) !important;
}
/* Floating login card */
body:has(span#login-marker) [data-testid="stForm"] {
    background: #FFFFFF !important;
    border-radius: 18px !important;
    padding: 36px 32px 28px !important;
    box-shadow:
        0 24px 64px rgba(0,0,0,.35),
        0 4px 16px rgba(0,0,0,.15) !important;
    border: 1px solid rgba(255,255,255,.08) !important;
}
</style>
"""

def inject_css():
    st.markdown(_CSS, unsafe_allow_html=True)


# ── Chart theme helpers ────────────────────────

_CHART_FONT = dict(family="system-ui, -apple-system, sans-serif",
                   color="#64748B", size=11)


def _theme(fig: go.Figure, h: int = 330) -> go.Figure:
    """Apply the silver / slate premium theme to any Plotly figure."""
    fig.update_layout(
        height=h,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=_CHART_FONT,
        title=dict(
            font=dict(size=13, color="#1E293B", weight=700),
            x=0, xanchor="left",
            pad=dict(l=0, b=12),
        ),
        margin=dict(l=0, r=0, t=44, b=0),
        legend=dict(
            bgcolor="rgba(0,0,0,0)", borderwidth=0,
            font=dict(size=10, color="#64748B"),
        ),
        hoverlabel=dict(
            bgcolor="#1E293B", font_size=11,
            font_color="#F1F5F9", bordercolor="#475569",
        ),
    )
    fig.update_xaxes(
        showgrid=False, zeroline=False,
        showline=True, linecolor="#E2E8F0", tickcolor="#E2E8F0",
        tickfont=dict(size=10, color="#94A3B8"),
    )
    fig.update_yaxes(
        showgrid=True, gridcolor="#EDF2F7", gridwidth=1,
        zeroline=False, showline=False,
        tickfont=dict(size=10, color="#94A3B8"),
    )
    return fig


def _theme_hbar(fig: go.Figure, h: int = 330) -> go.Figure:
    """Theme variant for horizontal bar charts (flip grid axis)."""
    _theme(fig, h)
    fig.update_xaxes(showgrid=True, gridcolor="#EDF2F7", showline=False)
    fig.update_yaxes(showgrid=False, showline=False)
    return fig


# ── Layout helpers ─────────────────────────────

def section(icon: str, title: str):
    """Styled section heading with bottom border."""
    st.markdown(
        f'<div class="sec-head">{icon}&ensp;{title}</div>',
        unsafe_allow_html=True,
    )


def gap(px: int = 12):
    st.markdown(f"<div style='margin-top:{px}px'></div>", unsafe_allow_html=True)


def banner(title: str, subtitle: str = ""):
    """Dark gradient page banner replacing st.title()."""
    sub = (f'<p style="margin:5px 0 0;font-size:.84rem;'
           f'color:#94A3B8;font-weight:400">{subtitle}</p>'
           if subtitle else "")
    st.markdown(f"""
<div style="background:linear-gradient(118deg,#1E293B 0%,#334155 100%);
            border-radius:14px;padding:26px 30px 22px;margin-bottom:26px">
  <p style="margin:0;font-size:1.55rem;font-weight:700;
            color:#FFFFFF;letter-spacing:-.02em">{title}</p>
  {sub}
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  DATABASE ENGINES
# ══════════════════════════════════════════════

@st.cache_resource
def get_dwh_engine():
    """Data Warehouse — all KPI / dashboard queries."""
    return create_engine(
        "postgresql+psycopg2://postgres:postgres@localhost:5432/datawarehouse",
        pool_pre_ping=True,
    )


@st.cache_resource
def get_univ_engine():
    """Universite source DB — authentication + events table."""
    return create_engine(
        "postgresql+psycopg2://postgres:postgres@localhost:5432/Universite",
        pool_pre_ping=True,
    )


@st.cache_data(ttl=60)
def query(_engine, sql, **params):
    with _engine.connect() as conn:
        return pd.read_sql(text(sql), conn, params=params)


# ══════════════════════════════════════════════
#  AUTHENTICATION
# ══════════════════════════════════════════════

def _md5(password: str) -> str:
    return hashlib.md5(password.encode("utf-8")).hexdigest()


def authenticate(email: str, password: str):
    """
    Returns (role, user_id, display_name, annee_etude_or_None) on success,
    or None on failure.
    """
    hashed = _md5(password)
    engine = get_univ_engine()
    try:
        with engine.connect() as conn:
            row = conn.execute(
                text("SELECT id_prof, nom, prenom "
                     "FROM professeurs WHERE email = :e AND mot_de_passe = :p"),
                {"e": email, "p": hashed},
            ).fetchone()
            if row:
                return ("prof", int(row[0]), f"{row[1]} {row[2]}", None)

            row = conn.execute(
                text("SELECT num_apogee, nom, prenom, annee_etude "
                     "FROM etudiants WHERE email = :e AND mot_de_passe = :p"),
                {"e": email, "p": hashed},
            ).fetchone()
            if row:
                return ("student", int(row[0]), f"{row[1]} {row[2]}", row[3])
    except Exception as exc:
        st.error(f"Erreur de connexion à la base de données : {exc}")
    return None


def do_logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


# ══════════════════════════════════════════════
#  LOGIN PAGE
# ══════════════════════════════════════════════

def show_login_page():
    inject_css()
    # Marker for CSS :has() — triggers dark background + card shadow
    st.markdown('<span id="login-marker" style="display:none"></span>',
                unsafe_allow_html=True)
    # Hide sidebar on login
    st.markdown("<style>[data-testid='stSidebar']{display:none}</style>",
                unsafe_allow_html=True)

    # Vertical breathing room
    st.markdown("<div style='height:72px'></div>", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.05, 1])
    with col:
        # Brand header above the card
        st.markdown("""
<div style="text-align:center;margin-bottom:22px">
  <div style="font-size:2.6rem;line-height:1">🎓</div>
  <p style="font-size:1.45rem;font-weight:700;color:#F1F5F9;
            margin:10px 0 4px;letter-spacing:-.02em">Portail Académique</p>
  <p style="font-size:.84rem;color:#94A3B8;margin:0">
    Tableau de bord universitaire — Connexion requise</p>
</div>
""", unsafe_allow_html=True)

        # The stForm is styled as a floating white card via CSS
        with st.form("login_form", clear_on_submit=False):
            st.markdown(
                "<p style='font-size:.72rem;font-weight:700;color:#94A3B8;"
                "text-transform:uppercase;letter-spacing:.08em;"
                "margin:0 0 4px'>Adresse email</p>",
                unsafe_allow_html=True,
            )
            email = st.text_input(
                "email", placeholder="prenom.nom@univ.ma",
                label_visibility="collapsed",
            )
            gap(6)
            st.markdown(
                "<p style='font-size:.72rem;font-weight:700;color:#94A3B8;"
                "text-transform:uppercase;letter-spacing:.08em;"
                "margin:0 0 4px'>Mot de passe</p>",
                unsafe_allow_html=True,
            )
            password = st.text_input(
                "password", type="password", placeholder="••••••••",
                label_visibility="collapsed",
            )
            gap(10)
            submitted = st.form_submit_button(
                "Se connecter  →",
                use_container_width=True,
                type="primary",
            )

        # Auth logic (outside form so errors render below card)
        if submitted:
            if not email.strip() or not password:
                st.warning("Veuillez remplir tous les champs.")
            else:
                with st.spinner("Vérification en cours…"):
                    result = authenticate(email.strip(), password)
                if result:
                    role, user_id, name, extra = result
                    st.session_state["role"]      = role
                    st.session_state["user_id"]   = user_id
                    st.session_state["user_name"] = name
                    if extra is not None:
                        st.session_state["annee_etude"] = extra
                    st.rerun()
                else:
                    st.error("Email ou mot de passe incorrect.")

        gap(10)
        with st.expander("Comptes de démonstration"):
            st.code(
                "Professeur : aniss.moumen@univ.ma     /  prof123\n"
                "Étudiant   : mehdi.sabri@etudiant.ma  /  etudiant123",
                language=None,
            )


# ══════════════════════════════════════════════
#  AUTHENTICATED SIDEBAR
# ══════════════════════════════════════════════

def render_authenticated_sidebar():
    role = st.session_state["role"]
    name = st.session_state["user_name"]

    is_prof     = role == "prof"
    badge_bg    = "#EFF6FF" if is_prof else "#F0FDF4"
    badge_bdr   = "#BFDBFE" if is_prof else "#BBF7D0"
    badge_color = "#1D4ED8" if is_prof else "#15803D"
    role_label  = "Professeur" if is_prof else "Étudiant"
    icon        = "👨‍🏫" if is_prof else "👨‍🎓"

    st.sidebar.markdown(f"""
<div style="padding:2px 0 18px;border-bottom:1px solid #E2E8F0;margin-bottom:16px">
  <p style="font-size:1.05rem;font-weight:700;color:#1E293B;
            margin:0;letter-spacing:-.01em">🎓 EduBoard</p>
  <p style="font-size:.70rem;color:#94A3B8;margin:2px 0 0;font-weight:500">
    Système Universitaire</p>
</div>
<div style="background:{badge_bg};border:1px solid {badge_bdr};
            border-radius:10px;padding:11px 14px;margin-bottom:4px">
  <p style="font-size:.65rem;font-weight:700;color:{badge_color};
            text-transform:uppercase;letter-spacing:.09em;margin:0">{role_label}</p>
  <p style="font-size:.88rem;font-weight:600;color:#1E293B;
            margin:3px 0 0">{icon}&nbsp; {name}</p>
</div>
""", unsafe_allow_html=True)

    st.sidebar.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    if st.sidebar.button("🚪  Déconnexion", use_container_width=True):
        do_logout()
    st.sidebar.markdown(
        "<hr style='border:none;border-top:1px solid #E2E8F0;margin:14px 0'>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════
#  PROFESSOR DASHBOARD
# ══════════════════════════════════════════════

def show_prof_dashboard(engine, univ_engine, user_id):
    inject_css()
    banner("👨‍🏫 Tableau de Bord Professeur",
           "Suivi pédagogique · Analyse des performances · Gestion des risques")

    # ── Row-level security ──────────────────────
    df_assigned = query(
        univ_engine,
        "SELECT code_module FROM enseigne WHERE id_prof = :pid",
        pid=user_id,
    )
    if df_assigned.empty:
        st.warning("Vous n'avez aucun module assigné pour le moment.")
        return
    assigned_codes = df_assigned["code_module"].tolist()

    placeholders = ", ".join(f":c{i}" for i in range(len(assigned_codes)))
    code_params  = {f"c{i}": v for i, v in enumerate(assigned_codes)}
    modules_df = query(
        engine,
        f"SELECT code_module, intitule, semestre, annee_etude "
        f"FROM DIM_MODULE WHERE code_module IN ({placeholders}) "
        f"ORDER BY semestre, intitule",
        **code_params,
    )
    temps_df = query(
        engine,
        "SELECT id_temps, annee_scolaire, semestre "
        "FROM DIM_TEMPS ORDER BY annee_scolaire, semestre",
    )

    # ── Sidebar filters ─────────────────────────
    st.sidebar.markdown(
        "<p style='font-size:.70rem;font-weight:700;color:#94A3B8;"
        "text-transform:uppercase;letter-spacing:.08em;"
        "margin:0 0 10px'>Filtres</p>",
        unsafe_allow_html=True,
    )
    module_options  = modules_df["intitule"].tolist()
    selected_module = st.sidebar.selectbox("Module", module_options)
    code_mod = modules_df.loc[
        modules_df["intitule"] == selected_module, "code_module"
    ].values[0]

    annees         = sorted(temps_df["annee_scolaire"].unique().tolist(), reverse=True)
    selected_annee = st.sidebar.selectbox("Année scolaire", ["Toutes"] + annees)
    seuil_absence  = st.sidebar.slider("Seuil d'absence (%)", 0, 100, 25, step=5)
    seuil_note     = st.sidebar.slider("Seuil note alerte", 0.0, 20.0, 10.0, step=0.5)

    if selected_annee == "Toutes":
        time_filter = ""
        time_params: dict = {"code_mod": code_mod}
    else:
        time_filter = "AND dt.annee_scolaire = :annee"
        time_params = {"code_mod": code_mod, "annee": selected_annee}

    # ════════════════════════════
    #  1 — STATISTIQUES & PERFORMANCE
    # ════════════════════════════
    section("📈", "Statistiques & Performance")

    q_moy_annee = f"""
        SELECT dt.annee_scolaire, ROUND(AVG(fn.moyenne)::numeric, 2) AS moyenne
        FROM FAIT_NOTES fn
        JOIN DIM_TEMPS dt ON fn.id_temps = dt.id_temps
        WHERE fn.code_module = :code_mod {time_filter}
        GROUP BY dt.annee_scolaire
        ORDER BY dt.annee_scolaire
    """
    df_moy_annee = query(engine, q_moy_annee, **time_params)

    q_notes = f"""
        SELECT de.nom || ' ' || de.prenom AS etudiant,
               fn.note_tp, fn.note_cc, fn.note_projet, fn.note_examen,
               fn.moyenne, fn.classement, fn.ecart_moyenne_classe,
               fn.statut_validation, dt.annee_scolaire
        FROM FAIT_NOTES fn
        JOIN DIM_ETUDIANT de ON fn.num_apogee = de.num_apogee
        JOIN DIM_TEMPS dt    ON fn.id_temps = dt.id_temps
        WHERE fn.code_module = :code_mod {time_filter}
        ORDER BY fn.moyenne DESC
    """
    df_notes = query(engine, q_notes, **time_params)

    col1, col2, col3, col4 = st.columns(4)
    if not df_notes.empty:
        col1.metric("Moyenne générale",   f"{df_notes['moyenne'].mean():.2f} / 20")
        col2.metric("Note maximale",      f"{df_notes['moyenne'].max():.2f} / 20")
        col3.metric("Note minimale",      f"{df_notes['moyenne'].min():.2f} / 20")
        pct_val = (df_notes["statut_validation"] == "Valide").mean() * 100
        col4.metric("Taux de validation", f"{pct_val:.0f} %")

    gap(8)
    c1, c2 = st.columns(2)
    with c1:
        if not df_moy_annee.empty:
            fig = px.line(
                df_moy_annee, x="annee_scolaire", y="moyenne",
                title=f"Évolution de la moyenne — {selected_module}",
                markers=True,
                labels={"annee_scolaire": "Année scolaire", "moyenne": "Moyenne /20"},
                color_discrete_sequence=["#3B82F6"],
            )
            fig.add_hline(y=10, line_dash="dash", line_color="#EF4444",
                          annotation_text="Seuil 10",
                          annotation_font=dict(color="#EF4444", size=10))
            _theme(fig, 310)
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        q_bar = """
            SELECT dm.intitule AS module,
                   ROUND(AVG(fn.moyenne)::numeric, 2) AS moyenne
            FROM FAIT_NOTES fn
            JOIN DIM_MODULE dm ON fn.code_module = dm.code_module
            JOIN DIM_TEMPS dt  ON fn.id_temps = dt.id_temps
            WHERE 1=1
        """
        params_bar: dict = {}
        if selected_annee != "Toutes":
            q_bar += " AND dt.annee_scolaire = :annee"
            params_bar["annee"] = selected_annee
        q_bar += " GROUP BY dm.intitule ORDER BY moyenne DESC LIMIT 12"
        df_bar = query(engine, q_bar, **params_bar)
        if not df_bar.empty:
            fig2 = px.bar(
                df_bar, x="moyenne", y="module", orientation="h",
                title="Classement des modules par moyenne",
                color="moyenne",
                color_continuous_scale="RdYlGn",
                range_color=[8, 16],
            )
            _theme_hbar(fig2, 310)
            fig2.update_coloraxes(showscale=False)
            st.plotly_chart(fig2, use_container_width=True)

    if not df_notes.empty:
        fig3 = px.histogram(
            df_notes, x="moyenne", nbins=15,
            title=f"Distribution des notes — {selected_module}",
            labels={"moyenne": "Moyenne /20", "count": "Étudiants"},
            color_discrete_sequence=["#64748B"],
        )
        fig3.add_vline(x=10, line_dash="dash", line_color="#EF4444",
                       annotation_text="Seuil 10",
                       annotation_font=dict(color="#EF4444", size=10))
        fig3.add_vline(x=12, line_dash="dot",  line_color="#F59E0B",
                       annotation_text="Seuil 12",
                       annotation_font=dict(color="#F59E0B", size=10))
        _theme(fig3, 260)
        st.plotly_chart(fig3, use_container_width=True)

    gap(4)
    st.markdown("**Profils étudiants**")
    tab_top, tab_bot, tab_risk = st.tabs(
        ["🏆 Top 5", "⚠️ Bottom 5", f"📉 En dessous de {seuil_note}/20"]
    )
    if not df_notes.empty:
        display_cols = ["etudiant", "moyenne", "classement", "statut_validation", "annee_scolaire"]
        with tab_top:
            st.dataframe(df_notes.head(5)[display_cols], use_container_width=True)
        with tab_bot:
            st.dataframe(df_notes.tail(5)[display_cols], use_container_width=True)
        with tab_risk:
            st.dataframe(
                df_notes[df_notes["moyenne"] < seuil_note][display_cols],
                use_container_width=True,
            )

    # ════════════════════════════
    #  2 — ABSENCES
    # ════════════════════════════
    section("🚨", "Absences")

    q_abs = f"""
        SELECT de.nom || ' ' || de.prenom AS etudiant,
               de.num_apogee,
               fa.date_seance, fa.seance, fa.justifiee,
               fa.nb_absences_total, fa.nb_seances_total,
               fa.taux_absence, fa.seuil_depasse,
               dt.annee_scolaire
        FROM FAIT_ABSENCES fa
        JOIN DIM_ETUDIANT de ON fa.num_apogee = de.num_apogee
        JOIN DIM_TEMPS dt    ON fa.id_temps = dt.id_temps
        WHERE fa.code_module = :code_mod {time_filter}
        ORDER BY fa.taux_absence DESC
    """
    df_abs = query(engine, q_abs, **time_params)

    if not df_abs.empty:
        col_a1, col_a2, col_a3 = st.columns(3)
        col_a1.metric("Taux d'absence moyen",    f"{df_abs['taux_absence'].mean():.1f} %")
        n_depasse = df_abs.drop_duplicates("etudiant")["seuil_depasse"].eq("O").sum()
        col_a2.metric("Étudiants seuil dépassé", int(n_depasse))
        pct_just = (df_abs["justifiee"] == "O").mean() * 100
        col_a3.metric("Absences justifiées",      f"{pct_just:.0f} %")

        gap(8)
        df_abs["date_seance"] = pd.to_datetime(df_abs["date_seance"])
        df_abs_time = df_abs.groupby("date_seance").size().reset_index(name="nb_absences")
        fig_abs = px.line(
            df_abs_time, x="date_seance", y="nb_absences",
            title="Évolution des absences dans le temps",
            labels={"date_seance": "Date", "nb_absences": "Absences"},
            color_discrete_sequence=["#F59E0B"],
        )
        _theme(fig_abs, 280)
        st.plotly_chart(fig_abs, use_container_width=True)

        gap(4)
        st.markdown("**Détail — filtrer par justification**")
        just_filter = st.radio(
            "Type", ["Toutes", "Justifiées (O)", "Non justifiées (N)"], horizontal=True
        )
        df_abs_show = df_abs.copy()
        if just_filter == "Justifiées (O)":
            df_abs_show = df_abs_show[df_abs_show["justifiee"] == "O"]
        elif just_filter == "Non justifiées (N)":
            df_abs_show = df_abs_show[df_abs_show["justifiee"] == "N"]
        st.dataframe(
            df_abs_show[[
                "etudiant", "date_seance", "seance",
                "justifiee", "taux_absence", "seuil_depasse",
            ]],
            use_container_width=True,
        )
    else:
        st.info("Aucune donnée d'absence pour ce module / cette période.")

    # ════════════════════════════
    #  3 — SCORE DE RISQUE
    # ════════════════════════════
    section("⚠️", "Score de Risque Étudiant")

    if not df_notes.empty:
        df_risk = df_notes[["etudiant", "moyenne", "statut_validation"]].copy()

        if not df_abs.empty:
            abs_by_stud = (
                df_abs.drop_duplicates(["etudiant"])
                      .set_index("etudiant")[["taux_absence", "seuil_depasse"]]
            )
            df_risk = df_risk.join(abs_by_stud, on="etudiant")
        else:
            df_risk["taux_absence"]  = 0.0
            df_risk["seuil_depasse"] = "N"

        q_trav = f"""
            SELECT de.nom || ' ' || de.prenom AS etudiant,
                   COUNT(*) FILTER (WHERE ft.rendu = 'N') AS non_rendus,
                   COUNT(*) AS total_travaux
            FROM FAIT_TRAVAUX ft
            JOIN DIM_ETUDIANT de ON ft.num_apogee = de.num_apogee
            JOIN DIM_TEMPS dt    ON ft.id_temps = dt.id_temps
            WHERE ft.code_module = :code_mod {time_filter}
            GROUP BY etudiant
        """
        df_trav_risk = query(engine, q_trav, **time_params)
        if not df_trav_risk.empty:
            df_trav_risk["taux_non_rendu"] = (
                df_trav_risk["non_rendus"] / df_trav_risk["total_travaux"] * 100
            ).round(1)
            df_risk = df_risk.merge(
                df_trav_risk[["etudiant", "taux_non_rendu"]], on="etudiant", how="left"
            )
        else:
            df_risk["taux_non_rendu"] = 0.0

        df_risk["taux_non_rendu"] = df_risk["taux_non_rendu"].fillna(0.0)
        df_risk["taux_absence"]   = df_risk["taux_absence"].fillna(0.0)
        df_risk["seuil_depasse"]  = df_risk["seuil_depasse"].fillna("N")

        note_norm = ((20 - df_risk["moyenne"].clip(0, 20)) / 20 * 40).round(1)
        abs_norm  = (df_risk["taux_absence"].clip(0, 100) / 100 * 35).round(1)
        trav_norm = (df_risk["taux_non_rendu"].clip(0, 100) / 100 * 25).round(1)

        df_risk["score_risque"]  = (note_norm + abs_norm + trav_norm).clip(0, 100).round(1)
        df_risk["niveau_risque"] = pd.cut(
            df_risk["score_risque"],
            bins=[-1, 30, 55, 100],
            labels=["🟢 Faible", "🟡 Moyen", "🔴 Élevé"],
        )
        df_risk = df_risk.sort_values("score_risque", ascending=False)

        fig_risk = px.bar(
            df_risk.head(20), x="etudiant", y="score_risque",
            color="niveau_risque",
            color_discrete_map={
                "🟢 Faible": "#10B981",
                "🟡 Moyen":  "#F59E0B",
                "🔴 Élevé":  "#EF4444",
            },
            title="Score de risque par étudiant (top 20)",
            labels={"score_risque": "Score / 100", "etudiant": "Étudiant"},
        )
        fig_risk.update_xaxes(tickangle=40)
        _theme(fig_risk, 350)
        st.plotly_chart(fig_risk, use_container_width=True)

        st.dataframe(
            df_risk[[
                "etudiant", "moyenne", "taux_absence",
                "taux_non_rendu", "score_risque", "niveau_risque",
            ]],
            use_container_width=True,
        )

    # ════════════════════════════
    #  4 — RÉCLAMATIONS
    # ════════════════════════════
    section("📝", "Réclamations")

    q_reclam = """
        SELECT de.nom || ' ' || de.prenom AS etudiant,
               dp.nom || ' ' || dp.prenom AS professeur,
               dm.intitule AS module,
               fr.type_reclamation, fr.statut,
               fr.date_depot, fr.date_reponse, fr.delai_traitement,
               dt.annee_scolaire
        FROM FAIT_RECLAMATIONS fr
        JOIN DIM_ETUDIANT de ON fr.num_apogee = de.num_apogee
        JOIN DIM_PROF dp     ON fr.id_prof    = dp.id_prof
        JOIN DIM_MODULE dm   ON fr.code_module = dm.code_module
        JOIN DIM_TEMPS dt    ON fr.id_temps   = dt.id_temps
        WHERE fr.code_module = :code_mod
    """
    params_reclam: dict = {"code_mod": code_mod}
    if selected_annee != "Toutes":
        q_reclam += " AND dt.annee_scolaire = :annee"
        params_reclam["annee"] = selected_annee
    q_reclam += " ORDER BY fr.date_depot DESC"
    df_reclam = query(engine, q_reclam, **params_reclam)

    if not df_reclam.empty:
        col_r1, col_r2, col_r3 = st.columns(3)
        col_r1.metric("Total réclamations", len(df_reclam))
        traitees = (df_reclam["statut"] == "traitee").sum()
        col_r2.metric("Traitées",   int(traitees))
        col_r3.metric("En attente", int(len(df_reclam) - traitees))

        gap(8)
        cr1, cr2 = st.columns(2)
        with cr1:
            fig_pie = px.pie(
                df_reclam, names="statut",
                title="Statut des réclamations",
                color_discrete_sequence=["#3B82F6", "#94A3B8", "#CBD5E1"],
                hole=0.45,
            )
            _theme(fig_pie, 300)
            fig_pie.update_traces(textfont_size=11, textfont_color="#FFFFFF")
            st.plotly_chart(fig_pie, use_container_width=True)
        with cr2:
            fig_type = px.bar(
                df_reclam.groupby("type_reclamation").size().reset_index(name="count"),
                x="type_reclamation", y="count",
                title="Types de réclamations",
                labels={"type_reclamation": "Type", "count": "Nombre"},
                color_discrete_sequence=["#475569"],
            )
            _theme(fig_type, 300)
            st.plotly_chart(fig_type, use_container_width=True)

        gap(4)
        st.markdown("**Suivi détaillé des réclamations**")
        st.dataframe(
            df_reclam[[
                "etudiant", "module", "type_reclamation", "statut",
                "date_depot", "date_reponse", "delai_traitement",
            ]],
            use_container_width=True,
        )
    else:
        st.info("Aucune réclamation pour ce module / cette période.")


# ══════════════════════════════════════════════
#  STUDENT DASHBOARD
# ══════════════════════════════════════════════

def show_student_dashboard(dwh_engine, univ_engine, num_apogee, user_name, annee_etude):
    inject_css()
    banner(
        f"👨‍🎓 Espace Étudiant",
        f"{user_name}  ·  Apogée {num_apogee}  ·  {annee_etude}",
    )

    # ════════════════════════════
    #  1 — NOTES & RÉSULTATS
    # ════════════════════════════
    section("📊", "Notes & Résultats")

    q_stud_notes = """
        SELECT dm.intitule AS module, dm.semestre,
               fn.note_tp, fn.note_cc, fn.note_projet, fn.note_examen,
               fn.moyenne, fn.classement, fn.ecart_moyenne_classe,
               fn.statut_validation, fn.evaluations_passees,
               dt.annee_scolaire
        FROM FAIT_NOTES fn
        JOIN DIM_MODULE dm ON fn.code_module = dm.code_module
        JOIN DIM_TEMPS dt  ON fn.id_temps    = dt.id_temps
        WHERE fn.num_apogee = :num
        ORDER BY dt.annee_scolaire, dm.semestre, dm.intitule
    """
    df_stud_notes = query(dwh_engine, q_stud_notes, num=num_apogee)

    if not df_stud_notes.empty:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Moyenne générale",      f"{df_stud_notes['moyenne'].mean():.2f} / 20")
        nb_val = (df_stud_notes["statut_validation"] == "Valide").sum()
        col2.metric("Modules validés",       f"{nb_val} / {len(df_stud_notes)}")
        best_mod  = df_stud_notes.loc[df_stud_notes["moyenne"].idxmax(), "module"]
        worst_mod = df_stud_notes.loc[df_stud_notes["moyenne"].idxmin(), "module"]
        col3.metric("Meilleur module",       best_mod)
        col4.metric("Module le plus faible", worst_mod)

        gap(8)
        st.markdown("**Détail des notes par module**")
        display_notes = df_stud_notes[[
            "module", "semestre", "annee_scolaire",
            "note_tp", "note_cc", "note_projet", "note_examen",
            "moyenne", "classement", "ecart_moyenne_classe", "statut_validation",
        ]].rename(columns={
            "module": "Module", "semestre": "Sem", "annee_scolaire": "Année",
            "note_tp": "TP", "note_cc": "CC", "note_projet": "Projet",
            "note_examen": "Exam", "moyenne": "Moy",
            "classement": "Rang", "ecart_moyenne_classe": "Écart",
            "statut_validation": "Statut",
        })
        st.dataframe(display_notes, use_container_width=True)

        gap(8)
        evo = df_stud_notes.groupby(["annee_scolaire", "semestre"])["moyenne"].mean().reset_index()
        evo["periode"] = evo["annee_scolaire"] + " / " + evo["semestre"]
        fig_evo = px.line(
            evo.sort_values(["annee_scolaire", "semestre"]),
            x="periode", y="moyenne", markers=True,
            title="Évolution de la moyenne par semestre",
            labels={"periode": "Période", "moyenne": "Moyenne /20"},
            color_discrete_sequence=["#3B82F6"],
        )
        fig_evo.add_hline(y=10, line_dash="dash", line_color="#EF4444",
                          annotation_text="Seuil 10",
                          annotation_font=dict(color="#EF4444", size=10))
        fig_evo.add_hline(y=12, line_dash="dot",  line_color="#F59E0B",
                          annotation_text="Seuil 12",
                          annotation_font=dict(color="#F59E0B", size=10))
        _theme(fig_evo, 300)
        st.plotly_chart(fig_evo, use_container_width=True)

        gap(4)
        c1, c2 = st.columns(2)
        with c1:
            fig_ecart = px.bar(
                df_stud_notes, x="module", y="ecart_moyenne_classe",
                title="Écart à la moyenne de classe (+ = au-dessus)",
                color="ecart_moyenne_classe",
                color_continuous_scale="RdYlGn",
                range_color=[-5, 5],
                labels={"module": "Module", "ecart_moyenne_classe": "Écart"},
            )
            fig_ecart.update_xaxes(tickangle=40)
            fig_ecart.add_hline(y=0, line_dash="solid",
                                line_color="#94A3B8", line_width=1)
            _theme(fig_ecart, 320)
            fig_ecart.update_coloraxes(showscale=False)
            st.plotly_chart(fig_ecart, use_container_width=True)

        with c2:
            val_df = df_stud_notes[["module", "statut_validation", "moyenne"]].copy()
            val_df["couleur"] = val_df["statut_validation"].map(
                {"Valide": "Validé", "Non valide": "Non validé"}
            )
            fig_val = px.bar(
                val_df, x="module", y="moyenne", color="couleur",
                color_discrete_map={"Validé": "#10B981", "Non validé": "#EF4444"},
                title="Validation par module",
                labels={"module": "Module", "moyenne": "Moyenne /20"},
            )
            fig_val.add_hline(y=10, line_dash="dash",
                              line_color="#94A3B8", line_width=1)
            fig_val.update_xaxes(tickangle=40)
            _theme(fig_val, 320)
            st.plotly_chart(fig_val, use_container_width=True)

        gap(4)
        st.markdown("**Classement dans la classe**")
        rank_df = df_stud_notes[["module", "classement", "annee_scolaire"]].dropna()
        if not rank_df.empty:
            st.dataframe(
                rank_df.rename(columns={
                    "module": "Module", "classement": "Rang", "annee_scolaire": "Année"
                }),
                use_container_width=True,
            )
    else:
        st.info("Aucune note enregistrée pour cet étudiant.")

    # ════════════════════════════
    #  2 — ABSENCES
    # ════════════════════════════
    section("🚨", "Absences")

    q_stud_abs = """
        SELECT dm.intitule AS module, fa.date_seance, fa.seance,
               fa.justifiee, fa.nb_absences_total, fa.nb_seances_total,
               fa.taux_absence, fa.seuil_depasse, dt.annee_scolaire
        FROM FAIT_ABSENCES fa
        JOIN DIM_MODULE dm ON fa.code_module = dm.code_module
        JOIN DIM_TEMPS dt  ON fa.id_temps    = dt.id_temps
        WHERE fa.num_apogee = :num
        ORDER BY fa.date_seance DESC
    """
    df_stud_abs = query(dwh_engine, q_stud_abs, num=num_apogee)

    if not df_stud_abs.empty:
        col_a1, col_a2, col_a3 = st.columns(3)
        col_a1.metric("Total absences",      int(df_stud_abs["nb_absences_total"].iloc[0]))
        pct_just = (df_stud_abs["justifiee"] == "O").mean() * 100
        col_a2.metric("Absences justifiées", f"{pct_just:.0f} %")
        any_depasse = (df_stud_abs["seuil_depasse"] == "O").any()
        col_a3.metric("Seuil dépassé",       "⚠️ OUI" if any_depasse else "✅ NON")

        gap(8)
        taux_max = float(df_stud_abs["taux_absence"].max())
        bar_color = "#EF4444" if taux_max > 25 else "#10B981"
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=taux_max,
            title={"text": "Taux d'absence max (%)",
                   "font": {"size": 13, "color": "#475569",
                            "family": "system-ui, sans-serif"}},
            number={"suffix": " %",
                    "font": {"size": 30, "color": "#1E293B",
                             "family": "system-ui, sans-serif"}},
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickfont": {"size": 10, "color": "#94A3B8"},
                    "tickcolor": "#E2E8F0",
                    "linecolor": "#E2E8F0",
                },
                "bar": {"color": bar_color, "thickness": 0.22},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0,   25],  "color": "#D1FAE5"},
                    {"range": [25,  50],  "color": "#FEF3C7"},
                    {"range": [50, 100],  "color": "#FEE2E2"},
                ],
                "threshold": {
                    "line": {"color": "#EF4444", "width": 3},
                    "thickness": 0.75,
                    "value": 25,
                },
            },
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            height=240,
            margin=dict(l=24, r=24, t=24, b=24),
            font=dict(family="system-ui, sans-serif"),
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

        gap(4)
        st.markdown("**Historique des absences**")
        st.dataframe(
            df_stud_abs[[
                "module", "date_seance", "seance",
                "justifiee", "taux_absence", "seuil_depasse",
            ]].rename(columns={
                "module": "Module", "date_seance": "Date", "seance": "Séance",
                "justifiee": "Justifiée", "taux_absence": "Taux (%)",
                "seuil_depasse": "Seuil dépassé",
            }),
            use_container_width=True,
        )
    else:
        st.success("Aucune absence enregistrée pour cet étudiant.")

    # ════════════════════════════
    #  3 — RÉCLAMATIONS
    # ════════════════════════════
    section("📝", "Réclamations")

    q_stud_reclam = """
        SELECT dm.intitule AS module,
               dp.nom || ' ' || dp.prenom AS professeur,
               fr.type_reclamation, fr.statut,
               fr.date_depot, fr.date_reponse, fr.delai_traitement,
               dt.annee_scolaire
        FROM FAIT_RECLAMATIONS fr
        JOIN DIM_MODULE dm ON fr.code_module = dm.code_module
        JOIN DIM_PROF dp   ON fr.id_prof     = dp.id_prof
        JOIN DIM_TEMPS dt  ON fr.id_temps    = dt.id_temps
        WHERE fr.num_apogee = :num
        ORDER BY fr.date_depot DESC
    """
    df_stud_reclam = query(dwh_engine, q_stud_reclam, num=num_apogee)

    if not df_stud_reclam.empty:
        col_rc1, col_rc2, col_rc3 = st.columns(3)
        col_rc1.metric("Réclamations déposées", len(df_stud_reclam))
        traitee_n = (df_stud_reclam["statut"] == "traitee").sum()
        col_rc2.metric("Traitées",   int(traitee_n))
        col_rc3.metric("En attente", int(len(df_stud_reclam) - traitee_n))

        gap(4)
        st.markdown("**Historique des réclamations**")
        st.dataframe(
            df_stud_reclam.rename(columns={
                "module": "Module", "professeur": "Professeur",
                "type_reclamation": "Type", "statut": "Statut",
                "date_depot": "Date dépôt", "date_reponse": "Date réponse",
                "delai_traitement": "Délai (j)", "annee_scolaire": "Année",
            }),
            use_container_width=True,
        )
    else:
        st.info("Aucune réclamation pour cet étudiant.")

    # ════════════════════════════
    #  4 — ÉVÉNEMENTS & ALERTES
    # ════════════════════════════
    section("📅", "Événements & Alertes")

    # Events live in the Universite source DB, joined with modules there
    q_events = """
        SELECT ev.type_evenement, ev.objet, ev.date_evenement,
               ev.heure_evenement, m.intitule AS module, ev.promotion
        FROM evenements ev
        JOIN modules m ON ev.code_module = m.code_module
        ORDER BY ev.date_evenement ASC
    """
    df_events = query(univ_engine, q_events)

    if not df_events.empty:
        today = date.today()
        df_events["date_evenement"] = pd.to_datetime(df_events["date_evenement"])
        df_events["jours_restants"] = df_events["date_evenement"].dt.date.apply(
            lambda d: (d - today).days
        )
        upcoming = df_events[df_events["jours_restants"] >= 0].copy()
        past     = df_events[df_events["jours_restants"] < 0].copy()

        if not upcoming.empty:
            st.markdown("**Événements à venir**")
            for _, ev in upcoming.iterrows():
                jj    = int(ev["jours_restants"])
                color = "🔴" if jj <= 7 else ("🟡" if jj <= 30 else "🟢")
                with st.expander(
                    f"{color} {ev['objet']} — "
                    f"{ev['date_evenement'].strftime('%d/%m/%Y')} ({jj} j)"
                ):
                    st.write(f"**Module :** {ev['module']}")
                    st.write(f"**Type :** {ev['type_evenement']}")
                    st.write(f"**Heure :** {ev['heure_evenement']}")
                    st.write(f"**Promotion :** {ev['promotion']}")
                    if jj <= 7:
                        st.warning(f"⚠️ Échéance dans {jj} jour(s) !")

        if not past.empty:
            gap(4)
            st.markdown("**Événements passés**")
            st.dataframe(
                past[["objet", "module", "type_evenement",
                       "date_evenement", "promotion"]],
                use_container_width=True,
            )
    else:
        st.info("Aucun événement dans le calendrier.")

    # ── Alertes ─────────────────────────────────
    gap(16)
    st.markdown("**🔔 Résumé des alertes**")
    alertes = []
    if not df_stud_abs.empty and (df_stud_abs["seuil_depasse"] == "O").any():
        alertes.append(
            "⚠️ Votre taux d'absence a dépassé le seuil réglementaire dans au moins un module."
        )
    if not df_stud_notes.empty:
        mods_risk = df_stud_notes[
            df_stud_notes["statut_validation"] == "Non valide"
        ]["module"].tolist()
        if mods_risk:
            alertes.append(f"📉 Modules non validés : {', '.join(mods_risk)}")
    if not df_stud_reclam.empty:
        pending = df_stud_reclam[df_stud_reclam["statut"] == "en_attente"]
        if not pending.empty:
            alertes.append(f"📝 {len(pending)} réclamation(s) en attente de réponse.")

    if alertes:
        for a in alertes:
            st.warning(a)
    else:
        st.success("✅ Aucune alerte active. Tout va bien !")


# ══════════════════════════════════════════════
#  MAIN ROUTING
# ══════════════════════════════════════════════

dwh_engine  = get_dwh_engine()
univ_engine = get_univ_engine()

if "role" not in st.session_state:
    show_login_page()

elif st.session_state["role"] == "prof":
    render_authenticated_sidebar()
    show_prof_dashboard(dwh_engine, univ_engine, st.session_state["user_id"])

elif st.session_state["role"] == "student":
    render_authenticated_sidebar()
    show_student_dashboard(
        dwh_engine,
        univ_engine,
        num_apogee  = st.session_state["user_id"],
        user_name   = st.session_state["user_name"],
        annee_etude = st.session_state.get("annee_etude", ""),
    )
