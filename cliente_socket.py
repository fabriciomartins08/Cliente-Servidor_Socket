import socket

# cria um socket para comunicação
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# define o endereço IP e porta do servidor
server_ip = '127.0.0.1'
server_port = 8888

# conecta-se ao servidor
client_socket.connect((server_ip, server_port))

# loop principal do cliente
while True:
    # lê o comando digitado pelo usuário
    command = input('Digite um comando (ADICIONAR, BUSCAR, PESQUISAR_LETRA, PESQUISAR_NOME, PROXIMO_REGISTRO, PROXIMA_LETRA, APAGAR, ALTERAR, SAIR): ')

    # envia o comando para o servidor
    client_socket.send(command.encode())

    # verifica se o comando é para sair da aplicação
    if command == 'SAIR':
        break

    # recebe a resposta do servidor
    resposta = client_socket.recv(1024).decode()

    # exibe a resposta para o usuário
    print(resposta)

# fecha o socket do cliente
client_socket.close()