import streamlit as st
import random

st.set_page_config(page_title="Apostemos a ver", page_icon="", layout="wide")

# --- Estados ---
st.session_state.setdefault("pagina", "inicio")
st.session_state.setdefault("numero", None)
st.session_state.setdefault("no_clicks", 0)
st.session_state.setdefault("respondio_si", False)

# ─────────────────────────────────────────
# 🎨 GIFs — CAMBIA AQUÍ LOS LINKS
# ─────────────────────────────────────────
GIF_PAGINA_1 = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExc3Jma2NtcXZlMnA0cDR1eHVqdTVqdG1xZ25odzFtcjM0dnJtYXFpaiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/R3cDiWHJ9pvghwCasO/giphy.gif"   # Página 1: "Piensa en un número"
GIF_PAGINA_2 = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN2d2MTZncDRlanl2aTh0eGtubzFiMmhleThvMmFhc3RiYTlsd3M5cSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/RM5m5NoNRtuYCj1szf/giphy.gif"   # Página 2: "La apuesta"
GIF_PAGINA_3 = "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3NTJhY2RjbW5mOG5sdzVoZHFpc2cwaGRzMzJ5OWxmM2c5OHd5c3hnbyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Yo3K8mThmCROx4xGeF/giphy.gif"   # Página 3: "GANEEEEEE"

# ─────────────────────────────────────────
# CSS base
# ─────────────────────────────────────────
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: #fff0f6;
}
h1, h2, h3 {
    text-align: center;
}
.card {
    background: #ffffff;
    border-radius: 20px;
    padding: 36px 28px;
    max-width: 600px;
    margin: 0 auto;
    box-shadow: 0 4px 24px rgba(255,75,75,0.10);
    text-align: center;
}
.big-number {
    font-size: 120px;
    font-weight: 900;
    color: #FF4B4B;
    text-align: center;
    line-height: 1;
}
.frase-final {
    font-size: 18px;
    color: #555;
    text-align: center;
    margin-top: 24px;
    font-style: italic;
    max-width: 580px;
    margin-left: auto;
    margin-right: auto;
}
.gif-container {
    display: flex;
    justify-content: center;
    margin: 20px auto;
}
.gif-container img {
    border-radius: 16px;
    max-width: 420px;
    width: 90%;
}
/* Botón SÍ primario */
button[data-testid="stBaseButton-primary"] {
    background-color: #FF4B4B !important;
    color: white !important;
    font-size: 28px !important;
    font-weight: 900 !important;
    border-radius: 14px !important;
    height: 70px !important;
    border: none !important;
}
/* Botón NO secundario */
button[data-testid="stBaseButton-secondary"] {
    font-size: 20px !important;
    border-radius: 14px !important;
    height: 55px !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# PÁGINA 1 — Inicio: escribe el número
# ─────────────────────────────────────────
if st.session_state.pagina == "inicio":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div class='card'>
        <h2>Soy adivino</h2>
        <p style='font-size:20px; color:#333;'>
            Piensa en un número del <strong>1 al 10</strong> y escríbelo abajo.<br>
            A ver…
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 🖼️ GIF PÁGINA 1
    st.markdown(f"""
    <div class='gif-container'>
        <img src='{GIF_PAGINA_1}' alt='gif'>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    with col:
        numero = st.number_input("Tu número:", min_value=1, max_value=10, step=1, value=None, placeholder="Escribe del 1 al 10")
        if st.button("Escribe", type="primary", use_container_width=True):
            if numero is not None:
                st.session_state.numero = int(numero)
                st.session_state.pagina = "adivino"
                st.rerun()
            else:
                st.warning("Escribe un número")


# ─────────────────────────────────────────
# PÁGINA 2 — Apuesta del juego
# ─────────────────────────────────────────
elif st.session_state.pagina == "adivino":

    no_clicks = st.session_state.no_clicks

    rx = random.randint(5, 78)
    ry = random.randint(8, 78)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class='card'>
        <h2>A todo el mundo le gustan las apuestas</h2>
        <p style='font-size:22px; color:#333; margin-top:10px;'>
            Si adivino el número en el que estabas pensando…<br>
            <strong>me debes una salida a comer. Pero si no lo adivino, no te vuelvo a hablar nunca en la vida jajaja ¿Va?</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 🖼️ GIF PÁGINA 2
    st.markdown(f"""
    <div class='gif-container'>
        <img src='{GIF_PAGINA_2}' alt='gif'>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if no_clicks >= 5:
        st.markdown("""
        <div style='text-align:center; font-size:22px; color:#FF4B4B; font-weight:700; margin-bottom:18px;'>
            No hay más opción, te tocó decir que sí 😎
        </div>
        """, unsafe_allow_html=True)
        col = st.columns([1, 2, 1])[1]
        with col:
            if st.button("¡SÍ! ", type="primary", use_container_width=True):
                st.session_state.respondio_si = True
                st.session_state.pagina = "resultado"
                st.rerun()

    else:
        st.markdown(f"""
        <style>
        button[data-testid="stBaseButton-secondary"] {{
            position: fixed !important;
            left: {rx}vw !important;
            top: {ry}vh !important;
            z-index: 99999 !important;
            width: 130px !important;
            transition: none !important;
        }}
        </style>
        """, unsafe_allow_html=True)

        col = st.columns([1, 2, 1])[1]
        with col:
            if st.button("¡SÍ!", type="primary", use_container_width=True):
                st.session_state.respondio_si = True
                st.session_state.pagina = "resultado"
                st.rerun()

        if st.button("No", type="secondary"):
            st.session_state.no_clicks += 1
            st.rerun()


# ─────────────────────────────────────────
# PÁGINA 3 — Resultado: GANÉ 🎉
# ─────────────────────────────────────────
elif st.session_state.pagina == "resultado":
    st.balloons()
    st.snow()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align:center;'>
        <div style='font-size:52px; font-weight:900; color:#FF4B4B;'>GANEEEEEEEE HPPTAAA</div>
        <div style='font-size:28px; margin-top:12px; color:#333;'>
            Este sábado paso por ti
        </div>
        <div class='big-number' style='margin: 28px 0;'>{st.session_state.numero}</div>
    </div>
    """, unsafe_allow_html=True)

    # 🖼️ GIF PÁGINA 3
    st.markdown(f"""
    <div class='gif-container'>
        <img src='{GIF_PAGINA_3}' alt='gif'>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='frase-final'>
        Sé que nadie te había hecho algo así,<br>
        y cualquiera que lo vea se le hará raro<br>
        pero se les hace raro porque no les da para hacerlo.
    </div>
    """, unsafe_allow_html=True)
