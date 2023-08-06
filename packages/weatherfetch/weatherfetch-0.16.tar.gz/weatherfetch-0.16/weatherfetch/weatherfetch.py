# Python program to find current 
# weather details of any city 
# using openweathermap api 

# import required modules 
import requests,datetime,sys,threading,queue
class weatherfetch:
    def get_api_url(city,out_queue):
        #executed by thread t1
        # api key obtained on registering in website
        api_key = "f19660f12a7cc34d0df3f7540855233a"
        # base_url variable to store url
        base_url = "http://api.openweathermap.org/data/2.5/forecast?"
        # complte_url variable to get get data of any city which is taken as input
        # complete url address
        complete_url =  base_url + "appid=" + api_key + "&q=" + city
        # the result is put on the queue (defined in main thread) for the other thread to use
        out_queue.put(complete_url)


    def get_city_weather_info(complete_url,out_queue):
    #executed by thread t2
    #flag variable to check if an exception occurs or not
        flag = False
        try:
        # get the weather info of the city using complete_url obtained from thread t1
        #timeout argument to indicate time needed to wait for data and download it from website
            data = requests.get(complete_url,timeout=(5, 14))
        #changing boolean of flag if no exception is raised
            flag = True
        # all possible exceptions from requests handled accordingly
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:\n",errc)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else\n",err)
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:\n",errh)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:\n",errt)
        # if exception is raised then exit the program    
        if not flag:
            sys.exit(1)
        # else put the data obtained from website in queue (defined in main thread)
        else:
            out_queue.put(data)


    def get_fifth_day_weather(info):
    # Data in json format
        x = info.json()
        flag = 0
    # time_delta variable to be used to get date after 5 days from today
        time_delta = datetime.timedelta(days=5)
    # check if the city searched for weather info is rigth or wrong
        if x["cod"] != "404":
    #         print(x)
        # get todays date and time. Both stored in today_date variable
            today_date = x['list'][0]['dt_txt']
            #print(today_date)
            # converting todays time in required format. date and formatted time stored in date_today variable
            date_today = datetime.datetime.strptime(today_date, '%Y-%m-%d %H:%M:%S')
            #print(date_today)
            # get date of the day 5 days later from today using time_delta variable
            date_needed = str(date_today + time_delta)
            #print(date_needed)
            # date and time split seperately
            req_date = date_needed.split()
            #print(req_date)
            #print('loop dates')
            # check for only till 5th day's date (from today)
        for day in range(0,len(x['list'])):
            date = x['list'][day]['dt_txt']
            only_date = date.split()
            #print(only_date)
            #check if required date and for which weather info is required is matched with item in list

            flag = 1
            # name of the file with city name and timestamp to be unique at each time
            filename = f"weather_forecast of {city_name} {datetime.datetime.now().strftime('%Y-%m-%d_%I-%M-%S-%p')}.txt"
            # create a file with filename variable in append format
            #print('filename given')
            with open(filename,'a') as f:
                y = x['list'][day]['main']
                z = x['list'][day]['weather']
                # store the temperature value corresponding to value of y
                current_temperature = y["temp"]
                # store the pressure value corresponding to value of y
                current_pressure = y["pressure"]
                # store the humidity value corresponding to value of y
                current_humidity = y["humidity"]
                # store the weather description value corresponding to value of z
                weather_description = z[0]["description"]
                # write necessary info in file
                f.write(f'The forecasted weather of {city_name} on {date}')
                f.write("\n")
                f.write(f'Temperature (in kelvin unit) = {current_temperature}' )
                f.write("\n")
                f.write(f'Atmospheric pressure (in hPa unit) = {current_pressure}' )
                f.write("\n")
                f.write(f'Humidity (in percentage) = {current_humidity}' )
                f.write("\n")
                f.write(f'Description = {weather_description}' )
                f.write("\n")
                f.write("\n")
                # closing the file
                f.close()

        else:
            # delclaring the non existence of city(user input)
            # to print city not found if x["cod"] is 404
            print(" City Not Found ")


    def main(): 
        # get name of the city from user
        city_name = 'Kakinada'
        # declaring queue to get return values from user defined functions
        my_queue = queue.Queue()
        #Thread t1 executing the get_api_url() function
        t1 = threading.Thread(target=get_api_url(city_name,my_queue))
        #start thread t1
        t1.start()
        # main program to wait till Thread t1 is completed
        t1.join()
        # get the return value from the get_api_url function
        func_value = my_queue.get()
        # Thread t2 executing get_city_weather_info() function
        t2 = threading.Thread(target=get_city_weather_info(func_value,my_queue))
        #start thread t2
        t2.start()
        # main program to wait till Thread t2 is completed
        t2.join()
        # get the return value from the get_city_weather_info function
        func_value = my_queue.get()
        # executing the get_fifth_day_weather function that write data to file
        get_fifth_day_weather(func_value)

