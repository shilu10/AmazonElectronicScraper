from bs4 import BeautifulSoup
import requests,csv
import re


class Scraper :    
    AL_ITEMS = [ ]
    #row1 and row2 for comparision in visual mode
    def __init__(self , product_search : str ,file_name : str , page_no = 1) :
        #checking for negative numbers in page argument from the users
        assert page_no > 0 , f' { page_no } is in negative . Please provide a positive pageno'
        
        self.__product_search = product_search
        self.__page_no = page_no
        self.__file_name = file_name
        
    
    # encapsulation 
    
    @property 
    def page_no(self) :
        return self.__page_no
      
    @property
    def product_search(self) :
        return self.__product_search
      
    @property
    def file_name(self) :
        return self.__file_name
    
    #@page_no.setter
    #def page_no(self, value) :
     #   self.__page_no = value
    
    @product_search.setter
    def product_search(self, value) :
        self.__product_search = value
        
   # @file_name.setter
    #def file_name(self, value) :
     #   self.__file_name = value
        
    
    def __finding(self , value , items) :
        if value != None :
            items.append(value.text.replace(',' , ''))
        else:
            items.append("")
             
    def run(self) :
        
        items = [ ]
        #Creating the Request Headers for HTTP
        self.product_search=self.product_search.replace(' ','+')
        url=f'https://www.amazon.in/s?k={self.product_search}&ref=nb_sb_noss_2'+str(self.page_no)+'?ie=UTF8&pg='+str(self.page_no)
        HEADERS = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept-Encoding":"gzip, deflate, br", "Accept":	"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
        #HEADERS = use ypur headers here
        
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

            # for finding original price 43
            original=t1.find('span',attrs={'class':"a-price a-text-price"})
            if original !=None:
                Original_Price=original.find('span',attrs={'aria-hidden':"true"})

            if Original_Price != None :
                items.append(Original_Price.get_text()[1:].replace(',',''))
            else:
                items.append('')
                
            #appending the final result
            self.AL_ITEMS.append(items)
            items = [ ]

        #Writing it to the csv file (Comma Seperated File)
        #for writing the column name
        if self.page_no == 1 :
            with open(self.file_name,'w') as file :
                writer = csv.writer(file)
                writer.writerow(['Product_Title','Price','No_of_ratings','Stars','Original_Price'])
                
        #appending the rows 
        with open(self.file_name,'a') as file :
            writer = csv.writer(file)
            writer.writerows(self.AL_ITEMS)
        return "[+] Details collected Successfully....."  
        
   

        
laptops = Scraper('laptops'  ,'LaptopAmazon.csv' , 15)
#if __name__ == '__main__' : 
laptops.run()
