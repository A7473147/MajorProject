from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector
from .forms import LoginForm


# Create your views here.
def home(request):
    print(request.POST)
    return render(request,'index.html');

def about(request):
    print(request.POST)
    return render(request,'about.html');

def downloads(request):
    return render(request,'downloads.html');

def contact(request):
    return render(request,'contact.html');

def showlogindata(request):
    fm=LoginForm()
    return render(request,'login.html',{'form':fm})
 

def login(request):
    # username=request.POST.get('username')
    # print(request.POST)
    # print(username)
    return render(request,'login.html');

def queries(request):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="major_project"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM UploadedData")
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