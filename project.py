############################################################################################################################
#Importy
import speech_recognition as sr
import pyttsx3
import keyboard
import spotipy
import spotipy.util as util
import ply.lex as lex
import ply.yacc as yacc
############################################################################################################################
#Dane dla spotify'a
client_id = 'placeholder'
client_secret = 'placeholder'
redirect_uri = 'http://localhost:8888/callback/'
scope = 'user-modify-playback-state'
############################################################################################################################
#Stworzenie instancji
recognizer = sr.Recognizer()

engine = pyttsx3.init()
engine.setProperty("voice", engine.getProperty('voices')[1].id)

token = util.prompt_for_user_token(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth=token)
############################################################################################################################
#Definicja komend i ich obsługiwanie
tokens = (
    'STOP',
    'PLAY',
    'SKIP',
    'BACK',
    'VOLUME',
    'VALUE',
    )

def t_STOP(t):
    r'pause | stop'
    return t

def t_PLAY(t):
    r'resume | play | start'
    return t

def t_SKIP(t):
    r'skip | next'
    return t

def t_BACK(t):
    r'back | previous'
    return t

def t_VOLUME(t):
    r'volume'
    return t

def t_VALUE(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    t.lexer.skip(1)

t_ignore  = ' \t'

def p_stop(p):
    'command : STOP'
    sp.pause_playback()
    SpeakText("Done.")

def p_play(p):
    'command : PLAY'
    sp.start_playback()
    SpeakText("Done.")

def p_skip(p):
    'command : SKIP'
    sp.next_track()
    SpeakText("Done.")

def p_back(p):
    'command : BACK'
    sp.previous_track()
    SpeakText("Done.")

def p_volume(p):
    'command : VOLUME VALUE'
    value = p[2]
    sp.volume(value)
    SpeakText("Done.")

def p_error(p):
    SpeakText("Error: Wrong command. Try again.")

lexer = lex.lex()
parser = yacc.yacc()
############################################################################################################################
#Funkcje
def VoiceTranscription():
    with sr.Microphone() as source:
        SpeakText("Recording...")
        audio_data = recognizer.record(source, duration=5)
        print("Recognizing...")
        text = recognizer.recognize_google(audio_data, language = "en-US")
    return text

def SpeakText(text):
    engine.say(text)
    print(text)
    engine.runAndWait()
############################################################################################################################
#Program
SpeakText("Good morning.")
SpeakText("Press 's'+'l' to give a voice command or press 's'+'escape' to end program.")
while True:
    if keyboard.is_pressed('s+l'):
        try:
            text = VoiceTranscription()
            print(f"Transcription: {text}")
            parser.parse(text)
            print("Press 's'+'l' to give a voice command or press 's'+'escape' to end program.")
        except:
            SpeakText("Error: Something went wrong while recognizing text. Try again.")
            print("Press 's'+'l' to give a voice command or press 's'+'escape' to end program.")
    elif keyboard.is_pressed('s+esc'):
        SpeakText("Goodbye.")
        break
