import time
import pyttsx3
import speech_recognition as sr
import eel

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')       #getting details of current voice
    engine.setProperty('voice', voices[0].id)   #changing index, changes voices. 1 for female
    engine.setProperty('rate', 174)             # setting up new voice rate
    #print(voices)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()


@eel.expose
def takecommand():
    r=sr.Recognizer()
    
    with sr.Microphone() as source:
        print("listening....")
        eel.DisplayMessage("listening....")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio=r.listen(source,10,6)
    
    try:
        print("Recognizing")
        eel.DisplayMessage("Recognizing....")
        query=r.recognize_google(audio,language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        #speak(query)
        #eel.ShowHood()
    except Exception as e:
        return ""
    
    return query.lower()

@eel.expose
def allCommands():
    
    query=takecommand();
    print(query)
    
    if "open" in query:
        from engine.features import openCommand
        openCommand(query)
    elif "on youtube" in query:
        from engine.features import PlayYoutube
        PlayYoutube(query)
    else:
        print("not run")
    eel.ShowHood()
    query="Hello, I am CHANAKYA"
    eel.DisplayMessage(query)


#text = takecommand()       

#speak(text)