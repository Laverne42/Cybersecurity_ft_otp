from getpass import getpass
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Implementación de cifrado/descifrado con AES en modo cbc
class Cripta:

    # Variables
    KEY = None
    SEED = None
    BLOCK = None

    # Constructor de la clase
    def __init__(self):
        self.SEED = "cb71De88D9ab1640".encode("utf-8")
        self.BLOCK = 16 # Tamaño de bloque: 128 bits 
    
        """
        El cifrado AES en modo cbc requiere una clave, 
        un vector de inicialización (semilla) y un tamaño de blouque, todos de 16 bytes

        """

    # Cifra un texto usando AES en modo cbc con vector de inicialización SEED
    def code(self, text):
        # Solicitar clave al usuario
        self.KEY = getpass("Introduce una contraseña: ").encode("utf-8")

        # Validar longitud de la clave
        if len(self.KEY) != 16:
            print ("La clave debe ser de 16 caracteres")
            exit (1)

        # Mecanismo de cifrado
        coder = AES.new(self.KEY, AES.MODE_CBC, self.SEED)

        # Cifrado de tal forma que los mensajes sean múltiplo del tamaño de bloque
        return coder.encrypt(pad(text.encode("utf-8"), self.BLOCK))

    # Descifra un texto usando AES en modo cbc con un vector de inicialización SEED  
    def decode(self, hidden_text):
        # Pedir una clave al usuario
        self.KEY = getpass("Introduce la contraseña: ").encode("utf-8")

        # Validar longitud de la clave
        if len(self.KEY) != 16:
            print:("La clave debe ser de 16 caracteres")
            exit (1)
        
        try:
            # Mecanismo de descifrado
            decoder = AES.new(self.KEY, AES.MODE_CBC, self.SEED)

            # Desciframos, eliminamos padding y recuperamos la cadena
            return unpad(decoder.decrypt(hidden_text), self.BLOCK).decode("utf-8", "ignore")
        
        except:
            print("Contraseña incorrecta")
            exit(1)
    
    # Cifra un fichero usando AES en modo cbc con un vector de inicialización SEED
    def code_file(self, file):
        # Leer el contenido del fichero
        with open(file, "r") as f:
            content = f.read()

        # Cifrar el contenido
        hidden = self.code(content)

        # Escribir el contenido cifrado en el fichero (bytes)
        with open(file, "wb") as f:
            f.write(hidden)

        # Texto escrito en el fichero
        return hidden
    
    # Descifra un fichero usando AES en modo cbd con un vector de inicialización SEED
    def decode_file(self, file):
        #Leer el contenido del fichero (bytes)
        with open(file, "rb") as f:
            content = f.read()

        # Descifrar el contenido del fichero
        text = self.decode(content)

        # Escribir el contenido (en claro) en el fichero
        with open(fichero, "w") as f:
            f.write(text)
        
        # Texto escrito en el fichero
        return text
    
    # Lee el contenido de un fichero cifrado
    def read_file(self, file):
        # Leer el contenido del fichero
        with open(file, "rb") as f:
            content = f.read()

        # Descifrar el contenido del fichero
        text = self.decode(content)

        # Texto escrito en el fichero
        return text

