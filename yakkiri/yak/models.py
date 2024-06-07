from django.db import models
from django.conf import settings
from django.utils import timezone
from medicine.models import 제품  # medicine 앱의 제품 모델을 가져옵니다

class ProviderInfo(models.Model):
    name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class PatientInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    is_pregnant = models.BooleanField(default=False)
    is_breastfeeding = models.BooleanField(default=False)
    disease = models.TextField()
    other_health_info = models.TextField()
    is_elderly = models.BooleanField(default=False)
    provider = models.ForeignKey(ProviderInfo, on_delete=models.CASCADE, related_name='patients')

    def __str__(self):
        return self.name

class PatientMedication(models.Model):
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE, related_name='medications')
    product = models.ForeignKey(제품, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)  # 복용량
    frequency = models.CharField(max_length=100)  # 복용 빈도

    def __str__(self):
        return f'{self.patient.name} - {self.product.제품명}'
