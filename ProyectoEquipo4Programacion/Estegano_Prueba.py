from PIL import Image
import math
img = Image.open('.\proyimag1T.png')
caracter_terminacion = [1, 1, 1, 1, 1, 1, 1, 1]


def obtener_representacion_ascii(caracter):
	return ord(caracter)

def obtener_representacion_binaria(numero):
	return bin(numero)[2:].zfill(8)

def cambiar_ultimo_bit(byte, nuevo_bit):
	return byte[:-1] + str(nuevo_bit)

def binario_a_decimal(binario):
	return int(binario, 2)

def modificar_color(color_original, bit):
	color_binario = obtener_representacion_binaria(color_original)
	color_modificado = cambiar_ultimo_bit(color_binario, bit)
	return binario_a_decimal(color_modificado)

def obtener_lista_de_bits(texto):
	lista = []
	for letra in texto:
		representacion_ascii = obtener_representacion_ascii(letra)
		representacion_binaria = obtener_representacion_binaria(representacion_ascii)
		for bit in representacion_binaria:
			lista.append(bit)
	for bit in caracter_terminacion:
		lista.append(bit)
	return lista

#caracter_terminacion = "11111111"
def obtener_lsb(byte):
	return byte[-1]

def caracter_desde_codigo_ascii(numero):
	return chr(numero)

def ocultar_texto(mensaje, ruta_imagen_original, ruta_imagen_salida="salida.png"):
	print("Ocultando mensaje...".format(mensaje))
	imagen = Image.open(ruta_imagen_original)
	pixeles = imagen.load()

	tamaño = imagen.size
	anchura = tamaño[0]
	altura = tamaño[1]

	lista = obtener_lista_de_bits(mensaje)
	contador = 0
	longitud = len(lista)
	for x in range(anchura):
		for y in range(altura):
			if contador < longitud:
				pixel = pixeles[x, y]


				rojo = pixel[0]
				verde = pixel[1]
				azul = pixel[2]

				if contador < longitud:
					rojo_modificado = modificar_color(rojo, lista[contador])
					contador += 1
				else:
					rojo_modificado = rojo

				if contador < longitud:
					verde_modificado = modificar_color(verde, lista[contador])
					contador += 1
				else:
					verde_modificado = verde

				if contador < longitud:
					azul_modificado = modificar_color(azul, lista[contador])
					contador += 1
				else:
					azul_modificado = azul

				pixeles[x, y] = (rojo_modificado, verde_modificado, azul_modificado)
			else:
				break
		else:
			continue
		break

	if contador >= longitud:
		print("Mensaje escrito correctamente")
	else:
		print("Advertencia: no se pudo escribir todo el mensaje, sobraron {} caracteres".format( math.floor((longitud - contador) / 8) ))

	imagen.save(ruta_imagen_salida)


def leer(ruta_imagen):
	imagen = Image.open(ruta_imagen)
	pixeles = imagen.load()

	tamaño = imagen.size
	anchura = tamaño[0]
	altura = tamaño[1]

	byte = ""
	mensaje = ""

	for x in range(anchura):
		for y in range(altura):
			pixel = pixeles[x, y]

			rojo = pixel[0]
			verde = pixel[1]
			azul = pixel[2]


			byte += obtener_lsb(obtener_representacion_binaria(rojo))
			if len(byte) >= 8:
				if byte == caracter_terminacion:
					break
				mensaje += caracter_desde_codigo_ascii(binario_a_decimal(byte))
				byte = ""

			byte += obtener_lsb(obtener_representacion_binaria(verde))
			if len(byte) >= 8:
				if byte == caracter_terminacion:
					break
				mensaje += caracter_desde_codigo_ascii(binario_a_decimal(byte))
				byte = ""

			byte += obtener_lsb(obtener_representacion_binaria(azul))
			if len(byte) >= 8:
				if byte == caracter_terminacion:
					break
				mensaje += caracter_desde_codigo_ascii(binario_a_decimal(byte))
				byte = ""

		else:
			continue
		break
	return mensaje

def escala_grises():
    img = Image.open('proyimag1T.png').convert('L')
    img.show()
    img.save('imagen_EscalaGrises.png','png')

#--------------------------------------------------
def menu():
    correcto = False
    num = 0
    while (not correcto):
        try:
            num = int(input('Elija una opción: '))
            correcto = True
        except ValueError:
            print('Error, elija de nuevo la opción: ')
    return num

salir = False
opcion = 0
while not salir:
    print('\033[1m' + 'PROYECTO ESTEGANO'.center(165) + '\033[0m')
    print('==================='.center(165))
    print()
    print('1) Insertar mensaje oculto en una imagen'.center(165))
    print('2) Extraer mensaje oculto de una imagen'.center(165))
    print('3) Cnvertir la imagen a escala de grises'.center(165))
    print('4) Salir'.center(134))


    print()
    opcion = menu()
    if opcion == 4:
        salir = True
	
    if opcion == 1:
		ocultar_texto(input('Mensaje que quieres ocultar: '), ".\proyimag1T.png")
		img.show()
		
    if opcion == 2:

		mensaje = leer("salida.png")
		print("El mensaje oculto es:")
		print(mensaje)
		img.show()

    if opcion == 3:
		escala_grises()
