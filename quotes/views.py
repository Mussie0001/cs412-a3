from django.shortcuts import render
import random

# Create your views here.
quotes = [
    "The future belongs to those who prepare for it today.",
    "Education is the passport to the future, for tomorrow belongs to those who prepare for it today.",
    "A man who stands for nothing will fall for anything.",
    "You can't separate peace from freedom because no one can be at peace unless he has his freedom."
]

images = [
    '/static/images/malcolm1.jpg',
    '/static/images/malcolm2.jpg',
    '/static/images/malcolm3.jpg',
    '/static/images/malcolm4.jpg',
]

def quote_view(request):
    quote = random.choice(quotes)
    image = random.choice(images)
    context = {
        'quote': quote,
        'image': image,
    }
    return render(request, 'quotes/quote.html', context)

def show_all(request):
    combined = zip(quotes, images)
    context = {
        'combined': combined,
    }
    return render(request, 'quotes/show_all.html', context)


def about(request):
    return render(request, 'quotes/about.html')
