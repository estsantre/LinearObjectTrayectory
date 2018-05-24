from multiprocessing import Process, Event
import deteccion_color
import conexion_arduino

event = None

while True:

    entrada = input(">>>")

    if entrada in ["azul", "rojo", "verde"]:
        print("INICIA")
        event = Event()
        p1 = Process(target=deteccion_color.seguir_color, args=(event, entrada))
        p1.start()

    elif entrada == "e":
        print("FIN")
        if event:
            event.set()
        break

    elif entrada == "c":
        conexion_arduino.cerrar_conexion()
        break
