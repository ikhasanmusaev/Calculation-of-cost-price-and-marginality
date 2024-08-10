from django.urls import path
from calculation.views import ProductCostCalculationView

urlpatterns = [
    path('calculate-cost/', ProductCostCalculationView.as_view(), name='calculate-cost'),
]
