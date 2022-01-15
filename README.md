# Amazon Electronic's Product Scraper

## Table of contents

* [General info](#general-info)
* [Project_Description](#Project_Description)
* [Technologies](#technologies)
* [Installation](#Installation)
* [Setup](#setup)


## General info
This project is simple a Amazon prodcut scraper.Web scraping, web harvesting, or web data extraction is data scraping used for extracting data from websites.



## Project Description
This project will be usefult for extracting the data from the amazon website.With that you can able to do lots of thing .For example you cn create a model which will predict whether the price of the product will decrease or not by extracting the data in various times and use a ML Model to bulid it.But you only can able to extract the electronic products details using this code.You can also run this program from your terminal using the arguments which is specified in Setup.

## Technologies
Project is created with:
* Python 3.9.2
* beautifulsoup4
* requests
* csv
* re
* argparse

## Installation

```bash
pip install beautifulsoup4
```

```bash
pip install argparse
```
```bash
pip install requests
```

## Setup
To run this project,clone this repository in your machine:

* Make sure to have a Python installed 

```
$ cd ../AmazonElectronicScraper
$ python3 run.py -p 1 -f "amazon.csv" -s "laptop"
$ python3 run.py -h 
```
* python3 run.py -h - To see the description and to get the help
* -f argument - It is used to specify the filename .Where you like to save the result.Please make sure to use the csv extension.
* -s argument - It is used to specify a search keyword .Like mobile phones, Latpops
* -p argument -It is used to speicfy , how many page you need to extract.
