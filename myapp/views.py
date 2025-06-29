from datetime import date
from django.utils import timezone


# Django core
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

# Django REST Framework
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response 

# Python native
import requests

# App imports
from .models import (
    Aktivitas, Transaksi, LogAktivitas, Lingkungan,
    SystemImplementation, ValidasiModel, HasilUjiModel, Catatan,ManagementsSI
)
from .forms import ValidasiModelForm, SignUpForm
from .serializers import (
    AktivitasSerializer, CatatanSerializer, TransaksiSerializer,
    LogAktivitasSerializer, LingkunganSerializer, SystemImplementationSerializer
)


@csrf_exempt
def catatan_pemeliharaan_view(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')
        teknisi = request.POST.get('teknisi')

        Catatan.objects.create(
            judul=judul,
            deskripsi=deskripsi,
            teknisi=teknisi
        )
        return redirect('catatan')

    daftar_catatan = Catatan.objects.all().order_by('-tanggal')
    return render(request, 'myapp/catatan.html', {'daftar_catatan': daftar_catatan})
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


def ringkasan_hasil_uji(request):
    from .models import HasilUjiModel
    hasil_list = HasilUjiModel.objects.all().order_by('-tanggal_uji')
    return render(request, 'myapp/ringkasan_uji.html', {'hasil_list': hasil_list})



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

def landing_view(request):
    return render(request, 'myapp/landing.html')


# Static Views
def dashboard_view(request):
    total_model = SystemImplementation.objects.count()
    tervalidasi = SystemImplementation.objects.filter(status_project='Tervalidasi').count()
    belum_diuji = SystemImplementation.objects.filter(status_project='Belum Diuji').count()
    terkirim = SystemImplementation.objects.filter(status_project='Terkirim').count()

    aktivitas_hari_ini = LogAktivitas.objects.filter(tanggal=now().date()).count()
    terakhir_log = LogAktivitas.objects.order_by('-tanggal').first()

    if total_model > 0:
        progress = int((tervalidasi / total_model) * 100)
    else:
        progress = 0

    return render(request, 'myapp/dashboard.html', {
        'progress': progress,
        'aktivitas_hari_ini': aktivitas_hari_ini,
        'terakhir_pemeliharaan': terakhir_log.tanggal if terakhir_log else None,
        'tervalidasi': tervalidasi,
        'belum_diuji': belum_diuji,
        'terkirim': terkirim
    })


def tambah_model_baru(request):
    if request.method == 'POST':
        nama_model = request.POST.get('nama_model')
        
        dokumentasi = request.POST.get('dokumentasi_model')  # <== INI BELUM ADA!

        laporan = request.FILES.get('laporan_model')

        nomor_terakhir = SystemImplementation.objects.count() + 1

        model_baru = SystemImplementation.objects.create(
            no=nomor_terakhir,
            nama_model=nama_model,
            dokumentasi_model=dokumentasi,
            laporan_model=laporan,
            status_project="Belum Diuji"
        )

        # ✅ Log aktivitas penambahan model manual
        LogAktivitas.objects.create(
            aktivitas=f"Model '{nama_model}' ditambahkan secara manual oleh SI.",
            tanggal=now(),
            status='Hijau' 
        )

        Aktivitas.objects.create(
    tanggal=date.today(),
    nama_aktivitas=f"Model '{nama_model}' ditambahkan secara manual oleh SI",
    status="Hijau"
)


        return redirect('log')

    return render(request, 'myapp/tambah_model_form.html')


#def dashboard_view(request):LAMAAA
    total_model = SystemImplementation.objects.count()
    total_validasi = ValidasiModel.objects.count()
    aktivitas_terakhir = LogAktivitas.objects.order_by('-tanggal')[:5]
    return render(request, 'myapp/dashboard.html', {
        'total_model': total_model,
        'total_validasi': total_validasi,
        'aktivitas_terakhir': aktivitas_terakhir
    })


def sistem_view(request):
    return render(request, 'myapp/sistem.html')

#aktivitas
def activity_view(request):
    aktivitas = Aktivitas.objects.all().order_by('-tanggal')
    return render(request, 'myapp/activity.html', {'aktivitas': aktivitas})

def tambah_aktivitas(request):
    if request.method == 'POST':
        tanggal = request.POST.get('tanggal') or str(date.today())
        nama_aktivitas = request.POST.get('nama_aktivitas')
        status = request.POST.get('status')
        
        Aktivitas.objects.create(
            tanggal=tanggal,
            nama_aktivitas=nama_aktivitas,
            status=status
        )
    return redirect('activity')

# Hapus aktivitas (per baris)

def hapus_aktivitas(request, id):
    aktivitas = get_object_or_404(Aktivitas, id=id)
    aktivitas.delete()
    return redirect('activity')

def daftar_catatan(request):
    catatan = Catatan.objects.all()
    return render(request, 'myapp/catatan.html', {'catatan': catatan})


#transksi 
from .models import TransaksiModel
def transaksi_model_view(request):
    transaksi_list = TransaksiModel.objects.all().order_by('-waktu_transaksi')
    return render(request, 'myapp/transaksi_model.html', {'transaksi_list': transaksi_list})


def lingkungan_view(request):
    lingkungan = Lingkungan.objects.all()
    return render(request, 'myapp/lingkungan.html', {'lingkungan': lingkungan})

def logactivity_view(request):

    data = SystemImplementation.objects.all().order_by('-timestamp')

    return render(request, 'myapp/logactivity.html', {'data_list': data})

@csrf_exempt  #PALSUU
def submit_model_form(request):
    if request.method == 'POST':
        no = request.POST.get('no')
        nama_model = request.POST.get('nama_model')
        status_project = request.POST.get('status_project')
        dokumentasi = request.POST.get('dokumentasi')
        laporan_file = request.FILES.get('laporan')

        # Simpan laporan jika ada
        laporan_url = None
        if laporan_file:
            from django.core.files.storage import FileSystemStorage
            fs = FileSystemStorage()
            filename = fs.save(laporan_file.name, laporan_file)
            laporan_url = fs.url(filename)

        # Simpan ke model SystemImplementation
        model_baru = SystemImplementation.objects.create(
            no=no,
            nama_model=nama_model,
            status_project=status_project,
            dokumentasi_model=dokumentasi,
            laporan_model=laporan_file  # akan otomatis tersimpan
        )

        # Simpan ke LogAktivitas
        LogAktivitas.objects.create(
            tanggal=date.today(),
            aktivitas=f"[No. {no}] Model diterima: {nama_model}",
            status=status_project,
            no=no,
            dokumentasi=dokumentasi,
            laporan=laporan_url or "Tidak ada"
        )

        # Tambah ke tabel Aktivitas (status Oranye)
        Aktivitas.objects.create(
            tanggal=date.today(),
            nama_aktivitas=f"Model '{nama_model}' berhasil disubmit oleh user",
            status="Oranye"
        )

        LogAktivitas.objects.create(
            aktivitas=f"Model '{nama_model}' ditambahkan secara manual oleh SI.",
            tanggal=now(),
            status='Hijau' 
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

            # ✅ Catat ke LogAktivitas (log internal)
            from django.utils.timezone import now
            from myapp.models import LogAktivitas, Aktivitas

            LogAktivitas.objects.create(
                aktivitas=f"Model '{saved_instance.nama_model}' diterima dari modul IC.",
                tanggal=now()
            )

            # ✅ Catat ke Aktivitas (halaman daftar aktivitas)
            from datetime import date
            Aktivitas.objects.create(
                tanggal=date.today(),
                nama_aktivitas=f"Model '{saved_instance.nama_model}' diterima dari Modul IC",
                status="Hijau"
            )



            return Response({
                "success": True,
                "message": "Model berhasil diterima.",
                "data": SystemImplementationSerializer(saved_instance).data
            }, status=status.HTTP_201_CREATED)

        print("SERIALIZER ERRORS:", serializer.errors)

        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({"success": False, "message": f"Terjadi kesalahan: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def laporan_integrasi_view(request):
    data = SystemImplementation.objects.all().order_by('-timestamp')
    return render(request, 'myapp/logactivity.html', {'data_list': data})



#def uji_model(request, id):
    validasi = get_object_or_404(ValidasiModel, id=id)

    if request.method == 'POST':
        hasil = request.POST.get('hasil_perhitungan')
        rekomendasi = request.POST.get('rekomendasi')
        kirim = 'kirim_ke_pm' in request.POST

        HasilUjiModel.objects.create(
            model_terkait=validasi,
            hasil_perhitungan=hasil,
            rekomendasi=rekomendasi,
            kirim_ke_pm=kirim
        )

        if kirim:
            # Simulasi kirim ke modul Project Management
            print(f"[INFO] Hasil uji model '{validasi.model_terkait.nama_model}' dikirim ke modul Project Management.")

        return redirect('daftar_model_tervalidasi')

    return render(request, 'myapp/form_uji_model.html', {'validasi': validasi})

def daftar_hasil_uji(request):
    hasil_list = HasilUjiModel.objects.all().order_by('-tanggal_uji')
    return render(request, 'ujiimplementasi/daftar_hasil_uji.html', {'hasil_list': hasil_list})


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
    


from django.contrib import messages


def hapus_aktivitas_detail(request, pk):
    aktivitas = get_object_or_404(Aktivitas, pk=pk)

    # Simpan ke Aktivitas (warna Merah)
    Aktivitas.objects.create(
        tanggal=date.today(),
        nama_aktivitas=f"Aktivitas '{aktivitas.nama_aktivitas}' telah dihapus",
        status="Merah"
    )

    aktivitas.delete()
    messages.success(request, "Aktivitas berhasil dihapus.")
    return redirect('activity')



def validasi_model(request, id):
    model_instance = SystemImplementation.objects.get(id=id)
    
    if request.method == 'POST':
        form = ValidasiModelForm(request.POST)
        if form.is_valid():
            validasi = form.save(commit=False)
            validasi.model_terkait = model_instance
            validasi.save()

            # 💡 Tambahkan ini:
            model_instance.status_project = 'Tervalidasi'
            model_instance.save()

            # Optional: Buat log aktivitas validasi
            LogAktivitas.objects.create(
                aktivitas=f"Model '{model_instance.nama_model}' divalidasi oleh user",
                tanggal=timezone.now()
            )

            return redirect('log')
    else:
        form = ValidasiModelForm()

    return render(request, 'myapp/validasi_model.html', {'form': form})


def daftar_model_tervalidasi(request):
    data_list = ValidasiModel.objects.filter(status_validasi="Valid").order_by('-tanggal_validasi')
    return render(request, 'ujiimplementasi/daftar_validasi.html', {'data_list': data_list})

def riwayat_uji_view(request):
    hasil_list = HasilUjiModel.objects.select_related('model_terkait', 'model_terkait__model_terkait').order_by('-tanggal_uji')
    return render(request, 'myapp/riwayat_uji.html', {'hasil_list': hasil_list})


#ke RIDHO
import json
def kirim_managements_ke_teman(request):
    if request.method == 'POST':
        deskripsi = request.POST.get('deskripsi')
        status = request.POST.get('status')

        if not all([deskripsi, status]):
            return render(request, 'myapp/kirimManagemen_form.html', {
                'error': 'Semua data wajib diisi.',
                'deskripsi': deskripsi,
            })

        if status not in ['belum selesai', 'selesai']:
            return render(request, 'myapp/kirimManagemen_form.html', {
                'error': 'Status harus \"belum selesai\" atau \"selesai\".',
                'deskripsi': deskripsi,
            })

        instance = ManagementsSI.objects.create(
            deskripsi=deskripsi,
            status=status
        )

        data = {
            'namaKelompok': "Sistem Implementasi",
            'deskripsi': deskripsi,
            'status': status,
        }

        try:
            print("Data yang dikirim:", json.dumps(data))
            response = requests.post(
                'http://10.24.80.60:8000/api/terima-managementsSI/',
                data=json.dumps(data),
                headers={'Content-Type': 'application/json'}
            )
            print("Kirim berhasil:", response.status_code)
            print("RESPON TEXT:", response.text)

            if response.status_code == 201:
                messages.success(request, "Proyek berhasil dikirim ke teman.")
            else:
                messages.warning(request, f"Gagal kirim. Respon: {response.status_code} - {response.text}")

        except Exception as e:
            print("Gagal kirim:", e)
            messages.error(request, f"Gagal kirim proyek: {e}")

        return redirect('/ujiimplementasi/')

    return render(request, 'myapp/form_uji_model.html')  # ✅ INI YANG BENAR



    
def hapus_model(request, id):
    obj = get_object_or_404(SystemImplementation, id=id)
    nama = obj.nama_model
    
    # Tambahkan pencatatan aktivitas sebelum delete
    Aktivitas.objects.create(
        tanggal=date.today(),
        nama_aktivitas=f"Model '{nama}' dihapus dari sistem",
        status="Merah"
    )

    obj.delete()
    messages.success(request, f"Berhasil menghapus model: {nama}")
    return redirect('log')

def simpan_hasil_uji(request, model_id):
    if request.method == 'POST':
        model = SystemImplementation.objects.get(id=model_id)
        hasil = request.POST.get('hasil_perhitungan')
        rekomendasi = request.POST.get('rekomendasi')
        kirim_pm = request.POST.get('kirim_pm')  # checkbox (jika ada)

        model.hasil_perhitungan = hasil
        model.rekomendasi = rekomendasi
        model.status_project = "Tervalidasi"
        model.save()  # WAJIB!

        # Buat log (opsional)
        LogAktivitas.objects.create(
            aktivitas=f"Model '{model.nama_model}' berhasil divalidasi",
            tanggal=now()
        )

        if kirim_pm:
            # proses kirim ke PM (jika ada)
            pass

        return redirect('dashboard')
    

    # === [catatan] ===
from .models import Catatan, SystemImplementation
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from datetime import date


def catatan_view(request):
    semua_catatan = Catatan.objects.all().order_by('-tanggal')
    return render(request, 'myapp/catatan.html', {'catatan_list': semua_catatan})


def tambah_catatan(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')
        teknisi = request.POST.get('teknisi')
        model_id = request.POST.get('model_terkait')

        model_terkait = SystemImplementation.objects.get(id=model_id) if model_id else None

        Catatan.objects.create(
            judul=judul,
            deskripsi=deskripsi,
            teknisi=teknisi,
            model_terkait=model_terkait
        )

        # Simpan juga ke Aktivitas jika mau
        from .models import Aktivitas
        Aktivitas.objects.create(
            tanggal=date.today(),
            nama_aktivitas=f"Catatan baru: {judul} oleh {teknisi}",
            status="Kuning"
        )

        return redirect('catatan')

    semua_model = SystemImplementation.objects.all()
    return render(request, 'myapp/tambah_catatan.html', {'models': semua_model})


def hapus_catatan(request, id):
    catatan = get_object_or_404(Catatan, id=id)
    catatan.delete()
    return redirect('catatan')
