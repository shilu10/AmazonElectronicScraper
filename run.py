import argparse
from scraper import Scraper

def parse() :
    parser = argparse.ArgumentParser(description = 'Exrtacting product info from amazon')
    parser.add_argument('-p' ,dest = "pageno", type = int, action = "store", default = False)
    parser.add_argument('-f', type=str ,dest = "file_name",  action = "store", default = "Amazon.csv")
    parser.add_argument('-s', dest = "search", type =str, action = "store", default = False)
    return parser

#parsing the value from the terminal input
value = parse()
value = value.parse_args()  

#creating a Scraper instance
laptops = Scraper(value.search  ,value.file_name , value.pageno)

if __name__ == "__main__" :
    print(laptops.run())
