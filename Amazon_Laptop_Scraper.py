import pandas as pd
import matplotlib.pyplot as mp
import seaborn as sns
from bs4 import BeautifulSoup
import requests,csv
from selenium import webdriver
import re


class Scraper :
    all_items = []
    #row1 and row2 for comparision in visual mode

    def __init__(self , product_search : str ,FileName : str , row1 = None , row2 = None , page_no = 1) :
        #checking for negative numbers in page argument from the users
        assert page_no < 0 , f' { page_no } is in negative . Please provide a positive pageno'
        self.product_search = product_search
        self.page_no = page_no
        self.FileName = FileName
        self.row1 = row1
        self.row2 = row2
    
    def finding(self , value , items):
        if value != None:
            items.append(value.text.replace(',',''))
        else:
            items.append("")
             
    def run(self) :
        items = []
        #Creating the Request Headers for HTTP
        self.product_search=self.product_search.replace(' ','+')
        url=f'https://www.amazon.in/s?k={self.product_search}&ref=nb_sb_noss_2'+str(self.page_no)+'?ie=UTF8&pg='+str(self.page_no)
        HEADERS = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept-Encoding":"gzip, deflate, br", "Accept":	"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

        #HTTP Response 
        page = requests.get(url,headers=HEADERS)

        #creating soup and getting the html content
        soup = BeautifulSoup(page.content,'html.parser')

        #Starting the search for our Content
        tag1 = soup.findAll('div',attrs={'data-component-type':'s-search-result'})

        for t1 in tag1 : 
            #Title of the product
            Product_Name=t1.find('span',attrs={'class':"a-size-medium a-color-base a-text-normal"})
            self.finding(Product_Name,items)

            #Price of the Product
            Price = t1.find('span',attrs={'class':"a-price-whole"})
            self.finding(Price,items)
            
            #Ratings of the Product
            ratings = t1.find('span',attrs={'class':"a-size-base"})
            self.finding(ratings,items)

            #How many stars that customer given
            stars = t1.find('span',attrs={'class':'a-icon-alt'})
            self.finding(stars,items)

            # for finding original price 
            original=t1.find('span',attrs={'class':"a-price a-text-price"})
            if original !=None:
                Original_Price=original.find('span',attrs={'aria-hidden':"true"})

            if Original_Price != None :
                items.append(Original_Price.get_text()[1:].replace(',',''))
            else:
                items.append('')

            #appending the final result
            self.all_items.append(items)
            items = []

        #Writing it to the csv file (Comma Seperated File)
        #for writing the column name
        if self.page_no == 1 :
            with open(self.FileName,'w') as file :
                writer = csv.writer(file)
                writer.writerow(['Product_Title','Price','No_of_ratings','Stars','Original_Price'])
                
        #appending the rows 
        with open(self.FileName,'a') as file :
            writer = csv.writer(file)
            writer.writerows(self.all_items)
        return "[+] Details collected Successfully....."  
    
    
    def visualization(self) :       
        df = pd.read_csv(self.FileName)
        df = df.drop_duplicates()
        df['Price'] = pd.to_numeric(df['Price'])
        df['Original_Price'] = pd.to_numeric(df['Original_Price'])
        df = df.dropna()
        df['Offer_Price'] = df['Original_Price']-df['Price']
        df['Stars'] = df['Stars'].astype(str)
        df['Stars'] = df['Stars'].apply(lambda col:col.split()[0])
        df['Stars'] = pd.to_numeric(df['Stars'])
        df['Company'] = df['Product_Title'].apply(lambda col:col.split()[0])
        return df


    def seaborn_visual(self , row1 , row2 ) :       
        fig = mp.figure(dpi=100,figsize=(6,6))
        sns.scatterplot(data = self.visualization() , x = row1 , y = row2 ,hue = 'Company')


if __name__ == '__main__' : 
    pass

    #laptops = Scraper('laptops'  ,'LaptopAmazon.csv' , page_no=2)
    #laptops.page_no
    #laptops.run()

    #for visualization in table
    #print(laptops.visualization())

    #visualizating in Graph
    #laptops.seaborn_visual('Price','Stars')
