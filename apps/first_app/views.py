from django.shortcuts import render, redirect
from django.conf import settings
from django.conf.urls.static import static
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import *
import bcrypt
import re
import stripe

def index(request):
    variables = {}
    if 'user_id' in request.session :
        variables['person_logged_in'] = User.objects.filter(id = request.session['user_id'])[0]
    return render(request, 'first_app/index.html', variables)

def register(request):
    return render(request, 'first_app/register.html')

def create_user(request):
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    errors = []
    if len(request.POST["first_name"]) < 1:
        errors.append("You must enter a first name")
    if len(request.POST["first_name"]) > 1 and not request.POST["first_name"].isalpha():
        errors.append("Your first name must not have numbers")
    if len(request.POST["last_name"]) < 1:
        errors.append("You must enter a last name")
    if  len(request.POST["last_name"]) > 1 and not request.POST["last_name"].isalpha():
        errors.append("Your last name must not have numbers")

    if len(request.POST["email"]) < 1:
        errors.append("You must enter an email")
    
    if len(request.POST["email"]) > 1 and not EMAIL_REGEX.match(request.POST["email"]):
        errors.append("Your email must be an email")

    if len(request.POST["password"]) < 8:
        errors.append("You must enter a password that is at least 8 characters")
    if not request.POST["password"] == request.POST["confirm_password"]:
        errors.append("Your password must match password confirmation")
    try:
        User.objects.filter(email=request.POST["email"])[0]
        messages.error(request, 'You are already registered')
    except:
        fname = request.POST["first_name"]
        lname = request.POST["last_name"]
        em = request.POST["email"]
        password = request.POST["password"]

        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            hashed_pw = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            correct_hashed_pw = hashed_pw.decode("utf-8")
            print(hashed_pw)
            print(correct_hashed_pw)
            new_user = User.objects.create(first_name = fname, last_name = lname, email = em, password = correct_hashed_pw)
            request.session['user_id'] = new_user.id
            print(new_user)
            Cart.objects.create(user_id = request.session['user_id'])
            return redirect('/user_profile/{}'.format(request.session['user_id']))
    return redirect("/register")

def user_profile(request, user_id):
    variables = {
        'user' : User.objects.filter(id = user_id)[0],
    }
    if 'user_id' in request.session :
        variables['person_logged_in'] = User.objects.filter(id = request.session['user_id'])[0]
        variables['sesh'] = request.session['user_id']
    return render(request, 'first_app/user_profile.html', variables)

def sign_in(request):
    return render(request, 'first_app/sign_in.html')

def sign_me_in(request):
    errors = []
    if len(request.POST["email"]) < 1:
        errors.append("You must enter an email!")
    if len(request.POST["password"]) < 8:
        errors.append("You must enter a password that is at least 8 characters!")

    if errors:
        for e in errors:
            messages.error(request, e)
    else:
        try:
            user = User.objects.filter(email=request.POST["email"])[0]
        except:
            messages.error(request, 'Your email does not exist. Please register.')
            return redirect('/sign_in')

        check_pass = bcrypt.checkpw(request.POST["password"].encode(), user.password.encode())
        print(check_pass)
        if check_pass:
            request.session["user_id"] = user.id
        else:
            messages.error(request, 'Email/Password does not match.')
            return redirect("/sign_in")

        return redirect('/user_profile/{}'.format(request.session["user_id"]))
    return redirect("/sign_in")

def logout(request):
    request.session.clear()
    return redirect("/")

def artists(request):
    variables = {
        'artists' : User.objects.all(),
    }
    if 'user_id' in request.session :
        variables['user'] = User.objects.filter(id = request.session['user_id'])[0]
    return render(request, 'first_app/artists.html', variables)

def artwork(request):
    variables = {
        'art' : Artwork.objects.all()
    }
    if 'user_id' in request.session :
        variables['user'] = User.objects.filter(id = request.session['user_id'])[0]
    return render(request, 'first_app/artwork.html', variables)

def new_artwork(request):
    variables = {}
    if 'user_id' in request.session :
        variables['user'] = User.objects.filter(id = request.session['user_id'])[0]
    return render(request, 'first_app/new_artwork.html', variables)

def create_item(request, methods='POST'):
    print(request.POST)
    print(request.FILES)
    errors = []
    if len(request.POST["title"]) < 1:
        errors.append("You must enter a title")

    if len(request.POST["description"]) < 1:
        errors.append("You must enter a description")

    if len(request.POST["price"]) < 1:
        errors.append("You must enter a price")

    if not 'art_photo' in request.FILES:
        errors.append("You must upload a product photo")

    if not 'art_file' in request.FILES:
        errors.append("You must upload a product file")
    
    try:
        Artwork.objects.filter(title = request.POST["title"])[0]
        messages.error(request, 'This product title is already taken')
    except:
        this_title = request.POST["title"]
        this_description = request.POST["description"]
        this_price = request.POST["price"]
        if request.method == 'POST' and 'art_photo' in request.FILES:
            this_photo = request.FILES["art_photo"]
        if request.method == 'POST' and 'art_file' in request.FILES:
            this_file = request.FILES["art_file"]
    
        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            new_product = Artwork.objects.create(title = this_title, description = this_description, price = this_price, art_photo = this_photo, art_file = this_file, user = User.objects.get(id = request.session['user_id']))
            # request.session['user_id'] = new_user.id
            print(new_product)
            return redirect('/user_profile/{}'.format(request.session['user_id']))
    return redirect("/new_artwork")
    
def product(request, art_id):
    variables = {
        'art' : Artwork.objects.filter(id = art_id)[0]
    }
    if 'user_id' in request.session :
        variables['user'] = User.objects.filter(id = request.session['user_id'])[0]
    return render(request, 'first_app/product.html', variables)

def cart(request):
    c = Cart.objects.get(user_id = request.session['user_id'])
    cart_artworks = c.artwork.all()
    total_price = 0
    for art in cart_artworks :
        total_price += art.price

    variables = {
        'artworks' : c.artwork.all(),
        'total_price' : total_price,
        'stripe_price' : total_price * 100
    }
    if 'user_id' in request.session :
        variables['user'] = User.objects.filter(id = request.session['user_id'])[0]
    return render(request, 'first_app/cart.html', variables)

def add_to_cart(request, art_id, user_id):
    # this_user = User.objects.filter(id = user_id)[0]
    if 'user_id' in request.session :
        c = Cart.objects.get(user__id = user_id)
        this_artwork = Artwork.objects.filter(id = art_id)[0]
        c.artwork.add(this_artwork)
    return redirect('/cart')
    # return redirect('/cart/{}'.format(user_id))

def edit_product(request, art_id):
    variables = {
        'art' : Artwork.objects.filter(id = art_id)[0]
    }
    if 'user_id' in request.session :
        variables['user'] = User.objects.filter(id = request.session['user_id'])[0]
    return render(request, 'first_app/edit_product.html', variables)

def edit_this_product(request, art_id, methods = 'POST'):
    print(request.POST)
    errors = []
    if len(request.POST["title"]) < 1:
        errors.append("You must enter a title")

    if len(request.POST["description"]) < 1:
        errors.append("You must enter a description")

    if len(request.POST["price"]) < 1:
        errors.append("You must enter a price")

    if not 'art_photo' in request.FILES:
        errors.append("You must upload a product photo")

    if not 'art_file' in request.FILES:
        errors.append("You must upload a product file")
    
    # try:
        # Artwork.objects.filter(title = request.POST["title"])[0]
        # messages.error(request, 'This product title is already taken')
    # except:
    if errors:
        for e in errors:
            messages.error(request, e)
    else:
        a = Artwork.objects.get(id = art_id)
        a.title = request.POST["title"]
        a.description = request.POST["description"]
        a.price = request.POST["price"]
        if request.method == 'POST' and 'art_photo' in request.FILES:
            a.art_photo = request.FILES["art_photo"]
        if request.method == 'POST' and 'art_file' in request.FILES:
            a.art_file = request.FILES["art_file"]
        a.save()
        return redirect("/product/{}".format(art_id))
    return redirect("/edit_product/{}".format(art_id))

def delete_product(request, art_id, user_id):
    Artwork.objects.get(id = art_id).delete()
    # request.session.clear()
    return redirect('/user_profile/{}'.format(user_id))

def edit_my_profile(request, user_id):
    variables = {}
    if 'user_id' in request.session :
        variables['user'] = User.objects.filter(id = request.session['user_id'])[0]
    return render(request, 'first_app/edit_profile.html', variables)

def edit_profile(request, user_id, methods = 'POST'):
    print("request ", request.POST)
    errors = []
    if len(request.POST["first_name"]) < 1:
        errors.append("You must enter a first name")
    if len(request.POST["first_name"]) > 1 and not request.POST["first_name"].isalpha():
        errors.append("Your first name must not have numbers")
    if len(request.POST["last_name"]) < 1:
        errors.append("You must enter a last name")
    if  len(request.POST["last_name"]) > 1 and not request.POST["last_name"].isalpha():
        errors.append("Your last name must not have numbers")
    # try:
        # User.objects.filter(email=request.POST["email"])[0]
        # messages.error(request, 'You are already registered')
    # except:
        # fname = request.POST["first_name"]
        # lname = request.POST["last_name"]
        # em = request.POST["email"]
        # password = request.POST["password"]

    if errors:
        for e in errors:
            messages.error(request, e)
    else:
        u = User.objects.get(id = user_id)
        u.first_name = request.POST["first_name"]
        u.last_name = request.POST["last_name"]
        u.save()
        return redirect('/user_profile/{}'.format(request.session['user_id']))
    return redirect('/edit_profile/{}'.format(request.session['user_id']))

def delete_profile(request, user_id):
    User.objects.get(id = user_id).delete()
    request.session.clear()
    return redirect("/")

def search(request):
    variables = {
        'art' : Artwork.objects.filter(title__startswith = request.POST['search']),
        'user' : User.objects.filter(first_name__startswith = request.POST['search'])
    }
    return render(request, 'first_app/search_output.html', variables)

def make_purchase(request):
    print(request.POST)
    # Set your secret key: remember to change this to your live secret key in production
    # See your keys here: https://dashboard.stripe.com/account/apikeys
    stripe.api_key = "sk_test_8iDEYyI6tlxGjdzmOIBjGRC5"

    # Token is created using Checkout or Elements!
    # Get the payment token ID submitted by the form:
    token = request.POST['stripeToken'] # Using Flask

    charge = stripe.Charge.create(
        amount=request.POST['amount'],
        currency="usd",
        source="tok_visa",
        transfer_group="{ORDER10}",
    )
    
    cart = Cart.objects.get(user_id = request.session['user_id'])

    for artwork in cart.artwork:
        # Create a Transfer to a connected account - for each shop (later):
        transfer = stripe.Transfer.create(
            amount=artwork.price,
            currency="usd",
            destination="{artwork.user.stripeID}",
            transfer_group="{ORDER10}",
        )

    return redirect("/cart")

def remove_item(request, art_id):
    cart = Cart.objects.get(user_id = request.session['user_id'])
    artwork = Artwork.objects.get(id = art_id)
    cart.artwork.remove(artwork)
    return redirect("/cart")
