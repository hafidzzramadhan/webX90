from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    submit_model_form,
    SystemImplementationAPIView,
    laporan_integrasi_view,
    aktivitas_detail_view,
    login_view, sistem_view, dashboard_view,
    activity_view, transaksi_view, signup_view,
    logactivity_view, catatan_view, lingkungan_view,
    hapus_aktivitas_detail, transaksi_detail_view,
    terima_model_api
)

urlpatterns = [
    # Auth
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # opsional

    # Halaman utama
    path('sistem/', sistem_view, name='sistem'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('activity/', activity_view, name='activity'),
    path('catatan/', catatan_view, name='catatan'),
    path('transaksi/', transaksi_view, name='transaksi'),
    path('logactivity/', logactivity_view, name='log'),
    path('lingkungan/', lingkungan_view, name='lingkungan'),

    # Detail
    path('activity/<int:pk>/', aktivitas_detail_view, name='activity_detail'),
    path('activity/delete/<int:pk>/', hapus_aktivitas_detail, name='hapus_aktivitas_detail'),
    path('transaksi/<int:pk>/', transaksi_detail_view, name='transaksi_detail'),

    # Form & Laporan
    path('form/submit/', submit_model_form, name='submit_model_form'),
    path('laporan-integrasi/', laporan_integrasi_view, name='laporan_integrasi'),

    # API
    path('api/system-implementation/', SystemImplementationAPIView.as_view(), name='system_implementation_api'),
    path('api/terima-model/', terima_model_api, name='terima_model_api'),

    # Reset Password
    path('reset-password/', auth_views.PasswordResetView.as_view(
        template_name='myapp/custom_password_reset.html'), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='myapp/custom_password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='myapp/custom_password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='myapp/custom_password_reset_complete.html'), name='password_reset_complete'),
]
