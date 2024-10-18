#importing all the libraries.
import requests
import tkinter as tk
from PIL import ImageTk,Image


#get the weather data.
def get_weather(api_key,city):
    url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response=requests.get(url)
    data=response.json()
    if response.status_code==200:
        weather_description=data['weather'][0]['description']
        temperature=data['main']['temp']
        humidity=data['main']['humidity']
        wind_speed=data['wind']['speed']
        return [weather_description,temperature,humidity,wind_speed]
    else:
        print("Error:",data['message'])

#get the forecast data.
def get_forecast(api_key,city):
    url=f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response=requests.get(url)
    if response.status_code==200:
        data=response.json()
        forecasts=data['list']
        d=[]
        for forecast in forecasts:
            l=[]
            date_time=forecast['dt_txt']
            temperature=forecast['main']['temp']
            weather_description=forecast['weather'][0]['description']
            l.append(date_time)
            l.append(temperature)
            l.append(weather_description)
            d.append(l)
        return d
    else:
        print("Error:",data['message'])

#main

#get all the data
api_key="71a90f8d7ba0203ac50aca99360b5af6"
city='Mumbai'
wdata=get_weather(api_key,city)
w0=wdata[0]
w1=wdata[1]
w=round(w1)
w2=wdata[2]
w3=wdata[3]
fdata=get_forecast(api_key,city)

#graph it
D=[]
T=[]
a=0
for i in fdata:
    D.append(i[0])
    T.append(i[1])
    a=a+1
    if(a==5):
        break
time=None
d=[]
for item in D:
    if '2024' in item:
        time=item.split()[1].strip()
        d.append(time)
root=tk.Tk()
root.title('PreWeather')
root.minsize(width=600,height=1250)
root.configure(bg='#2596be')






#create labels.
label1=tk.Label(root,text="PreWeather",font=('Arial',40),fg='lightblue',bg='#145369')
label1.place(x=5,y=0,height=50)
label2=tk.Label(root,text=city,font=('Arial',30),fg='lightblue',bg='#2596be')
label2.place(x=5,y=50,height=50)
label3=tk.Label(root,text=w,font=('Arial',80),fg='lightblue',bg='#2596be')
label3.place(x=5,y=100,width=120,height=80)
label5=tk.Label(root,text="c",font=('Arial',40),fg='lightblue',bg='#2596be')
label5.place(x=125,y=140,height=40)
label4=tk.Label(root,text=w0,font=('Arial',15),fg='lightblue',bg='#2596be')
label4.place(x=5,y=200,height=30)

#creating the canvas.
canvas1=tk.Canvas(root,width=200,height=100,bg='lightblue')
text_id1=canvas1.create_text(130,20,text="Humidity",font=('Arial',20),fill='#2587be')
text_id2=canvas1.create_text(140,70,text=w2,font=('Arial',30),fill='#2596be')
text_id5=canvas1.create_text(170,70,text="%",font=('Arial',20),fill='#2596be')
canvas1.place(x=5,y=300)

canvas2=tk.Canvas(root,width=200,height=100,bg='lightblue')
text_id3=canvas2.create_text(100,20,text="Wind Speed",font=('Arial',20),fill='#2587be')
text_id4=canvas2.create_text(90,70,text=w3,font=('Arial',30),fill='#2596be')
text_id6=canvas2.create_text(150,70,text="m/s",font=('Arial',20),fill='#2596be')
canvas2.place(x=215,y=300)
root.mainloop()
