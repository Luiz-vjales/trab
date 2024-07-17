import socket
import struct

def converter_b16_para_b10(hex_num):
    return int(hex_num, 16)

def converter_b10_para_b2(dec_num):
    return bin(int(dec_num)).replace("0b", "")

def adicao(bin1, bin2):
    max_len = max(len(bin1), len(bin2))
    bin1 = bin1.zfill(max_len)
    bin2 = bin2.zfill(max_len)
    resultado = bin(int(bin1, 2) + int(bin2, 2)).replace("0b", "").zfill(max_len)
    overflow = len(resultado) > max_len
    resultado = resultado[-max_len:]  # Mantenha apenas os bits dentro max_len
    return resultado, overflow

def subtracao(bin1, bin2):
    max_len = max(len(bin1), len(bin2))
    bin1 = bin1.zfill(max_len)
    bin2 = bin2.zfill(max_len)
    resultado = bin((int(bin1, 2) - int(bin2, 2)) & ((1 << max_len) - 1)).replace("0b", "").zfill(max_len)
    overflow = len(resultado) > max_len
    resultado = resultado[-max_len:]  # Mantenha apenas os bits dentro max_len
    return resultado, overflow

def complemento_a_2(bin_num):
    # Converter string binária em inteiro
    num = int(bin_num, 2)
    # Calcula complemento a 2
    complement = ((1 << len(bin_num)) - num) & ((1 << len(bin_num)) - 1)
    return bin(complement).replace("0b", "").zfill(len(bin_num))

def divisao(bin1, bin2):
    if bin2 == '0':
        return "Erro: Divisão por zero"
    # Converte bin2 em complemento de dois se for negativo
    if bin2[0] == '1':
        bin2 = complemento_a_2(bin2)
    dividendo = int(bin1, 2)
    divisor = int(bin2, 2)
    quociente = dividendo // divisor
    return bin(quociente).replace("0b", "").zfill(8)

def float_ieee754(value):
    packed = struct.pack('>f', value)
    bits = ''.join(f'{byte:08b}' for byte in packed)
    return bits

def utf8(string):
    return ' '.join(format(ord(char), '02x') for char in string)

def solicitacao(request):
    try:
        operation, value1, value2 = request.split(':')
    except ValueError:
        operation, value1 = request.split(':')
        value2 = None

    if operation == "conv_16_10":
        resultado = converter_b16_para_b10(value1)
    elif operation == "conv_10_2":
        resultado = converter_b10_para_b2(value1)
    elif operation == "add_bin":
        resultado, overflow = adicao(value1, value2)
        resultado = f"{resultado} (Overflow: {'Yes' if overflow else 'No'})"
    elif operation == "sub_bin":
        resultado, overflow = subtracao(value1, value2)
        resultado = f"{resultado} (Overflow: {'Yes' if overflow else 'No'})"
    elif operation == "div_bin":
        resultado = divisao(value1, value2)
    elif operation == "ieee_754":
        resultado = float_ieee754(float(value1))
    elif operation == "utf8_enc":
        resultado = utf8(value1)
    else:
        resultado = "Operação desconhecida"

    return str(resultado)

def start_servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65432))
    server_socket.listen(1)
    print("Servidor aguardando conexão...")

    conn, addr = server_socket.accept()
    print(f"Conectado por {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        request = data.decode()
        response = solicitacao(request)
        conn.sendall(response.encode())

    conn.close()

if __name__ == "__main__":
    start_servidor()
