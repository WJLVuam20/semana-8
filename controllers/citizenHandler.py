from models import classes
from transcriptor import transcribe_audio


class CitizenHandler:
    def __init__(self):
        self.citizens = classes.Queue()
    
    def add_citizen(self, citizen=None):
        if citizen:
            self.citizens.enqueue(citizen)
        else:           
            print("Di o escribe la cédula:")
            cedula = transcribe_audio() or input("Cédula: ")

            print("Di o escribe el nombre completo:")
            nombre = transcribe_audio() or input("Nombre: ")

            print("Di o escribe el trámite:")
            tramite = transcribe_audio() or input("Trámite: ")

            print("Di o escribe la hora de llegada (ej. 10:30):")
            hora = transcribe_audio() or input("Hora: ")

            nuevo_ciudadano = classes.Citizen(cedula, nombre, tramite, hora)
            self.citizens.enqueue(nuevo_ciudadano)
    
    def show_next_citizen(self):
        return self.citizens.peek()
    
    def serve_citizen(self):
        self.citizens.dequeue()