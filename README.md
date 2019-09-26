<h1 align="center">
  <br>
  Whatever the Weather
</h1>

<h4 align="center">
  <a>Sensing & IOT Module, Design Engineering, Imperial College London</a>
  <br><br>
  <a href="https://github.com/leahpattison/Sensing-IOT/blob/master/Leah-Pattison-SIOT.pdf">Read the report</a>
</h4>

<p align="center">
	<sub>A project exploring the effect of weather on music taste utilising the Spotify and DarkSky API's. The video uploaded demonstrates how to open and run the application once setup. </sub>
</p>
<br>
<p align="center">
</h1>
<br>

## 1. Data Collection

The `Data_Collection/` directory contains all scripts and data backups used during part 1 of the coursework. These were loaded onto a Rasberry Pi. 

### File descriptions

> **API.py** 	    Data collection scripts for collecting data from Spotify and Dark Sky
> **Analysis.py**   Utility script for analysing any gaps in the data  
> **Main.py**       Raw data collection script 


## 2. Data Analysis

The `Time_Series/` directory the Python data analytics.

<p align="center">
	<a href="https://github.com/leahpattison/Sensing-IOT/blob/master/Time_Series/Time%20Series%20Analysis.ipynb" target="_blank">View the Jupyter Notebook</a>
</p>

**Note**: API keys and credential files have not been committed.

## 3. Application

The `Application/` directory contains all files related to the web application created to create a playlist based on the weather in the users current location. This application was created using flask. 

## References

* Information for implementing Spotify API

``` bash
https://developer.spotify.com/documentation/web-api/
```

* Information for implementing Dark Sky API

``` bash
https://darksky.net/dev
```

![LICENSE](CC4.0-BY.jpg)
