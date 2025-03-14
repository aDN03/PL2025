import json
import ply.lex as lex
from datetime import datetime

balance = 0.0
coin_mode = False
select_mode = False

with open('stock.json', 'r') as json_file:
    stock = json.load(json_file)

def centToEC(value):
    euro = int(value)
    cents = int(round((value - euro) * 100))

    if euro != 0 and cents != 0:
        return f"{euro}e{cents}c"
    elif euro != 0:
        return f"{euro}e"
    elif cents != 0:
        return f"{cents}c"
    else:
        return "0c"

def change(value):
    coins = [200, 100, 50, 20, 10, 5, 2, 1]
    result = ""
    value = int(round(value * 100))

    for coin in coins:
        count = value // coin

        if count > 0:
            if coin >= 100:
                result += f"{count}x {coin // 100}e, "
            else:
                result += f"{count}x {coin}c, "
            
            value -= coin * count
    
    if result:
        result = result[:-2]
        result += '.'
    else:
        result = '0x 0c.'
    
    return result

tokens = (
    'OP',
    'ID',
    'COIN',
    'DOTS',
    'VIR'
)

t_VIR = r','
t_ignore = ' \t\n'

def t_OP(token):
    r'\b[A-Z]+\b'
    global coin_mode, select_mode, balance

    if token.value == 'LISTAR':
        print('maq:')
        print('cod | nome | quantidade | preço')
        print('---------------------------------')
        for product in stock:
            print(f"{product['cod']} {product['nome']} {product['quant']} {product['preco']:.2f}€")
    
    elif token.value == 'MOEDA':
        coin_mode = True

    elif token.value == 'SELECIONAR':
        select_mode = True

    elif token.value == 'SAIR':
        print(f'maq: Pode retirar o troco: {change(balance)}')
        print('maq: Até à próxima')

def t_ID(token):
    r'[A-Z]\d+'
    global select_mode, stock, balance
    
    if select_mode:
        for product in stock:
            if product['cod'] == token.value:
                if product['quant'] == 0:
                    print(f"maq: Produto \"{product['nome']}\" esgotado.")
                elif balance >= product['preco']:
                    balance -= product['preco']
                    product['quant'] -= 1
                    print(f'maq: Pode retirar o produto "{product["nome"]}"')
                    print(f'maq: Saldo = {centToEC(balance)}')
                else:
                    print('maq: Saldo insuficiente para satisfazer o seu pedido')
                    print(f'maq: Saldo = {centToEC(balance)}; Pedido = {centToEC(product["preco"])}')

                select_mode = False 
                return

        print("maq: Código inválido")
        select_mode = False

def t_COIN(token):
    r'\d+[ec]'
    global balance
    
    if coin_mode:
        if token.value.endswith('e'):
            balance += float(token.value[:-1])
        else:
            balance += float(token.value[:-1]) * 0.01

def t_DOTS(token):
    r'\.'
    global coin_mode
    coin_mode = False
    print(f'maq: Saldo = {centToEC(balance)}')

def t_error(token):
    print(f"maq: Entrada inválida -> {token.value}")
    token.lexer.skip(1)

lexer = lex.lex()

def tokenize_input(data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok: 
            break

now = datetime.now().strftime("%Y-%m-%d %H:%M")
print("maq: " + now + ", Stock carregado, Estado atualizado.")
print("maq: Bom dia. Estou disponível para atender o seu pedido.")

while True:
    user_input = input('>> ').strip()
    tokenize_input(user_input)
    
    if user_input == "SAIR":
        break

with open('stock.json', 'w') as json_file:
    json.dump(stock, json_file, indent=4)
