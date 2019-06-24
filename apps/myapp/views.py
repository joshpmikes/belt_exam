from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
import re

def index (request):
    return render(request, "myapp/index.html")

def create_user(request):
    error = False
    if len(request.POST["first_name"]) < 2:
        messages.error(request, "first name must be a minumum of 2 characters")
        error = True
    if len(request.POST["last_name"]) < 2:
        messages.error(request, "last name must be a minumum of 2 characters")
        error = True
    if len(request.POST["email"]) < 7:
        messages.error(request, "invalid email")
        error = True
    if request.POST["password"] != request.POST["c_password"]:
        messages.error(request, "Passwords did not match! Try again.")
        error = True

    matching_users = User.objects.filter(email = request.POST['email'])
    if len(matching_users) > 0:
        messages.error(request, "Account already associated with email.")
        error = True

    if error:
        return redirect ('/')
   
    hashed = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
    user = User.objects.create(first_name=request.POST["first_name"],last_name=request.POST["last_name"],email=request.POST["email"],password=hashed)

    request.session['user_id'] = user.id

    return redirect ("/quotes")

def login(request):
    matching_users = User.objects.filter(email = request.POST['email'])
    if len(matching_users) > 0:
        user = matching_users[0]
        if bcrypt.checkpw(request.POST['password'].encode(),user.password.encode()):
            request.session['user_id'] = user.id
            print(request.POST['password'])
            return redirect('/quotes')
        else : 
            messages.error(request, "Invalid password.")
    else:
        messages.error(request, "Invalid email.")
    return redirect ('/')

def quotes(request):
    if not 'user_id' in request.session:
        return redirect('/')
    context = {
        "user" : User.objects.get(id=request.session['user_id']),
        "all_quotes": Quote.objects.all()
    }


    return render(request, "myapp/quotes.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")

def upload_quote(request):
    error = False
    if len(request.POST["author"]) < 4:
        messages.error(request, "The author must be a minumum of 4 characters")
        error=True
    if len(request.POST["actual_quote"]) < 11:
        messages.error(request, "The quote must be a minumum of 11 characters")
        error=True
    if error:
        return redirect ("/quotes")
        
    else:
        user = User.objects.get(id=request.session['user_id'])
        new_quote = Quote.objects.create(author=request.POST["author"], actual_quote=request.POST["actual_quote"], uploaded_by= user)
        messages.error(request, "You have successfully added a new quote! Add another below!")
        return redirect ("/quotes")

def like_quote(request, quote_id):
    user = User.objects.get(id=request.session['user_id'])
    quote = Quote.objects.get(id=quote_id)
    all_likes = quote.users_who_liked.all()
    if user in all_likes:
        messages.error(request, "You have already liked this quote")
        return redirect("/quotes")

    else:
        quote = Quote.objects.get(id=quote_id)
        user = User.objects.get(id=request.session['user_id'])
        user.quotes_liked.add(quote)
        return redirect ("/quotes")

def delete_quote(request, quote_id):
    user = User.objects.get(id=request.session['user_id'])
    quote = Quote.objects.get(id=quote_id)
    quote.delete()
    return redirect ("/quotes")

def user_page(request, user_id):
    context = {
        "user" : User.objects.get(id=user_id),
    }
   
    return render (request, "myapp/userpage.html", context)

def edit_user(request, user_id):
    context = {
        "user" : User.objects.get(id=user_id)
    }
    return render(request, "myapp/edit_user.html", context)

def update_user(request, user_id):
    error = False
    if len(request.POST["first_name"]) < 2:
        messages.error(request, "first name must be a minumum of 2 characters")
        error = True
    if len(request.POST["last_name"]) < 2:
        messages.error(request, "last name must be a minumum of 2 characters")
        error = True

    addy_to_verify = request.POST["email"]
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addy_to_verify)
    if match == None:
        messages.error(request, "invalid email")
        error = True

    matching_users = User.objects.filter(email = request.POST['email'])
    if len(matching_users) > 0:
        messages.error(request, "Account already associated with email.")
        error = True

    if error:
        return redirect (f'/myaccount/{user_id}')

    else:
        user = User.objects.get(id=request.session['user_id'])
        user.first_name= request.POST["first_name"]
        user.last_name= request.POST["last_name"]
        user.email= request.POST["email"]
        user.save()
        return redirect ("/quotes")
        