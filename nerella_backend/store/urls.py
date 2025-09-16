from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, InvoiceViewSet, RegisterView, UserView, ProductByBarcodeView

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('invoices', InvoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserView.as_view(), name='profile'),
    path('product/barcode/<str:barcode>/', ProductByBarcodeView.as_view(), name='product-barcode'),
]
