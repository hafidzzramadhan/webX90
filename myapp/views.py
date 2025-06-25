from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import requests, json, traceback
from datetime import date

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import (
    Aktivitas, Catatan, Transaksi, LogAktivitas, Lingkungan, SystemImplementation
)
from .models import ValidasiModel
from .forms import ValidasiModelForm
from .forms import SignUpForm
from .serializers import (
    AktivitasSerializer, CatatanSerializer, TransaksiSerializer,
    LogAktivitasSerializer, LingkunganSerializer, SystemImplementationSerializer
)

# Auth Views

def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=identifier).first() or User.objects.filter(email=identifier).first()
        if user:
            auth_user = authenticate(request, username=user.username, password=password)
            if auth_user:
                login(request, auth_user)
                return redirect('dashboard')
        return render(request, 'myapp/login.html', {'error': 'Login gagal. Cek kembali username/email dan password.'})
    return render(request, 'myapp/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            return render(request, 'myapp/signup.html', {'error': 'Password tidak cocok'})
        if User.objects.filter(username=username).exists():
            return render(request, 'myapp/signup.html', {'error': 'Username sudah digunakan'})
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('dashboard')
    return render(request, 'myapp/signup.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# Static Views

def dashboard_view(request):
    return render(request, 'myapp/dashboard.html')

def sistem_view(request):
    return render(request, 'myapp/sistem.html')

def activity_view(request):
    aktivitas = Aktivitas.objects.all()
    return render(request, 'myapp/activity.html', {"aktivitas": aktivitas})

def catatan_view(request):
    catatan_list = Catatan.objects.all()
    return render(request, 'myapp/catatan.html', {'catatan_list': catatan_list})

def transaksi_view(request):
    transaksi_list = Transaksi.objects.all()
    return render(request, 'myapp/transaksi.html', {'transaksi_list': transaksi_list})

def lingkungan_view(request):
    lingkungan_list = Lingkungan.objects.all()
    return render(request, 'myapp/lingkungan.html', {'lingkungan_list': lingkungan_list})

def logactivity_view(request):

    data = SystemImplementation.objects.all().order_by('-timestamp')

    return render(request, 'myapp/logactivity.html', {'data_list': data})

@csrf_exempt
def submit_model_form(request):
    if request.method == 'POST':
        no = request.POST.get('no')
        nama_model = request.POST.get('nama_model')
        status = request.POST.get('status_project')
        dokumentasi = request.POST.get('dokumentasi')
        laporan_file = request.FILES.get('laporan')

        laporan_url = None
        if laporan_file:
            from django.core.files.storage import FileSystemStorage
            fs = FileSystemStorage()
            filename = fs.save(laporan_file.name, laporan_file)
            laporan_url = fs.url(filename)

        LogAktivitas.objects.create(
            tanggal=date.today(),
            aktivitas=f"[No. {no}] Model diterima: {nama_model}",
            status=status,
            no=no,
            dokumentasi=dokumentasi,
            laporan=laporan_url or "Tidak ada"
        )
        return redirect('log')
    return render(request, 'myapp/logactivity.html')

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def terima_model_api(request):
    try:
        file_laporan = request.FILES.get('laporan_model')
        data = request.data

        payload = {
            "no": data.get("no"),
            "nama_model": data.get("nama_model"),
            "status_project": data.get("status_project"),
            "dokumentasi_model": data.get("dokumentasi_model"),
            "laporan_model": file_laporan,
        }

        serializer = SystemImplementationSerializer(data=payload)
        if serializer.is_valid():
            saved_instance = serializer.save()
            return Response({
                "success": True,
                "message": "Model berhasil diterima.",
                "data": SystemImplementationSerializer(saved_instance).data
            }, status=status.HTTP_201_CREATED)

        # ⬇️ Tambahkan ini
        print("SERIALIZER ERRORS:", serializer.errors)

        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({"success": False, "message": f"Terjadi kesalahan: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def laporan_integrasi_view(request):
    data = SystemImplementation.objects.all().order_by('-timestamp')
    return render(request, 'myapp/logactivity.html', {'data_list': data})

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


class SystemImplementationAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        data = SystemImplementation.objects.all().order_by('-timestamp')
        serializer = SystemImplementationSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        file_laporan = request.FILES.get('laporan_model')
        data = request.data

        payload = {
            "no": data.get("no"),
            "nama_model": data.get("nama_model"),
            "status_project": data.get("status_project"),
            "dokumentasi_model": data.get("dokumentasi_model"),
            "laporan_model": file_laporan,
        }

        serializer = SystemImplementationSerializer(data=payload)
        if serializer.is_valid():
            saved = serializer.save()
            return Response({
                "success": True,
                "message": "Model berhasil disimpan via APIView.",
                "data": SystemImplementationSerializer(saved).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

def aktivitas_detail_view(request, pk):
    aktivitas = get_object_or_404(Aktivitas, pk=pk)
    return render(request, 'myapp/aktivitas_detail.html', {'aktivitas': aktivitas})

from django.contrib import messages

def hapus_aktivitas_detail(request, pk):
    aktivitas = get_object_or_404(Aktivitas, pk=pk)
    aktivitas.delete()
    messages.success(request, "Aktivitas berhasil dihapus.")
    return redirect('activity')  # Pastikan nama ini sama dengan URL `activity/`

def transaksi_detail_view(request, pk):
    transaksi = get_object_or_404(Transaksi, pk=pk)
    return render(request, 'myapp/transaksi_detail.html', {'transaksi': transaksi})



def validasi_model(request, id):
    model_instance = SystemImplementation.objects.get(id=id)
    
    if request.method == 'POST':
        form = ValidasiModelForm(request.POST)
        if form.is_valid():
            validasi = form.save(commit=False)
            validasi.model_terkait = model_instance
            validasi.save()
            return redirect('log')
    else:
        form = ValidasiModelForm()

    return render(request, 'validasi_model.html', {'form': form})


def daftar_model_tervalidasi(request):
    data_list = ValidasiModel.objects.filter(status_validasi="Valid").order_by('-tanggal_validasi')
    return render(request, 'ujiimplementasi/daftar_validasi.html', {'data_list': data_list})
