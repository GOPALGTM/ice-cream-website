from django.shortcuts import render, HttpResponse
from datetime import datetime


from myapp.models import Contact
from django.contrib import messages

# Create your views here.

def index(reequest):
    return render(reequest,'index.html')

    #return HttpResponse("this is homepage")
def about(reequest):
    # return HttpResponse("this is about page")
    return render(reequest,'about.html')

def services(reequest):
   # return HttpResponse("this is services page")
    return render(reequest,'services.html')
    
def contact(reequest):
    if reequest.method == "POST":
      name=reequest.POST.get('name')
      email=reequest.POST.get('email')
      phone=reequest.POST.get('phone')
      desc=reequest.POST.get('desc')
      contact=Contact(name=name, email=email,phone=phone,desc=desc, date=datetime.today())
      contact.save()
      messages.success(reequest, 'your  message has been sent...')

    return render(reequest,'contact.html')
  #  return HttpResponse("this is contact page")
