from django.contrib import admin
from.models import *


admin.site.register([
    DeliveryBoy,
    OrderItem,
    Order,
    Address,
    Product,
    CartItem,

])