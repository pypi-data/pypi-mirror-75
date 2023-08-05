from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from .forms import NewUserForm, SearchForm, CollectionSearchForm, EditUserForm, UpdateUserForm, UpdateSellerForm, UpdatePreferencesForm
from .models import Card, Listing, Collection, Collection_Content, Card_Type, Card_Rarity, Bazaar_User, Seller, User_Preferences, Notification
from urllib.parse import unquote_plus, quote_plus


# homepage view
def home(request):
    raw_string = request.META['QUERY_STRING']
    query_parameters = raw_string.split("&")

    card_name = ''
    card_name_raw = ''
    card_text = ''
    card_text_raw= ''
    card_flavor_text = ''
    card_flavor_text_raw = ''
    card_keywords = ''
    card_keywords_raw = ''
    card_artist = ''
    card_artist_raw = ''
    set_name = ''
    set_name_raw = ''
    seller_name = ''
    seller_name_raw = ''
    auction_house_search = ''
    auction_house_search_raw = ''
    sponsored = ''
    sponsored_raw = ''
    color_black = ''
    color_red = ''
    color_white = ''
    color_blue = ''
    color_green = ''  
    min_power = 0
    max_power = 0
    min_toughness = 0
    max_toughness = 0
    min_converted_mana_cost = 0
    max_converted_mana_cost = 0
    #Arbitrarily picked -7777777 as a default sentinel value
    collection_number = -7777777
    minprice = 0.00
    maxprice = 0.00

    card_type = 'NO_VALUE' 
    card_rarity = 'NO_VALUE'




    sort_by_choice = 'card_name'
    sorting_order = 'ascending'


    page = 1
    if raw_string != '':
        for parameter in query_parameters: 
            parameter_tokens = parameter.split("=")
            parameter_name = parameter_tokens[0]
            if len(parameter_tokens) <= 0:
                parameter_val = None
            else:
                parameter_val = parameter_tokens[1]
            if parameter_name == "card_name":
                card_name_raw = parameter_val
                card_name = unquote_plus(card_name_raw)
            elif parameter_name == "card_type":
                card_type = parameter_val
            elif parameter_name == "card_rarity":
                card_rarity = parameter_val
            elif parameter_name == "sort_by_choice":
                sort_by_choice = parameter_val
            elif parameter_name == "sorting_order":
                sorting_order = parameter_val
            elif parameter_name == "page":
                page = parameter_val
            elif parameter_name == "card_text":
                card_text_raw = parameter_val
                card_text = unquote_plus(card_text_raw)
            elif parameter_name == "color_black" and parameter_val == "on":
                color_black = "on"
            elif parameter_name == "color_red" and parameter_val == "on":
                color_red = "on"
            elif parameter_name == "color_white" and parameter_val == "on":
                color_white = "on"
            elif parameter_name == "color_blue" and parameter_val == "on":
                color_blue = "on"
            elif parameter_name == "color_green" and parameter_val == "on":
                color_green = "on"                                                                             
            elif parameter_name == "card_keywords":
                card_keywords_raw = parameter_val
                card_keywords = unquote_plus(card_keywords_raw)
            elif parameter_name == "min_power":
                min_power = int(parameter_val)
            elif parameter_name == "max_power":
                max_power = int(parameter_val)                
            elif parameter_name == "min_toughness":
                min_toughness = int(parameter_val)
            elif parameter_name == "max_toughness":
                max_toughness = int(parameter_val)
            elif parameter_name == "min_converted_mana_cost":
                min_converted_mana_cost = int(parameter_val)
            elif parameter_name == "max_converted_mana_cost":
                max_converted_mana_cost = int(parameter_val)                
            elif parameter_name == "collection_number" and parameter_val != '':
                collection_number = int(parameter_val)
            elif parameter_name == "card_flavor_text":
                card_flavor_text_raw = parameter_val
                card_flavor_text = unquote_plus(card_flavor_text_raw)
            elif parameter_name == "card_artist":
                card_artist_raw = parameter_val
                card_artist = unquote_plus(card_artist_raw)
            elif parameter_name == "set_name":
                set_name_raw = parameter_val
                set_name = unquote_plus(set_name_raw)
            elif parameter_name == "minprice":
                 minprice = float(parameter_val)
            elif parameter_name == "maxprice":
                 maxprice = float(parameter_val)
            elif parameter_name == "seller_name":
                seller_name_raw = parameter_val
                seller_name = unquote_plus(seller_name_raw)
            elif parameter_name == "auction_house_search":
                auction_house_search_raw = parameter_val
                auction_house_search = unquote_plus(auction_house_search_raw)
            elif parameter_name == "sponsored":
                sponsored_raw = parameter_val
                sponsored = unquote_plus(sponsored_raw)


    #If the collection_number is set to -7777777, reset it to None
    if collection_number == -7777777:
        collection_number = None

    if request.method == "GET":              
        #Place form variables from GET request into form
        form = SearchForm({
            'auction_house_search': auction_house_search,
            'sponsored': sponsored,
            'card_name': card_name,
            'card_text': card_text,
            'card_flavor_text': card_flavor_text,
            'card_artist': card_artist,
            'set_name': set_name,
            'seller_name': seller_name, 
            'minprice': minprice,
            'maxprice': maxprice,
            'min_converted_mana_cost': min_converted_mana_cost,
            'max_converted_mana_cost': max_converted_mana_cost,
            'min_power': min_power,
            'max_power': max_power,
            'min_toughness': min_toughness,
            'max_toughness': max_toughness,
            'card_keywords': card_keywords,
            'card_type': card_type,
            'color_black': color_black, 
            'color_red': color_red,
            'color_white': color_white,
            'color_blue': color_blue,
            'color_green': color_green,
            'card_rarity': card_rarity,
            'collection_number': collection_number,
            'sort_by_choice': sort_by_choice,
            'sorting_order': sorting_order
        })
    
        if form.is_valid():
            listing_manager = Listing.objects


            #TODO: Look into issue with filtering on boolean
            #Related link: https://stackoverflow.com/questions/6933196/django-boolean-queryset-filter-not-working
            if auction_house_search == 'no':
                listings = listing_manager.filter(user_listing = False)
            else:
                listings = listing_manager.filter(user_listing = True)

            if sponsored == 'no':
                listings = listing_manager.filter(sponsored = False)
            else:
                listings = listing_manager.filter(sponsored = True)

            # Filtering by name (if name not specified, this will return all cards)
            listings = listing_manager.filter(product_id__name__icontains = card_name)

            # Filtering by card_text (if card_text not specified, this will return all cards)
            if card_text != '':
                listings = listing_manager.filter(product_id__card_text__icontains = card_text)

            # Filtering by card_artist (if card_artist not specified, this will return all cards)
            if card_artist != '':
                listings = listing_manager.filter(product_id__artist__icontains = card_artist)

            # Filtering by card_flavor_text (if card_flavor_text not specified, this will return all cards)
            if card_flavor_text != '':
                listings = listing_manager.filter(product_id__flavor_text__icontains = card_flavor_text)

            #Filter by Card Keywords
            if card_keywords != '':
                listings = listing_manager.filter(product_id__card_keywords__icontains = card_keywords)

            #Filter by Card Keywords
            if set_name != '':
                listings = listing_manager.filter(product_id__set_name__icontains = set_name)

            # Filter by Card Type
            if form.cleaned_data['card_type'] != 'NO_VALUE':
                listings = listings.filter(product_id__type_id__card_type__contains = card_type)

            # Filter by Card Rarity
            if form.cleaned_data['card_rarity'] != 'NO_VALUE':
                listings = listings.filter(product_id__rarity_id__card_rarity__iexact = card_rarity)

            #Filter by Toughness
            if min_toughness != 0 and max_toughness != 0:
                listings = listings.filter(product_id__toughness__lte = max_toughness)
                listings = listings.filter(product_id__toughness__gte = min_toughness)
            
            #Filter by Power
            if min_power != 0 and max_power != 0:
                listings = listings.filter(product_id__power__lte = max_power)
                listings = listings.filter(product_id__power__gte = min_power)

            #Filter by Converted Mana Cost
            if min_converted_mana_cost != 0 and max_converted_mana_cost != 0:
                listings = listings.filter(product_id__converted_mana_cost__lte = max_converted_mana_cost)
                listings = listings.filter(product_id__converted_mana_cost__gte = min_converted_mana_cost)
      
            #Filter by Price
            if minprice != float(0) and maxprice != float(0):
                listings = listings.filter(price__lte = maxprice)
                listings = listings.filter(price__gte = minprice)

            #Filter by Card Colors
            color_filter = False
            if color_black == "on":
                listings = listings.filter(product_id__card_color__icontains = 'B')
                color_filter = True
            if color_red == "on":
                listings = listings.filter(product_id__card_color__contains = 'R')
                color_filter = True
            if color_white == "on":
                listings = listings.filter(product_id__card_color__icontains = 'W')
                color_filter = True
            if color_blue == "on":
                listings = listings.filter(product_id__card_color__icontains = 'U')
                color_filter = True
            if color_green == "on":
                listings = listings.filter(product_id__card_color__icontains = 'G')
                color_filter = True
            
            #Exclude non-colored cards if any filtering based on color has been done
            if color_filter:
                listings = listings.exclude(product_id__card_color = 'No color available')


            #Filter by Collection Number 
            if collection_number != None:
                listings = listings.filter(product_id__collection_number__iexact = collection_number)

            #Filter by seller name 
            #TODO: Implement Auction house search, may require model change and need to search by different column
            if auction_house_search == 'no':
                if seller_name != '':
                    listings = listing_manager.filter(seller_key_id__seller_name__icontains = seller_name)

  
            # Implement sorts
            if sort_by_choice == 'card_name':
                sort_param = "product_id__name"
            elif sort_by_choice == 'card_rarity':
                sort_param = "product_id__rarity_id__card_rarity"
            elif sort_by_choice == 'card_type':
                sort_param = "product_id__type_id__card_type"

            if sorting_order == "descending":
                sort_param = "-" + sort_param
### BEGIN query string 

            if card_name != '': 
                dynamic_form_qs = r"card_name=" + quote_plus(card_name) + r"&"
            else:
                dynamic_form_qs = r"card_name=" + card_name + r"&"

            dynamic_form_qs = dynamic_form_qs + r"min_converted_mana_cost=" + str(min_converted_mana_cost) + r"&"
            dynamic_form_qs = dynamic_form_qs + r"max_converted_mana_cost=" + str(max_converted_mana_cost) + r"&"


            dynamic_form_qs = dynamic_form_qs + r"min_power=" + str(min_power) + r"&"
            dynamic_form_qs = dynamic_form_qs + r"max_power=" + str(max_power) + r"&"


            dynamic_form_qs = dynamic_form_qs + r"min_toughness=" + str(min_toughness) + r"&"
            dynamic_form_qs = dynamic_form_qs + r"max_toughness=" + str(max_toughness) + r"&"

            if card_keywords != '': 
                dynamic_form_qs = dynamic_form_qs + r"card_keywords=" + quote_plus(card_keywords) + r"&"
            else:
                dynamic_form_qs = dynamic_form_qs + r"card_keywords=" + card_keywords + r"&"
            
            #Add the colors to the query string
            if color_black != '':
                dynamic_form_qs = dynamic_form_qs + r"color_black=" + quote_plus(color_black) + r"&"

            if color_red != '':
                dynamic_form_qs = dynamic_form_qs + r"color_red=" + quote_plus(color_red) + r"&"

            if color_white != '':
                dynamic_form_qs = dynamic_form_qs + r"color_white=" + quote_plus(color_white) + r"&"

            if color_blue != '':
                dynamic_form_qs = dynamic_form_qs + r"color_blue=" + quote_plus(color_blue) + r"&"

            if color_green != '':
                dynamic_form_qs = dynamic_form_qs + r"color_green=" + quote_plus(color_green) + r"&"

            if card_text != '': 
                dynamic_form_qs = dynamic_form_qs + r"card_text=" + quote_plus(card_text) + r"&"
            else:
                dynamic_form_qs = dynamic_form_qs + r"card_text=" + card_text + r"&"

            if card_flavor_text != '': 
                dynamic_form_qs = dynamic_form_qs + r"card_flavor_text=" + quote_plus(card_flavor_text) + r"&"
            else:
                dynamic_form_qs = dynamic_form_qs + r"card_flavor_text=" + card_flavor_text + r"&"

            if card_type != '': 
                dynamic_form_qs = dynamic_form_qs + r"card_type=" + quote_plus(card_type) + r"&"
            else:
                dynamic_form_qs = dynamic_form_qs + r"card_type=" + card_type + r"&"

            if card_rarity != '': 
                dynamic_form_qs = dynamic_form_qs + r"card_rarity=" + quote_plus(card_rarity) + r"&"
            else:
                dynamic_form_qs = dynamic_form_qs + r"card_rarity=" + card_rarity + r"&"

            dynamic_form_qs = dynamic_form_qs + r"collection_number=" + str(collection_number) + r"&"

            if sort_by_choice != '': 
                dynamic_form_qs = dynamic_form_qs + r"sort_by_choice=" + quote_plus(sort_by_choice) + r"&"
            else:
                dynamic_form_qs = dynamic_form_qs + r"sort_by_choice=" + sort_by_choice + r"&"

            if card_artist != '': 
                dynamic_form_qs = dynamic_form_qs + r"card_artist=" + quote_plus(card_artist) + r"&"
            else:
                dynamic_form_qs = dynamic_form_qs + r"card_artist=" + card_artist + r"&"

            if sorting_order != '': 
                dynamic_form_qs = dynamic_form_qs + r"sorting_order=" + quote_plus(sorting_order)
            else:
                dynamic_form_qs = dynamic_form_qs + r"sorting_order=" + sorting_order 

            if set_name != '': 
                dynamic_form_qs = dynamic_form_qs + r"set_name=" + quote_plus(set_name)
            else:
                dynamic_form_qs = dynamic_form_qs + r"set_name=" + set_name 

            dynamic_form_qs = dynamic_form_qs + r"minprice=" + str(minprice) + r"&"
            dynamic_form_qs = dynamic_form_qs + r"maxprice=" + str(maxprice) + r"&"

            if seller_name != '': 
                dynamic_form_qs = dynamic_form_qs + r"seller_name=" + quote_plus(seller_name)
            else:
                dynamic_form_qs = dynamic_form_qs + r"seller_name=" + seller_name 

            if auction_house_search != '': 
                dynamic_form_qs = dynamic_form_qs + r"auction_house_search=" + quote_plus(auction_house_search)
            else:
                dynamic_form_qs = dynamic_form_qs + r"auction_house_search=" + auction_house_search 

            if sponsored != '': 
                dynamic_form_qs = dynamic_form_qs + r"sponsored=" + quote_plus(sponsored)
            else:
                dynamic_form_qs = dynamic_form_qs + r"sponsored=" + sponsored 
                
            #TODO: Debug pring statement for form query string
            #print("DYNAMIC_STRING:")
            #print(dynamic_form_qs)
### END query string 

            # Sort the QuerySet per the parameter
            listings = listings.order_by(sort_param)
            # display only 25 cards per page
            paginator = Paginator(listings, 24)

            try:
                page_obj = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                page = 1
                page_obj = paginator.page(page)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                page_obj = paginator.page(paginator.num_pages)    
            return render(request=request,
                          template_name='main/home.html',
                          context={'data': page_obj, 'form': form,'dynamic_form_qs': dynamic_form_qs})  # load necessary schemas
        else:
            listings = Listing.objects.all()
            # display only 25 cards per page
            paginator = Paginator(listings, 24)

            try:
                page_obj = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                page = 1
                page_obj = paginator.page(page)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                page_obj = paginator.page(paginator.num_pages)

            #Place form variables from GET request into form
            form = SearchForm({
                'auction_house_search': auction_house_search,
                'sponsored': sponsored,
                'card_name': card_name,
                'card_text': card_text,
                'card_flavor_text': card_flavor_text,
                'card_artist': card_artist,
                'set_name': set_name,
                'seller_name': seller_name, 
                'minprice': minprice,
                'maxprice': maxprice,
                'min_converted_mana_cost': min_converted_mana_cost,
                'max_converted_mana_cost': max_converted_mana_cost,
                'min_power': min_power,
                'max_power': max_power,
                'min_toughness': min_toughness,
                'max_toughness': max_toughness,
                'card_keywords': card_keywords,
                'card_type': card_type,
                'color_black': color_black, 
                'color_red': color_red,
                'color_white': color_white,
                'color_blue': color_blue,
                'color_green': color_green,
                'card_rarity': card_rarity,
                'collection_number': collection_number,
                'sort_by_choice': sort_by_choice,
                'sorting_order': sorting_order
            })


            
            return render(request=request,
                          template_name='main/home.html',
                          context={'data': page_obj, 'form': form, 'dynamic_form_qs': dynamic_form_qs})  # load necessary schemas



# registration page form
def register(request):
    # upon submit
    if request.method == "POST":
        form = NewUserForm(request.POST)
        # validate user input, create new user account, login user
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("main:home")
        # error, don't create new user account
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            
            return render(request=request,
                          template_name="main/registration/register.html",
                          context={"form": form})
    form = NewUserForm
    return render(request=request,
                  template_name="main/registration/register.html",
                  context={"form": form})


# login form
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        # validate user input
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # authenticate user in db
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request=request,
                  template_name="main/registration/login.html",
                  context={"form": form})


# user collection and notification management
def collection(request):
    # if a user is logged in see if they have a collection
    if request.user.is_authenticated:
        users_collection = None
        cards_in_collection = []
        try:
            users_collection = Collection.objects.get(owning_auth_user_id=request.user.id)
        except Collection.DoesNotExist:
            pass
        # if the user has a collection, get it
        if users_collection:
            collection_content, product_ids, return_dicts = [], [], []
            try:
                collection_content = Collection_Content.objects.filter(collection_id=users_collection.id)
                if request.method == "POST":
                    form = CollectionSearchForm(request.POST)
                    if form.is_valid():
                        # Filter by Ownership
                        if form.cleaned_data['own'] == 'yes' and form.cleaned_data['dont_own'] == 'yes':
                            pass
                        elif form.cleaned_data['own'] == 'no' and form.cleaned_data['dont_own'] == 'yes':
                            collection_content = collection_content.filter(obtained=False)
                        elif form.cleaned_data['own'] == 'yes' and form.cleaned_data['dont_own'] == 'no':
                            collection_content = collection_content.filter(obtained=True)
                        else:
                            collection_content = None

                        # now filter on Card attributes
                        if collection_content is not None:
                            for item in collection_content:
                                product_ids.append(item.card_id_id)
                            cards_in_collection = Card.objects.filter(product_id__in=product_ids)

                            # Filtering by name (if name not specified, this will return all cards)
                            cards_in_collection = cards_in_collection.filter(name__contains=form.cleaned_data['card_name'])
                            # Filter by Card Type
                            if form.cleaned_data['card_type'] != 'NO_VALUE':
                                cards_in_collection = cards_in_collection.filter(
                                    type_id__card_type__contains=form.cleaned_data['card_type'])

                            # Filter by Card Rarity
                            if form.cleaned_data['card_rarity'] != 'NO_VALUE':
                                cards_in_collection = cards_in_collection.filter(
                                    rarity_id__card_rarity__iexact=form.cleaned_data['card_rarity'])

                            # Implement sorts
                            if form.cleaned_data['sort_by_choice'] == 'card_name':
                                sort_param = "name"
                            elif form.cleaned_data['sort_by_choice'] == 'card_rarity':
                                sort_param = "card_rarity"
                            elif form.cleaned_data['sort_by_choice'] == 'card_type':
                                sort_param = "type_id__card_type"
                            if form.cleaned_data['sorting_order'] == "descending":
                                sort_param = "-" + sort_param

                            # Sort the QuerySet per the parameter
                            cards_in_collection = cards_in_collection.order_by(sort_param)
                            for card in cards_in_collection:
                                own = collection_content.get(card_id_id=card.product_id).obtained
                                return_dicts.append({'card': card, 'own': own})
                        # display only 25 cards per page
                        paginator = Paginator(return_dicts, 24)
                        page = request.GET.get('page')
                        try:
                            page_obj = paginator.page(page)
                        except PageNotAnInteger:
                            # If page is not an integer, deliver first page.
                            page_obj = paginator.page(1)
                        except EmptyPage:
                            # If page is out of range (e.g. 9999), deliver last page of results.
                            page_obj = paginator.page(paginator.num_pages)
                        return render(request=request,
                                      template_name='main/collection_and_notification_portal.html',
                                      context={'data': page_obj, 'form': form})  # load necessary schemas
                    else:
                        for item in collection_content:
                            card = Card.objects.get(product_id=item.card_id_id)
                            own = item.obtained
                            cards_in_collection.append({'card': card, 'own': own})
                        # display only 25 cards per page
                        paginator = Paginator(cards_in_collection, 24)
                        page = request.GET.get('page')
                        return render(request=request,
                                      template_name='main/collection_and_notification_portal.html',
                                      context={'data': page_obj, 'form': form})  # load necessary schemas
                else:
                    for item in collection_content:
                        card = Card.objects.get(product_id=item.card_id_id)
                        own = item.obtained
                        cards_in_collection.append({'card': card, 'own': own})
                    # display only 25 cards per page
                    paginator = Paginator(cards_in_collection, 24)
                    page = request.GET.get('page')
                    try:
                        page_obj = paginator.page(page)
                    except PageNotAnInteger:
                        # If page is not an integer, deliver first page.
                        page_obj = paginator.page(1)
                    except EmptyPage:
                        # If page is out of range (e.g. 9999), deliver last page of results.
                        page_obj = paginator.page(paginator.num_pages)

                    form = CollectionSearchForm
                    return render(request=request,
                                  template_name='main/collection_and_notification_portal.html',
                                  context={'data': page_obj, 'form': form})  # load necessary schemas

            except Collection_Content.DoesNotExist:
                pass


# log user out of system
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out succesfully!")
    return redirect("main:home")

 
# card details page
def card_view(request, selected=None):
    # get primary key from url
    card_id = request.GET.get('selected', '')

    try: 
        # get card object from pk
        card = Card.objects.get(product_id=card_id)
        card_saved = False

        # get listing objects for this card
        listings = Listing.objects.filter(product_id=card_id)

        # if a user is logged in see if they have a collection
        if request.user.is_authenticated:
            users_collection = None
            collection_content = []
            try:
                users_collection = Collection.objects.get(owning_auth_user_id=request.user.id)
            except Collection.DoesNotExist:
                pass
            # if the user has a collection, get it
            if users_collection:
                try:
                    collection_content = Collection_Content.objects.filter(collection_id=users_collection.id)
                except Collection_Content.DoesNotExist:
                    pass
                # check to see if selected card is in collection
                for collected_card in collection_content:
                    if collected_card.card_id_id == card.product_id:
                        card_saved = True  # found card
                        break
        return render(request=request,
                      template_name="main/details.html",
                      context={"c": card, 'card_saved': card_saved, "l": listings}
                      )
    except Card.DoesNotExist:
        return render(request=request,
                      template_name="main/details.html",
                      )
    except ValueError:
        return render(request=request,
                      template_name="main/details.html",
                      )


def add_to_collection_view(request, selected=None):
    try:
        # get card object from pk
        card = Card.objects.get(product_id=request.GET.get('selected', ''))

        # if a user is logged in see if they have a collection
        if request.user.is_authenticated:
            users_collection = None
            try:
                users_collection = Collection.objects.get(owning_auth_user_id=request.user.id)
            except Collection.DoesNotExist:
                pass
            # if the user has a collection, and it isn't already in their collection (should never happen, but jic)
            # add this card to it
            if users_collection:
                card_there_already = None
                try:
                    card_there_already = Collection_Content.objects.get(card_id=card.product_id,
                                                                        collection_id=users_collection)
                except Collection_Content.DoesNotExist:
                    pass
                if not card_there_already:
                    Collection_Content(collection_id=users_collection, card_id=card, obtained=False).save()
            # if the user does not have a collection, make them one and add this card to it
            else:
                Collection(owning_auth_user_id=request.user.id,
                           collection_name="{0}'s Collection".format(request.user.username)).save()
                users_collection = Collection.objects.get(owning_auth_user_id=request.user.id)
                Collection_Content(collection_id=users_collection, card_id=card, obtained=False).save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Card.DoesNotExist:
        return redirect(to=card_view(request, selected=selected))
    except ValueError:
        return redirect(to=card_view(request, selected=selected))


def remove_from_collection_view(request, selected=None):
    try:
        # get card object from pk
        card = Card.objects.get(product_id=request.GET.get('selected', ''))

        # if a user is logged in see if they have a collection
        if request.user.is_authenticated:
            users_collection = None
            try:
                users_collection = Collection.objects.get(owning_auth_user_id=request.user.id)
            except Collection.DoesNotExist:
                pass
            # if the user has a collection, the card is in their collection, done
            if users_collection:
                card_in_collection = None
                try:
                    card_in_collection = Collection_Content.objects.get(card_id=card.product_id,
                                                                        collection_id=users_collection)
                except Collection_Content.DoesNotExist:
                    pass
                if card_in_collection:
                    card_in_collection.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Card.DoesNotExist:
        return redirect(to=card_view(request, selected=selected))
    except ValueError:
        return redirect(to=card_view(request, selected=selected))


def toggle_ownership_view(request, selected=None):
    try:
        # get card object from pk
        card = Card.objects.get(product_id=request.GET.get('selected', ''))

        # if a user is logged in see if they have a collection
        if request.user.is_authenticated:
            users_collection = None
            try:
                users_collection = Collection.objects.get(owning_auth_user_id=request.user.id)
            except Collection.DoesNotExist:
                pass
            # find the card in the collection and change the value
            if users_collection:
                card_of_interest = None
                try:
                    card_of_interest = Collection_Content.objects.get(card_id=card.product_id,
                                                                      collection_id=users_collection)
                except Collection_Content.DoesNotExist:
                    pass
                if card_of_interest:
                    desired_value = not card_of_interest.obtained
                    Collection_Content.objects.filter(card_id=card.product_id, collection_id=users_collection).\
                        update(obtained=desired_value)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Card.DoesNotExist:
        return redirect(to=card_view(request, selected=selected))
    except ValueError:
        return redirect(to=card_view(request, selected=selected))


def search(request):
    # upon submit
    if request.method == "POST":
        form = SearchForm(request.POST)
        # validate user input, create new user account, login user
        if form.is_valid():
            card_manager = Card.objects
            # Filtering by name (if name not specified, this will return all cards)
            cards = card_manager.filter(name__icontains = form.cleaned_data['card_name'])

            # filter by Card Type
            if form.cleaned_data['card_type'] != 'NO_VALUE':
                cards = cards.filter(type_id__card_type__contains=form.cleaned_data['card_type'])

            # Filter by Card Rarity
            if form.cleaned_data['card_rarity'] != 'NO_VALUE':
                cards = cards.filter(rarity_id__card_rarity__iexact=form.cleaned_data['card_rarity'])

            # Implement sorts
            if form.cleaned_data['sort_by_choice'] == 'card_name':
                sort_param = "name"
            elif form.cleaned_data['sort_by_choice'] == 'card_rarity':
                sort_param = "rarity_id__card_rarity"
            elif form.cleaned_data['sort_by_choice'] == 'card_type':
                sort_param = "type_id__card_type"

            if form.cleaned_data['sorting_order'] == "descending":
                sort_param = "-" + sort_param

            # Sort the QuerySet per thje parameter
            cards = cards.order_by(sort_param)

            return render(request=request,
                          template_name='main/home.html',
                          context={"data": cards, "form": form})
        else:
            # Restart the form submission process with bound data from previous request
            form = SearchForm(request.POST)
            return render(request = request,
                          template_name = "main/home.html",
                          context={"data": Card.objects.all(), "form": form})
    else:
        cards = Card.objects.all()
        # display only 25 cards per page
        paginator = Paginator(cards, 24)
        page = request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page_obj = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page_obj = paginator.page(paginator.num_pages)

        form = SearchForm
        return render(request=request,
                      template_name='main/home.html',
                      context={'data': page_obj, 'form': form})  # load necessary schemas


# user portal page - display profile
def profile(request):
    #only load page if user is authenticated
    try: 
        #get or initialize bazaar user object
        user, newacc = Bazaar_User.objects.get_or_create(auth_user_id_id=request.user.id, completed_sales=0)
    except:
        raise Http404("Page does not exist")
    if not user:
        user = newacc
    return render(request=request,
                  template_name='main/account/profile.html',
                  context={'user': user})


# user portal page - dislay preferences 
def preferences(request):
    try:
        userPref, newPref = User_Preferences.objects.get_or_create(user_id_id=request.user.id)
    except:
        raise Http404("Page does not exist")
    if not userPref:
        userPref = newPref
    return render(request=request,
                  template_name='main/account/preferences.html',
                  context={'pref': userPref})


# user portal page - dislay seller profile 
def sell(request):
    if not request.user.is_authenticated:
        raise Http404("Page does not exist")
    else:
        userSell, newSell = Seller.objects.get_or_create(seller_user_id=request.user.id, completed_sales=0, seller_key=request.user.username, seller_type="New")
        if not userSell:
            userSell = newSell
        return render(request=request,
                    template_name='main/account/vendor.html',
                    context={'seller': userSell })


#user portal page - edit profile
def edit(request):
    #only load page if user is authenticated 
    try: 
        bazUser = Bazaar_User.objects.get(auth_user_id_id=request.user.id)
    except Bazaar_User.DoesNotExist:
        raise Http404("Page does not exist")
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=bazUser.auth_user_id)
        bazForm = UpdateUserForm(request.POST, instance=bazUser.auth_user_id)
        if form.is_valid() and bazForm.is_valid():
            form.save()
            #save form data in user instance
            bazUser.location = bazForm.cleaned_data['location']
            bazUser.save()
            #return to user profile page displaying updated data
            return redirect("main:profile")
    else:
        #instantiate model data in built in and custom user forms
        form = EditUserForm(instance=bazUser.auth_user_id)
        bazForm = UpdateUserForm(instance=bazUser)
    return render(request=request,
                  template_name='main/account/edit.html',
                  context={'form': form, 'bazForm': bazForm})


# user portal page - edit preferences 
def editpref(request):
    try:
        userPref = User_Preferences.objects.get(user_id_id=request.user.id)
    except User_Preferences.DoesNotExist:
        raise Http404("Page does not exist")
    if request.method == 'POST':
        form = UpdatePreferencesForm(request.POST)
        if form.is_valid():
            #update user preference object instance with form data
            userPref.email_notif = form.cleaned_data['email_notif']
            userPref.subscribe_email = form.cleaned_data['subscribe_email']
            userPref.view_email = form.cleaned_data['view_email']
            userPref.save()
            return redirect("main:preferences")
    else:
        #instantiate form with current user preferences from model
        form = UpdatePreferencesForm(initial={'email_notif': userPref.email_notif, 'subscribe_email': userPref.subscribe_email, 'view_email': userPref.view_email })
    return render(request=request,
                template_name='main/account/editpref.html',
                context={'form': form}) 


# user portal page - edit seller details
def editsell(request):
    if not request.user.is_authenticated:
        raise Http404("Page does not exist")
    else:
        userSell = Seller.objects.get(seller_user_id=request.user.id)
        if request.method == 'POST':
            form = UpdateSellerForm(request.POST, instance = userSell)
            if form.is_valid():
                userSell.seller_name = form.cleaned_data['seller_name']
                userSell.save()
                return redirect("main:sell")
        else:
            form = UpdateSellerForm(instance = userSell)
        return render(request=request,
                    template_name='main/account/editvend.html',
                    context={'form': form}) 


# user portal page - form to change password when known
def changepass(request):
    #only load page if user is authenticated
    if not request.user.is_authenticated:
        raise Http404("Page does not exist")
    else:
        if request.method == 'POST':
            #built-in change pass form with user instance
            form = PasswordChangeForm(data=request.POST, user=request.user)
            if form.is_valid():
                form.save()
                #authenticate user
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('main:profile')
            else:
                messages.error(request, 'Incorrect password entered.')
                return redirect('main:changepass')
        else:
            form = PasswordChangeForm(request.user)
        return render(request=request,
                    template_name='main/account/editpass.html',
                    context={'form': form}) 
                    

#add notif flag to db
def add_notif(request, l=None):
    #get listing object from url
    listing = Listing.objects.get(pk = l)
    #get card object from listing
    card = Card.objects.get(product_id = listing.product_id.product_id)
    #create and save notification object for desired user/card/price
    try:
        notif = Notification(auth_user_id=request.user, card_id=card, price_threshold=listing.price)
        notif.save()
    except IntegrityError:
        notif = Notification.objects.get(auth_user_id=request.user, card_id=card, price_threshold=listing.price)
    return render(request=request,
                  template_name='main/notifications.html',
                  context={'item': notif})
