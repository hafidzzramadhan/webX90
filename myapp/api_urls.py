from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AktivitasViewSet, CatatanViewSet, TransaksiViewSet,
    LogAktivitasViewSet, LingkunganViewSet
)

router = DefaultRouter()
router.register(r'aktivitas', AktivitasViewSet)
router.register(r'catatan', CatatanViewSet)
router.register(r'transaksi', TransaksiViewSet)
router.register(r'log', LogAktivitasViewSet)
router.register(r'lingkungan', LingkunganViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
