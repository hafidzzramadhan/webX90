from django.urls import path
from .views import (
    login_view, sistem_view, dashboard_view,
    activity_view, transaksi_view, signup_view,
    logactivity_view, catatan_view, lingkungan_view
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),  # ✅ ubah path signup agar tidak nested di /login/signup
    path('sistem/', sistem_view, name='sistem'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('activity/', activity_view, name='activity'),
    path('catatan/', catatan_view, name='catatan'),
    path('transaksi/', transaksi_view, name='transaksi'),
    path('logactivity/', logactivity_view, name='log'),
    path('lingkungan/', lingkungan_view, name='lingkungan'),
]
