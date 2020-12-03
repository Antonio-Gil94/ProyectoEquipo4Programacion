from PIL import Image                   #Importamos libreria
import math                             #Importamos libreria

#========================================== FUNCIONES =========================================================================

class color:
   BOLD = '\033[1m'
   END = '\033[0m'
img = Image.open('proyimag1T.png')                              #Img es igual a la imagen abierta con open
caracter_terminacion = [1, 1, 1, 1, 1, 1, 1, 1]


def RepresentacionAsci(caracter): # Convierte cada letra al número que le corresponde en el código ASCII
    return ord(caracter)


def RepresentacionBinaria(numero): # Cada código es convertido a binario
    return bin(numero)[2:].zfill(8)


def cambiar_ultimo_bit(byte, nuevo_bit): # Por cada bit en ese byte creamos una lista
    return byte[:-1] + str(nuevo_bit)


def binario_a_decimal(binario): # Cambia de binario a decimal
    return int(binario, 2)


def CambioColor(color_original, bit): # Cambia el color para que el texto se camufle en la imagen
    color_binario = RepresentacionBinaria(color_original)
    color_modificado = cambiar_ultimo_bit(color_binario, bit)
    return binario_a_decimal(color_modificado)


def ListaBytes(texto): # Crea una lista con los bytes de la imagen
    lista = []
    for letra in texto:
        representacion_ascii = RepresentacionAsci(letra)
        representacion_binaria = RepresentacionBinaria(representacion_ascii)
        for bit in representacion_binaria:
            lista.append(bit)
    for bit in caracter_terminacion:
        lista.append(bit)
    return lista



def obtener_lsb(byte): # Obtiene el lsb de la imagen
    return byte[-1]

def ocultar_texto(mensaje, ruta_imagen_original, ruta_imagen_salida="proyimod1T.png"): # Modifica la imagen para que el texto se pueda camuflar
    
    imagen = Image.open(ruta_imagen_original)
    pixeles = imagen.load()
    tamaño = imagen.size
    anchura = tamaño[0]
    altura = tamaño[1]
    lista = ListaBytes(mensaje)
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
                    RojoModf = CambioColor(rojo, lista[contador])
                    contador += 1
                else:
                    RojoModf = rojo

                if contador < longitud:
                    VerdeModf = CambioColor(verde, lista[contador])
                    contador += 1
                else:
                    VerdeModf = verde

                if contador < longitud:
                    AzulModf = CambioColor(azul, lista[contador])
                    contador += 1
                else:
                    AzulModf = azul

                pixeles[x, y] = (RojoModf, VerdeModf, AzulModf)
            else:
                break
        else:
            continue
        break

    imagen.save(ruta_imagen_salida)



def caracter_desde_codigo_ascii(numero): # Devuelve los caracteres desde el código ASCII
    return chr(numero)


def escala_grises(): # Cambiar la imagen a escala de grises
    f = Image.open('proyimag1T.png').convert('L')
    f.show()
    f.save('imagen_EscalaGrises.png', 'png')
    f.close()





def leer(ruta_imagen): # Lee el tamaño, anchura y altura de la imagen
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


            byte += obtener_lsb(RepresentacionBinaria(rojo))
            if len(byte) >= 8:
                if byte == caracter_terminacion:
                    break
                mensaje += caracter_desde_codigo_ascii(binario_a_decimal(byte))
                byte = ""

            byte += obtener_lsb(RepresentacionBinaria(verde))
            if len(byte) >= 8:
                if byte == caracter_terminacion:
                    break
                mensaje += caracter_desde_codigo_ascii(binario_a_decimal(byte))
                byte = ""

            byte += obtener_lsb(RepresentacionBinaria(azul))
            if len(byte) >= 8:
                if byte == caracter_terminacion:
                    break
                mensaje += caracter_desde_codigo_ascii(binario_a_decimal(byte))
                byte = ""

        else:
            continue
        break
    return mensaje


def Pixeles(ruta_imagen_original): # Para medir la anchura y altura de los píxeles
            f = Image.open(ruta_imagen_original)
            pixeles = f.load()
            tamaño = f.size
            anchura = tamaño[0]
            altura = tamaño[1]
            f.close()
            print(color.BOLD + 'Proyimag1T.png tiene un {} de ancho y {} de alto'.format(anchura, altura) + color.END)


def menu(): # Menú visual del código
    correcto = False
    num = 0
    while (not correcto):
        try:
            num = int(input('Elija una opción: '))
            correcto = True
        except ValueError:
            print('Error, elija de nuevo la opción: ')
    return num

#===================================================== VARIABLES =============================================================================

salir = False
opcion = 0

#===================================================== EJECUCION ============================================================================

while not salir:

    print('\033[1m' + 'PROYECTO ESTEGANO'.center(165) + '\033[0m')
    print('==================='.center(165))
    print()
    print('1) Insertar mensaje oculto en una imagen'.center(165))
    print('2) Extraer mensaje oculto de una imagen'.center(165))
    print('3) Convertir la imagen a escala de grises'.center(168))
    print('4) Salir'.center(134))
    print()

    opcion = menu()

    if opcion == 4:
        salir = True

    if opcion == 1:
        print()
        print(color.BOLD + "OPCIÓN: Insertar mensaje oculto en una imagen" + color.END)
        oculto = input(color.BOLD + "Introduzca el mensaje de texto a ocultar: " + color.END)
        Pixeles("proyimag1T.png")
        print(color.BOLD + "Insertando el texto en la imagen..." + color.END)
        print(color.BOLD + "El fichero proyimod1T.png es diferente a proyimag1T.png" + color.END)
        ocultar_texto(oculto, "proyimag1T.png")
        print()
        img.show()

    if opcion == 2:
        print()
        print(color.BOLD + "OPCIÓN: Extraer mensaje oculto de una imagen" + color.END)
        print(color.BOLD + "El fichero de la imagen con texto se llama: proyimod1T.png " + color.END)
        print(color.BOLD + "Extrayendo el texto de la imagen..." + color.END)
        mensaje = leer("proyimod1T.png")
        print(color.BOLD + "El mensaje oculto es: " + oculto + color.END)
        img.show()
        print()

    if opcion == 3:
        print()
        print(color.BOLD + "OPCIÓN: Convertir la imagen a escala de grises" + color.END)
        print(color.BOLD + "El fichero de la imagen se llama: proyimag1T.png" + color.END)
        print(color.BOLD + "Convirtiendo la imagen a escala de grises..." + color.END)
        escala_grises()
        print()
