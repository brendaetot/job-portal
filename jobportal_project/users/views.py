from django.shortcuts import render, redirect 
import mysql.connector
from django.http import HttpResponse
import base64
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



# Create your views here.
import mysql.connector

    # Connect to the database
db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="jobs2"
    )
    
    # Create a cursor object to execute queries
mycursor = db.cursor()
def home(request):
    return render(request, 'index.html')

def regapplicant(request):
    err=''
    if request.method=="POST" and request.FILES.get('document'):
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword=request.POST.get('confirmpassword')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        nationality = request.POST.get('nationality')
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        country_code = request.POST.get('country-code')
        country = request.POST.get('country')
        education_level = request.POST.get('education-level')
        years_of_experience = request.POST.get('years-of-experience')
        resume = request.FILES['document']
        file_content =resume.read()
        encoded_file = base64.b64encode(file_content).decode('utf-8')

        
        if password==confirmpassword:
            sql = "INSERT INTO applicants(name,email,password,dob,gender,nationality,location,phone,country_code, country,education_level,years_of_experience,resume) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (name,email,password,dob,gender,nationality,location,phone,country_code,country,education_level,years_of_experience,encoded_file)
            mycursor.execute(sql, val)
            db.commit()
            err="password don't match"
            print("Retry")
            return redirect('login_applicant')
        else:

            sql = "INSERT INTO applicants(name,email,password,dob,gender,nationality,location,phone,country_code, country,education_level,years_of_experience,resume) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (name,email,password,dob,gender,nationality,location,phone,country_code,country,education_level,years_of_experience,resume.read())
            mycursor.execute(sql, val)
            db.commit()
            return redirect('login_applicant')
            # err="password don't match"
            # print("Retry")
    return render(request,"regapplicant.html",{'msg':err})
    

def regemployer(request):
   
    err=''
    if request.method=="POST":
        companyname=request.POST.get('companyname')
        companyemail=request.POST.get('companyemail')
        countrycode=request.POST.get('countrycode')
        country=request.POST.get('country')
        location=request.POST.get('location')
        password=request.POST.get('password')
        confirmpassword=request.POST.get('confirmpassword')
        if password==confirmpassword:
            sql="INSERT INTO recruiter(company_name,company_email,country_code,country,location,password) VALUES(%s,%s,%s,%s, %s, %s)"
            VAL=(companyname,companyemail,countrycode,country,location,password)
            mycursor.execute(sql,VAL)
            db.commit()
            return redirect('login_recruiter')
        else:
            err="password don't match"
            print("Retry")
    return render(request,"regemployer.html",{'msg':err})

def signup(request):
    return render(request, 'signup.html')

def base(request):
    return render(request, 'base.html')
def addjobs(request):
     if request.method=="POST":
        jobTitle=request.POST.get('jobTitle')
        jobDescription=request.POST.get('jobDescription')
        jobLocation=request.POST.get('jobLocation')
        jobType=request.POST.get('jobType')
        jobCategory=request.POST.get('jobCategory')
        jobRequirements=request.POST.get('jobRequirements')
        sql="INSERT INTO job_postings(Job_Title,Job_Description,Job_Location,Job_Type,Job_Category,Job_Requirements) VALUES(%s,%s,%s,%s, %s, %s)"
        VAL=(jobTitle,jobDescription,jobLocation,jobType,jobCategory,jobRequirements)
        mycursor.execute(sql,VAL)
        db.commit()
        return redirect('recruiter_dashboard')



# def login_applicant(request):

#     err=''
#     if request.method=="POST":
#         email=request.POST.get('email')
#         password=request.POST.get('password')
#         sql="SELECT * FROM applicants"
#         mycursor.execute(sql)
#         results=mycursor.fetchall()
#         print(results)
#         for i in results:
#             print(i)
#             if i[2]==email and i[3]==password:
#                 print("logged in")
#                 # err="Successful Login"
#                 return redirect('applicant_dashboard')
#             else:
#                 err="invalid email address or password"
#     return render(request, 'login_applicant.html', {'msg':err})
# def login_recruiter(request):
#     err=""
#     if request.method=="POST":
#         email=request.POST.get('email')
#         password=request.POST.get('password')
#         sql="SELECT * FROM recruiter"
#         mycursor.execute(sql)
#         results=mycursor.fetchall()
#         print(results)
#         for i in results:
#             print(i)
#             if i[2]==email and i[6]==password:
#                 # print("logged in")
#                 # err="login Successful"
#                 return redirect('recruiter_dashboard')
#             else:
#                 err="invalid email address or password"
#     return render(request, 'login_recruiter.html', {'msg':err})
# SESSION LOGIN AND LOGOUT


def login_applicant(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # picking data from the database
        sql = "SELECT * FROM applicants WHERE email = %s AND password = %s"
        mycursor.execute(sql, (email, password))
        user = mycursor.fetchone()

        if user:
            messages.success(request, 'Login successful.')
            return redirect('applicant_dashboard')
        else:
            messages.error(request, 'Invalid email address or password.')

    return render(request, 'login_applicant.html')
def login_recruiter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # picking data from the database
        sql = "SELECT * FROM recruiter WHERE company_email = %s AND password = %s"
        mycursor.execute(sql, (email, password))
        user = mycursor.fetchone()

        if user:
            messages.success(request, 'Login successful.')
            return redirect('recruiter_dashboard')
        else:
            messages.error(request, 'Invalid email address or password.')

    return render(request, 'login_recruiter.html')




def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('home')  



def applicant_dashboard(request):
    sql="SELECT * FROM job_postings"
    mycursor.execute(sql)
    results=mycursor.fetchall()
    print(results)
    return render(request, 'applicant_dashboard.html', {'results':results})
def recruiter_dashboard(request):
    sql="SELECT * FROM job_postings"
    mycursor.execute(sql)
    results=mycursor.fetchall()
    print(results)
    return render(request, 'recruiter_dashboard.html', {'results':results})


def edit_job(request, id):
    
    if request.method == 'POST':
        job_title = request.POST['jobTitle']
        job_description = request.POST['jobDescription']
        job_location = request.POST['jobLocation']
        job_type = request.POST['jobType']
        job_category = request.POST['jobCategory']
        job_requirements = request.POST['jobRequirements']
        
        with db.cursor() as cursor:
            cursor.execute("""
            UPDATE job_postings
            SET job_title = %s, job_description = %s, job_location = %s, job_type = %s, job_category = %s, job_requirements = %s
            WHERE id = %s
            """, [job_title, job_description, job_location, job_type, job_category, job_requirements, id])    # return HttpResponse("Edited Job with ID: " + id)
            return redirect('/recruiter_dashboard')
        
    else:
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM job_postings
                WHERE id = %s
            """, [id])
            job = cursor.fetchone()
            id = job[0]
            title = job[1]
            description =job[2]
            location = job[3]
            type = job[4]
            category = job[5]
            requirements = job[6]
        
        
        
        return render(request, 'edit_job.html', { 'id': id, 'title':title, 'description':description, 'location':location, 'type':type, 'category':category, 'requirements':requirements})
    
def delete_job(request, job_id):
    # a raw SQL DELETE query to remove data from the database
    with db.cursor() as cursor:
        sql = "DELETE FROM job_postings WHERE id = %s"  
        cursor.execute(sql, [job_id])
        return redirect('/recruiter_dashboard')

    # return HttpResponse("A job with ID {} has been deleted.".format(job_id))

def logout_applicant(request):
    try:
        del request.session['user']
    except:
        return redirect('login_applicant')
    return redirect('login_applicant')
def logout_recruiter(request):
    try:
        del request.session['user']
    except:
        return redirect('login_recruiter')
    return redirect('login_recruiter')


