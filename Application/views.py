from django.shortcuts import render
from django.shortcuts import redirect
from django.middleware import csrf
from Application.forms import *
from django.template import loader
import json
import datetime
import requests

def search(request):
    form = SearchForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data = ticketSearch(request)
            cards = None
            if data is not None:
                if data['page']['totalElements'] != 0:
                    cards = populateCards(data['_embedded'],request)
            context = { 'form': form,
                        'cards': cards }
            return render(request,'index.html',context)
    return redirect('index')

def index(request):
    form = SearchForm(request.POST or None)
    context = { 'form': form,
                'cards': None }
    return render(request,'index.html',context)

def ticketSearch(request):
    try:
        body = request.POST
        url = "https://app.ticketmaster.com/discovery/v2/events.json"
        apikey = "O6aGpfnEnszpUGrGxhpRgUXEPFlTGXBG"
        genre = body['genre']
        city = body['city']
        params = {
            "apikey" : apikey,
            "classificationName" : genre,
            "city" : city,
            "sort" : "date,asc"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data_unicode = response.content.decode("utf-8")
        data_decoded = json.loads(data_unicode)
        return data_decoded

    except requests.exceptions.RequestException as e:
        print(f"Request Failed: {e}")
        return None


def populateCards(events,request):
    cards = []
    for event in events['events']:
        template = loader.get_template('card.html')
        venue = event['_embedded']['venues'][0]
        if 'pricerange' in event:
            if event['pricerange'] is not None:
                priceMin = event['priceRanges']['priceMin']
                priceMax = event['priceRanges']['priceMax']
            else:
                priceMin = 0
                priceMax = 0
        else:
            priceMin = 0
            priceMax = 0
        if event['dates']['start'].get('dateTime') is not None:
            date = datetime.datetime.strptime(event['dates']['start']['dateTime'], "%Y-%m-%dT%H:%M:%SZ")
            eventDate = date.date()
            eventTime = date.time()
        else:
            eventDate = "Date TBA"
            eventTime = "Time TBA"

        imgUrl = getfirst4by3image(event['images'])

        context = {
            'csrfToken' : csrf.get_token(request),
            'event_bundle' : {
                'id' : event['id'],
                'title' : event['name'],
                'venue' : event['_embedded']['venues'][0]['name'],
                'address': venue['address']['line1'],
                'cityState': venue['city']['name'] + ", " + venue['state']['stateCode'],
                'date':eventDate,
                'time':eventTime,
                'priceMin': priceMin,
                'priceMax': priceMax,
                'url' : event['url'],
                'imgUrl': imgUrl
            }
        }
        cards.append(template.render(context))
    return cards

def getfirst4by3image(images):
    for image in images:
        if image.get('ratio') is not None:
            if image['ratio'] == '4_3':
                return image['url']
    return None

def saveTicket(request):
    form = TicketForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('my_tickets')
    else:
        print(form.errors)
    return render(request,'index.html')

def myTickets(request):
    tickets = Ticket.objects.all()
    priceRangeMin = 0;
    priceRangeMax = 0;
    numTickets = 0;
    for ticket in tickets:
        priceRangeMin += ticket.priceMin
        priceRangeMax += ticket.priceMax
        numTickets += 1
    context = { 'tickets' : tickets, 'priceRangeMin' : priceRangeMin , 'priceRangeMax' : priceRangeMax, 'numTickets' : numTickets, 'csrfToken' : csrf.get_token(request) }
    return render(request,'userTickets.html',context)

def updateTicket(request):
    return None

def ticket(request):
    return None

def deleteTicket(request,id):
    if request.method == 'POST':
        eraseTicket = Ticket.objects.get(id=id)
        eraseTicket.delete()
        return redirect(myTickets)
    return render(request,'index.html')