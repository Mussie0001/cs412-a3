from django.shortcuts import render, redirect
import random
from datetime import datetime, timedelta

def main(request):
    return render(request, 'restaurant/main.html')

def order(request):
    sauces = [
        'Salsa Verde',
        'Pico de Gallo',
        'Chipotle Sauce',
        'Mango Habanero',
        'Garlic Aioli',
        'Avocado Crema',
        'Sour Cream',
        'Queso',
    ]
    daily_special_sauces = random.sample(sauces, 4)
    context = {'daily_special_sauces': daily_special_sauces}
    return render(request, 'restaurant/order.html', context)

def confirmation(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        special_instructions = request.POST.get('special_instructions')

        selected_items = request.POST.getlist('items')
        selected_extras = request.POST.getlist('extras')

        menu_items = {
            'taco': {'name': 'Taco', 'price': 3.00},
            'burrito': {'name': 'Burrito', 'price': 7.00},
            'quesadilla': {'name': 'Quesadilla', 'price': 5.00},
            'daily_special': {
                'name': 'Daily Special - Taco with 4 Special Sauces',
                'price': 8.00,
                'sauces': request.POST.get('daily_special_sauces'),
            },
        }

        ordered_items = []
        total_price = 0.0

        for item_key in selected_items:
            if item_key in menu_items:
                item = menu_items[item_key]
                item_copy = item.copy()  
                item_copy['extras'] = selected_extras  
                ordered_items.append(item_copy)
                total_price += item['price']

        num_items_ordered = len(ordered_items)
        if 'Guacamole' in selected_extras:
            total_price += 1.50 * num_items_ordered  

        ready_in_minutes = random.randint(15, 20)
        ready_time = datetime.now() + timedelta(minutes=ready_in_minutes)
        ready_time_formatted = ready_time.strftime('%I:%M %p')

        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'special_instructions': special_instructions,
            'ordered_items': ordered_items,
            'extras': selected_extras,
            'total_price': "{:.2f}".format(total_price),
            'ready_time': ready_time_formatted,
        }

        return render(request, 'restaurant/confirmation.html', context)
    else:
        return redirect('order')






