# 🚄 Deutsche Bahn Vertrieb — Dashboard de Transformación Digital (OKRs)

Dashboard ejecutivo de monitoreo estratégico basado en OKRs para el caso de transformación digital de **Deutsche Bahn Vertrieb GmbH**, desarrollado en Streamlit.

---

## 📋 Descripción

Este dashboard permite a la alta gerencia monitorear el progreso de la transformación digital de DB Vertrieb,
estructurado alrededor de cuatro pivotes de **capacidades dinámicas**:

| Pivote | Descripción |
|--------|-------------|
| ⚙️ Alineamiento Dinámico | Sincronización entre estrategia IT, estructura y canales de venta |
| 🎯 Liderazgo Digital | Conducción ejecutiva, formación y adopción de SAFe |
| 💡 Innovación Centrada en el Cliente | Adopción digital, Innovation Labs y CSAT |
| ⚡ Agilidad Operativa | Time-to-market, DevOps, Scrum y automatización |

---

## 🗂️ Estructura del repositorio

```
├── app.py            # Aplicación principal Streamlit (datos simulados incluidos)
├── requirements.txt  # Dependencias Python
└── README.md         # Este archivo
```

> ⚠️ **No se requieren archivos CSV, bases de datos ni archivos externos.**
> Toda la simulación de datos está incorporada directamente en `app.py`.

---

## 🚀 Instalación y ejecución local

```bash
# 1. Clona el repositorio
git clone https://github.com/tu-usuario/db-vertrieb-okr-dashboard.git
cd db-vertrieb-okr-dashboard

# 2. Crea un entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Ejecuta la app
streamlit run app.py
```

La app se abrirá automáticamente en `http://localhost:8501`

---

## ☁️ Despliegue en Streamlit Community Cloud

1. Sube los tres archivos a un repositorio de GitHub (público o privado).
2. Ve a [share.streamlit.io](https://share.streamlit.io) e inicia sesión con GitHub.
3. Haz clic en **"New app"** y selecciona tu repositorio.
4. Configura:
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Haz clic en **"Deploy"** — ¡listo!

---

## 📊 Páginas del dashboard

| Página | Contenido |
|--------|-----------|
| 🏠 Ambiente del Problema | Contexto estratégico: tomador de decisiones, tarea estratégica y entorno |
| ⚙️ Alineamiento Dinámico | 3 objetivos, 6 KRs, gráficos de tendencia y gauges |
| 🎯 Liderazgo Digital | 3 objetivos, 6 KRs, adopción SAFe, formación ágil |
| 💡 Innovación Centrada en Cliente | 3 objetivos, 6 KRs, app users, CSAT, prototipos |
| ⚡ Agilidad Operativa | 3 objetivos, 5 KRs, time-to-market, DevOps, automatización |

---

## 📚 Caso de referencia

> Fortmann, L., Haffke, I., & Benlian, A. (2019).
> *Navigating Through Digital Transformation Using Bimodal IT: How Changing IT Organizations
> Facilitates the Digital Transformation Journey at Deutsche Bahn Vertrieb GmbH.*
> In N. Urbach & M. Röglinger (Eds.), *Digitalization Cases*. Springer.

---

## 🛠️ Stack tecnológico

- **Streamlit** — Framework de dashboards en Python
- **Pandas** — Manipulación de datos
- **Plotly** — Visualizaciones interactivas (líneas, barras, gauges)

---

*Dashboard desarrollado como herramienta académica de monitoreo estratégico.*
