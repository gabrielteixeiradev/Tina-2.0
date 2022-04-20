from email.mime import audio
import speech_recognition as sr
import pyttsx3
#Criar um reconhecedor de voz
r = sr.Recognizer()
maquina = pyttsx3.init()
maquina.say('Olá, sou a Tina, sua serva virtual!')
maquina.say('como posso ajudar?')
maquina.runAndWait()

def executa_comando():

    #abrir o microfone para captura de audio
    with sr.Microphone() as source:
        print("Escutando...") #mensagem de inicio
        while True:
            audio = r.listen(source) #captura o audio
            print(r.recognize_google(audio, language='pt-BR')) #faz a transcrição do audio
            audio = audio.lower()
            if "Tina" in audio:
                audio = audio.replace("Tina", "")
                print(audio)
                
