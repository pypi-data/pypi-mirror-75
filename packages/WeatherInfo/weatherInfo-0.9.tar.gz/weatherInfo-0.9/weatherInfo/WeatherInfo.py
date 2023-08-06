import requests,json 
import csv,threading
import sys

class WeatherInfo:   
    def getWeatherInfo(self,counter,api_key,city,file_name):
		threading.Thread.__init__(self)
        self.threadID = counter
        self.counter = counter
        self.api_key = api_key
        self.city = city
        self.file_name =file_name
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
    def thearedfunc():
        threadLock = threading.Lock()
        threads = []
        #apikey = sys.argv[0] 
        #city =  sys.argv[1]
        #filepath = sys.argv[2]
        apikey = input("1")
        city =  input("2")
        filepath = input("3")
        thread1 = threading.Thread(WeatherInfo( 1,apikey,city,filepath).getWeatherInfo())
        #thread1 = threading.Thread(WeatherInfo( 1,"17f5118cc7342b5b6fd0abbfb058c3bd","warangal","D:/Learning/").getWeatherInfo())
        thread1.start() 
        #thread2.start() 
        threads.append(thread1)
        #threads.append(thread2)
        for thread in threads:
            thread.join()
                
#if __name__ == '__main__':
#    WeatherInfo.thearedfunc()

    
    