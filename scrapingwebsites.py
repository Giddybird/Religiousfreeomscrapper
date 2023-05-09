import scrapy
import pandas as pan
import requests
from bs4 import BeautifulSoup
import numpy as np
from math import nan, isnan
from requests.exceptions import Timeout
from urllib.error import HTTPError
import pathlib
from PyPDF2 import PdfFileReader
import PyPDF2
from pathlib import Path
import os
import pdfkit
from pyhtml2pdf import converter
converter.convert
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import progressbar
from playsound import playsound
 
widgets = [' [',
         progressbar.Timer(format= 'elapsed time: %(elapsed)s'),
         '] ',
           progressbar.Bar('█'),' (',
           progressbar.ETA(), ') ',
          ]
 

#Importing The List of URLS into an empty Dataframe
df=[]              
df=pan.read_csv('/Users/Gideon/Desktop/Fortune500_Religious_Freedom/URLS.csv')
df2=df

URLS=df["URLS"]

#Declaring the Protected Class List
protectedclasslist=['Race','Gender','Disability','SOGI','Military','Age','Family','Religion']



#Importing the Fortune 500 Company List.
companylist = pan.read_csv ('/Users/Gideon/Desktop/Fortune500_Religious_Freedom/fortune500list.csv')


#Adding Colomuns for each Protected Class in the data frame.  And Attaching the company list.
df["Race"]=np.nan
df["Gender"]=np.nan
df["Disability"]=np.nan
df["SOGI"]=np.nan
df["Military"]=np.nan
df["Age"]=np.nan
df["Family"]=np.nan
df["Religion"]=np.nan
df["Company_Name"]=companylist
print(df)


#Reading in the Terms list
Mastertermlist = pan.read_csv('/Users/Gideon/Desktop/Fortune500_Religious_Freedom/Mastertermslist-edited.csv')

#Checking the term list.
print(Mastertermlist)

#declaring important variables
tracking=-1
termsmasterlist=[]
terms=[]
currentlist=[]
failedtoreach=[]
NeedstobemanuallyScraped=[]
verboten=[]
aspx=[]
electednottorespond=[]

#Declaring Some Scraper Settings, and declaring  
HEADERS={"Mozilla/5.0" : "(Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
pdfcounter=0
blacklisted=['https://www.lkqcorp.com/wp-content/uploads/2020/10/LKQCorp_COE_Booklet_10-2020_web.pdf','https://investor.drhorton.com/~/media/Files/D/D-R-Horton-IR/documents/human-rights-policy-final.pdf','https://www.uber.com/us/en/about/diversity/','https://investors.lennar.com/~/media/Files/L/Lennar-IR-V3/documents/governance-documents/lennar-2022-social-responsibility-report.pdf','https://www.delekus.com/wp-content/uploads/2020/09/2020-09-24-DEI-Policy-FINAL-website.pdf','https://www.citizensbank.com/diversity-equity-and-inclusion/default.aspx','https://investors.watsco.com/static-files/da132c80-d459-42d8-ba28-86c0ce35cd57','https://www.selectmedical.com/-/media/project/selectmedical/dotcom/usa/pdf/sm-diversity-and-inclusion-report-04-2022.pdf?t=20220405125212','https://www.biglots.com/images/marketing/2021/2020_BigLots_CSR_Report_FINAL.pdf','https://www.diamondbackenergy.com/static-files/faf5ab25-5ab5-4404-8c04-c7bd387ae418','https://www.oracle.com/corporate/careers/diversity-inclusion/','https://www.bookingholdings.com/cr-cards/diversity-inclusion-and-belonging-2021/']
seleniumresistnat=['https://www.targaresources.com/sustainability/social','https://www.mckesson.com/About-McKesson/Impact/Inclusion-and-Diversity/','https://www.chrobinson.com/en-us/about-us/corporate-responsibility/diversity-inclusion/','https://www.bakerhughes.com/company/corporate-responsibility/people/diversity-equity-and-inclusion']



#### @@WEBDriVer IS HERE ####

#Options = webdriver.ChromeOptions()
#settings = {
#       "recentDestinations": [{
#            "id": "Save as PDF",
#            "origin": "local",
#            "account": "",
#        }],
#        "selectedDestinationId": "Save as PDF",
#        "version": 2
#    }
#prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings), 'savefile.default_directory': '/Users/Gideon/Desktop/Fortune500_Religious_Freedom/2022_Saved_Website_Data'}
#Options.add_experimental_option('prefs', prefs)
#Options.add_argument('--kiosk-printing')
#driver_path = '/Users/Gideon/Desktop/Python_Testing/Google_Scraper/jeeves/jeeves/The_Chrome_WebDriver/chromedriver_2'
#driver = webdriver.Chrome(options=Options, executable_path=driver_path)


bar = progressbar.ProgressBar(max_value=500,
                              widgets=widgets).start()

    
    


##the j loop, what happens for every url

playsound('Beggining.mp3')
for j in df['URLS']:
    
    #Adds on to the tracking variable
    tracking=tracking+1
    currentcompanyname=df.iat[tracking,10]
    print("commencing to scrape ", currentcompanyname)
    bar.update(tracking)
    #Checks if URL has been blacklisted
    if j in blacklisted:
        ##Automatically sets the values for this site to 0?
        text=' nothing '
        df.loc[tracking,2:10]=nan
        print(" ")
        print("Site is Blacklisted Saving No Data")
        print(" ")
        print(" ")
        pass
    else:
        #checks if the URL has a unique file type
        pdf='.pdf'      
        file_extension = pathlib.Path(j).suffix 
        if file_extension==".aspx":
            aspx.append(j)
            #df.loc[tracking,2:10]=nan
            r_obj = requests.Session()
            fr_soup=r_obj.get(j,timeout=3)
            soup= BeautifulSoup(fr_soup.content, "lxml")
            soup.body
            page_body = soup.body
            text = page_body.get_text()
            print(text)
            print("I Found an ASPX!")
            count=text.count("The")
            print("Just to Prove it here are the number of times the word 'The' appears in it", count)
        if "static" in j:
            print("I FOUND A STATIC FILE")
            text=" "
            path=os.path.join('/Users/Gideon/Desktop/Fortune500_Religious_Freedom/2022_Saved_Website_Data/',currentcompanyname+".pdf")
            filename = Path(path)  ##  Okay it was working, and now its using the one before its name.... which is odd...
            response = requests.get(j)
            print(filename)
            filename.write_bytes(response.content)
            pdfFileObj = open(filename,'rb')
            pdfReader= PyPDF2.PdfFileReader(pdfFileObj)
            totalpages=pdfReader.numPages
            for x in range(totalpages):
                pageObj=pdfReader.getPage(x)
                text1=pageObj.extractText()
                text=text+" "+text1
            pdfFileObj.close()
            pdfcounter=pdfcounter+1
        #PDF Exception
        if file_extension==pdf:
            text="  "
            #Save PDF in System
            path=os.path.join('/Users/Gideon/Desktop/Fortune500_Religious_Freedom/2022_Saved_Website_Data/',currentcompanyname+".pdf")
            filename = Path(path)  ##  Okay it was working, and now its using the one before its name.... which is odd...
            response = requests.get(j)
            print(filename)
            filename.write_bytes(response.content)
            pdfFileObj = open(filename,'rb')
            pdfReader= PyPDF2.PdfFileReader(pdfFileObj)
            totalpages=pdfReader.numPages
            for x in range(totalpages):
                pageObj=pdfReader.getPage(x)
                text1=pageObj.extractText()
                text=text+" "+text1
            pdfFileObj.close()
            pdfcounter=pdfcounter+1            
        else:
            try:
                page=requests.get(j, timeout=3, headers={'User-Agent': 'Mozilla/5.0'})
                path=os.path.join('/Users/Gideon/Desktop/Fortune500_Religious_Freedom/2022_Saved_Website_Data/',currentcompanyname+".pdf")
            except:
                print(" ")
                print("Big Error")
                print("Skipping, Site electing not to be scrapped")
                print(" ")
                df.loc[tracking,2:10]=nan
                electednottorespond.append(j)
                cumulativecount=0
                pass
            soup = BeautifulSoup(page.content, 'html.parser')
            page_body = soup.body
            text = page_body.get_text()
        columncounter=1   
        for i in protectedclasslist:
            terms=Mastertermlist[i].tolist()
            cleanedList = [x for x in terms if str(x) != 'nan']
            cumulativecount=0
            for k in cleanedList:
                count=text.count(k)
                cumulativecount=count+cumulativecount
            columncounter=columncounter+1
            df.iat[tracking,columncounter]=cumulativecount    
            print(i, " ", cumulativecount)
            cumulativecount=0
    print("Scrapping is Complete")
    print(" ")
    print(" ")
    if tracking==501:
        break

failedtoreach=failedtoreach.append(aspx)
dict=failedtoreach
df3=pan.DataFrame(dict)
df3.to_csv("/Users/Gideon/Desktop/Fortune500_Religious_Freedom/Exceptions.csv", index= False)
            
df.to_csv('/Users/Gideon/Desktop/Fortune500_Religious_Freedom/ScrappedData.csv', index=False) 
print(" ")   
print("Loop Completed on Loop: ",tracking)
print(" ")
print("The Number Of PDFS SCrapped Were: ", pdfcounter)
print(" ")
print(" ")
print(" ")
print("The sites the elected not to be scrapped were ",electednottorespond)
print(" ")
print(" ")
print("The List of Sites Currently Black Listed Is: ", blacklisted)
playsound('Test Complete.mp3')


#print("Commencing PDF Saving Expect this it take 4 hours")

print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(df)
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print("Project Complete Sir, Data Waiting your Review")
print(" ")
print(" ")
#print('Comencing PDF Cataloging')






##Remaining Items
#going to need to use BORB for all these PDFs with HTML in them.  can borb replace my PDF functions?

#static Files?
#integrate everything into one script.  

#I think Uber is Blacklisted.