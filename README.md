# Address-Extraction








The overall precision of the code was 44%, meaning i could extract data from 1086 urls, the code took aprox  4min to execute with 3 instances of  826 requests at once,
my network got throttled so i probably can get better results on a better internet package. 
![image](https://github.com/PetruMariuta/Address-Extraction/assets/118382269/5e3d4f8e-08cd-4606-9976-aa00ba3f986a)



A part of the data extracted for refference:
![image](https://github.com/PetruMariuta/Address-Extraction/assets/118382269/0433578f-7625-4910-b61e-4ed532f91de7)




This code performs a web scraping task on a set of 2479 websites. It reads data from a Parquet file containing website information, extracts URLs from the data, and then uses asynchronous requests to retrieve web page content from those URLs. It parses the HTML content using BeautifulSoup, searches for specific elements (span, p, a), and extracts information such as addresses and postcodes. The extracted data is stored in a list. Finally, the gathered data is written to a text file, and the execution time and precision of the task are printed.

There are some commented-out sections in the code, such as the use of the Faker library to generate fake IP addresses and the splitting of the dataframe into smaller portions (df_split). Additionally, the code sets a specific User-Agent header (headers) for the HTTP requests to handle sites that dislike aiohttp's user agent.

The code is organized into functions and utilizes asynchronous programming techniques to improve efficiency by making concurrent requests.
