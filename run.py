import argparse
from app import Scraper

def parse() :
    parser = argparse.ArgumentParser(description = 'Exrtacting product info from amazon')
    parser.add_argument('-p' ,dest = "pageno", type = int, action = "store", default = False)
    parser.add_argument('-f', type=str ,dest = "file_name",  action = "store", default = "Amazon.csv")
    parser.add_argument('-s', dest = "search", type =str, action = "store", default = False)
    return parser

value = parse()
value = value.parse_args()  

laptops = Scraper(value.search  ,value.file_name , value.pageno)

if __name__ == "__main__" :
    print(laptops.run())
