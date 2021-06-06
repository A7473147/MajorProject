from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector
from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv


# Create your views here.
def home(request):
    print(request.POST)
    return render(request,'index.html');

def about(request):
    print(request.POST)
    return render(request,'about.html');

def downloads(request):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="major_project"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM UploadedData")

    myresult = mycursor.fetchall()
    return render(request,'downloads.html',{'myresult': myresult});

def contact(request):
    return render(request,'contact.html');

def login(request):
    # username=request.POST.get('username')
    # print(request.POST)
    # print(username)
    return render(request,'login.html');

def scriptrequest(request):
    requested_by =request.POST.get('name')
    email=request.POST.get('email')
    mob_no=request.POST.get('mobile')
    website_name=request.POST.get('website_name')
    website_url=request.POST.get('website_url')
    print(requested_by,email,mob_no,website_name,website_url)
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="major_project"
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO Queries (Name, Email,Mobile,Website_name,Website_link) VALUES (%s, %s,%s, %s,%s)"
    val = (requested_by,email,mob_no,website_name,website_url)
    mycursor.execute(sql, val)
    mydb.commit()

    # print(mycursor.rowcount, "record inserted.")
    return render(request,'login.html');

def queries(request):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="major_project"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Queries")
    myresult = mycursor.fetchall()
    return render(request,'queries.html',{'myresult': myresult});


def scriptavailable(request):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="major_project"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM UploadedData")

    myresult = mycursor.fetchall()

    
    return render(request,'scriptavailable.html',{'myresult': myresult});


def adddata(request):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="major_project"
    )
    requested_by =request.POST.get('requester')
    web_name=request.POST.get('wn')
    web_link=request.POST.get('wl')
    script_name=request.POST.get('sn')
    description=request.POST.get('desc')
    print(web_name,web_link,script_name,description,requested_by)
    mycursor = mydb.cursor()
    print(request.POST)

    sql = "INSERT INTO UploadedData (WebsiteName,WebsiteUrl,ScriptName,Description,RequestedBy) VALUES (%s, %s,%s, %s,%s)"
    val = (web_name,web_link,script_name,description,requested_by)
    mycursor.execute(sql, val)
    mydb.commit()
    s= "Thank you we got your data, We will try to resolve your query as soon as possible"
    return render(request,'addscript.html',{'s':s});


def addscript(request):
    
    return render(request,'addscript.html');


def downloadscript(request, id):
    if id ==1 :
        amazonLaptop()
    elif id ==2 :
        flipkartLaptops()
    elif id ==3:
        flipkart_smartphones()
    return render(request,'downloads.html');


def flipkart_smartphones():
    products = []
    prices = []
    ratings = []
    pages = list(range(1,24))
    for page in pages:
      req = requests.get("https://www.flipkart.com/search?q=smartphone&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_5_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_5_na_na_ps&as-pos=1&as-type=RECENT&suggestionId=smartphone%7CMobiles&requestId=2eeafc6f-c849-4545-9be5-76316776a5f3&as-searchtext=smart={}".format(page)).text 
      soup = BeautifulSoup(req,'html.parser')
      name = soup.find_all('div' , class_='_4rR01T')
      for i in range(len(name)):
        products.append(name[i].text)
      price = soup.find_all('div',class_='_30jeq3 _1_WHN1') 
      # Extracting price of each laptop from the website
      for i in range(len(price)):
        prices.append('Rs.'+price[i].text)
      rating = soup.find_all('div',class_='_3LWZlK')
      for i in range(len(rating)):
        ratings.append(rating[i].text)
    ratinglist = ratings[:len(products)]
    print(len(ratinglist))
    df = {'Product':products,'Price':prices,'Rating':ratinglist}
    dataset = pd.DataFrame(df)

    dataset.to_csv('flipkart_smartphones.csv')

def flipkartLaptops():
    products = [] # Create a list to store the descriptions
    prices = []

    processor = []
    ram = []
    os = []
    storage = []
    warranty = []
    inches = []
    pages = list(range(1,21))
    for page in pages:
      req = requests.get("https://www.flipkart.com/search?q=laptops&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off={}".format(page)).text  # URL of the website which you want to scrape
      #content = req.content # Get the content
      soup = BeautifulSoup(req,'html.parser')
      #print(soup.prettify())

      name = soup.find_all('div' , class_='_4rR01T')
      for i in range(len(name)):
        products.append(name[i].text)
      len(products)
      price = soup.find_all('div',class_='_30jeq3 _1_WHN1') 
      # Extracting price of each laptop from the website
      for i in range(len(price)):
        prices.append(price[i].text)
      commonclass = soup.find_all('li',class_='rgWa7D') # We observe that the classnames for the different specifications are under one div.So we need to apply some method to extract the different features.
      # Create empty lists for the features
      for i in range(0,len(commonclass)):
        p=commonclass[i].text # Extracting the text from the tags
        if("Core" in p): 
            processor.append(p)
        elif("RAM" in p): 
            ram.append(p)
        elif("HDD" in p or "SSD" in p):
            storage.append(p)
        elif("Operating" in p):
            os.append(p)
        elif("Display" in p):
            inches.append(p)
        elif("Warranty" in p):
            warranty.append(p)
    df = {'Product':products,'RAM':ram,'Price':prices}
    dataset = pd.DataFrame(df)

    dataset.to_csv('laptop.csv')

def amazonLaptop():
      products = [] # Create a list to store the descriptions
      prices = []
      pages = list(range(1,21))
      for page in pages:
        req = requests.get("https://www.amazon.in/s?k=laptop&ref=nb_sb_noss_2&page={}".format(page)).text  # URL of the website which you want to scrape
        #content = req.content # Get the content
        soup = BeautifulSoup(req,'html.parser')
        name = soup.find_all('span' , class_='a-size-medium a-color-base a-text-normal')
        for i in range(len(name)):
          products.append(name[i].text)
        len(products)
        price = soup.find_all('span', class_='a-price-whole') 
        for i in range(len(price)):
          prices.append(price[i].text)
      productlist = products[:len(prices)]
      df = {'Product':productlist,'Price':prices}
      dataset = pd.DataFrame(df)

      dataset.to_csv('amazonLaptop.csv')
