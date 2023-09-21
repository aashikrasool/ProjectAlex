from tkinter import *
from tkinter import Button
import pyttsx3
import datetime
import speech_recognition as sr
import smtplib
from secret import senderemail, epwd, to
from email.message import EmailMessage
import pywhatkit
import wikipedia
import pyjokes
import requests
import clipboard
import PyPDF2
from tkinter.filedialog import *
import pyautogui
import webbrowser as wb
from tkinter import messagebox
from PIL import Image,ImageTk


import main

root = Tk()
root.title('Mr.Alex')
p1= PhotoImage(file= 'download.png')
root.iconphoto(False,p1)
root.geometry('900x900')


def click():
    engine = pyttsx3.init()

    def speak(audio):
        engine.say(audio)
        engine.runAndWait()

    def getvoices(voice):
        voices = engine.getProperty('voices')
        if voice == 1:
            engine.setProperty('voice', voices[0].id)
            speak("hello this is Mr.alex")
        if voice == 2:
            engine.setProperty('voice', voices[1].id)
            speak("hello this is  Mrs.alex")

    def time():
        Time = datetime.datetime.now().strftime("%I:%M:%S %p")
        speak("the current time is")
        speak(Time)

    def covid():
        speak("here the today's covid status in South Korea")
        wb.open('https://coronaboard.kr/en/')

    def news():
        speak("here the latest news in South Korea")
        wb.open('https://www.koreatimes.co.kr/www2/index.asp')

    def date():
        year = int(datetime.datetime.now().year)
        month = int(datetime.datetime.now().month)
        date = int(datetime.datetime.now().day)
        speak("the current date is")
        speak(date)
        speak(month)
        speak(year)

    def read():
        book = askopenfilename(title="add a pdf file")

        pdfReader = PyPDF2.PdfFileReader(book)
        pages = pdfReader.numPages
        for num in range(0, pages):
            speaker = pyttsx3.init()
            page = pdfReader.getPage(num)
            text = page.extractText()
            speaker.say(text)
            speaker.runAndWait()

    def sendEmail(receiver, subject, content):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(senderemail, epwd)
        email = EmailMessage()
        email['From'] = senderemail
        email['To'] = receiver
        email['Subject'] = subject
        email.set_content(content)
        server.send_message(email)
        server.close()

    def sendWhatsapp(phone_no, message):
        phone_no = phone_no
        Message = message
        pywhatkit.sendwhatmsg_instantly(phone_no, Message)

    # wb.open('https://web.whatsapp.com/send?phone=' + phone_no + '@text=' + Message)
    # sleep(10)
    # pyautogui.press('enter')

    def wishme():
        speak("welcome back to Alex!")
        time()
        date()
        speak("Mr.Alex is  at your service zone, How can I help you Sir")

    def greet():
        hour = datetime.datetime.now().hour
        if 6 <= hour < 12:
            speak("Good Morning Sir!")
        elif 12 <= hour < 18:
            speak("Good Afternoon Sir!")
        elif 18 <= hour < 24:
            speak("Good evening Sir!")
        else:
            speak("Good night Sir!")

    def takeCommand():
        query = input("How can I help you?")
        return query

    def takeCommandMic():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listning.....")
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            print("Recognizning.....")
            query = r.recognize_google(audio, language="en-IN")
            print(query)
        except Exception as e:
            print(e)
            speak("can you repeate it?")
            return "None "
        return query

    if __name__ == "__main__":
        getvoices(1)
        greet()
        wishme()
        while True:
            query = takeCommandMic().lower()
            if 'time' in query:
                time()

            elif 'date' in query:
                date()
            if 'play' in query:
                song = query.replace('play', '')
                speak('playing ' + song)
                pywhatkit.playonyt(song)
            elif 'joke' in query:
                speak(pyjokes.get_joke())
            elif 'who is' in query:
                person = query.replace('who is', '')
                info = wikipedia.summary(person, 1)  # line number to play
                print(info)
                speak(info)
            elif 'read' in query:
                read()
            elif 'weather' in query:
                # https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid=e45a2abe29c83791d0cc596744f76039
                api_key = "&appid=e45a2abe29c83791d0cc596744f76039"
                main_url = "https://api.openweathermap.org/data/2.5/weather?q="
                speak("which city you are living?")
                city = takeCommandMic()
                full_url = main_url + city + api_key
                res = requests.get(full_url)
                data = res.json()

                weather = data['weather'][0]['main']
                temp = data['main']['temp']
                descp = data['weather'][0]['description']

                # temp= round((temp -32) * 5/9)
                print(weather)
                print(temp)
                print(descp)
                speak('Temperature is : {} in farenhite'.format(temp))
                speak('weather is {}'.format(descp))
            elif 'message' in query:
                user_name = {
                    'alex': 'add a phone number'
                }
                try:
                    speak("To whom do you want to send the Whatsapp message?")
                    name = takeCommandMic().lower()
                    phone_no = user_name[name]
                    speak("What is the subject of message")
                    message = takeCommandMic()
                    sendWhatsapp(phone_no, message)
                    speak("message has successfully sent to the receiver ")
                except Exception as e:
                    print(e)
                    speak("message is unable to send")
            elif 'covid' in query:
                covid()
            elif 'news' in query:
                news()
            elif 'email' in query:
                email_list = {'alex': 'add an email'}
                try:
                    speak("To whom do you want to send the email?")
                    name = takeCommandMic().lower()
                    receiver = email_list[name]
                    speak("What is the subject of email?")
                    subject = takeCommandMic()
                    speak("Sir, what should I want to send? ")
                    content = takeCommandMic()
                    sendEmail(receiver, subject, content)
                    speak("Email has successfully sent to the receiver ")
                except Exception as e:
                    print(e)
                    speak("Email is unable to send")
            elif 'offline' in query:
                quit()

    # while True:
    # voice = int(input("Enter 1 to male\nEnter 2 to female"))
    # speak(audio)
    # getvoices(voice)
    # greet()
    # wishme()

load = Image.open('imdg.jpg')
render =ImageTk.PhotoImage(load)
img= Label(root, image=render)
img.place(x=0 , y=0)
b=Button(root,text="Start!", image=p1, command=click)

b.pack(side=LEFT,padx=100,)
root.mainloop()
