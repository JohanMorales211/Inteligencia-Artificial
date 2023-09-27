import speech_recognition as sr
import pyttsx3
import pywhatkit
import urllib.request
import json
import datetime
import wikipedia
import openai
import calendar

name = 'cortana'

# your api key
openai.api_key = "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"

# your YouTube API key
key = "your_api_key"

flag = 1

listener = sr.Recognizer()

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# editing default configuration
engine. setProperty('rate', 178)
engine.setProperty('volume', 0.7)

def ask_openai(question):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=question,
        max_tokens=2048,
        n = 1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]


def calculate(expression):
    try:
        result = eval(expression)
        return result
    except:
        return "Lo siento, no pude entender la expresión matemática que me diste"


def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    flag = 1
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            voice = listener.listen(source)
            rec = listener.recognize_google(voice, language='es-ES')
            rec = rec.lower()
            
            if name in rec:
                rec = rec.replace(name, '')
                flag = run(rec)
            else:
                talk("Vuelve a intentarlo, no reconozco: " + rec)
    except:
        pass
    return flag

def run(rec):
    if 'reproduce' in rec:
        music = rec.replace('reproduce', '')
        talk('Reproduciendo ' + music)
        pywhatkit.playonyt(music)
    elif 'cuantos suscriptores tiene' in rec:
        name_subs = rec.replace('cuantos suscriptores tiene', '')
        data = urllib.request.urlopen(f'https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername={name_subs.strip()}&key={key}').read()
        subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
        talk(name_subs + " tiene {:,d}".format(int(subs)) + " suscriptores!")
    elif 'hora' in rec:
        hora = datetime.datetime.now().strftime('%I:%M %p')
        talk("Son las " + hora)
    elif 'busca' in rec:
        order = rec.replace('busca', '')
        wikipedia.set_lang("es")
        info = wikipedia.summary(order, 1)
        talk(info)
    elif 'salir' in rec:
        flag = 0
        talk("Saliendo...")
    elif 'pregunta' in rec:
        question = rec.replace('pregunta', '')
        answer = ask_openai(question)
        talk(answer)
    elif 'calcula' in rec:
        expression = rec.replace('calcula', '')
        result = calculate(expression)
        talk("El resultado es: " + str(result))
    elif 'el tiempo en' in rec:
        city = rec.replace('el tiempo en', '')
        # your API key here
        api_key = "your_api_key"
        # base_url variable to store url 
        base_url = "http://api.openweathermap.org/data/2.5/weather?" 
        complete_url = base_url + "appid=" + api_key + "&q=" + city 
        response = urllib.request.urlopen(complete_url) 
        x = response.read() 
        y = json.loads(x) 
        current_temperature = y["main"]["temp"] 
        current_pressure = y["main"]["pressure"] 
        current_humidity = y["main"]["humidity"] 
        talk("Temperatura en " + city + " es " +
                                    str(current_temperature) + 
                            " grados Kelvin, presión atmosférica es " +
                                    str(current_pressure) + " hPa y humedad es " +
                                    str(current_humidity) + "%")
    elif 'calendario' in rec:
        yy = datetime.datetime.now().year
        mm = datetime.datetime.now().month
        talk("El calendario para el mes de " + calendar.month_name[mm] + " es:")
        print(calendar.month(yy, mm))
    elif 'recordatorio' in rec:
        reminder = rec.replace('recordatorio', '')
        talk("Se ha guardado el recordatorio: " + reminder)
    elif 'busca archivo' in rec:
        file = rec.replace('busca archivo', '')
        # your code
        talk("Se ha encontrado el archivo: " + file)
    elif 'controla dispositivo' in rec:
        device = rec.replace('controla dispositivo', '')
        # your code
        talk("Se ha controlado el dispositivo: " + device)
    else:
        talk("Vuelve a intentarlo, no reconozco: " + rec)
    return flag

while flag:
    flag = listen() # Aquí agregué un comentario para evitar que se muestre la respuesta en la consola.