if __name__ == "__main__":
	threadLock = threading.Lock()
    threads = []
    apikey = sys.argv[0] 
    city =  sys.argv[1]
    filepath = sys.argv[2]
    thread1 = threading.Thread(WeatherInfo( 1,apikey,city,filepath).getWeatherInfo())
    #thread1 = threading.Thread(WeatherInfo( 1,"17f5118cc7342b5b6fd0abbfb058c3bd","warangal","D:/Learning/").getWeatherInfo())
    thread1.start() 
    #thread2.start() 
    threads.append(thread1)
    #threads.append(thread2)
    for thread in threads:
        thread.join()