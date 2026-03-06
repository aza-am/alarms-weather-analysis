**Air Alarms Prediction (Data Collection Pipeline)**

Repository contains data collection module for a university project focused on predicting air raid alarms in Ukraine using historical weather data and ISW reports
<br>
<br>

TEAM №6:

**Team Lead**: Myrhorodska Diana

Markovska Taisiya

Zaiets Anastasiia

<br>
<br>
This repository includes automated data collection scripts:


weather_forecast.py

A script that integrates with the **Visual Crossing API**

  * Fetches the 24-hour hourly weather forecast for a specified city using metric units
  * Extracts the granular hourly data array and saves it locally as a JSON file for time-series alignment


daily_isw.py

A web scraping tool built with "BeautifulSoup"

  * Automatically generates URLs and scrapes daily report titles from the **Institute for the Study of War**
  * Extracts the relevant "<title>" tags and saves the collected intelligence data into a CSV format
