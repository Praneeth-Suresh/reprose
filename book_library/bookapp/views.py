from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader, Template
from django.middleware.csrf import get_token
from bookapp.models import users, Listings
import smtplib

# Create your views here.
def homepage(request):
    if 'user_login' in request.session:
        context = {
        "home_class": "active",
        "about_class": "inactive",
        "contact_class": "inactive",
        "ishidden": "hidden",
        "isnothidden": ""
        }
    else:
        context = {
            "home_class": "active",
            "about_class": "inactive",
            "contact_class": "inactive",
            "ishidden": "",
            "isnothidden": "hidden"
        }

    renderdata = {}
    renderdata['context'] = context
    template = loader.get_template('homepage.html')
    return HttpResponse(template.render(renderdata, request))

def signup(request):
    #Create csrf token
    csrf_token = get_token(request)

    #If the form is submitted
    if request.method == "POST":
        #check if email id does not already exist
        if not users.objects.filter(email_id=request.POST["email"]):
            #check if passwords match or not
            if request.POST["password_1"] == request.POST["password_2"]:
                error_message = ""
                context = {
                    "csrf_token": csrf_token,
                    "error_message": error_message,
                    "ishidden": "",
                    "isnothidden": "hidden"
                }
                firstname = request.POST["firstname"]
                lastname = request.POST["lastname"]
                emailid = request.POST["email"]
                pw = request.POST["password_1"]
                data = users(firstname=firstname, lastname=lastname, email_id=emailid, password=pw)
                data.save()
                request.session['user_login'] = str(users.objects.get(email_id=emailid).id)
                request.session.modify = True
                return redirect('homepage')
            else:
                error_message = "Passwords do not match"
                context = {
                    "csrf_token": csrf_token,
                    "error_message": error_message,
                    "ishidden": "",
                    "isnothidden": "hidden"
                }
                renderdata = {}
                renderdata['context'] = context 
                template = loader.get_template('signup.html')
                return HttpResponse(template.render(renderdata, request))
        else:
            error_message = "Email ID is already registered"
            context = {
                "csrf_token": csrf_token,
                "error_message": error_message,
                "ishidden": "",
                "isnothidden": "hidden"
            }
            template = loader.get_template('signup.html')
            renderdata = {}
            renderdata['context'] = context
            return HttpResponse(template.render(renderdata, request))
    else:
        context = {
            "csrf_token": csrf_token,
            "ishidden": "",
            "isnothidden": "hidden"
        }
        renderdata = {}
        renderdata['context'] = context
        template = loader.get_template('signup.html')
        return HttpResponse(template.render(renderdata, request))

def login(request):
    #Create csrf token
    csrf_token = get_token(request)

    #Once form is submitted
    if request.method == "POST":
        email_address = request.POST["email"]
        pw = request.POST["password"]
        #Check if the particular email id and password exits in the database
        if users.objects.filter(email_id=email_address) and users.objects.filter(password=pw):
            user_id = users.objects.get(email_id=email_address).id
            if pw == users.objects.get(id=user_id).password:
                error_message = ""
                context = {
                    "csrf_token": csrf_token,
                    "error_message": error_message,
                    "ishidden": "",
                    "isnothidden": "hidden"
                    }
                request.session['user_login'] = str(users.objects.get(email_id=email_address).id)
                request.session.modify = True
                return redirect('homepage')
            else:
                error_message = "record not found"
                context = {
                    "csrf_token": csrf_token,
                    "error_message": error_message,
                    "ishidden": "",
                    "isnothidden": "hidden"
                }

                renderdata = {}
                renderdata['context'] = context

                template = loader.get_template('login.html')
                return HttpResponse(template.render(renderdata, request))
        else:
            error_message = "record not found"
            context = {
                "csrf_token": csrf_token,
                "error_message": error_message,
                "ishidden": "",
                "isnothidden": "hidden"
            }
            renderdata = {}
            renderdata['context'] = context

            template = loader.get_template('login.html')
            return HttpResponse(template.render(renderdata, request))
    else:
        context = {
            "csrf_token": csrf_token,
            "ishidden": "",
            "isnothidden": "hidden"
        }

        renderdata = {}
        renderdata['context'] = context
        
        template = loader.get_template('login.html')
        return HttpResponse(template.render(renderdata, request))

def about(request):
    if 'user_login' in request.session:
        context = {
            "ishidden": "hidden",
            "isnothidden": "",
            "home_class": "inactive",
            "about_class": "active",
            "contact_class": "inactive",
        }
    else:
        context = {
            "ishidden": "",
            "isnothidden": "hidden",
            "home_class": "inactive",
            "about_class": "active",
            "contact_class": "inactive",
        }

    renderdata = {}
    renderdata['context'] = context
    template = loader.get_template('about.html')
    return HttpResponse(template.render(renderdata))

def contact(request):
    if 'user_login' in request.session:
        context = {
            "ishidden": "hidden",
            "isnothidden": "",
            "home_class": "inactive",
            "about_class": "inactive",
            "contact_class": "active",
        }
    else:
        context = {
            "ishidden": "",
            "isnothidden": "hidden",
            "home_class": "inactive",
            "about_class": "inactive",
            "contact_class": "active",
        }

    renderdata = {}
    renderdata['context'] = context
    template = loader.get_template('contact.html')
    return HttpResponse(template.render(renderdata))

def website_template(request):
    template = loader.get_template('website_template.html')
    return HttpResponse(template.render())

def test(request):
    template = loader.get_template('test.html')
    return HttpResponse(template.render())

def profile(request):
    if 'user_login' in request.session:
        context = {
            "ishidden": "hidden",
            "isnothidden": "",
            "home_class": "inactive",
            "about_class": "inactive",
            "contact_class": "inactive",
        }
    else:
        context = {
            "ishidden": "",
            "isnothidden": "hidden",
            "home_class": "inactive",
            "about_class": "inactive",
            "contact_class": "inactive",
        }

    print("request session")
    print(request.session)

    renderdata = {}
    renderdata['context'] = context
    template = loader.get_template('profile.html')
    return HttpResponse(template.render(renderdata, request))

def browse_listings(request):
    csrf_token = get_token(request)
    if request.method == "POST":
        query = request.POST["query"]
        if 'user_login' in request.session:
            context = {
                "csrf_token": csrf_token,
                "ishidden": "hidden",
                "isnothidden": "",
                "home_class": "inactive",
                "about_class": "inactive",
                "contact_class": "inactive",
                "query": query,
                "madequery": ""
            }
        else:
            context = {
                "csrf_token": csrf_token,
                "ishidden": "",
                "isnothidden": "hidden",
                "home_class": "inactive",
                "about_class": "inactive",
                "contact_class": "inactive",
                "query": query,
                "madequery": ""
            }
    else:
        if 'user_login' in request.session:
            context = {
                "csrf_token": csrf_token,
                "ishidden": "hidden",
                "isnothidden": "",
                "home_class": "inactive",
                "about_class": "inactive",
                "contact_class": "inactive",
                "query": "",
                "madequery": "hidden"
            }
        else:
            context = {
                "csrf_token": csrf_token,
                "ishidden": "",
                "isnothidden": "hidden",
                "home_class": "inactive",
                "about_class": "inactive",
                "contact_class": "inactive",
                "query": "",
                "madequery": "hidden"
            }
    
    # [book name, book imgurl, book description]
    listings = {
        'Book1': {
            'name': "Lord of the Rings",
            'imgurl': "https://hips.hearstapps.com/hmg-prod/images/lordoftherings-1636391090.jpg",
            'description': "Lord of the rings is a stunning masterpiece of a book",
        },
        'Book2': {
            'name': "Harry Potter",
            'imgurl': "https://self-publishingschool.com/wp-content/uploads/2023/05/harry-potter-books-in-order.webp",
            'description': "Harry Potter is about a potter called Harry",
        },
    
    }

    # add context and listings into a 2d dict called renderdata

    renderdata = {}

    renderdata['context'] = context
    renderdata['listings'] = listings

    template = loader.get_template('search.html')
    return HttpResponse(template.render(renderdata, request))

def add_listing(request):
    csrf_token = get_token(request)
    context = {
        "csrf_token": csrf_token,
    }
    if request.method == "POST":
        book_title = request.POST["title"]
        isbn = request.POST["isbn"]
        genre = request.POST["genre"]
        isForSale = bool(request.POST["sale"])
        data = Listings(userid=request.session['user_login'], book_title=book_title, isbn=isbn, genre=genre, for_sale=isForSale, for_borrowing=not isForSale)
        data.save()
        print(data)
    else:
        template = loader.get_template('add_listing.html')
        return HttpResponse(template.render(context, request))

def signout(request):
    del request.session['user_login']
    return redirect('homepage')

def forgot(request):
    #Create csrf token
    csrf_token = get_token(request)

    #Once form is submitted
    if request.method == "POST":
        user_email_address = request.POST["email"]

        print("email address: ", user_email_address) # Needs to send email with new password

        # send email to reset password
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login('ispsinstock@gmail.com', 'acsfrsxmxbtcrmbj')

        
            subject = 'Reprose Password Reset'
            body = f'To reset your password, click on the following link: https://www.youtube.com/watch?v=htlhY5BgrKU&ab_channel=SnowyJake'

            msg = f'Subject: {subject}\n\n{body}'

            smtp.sendmail('ispsinstock@gmail.com', user_email_address, msg)


        return redirect('homepage')
    else:
        context = {
            "csrf_token": csrf_token,
            "ishidden": "",
            "isnothidden": "hidden"
        }

        renderdata = {}
        renderdata['context'] = context
        
        template = loader.get_template('forgotPassword.html')
        return HttpResponse(template.render(renderdata, request))
    


