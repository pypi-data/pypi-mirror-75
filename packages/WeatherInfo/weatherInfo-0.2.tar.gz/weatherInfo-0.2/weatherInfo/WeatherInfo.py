import requests,json 
import csv,threading
import sys

class WeatherInfo(threading.Thread):
    def __init__(self,counter,api_key,city,file_name):
        threading.Thread.__init__(self)
        self.threadID = counter
        self.counter = counter
        self.api_key = api_key
        self.city = city
        self.file_name =file_name
    def getWeatherInfo(self):
        url =  "http://api.openweathermap.org/data/2.5/forecast?" + "q=" + self.city + "&appid=" + self.api_key
        threadLock.acquire()
        #print(url)
        file_name =self.file_name+self.city+'.txt'
        response = requests.get(url)
        #print(response)
        if response.status_code == 200:
            json_response = response.json()
            list1 = json_response['list']
            with open(file_name, 'w') as weathercsvfile:
                fieldnames = ['temperature', 'temp_min','temp_max','humidity','date','cityname']
                writer_weather = csv.DictWriter(weathercsvfile, fieldnames=fieldnames)
                writer_weather.writeheader()
                for i in range(0,len(list1)):
                    temperature= list1[i]['main']['temp']
                    temp_min= list1[i]['main']['temp_min']
                    temp_max= list1[i]['main']['temp_max']
                    humidity = list1[i]['main']['humidity']
                    date= list1[i]['dt_txt']
                    writer_weather.writerow({'temperature': temperature, 'temp_min': temp_min,'temp_max':temp_max,'humidity':humidity,'date':date,'cityname':self.city})
        else:
            print('error in http request',response.status_code)
        threadLock.release()
                
    
    
    