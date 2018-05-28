import serial

active = True

try:
    serial_out = serial.Serial("/dev/ttyACM0", 9600)
    print("Se conectó a /dev/ttyACM0")
except:
    try:
        serial_out = serial.Serial("/dev/ttyACM1", 9600)
        print("Se conectó a /dev/ttyACM1")
    except:
        active = False
        print("No se conectó al Arduino")


#Función para enviar datos
def send_serial(data):

    if active:
        data = "{0}\n".format(data)
        serial_out.write(bytes(data, encoding='utf-8'))

def close_connection():

    if active:
        send_serial("50")
        serial_out.close()
