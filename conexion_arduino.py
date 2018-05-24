import serial

activo = True

try:
    serial_out = serial.Serial("/dev/ttyACM0", 9600)
    print("Se conectó a /dev/ttyACM0")
except:
    try:
        serial_out = serial.Serial("/dev/ttyACM1", 9600)
        print("Se conectó a /dev/ttyACM1")
    except:
        activo = False
        print("No se conectó al Arduino")

def enviardato(dato):

    if activo:
        # dato = dato.encode('UTF-8')  # Se convierte a bits
        serial_out.write(dato)


def cerrar_conexion():

    if activo:
        serial_out.write(b'5')
        serial_out.close()
