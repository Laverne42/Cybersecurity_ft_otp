# Cybersecurity_ft_otp
Proyecto ft_otp del Bootcamp de Ciberseguridad Campus 42 Málaga.<p> 
Basado en el código de https://github.com/15Galan

Un programa que, partiendo de una clave en formato hexadecimal de un mínimo de 64 caracteres, 
genera una clave OTP (30 segundos).
La semilla (clave inicial) se recibe por argumentos almacenada en un archivo sin cifrar.
El programa la lee, la cifra y la almacena en un nuevo archivo tras pedir una contraseña al usuario.
Para obtener la OTP el usuario introduce la contraseña elegida, que hace que el programa desencripte
la seed, la descifre, la lea y la vuelva a almacenar cifrada. Si el resultado es correcto, se genera
la OTP. 
También se puede pedir un código QR por terminal con la flag correspondiente que enlaza a la
seed cifrada.

- Almacenamos una frase o texto en claro en un archivo (text.txt).
- Pasamos el texto guardado a una semilla en hexadecimal (mínimo de 64 caracteres):<p>
  xxd -p -c256 text.txt > hextext.txt
- Ciframos el archivo con contraseña. El programa solicita una clave de 16 caracteres:<p>
  python3 ft_otp.py -g hextext.txt<p>
  Esto genera un archivo ft_otp.key cifrado con contraseña.
- Ejecutamos el programa con la flag -k para generar nuestra clave OTP:<p>
  python3 ft_otp.py -k ft_otp.key<p>
  Introducimos la contraseña creada anteriormente y se nos muestra la clave OTP por pantalla (validez de 30 segundos).
- Con la flag -qr se muestra por pantalla un código QR con la semilla en hexadecimal.
