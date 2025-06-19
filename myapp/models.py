from django.db import models

class Aktivitas(models.Model):
    tanggal = models.DateField()
    nama_aktivitas = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nama_aktivitas} - {self.status}"

class Catatan(models.Model):
    tanggal = models.DateField()
    judul = models.CharField(max_length=255)
    deskripsi = models.TextField()
    teknisi = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.judul} - {self.teknisi}"

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

    def __str__(self):
        return f"{self.aktivitas} - {self.status}"

class Lingkungan(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField()
    tanggal_diperbarui = models.DateField()

    def __str__(self):
        return self.nama
