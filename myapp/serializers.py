from rest_framework import serializers
from .models import Aktivitas, Catatan, Transaksi, LogAktivitas, Lingkungan

class AktivitasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aktivitas
        fields = '__all__'

class CatatanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catatan
        fields = '__all__'

class TransaksiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaksi
        fields = '__all__'

class LogAktivitasSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogAktivitas
        fields = '__all__'

class LingkunganSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lingkungan
        fields = '__all__'
