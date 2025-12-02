import pandas as pd
import csv
import matplotlib as mp
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime
import requests
import json

class meteo :
    def __init__(self) : 
        self.loaded_csv = []
        self.stats = {}
        
    def load_file(self) : 
        df = pd.read_csv('meteo.csv', sep=",", parse_dates=['date'])
        df = df.astype('int64') #date as timestamp (integer)
        self.loaded_csv = df.to_dict(orient='records')
        
    def statistics(self) : 
        temperatures_values = [self.loaded_csv[i].get('temperature') for i in range(len(self.loaded_csv))]
        self.stats['mean_temp'] = sum(temperatures_values) / len(temperatures_values)
        self.stats['min_temp'] = min(temperatures_values)
        self.stats['max_temp'] = max(temperatures_values)

        humidity_values = [self.loaded_csv[i].get('humidite') for i in range(len(self.loaded_csv))]
        self.stats['mean_humidity'] = sum(humidity_values) / len(humidity_values)

        rain_values = [self.loaded_csv[i].get('pluie') for i in range(len(self.loaded_csv))]
        self.stats['rain_days'] = sum(rain_values)
        
    
    def display_rapport(self) : 
        print(f"----- RAPPORT MÉTÉO -----\n"
              f"Température moyenne: {self.stats['mean_temp']} °C\n"
              f"Température minimale: {self.stats['min_temp']} °C\n"
              f"Température maximale: {self.stats['max_temp']} °C\n"
              f"Humidité moyenne: {self.stats['mean_humidity']} %\n"  
              f"Jours de pluie: {self.stats['rain_days']} jours\n"
              f"-------------------------")
    
    
    def display_graphic1(self) : 
        dates = [self.loaded_csv[i]['date'] for i in range(len(self.loaded_csv))]
        dates = pd.to_datetime(dates) 
        temperatures_values = [self.loaded_csv[i].get('temperature') for i in range(len(self.loaded_csv))]
        plt.ion()
        plt.plot(dates, temperatures_values)
        plt.grid()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gcf().autofmt_xdate()
        plt.title("Temperatures sur le debut d'année")
        plt.xlabel("date")
        plt.ylabel("température (°C)")
        plt.show()
        plt.waitforbuttonpress(0)
        plt.close('all')


    def display_hot_cold_days(self) : 
        max_index = []
        for i,v in enumerate(self.loaded_csv) : 
            if self.loaded_csv[i]["temperature"] == self.stats['max_temp'] :
                max_index.append(i)
        min_index = []
        for i,v in enumerate(self.loaded_csv) : 
            if self.loaded_csv[i]["temperature"] == self.stats['min_temp'] :
                min_index.append(i)
        
        cold_days = []
        for i in min_index : 
            d = datetime.fromtimestamp(self.loaded_csv[i]["date"] * 1e-9).date()
            cold_days.append(d.strftime("%Y-%m-%d")) # to string 
        print(cold_days)

        hot_days = []
        for i in max_index : 
            d = datetime.fromtimestamp(self.loaded_csv[i]["date"] * 1e-9).date()
            hot_days.append(d.strftime("%Y-%m-%d")) # to string 
        print(hot_days)

        
    def display_graphic2(self) : 
        dates = [self.loaded_csv[i]['date'] for i in range(len(self.loaded_csv))]
        dates = pd.to_datetime(dates) 
        humidity_values = [self.loaded_csv[i].get('humidite') for i in range(len(self.loaded_csv))]
        plt.ion()
        plt.plot(dates, humidity_values)
        plt.grid()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gcf().autofmt_xdate()
        plt.title("Humidité sur le debut d'année")
        plt.xlabel("date")
        plt.ylabel("taux humidité (%)")
        plt.show()
        plt.waitforbuttonpress(0)
        plt.close('all')
    

    def API_meteo(self, city) : 
        geo = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_data = requests.get(geo).json()
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        meteo = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true"
        )
        self.infos_meteo = requests.get(meteo).json()
        
    def export_API_meteo_report(self) : 
        with open('rapport.txt', 'w') as file:
            file.write(json.dumps(self.infos_meteo))

       

    
if __name__ == "__main__" : 
    meteo_analysis = meteo()
    meteo_analysis.load_file()
    meteo_analysis.statistics()
    meteo_analysis.display_rapport()
    meteo_analysis.display_graphic1()
    meteo_analysis.display_hot_cold_days()
    meteo_analysis.display_graphic2()
    meteo_analysis.API_meteo("Montpellier")
    meteo_analysis.export_API_meteo_report()







    