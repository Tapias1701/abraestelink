import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Gana para ver", layout="wide")

# ─────────────────────────────────────────
# GIF — CAMBIA AQUÍ EL LINK
# ─────────────────────────────────────────
GIF_MENSAJE = "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3dGFzMHQ1OTB3ZGdqYW9uMWVpcXFibXdlZmZxNXVvdzJzMjdmZ212NSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/z9QSZXAxx3iOQz6FeG/giphy.gif"

# --- Estado ---
st.session_state.setdefault("pagina", "juego")
st.session_state.setdefault("gano", False)

# Detectar canasta via query param
if st.query_params.get("gano") == "1":
    st.session_state.gano = True

# ─────────────────────────────────────────
# CSS global
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #0a0a0a !important;
}
[data-testid="stMainBlockContainer"] { padding-top: 0 !important; }
button[data-testid="stBaseButton-primary"] {
    background-color: #ff6b00 !important;
    color: white !important;
    font-size: 20px !important;
    font-weight: 900 !important;
    border-radius: 14px !important;
    height: 64px !important;
    border: none !important;
    letter-spacing: 3px !important;
    animation: glow 0.8s infinite alternate;
}
@keyframes glow {
    from { box-shadow: 0 0 12px #ff6b00aa; }
    to   { box-shadow: 0 0 32px #ff6b00ff; }
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# PÁGINA 1 — El juego
# ─────────────────────────────────────────
if st.session_state.pagina == "juego":

    JUEGO = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body {
    background:#0a0a0a; width:100%; height:100vh;
    display:flex; flex-direction:column; align-items:center;
    overflow:hidden; font-family:'Bebas Neue','Arial Black',sans-serif;
  }
  #titulo {
    color:#fff; font-size:28px; letter-spacing:3px;
    text-transform:uppercase; text-align:center;
    margin-top:20px; margin-bottom:4px; line-height:1.2; padding:0 16px;
  }
  #sub { color:#ff6b00; font-size:13px; font-family:Arial,sans-serif; margin-bottom:8px; text-align:center; }
  #scorebar {
    display:flex; justify-content:space-between; width:420px;
    color:#888; font-size:13px; font-family:Arial,sans-serif; margin-bottom:5px; padding:0 4px;
  }
  #scorebar b { color:#ff6b00; }
  canvas { cursor:crosshair; border-radius:10px; display:block; }
  #win-text {
    display:none; color:#ff6b00; font-size:44px; letter-spacing:4px;
    margin-top:14px; text-align:center;
    animation:parpadeo 0.5s infinite alternate;
  }
  #instruccion {
    display:none; color:#aaa; font-size:15px; font-family:Arial,sans-serif;
    margin-top:6px; text-align:center;
  }
  @keyframes parpadeo { from{opacity:1} to{opacity:0.3} }
</style>
</head>
<body>
<div id="titulo">si ganas desbloqueas<br>el siguiente mensaje</div>
<div id="sub">Haz clic para lanzar — mete 1 canasta</div>
<div id="scorebar">
  <span>Canastas: <b id="s-score">0</b></span>
  <span>Lanzamientos: <b id="s-throws">0</b></span>
</div>
<canvas id="c" width="420" height="370"></canvas>
<div id="win-text">CANASTA!</div>
<div id="instruccion">Cargando...</div>

<script>
const canvas=document.getElementById('c'), ctx=canvas.getContext('2d');
const W=canvas.width, H=canvas.height;
let balls=[], score=0, throws=0, won=false;
const hoop={x:W/2,y:100,rimW:58,rimH:8,netH:52};

function drawHoop(){
  ctx.fillStyle='#ffffff15'; ctx.fillRect(hoop.x+hoop.rimW/2+3,hoop.y-52,8,56);
  ctx.fillStyle='#ffffff20'; ctx.fillRect(hoop.x+hoop.rimW/2-16,hoop.y-56,52,36);
  ctx.strokeStyle='#ff6b00'; ctx.lineWidth=5;
  ctx.beginPath(); ctx.ellipse(hoop.x,hoop.y,hoop.rimW/2,hoop.rimH/2,0,0,Math.PI*2); ctx.stroke();
  ctx.strokeStyle='#ffffff50'; ctx.lineWidth=1.5;
  for(let i=0;i<=8;i++){
    const nx=(hoop.x-hoop.rimW/2)+(hoop.rimW/8)*i, bx=hoop.x+(nx-hoop.x)*0.38;
    ctx.beginPath(); ctx.moveTo(nx,hoop.y+hoop.rimH/2); ctx.lineTo(bx,hoop.y+hoop.netH); ctx.stroke();
  }
  ctx.strokeStyle='#ffffff28';
  for(let r=1;r<=4;r++){
    const t=r/4, ly=hoop.y+hoop.rimH/2+hoop.netH*t*0.88, lw=(hoop.rimW/2)*(1-t*0.52);
    ctx.beginPath(); ctx.moveTo(hoop.x-lw,ly); ctx.lineTo(hoop.x+lw,ly); ctx.stroke();
  }
}

function drawShooter(){
  const sx=W/2,sy=H-42,r=22;
  const g=ctx.createRadialGradient(sx,sy,2,sx,sy,r+12);
  g.addColorStop(0,'#ff6b0066'); g.addColorStop(1,'transparent');
  ctx.beginPath(); ctx.arc(sx,sy,r+12,0,Math.PI*2); ctx.fillStyle=g; ctx.fill();
  ctx.beginPath(); ctx.arc(sx,sy,r,0,Math.PI*2); ctx.fillStyle='#e85d04'; ctx.fill();
  ctx.strokeStyle='#1a0a00'; ctx.lineWidth=1.5; ctx.stroke();
  ctx.strokeStyle='#00000055'; ctx.lineWidth=1.5;
  ctx.beginPath(); ctx.arc(sx,sy,r,0.2,Math.PI-0.2); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(sx-r,sy); ctx.lineTo(sx+r,sy); ctx.stroke();
}

function drawBall(b){
  ctx.save(); ctx.translate(b.x,b.y); ctx.rotate(b.rot);
  ctx.beginPath(); ctx.arc(0,0,b.r,0,Math.PI*2); ctx.fillStyle='#e85d04'; ctx.fill();
  ctx.strokeStyle='#00000055'; ctx.lineWidth=1.5;
  ctx.beginPath(); ctx.arc(0,0,b.r,0.2,Math.PI-0.2); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(-b.r,0); ctx.lineTo(b.r,0); ctx.stroke();
  ctx.restore();
}

function checkScore(b){
  const rl=hoop.x-hoop.rimW/2+b.r*0.45, rr=hoop.x+hoop.rimW/2-b.r*0.45;
  if(!b.scored&&b.vy>0&&b.y>=hoop.y&&b.y<=hoop.y+24&&b.x>rl&&b.x<rr){
    b.scored=true; score++;
    document.getElementById('s-score').textContent=score;
    if(!won){
      won=true;
      document.getElementById('win-text').style.display='block';
      document.getElementById('instruccion').style.display='block';
      
      setTimeout(() => {
          try {
              // Intento 1: Actualizar la URL padre y recargar
              const url = new URL(window.parent.location.href);
              url.searchParams.set('gano', '1');
              window.parent.history.pushState({}, '', url.toString());
              window.parent.location.reload();
          } catch(e) {
              // Intento 2: Redirección forzada al nivel superior (por si el iframe está muy restringido)
              window.top.location.href = "?gano=1";
          }
      }, 1500);
    }
  }
  [hoop.x-hoop.rimW/2, hoop.x+hoop.rimW/2].forEach(rx=>{
    const d=Math.sqrt((b.x-rx)**2+(b.y-hoop.y)**2);
    if(d<b.r+6){
      const nx=(b.x-rx)/d, ny=(b.y-hoop.y)/d, dot=b.vx*nx+b.vy*ny;
      b.vx=(b.vx-2*dot*nx)*0.55; b.vy=(b.vy-2*dot*ny)*0.55;
      b.x=rx+nx*(b.r+7); b.y=hoop.y+ny*(b.r+7);
    }
  });
}

function update(){
  balls.forEach(b=>{
    b.vy+=0.45; b.x+=b.vx; b.y+=b.vy; b.rot+=b.rotSpeed;
    checkScore(b); if(b.y>H+60) b.dead=true;
  });
  balls=balls.filter(b=>!b.dead);
}

function draw(){
  ctx.clearRect(0,0,W,H); ctx.fillStyle='#0a0a0a'; ctx.fillRect(0,0,W,H);
  ctx.strokeStyle='#ffffff08'; ctx.lineWidth=1;
  ctx.beginPath(); ctx.moveTo(40,H-80); ctx.lineTo(W-40,H-80); ctx.stroke();
  drawHoop(); balls.forEach(drawBall);
  if(!won) drawShooter();
  if(won){ ctx.fillStyle='rgba(0,0,0,0.45)'; ctx.fillRect(0,0,W,H); }
}

function shoot(mx,my){
  if(won) return;
  throws++; document.getElementById('s-throws').textContent=throws;
  const dx=mx-W/2, dy=my-(H-42), dist=Math.sqrt(dx*dx+dy*dy);
  const speed=Math.min(dist/9,21);
  balls.push({x:W/2,y:H-42,vx:(dx/dist)*speed,vy:(dy/dist)*speed,
    r:22,rot:0,rotSpeed:(Math.random()-0.5)*0.28,scored:false,dead:false});
}

canvas.addEventListener('click',e=>{
  const r=canvas.getBoundingClientRect(); shoot(e.clientX-r.left,e.clientY-r.top);
});

function loop(){ update(); draw(); requestAnimationFrame(loop); }
loop();
</script>
</body>
</html>"""

    components.html(JUEGO, height=620, scrolling=False)

    col = st.columns([1, 2, 1])[1]
    with col:
        if st.session_state.gano:
            if st.button("DESBLOQUEAR MENSAJE", type="primary", use_container_width=True):
                st.session_state.pagina = "mensaje"
                st.query_params.clear()
                st.rerun()
        else:
            st.button("BLOQUEADO — mete la canasta primero", disabled=True, use_container_width=True)


# ─────────────────────────────────────────
# PÁGINA 2 — El mensaje
# ─────────────────────────────────────────
elif st.session_state.pagina == "mensaje":

    st.markdown(f"""
<style>
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
    background: #0a0a0a !important;
}}
.mensaje-titulo {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 50px;
    color: #ffffff;
    text-align: center;
    line-height: 1.15;
    margin: 60px auto 28px auto;
    max-width: 700px;
    letter-spacing: 2px;
}}
.gif-wrap {{ display:flex; justify-content:center; margin:0 auto; }}
.gif-wrap img {{ border-radius:18px; max-width:460px; width:90%; }}
</style>
<div class='mensaje-titulo'>
    Como te dije, linda sonrisa y lindo feed,<br>aparte dificil de llamar la atencion, mejor aun
</div>
<div class='gif-wrap'>
    <img src='{GIF_MENSAJE}' alt='gif'>
</div>
""", unsafe_allow_html=True)