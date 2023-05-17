from pyarrow import parquet
import pandas as pd
import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup as BS 
import re
from faker import Faker
import json

#micunealta in caz de ip restrictionat de la nr. de request-uri
#faker = Faker()  
#ip_addr = faker.ipv4() 



data = parquet.read_table(r'C:\path to\.parquet')
df = data.to_pandas()
#print(df)
#2479  websites?!?! 



#code was ran in 3 different instaces due to my network crashing/throttling
#df_split = df.head(826)
# df_split = df.iloc[827:1653]  
df_split = df.iloc[1653:2480]



#some sites dislike aiohttps user agent
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}

urls = []
def get_urls():
    for index, row in df_split.iterrows():
        domain = row['domain']
        #print(domain)
        urls.append("http://" +  domain) #https:// nu merge pentru fiecare site
        
    


start_time = time.time()



async def get_data(session, url):

    global precision
    precision = 0

    try:
        async with session.get(url, headers=headers) as resp:
            
            
            if 300 > resp.status >= 200 :

                response_text = await resp.text()
                soup = BS(response_text, 'html.parser')                                
                #if url.endswith(".com") == False: ar merge si cu endswith("de" sau "uk") si un re pentru zonele lor
                
                address_elements =  soup.find_all(['span', 'p', 'a'])  #html2text si scrapy ar merge chiar mai bn
                

                for url_data in address_elements:
                        
                        address_text = url_data.text
                        postcode = re.search(r'\b\d{5}\b', address_text)
                        pattern = r'\b(?:address|contact|other)\b'
                        #matches = re.findall(pattern, address_text)
                        
                        if postcode:

                            element_text = " ".join(url_data.stripped_strings)                            
                            #print(url, element_text)
                            precision += 1
                            return f"{url}:  {element_text}"
                        
    
            else:
             
                precision += 1
                return f"{url} encountered an HTTP response status code: {resp.status}" 
                #print("failed url",url )
                pass


    except (BaseException) as e:

        precision += 1
        print(f" {url} had a BaseException as {e}")
        pass




async def make_requests():

    total_timeout  =  aiohttp.ClientTimeout(total=None)
    limits = aiohttp.TCPConnector(limit=None)

    async with aiohttp.ClientSession(connector=limits, timeout = total_timeout) as session:
        global gathered_data
        gathered_data = []
        
        for url in urls: 
              #try: 
               gathered_data.append(asyncio.ensure_future(get_data(session, url)))
              #except(BaseException):
               pass
          
        url_output = await asyncio.gather(*gathered_data)

        with open(r'C:\path to\\answer.txt', "w") as file:
            
            for output in url_output:
                
                if output is not None:
                    #print(output)
                    file.write(str(output) + '\n', encoding='utf-8')
               
                      
                    

#this won't work in python 3.11
def main():

  get_urls()
  loop = asyncio.get_event_loop()
  loop.run_until_complete(make_requests())
  print("--- %s seconds ---" % round(time.time() - start_time))
  print(f"Precision = {round((precision/826)*100)}%")
  


if __name__ == "__main__":

    main()

    #monkey patching
    #loop = asyncio.new_event_loop()
    #loop.run_until_complete(make_requests())
  

#country, region, city, postcode, road, and road number 

# poate merg aflate si dupa ip adress, posibil si road number -- merge dar contra-cost

# fac regex dupa postcode i guess

#incerc sa obtin doar datele din html, si dupa fac regex
