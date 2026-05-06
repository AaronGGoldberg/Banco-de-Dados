from requests import request
import json
IP = "localhost"

def criar_grupos():
    cli = f'http://{IP}:8000/api/grupos/'
    grupos =  open('grupos.json', 'r').read()
    grupos=json.loads(grupos)
    for grupo in grupos:    
        request('POST', cli, json=grupo)

def criar_selecoes():
    cli = f'http://{IP}:8000/api/selecoes/'
    selecoes = open('selecoes.json', 'r').read()
    selecoes=json.loads(selecoes)
    for selecao in selecoes:    
        request('POST', cli, json=selecao)

def criar_jogadores():
    cli = f'http://{IP}:8000/api/jogadores/'
    jogadores = open('jogadores.json', 'r').read()
    jogadores=json.loads(jogadores)
    for jogador in jogadores:    
        request('POST', cli, json=jogador)

def criar_tecnicos():
    cli = f'http://{IP}:8000/api/tecnicos/'
    tecnicos = open('tecnicos.json', 'r').read()
    tecnicos=json.loads(tecnicos)
    for tecnico in tecnicos:    
        request('POST', cli, json=tecnico)

def criar_jogos():
    cli = f'http://{IP}:8000/api/jogos/'
    jogos = open('jogos.json', 'r').read()
    jogos=json.loads(jogos)
    for jogo in jogos:    
        request('POST', cli, json=jogo)

#criar_jogos()
#criar_tecnicos()
#criar_jogadores()
#criar_selecoes()
#criar_grupos()