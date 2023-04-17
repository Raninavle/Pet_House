from django.shortcuts import render,redirect
from django.http import HttpResponse
from adminapp.models import Category,Pets,UserInfo,Pet_Cat,Old_Order,PaymentMaster
from userapp.models import MyCart,OrderMaster
from django.contrib import messages
import random
from twilio.rest import Client
# Create your views here.
def homepage(request):
    cat = Category.objects.all()
    pet = Pets.objects.all()
    return render(request,'homepage.html',{'category':cat,'pet':pet})

def login(request):
    uname = request.POST["username"]
    pwd = request.POST["password"]
    pet = Pets.objects.all()
    
    try:
        user = UserInfo.objects.get(username=uname, pwd=pwd)
    except:
        alert = "!!.Invalid Credential..!!"
        return render(request,"homepage.html",{"alert1":alert,'pet':pet})
    else:
        request.session["uname"] = user.username
        if ("uname" in request.session):
            request.session["fname"] = user.fname
            return redirect(homepage)
        

def signup(request):
    pet = Pets.objects.all()
    fname = request.POST["fname"].upper()
    lname = request.POST["lname"].upper()
    mob = request.POST["mob"]
    username = request.POST["user"]
    password = request.POST["pwd"]
    user = UserInfo()
    user.fname = fname
    user.lname = lname
    user.mobile = mob
    user.username = username
    user.pwd = password
    try:
        user.save()
    except:
        alert = "!!.USER-NAME EXIST.!!"
        return render(request,"homepage.html",{"alert1":alert,'pet':pet})
    else:
        alert = "!!.SIGN-UP SUCCESSFULL.!!"
        return render(request,"homepage.html",{"alert1":alert,'pet':pet})
        
def about(request):
    cat = Category.objects.all()
    return render(request,"about.html",{"category":cat})


def gallary(request):
    cat = Category.objects.all()
    pet = Pets.objects.all()
    return render(request,"gallary.html",{"category":cat,"pet":pet})

def contact(request):
    cat = Category.objects.all()
    return render(request,"contact.html",{"category":cat})

def logout(request):
    request.session.clear()
    return redirect(homepage)


def viewsSection(request,id):
    animl = Pet_Cat.objects.filter(pet=id)
    cat = Category.objects.all()
    pet = Pets.objects.all()
    return render(request, "viewsSection.html",{'category':cat,'pet':pet,'animl':animl})


def showPets(request,id):
    pets = Pets.objects.filter(cat=id)
    cat = Category.objects.all()
    return render (request,"gallary.html",{'category':cat,'pet':pets})

def readMore(request,id):
    cat = Category.objects.all()
    try:
        animl = Pet_Cat.objects.get(id=id)
    except:
        return redirect(homepage)
    else:
        return render (request,"readMore.html",{'category':cat,'animl':animl})




def addTocart(request):
    if(request.method == "POST"):
        if("uname" in request.session):
            petid = request.POST['petid']
            user = request.session['uname']
            pet = Pet_Cat.objects.get(id=petid)
            user = UserInfo.objects.get(username = user)
            try:
                cart = MyCart.objects.get(pet=pet, user=user)# match data                   
            except:
                cart = MyCart()
                cart.user = user
                cart.pet=pet
                cart.save()
                return redirect(showAllCart)
            else:
                messages.success(request, "* Already In Cart")
                return redirect(showAllCart)
        else:
            pet = Pets.objects.all()
            alert = "!!..PLEASE SIGN-IN..!!"
            return render(request,"homepage.html",{"alert1":alert,'pet':pet})
        
def showAllCart(request):
    cat = Category.objects.all()
    if(request.method =="GET"):
        uname = request.session["uname"]
        user = UserInfo.objects.get(username = uname)
        cartitem = MyCart.objects.filter(user=user)
        his = Old_Order.objects.filter(user=user.id)
        #print(cartitem.id)
        total = 0
        for item in cartitem:
            total = (total) + float(item.pet.price)

        request.session["total"] = total
        return render(request,"showAllCart.html",{'item':cartitem,'category':cat,'history':his})

    
def removeItem(request):
    uname = request.session["uname"]
    user = UserInfo.objects.get(username = uname)
    id = request.POST["petid"]
    pet = Pet_Cat.objects.get(id=id)
    item = MyCart.objects.get(user=user,pet=pet)
    item.delete()
    return redirect(showAllCart)

def MakePayment(request):
    if(request.method == "GET"):
        cat = Category.objects.all()
        return render(request, "makepayment.html",{'category':cat})

    else:
        cardno = request.POST["cardno"]
        cvv = request.POST["cvv"]
        expiry = request.POST["expiry"]
        try:
            # retrieve a PaymentMaster object that matches the extracted card details from the database
            buyer = PaymentMaster.objects.get(cardno = cardno,cvv=cvv,expiry=expiry)
        except:
            alert = "* INVALID-DETAILS"
            return render(request,"makepayment.html",{"alert":alert})
        else:
             #Its a match
            owner = PaymentMaster.objects.get(cardno='12345',cvv='222',expiry='12/2026')
            # updates the balances of the owner and buyer's payment accounts,
            owner.balance += request.session["total"]
            buyer.balance -=request.session["total"]
            owner.save()
            buyer.save()
            #Delete all items from cart
            uname = request.session["fname"]
            user = UserInfo.objects.get(fname = uname)
            
            order = OrderMaster()
            order.user = user
            order.amount = request.session["total"]
            #order.dateOfOrder = datetime.now
            #Fetch all cart items for that user
            details = ""
            items = MyCart.objects.filter(user=user)
            for item in items:
                details += (item.pet.category)+","
                item.delete()            
            order.details = details
            order.save()
            return render(request,"PaymentSuccess.html",{})

            