from django.urls import path
from .views import BeneficiarySearchView

urlpatterns = [
    path('beneficiaries/', BeneficiarySearchView.as_view(), name='beneficiary-search'),
]
