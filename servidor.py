import socket
import json
from blockchain import Blockchain

HOST = "127.0.0.1"
PUERTO = 5000

cadena = Blockchain()

print("=" * 60)
print("SERVIDOR BLOCKCHAIN INICIADO")
print("=" * 60)
print(f"Escuchando en {HOST}:{PUERTO}")
print(f"Dificultad de minado: {cadena.dificultad}")
print("=" * 60)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PUERTO))
    s.listen()

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"\n[+] Conexion recibida desde {addr}")
            data = conn.recv(4096).decode()
            mensaje = json.loads(data)

            print(f"[Mensaje recibido] '{mensaje['texto']}' de {mensaje['remitente']}")
            print("[*] Minando bloque...")

            bloque = cadena.agregar_bloque(mensaje["texto"], mensaje["remitente"])

            respuesta = {
                "estado": "OK",
                "bloque": bloque.to_dict(),
                "cadena_valida": cadena.es_valida(),
                "total_bloques": len(cadena.cadena)
            }

            conn.sendall(json.dumps(respuesta).encode())
            print(f"[+] Bloque {bloque.indice} agregado. Total: {len(cadena.cadena)}")
            print(f"[+] Cadena valida: {cadena.es_valida()}")
