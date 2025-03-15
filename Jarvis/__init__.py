import speech_recognition as sr
import pyttsx3
import threading
import keyboard  # ✅ Import keyboard to detect Ctrl key

from Jarvis.features import date_time
from Jarvis.features import launch_app
from Jarvis.features import website_open
from Jarvis.features import weather
from Jarvis.features import wikipedia
from Jarvis.features import news
from Jarvis.features import send_email
from Jarvis.features import google_search
from Jarvis.features import google_calendar
from Jarvis.features import note
from Jarvis.features import system_stats
from Jarvis.features import loc
from Jarvis.features.deepseek_integration import query_deepseek


class JarvisAssistant:
    def __init__(self):
        """Initialize the assistant and speech engine."""
        self.engine = pyttsx3.init('sapi5')
        self.engine.setProperty('rate', 200)  # Adjust speech speed
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        self.speech_lock = threading.Lock()
        self.stop_speaking = False  # ✅ Flag to stop speaking

    def mic_input(self):
        """
        Fetch input from mic.
        Returns: user's voice input as text if recognized, False if failed.
        """
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("🎙️ Listening....")
                r.energy_threshold = 4000
                audio = r.listen(source)
            try:
                print("🔎 Recognizing...")
                command = r.recognize_google(audio, language='en-in').lower()
                print(f'You said: {command}')
            except:
                print('⚠️ Please try again')
                command = self.mic_input()
            return command
        except Exception as e:
            print(e)
            return False

    def tts(self, text):
        """
        Speak text fluently and stop when Ctrl is pressed.
        """
        self.stop_speaking = False  # Reset stop flag

        def check_ctrl_key():
            """Listen for Ctrl key press and stop speech."""
            while self.engine.isBusy():  # While speaking
                if keyboard.is_pressed("ctrl"):  # ✅ Detect Ctrl key
                    print("Ctrl key pressed! Stopping speech...")
                    self.stop_speaking = True  # Set stop flag
                    return

        # Start Ctrl key detection in a separate thread
        stop_thread = threading.Thread(target=check_ctrl_key)
        stop_thread.daemon = True  # Auto-stop when main program stops
        stop_thread.start()

        # Speak the text normally
        with self.speech_lock:
            for sentence in text.split(". "):  # ✅ Split text into sentences
                if self.stop_speaking:  # ✅ Stop if Ctrl was pressed
                    break
                self.engine.say(sentence)
                self.engine.runAndWait()  # Speak one sentence at a time

    def tell_me_date(self):
        return date_time.date()

    def tell_time(self):
        return date_time.time()

    def launch_any_app(self, path_of_app):
        """Launch any Windows application."""
        return launch_app.launch_app(path_of_app)

    def website_opener(self, domain):
        """Open a website based on the domain."""
        return website_open.website_opener(domain)

    def weather(self, city):
        """Fetch weather for a given city."""
        try:
            return weather.fetch_weather(city)
        except Exception as e:
            print(e)
            return False

    def tell_me(self, topic):
        """Fetch Wikipedia information."""
        return wikipedia.tell_me_about(topic)

    def news(self):
        """Fetch top news of the day."""
        return news.get_news()

    def send_mail(self, sender_email, sender_password, receiver_email, msg):
        """Send an email."""
        return send_email.mail(sender_email, sender_password, receiver_email, msg)

    def google_calendar_events(self, text):
        """Fetch Google Calendar events."""
        service = google_calendar.authenticate_google()
        date = google_calendar.get_date(text)
        return google_calendar.get_events(date, service) if date else None

    def search_anything_google(self, command):
        google_search.google_search(command)

    def take_note(self, text):
        note.note(text)

    def system_info(self):
        return system_stats.system_stats()

    def location(self, location):
        current_loc, target_loc, distance = loc.loc(location)
        return current_loc, target_loc, distance

    def my_location(self):
        city, state, country = loc.my_location()
        return city, state, country
