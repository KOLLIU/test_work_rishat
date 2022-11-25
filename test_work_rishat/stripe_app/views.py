from django.http import HttpResponse
from django.shortcuts import render, redirect

import os
from environ import environ

from stripe_app.forms import OrderForm
from stripe_app.models import Item, Discount

import stripe

from test_work_rishat.settings import BASE_DIR

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

stripe.api_key = env("stripe_secret_key")


def create_session(name, unit_amount, description="", quantity=1, currency="rub", success_url="http://localhost:8000",
                   cancel_url="http://localhost:8000", discounts=None):
    data = {
        "line_items": [
            {
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': name,
                        'description': description
                    },
                    'unit_amount': unit_amount * 100,
                },
                'quantity': quantity,
            }
        ],
        "mode": 'payment',
        "success_url": success_url,
        "cancel_url": cancel_url,
    }
    if discounts is not None:
        data["discounts"] = discounts

    session = stripe.checkout.Session.create(**data)
    return session


def index(request):
    return redirect("get_items")


def create_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            items = order.get_items()
            order_name = "|".join([item.name for item in items])
            order_description = "|".join([item.description for item in items])
            order_amount = sum([item.price for item in items])
            session = create_session(name=order_name, description=order_description, unit_amount=order_amount)
            return redirect(session.url)
        else:
            return redirect("create_order")
    else:
        form = OrderForm()
        context = {"form": form}
        return render(request, "stripe_app/order.html", context=context)


def get_items(request):
    items = Item.objects.all()
    context = {"items": items}

    return render(request, "stripe_app/items.html", context=context)


def get_item(request, id):
    item = Item.objects.get(id=id)
    discounts = Discount.objects.all()

    context = {"item": item, "discounts": discounts}

    return render(request, "stripe_app/item.html", context=context)


def buy(request, id):
    item = Item.objects.get(id=id)

    session = create_session(name=item.name, description=item.description, unit_amount=item.price)

    return HttpResponse(session["id"], content_type="text/plain")


def discount_buy(request, id, discount_id):
    item = Item.objects.get(id=id)

    discounts = Discount.objects.get(id=discount_id).return_discounts()

    session = create_session(name=item.name, description=item.description, unit_amount=item.price, discounts=discounts)

    return HttpResponse(session["id"], content_type="text/plain")
