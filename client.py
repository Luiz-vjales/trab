import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))

    while True:
        print("\nEscolha a operação:")
        print("1. Converter numero hexadecimal para base 10")
        print("2. Converter numero decimal para base 2")
        print("3. Somar dois números binários")
        print("4. Subtrair dois números binários")
        print("5. Divisão de dois números binários")
        print("6. Converter um número decimal para IEEE 754")
        print("7. Codificar uma string em UTF-8")
        print("0. Sair")
        choice = input("Digite o número da operação desejada: ")

        if choice == "0":
            print("Encerrando o cliente...")
            break

        value1 = input("Digite o primeiro valor: ")

        if choice in ["3", "4", "5"]:
            value2 = input("Digite o segundo valor: ")
        else:
            value2 = ""

        if choice == "1":
            operation = "conv_16_10"
        elif choice == "2":
            operation = "conv_10_2"
        elif choice == "3":
            operation = "add_bin"
        elif choice == "4":
            operation = "sub_bin"
        elif choice == "5":
            operation = "div_bin"
        elif choice == "6":
            operation = "ieee_754"
        elif choice == "7":
            operation = "utf8_enc"
        else:
            print("Operação inválida")
            continue

        request = f"{operation}:{value1}:{value2}"
        client_socket.sendall(request.encode())

        data = client_socket.recv(1024)
        print(f"Resultado: {data.decode()}")

    client_socket.close()

if __name__ == "__main__":
    start_client()
