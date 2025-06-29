from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import (
    submit_model_form,
    SystemImplementationAPIView,
    laporan_integrasi_view,
    #aktivitas_detail_view,
    login_view, sistem_view, dashboard_view,
    activity_view, transaksi_model_view, signup_view,
    logactivity_view, daftar_catatan, lingkungan_view,
    hapus_aktivitas_detail, #transaksi_detail_view,
    terima_model_api,validasi_model,daftar_model_tervalidasi,ringkasan_hasil_uji,riwayat_uji_view,tambah_lingkungan
)

urlpatterns = [
    # Auth
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # opsional

    # Halaman utama
    path('sistem/', sistem_view, name='sistem'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('activity/', activity_view, name='activity'),
    
    path('transaksi-model/', views.transaksi_model_view, name='transaksi_model'),
    path('logactivity/', logactivity_view, name='log'),
    path('lingkungan/', views.lingkungan_view, name='lingkungan'),
    path('Catatan/', views.catatan_pemeliharaan_view, name='catatan'),#APUS AJA
    path('catatan/', views.catatan_view, name='catatan'),
    path('catatan/tambah/', views.tambah_catatan, name='tambah_catatan'),
    path('catatan/hapus/<int:id>/', views.hapus_catatan, name='hapus_catatan'),




    # Detail
    path('activity/', activity_view, name='activity'),
   
    path('activity/delete/<int:pk>/', hapus_aktivitas_detail, name='hapus_aktivitas_detail'),
    
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
    path('validasi/<int:id>/', validasi_model, name='validasi_model'),
    path('ujiimplementasi/', daftar_model_tervalidasi, name='daftar_model_tervalidasi'),
   
   
    path('riwayat-uji/', riwayat_uji_view, name='riwayat_uji'),
    path('ringkasan-uji/', views.ringkasan_hasil_uji, name='ringkasan_uji'),
    path('tambah-aktivitas/', views.tambah_aktivitas, name='tambah_aktivitas'),
    path('hapus-aktivitas/<int:id>/', views.hapus_aktivitas, name='hapus_aktivitas'),
    path('log/hapus/<int:id>/', views.hapus_model, name='hapus_model'),
   # myapp/urls.py
   path('kirimmanagement/', views.kirim_managements_ke_teman, name='kirim_managements_ke_teman'),
   path('', views.landing_view, name='landing'),
   path('tambah-model/', views.tambah_model_baru, name='submit_model_form'),
   path('transaksi-model/', views.transaksi_model_view, name='transaksi_model'),
   path('lingkungan/', views.lingkungan_view, name='lingkungan'),
   path('lingkungan/tambah/', tambah_lingkungan, name='tambah_lingkungan'),

   
   




    


]
