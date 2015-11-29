import urllib, urllib2
import json
import httplib2

from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.context_processors import csrf
from django.views import generic

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import PurchaseHistory
from .forms import PurchaseHistoryForm

import logging
log = logging.getLogger(__name__)

'''
def index(request):
    url = "https://careers.undercovertourist.com/assignment/1/products/"
    products = getProduct(url)['results']
    
    args = {
        'user':request.user,
        'products':products,
    }
    
    return render_to_response('index.html', args)
'''

class IndexView(generic.ListView):
    model = None
    template_name = 'index.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        url = "https://careers.undercovertourist.com/assignment/1/products/"
        return getProduct(url)['results']
    

    
'''
def detail(request, productID=False):
    if not productID:
        return redirect("index")
    else:
        url = "https://careers.undercovertourist.com/assignment/1/products/"+str(productID)+"/"
        product = getProduct(url)
        
        args = {
            'user':request.user,
            'product':product,
        }
        
        return render_to_response('detail.html', args)
'''


class DetailView(generic.ListView):
    model = None
    template_name = 'detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        url = "https://careers.undercovertourist.com/assignment/1/products/"+str(self.kwargs['productID'])+"/"
        return getProduct(url)
    

'''
def purchase(request, productID=False):
    if request.method == 'POST':
        form = PurchaseHistoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            price = form.cleaned_data['price']
            phone = form.cleanPhone()
            quantity = form.cleaned_data['quantity']
            
            #Send Purchase Order to API
            purchaseData = {
                "customer_email": email,
                "customer_name": name,
                "customer_phone": phone,
                "quantity": int(quantity)
            }
            
            url = 'https://careers.undercovertourist.com/assignment/1/products/'+str(productID)+'/purchase'
            http = httplib2.Http()
            headers = {'Content-type': 'application/x-www-form-urlencoded', 'X-Auth':'robert.boyett'}
            response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(purchaseData))
            content = json.loads(content)
            
            
            if response['status'] == '200':
                #Create PurchaseHistory
                purchaseHistory = PurchaseHistory.objects.create(
                    fullName = name,
                    confirmation_code = content['confirmation_code'],
                    name = content['product']['name'],
                    price = float(content['product']['price']),
                    email = email,
                    phone = phone,
                    quantityTickets = quantity,
                )
                data = {'success':{'purchaseID':purchaseHistory.id}}
            
            else:
                #error
                data = {'error':'Sorry, we are having problems with our system.  Please try to submit your purchase again.  If this problem continues, please contact us at (800)555-5555.'}
                
            return HttpResponse(json.dumps(data))
            
        else:
            return HttpResponse(form.errors.as_json())
        
    else:
        url = "http://careers.undercovertourist.com/assignment/1/products/"+str(productID)+"/"
        product = getProduct(url)
        
        if request.user.is_authenticated():
            form = PurchaseHistoryForm(initial={"name":request.user.get_full_name, "email":request.user.email, "price":product['price']})
        else:
            form = PurchaseHistoryForm(initial={"price":product['price']})
        args = {
            "user":request.user,
            "form":form,
            "product":product,
        }
        args.update(csrf(request))
        
        return render_to_response("purchase.html", args)
'''

class PurchaseView(generic.FormView):
    template_name = 'purchase.html'
    form_class = PurchaseHistoryForm

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        price = form.cleaned_data['price']
        phone = form.cleanPhone()
        quantity = form.cleaned_data['quantity']
            
        #Send Purchase Order to API
        purchaseData = {
            "customer_email": email,
            "customer_name": name,
            "customer_phone": phone,
            "quantity": int(quantity)
        }
            
        url = 'https://careers.undercovertourist.com/assignment/1/products/'+str(self.kwargs['productID'])+'/purchase'
        http = httplib2.Http()
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'X-Auth':'robert.boyett'}
        response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(purchaseData))
        content = json.loads(content)
        
        log.info(content['confirmation_code'])
        log.info(response['status'])
        
        if response['status'] == '200':
            #Create PurchaseHistory
            purchaseHistory = PurchaseHistory.objects.create(
                fullName = name,
                confirmation_code = content['confirmation_code'],
                name = content['product']['name'],
                price = float(content['product']['price']),
                email = email,
                phone = phone,
                quantityTickets = int(quantity),
            )
            
            
            emailArgs = {
                "purchaseHistory":purchaseHistory,
            }
            #Send email confirmation
            subject = "My Travel Shop Purchase Confirmation"
            sender = "My Travel Shop Inc. <purchase@ducksoup.us>"
    
            html_content = render_to_string('email_verification.html', emailArgs)
            text_content = render_to_string('email_verification.txt', emailArgs)
            msg = EmailMultiAlternatives(subject, text_content,
                                         sender, [email])
            
            msg.attach_alternative(html_content, "text/html")
            
            msg.mixed_subtype = 'related'
            msg.send()
            
            data = {'success':{'purchaseID':purchaseHistory.id}}
        
        else:
            #error
            data = {'error':'Sorry, we are having problems with our system.  Please try to submit your purchase again.  If this problem continues, please contact us at (800)555-5555.'}
            
        return HttpResponse(json.dumps(data))
    
    def form_invalid(self, form):
        return HttpResponse(form.errors.as_json())
    
    def get(self, request, *args, **kwargs):
        url = "http://careers.undercovertourist.com/assignment/1/products/"+str(self.kwargs['productID'])+"/"
        product = getProduct(url)
        
        if request.user.is_authenticated():
            form = PurchaseHistoryForm(initial={"name":request.user.get_full_name, "email":request.user.email, "price":product['price']})
        else:
            form = PurchaseHistoryForm(initial={"price":product['price']})
        
        return self.render_to_response(self.get_context_data(form=form, product=product))
        
        
        
    

class SuccessView(generic.DetailView):
    model = PurchaseHistory
    template_name = 'success.html'
    context_object_name = 'purchaseHistory'







#----------------------------misc functions---------------------------
def getProduct(url):
    try:
        #X-Auth: roger.moore
        opener = urllib2.build_opener()
        opener.addheaders = [('X-Auth', 'robert.boyett')]
        response = opener.open(url)
        
        #response = urllib2.urlopen(url)
        return json.loads(response.read())
    except urllib2.URLError, e:
        log.error('URLError = ' + str(e.reason))
        return False
            
    
    


import string
from time import time
from itertools import chain
from random import seed, choice, sample


def generateConfirmationCode(length=10, digits=5, upper=0, lower=5):
    seed(time())

    lowercase = string.lowercase.translate(None, "o")
    uppercase = string.uppercase.translate(None, "O")
    letters = "{0:s}{1:s}".format(lowercase, uppercase)

    confirmationCode = list(
        chain(
            (choice(uppercase) for _ in range(upper)),
            (choice(lowercase) for _ in range(lower)),
            (choice(string.digits) for _ in range(digits)),
            (choice(letters) for _ in range((length - digits - upper - lower)))
        )
    )

    return "".join(sample(confirmationCode, len(confirmationCode)))





