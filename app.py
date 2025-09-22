import re
import uuid
from urllib.parse import unquote, quote
from flask import Flask, render_template, request, redirect, url_for, session, make_response
import os





app = Flask(__name__)
app.secret_key = "segredo"

#app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# ---------------------- CATÁLOGO --------------------------- #
CATALOGO = {
    "JM001": {"nome": "JM001 - Jaqueta Puffer - P", "tamanho": "P", "produto": "Jaqueta Puffer", "preco": 180.00},
    "JM002": {"nome": "JM002 - Jaqueta Puffer - M", "tamanho": "M", "produto": "Jaqueta Puffer", "preco": 180.00},
    "JM003": {"nome": "JM003 - Jaqueta Puffer - G", "tamanho": "G", "produto": "Jaqueta Puffer", "preco": 180.00},
    "JM004": {"nome": "JM004 - Jaqueta Puffer - GG", "tamanho": "GG", "produto": "Jaqueta Puffer", "preco": 180.00},
    "JF001": {"nome": "JF001 - Jaqueta Puffer Feminino - P", "tamanho": "P", "produto": "Jaqueta Puffer Feminino", "preco": 180.00},
    "JF002": {"nome": "JF002 - Jaqueta Puffer Feminino - M", "tamanho": "M", "produto": "Jaqueta Puffer Feminino", "preco": 180.00},
    "JF003": {"nome": "JF003 - Jaqueta Puffer Feminino - G", "tamanho": "G", "produto": "Jaqueta Puffer Feminino", "preco": 180.00},
    "JF004": {"nome": "JF004 - Jaqueta Puffer Feminino - GG", "tamanho": "GG", "produto": "Jaqueta Puffer Feminino", "preco": 180.00},
    "CO001": {"nome": "CO001 - Colete Puffer - P", "tamanho": "P", "produto": "Colete Puffer", "preco": 160.00},
    "CO002": {"nome": "CO002 - Colete Puffer - M", "tamanho": "M", "produto": "Colete Puffer", "preco": 160.00},
    "CO003": {"nome": "CO003 - Colete Puffer - G", "tamanho": "G", "produto": "Colete Puffer", "preco": 160.00},
    "CO004": {"nome": "CO004 - Colete Puffer - GG", "tamanho": "GG", "produto": "Colete Puffer", "preco": 160.00},
    "CV001": {"nome": "CV001 - Corta Vento - P", "tamanho": "P", "produto": "Corta Vento", "preco": 170.00},
    "CV002": {"nome": "CV002 - Corta Vento - M", "tamanho": "M", "produto": "Corta Vento", "preco": 170.00},
    "CV003": {"nome": "CV003 - Corta Vento - G", "tamanho": "G", "produto": "Corta Vento", "preco": 170.00},
    "CV004": {"nome": "CV004 - Corta Vento - GG", "tamanho": "GG", "produto": "Corta Vento", "preco": 170.00},
    "MC001": {"nome": "MC001 - Moletom preto com capuz e bolso na frente e logo no peito - P", "tamanho": "P", "produto": "Moletom preto com capuz e bolso na frente e logo no peito", "preco": 87.00},
    "MC002": {"nome": "MC002 - Moletom preto com capuz e bolso na frente e logo no peito - M", "tamanho": "M", "produto": "Moletom preto com capuz e bolso na frente e logo no peito", "preco": 87.00},
    "MC003": {"nome": "MC003 - Moletom preto com capuz e bolso na frente e logo no peito - G", "tamanho": "G", "produto": "Moletom preto com capuz e bolso na frente e logo no peito", "preco": 87.00},
    "MC004": {"nome": "MC004 - Moletom preto com capuz e bolso na frente e logo no peito - GG", "tamanho": "GG", "produto": "Moletom preto com capuz e bolso na frente e logo no peito", "preco": 87.00},
    "MS001": {"nome": "MS001 - Moletom preto sem capuz e bolso na frente e logo no peito - P", "tamanho": "P", "produto": "Moletom preto sem capuz e bolso na frente e logo no peito", "preco": 77.00},
    "MS002": {"nome": "MS002 - Moletom preto sem capuz e bolso na frente e logo no peito - M", "tamanho": "M", "produto": "Moletom preto sem capuz e bolso na frente e logo no peito", "preco": 77.00},
    "MS003": {"nome": "MS003 - Moletom preto sem capuz e bolso na frente e logo no peito - G", "tamanho": "G", "produto": "Moletom preto sem capuz e bolso na frente e logo no peito", "preco": 77.00},
    "MS004": {"nome": "MS004 - Moletom preto sem capuz e bolso na frente e logo no peito - GG", "tamanho": "GG", "produto": "Moletom preto sem capuz e bolso na frente e logo no peito", "preco": 77.00},
    "MJ001": {"nome": "MJ001 - Moletom tipo jaqueta e capuz azul marinho com logo no peito - P", "tamanho": "P", "produto": "Moletom tipo jaqueta e capuz azul marinho com logo no peito", "preco": 112.00},
    "MJ002": {"nome": "MJ002 - Moletom tipo jaqueta e capuz azul marinho com logo no peito - M", "tamanho": "M", "produto": "Moletom tipo jaqueta e capuz azul marinho com logo no peito", "preco": 112.00},
    "MJ003": {"nome": "MJ003 - Moletom tipo jaqueta e capuz azul marinho com logo no peito - G", "tamanho": "G", "produto": "Moletom tipo jaqueta e capuz azul marinho com logo no peito", "preco": 112.00},
    "MJ004": {"nome": "MJ004 - Moletom tipo jaqueta e capuz azul marinho com logo no peito - GG", "tamanho": "GG", "produto": "Moletom tipo jaqueta e capuz azul marinho com logo no peito", "preco": 112.00},
    "CS001": {"nome": "CS001 - Camiseta Sicredi Soma - P", "tamanho": "P", "produto": "Camiseta Sicredi Soma", "preco": 28.50},
    "CS002": {"nome": "CS002 - Camiseta Sicredi Soma - M", "tamanho": "M", "produto": "Camiseta Sicredi Soma", "preco": 28.50},
    "CS003": {"nome": "CS003 - Camiseta Sicredi Soma - G", "tamanho": "G", "produto": "Camiseta Sicredi Soma", "preco": 28.50},
    "CS004": {"nome": "CS004 - Camiseta Sicredi Soma - GG", "tamanho": "GG", "produto": "Camiseta Sicredi Soma", "preco": 28.50},
    "CP001": {"nome": "CP001 - Camiseta Preta Só logo Sicredi Branca - P", "tamanho": "P", "produto": "Camiseta Preta Só logo Sicredi Branca", "preco": 28.50},
    "CP002": {"nome": "CP002 - Camiseta Preta Só logo Sicredi Branca - M", "tamanho": "M", "produto": "Camiseta Preta Só logo Sicredi Branca", "preco": 28.50},
    "CP003": {"nome": "CP003 - Camiseta Preta Só logo Sicredi Branca - G", "tamanho": "G", "produto": "Camiseta Preta Só logo Sicredi Branca", "preco": 28.50},
    "CP004": {"nome": "CP004 - Camiseta Preta Só logo Sicredi Branca - GG", "tamanho": "GG", "produto": "Camiseta Preta Só logo Sicredi Branca", "preco": 28.50},
    "CB001": {"nome": "CB001 - Camiseta Branca Só logo Sicredi Preta - P", "tamanho": "P", "produto": "Camiseta Branca Só logo Sicredi Preta", "preco": 28.50},
    "CB002": {"nome": "CB002 - Camiseta Branca Só logo Sicredi Preta - M", "tamanho": "M", "produto": "Camiseta Branca Só logo Sicredi Preta", "preco": 28.50},
    "CB003": {"nome": "CB003 - Camiseta Branca Só logo Sicredi Preta - G", "tamanho": "G", "produto": "Camiseta Branca Só logo Sicredi Preta", "preco": 28.50},
    "CB004": {"nome": "CB004 - Camiseta Branca Só logo Sicredi Preta - GG", "tamanho": "GG", "produto": "Camiseta Branca Só logo Sicredi Preta", "preco": 28.50},
    "PO001": {"nome": "PO001 - Camiseta Polo preta com logo branca - P", "tamanho": "P", "produto": "Camiseta Polo preta com logo branca", "preco": 59.50},
    "PO002": {"nome": "PO002 - Camiseta Polo preta com logo branca - M", "tamanho": "M", "produto": "Camiseta Polo preta com logo branca", "preco": 59.50},
    "PO003": {"nome": "PO003 - Camiseta Polo preta com logo branca - G", "tamanho": "G", "produto": "Camiseta Polo preta com logo branca", "preco": 59.50},
    "PO004": {"nome": "PO004 - Camiseta Polo preta com logo branca - GG", "tamanho": "GG", "produto": "Camiseta Polo preta com logo branca", "preco": 59.50},
    "CP001A": {"nome": "CP001 - Camiseta Padre Amistad - P", "tamanho": "P", "produto": "Camiseta Padre Amistad", "preco": 39.90},
    "CP002A": {"nome": "CP002 - Camiseta Padre Amistad - M", "tamanho": "M", "produto": "Camiseta Padre Amistad", "preco": 39.90},
    "CP003A": {"nome": "CP003 - Camiseta Padre Amistad - G", "tamanho": "G", "produto": "Camiseta Padre Amistad", "preco": 39.90},
    "CP004A": {"nome": "CP004 - Camiseta Padre Amistad - GG", "tamanho": "GG", "produto": "Camiseta Padre Amistad", "preco": 39.90},
    "BR001": {"nome": "BR001 - Boné rosa", "tamanho": "", "produto": "Boné rosa", "preco": 16.50},
    "BV001": {"nome": "BV001 - Boné Verde", "tamanho": "", "produto": "Boné Verde", "preco": 16.50},
    "BO001": {"nome": "BO001 - Botinas - 38", "tamanho": "38", "produto": "Botinas", "preco": 149.90},
    "BO002": {"nome": "BO002 - Botinas - 39", "tamanho": "39", "produto": "Botinas", "preco": 149.90},
    "BO003": {"nome": "BO003 - Botinas - 40", "tamanho": "40", "produto": "Botinas", "preco": 149.90},
    "BO004": {"nome": "BO004 - Botinas - 41", "tamanho": "41", "produto": "Botinas", "preco": 149.90},
    "BO005": {"nome": "BO005 - Botinas - 42", "tamanho": "42", "produto": "Botinas", "preco": 149.90},
    "BO006": {"nome": "BO006 - Botinas - 43", "tamanho": "43", "produto": "Botinas", "preco": 149.90},
    "KT001": {"nome": "KT001 - Kit Terere", "tamanho": "", "produto": "Kit Terere", "preco": 220.00},
    "MT001": {"nome": "MT001 - Mateira", "tamanho": "", "produto": "Mateira", "preco": 166.70},
    "GC001": {"nome": "GC001 - Guarda-chuva invertido", "tamanho": "", "produto": "Guarda-chuva invertido", "preco": 79.90},
    "CE001": {"nome": "CE001 - Cuia de embuia", "tamanho": "", "produto": "Cuia de embuia", "preco": 49.90},
    "CP001B": {"nome": "CP001 - Cuia de Porongo", "tamanho": "", "produto": "Cuia de Porongo", "preco": 39.90},
    "SQ001": {"nome": "SQ001 - Squezze 600ml aluminio", "tamanho": "", "produto": "Squezze 600ml aluminio", "preco": 29.70},
    "CL001": {"nome": "CL001 - Cooler 12 latas", "tamanho": "", "produto": "Cooler 12 latas", "preco": 37.70},
    "CT001": {"nome": "CT001 - 10 caixa térmica de 12 litros", "tamanho": "", "produto": "10 caixa térmica de 12 litros", "preco": 89.90},
    "CT002": {"nome": "CT002 - 10 caixa térmica de 34 litros", "tamanho": "", "produto": "10 caixa térmica de 34 litros", "preco": 129.90},
    "MA001": {"nome": "MA001 - Mala para viagem", "tamanho": "", "produto": "Mala para viagem", "preco": 299.90},
    "MO001": {"nome": "MO001 - Mochila de Couro Sintético", "tamanho": "", "produto": "Mochila de Couro Sintético", "preco": 239.90},
    "GT001": {"nome": "GT001 - Garrafa Térmica 1 litro", "tamanho": "", "produto": "Garrafa Térmica 1 litro", "preco": 109.90},
    "GT002": {"nome": "GT002 - Garrafa Térmica 1,5 litro", "tamanho": "", "produto": "Garrafa Térmica 1,5 litro", "preco": 129.90},
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

"""   
@app.route('/')
def index():
    # Pega o cid da URL ou cria um novo
    cid = request.args.get('cid', '').strip()
    #if not cid:
    #    cid = uuid.uuid4().hex[:8]
    #    return redirect(url_for('index', cid=cid))
    if not cid:
        cid = uuid.uuid4().hex[:8]
        # Mantém todos os parâmetros originais na URL ao redirecionar, adicionando o novo cid
        args_dict = request.args.to_dict()
        args_dict['cid'] = cid
        return redirect(url_for('index', **args_dict))

    
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

"""


@app.route('/')
@app.route('/index')

def index():
    # 1. Tenta pegar da URL
    cid = request.args.get('cid')
    # 2. Se não tiver, tenta pegar do cookie
    if not cid:
        cid = request.cookies.get('cid')
    # 3. Se não tiver, gera nova
    if not cid:
        cid = uuid.uuid4().hex[:8]

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

    # Salva carrinho se mudou e "limpa" a URL (mantendo só cid)
    if changed:
        save_cart(cid, carrinho)
        return redirect(url_for('index', cid=cid))

    # Calcula totais
    total = 0.0
    for produto, info in carrinho.items():
        subtotal = info["preco"] * info["qtd"]
        total += subtotal

    capital = total / 2
    my_quote = ""  # Ou defina um valor se usa no template

    resp = make_response(render_template(
        'index.html',
        carrinho=carrinho,
        total=total,
        capital=capital,
        cid=cid,
        quote=""
    ))
    # 4. Salva a cid no cookie por 30 dias
    resp.set_cookie('cid', cid, max_age=60*60*24*30)
    return resp


if __name__ == '__main__':
    app.run(debug=True)
