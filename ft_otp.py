
import qrcode_terminal
import argparse
import hashlib
import struct
import hmac
import time
import re
import os

from cripta import Cripta as AES

"""
Proyecto basado en el código de https://github.com/15Galan

Un programa que, partiendo de una clave en formato hexadecimal de un mínimo de 64 caracteres, 
genera una clave OTP (30 segundos).
La semilla (clave inicial) se recibe por argumentos almacenada en un archivo sin cifrar.
El programa la lee, la cifra y la almacena en un nuevo archivo tras pedir una contraseña al usuario.
Para obtener la OTP el usuario introduce la contraseña elegida, que hace que el programa desencripte
la seed, la descifre, la lea y la vuelva a almacenar cifrada. Si el resultado es correcto, se genera
la OTP. 
También se puede pedir un código QR por terminal con la flag correspondiente que enlaza a la
seed cifrada.  
"""

# Lectura de los argumentos que entran por línea de comandos
def read_arg():
    # Inicialización del gestor de argumentos
    manager = start_manager()

    return manager.g, manager.k, manager.qr

# Inicialización del parser
def start_manager():
    # Analizador de argumentos de la línea de comandos
    manager = argparse.ArgumentParser(
    description= "Herramienta para generar contraseñas TOTP.",
    )

    # Opciones de flags
    manager.add_argument(
        "-g",
        metavar="file",
        help="almacena una clave hexadecimal de un mínimo de 64 caracteres en un fichero 'ft_otp.key'.",
        type=str)
    manager.add_argument(
        "-k",
        metavar="file",
        help="genera una contraseña temporal usando un fichero y la muestra en pantalla",
        type=str)
    manager.add_argument(
        "-qr",
        metavar="file",
        help="muestra un QR con la clave secreta.",
        type=str)

    # Obtener los argumentos de la línea de comandos
        
    return manager.parse_args()

# Comprobación de que el fichero contiene una clave con los requisitos exigidos
def validate_file(file):
    global key

    # El fichero existe y es legible (tiene permiso de lectura)
    if not (os.path.isfile(file) or os.access(file, os.R_OK)):
        print("Error: el fichero no existe o no tiene permiso de lectura.")

        return False
    
    # Extraer clave del fichero
    with open(file, "r") as f:
        key = f.read()

    # Verificación de que la clave es hexadecimal y que contiene al menos 64 caracteres
    if not re.match(r'^[0-9a-fA-F]{64,}$', key):
        print("La clave no está en formato hexadecimal o no tiene el mínimo de 64 caracteres.")

        return False
    
    return True

# Generar un código temporal usando una clave hexadecimal secreta.
def generate_OTP(key):

    # Codificar la clave hexadecimal en una cadena de bytes
    key_b = bytes.fromhex(key)

    # Obtener y truncar el tiempo actual a una ventana de 30 segundos
    time_a = int(time.time() // 30)

    # Codificar el tiempo en una cadena de bytes
    time_b = struct.pack(">Q", time_a)

    # Generar el hash de la clave secreta como cadena de bytes
    hash_b = hmac.digest(key_b, time_b, hashlib.sha1)

    # Obtener el offset (operación AND entre '0b????' y '0b1111')
    offset = hash_b[19] & 15

    # Generar el código ([0] porque 'struct.unpack' devuelve una lista)
    code = struct.unpack('>I', hash_b[offset:offset + 4])[0]
    code = (code & 0x7FFFFFF) % 1000000 # Para obtener una clave de 6 dígitos

    """
    Generar un Valor HTOP (en este caso de 6 dígitos).
    1. Generar un valor HMAC-SHA1.
        - Usando el valor de la clave y el valor del tiempo actual.
        - Será un 'str' de 20 bytes.
    2. Generar un 'str' de 4 bytes ("Truncamiento Dinámico").
        - Usando el valor HMAC-SHA1 anterior.
        - Será un 'str' de 4 bytes a partir del byte 'hash[offset]'.
    3. Computar el Valor HTOP.
        - Convertir el 'str' anterior a un entero.
        - Aplicarle módulo 10^'d', siendo 'd' la cantidad de dígitos (en este caso d = 6).
    
    * Extraído de la sección 5.3 del RFC 4226.
    """

    # Devolver el código como str
    return "{:06d}".format(code)

# ---------------------------------------------------- #

if __name__ == "__main__":
    # Leer los argumentos de la línea de comandos
    shared_key_file, coded_file, qr = read_arg()

    # Si se solicitó generar una clave (-g)
    if shared_key_file:
        if validate_file(shared_key_file):
            # Almacenar la clave en un fichero .key
            with open("ft_otp.key", "w") as f:
                f.write(key)
            
            print("Clave guardada en ft_otp.key")

            # Cifrar el fichero con la clave
            AES().code_file("ft_otp.key")

            print("El fichero ft_otp.key se ha cifrado con contraseña")
        else:
            exit(1)
    
    # Si se solicitó generar un código temporal (-k) o mostrar el QR de la clave (-qr)
    elif coded_file or qr:
        # Usar el fichero recibido por cualquiera de las dos opciones
        file = coded_file if coded_file else qr # El fichero es el mismo pero se recibe de distinta forma

        # Verificar que el fichero cifrado existe y tiene permiso de lectura
        if not (os.path.isfile(file) or os.access(file, os.R_OK)):
            print("Error: el fichero no existe o no tiene permiso de lectura")

            exit(1)
        
        else:
            # Extraer la clave del fichero
            key = AES().read_file(file)

            # Si se solicitó generar una contraseña (-k)
            if coded_file:
                # Generar y mostrar el código OTP
                print("Código generado:", generate_OTP(key))

            # Si se solicitó un QR (-qr)
            else:
                # Generar y mostrar el QR
                print("QR con la clave:")
                qrcode_terminal.draw(key)

    else:
        print("No se ha introducido ninguna opción")    
        exit(1)