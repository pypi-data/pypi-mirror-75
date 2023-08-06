from .config import weather_url_start,api_key,weather_url_end
from .transformer import OutputTransformer
import requests
import json
import concurrent.futures
import logging
from colorama import Fore, Back, Style
import datetime
class Weather:
    @staticmethod
    def hitEndpoint(city_name):
        final_url=weather_url_start+str(city_name)+weather_url_end+str(api_key)
        try:
            response=requests.post(final_url,data=city_name,headers={"Content-Type":"application/json"})
            #changing boolean of flag if no exception is raised
        # all possible exceptions from requests handled accordingly
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:\n",errc)
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:\n",errh)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:\n",errt)

        return response
    @staticmethod
    def getWeather(city_name):
        obj=Weather()
        #Hitting open weather map endpoint in seperate thread to achieve MultiTasking
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(obj.hitEndpoint,city_name)
            response= future.result()
        data=response.json()
        #Error Handling if open weather api is not success
        if response.status_code!=200:
            res_json=OutputTransformer().error_handling_transformer()
            print(res_json)
        #If success, writing output to a file
        else:
            for day in range(0,len(data['list'])):
                date = data['list'][day]['dt_txt']
                filename = f"weather_forecast of {city_name} {datetime.datetime.now().strftime('%Y-%m-%d_%I-%M-%S-%p')}.txt"
                # create a file with filename variable in append format
                #print('filename given')
                with open(filename,'a') as f:
                    y = data['list'][day]['main']
                    z = data['list'][day]['weather']
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
            '''
            with open('result.json', 'w') as f:
                json.dump(data, f)
            print(Back.GREEN+"Check result.json file in output folder to view result")
            '''
            print(data)