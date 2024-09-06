import speech_recognition as sr
import pyttsx3
import webbrowser
import music
import requests
from datetime import datetime 

import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()
'''
Is developing a virtual assistant project called Nova using Python,
which includes functionalities for music playback, weather information retrieval,
news fetching, date and time reporting, web browsing, and activation/deactivation commands.

1-activate on wake up call ___________________-Nova
 -need to activate once 
 -For deactivation say________________________-Stop

2-for music - say "play music" 
 -will play a specific song on________________-play {songname} - OR - {songname}

3-For weather - say "weather" or "give weather reports" :
 -will play a weather of specific city on_____-weather in {cityname} - OR - {cityname}

4-for news - say "news" or "tell news" :
 -can stop news in between by saying _________-{stop reading} - OR  -{pause}

5-For interactive news reading:
 -NOVA itself, ask to keep reading news or not after 3 headlines
                               Choose _______- {yes} - OR - - {No} 
6-For date and time:
     - Say "current time" to get the current time.
     - Say "current date" to get today's date.                               

'''
def speak(text):
    engine = pyttsx3.init()
    #rate = engine.getProperty('rate')   # getting details of current speaking rate
    #print (rate)  
    engine.setProperty('rate', 150) 
    engine.say(text)
    engine.runAndWait()

def listen_command():
    try:
        
        rec=sr.Recognizer()
        with sr.Microphone() as source:
            print('listening')
            rec.adjust_for_ambient_noise(source ,duration=1)
            audio=rec.listen(source,phrase_time_limit=2)
            
        print('recognising')
  

        text=rec.recognize_google(audio, language='en-IN') 
        return text.lower().strip()  # jisse neeceh na kern apadhe
                             
    except sr.UnknownValueError:
            print("Sorry, I did not understand that.") 
            return ""
    except Exception as e:
            print(f"Error {e}")   
            return ""

def play_music(song):
                    link = music.music_dict.get(song)#using get wont give key error if no data in song

                    if link: # means true h jab
                        webbrowser.open(link)
                        
                    else:
                        print(f"Song '{song}' not found in the music library.")
                        speak(f"Sorry, I couldn't find the song '{song}' .")


def get_weather(city):
    # Get the API key from environment variables
    weather_api_key = os.getenv("WEATHER_API_KEY")

    if not weather_api_key:
        print("API key for weather service is not set.")
        speak("Sorry, I couldn't get the weather information at the moment.")
        return

    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city.title()}&appid={weather_api_key}&units=metric"

    try:
        resp = requests.get(weather_url)
        data = resp.json()

        if resp.status_code == 200:
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            city_name = data['name']

            weather_info = f"Current weather in {city_name}: {weather_description}. Temperature: {temperature} degrees Celsius."
            print(weather_info)
            speak(weather_info)

        else:
            print(f"Failed to get weather data. Status code: {resp.status_code}")
            speak("Sorry, I couldn't get the weather information at the moment.")

    except Exception as e:
        print(f"Error getting weather data: {e}")
        speak("Sorry, I couldn't get the weather information at the moment.")
     


def get_news(): 
         
        speak(".....Let me get the latest news for you.....")
        newsapi_key = os.getenv("NEWS_API_KEY")

        if not newsapi_key:
            print("API key for news service is not set.")
            speak("Sorry, I couldn't get the news at the moment.")
            return

        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi_key}"
          
        try:
            resp=requests.get(url)
            if resp.status_code == 200 :
                 news_data= resp.json() 
                 articles=news_data["articles"]# will retrive a list of article , in that present, list of multiple dictionary 

                 for index,article in enumerate(articles,start=1):
                    title=article["title"]  # iterate over that list inside dict and give title
                    print(f"News {index}: {title}")
                    speak(f"News {index}: {title}") 

                    # Provide periodic updates to the user
                    if index % 3 == 0:  # Update every 3 news items
                        speak("I am still reading the news... Please wait.")

                        # Check if user wants to do something else
                        speak("Would you like to do something else while I continue with the news?")

                        while True:
                            response = listen_command()
                            if "yes" in response:
                                print(f"----you said-----{response}")
                                speak("Okay, let me know when you're ready to continue.")
                                return  # Exit the news fetching if user wants to do something else
                            elif "no" in response:
                                print(f"----you said-----{response}")
                                break
                            else:
                                speak("Sorry, I didn't catch that. Would you like to do something else?")


                    # Check for interruption command during speech
                    command = listen_command()
                    if "stop reading" in command or "pause" in command:
                        speak("Stopping news update.")
                        break
            else:
                print(f"Failed to get news. Status code: {resp.status_code}")
                speak("Sorry, I couldn't get the news at the moment.")

        except Exception as e:
            print(f"Error fetching news: {e}")
            speak("Sorry, I couldn't get the news at the moment.")

def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")     # 10:30:26
    speak(f"The current time is {current_time}")

def get_date():
    now = datetime.now()
    current_date = now.strftime("%A, %B %d, %Y")  # E.g., "Monday, July 13, 2024"
    speak(f"Today is {current_date}")


def handel_command(c):
     if  "open google" in c  :
          speak("......Opening Google........ ")
          webbrowser.open("https://www.google.com")                
     elif  "open youtube" in c  :
          speak("......linkedine Opening........ ")
          webbrowser.open("https://www.linkedine.com")                
     elif  "open facebook" in c  :
          speak("......facebook Opening........ ")
          webbrowser.open("https://www.linkedin.com")                
     elif  "open linkedin" in c  :
          speak("......linkedin Opening........ ")
          webbrowser.open("https://www.linkedin.com")                
     elif  "open instagram" in c  :
          speak("......instagram Opening........ ") 
          webbrowser.open("https://www.instagram.com")

     elif "play music" in c:
           speak(".....Which song you want me to play..... ")
           while True :
                command_3 = listen_command() # command---play {song name} like play lover
                print(f"............did u say........ {command_3}.........") 
                if command_3 and command_3.startswith("play")  :
                    song = " ".join(command_3.split(" ")[1:]) #Join all words after "play"
                    play_music(song)
                    break

                elif command_3 :  
                    song = command_3.strip()  # unwanted space na aaye
                    play_music(song)
                    break
                    
                else:
                    print(f"Please specify a song name")
                    speak(f"Please specify a song name.")   

     elif "weather" in c:
        speak("......Sure, which city's weather would you like to know?........")
        # Giving command ---- weather or gimme weather reports
        while True :
            command_4 = listen_command() # here give command --weather in delhi/mumbai
            print(f"............did u say........ {command_4}.........")
            
            # Check if the city name is non empty string          
                                          #do this          # @ todoooo yahi sahi hoga kerna and if "weather in" in command_4 bhi sahi hoga
            if command_4 and len(command_4.split(" ") ) >=3 :  #  @is startswith("weather in") kerke bhi ker sakte h
                                                             # " ".join(command_4.split(" ")[2:] )  yeh string hogi not list 
                    city = " ".join(command_4.split(" ")[2:] )
                    get_weather(city)                    
                    break  
                                                         
            elif command_4 : # " ".join(command_4.split(" ")[2:] )  yeh string hogi not list 
                    city =command_4.strip()                 
                    get_weather(city)                    
                    break

            # elif city== "" empty string        
            else:          
                print("......Please specify the city to get the weather information......")
                speak("......Please specify the city to get the weather information......")

     elif "news" in c:
         get_news()

     elif "time" in c:
        get_time()
     elif "date" in c:
        get_date()

if __name__ == "__main__":

    speak("Initializing complete ,  Hello i am Nova.....")

    while True:
       command = listen_command()   
       print(f"............Nova not Activated........ {command}")
       if "nova" in command or command== 'nova': 

            print(f"............Nova Activated........ {command}")  
        
            speak("............Nova Activated........  ")    

            while True :
                command_2 = listen_command()
                print(f"............waiting for command........ {command_2}") 
                if 'stop' in command_2 or command_2 == "stop" :
                    print(f"............Nova deavtivated........ {command_2}")
                    speak("............Nova DEactivated........  ") 
                    break

                handel_command(command_2)
