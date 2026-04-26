# Evaluación 2 — Cadena de Bloques con Mensajería

Asignatura: Seguridad de la Información
Fundación Universitaria Compensar

---

## Descripción

Este proyecto implementa una cadena de bloques (blockchain) sencilla en Python que permite el intercambio de mensajes entre dos servidores. Cada mensaje enviado se guarda como un bloque en la cadena, garantizando integridad mediante hashes SHA-256 y prueba de trabajo (Proof of Work).

## Estructura del proyecto

```
Evaluacion-2/
├── blockchain.py    # Logica de la cadena de bloques
├── servidor.py      # Servidor que recibe mensajes y los mina
├── cliente.py       # Cliente que envia mensajes
└── README.md        # Este archivo
```

## Cómo se crea un bloque

Cada bloque contiene los siguientes campos:

- **indice**: posicion del bloque en la cadena
- **timestamp**: fecha y hora de creacion
- **mensaje**: contenido del mensaje
- **remitente**: quien envia el mensaje
- **hash_anterior**: hash del bloque previo (lo que hace la cadena)
- **nonce**: numero que cambia hasta cumplir la dificultad
- **hash**: hash SHA-256 del bloque

Pasos:

1. Se toman los datos del mensaje recibido
2. Se calcula el hash con SHA-256 sobre todos los campos
3. Se hace **mining** (Proof of Work): se incrementa el nonce hasta que el hash empiece con N ceros (dificultad = 3 en este caso)
4. Una vez encontrado el hash valido, el bloque se agrega a la cadena
5. La cadena se valida verificando que cada bloque referencia correctamente al anterior

## Cómo ejecutarlo paso a paso

**Paso 1.** Abrir una terminal y ejecutar el servidor:

```bash
python servidor.py
```

El servidor queda escuchando en `127.0.0.1:5000` y crea automaticamente el bloque genesis.

**Paso 2.** Abrir otra terminal y ejecutar el cliente:

```bash
python cliente.py
```

**Paso 3.** Ingresar el nombre del remitente y enviar mensajes. Cada mensaje:

- Se envia al servidor por socket TCP
- El servidor lo recibe, crea un bloque nuevo, lo mina y lo agrega a la cadena
- Devuelve la confirmacion al cliente con el hash del bloque

**Paso 4.** Para detener el cliente, escribir `salir`.

## Funcionalidad de mensajería entre dos servidores

El sistema usa **sockets TCP** para la comunicacion:

- El servidor escucha en el puerto 5000
- El cliente se conecta, envia el mensaje en formato JSON y recibe la respuesta
- Cada mensaje se convierte en un bloque inmutable de la cadena

Si se quisiera tener dos nodos completos (peer-to-peer), cada nodo deberia tener su propia cadena y sincronizarse mediante un protocolo de consenso, lo cual es exactamente como funciona Bitcoin a mayor escala.

## Tipo de encriptación que se maneja en blockchain

Blockchain no usa "encriptación" en el sentido tradicional (no oculta los datos). Lo que usa son **funciones hash criptográficas** y **firma digital con criptografía asimétrica**:

### 1. Funciones hash criptográficas

- **SHA-256** es la mas usada (Bitcoin la usa)
- Toma cualquier entrada y produce una salida de 256 bits
- Es de una sola via: no se puede revertir
- Cualquier cambio minimo en la entrada produce un hash totalmente diferente
- Garantiza la **integridad** de cada bloque y enlaza la cadena

### 2. Criptografía asimétrica (clave pública/privada)

- **ECDSA** (Elliptic Curve Digital Signature Algorithm) es el estandar en Bitcoin y Ethereum
- Cada usuario tiene una clave privada (secreta) y una clave publica (compartida)
- La clave privada firma las transacciones
- La clave publica permite verificar que la firma es autentica
- Esto garantiza la **autenticacion** y el **no repudio**

### 3. Estructuras de datos criptográficas

- **Arboles de Merkle**: organizan las transacciones de forma que se pueda verificar la integridad de muchas transacciones con un solo hash raiz
- **Direcciones**: en Bitcoin son hashes de la clave publica (RIPEMD-160 sobre SHA-256)

### Resumen

| Mecanismo | Algoritmo | Para que sirve |
|-----------|-----------|----------------|
| Hash | SHA-256 | Integridad, enlace de bloques, mining |
| Firma digital | ECDSA | Autenticar transacciones |
| Direcciones | RIPEMD-160 | Identificar wallets |
| Estructura | Merkle Tree | Verificacion eficiente |

## Ejemplo de salida del servidor

```
============================================================
SERVIDOR BLOCKCHAIN INICIADO
============================================================
Escuchando en 127.0.0.1:5000
Dificultad de minado: 3
============================================================
[Bloque 0 minado] Hash: 000a3f8b2c4e...

[+] Conexion recibida desde ('127.0.0.1', 53842)
[Mensaje recibido] 'Hola Bob' de Alice
[*] Minando bloque...
[Bloque 1 minado] Hash: 000bf72a1d4e...
[+] Bloque 1 agregado. Total: 2
[+] Cadena valida: True
```

## Conclusión

Esta implementacion demuestra los conceptos fundamentales de blockchain:

- **Inmutabilidad**: cambiar un bloque rompe el hash y se detecta
- **Integridad**: cada bloque referencia al anterior con su hash
- **Proof of Work**: el mining hace costoso modificar la cadena
- **Descentralizacion**: aunque aqui es cliente-servidor, el principio se aplica a redes P2P

En sistemas reales como Bitcoin, esto se escala a miles de nodos que validan y propagan bloques, usando consenso distribuido para mantener una sola version de la verdad sin necesidad de una autoridad central.

## Requisitos

- Python 3.6 o superior
- No requiere librerias externas, solo modulos estandar (`socket`, `hashlib`, `json`, `time`)
