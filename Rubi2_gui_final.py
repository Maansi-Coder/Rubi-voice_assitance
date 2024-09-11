######################### All imported Libraries ########3
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import pickle 
import pywhatkit
import random
import PyPDF2
import keyboard
from keyboard import press_and_release
import time
import pyautogui
from pywikihow import search_wikihow
import Alarm
import Birth
import mysql.connector as sqltor
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from Rubi2_gui import Ui_Form
import sys
from sys import exit
################# Other functions ########################
mycon=sqltor.connect(host="localhost",user="root",passwd="maansi",database="rubi")
cursor=mycon.cursor()

engine= pyttsx3.init('sapi5')
voices= engine.getProperty('voices')
#print(voices[0].id)

engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    print("Rubi: ",audio)
    
 
def wishme():
    hour= int(datetime.datetime.now().hour)
 
    if hour >=3 and hour <12:
        speak("Good Morning")
    elif hour>=12 and hour <18:
        speak("Good Afternoon")
    elif hour>=18 and hour<20:
        speak("Good Evening")
    else:
        speak("Good night")
        
    strtime= datetime.datetime.now().strftime("%H:%M:%S")
    print("Its ", strtime)  
    


def Search_binary(to):
    
    cursor.execute("select * from contact")
    data= cursor.fetchall()
    for row in data:
        if row[0]== to:
            return row[1]
        
def Send_time():
    global hour
    hour= str(datetime.datetime.now())
                
    h=int(hour[11:13])
                
    m =int(hour[14:16])+1
    
    if m>59:
        h= h+1
        
    return h, m 
    

def birth_wish():
    cursor.execute("select * from birth_day")
    data= cursor.fetchall()
   
    for i in data:
         c= str(i[0])
         x= str(datetime.datetime.now().date())
         if c[5:7] == x[5:7]:
             if c[-2:] == x[-2:]:
                 try:
                    if i[1] == "Ruby":
                        speak("Did you remember Today's day")
                        print("\U0001F60E")
                        speak("Today is something special Did you remeber")
                        w= take_command().lower()
                        if "sorry" in w or "don't know" in w:
                            speak("Ooohhh ")
                            print("\U0001F61E","\U0001F624","\U0001F621")
                            
                            speak("You Forgot My Birthday")
                        elif "your birthday" in w:
                            speak("You Remember my birthday")
                            print("\U0001F604","\U0001F97A")
                            speak("Thankyou Very much")
                        
                    elif i[1] =="Maansi":
                        speak("Its Your Birthday")
                        speak("I wish You you Happiest Birthday")
                        print("\U0001F929", "\U0001F973","\U0001F973","\U0001F929",)
                        reply= take_command().lower()
                        if "thank you" in reply:
                            speak("Then Will You Invite me in your Birthday Party")
                            c= take_command()
                            speak("Thank you")
                
                    else:
                        speak("Today is "+ i[1]+"'s" + " Birthday")
                        speak("Did you wish them")
                        print("\U0001F9D0")
                        ans= take_command().lower()
                        if "no" in ans:
                            speak("Then wish them now")
                        elif "yes" in ans:
                            speak("Ok, You can continue your work")
                        else:
                            speak("First answer My question")
                            birth_wish()
                        
                 except Exception as e:
                    return None
                
        
class MainThread(QThread): 
    def __init__(self):
        super(MainThread,self).__init__()
    
    def run(self): 
        self.command()

    def take_command(self):
        r= sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening......")
            r.pause_threshold = 1
            audio= r.listen(source)
            
        try:
            print("Recognising.......")
            query= r.recognize_google(audio, language= "en-in")
            print("User said: ",query)
            
        except Exception as e:
            print(e)
            
            print("Say that again please ..........")
            return "None"
        
        return query
    
    def command(self):
    
        wishme()        
        speak("My name is Rubi")
        print("\U0001F603")
        speak(" I wish you all are with good health")
        birth_wish()
        speak("How can I help you")
        
        while True:
            try:
                self.query= self.take_command().lower()
                # Logic queries
                if 'wikipedia' in self.query:
                    speak("Serching wikipedia...")
                    query= self.query.replace("wikipedia", "")
                    result= wikipedia.summary(query, sentences=2)
                    speak("Wikipedia says")
                    print(result)
                    speak(result)
                    
                elif "happy birthday" in self.query:
                    
                    speak("Thankyou So much") 
                    print("\U0001F60A")
                    speak("We will have a great Party Tonight")
                    print("\U0001F942")
                    
                elif "shutdown" in self.query or "shut down" in self.query:
                    pywhatkit.shutdown(time=100) 
                    
                elif "cancle shutdown" in self.query:
                    pywhatkit.cancelShutdown()
                
                elif "open youtube" in self.query:
                    speak("What should I search on youtube")
                    sea= self.take_command()
                    a= 'https://www.youtube.com/results?search_query='+sea
                    webbrowser.open(a)
                    speak("I found this on your search")
                    
                elif "open html" in self.query:
                    webbrowser('https://youtube.com/playlist?list=PLfqMhTWNBTe3H6c9OGXb5_6wcc1Mca52n')
                    
                    
                elif "play song" in self.query:
                    speak("which song you want to hear")
                    song= self.take_command()
                    speak("playing"+song)
                    pywhatkit.playonyt(song)
                
                elif "open google" in self.query:
                    speak("What should I search on Google")
                    search= self.take_command()
                    search=search.replace("search","")
                    pywhatkit.search(search)
                
                elif "open new tab" in self.query:
                    keyboard.press_and_release('ctrl+n')
                
                elif "open whatsapp" in self.query:
                    webbrowser.open('https://web.whatsapp.com/')     
                    
                elif "open email" in self.query:
                    speak("Which Email ID should I open")
                    email= self.take_command().lower()
                    if "my own" in email:
                        webbrowser.open('https://mail.google.com/mail/u/0/?tab=wm&ogbl#inbox')
                    elif "college id" in email:
                        webbrowser.open('https://mail.google.com/mail/u/1/#inbox')
                    else:
                        speak("this email is not available in pc")
                
                elif "open classroom" in self.query:
                    webbrowser.open('https://classroom.google.com/u/1/c/MTI3ODE0ODYxOTIz')
                
                elif "how are you" in self.query:
                    speak("I am Fine, What about you")
                    
                elif "fine" in self.query:
                    speak("I am glad to hear that")
                
                elif "about yourself" in self.query:
                    speak("I am Ruby, An AI Assistant")
                    speak("I am programmed throgh Python")
                    speak("I am developed by Maansi")
                    speak("If you want to know more about me ")
                    speak("Then talk to her")
                    #speak("she knows about me more then me")
            
                elif "your birthday" in self.query:
                    speak("My Birthday is on 18 April 2021")
                      
                elif "change your" in self.query:
                    speak("Take permission from my developer")
                
                elif "thank you" in self.query:
                    speak("I am glad to help you")
                    
                elif "read pdf" in self.query:
                    speak("Enter Pdf Book that should I read")
                    book=input("Enter PDF name: ")
                    path= "C:\\Users\\maans\\OneDrive\\Documents\\Novels\\"+book+".pdf"
                    f= open(path,"rb")
                    reader= PyPDF2.PdfFileReader(f)
                    pages= reader.numPages
                    speak("Total number of pages are"+str(pages))
                    speak("which pages should I read")
                    pg= int(input("Enter Page number: "))
                    pag= reader.getPage(pg)
                    text= pag.extractText()
                    speak(text)
                    
                elif "open notepad" in self.query:
                    way= "C:\\WINDOWS\\system32\\notepad.exe"
                    os.startfile(way)
                    
                    
                    speak("What would you write in notepad")
                    com= take_command()
                    if "I will" in com:
                        speak("Ok")
                        
                    if "type" in com:
                        s= com.replace("write", "")
                        time.sleep(3)
                        pyautogui.write(s)  
                    
                elif "close" in self.query:
                    keyboard.press_and_release('alt+f4')
        
                elif "open sublime text" in self.query:
                    way= "C:\\Program Files\\Sublime Text 3\\sublime_text.exe"
                    os.startfile(way) 
                    
                elif "tell me about" in self.query:
                    query= self.query.replace("tell me about", "")
                    speak(pywhatkit.info(query,3))
                
                    
                elif "play music" in self.query:
                    music_dr= "C:\\Users\\maans\\Music"
                    songs= os.listdir(music_dr)
                    y= random.randint(0,len(songs))
                    os.startfile(os.path.join(music_dr, songs[y]))
                
                elif "current time" in self.query:
                    strtime= datetime.datetime.now().strftime("%H:%M:%S")
                    speak("The Time is ")
                    speak(strtime)
                    
                elif "current date" in self.query:
                    strdate= datetime.datetime.now().date()
                    speak("The Date is ")
                    speak(strdate)    
                    
                elif "add birthday" in self.query:
                
                    speak("Enter Name ")
                    name= input("Enter name:")
                    speak("Enter Birth date to person")
                    dat= input("Enter Date of Birth: ")
                    st="Insert into contact(b_date,name) values('{}','{}')".format(dat,name)
                    cursor.execute(st)
                    mycon.commit()
            
                elif "new contact" in self.query:
                    speak("Enter Name of Contact")
                    speak("Please enter name in lower case")
                    name= input("Enter name: ")
                    speak("Enter Contact Number")
                    nu= input("Enter Number: ")
                    contact_no= "+91"+nu
                    st="Insert into contact(name,number) values('{}','{}')".format(name,contact_no)
                    cursor.execute(st)
                    mycon.commit()
                    speak("Successfully added") 
                
                elif "send a message" in self.query:
                    speak("To whom you want to send message")
                    to = self.take_command().lower()
                    to= ((to.split())[0])
                    nu= Search_binary(to)
                    if nu== None:
                        speak("Contact not found")
                        speak("Please first add that contact")
                
                    else:
                        speak("What message should I give ")
                        st= self.take_command()
                        ho, mi = Send_time()
                        pywhatkit.sendwhatmsg(nu, st,ho,mi)
               
                elif "show contact" in self.query:
                    cursor.execute("select * from contact")
                    data= cursor.fetchall()
                    for row in data:
                        print(row)
                        
                elif "how to " in self.query:
                    query= self.query.replace("how to","")
                    max_results= 1
                    how_to= search_wikihow(query, max_results)
                    assert len(how_to)==1
                    how_to[0].print()
                    speak(how_to[0].summary)
                    
                elif "alarm" in self.query:
                   speak("Please tell me time to set alarm, for example 5:30 am")
                   ti= self.take_command()
                   t= ti.replace("set ","")
                   t= ti.replace("alarm","")
                   t= ti.replace("to","")
                   t= t.replace(".","")
                   t= t.upper()
                   
                   Alarm.alarm(t)
                   
                elif "timer" in self.query:
                    speak("How many Minutes to wait") 
                    mi = int(input("How many minutes you want to wait"))
                    speak("Timer Started")
                    seconds= 60* mi
                    for i in range(seconds,0,-1):
                        time.sleep(1)
                    print("Time IS Up")    
                    speak("Time up")
           
                elif "sleep" in self.query:
                    speak("You can call me any time")
                    mycon.close()
                    break;
            except Exception as e1:  
                speak("Command cannot be perfomed because of following error")
                print(e1)
                continue;
                
startExe= MainThread()                
        
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui= Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        
    def startTask(self):
        self.ui.movie= QtGui.QMovie("equiler.gif")
        self.ui.speaker.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer= QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExe.start()
        
      
    def showTime(self):
        cur_time=QTime.currentTime()
        cur_date=QDate.currentDate()
        label_time= cur_time.toString('hh:mm:ss')
        label_date= cur_date.toString(Qt.ISODate)
        self.ui.date_text.setText(label_date)
        self.ui.time_taxt.setText(label_time)
        
app= QApplication(sys.argv)
rubi= Main()
rubi.show()
exit(app.exec_())          
                    
######################### Queries ##############################



