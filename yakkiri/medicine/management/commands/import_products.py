import csv
from django.core.management.base import BaseCommand
from medicine.models import 제품, 품목_사용정보, 업체, 성분, 제품_상세정보, 금기정보, 제품_금기정보, 노인주의상세정보, 병용금기상세정보, 연령별금기상세정보, 용량주의상세정보, 임부금기상세정보, 투여기간상세정보, 효능군중복상세정보
from django.db import models

class Command(BaseCommand):
    help = 'Imports data from CSV files into the database'

    def handle(self, *args, **options):
        self.import_data('금기정보.csv', 금기정보, ['금기코드','금기유형'])
        self.import_data('업체.csv', 업체, ['업체코드','업체명'])
        self.import_data('성분.csv', 성분, ['id','주성분코드','성분명','제형'])
        self.import_data('품목_사용정보.csv', 품목_사용정보,['품목기준코드','효능','사용법','주의사항경고','주의사항','상호작용','부작용','보관법'])
        self.import_data('제품.csv',제품,['제품코드','품목기준코드','제품명','업체코드','주성분코드'])
        self.import_data('제품_금기정보.csv',제품_금기정보,['id','제품코드','금기코드'])
        self.import_data('제품_상세정보.csv',제품_상세정보,['제품코드','ATC코드','규격','단위','상한금액','전일','급여여부'])
        self.import_data('노인주의상세정보.csv',노인주의상세정보,['제품코드','노인주의_약품상세정보'])
        self.import_data('임부금기상세정보.csv',임부금기상세정보,['제품코드','임부금기_금기등급','임부금기_상세정보'])
        self.import_data('병용금기상세정보.csv',병용금기상세정보,['id','제품코드','상대제품코드','상세정보'])
        self.import_data('효능군중복주의상세정보.csv',효능군중복상세정보,['제품코드','효능군중복_효능군','효능군중복_Group'])
        self.import_data('용량주의상세정보.csv',용량주의상세정보,['제품코드','일일최대투여량','일일최대투여기준량','용량주의_상세내용'])
        self.import_data('투여기간상세정보.csv',투여기간상세정보,['제품코드','최대투여기간일수','주성분함량'])
        self.import_data('연령별금기상세정보.csv',연령별금기상세정보,['제품코드','특정연령','특정연령단위','연령처리조건','상세정보'])

    def import_data(self, file_name, model, fields):
        path = f'csv/{file_name}'
        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                obj_data = {}
                skip = False
                for field in fields:
                    value = row[field].strip()
                    field_obj = model._meta.get_field(field)

                    if value == '':
                        if field_obj.null:  # 필드가 null을 허용하면 None을 할당
                            value = None
                        else:
                            self.stdout.write(self.style.WARNING(f"{field} 필드에 비어 있는 필수 값이 있습니다. {row}, 행을 건너뜁니다."))
                            skip = True
                            break

                    else:
                        try:
                            if isinstance(field_obj, models.ForeignKey):
                                related_model = field_obj.related_model
                                value = related_model.objects.get(pk=value)

                            elif isinstance(field_obj, models.IntegerField):
                                # 부동 소수점이 포함된 값을 먼저 실수로 변환 후 정수로 변환
                                value = int(float(value))

                            elif isinstance(field_obj, models.FloatField):
                                value = float(value)

                        except (ValueError, related_model.DoesNotExist) as e:
                            self.stdout.write(self.style.ERROR(f"{field} 필드 처리 중 오류: {e}"))
                            skip = True
                            break

                    obj_data[field] = value

                if not skip:  # 루프가 break 없이 완료되면 업데이트 또는 생성 실행
                    obj, created = model.objects.update_or_create(
                        defaults=obj_data,
                        **{model._meta.pk.name: row[model._meta.pk.name]}
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'{model._meta.model_name} 모델에 {obj}가 생성되었습니다.'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'{model._meta.model_name} 모델이 {obj}로 업데이트되었습니다.'))


