# cliente_api.py
# Para instalar: pip install requests

import requests
import json

BASE_URL = 'http://localhost:8000/amazon_api/'

def listar_clientes():
    """Retorna todos os clientes cadastrados."""
    response = requests.get(BASE_URL + 'clientes/')
    
    if response.status_code == 200:
        return response.json()
    return []

def criar_cliente(nome, email, telefone=''):
    """Cadastra um novo cliente via POST."""
    payload = {'nome': nome, 'email': email, 'telefone': telefone}
    response = requests.post(BASE_URL + 'clientes/', json=payload)
    
    if response.status_code == 201:
        print(f'Cliente criado: {response.json()}')
    else:
        print(f'Erro {response.status_code}: {response.text}')

def buscar_cliente(cliente_id):
    """Busca um cliente específico pelo seu ID."""
    response = requests.get(BASE_URL + f'clientes/{cliente_id}/')
    
    if response.status_code == 200:
        return response.json()
    return None

if __name__ == '__main__':
    
    # Criar alguns clientes de teste
    criar_cliente('Maria da Silva', 'maria@email.com', '(84) 91111-2222')
    criar_cliente('João de Souza', 'joao@email.com', '(84) 93333-4444')
    
    # Listar todos os clientes
    print('\n--- Clientes cadastrados ---')
    
    for c in listar_clientes():
        print(f" [{c['id']}] {c['nome']} — {c['email']}")