import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DB Vertrieb · Digital Transformation OKRs",
    page_icon="🚄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global style ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stSidebar"] { background-color: #1a1a2e; }
  [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
  .kpi-card {
    background: linear-gradient(135deg, #1e3a5f, #16213e);
    border-radius: 12px; padding: 18px 22px;
    border-left: 4px solid #e63946;
    color: white; margin-bottom: 10px;
  }
  .kpi-value { font-size: 2rem; font-weight: 700; color: #f1c40f; }
  .kpi-label { font-size: 0.85rem; color: #b0c4de; margin-top: 4px; }
  .kpi-meta  { font-size: 0.75rem; color: #7f8c8d; margin-top: 2px; }
  .obj-header {
    background: linear-gradient(90deg, #e63946, #c0392b);
    color: white; padding: 10px 18px; border-radius: 8px;
    font-weight: 600; margin-bottom: 8px;
  }
  .why-box {
    background: #f0f4f8; border-left: 4px solid #2980b9;
    padding: 10px 14px; border-radius: 6px;
    font-size: 0.88rem; color: #2c3e50; margin-bottom: 10px;
  }
  .section-title { color: #e63946; font-size: 1.1rem; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SIMULATED DATA
# ══════════════════════════════════════════════════════════════════════════════
MONTHS = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
          "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

# ── Página 2: Alineamiento Dinámico ──────────────────────────────────────────
d_digital_sales_share = [38, 41, 43, 46, 48, 51, 54, 56, 58, 61, 63, 65]
d_it_strategy_alignment = [45, 50, 55, 60, 63, 66, 68, 70, 72, 74, 76, 78]
d_release_cycles = [2, 2, 3, 4, 4, 6, 6, 8, 9, 10, 11, 12]
d_cross_channel_projects = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]
d_omnichannel_nps = [28, 30, 31, 33, 35, 36, 38, 39, 41, 43, 44, 46]

# ── Página 3: Liderazgo Digital ───────────────────────────────────────────────
d_cdo_initiatives = [1, 2, 2, 3, 4, 4, 5, 5, 6, 7, 7, 8]
d_digital_training_pct = [10, 15, 22, 30, 38, 45, 52, 58, 64, 70, 74, 78]
d_agile_certified = [5, 8, 12, 18, 25, 32, 40, 48, 55, 62, 68, 72]
d_leadership_digital_score = [42, 45, 48, 51, 54, 57, 60, 62, 65, 67, 69, 71]
d_safe_adoption = [0, 5, 12, 20, 28, 36, 44, 52, 58, 63, 67, 70]

# ── Página 4: Innovación Centrada en el Cliente ───────────────────────────────
d_app_users = [1.2, 1.35, 1.5, 1.65, 1.82, 2.0, 2.18, 2.35, 2.5, 2.65, 2.78, 2.9]
d_csat = [62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]
d_lab_prototypes = [0, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
d_innovation_ideas = [5, 8, 11, 14, 17, 20, 23, 26, 28, 30, 32, 35]
d_digital_ticket_pct = [52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 71, 73]

# ── Página 5: Agilidad Operativa ──────────────────────────────────────────────
d_time_to_market = [100, 94, 88, 82, 76, 70, 65, 60, 55, 50, 46, 42]  # % of baseline
d_releases_per_month = [0.5, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5]
d_devops_coverage = [10, 15, 22, 30, 38, 45, 52, 58, 63, 67, 70, 74]
d_scrum_teams = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 12]
d_process_automation = [15, 18, 22, 26, 30, 35, 40, 44, 48, 52, 56, 60]

# ── Helper colors ─────────────────────────────────────────────────────────────
RED   = "#e63946"
GOLD  = "#f1c40f"
BLUE  = "#2980b9"
GREEN = "#27ae60"
GRAY  = "#95a5a6"

# ══════════════════════════════════════════════════════════════════════════════
#  REUSABLE COMPONENTS
# ══════════════════════════════════════════════════════════════════════════════
def kpi_card(value, label, meta=""):
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-value">{value}</div>
      <div class="kpi-label">{label}</div>
      <div class="kpi-meta">{meta}</div>
    </div>""", unsafe_allow_html=True)

def why_box(text):
    st.markdown(f'<div class="why-box">💡 <strong>Por qué este KR es importante:</strong> {text}</div>',
                unsafe_allow_html=True)

def obj_header(obj_id, name, justification):
    st.markdown(f'<div class="obj-header">📌 {obj_id} · {name}</div>', unsafe_allow_html=True)
    st.caption(f"*Justificación estratégica:* {justification}")

def line_chart(y_data, title, y_label, color=BLUE, target=None, target_label="Meta"):
    df = pd.DataFrame({"Mes": MONTHS, "Valor": y_data})
    fig = px.line(df, x="Mes", y="Valor", title=title,
                  markers=True, color_discrete_sequence=[color])
    if target:
        fig.add_hline(y=target, line_dash="dash", line_color=GREEN,
                      annotation_text=f"{target_label}: {target}",
                      annotation_position="bottom right")
    fig.update_layout(height=280, margin=dict(t=40, b=20, l=30, r=20),
                      plot_bgcolor="#f8f9fa", paper_bgcolor="white",
                      yaxis_title=y_label, xaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

def bar_chart(y_data, title, y_label, color=BLUE):
    df = pd.DataFrame({"Mes": MONTHS, "Valor": y_data})
    fig = px.bar(df, x="Mes", y="Valor", title=title,
                 color_discrete_sequence=[color])
    fig.update_layout(height=280, margin=dict(t=40, b=20, l=30, r=20),
                      plot_bgcolor="#f8f9fa", paper_bgcolor="white",
                      yaxis_title=y_label, xaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

def gauge_chart(value, title, max_val=100, color=BLUE):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"size": 13}},
        gauge={
            "axis": {"range": [0, max_val]},
            "bar":  {"color": color},
            "steps": [
                {"range": [0,   max_val*0.4], "color": "#fadbd8"},
                {"range": [max_val*0.4, max_val*0.7], "color": "#fdebd0"},
                {"range": [max_val*0.7, max_val], "color": "#d5f5e3"},
            ],
            "threshold": {"line": {"color": RED, "width": 3},
                          "thickness": 0.8, "value": max_val*0.85},
        }
    ))
    fig.update_layout(height=250, margin=dict(t=40, b=10, l=20, r=20))
    st.plotly_chart(fig, use_container_width=True)

def progress_bar(current, target, label):
    pct = min(int(current / target * 100), 100)
    color = GREEN if pct >= 75 else (GOLD if pct >= 50 else RED)
    st.markdown(f"""
    <div style="margin-bottom:10px">
      <div style="font-size:0.82rem;color:#555;margin-bottom:3px">{label}</div>
      <div style="background:#eee;border-radius:8px;height:18px;width:100%">
        <div style="background:{color};width:{pct}%;height:18px;border-radius:8px;
                    text-align:center;color:white;font-size:0.75rem;line-height:18px">
          {pct}%
        </div>
      </div>
      <div style="font-size:0.75rem;color:#888;margin-top:2px">
        Actual: {current} · Meta: {target}
      </div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Deutsche_Bahn_AG-Logo.svg/200px-Deutsche_Bahn_AG-Logo.svg.png",
    width=140,
)
st.sidebar.title("DB Vertrieb")
st.sidebar.caption("Dashboard de Transformación Digital")
st.sidebar.markdown("---")

pages = {
    "🏠  Ambiente del Problema":         "p1",
    "⚙️  Alineamiento Dinámico":         "p2",
    "🎯  Liderazgo Digital":             "p3",
    "💡  Innovación Centrada en Cliente": "p4",
    "⚡  Agilidad Operativa":             "p5",
}
selection = st.sidebar.radio("Navegación", list(pages.keys()))
page = pages[selection]

st.sidebar.markdown("---")
st.sidebar.caption(f"Período: Ene–Dic 2024  |  Actualizado: {datetime.now().strftime('%d/%m/%Y')}")

# ══════════════════════════════════════════════════════════════════════════════
#  PÁGINA 1 — AMBIENTE DEL PROBLEMA
# ══════════════════════════════════════════════════════════════════════════════
if page == "p1":
    st.title("🚄 Deutsche Bahn Vertrieb GmbH")
    st.subheader("Ambiente del Problema — Contexto Estratégico de Transformación Digital")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        kpi_card("~5.800", "Empleados en DB Vertrieb", "Sede: Frankfurt, Alemania")
    with col2:
        kpi_card("2016", "Año de reintegración IT", "De bimodal separado a unificado")
    with col3:
        kpi_card("5x", "Meta de reducción time-to-market", "Objetivo declarado por el CIO")

    st.markdown("---")

    # ── 1. Tomador de decisiones ──────────────────────────────────────────────
    with st.expander("👤  1. Tomador de Decisiones", expanded=True):
        col_a, col_b = st.columns([1, 2])
        with col_a:
            st.markdown("""
            | Rol | Responsable |
            |-----|-------------|
            | **CDO** (Chief Digital Officer) | Dirige la División Digital |
            | **CIO** (Chief Information Officer) | Lidera la función TI reintegrada |
            | **Head of Sales Processes** | Coordinación de canales y procesos |
            """)
        with col_b:
            st.markdown("""
            El principal tomador de decisiones estratégicas en DB Vertrieb es el **Chief Digital Officer (CDO)**,
            quien fue designado para encabezar la nueva División Digital creada en 2016. Su posición en el
            comité ejecutivo de la compañía le otorga autoridad directa sobre la agenda de digitalización y
            sobre el CIO, quien reporta dentro de su división.

            El CDO es responsable de liderar la transformación digital porque la alta dirección reconoció que
            la digitalización dejó de ser un tema exclusivamente tecnológico para convertirse en el núcleo
            estratégico del negocio de venta de servicios de movilidad. Su rol es garantizar que la estrategia
            IT esté completamente alineada con la estrategia corporativa de digitalización y que la experiencia
            omnicanal del cliente se convierta en una ventaja competitiva sostenible.
            """)

    # ── 2. Tarea estratégica ──────────────────────────────────────────────────
    with st.expander("🎯  2. Tarea Estratégica", expanded=True):
        st.markdown("""
        **Desafío central:**
        DB Vertrieb operaba durante 15 años con dos unidades IT completamente separadas: una tradicional
        (eficiente, orientada a costos, 2 releases/año) y otra digital (ágil, orientada al cliente, releases
        semanales). Esta estructura bimodal separada generó silos culturales, impidió una estrategia omnicanal
        y dejó a la empresa incapaz de responder a la velocidad que el mercado demandaba.

        **Transformación requerida:**
        La dirección debía ejecutar tres proyectos transformacionales simultáneos:
        - Fusionar ambas funciones IT en una División Digital unificada bajo el CDO.
        - Escalar la mentalidad ágil de la antigua Online IT a toda la organización mediante SAFe.
        - Redefinir la arquitectura organizacional alrededor de los *customer journeys* y establecer
          una unidad de gestión omnicanal.

        **Resultados estratégicos esperados:**
        - Ser 5 veces más rápidos en time-to-market para nuevas funcionalidades.
        - Lograr releases mensuales para funcionalidades interdependientes y semanales para features independientes.
        - Ofrecer la mejor experiencia de cliente en la industria de transporte de pasajeros en Alemania.
        - Habilitar una estrategia omnicanal real, con datos y sistemas integrados entre todos los canales de venta.
        """)

    # ── 3. Entorno ────────────────────────────────────────────────────────────
    with st.expander("🌍  3. Entorno", expanded=True):
        col_x, col_y = st.columns(2)
        with col_x:
            st.markdown("""
            **Presión competitiva**
            Nuevos competidores digitales emergieron en el transporte de pasajeros alemán: plataformas de
            car-sharing, autocares de larga distancia y agregadores de movilidad que buscan apropiarse de
            la interfaz con el cliente mediante plataformas digitales integradas.

            **Digitalización del sector**
            Los canales digitales pasaron de ser un complemento periférico ("la cola del perro", en palabras del CIO)
            a ser el núcleo del negocio. La penetración de smartphones y la expectativa de experiencias
            digitales fluidas transformaron la manera en que los clientes compran y usan servicios de transporte.

            **Cambios en el comportamiento del cliente**
            Los clientes esperan journeys sin fricción entre canales físicos y digitales: comprar en app,
            recoger en taquilla, recibir alertas en tiempo real. La tolerancia a bugs o retrasos en
            actualizaciones digitales es prácticamente nula.
            """)
        with col_y:
            st.markdown("""
            **Restricciones organizacionales**
            La separación estructural entre la división de e-commerce (con su IT online) y la división CIO
            (con el IT tradicional) estaba definida al nivel más alto de la jerarquía. Ambas unidades
            operaban en edificios distintos, lo que agravaba la falta de colaboración. Los silos culturales
            y metodológicos generados en 15 años de separación representaban una resistencia profunda al cambio.

            **Desafíos tecnológicos**
            La arquitectura heredada de sistemas mainframe y host systems —altamente interdependiente—
            dificultaba la modularización necesaria para implementar SAFe (releases por partes). La
            integración DevOps con el proveedor externo de operaciones IT del Grupo DB añadía una capa
            adicional de complejidad a la transformación técnica.
            """)

    st.info("📌 Navega por el menú lateral para explorar los OKRs de cada pivote estratégico de capacidades dinámicas.")

# ══════════════════════════════════════════════════════════════════════════════
#  PÁGINA 2 — ALINEAMIENTO DINÁMICO
# ══════════════════════════════════════════════════════════════════════════════
elif page == "p2":
    st.title("⚙️ Alineamiento Dinámico")
    st.caption("Capacidad de la organización para sincronizar estrategia IT, estructura y canales de venta en tiempo real.")
    st.markdown("---")

    # KPIs summary
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("65%", "Ventas por canales digitales", "Meta anual: 65%")
    with c2: kpi_card("78%", "Alineamiento estrategia IT", "Meta: 80%")
    with c3: kpi_card("12/año", "Ciclos de release", "Meta: ≥12 releases/año")
    with c4: kpi_card("46 pts", "NPS omnicanal", "Meta: 50 puntos")
    st.markdown("---")

    # OBJ-AD-01
    obj_header("OBJ-AD-01", "Integrar la estrategia IT en la estrategia corporativa de digitalización",
               "La fusión de las funciones IT en una División Digital unificada requiere que los objetivos tecnológicos "
               "y de negocio se planifiquen de forma conjunta. Sin alineamiento estratégico, los recursos se dispersan "
               "y los canales compiten en lugar de complementarse.")
    col1, col2 = st.columns(2)
    with col1:
        why_box("Mide el porcentaje de ventas realizadas a través de canales digitales vs. tradicionales. "
                "Es el indicador más directo del avance de la digitalización comercial y valida la inversión "
                "en la División Digital.")
        line_chart(d_digital_sales_share, "KR1 · Participación de Ventas Digitales (%)",
                   "% del total de ventas", color=RED, target=65, target_label="Meta anual")
    with col2:
        why_box("Mide el grado en que los planes IT reflejan las prioridades del negocio. "
                "En DB Vertrieb, la ausencia de este alineamiento fue la causa raíz de la desconexión "
                "entre el IT tradicional y los canales digitales.")
        gauge_chart(d_it_strategy_alignment[-1], "KR2 · Alineamiento IT-Estrategia (%)", 100, BLUE)
        progress_bar(d_it_strategy_alignment[-1], 80, "Meta: 80% de alineamiento IT-Estrategia Corporativa")

    st.markdown("---")

    # OBJ-AD-02
    obj_header("OBJ-AD-02", "Escalar la velocidad de entrega IT mediante ciclos de release frecuentes",
               "El CIO estableció la meta de ser 5x más rápido en time-to-market. Aumentar la frecuencia "
               "de releases es el mecanismo operativo central para lograrlo.")
    col1, col2 = st.columns(2)
    with col1:
        why_box("Los ciclos de release son el pulso de la organización ágil. El IT tradicional operaba "
                "con apenas 2-4 releases anuales; el objetivo post-reintegración es alcanzar cadencia mensual "
                "para funcionalidades interdependientes y semanal para features independientes.")
        bar_chart(d_release_cycles, "KR1 · Ciclos de Release por Año (acumulado)", "Releases acumulados", GREEN)
    with col2:
        why_box("Los proyectos transversales entre canales son el test real de la integración IT. "
                "Mientras existían silos, estos proyectos eran subóptimos y causaban tensión entre equipos.")
        line_chart(d_cross_channel_projects, "KR2 · Proyectos Omnicanal Activos",
                   "Proyectos simultáneos", color=GOLD, target=6, target_label="Meta")

    st.markdown("---")

    # OBJ-AD-03
    obj_header("OBJ-AD-03", "Mejorar la experiencia omnicanal y la satisfacción del cliente en todos los puntos de contacto",
               "La razón de ser de toda la transformación es ofrecer la mejor experiencia de cliente "
               "en la industria. El NPS omnicanal es el termómetro estratégico de ese objetivo.")
    col1, col2 = st.columns(2)
    with col1:
        why_box("El NPS omnicanal captura si el cliente percibe coherencia y fluidez entre los canales "
                "de DB Vertrieb. Una experiencia fragmentada —consecuencia directa de los silos IT previos— "
                "se refleja inmediatamente en este indicador.")
        line_chart(d_omnichannel_nps, "KR1 · NPS Omnicanal (Net Promoter Score)",
                   "Puntos NPS", color=BLUE, target=50, target_label="Meta")
    with col2:
        st.markdown("**Resumen de progreso — OBJ-AD-03**")
        progress_bar(46, 50, "NPS Omnicanal (meta: 50 pts)")
        progress_bar(65, 65, "Participación ventas digitales (meta: 65%)")
        progress_bar(78, 80, "Alineamiento IT-Estrategia (meta: 80%)")
        progress_bar(12, 12, "Releases anuales (meta: 12)")

# ══════════════════════════════════════════════════════════════════════════════
#  PÁGINA 3 — LIDERAZGO DIGITAL
# ══════════════════════════════════════════════════════════════════════════════
elif page == "p3":
    st.title("🎯 Liderazgo Digital")
    st.caption("Capacidad de la alta dirección y los mandos medios para conducir la transformación con visión, "
               "decisión y desarrollo del talento digital.")
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("8", "Iniciativas CDO activas", "Meta anual: 8")
    with c2: kpi_card("78%", "Empleados con formación digital", "Meta: 80%")
    with c3: kpi_card("72%", "Certificados en metodologías ágiles", "Meta: 75%")
    with c4: kpi_card("70%", "Adopción SAFe", "Meta: 75%")
    st.markdown("---")

    # OBJ-LD-01
    obj_header("OBJ-LD-01", "Fortalecer el liderazgo ejecutivo digital con el CDO como catalizador de la transformación",
               "La creación del rol CDO —con asiento en el comité ejecutivo— fue el movimiento estructural "
               "más importante de la reorganización 2016. Su efectividad se mide por el número y calidad "
               "de las iniciativas estratégicas que activa.")
    col1, col2 = st.columns(2)
    with col1:
        why_box("Las iniciativas del CDO son el vehículo a través del cual la visión digital se convierte en "
                "acción. Rastrear su cantidad y avance permite a la alta dirección evaluar si el liderazgo "
                "digital está produciendo resultados concretos.")
        bar_chart(d_cdo_initiatives, "KR1 · Iniciativas Estratégicas Lanzadas por CDO", "Iniciativas acumuladas", RED)
    with col2:
        why_box("El índice de madurez de liderazgo digital evalúa cuán preparados están los líderes de nivel "
                "medio y alto para tomar decisiones basadas en datos, gestionar equipos ágiles y comunicar "
                "la visión digital. Es crítico porque el CDO no puede transformar solo.")
        line_chart(d_leadership_digital_score, "KR2 · Índice de Madurez de Liderazgo Digital (%)",
                   "Score (%)", color=GOLD, target=75, target_label="Meta")

    st.markdown("---")

    # OBJ-LD-02
    obj_header("OBJ-LD-02", "Desarrollar capacidades digitales y ágiles en toda la fuerza laboral",
               "La experiencia de DB Vertrieb mostró que el mayor riesgo de la reintegración era la brecha "
               "cultural entre equipos. Invertir en formación obligatoria fue la palanca más efectiva para "
               "construir cohesión y una mentalidad común.")
    col1, col2 = st.columns(2)
    with col1:
        why_box("El porcentaje de empleados formados es el indicador de cobertura de la transformación cultural. "
                "En DB Vertrieb, hacer los cursos obligatorios generó un aumento notable en la cohesión y "
                "el compromiso —el Head of Sales Processes lo describió como generador de 'gran cohesión de equipo'.")
        line_chart(d_digital_training_pct, "KR1 · Empleados con Formación Digital Completada (%)",
                   "% del total", color=BLUE, target=80, target_label="Meta")
    with col2:
        why_box("Las certificaciones en Scrum, SAFe y metodologías ágiles no son solo títulos: son la "
                "evidencia de que el lenguaje y los métodos de trabajo se están homogeneizando entre los "
                "antiguos IT tradicional y online.")
        line_chart(d_agile_certified, "KR2 · Empleados Certificados en Metodologías Ágiles (%)",
                   "% del total", color=GREEN, target=75, target_label="Meta")

    st.markdown("---")

    # OBJ-LD-03
    obj_header("OBJ-LD-03", "Implementar SAFe como marco de escalado ágil a nivel corporativo",
               "SAFe (Scaled Agile Framework) es el mecanismo elegido por DB Vertrieb para llevar la agilidad "
               "de un equipo de 20 personas (la antigua Online IT) a una organización de cientos. "
               "Su adopción es el hito técnico-organizacional más crítico de la transformación.")
    col1, col2 = st.columns(2)
    with col1:
        why_box("La adopción de SAFe determina si la organización puede coordinar múltiples equipos ágiles "
                "hacia objetivos estratégicos comunes. Sin este marco, el escalado de la agilidad deriva "
                "en caos o en reaparición de silos.")
        line_chart(d_safe_adoption, "KR1 · Adopción de SAFe en Equipos IT (%)",
                   "% de equipos bajo SAFe", color=RED, target=75, target_label="Meta")
    with col2:
        st.markdown("**Estado actual — Liderazgo Digital**")
        progress_bar(8,  8,  "Iniciativas CDO lanzadas (meta: 8)")
        progress_bar(78, 80, "Empleados formados digitalmente (meta: 80%)")
        progress_bar(72, 75, "Certificados en ágil (meta: 75%)")
        progress_bar(70, 75, "Adopción SAFe (meta: 75%)")
        progress_bar(71, 75, "Índice madurez liderazgo (meta: 75%)")

# ══════════════════════════════════════════════════════════════════════════════
#  PÁGINA 4 — INNOVACIÓN CENTRADA EN EL CLIENTE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "p4":
    st.title("💡 Innovación Centrada en el Cliente")
    st.caption("Capacidad de generar, prototipar y escalar innovaciones que mejoran la experiencia del cliente en todos los canales.")
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("2.9M", "Usuarios activos de la app", "Meta: 3.0M")
    with c2: kpi_card("73", "CSAT score", "Meta: 75 puntos")
    with c3: kpi_card("10", "Prototipos de Innovation Lab", "Meta: 10 al año")
    with c4: kpi_card("73%", "Tickets digitales / total", "Meta: 75%")
    st.markdown("---")

    # OBJ-IC-01
    obj_header("OBJ-IC-01", "Acelerar la adopción de canales digitales de venta por parte del cliente final",
               "El crecimiento de usuarios en la app y la proporción de tickets vendidos digitalmente "
               "son los indicadores más directos de que la propuesta de valor digital de DB Vertrieb "
               "está resonando con el mercado.")
    col1, col2 = st.columns(2)
    with col1:
        why_box("El número de usuarios activos de la app refleja la penetración del canal digital más "
                "relevante. Un crecimiento sostenido valida las inversiones en UX, funcionalidad y "
                "estabilidad que el equipo Online IT priorizó históricamente.")
        line_chart(d_app_users, "KR1 · Usuarios Activos Mensuales — App DB (millones)",
                   "Millones de usuarios", color=RED, target=3.0, target_label="Meta 3.0M")
    with col2:
        why_box("El porcentaje de tickets digitales vs. totales mide el desplazamiento desde canales "
                "físicos (taquillas, máquinas) hacia los digitales. Es un KR de transformación estructural "
                "del modelo comercial de DB Vertrieb.")
        line_chart(d_digital_ticket_pct, "KR2 · Tickets Vendidos Digitalmente (%)",
                   "% del total de tickets", color=BLUE, target=75, target_label="Meta 75%")

    st.markdown("---")

    # OBJ-IC-02
    obj_header("OBJ-IC-02", "Mejorar la satisfacción del cliente mediante experiencias personalizadas y sin fricción",
               "El objetivo final de toda la transformación IT es la experiencia del cliente. "
               "El CSAT es el puente entre los cambios internos (arquitectura, procesos, metodologías) "
               "y el valor percibido externamente.")
    col1, col2 = st.columns(2)
    with col1:
        why_box("El Customer Satisfaction Score (CSAT) agrega la percepción del cliente sobre la "
                "calidad de la experiencia en los canales de DB Vertrieb. Su mejora sostenida es la "
                "evidencia de que la reintegración IT y la estrategia omnicanal están funcionando.")
        line_chart(d_csat, "KR1 · CSAT — Satisfacción del Cliente (sobre 100)",
                   "Puntos CSAT", color=GREEN, target=75, target_label="Meta 75")
    with col2:
        why_box("Los ideas generadas en los Innovation Labs miden la vitalidad del pipeline de innovación. "
                "Los labs de DB Vertrieb fueron creados específicamente para romper la mentalidad conservadora "
                "de los canales tradicionales y fomentar el pensamiento de diseño.")
        bar_chart(d_innovation_ideas, "KR2 · Ideas Generadas en Innovation Labs (acumuladas)",
                  "Ideas acumuladas", GOLD)

    st.markdown("---")

    # OBJ-IC-03
    obj_header("OBJ-IC-03", "Operacionalizar los Innovation Labs como motor de prototipos validados",
               "Los laboratorios de innovación instalados en 2016 deben producir prototipos concretos "
               "que pasen a producción. Sin esta conexión con el IT, los labs se convierten en "
               "ejercicios de ideación sin impacto real.")
    col1, col2 = st.columns(2)
    with col1:
        why_box("Los prototipos generados en los labs que superan la prueba de factibilidad IT son el "
                "indicador más concreto de que la colaboración entre business, labs y el equipo técnico "
                "está produciendo innovación aplicable.")
        line_chart(d_lab_prototypes, "KR1 · Prototipos del Innovation Lab Validados (acumulados)",
                   "Prototipos validados", color=RED, target=10, target_label="Meta 10/año")
    with col2:
        st.markdown("**Resumen de progreso — Innovación al Cliente**")
        progress_bar(2.9,  3.0, "Usuarios activos app (meta: 3.0M)")
        progress_bar(73,   75,  "CSAT score (meta: 75)")
        progress_bar(10,   10,  "Prototipos Innovation Lab (meta: 10)")
        progress_bar(35,   40,  "Ideas generadas en labs (meta: 40)")
        progress_bar(73,   75,  "Tickets digitales (meta: 75%)")

# ══════════════════════════════════════════════════════════════════════════════
#  PÁGINA 5 — AGILIDAD OPERATIVA
# ══════════════════════════════════════════════════════════════════════════════
elif page == "p5":
    st.title("⚡ Agilidad Operativa")
    st.caption("Capacidad de la organización para ejecutar cambios, lanzar productos y adaptarse a nuevas condiciones con rapidez y eficiencia.")
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("42%", "Time-to-market vs. baseline", "Meta: ≤40% (60% reducción)")
    with c2: kpi_card("5/mes", "Releases mensuales IT", "Meta: ≥6/mes")
    with c3: kpi_card("74%", "Cobertura DevOps", "Meta: 80%")
    with c4: kpi_card("60%", "Procesos automatizados", "Meta: 65%")
    st.markdown("---")

    # OBJ-AO-01
    obj_header("OBJ-AO-01", "Reducir el time-to-market en un 60% respecto a la línea base pre-transformación",
               "El CIO declaró explícitamente la meta de ser '5 veces más rápido end-to-end'. "
               "Este objetivo convierte esa aspiración en un KR medible y rastreable mensualmente.")
    col1, col2 = st.columns(2)
    with col1:
        why_box("El time-to-market mide cuánto tiempo transcurre desde que surge una idea de producto "
                "hasta que llega al cliente. Reducirlo es la promesa central de la reorganización IT "
                "de DB Vertrieb y el criterio con el que el CIO evaluará el éxito de la transformación.")
        line_chart(d_time_to_market, "KR1 · Time-to-Market (% de baseline; menor = mejor)",
                   "% del tiempo baseline", color=RED, target=40, target_label="Meta ≤40%")
    with col2:
        why_box("El número de releases mensuales es el proxy más directo de la velocidad del IT. "
                "El objetivo es alcanzar releases mensuales para funcionalidades complejas y semanales "
                "para features independientes, según el roadmap del CIO.")
        bar_chart(d_releases_per_month, "KR2 · Releases IT por Mes",
                  "Releases / mes", GREEN)

    st.markdown("---")

    # OBJ-AO-02
    obj_header("OBJ-AO-02", "Implementar DevOps y prácticas de integración continua en toda la función IT reintegrada",
               "DevOps es el puente entre el equipo de desarrollo interno de DB Vertrieb y el proveedor "
               "externo de operaciones del Grupo DB. Sin esta integración, la agilidad del desarrollo "
               "queda bloqueada en la fase de despliegue.")
    col1, col2 = st.columns(2)
    with col1:
        why_box("La cobertura DevOps mide qué porcentaje de los equipos IT trabaja bajo prácticas de "
                "integración y entrega continua. Es un prerequisito técnico para cumplir los objetivos "
                "de frecuencia de releases y reducción del time-to-market.")
        line_chart(d_devops_coverage, "KR1 · Cobertura DevOps en Equipos IT (%)",
                   "% de equipos con DevOps", color=BLUE, target=80, target_label="Meta 80%")
    with col2:
        why_box("Los equipos Scrum formales —en contraste con la organización Scrum-like anterior— "
                "son la unidad básica de ejecución ágil en SAFe. Su número refleja la velocidad de "
                "institucionalización del nuevo modelo operativo.")
        line_chart(d_scrum_teams, "KR2 · Equipos Scrum Formales Activos",
                   "Número de equipos", color=GOLD, target=12, target_label="Meta 12")

    st.markdown("---")

    # OBJ-AO-03
    obj_header("OBJ-AO-03", "Aumentar la automatización de procesos para liberar capacidad operativa",
               "La automatización de procesos repetitivos en IT y en los canales de venta libera capacidad "
               "para la innovación. Es la palanca de productividad que permite a DB Vertrieb hacer más "
               "con los mismos recursos durante el período de transición.")
    col1, col2 = st.columns(2)
    with col1:
        why_box("El porcentaje de procesos automatizados mide cuántos flujos de trabajo que antes "
                "requerían intervención manual ahora se ejecutan automáticamente. Reduce errores, "
                "acelera entregas y disminuye la carga operativa de los equipos en transformación.")
        line_chart(d_process_automation, "KR1 · Procesos Operativos Automatizados (%)",
                   "% de procesos automatizados", color=GREEN, target=65, target_label="Meta 65%")
    with col2:
        st.markdown("**Resumen de progreso — Agilidad Operativa**")
        progress_bar(58,  40,  "Time-to-market vs baseline (meta: ≤40%)") # current=58 out of 100 (still reducing)
        progress_bar(5,   6,   "Releases por mes (meta: ≥6)")
        progress_bar(74,  80,  "Cobertura DevOps (meta: 80%)")
        progress_bar(12,  12,  "Equipos Scrum activos (meta: 12)")
        progress_bar(60,  65,  "Procesos automatizados (meta: 65%)")

    st.markdown("---")
    st.markdown("""
    <div style="background:#1a1a2e;color:#e0e0e0;padding:16px 20px;border-radius:10px;
                border-left:4px solid #e63946;font-size:0.85rem">
    <strong>📊 Estado consolidado de la transformación digital — DB Vertrieb</strong><br>
    El dashboard refleja el progreso a Diciembre 2024. Los cuatro pivotes de capacidades dinámicas muestran avance
    sostenido. Los mayores desafíos persisten en la adopción completa de SAFe, la cobertura DevOps y la reducción
    del time-to-market —consistente con las lecciones aprendidas del caso, donde la reintegración tomó más tiempo
    del esperado en producir resultados tangibles. La alta dirección debe priorizar estas áreas en el próximo ciclo.
    </div>
    """, unsafe_allow_html=True)
