from django.urls import path

from stripe_app.views import index, get_items, get_item, buy, create_order, discount_buy

urlpatterns = [path("", index, name="main_stripe"),
               path("get_items", get_items, name="get_items"),
               path("item/<int:id>", get_item, name="get_item"),
               path("buy/<int:id>", buy, name="buy"),
               path("create_order", create_order, name="create_order"),
               path("discount_buy/<int:id>/<str:discount_id>", discount_buy, name="discount_buy")
               ]
