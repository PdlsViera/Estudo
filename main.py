from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from PIL import Image
import io

# Criação do app e configuração de sessão
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="segredo123")  # Altere por uma chave mais segura

templates = Jinja2Templates(directory="templates")

# --- Tela de login ---
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# --- Valida login ---
@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == "cliente" and password == "senha123":
        request.session["usuario"] = username
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "erro": "Usuário ou senha inválidos"})

# --- Página principal protegida ---
@app.get("/", response_class=HTMLResponse)
def formulario(request: Request):
    if "usuario" not in request.session:
        return RedirectResponse("/login")
    return templates.TemplateResponse("index.html", {"request": request})

# --- Processa imagem (também protegido) ---
@app.post("/processar")
async def processar_imagem(
    request: Request,
    imagem: UploadFile = File(...),
    acao: str = Form(...)
):
    if "usuario" not in request.session:
        return RedirectResponse("/login")

    conteudo = await imagem.read()

    try:
        img = Image.open(io.BytesIO(conteudo))
    except Exception as e:
        return {"erro": f"Imagem inválida: {str(e)}"}

    # Exemplo de processamento: redimensionar
    img = img.resize((200, 200))

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)

    if acao == "visualizar":
        return StreamingResponse(
            buffer,
            media_type="image/jpeg",
            headers={"Content-Disposition": "inline; filename=imagem_visualizada.jpg"}
        )
    else:  # "baixar"
        return StreamingResponse(
            buffer,
            media_type="image/jpeg",
            headers={"Content-Disposition": "attachment; filename=imagem_baixada.jpg"}
        )

# --- Logout ---
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login")
