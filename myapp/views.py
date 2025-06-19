from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import Aktivitas, Catatan, Transaksi, LogAktivitas, Lingkungan
from .serializers import (
    AktivitasSerializer, CatatanSerializer, TransaksiSerializer,
    LogAktivitasSerializer, LingkunganSerializer
)

# LOGIN VIEW (dummy login)
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # langsung redirect ke dashboard tanpa autentikasi
        return redirect('dashboard')
    return render(request, 'myapp/login.html')

# SISTEM VIEW (opsional)
def sistem_view(request):
    return render(request, 'myapp/sistem.html')

# DASHBOARD VIEW
def dashboard_view(request):
    return render(request, 'myapp/dashboard.html')

def activity_view(request):
    aktivitas = Aktivitas.objects.all()
    return render(request, 'myapp/activity.html', {"aktivitas": aktivitas})

def catatan_view(request):
    catatan_list = Catatan.objects.all()
    return render(request, 'myapp/catatan.html', {'catatan_list': catatan_list})

def transaksi_view(request):
    transaksi_list = Transaksi.objects.all()
    return render(request, 'myapp/transaksi.html', {'transaksi_list': transaksi_list})

def signup_view(request):
    return render(request, 'myapp/signup.html')

def logactivity_view(request):
    log_list = LogAktivitas.objects.all()
    return render(request, 'myapp/logactivity.html', {'log_list': log_list})

def lingkungan_view(request):
    lingkungan_list = Lingkungan.objects.all()
    return render(request, 'myapp/lingkungan.html', {'lingkungan_list': lingkungan_list})

# API ViewSets
class AktivitasViewSet(viewsets.ModelViewSet):
    queryset = Aktivitas.objects.all()
    serializer_class = AktivitasSerializer

class CatatanViewSet(viewsets.ModelViewSet):
    queryset = Catatan.objects.all()
    serializer_class = CatatanSerializer

class TransaksiViewSet(viewsets.ModelViewSet):
    queryset = Transaksi.objects.all()
    serializer_class = TransaksiSerializer

class LogAktivitasViewSet(viewsets.ModelViewSet):
    queryset = LogAktivitas.objects.all()
    serializer_class = LogAktivitasSerializer

class LingkunganViewSet(viewsets.ModelViewSet):
    queryset = Lingkungan.objects.all()
    serializer_class = LingkunganSerializer
