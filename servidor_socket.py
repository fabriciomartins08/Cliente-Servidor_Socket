import socket
import string

# cria um socket para comunicação
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# define o endereço IP e porta do servidor
server_ip = '127.0.0.1'
server_port = 8888

# vincula o socket ao endereço IP e porta do servidor
server_socket.bind((server_ip, server_port))

# coloca o servidor em modo de escuta
server_socket.listen(1)

# inicializa a agenda
agenda = {}

# função para pesquisar por letra
def pesquisar_letra(letra, agenda):
    contatos_letra = []
    for nome, dados_contato in agenda.items():
        if nome.startswith(letra.upper()):
            contatos_letra.append((nome, dados_contato['telefone'], dados_contato['email']))
    if contatos_letra:
        resposta = '\n'.join([f'{nome}: {telefone}, {email}' for nome, telefone, email in contatos_letra])
    else:
        resposta = f'Nenhum contato encontrado com a letra {letra}'
    return resposta

# função para pesquisar por nome
def pesquisar_nome(nome, agenda):
    if nome in agenda:
        contato = agenda[nome]
        resposta = f'Telefone de {nome}: {contato["telefone"]}\nE-mail de {nome}: {contato["email"]}'
    else:
        resposta = f'{nome} não encontrado na agenda'
    return resposta

# função para retornar o próximo registro da agenda
def proximo_registro(agenda):
    if not agenda:
        resposta = 'A agenda está vazia'
    else:
        nome = next(iter(agenda))
        contato = agenda[nome]
        resposta = f'Próximo registro: {nome}, {contato["telefone"]}, {contato["email"]}'
    return resposta

def proxima_letra(letra_atual, agenda):
    for letra in string.ascii_uppercase:
        if letra > letra_atual:
            for nome, dados_contato in agenda.items():
                if nome.startswith(letra):
                    return f'{nome}: {dados_contato["telefone"]}, {dados_contato["email"]}'
    return f'Não há contatos cujo nome comece com uma letra posterior a {letra_atual}'

def apagar_registro(nome, agenda):
    if nome in agenda:
        agenda.pop(nome)
        resposta = f'{nome} removido da agenda'
    else:
        resposta = f'{nome} não encontrado na agenda'
    return resposta

def alterar_registro(nome, telefone, email, agenda):
    if nome in agenda:
        agenda[nome] = {'telefone': telefone, 'email': email}
        resposta = f'{nome} atualizado na agenda'
    else:
        resposta = f'{nome} não encontrado na agenda'
    return resposta

# loop principal do servidor
while True:
    print('Aguardando conexão...')
    # aguarda uma conexão com um cliente
    client_socket, client_address = server_socket.accept()
    print('Conexão estabelecida com', client_address)

    while True:
        # recebe o comando enviado pelo cliente
        command = client_socket.recv(1024).decode()
        print('Comando recebido:', command)

        # verifica se o comando é para sair da aplicação
        if command == 'SAIR':
            break

        # separa o comando em suas partes
        parts = command.split()

        # verifica qual o tipo de comando
        if parts[0] == 'ADICIONAR':
            # adiciona um novo contato na agenda
            nome = parts[1]
            telefone = parts[2]
            email = parts[3]
            agenda[nome] = {'telefone': telefone, 'email': email}
            resposta = 'Contato adicionado com sucesso!'
        elif parts[0] == 'BUSCAR':
            # busca um contato na agenda
            nome = parts[1]
            if nome in agenda:
                contato = agenda[nome]
                resposta = f'Telefone de {nome}: {contato["telefone"]}\nE-mail de {nome}: {contato["email"]}'
            else:
                resposta = f'{nome} não encontrado na agenda'
        elif parts[0] == 'PESQUISAR_LETRA':
            # pesquisa por letra na agenda
            letra = parts[1]
            resposta = pesquisar_letra(letra, agenda)
        elif parts[0] == 'PESQUISAR_NOME':
            # pesquisa por nome na agenda
            nome = parts[1]
            resposta = pesquisar_nome(nome, agenda)
        elif parts[0] == 'PROXIMO_REGISTRO':
            # retorna o próximo registro da agenda
            resposta = proximo_registro(agenda)
        elif parts[0] == 'PROXIMA_LETRA':
            letra_atual = parts[1].upper() if len(parts) > 1 else 'A'
            resposta = proxima_letra(letra_atual, agenda)
        elif parts[0] == 'APAGAR':
            # apaga um registro da agenda
            nome = parts[1]
            resposta = apagar_registro(nome, agenda)
        elif parts[0] == 'ALTERAR':
    	    # altera um registro na agenda
                    nome = parts[1]
                    elefone = parts[2]
                    email = parts[3]
                    resposta = alterar_registro(nome, telefone, email, agenda)
        else:
            # comando inválido
            resposta = 'Comando inválido'

        # envia a resposta para o cliente
        client_socket.send(resposta.encode())

    # encerra a conexão com o cliente
    client_socket.close()
    print('Conexão encerrada com', client_address)