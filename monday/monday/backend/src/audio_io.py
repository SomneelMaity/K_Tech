import speech_recognition as sr

def listen_once(language="en-US"):
    recognizer = sr.Recognizer()
    
    recognizer.pause_threshold = 3
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=0.7)
        print("Hello Sir, Monday here, how can i help you today?")
        audio = recognizer.listen(source, timeout=None, phrase_time_limit=None)
        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio, language=language)
            return text.strip()
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None