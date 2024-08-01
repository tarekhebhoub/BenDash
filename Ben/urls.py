# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, ProductViewSet, InvoiceViewSet, PaymentViewSet,logout,GetVentes,GetVenteDetails,Create_invoice_with_products
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'products', ProductViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('tryToken/',views.tryToken),
    path('logout/', logout, name='logout'),
    path('getVentes/',GetVentes,name='getVentes'),
    path('getVenteDetails/<int:pk>/',GetVenteDetails,name='getVenteDetails'),
    path('createInvoice/',Create_invoice_with_products,name='createInvoice')

]
