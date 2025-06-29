from rest_framework import serializers
from .models import Aktivitas, Catatan, Transaksi, LogAktivitas, Lingkungan,SystemImplementation,ManagementsSI

class AktivitasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aktivitas
        fields = '__all__'

class CatatanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catatan
        fields = '__all__'

#ke ridho
class ManagementsSISerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagementsSI
        fields = '_all_'


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


class SystemImplementationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemImplementation
        fields = '__all__'

