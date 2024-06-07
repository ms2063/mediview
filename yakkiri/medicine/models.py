from django.db import models


class 업체(models.Model):
    업체코드 = models.IntegerField(primary_key=True)
    업체명 = models.TextField()

class 성분(models.Model):
    주성분코드 = models.CharField(max_length=255)
    성분명 = models.CharField(max_length=255)
    제형 = models.TextField(null=True)
    class Meta:
        unique_together = (('주성분코드', '성분명'),)

class 품목_사용정보(models.Model):
    품목기준코드 = models.IntegerField(primary_key=True)
    효능 = models.TextField(null=True)
    사용법 = models.TextField(null=True)
    주의사항경고 = models.TextField(null=True)
    주의사항 = models.TextField(null=True)
    상호작용 = models.TextField(null=True)
    부작용 = models.TextField(null=True)
    보관법 = models.TextField(null=True)

class 제품(models.Model):
    제품코드 = models.IntegerField(primary_key=True)
    품목기준코드 = models.IntegerField(null=True)
    제품명 = models.TextField()
    업체코드 = models.ForeignKey(업체, on_delete=models.CASCADE,null=True)
    주성분코드 = models.CharField(max_length=255)
    

class 제품_상세정보(models.Model):
    제품코드 = models.ForeignKey(제품, on_delete=models.CASCADE,primary_key=True)
    ATC코드 = models.TextField(null=True)
    규격 = models.TextField()
    단위 = models.TextField()
    상한금액 = models.TextField(null=True)
    전일 = models.TextField()
    급여여부 = models.IntegerField()

class 금기정보(models.Model):
    금기코드 = models.IntegerField(primary_key=True)
    금기유형 = models.TextField()

class 제품_금기정보(models.Model):
    제품코드 = models.ForeignKey(제품, on_delete=models.CASCADE)
    금기코드 = models.ForeignKey(금기정보, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('제품코드', '금기코드'),)

class 노인주의상세정보(models.Model):
    제품코드 = models.ForeignKey(제품, on_delete=models.CASCADE,primary_key=True)
    노인주의_약품상세정보 = models.TextField()

class 병용금기상세정보(models.Model):
    제품코드 = models.ForeignKey(제품, on_delete=models.CASCADE)
    상대제품코드 = models.IntegerField()
    상세정보 = models.TextField()
    class Meta:
        unique_together = (('제품코드', '상대제품코드'),)

class 연령별금기상세정보(models.Model):
    제품코드 = models.ForeignKey(제품, on_delete=models.CASCADE,primary_key=True)
    특정연령 = models.IntegerField()
    특정연령단위 = models.TextField()
    연령처리조건 = models.TextField()
    상세정보 = models.TextField(null=True)

class 용량주의상세정보(models.Model):
    제품코드 = models.ForeignKey(제품, on_delete=models.CASCADE,primary_key=True)
    일일최대투여량 = models.TextField()
    일일최대투여기준량 = models.FloatField()
    용량주의_상세내용 = models.TextField(null=True)

class 임부금기상세정보(models.Model):
    제품코드 = models.ForeignKey(제품, on_delete=models.CASCADE,primary_key=True)
    임부금기_금기등급 = models.TextField()
    임부금기_상세정보 = models.TextField(null=True)

class 투여기간상세정보(models.Model):
    제품코드 = models.ForeignKey(제품, on_delete=models.CASCADE,primary_key=True)
    최대투여기간일수 = models.IntegerField()
    주성분함량 = models.TextField()

class 효능군중복상세정보(models.Model):
    제품코드 = models.ForeignKey(제품, on_delete=models.CASCADE,primary_key=True)
    효능군중복_효능군 = models.TextField()
    효능군중복_Group = models.TextField()
