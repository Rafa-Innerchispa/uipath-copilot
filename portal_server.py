import os
import json
import uuid
import hashlib
import logging
from fastapi import FastAPI, Form, Cookie, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
import pymongo

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI(title="Ralphi IA unique portal")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORTAL_DIR = os.path.join(BASE_DIR, "portal")
SERVICES_JSON = os.path.join(PORTAL_DIR, "services.json")

ACTIVE_SESSIONS = {}

def get_db():
    try:
        # Use hackathon_autopilot to share the users collection
        client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        return client["hackathon_autopilot"]
    except Exception as e:
        logging.error(f"Error connecting to MongoDB: {e}")
        return None

async def get_current_user(session_token: str = Cookie(None)):
    if not session_token:
        return None
    db = get_db()
    if db is not None:
        try:
            sess = db.sessions.find_one({"session_token": session_token})
            if sess:
                return sess["username"]
        except Exception as e:
            logging.error(f"Error verifying session: {e}")
    return None

@app.get("/", response_class=HTMLResponse)
async def get_portal(user: str = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login")
    
    index_path = os.path.join(PORTAL_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Inject username
            content = content.replace("<h1>Ralphi IA v2.0</h1>", f"<h1>Ralphi IA v2.0 <span style='font-size:1rem;font-weight:normal;color:#8b5cf6;'>(Usuario: {user})</span></h1>")
            response = HTMLResponse(content=content)
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            return response
    return HTMLResponse(content="<h1>index.html not found</h1>", status_code=404)

@app.get("/login", response_class=HTMLResponse)
async def get_login_page(user: str = Depends(get_current_user)):
    if user:
        return RedirectResponse(url="/")
    
    login_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Iniciar Sesión — Ralphi IA</title>
      <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
      <style>
        :root {
          --bg: #05070a;
          --surface: rgba(255, 255, 255, 0.03);
          --border: rgba(255, 255, 255, 0.08);
          --accent: #8b5cf6;
          --text: #f1f5f9;
          --muted: #94a3b8;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
          font-family: 'DM Sans', sans-serif;
          background-color: var(--bg);
          color: var(--text);
          display: flex;
          align-items: center;
          justify-content: center;
          min-height: 100vh;
          overflow: hidden;
          position: relative;
        }
        body::before {
          content: "";
          position: absolute;
          width: 300px;
          height: 300px;
          background: radial-gradient(circle, rgba(139, 92, 246, 0.25) 0%, transparent 70%);
          top: 10%;
          left: 10%;
          filter: blur(40px);
        }
        body::after {
          content: "";
          position: absolute;
          width: 300px;
          height: 300px;
          background: radial-gradient(circle, rgba(59, 130, 246, 0.2) 0%, transparent 70%);
          bottom: 10%;
          right: 10%;
          filter: blur(40px);
        }
        .container {
          background: var(--surface);
          border: 1px solid var(--border);
          padding: 2.5rem;
          border-radius: 20px;
          width: 100%;
          max-width: 420px;
          backdrop-filter: blur(20px);
          -webkit-backdrop-filter: blur(20px);
          box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
          position: relative;
          z-index: 10;
        }
        h2 { font-size: 1.8rem; margin-bottom: 0.5rem; font-weight: 700; text-align: center; }
        p.subtitle { color: var(--muted); text-align: center; font-size: 0.88rem; margin-bottom: 2rem; }
        .form-group { margin-bottom: 1.25rem; display: flex; flex-direction: column; gap: 0.4rem; }
        label { font-size: 0.82rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 0.4rem; }
        input {
          width: 100%;
          background: rgba(255, 255, 255, 0.04);
          border: 1px solid var(--border);
          border-radius: 10px;
          padding: 0.8rem 1rem;
          color: #fff;
          font-size: 0.95rem;
          outline: none;
          transition: border-color 0.3s;
        }
        input:focus { border-color: var(--accent); }
        button {
          width: 100%;
          background: var(--accent);
          color: #fff;
          border: none;
          padding: 0.9rem;
          border-radius: 10px;
          font-weight: 700;
          font-size: 1rem;
          cursor: pointer;
          transition: transform 0.2s, box-shadow 0.2s;
          margin-top: 0.5rem;
          box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
        }
        button:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5); }
        .toggle-mode { text-align: center; margin-top: 1.5rem; font-size: 0.88rem; color: var(--muted); }
        .toggle-mode a { color: var(--accent); text-decoration: none; font-weight: 600; }
        .toggle-mode a:hover { text-decoration: underline; }
        .hidden { display: none !important; }
      </style>
    </head>
    <body>
      <div class="container" id="login-box">
        <h2>Iniciar Sesión</h2>
        <p class="subtitle">Accede al ecosistema multiempresa Ralphi IA</p>
        <form action="/api/auth/login" method="POST">
          <div class="form-group">
            <label for="user">Usuario</label>
            <input type="text" id="user" name="username" required placeholder="Ingresa tu usuario">
          </div>
          <div class="form-group">
            <label for="pass">Contraseña</label>
            <input type="password" id="pass" name="password" required placeholder="Ingresa tu contraseña">
          </div>
          <button type="submit">Entrar al Ecosistema</button>
        </form>
        <div class="toggle-mode">
          ¿No tienes cuenta? <a href="#" onclick="toggleRegister(true)">Crear cuenta</a>
        </div>
      </div>

      <div class="container hidden" id="register-box">
        <h2>Crear Usuario</h2>
        <p class="subtitle">Registra una nueva cuenta en el servidor</p>
        <form action="/api/auth/register" method="POST">
          <div class="form-group">
            <label for="reg-user">Usuario</label>
            <input type="text" id="reg-user" name="username" required placeholder="Crea un nombre de usuario">
          </div>
          <div class="form-group">
            <label for="reg-pass">Contraseña</label>
            <input type="password" id="reg-pass" name="password" required placeholder="Crea una contraseña segura">
          </div>
          <button type="submit" style="background:#3b82f6; box-shadow:0 4px 15px rgba(59, 130, 246, 0.4);">Registrarse & Entrar</button>
        </form>
        <div class="toggle-mode">
          ¿Ya tienes cuenta? <a href="#" onclick="toggleRegister(false)">Iniciar Sesión</a>
        </div>
      </div>

      <script>
        function toggleRegister(showRegister) {
          if (showRegister) {
            document.getElementById('login-box').classList.add('hidden');
            document.getElementById('register-box').classList.remove('hidden');
          } else {
            document.getElementById('register-box').classList.add('hidden');
            document.getElementById('login-box').classList.remove('hidden');
          }
        }
      </script>
    </body>
    </html>
    """
    return HTMLResponse(content=login_html)

@app.post("/api/auth/login")
async def login(username: str = Form(...), password: str = Form(...)):
    db = get_db()
    if db is not None:
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            user = db.users.find_one({"username": username, "password_hash": password_hash})
            if user:
                session_token = str(uuid.uuid4())
                db.sessions.update_one(
                    {"username": username},
                    {"$set": {"session_token": session_token}},
                    upsert=True
                )
                response = RedirectResponse(url="/", status_code=303)
                response.set_cookie(key="session_token", value=session_token, httponly=True)
                return response
            else:
                return HTMLResponse(content="<h3>Usuario o contraseña incorrectos. <a href='/login'>Intentar de nuevo</a></h3>", status_code=401)
        except Exception as e:
            return HTMLResponse(content=f"<h3>Error: {e}</h3>", status_code=500)
    return HTMLResponse(content="<h3>Sin conexión a DB.</h3>", status_code=500)

@app.post("/api/auth/register")
async def register(username: str = Form(...), password: str = Form(...)):
    db = get_db()
    if db is not None:
        try:
            existing = db.users.find_one({"username": username})
            if existing:
                return HTMLResponse(content="<h3>El usuario ya existe. <a href='/login'>Intentar de nuevo</a></h3>", status_code=400)
            
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            new_user = {
                "username": username,
                "password_hash": password_hash,
                "role": "user"
            }
            db.users.insert_one(new_user)
            
            session_token = str(uuid.uuid4())
            db.sessions.update_one(
                {"username": username},
                {"$set": {"session_token": session_token}},
                upsert=True
            )
            response = RedirectResponse(url="/", status_code=303)
            response.set_cookie(key="session_token", value=session_token, httponly=True)
            return response
        except Exception as e:
            return HTMLResponse(content=f"<h3>Error: {e}</h3>", status_code=500)
    return HTMLResponse(content="<h3>Sin conexión a DB.</h3>", status_code=500)

@app.post("/api/auth/logout")
async def logout(session_token: str = Cookie(None)):
    db = get_db()
    if db is not None and session_token:
        try:
            db.sessions.delete_one({"session_token": session_token})
        except Exception as e:
            logging.error(f"Error deleting session: {e}")
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="session_token")
    return response

@app.get("/services.json")
async def get_services(user: str = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="No autorizado")
    if os.path.exists(SERVICES_JSON):
        with open(SERVICES_JSON, "r", encoding="utf-8") as f:
            response = JSONResponse(content=json.load(f))
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            return response
    response = JSONResponse(content={"featured": [], "services": []})
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response

@app.get("/assets/{filename}")
async def get_assets(filename: str):
    from fastapi.responses import FileResponse
    asset_path = os.path.join(PORTAL_DIR, "assets", filename)
    if os.path.exists(asset_path):
        return FileResponse(asset_path)
    return HTMLResponse(content="Not Found", status_code=404)

@app.get("/api/users")
async def get_users_list(user: str = Depends(get_current_user)):
    if not user:
         raise HTTPException(status_code=401, detail="No autorizado")
    db = get_db()
    usernames = []
    if db is not None:
        try:
            users = db.users.find({}, {"username": 1, "_id": 0})
            usernames = [u["username"] for u in users]
        except Exception as e:
            logging.error(f"Error querying users: {e}")
    return JSONResponse(content=usernames)
