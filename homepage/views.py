from django.shortcuts import render, render_to_response

def index(request):
    return render_to_response('homepage/index.html')

def portfolio(request):
    return render_to_response('homepage/portfolio.html')

def contact(request):
    return render_to_response('homepage/contact.html')

