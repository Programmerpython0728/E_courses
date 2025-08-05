from django.urls import path
from .views import CreateChargeView

urlpatterns = [
    path('charge/', CreateChargeView.as_view(), name='create-charge'),
]
