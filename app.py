import re
import uuid
from urllib.parse import unquote, quote
from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# ---------------------- CATÁLOGO (exemplo) --------------------------- #
CATALOGO = {
    # "codigo": {"nome": "Nome do produto", "preco": 0.00}
    "89": {"nome": "Prato", "preco": 95.90},
    "50": {"nome": "Camiseta", "preco": 20.55},
    # adicione aqui: "COD": {"nome": "Produto", "preco": 12.34}
}

# ---------------------- STORE COMPARTILHADO (persistência) ----------------- #
# Em produção, você pode usar Redis ou banco de dados
CART_STORE = {}

def _normalize_key(k: str) -> str:
    return k.lower().replace("+", "").replace(" ", "")

def _get_param(args, accepted_names: set):
    for k in args.keys():
        if _normalize_key(k) in accepted_names:
            return args.get(k), k
    return None, None

def _to_int(val, default=1):
    if val is None:
        return default
    try:
        return int(val)
    except Exception:
        m = re.search(r"-?\d+", str(val))
        if m:
            try:
                return int(m.group(0))
            except Exception:
                return default
        return default

def _add_item(carrinho, nome: str, preco, qtd=1):
    if not nome:
        return
    try:
        preco = float(str(preco).replace(",", "."))
    except Exception:
        return
    try:
        qtd = int(qtd)
    except Exception:
        qtd = 1

    if nome in carrinho:
        carrinho[nome]["qtd"] += qtd
        carrinho[nome]["preco"] = preco
    else:
        carrinho[nome] = {"preco": preco, "qtd": qtd}

def _add_code(carrinho, codigo: str, qtd=1):
    if not codigo:
        return
    codigo = unquote(str(codigo)).strip()
    qtd = _to_int(qtd, 1)
    item = CATALOGO.get(codigo)
    if not item:
        return
    _add_item(carrinho, item["nome"], item["preco"], qtd)

def get_cart(cid):
    """Recupera carrinho do store ou cria um novo"""
    if cid and cid in CART_STORE:
        return CART_STORE[cid].copy()
    return {}

def save_cart(cid, carrinho):
    """Salva carrinho no store"""
    if cid:
        CART_STORE[cid] = carrinho.copy()

@app.route('/')
def index():
    # Pega o cid da URL ou cria um novo
    cid = request.args.get('cid', '').strip()
    if not cid:
        cid = uuid.uuid4().hex[:8]
        return redirect(url_for('index', cid=cid))
    
    # Carrega carrinho
    carrinho = get_cart(cid)
    changed = False
    
    # Processa parâmetros da URL
    args = request.args
    
    # limpar carrinho: ?clear=1
    if args.get("clear"):
        carrinho = {}
        changed = True

    # remover item por nome ou código: ?rm=Camiseta ou ?rm=50
    rm_val, _ = _get_param(args, {"rm", "remove", "del"})
    if rm_val:
        key = unquote(str(rm_val)).strip()
        # tenta por nome
        if key in carrinho:
            del carrinho[key]
            changed = True
        else:
            # tenta por código -> mapeia para nome
            item = CATALOGO.get(key)
            if item and item["nome"] in carrinho:
                del carrinho[item["nome"]]
                changed = True

    # múltiplos códigos: ?codes=89|2;50|1
    codes_val, _ = _get_param(args, {"codes", "itens", "items", "codigos"})
    if codes_val:
        for chunk in str(codes_val).split(";"):
            if not chunk.strip():
                continue
            parts = [p.strip() for p in chunk.split("|")]
            if len(parts) == 1:
                _add_code(carrinho, parts[0], 1)
            else:
                _add_code(carrinho, parts[0], parts[1])
            changed = True

    # único código: aceita Codigo, codigo, code, cod, sku, id
    code_val, _ = _get_param(args, {"codigo", "code", "cod", "sku", "id"})
    if code_val is not None:
        qty_val, _ = _get_param(args, {"quantidade", "qty", "q"})
        _add_code(carrinho, code_val, qty_val if qty_val is not None else 1)
        changed = True

    # compat: formato antigo ?produto=Nome&preco=9,90&quantidade=2
    if "produto" in args and "preco" in args:
        nome = args.get("produto")
        preco = args.get("preco")
        qtd = args.get("quantidade", 1)
        _add_item(carrinho, unquote(nome), preco, qtd)
        changed = True

    if changed:
        save_cart(cid, carrinho)
        # Redireciona para limpar a URL, mantendo apenas o cid
        return redirect(url_for('index', cid=cid))
    
    # Calcula totais
    total = 0.0
    for produto, info in carrinho.items():
        subtotal = info["preco"] * info["qtd"]
        total += subtotal
    
    capital = total / 2
    
    return render_template('index.html', 
                         carrinho=carrinho, 
                         total=total, 
                         capital=capital, 
                         cid=cid,
                         quote=quote)

if __name__ == '__main__':
    app.run(debug=True)