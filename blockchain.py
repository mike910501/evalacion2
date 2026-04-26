import hashlib
import json
from time import time


class Bloque:
    def __init__(self, indice, mensaje, remitente, hash_anterior):
        self.indice = indice
        self.timestamp = time()
        self.mensaje = mensaje
        self.remitente = remitente
        self.hash_anterior = hash_anterior
        self.nonce = 0
        self.hash = self.calcular_hash()

    def calcular_hash(self):
        contenido = {
            "indice": self.indice,
            "timestamp": self.timestamp,
            "mensaje": self.mensaje,
            "remitente": self.remitente,
            "hash_anterior": self.hash_anterior,
            "nonce": self.nonce
        }
        cadena = json.dumps(contenido, sort_keys=True).encode()
        return hashlib.sha256(cadena).hexdigest()

    def minar(self, dificultad):
        # Proof of Work: buscar un hash que empiece con N ceros
        objetivo = "0" * dificultad
        while not self.hash.startswith(objetivo):
            self.nonce += 1
            self.hash = self.calcular_hash()
        print(f"[Bloque {self.indice} minado] Hash: {self.hash}")

    def to_dict(self):
        return {
            "indice": self.indice,
            "timestamp": self.timestamp,
            "mensaje": self.mensaje,
            "remitente": self.remitente,
            "hash_anterior": self.hash_anterior,
            "nonce": self.nonce,
            "hash": self.hash
        }


class Blockchain:
    def __init__(self):
        self.dificultad = 3
        self.cadena = [self.crear_bloque_genesis()]

    def crear_bloque_genesis(self):
        bloque = Bloque(0, "Bloque Genesis", "Sistema", "0")
        bloque.minar(self.dificultad)
        return bloque

    def ultimo_bloque(self):
        return self.cadena[-1]

    def agregar_bloque(self, mensaje, remitente):
        nuevo = Bloque(
            indice=len(self.cadena),
            mensaje=mensaje,
            remitente=remitente,
            hash_anterior=self.ultimo_bloque().hash
        )
        nuevo.minar(self.dificultad)
        self.cadena.append(nuevo)
        return nuevo

    def es_valida(self):
        for i in range(1, len(self.cadena)):
            actual = self.cadena[i]
            anterior = self.cadena[i - 1]
            if actual.hash != actual.calcular_hash():
                return False
            if actual.hash_anterior != anterior.hash:
                return False
        return True

    def mostrar(self):
        for bloque in self.cadena:
            print(json.dumps(bloque.to_dict(), indent=2))
            print("-" * 60)
