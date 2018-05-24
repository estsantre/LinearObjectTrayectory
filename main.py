import deteccion_color
import conexion_arduino

while True:

    entrada = input(">>>")

    if entrada in ["azul", "rojo", "verde"]:
        print("INICIA")
        deteccion_color.seguir_color(entrada)

    elif entrada == "c":
        conexion_arduino.cerrar_conexion()
        break
