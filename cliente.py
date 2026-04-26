import socket
import json

HOST = "127.0.0.1"
PUERTO = 5000

print("=" * 60)
print("CLIENTE BLOCKCHAIN")
print("=" * 60)

remitente = input("Ingrese su nombre: ")

while True:
    texto = input(f"\n[{remitente}] Mensaje (o 'salir'): ")
    if texto.lower() == "salir":
        print("Cerrando cliente...")
        break

    mensaje = {
        "remitente": remitente,
        "texto": texto
    }

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PUERTO))
            s.sendall(json.dumps(mensaje).encode())

            respuesta = s.recv(4096).decode()
            datos = json.loads(respuesta)

            print(f"\n[Respuesta del servidor]")
            print(f"  Estado: {datos['estado']}")
            print(f"  Bloque #{datos['bloque']['indice']}")
            print(f"  Hash: {datos['bloque']['hash']}")
            print(f"  Hash anterior: {datos['bloque']['hash_anterior']}")
            print(f"  Nonce: {datos['bloque']['nonce']}")
            print(f"  Cadena valida: {datos['cadena_valida']}")
            print(f"  Total de bloques: {datos['total_bloques']}")
    except ConnectionRefusedError:
        print("[!] No se pudo conectar al servidor. Verifique que este corriendo.")
