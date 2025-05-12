import speech_recognition as sr

def transcribe_audio():
    reconocedor = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ajustando ruido ambiental...")
        reconocedor.adjust_for_ambient_noise(source, duration=1)
        print("Habla ahora...")

        try:
            audio = reconocedor.listen(source, timeout=5, phrase_time_limit=10)
            print("Reconociendo...")
            texto = reconocedor.recognize_google(audio, language='es-ES')
            print(f"Texto reconocido: {texto}")
            return texto.lower()
        except sr.WaitTimeoutError:
            print("No se detectó audio.")
        except sr.UnknownValueError:
            print("No se entendió lo que dijiste.")
        except sr.RequestError as e:
            print(f"Error al conectar: {e}")
        except Exception as e:
            print(f"Otro error: {e}")
        return None
