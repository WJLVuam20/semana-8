from controllers import citizenHandler
from transcriptor import transcribe_audio

def menu():
    handler = citizenHandler.CitizenHandler()

    while True:
        print("\n--- MENÚ VENTANILLA ---")
        print("1. Ingresar ciudadano")
        print("2. Mostrar siguiente ciudadano")
        print("3. Atender ciudadano")
        print("4. Salir")
        print("\nPuedes hablar o escribir tu opción:")

        opcion = transcribe_audio() or input("Opción: ")

        match opcion:
            case "1" | "uno":
                handler.add_citizen()
            case "2" | "dos":
                print("Siguiente ciudadano:")
                print(handler.show_next_citizen())
            case "3" | "tres":
                handler.serve_citizen()
            case "4" | "cuatro":
                print("Saliendo...")
                break
            case _:
                print("Opción no válida.")

if __name__ == "__main__":
    menu()
