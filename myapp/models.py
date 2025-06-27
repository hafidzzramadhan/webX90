from django.db import models



class Catatan(models.Model):
    model_terkait = models.ForeignKey('SystemImplementation', on_delete=models.CASCADE, null=True, blank=True)
    tanggal = models.DateField(auto_now_add=True)
    judul = models.CharField(max_length=255)
    deskripsi = models.TextField()
    teknisi = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.judul} - {self.tanggal}"
    
class Aktivitas(models.Model):
    tanggal = models.DateField()
    nama_aktivitas = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nama_aktivitas} - {self.status}"


class Transaksi(models.Model):
    model = models.CharField(max_length=100)
    jenis = models.CharField(max_length=100)
    tanggal_input = models.DateField()

    def __str__(self):
        return f"{self.model} - {self.jenis}"

class LogAktivitas(models.Model):
    tanggal = models.DateField()
    aktivitas = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    no = models.CharField(max_length=20, null=True, blank=True)
    dokumentasi = models.URLField(null=True, blank=True)
    laporan = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.aktivitas} - {self.status}"


class Lingkungan(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField()
    tanggal_diperbarui = models.DateField()

    def __str__(self):
        return self.nama

class SystemImplementation(models.Model):
    no = models.IntegerField()
    nama_model = models.CharField(max_length=100, default="default_model")
    status_project = models.CharField(max_length=50)
    
    # Dulu: final_model = models.CharField(max_length=100)
    dokumentasi_model = models.URLField(help_text="Link ke Google Colab")

    # Dulu: dokumentasi_link = models.URLField()
    laporan_model = models.FileField(upload_to='laporan/', null=True, blank=True, help_text="Upload PDF laporan model")

    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.nama_model} - {self.status_project}"
    
class ValidasiModel(models.Model):
    model_terkait = models.ForeignKey(SystemImplementation, on_delete=models.CASCADE)
    validator = models.CharField(max_length=100)
    catatan = models.TextField(blank=True, null=True)
    status_validasi = models.CharField(max_length=50, choices=[("Valid", "Valid"), ("Perlu Revisi", "Perlu Revisi")])
    tanggal_validasi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Validasi untuk {self.model_terkait.nama_model} oleh {self.validator}"

class HasilUjiModel(models.Model):
    model_terkait = models.ForeignKey(ValidasiModel, on_delete=models.CASCADE)
    hasil_perhitungan = models.TextField()
    rekomendasi = models.TextField()
    kirim_ke_pm = models.BooleanField(default=False)
    tanggal_uji = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Hasil uji untuk {self.model_terkait}"


class Transaksi(models.Model):
    nama_transaksi = models.CharField(max_length=100)
    deskripsi = models.TextField()
    waktu = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_transaksi

class TransaksiModel(models.Model):
    waktu_transaksi = models.DateTimeField(auto_now_add=True)
    nama_model = models.CharField(max_length=200)
    input_data = models.TextField()
    output_data = models.TextField()

    def __str__(self):
        return f"{self.nama_model} - {self.waktu_transaksi}"