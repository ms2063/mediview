from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import PatientInfo, ProviderInfo, PatientMedication
from .forms import PatientInfoForm, ProviderInfoForm, MedicationForm, ProductSearchForm
from medicine.models import *
from django.template.loader import render_to_string
import pdfkit
from django.http import HttpResponse
from django.conf import settings

@login_required
def step1(request):
    if request.method == 'POST':
        patient_form = PatientInfoForm(request.POST)
        provider_form = ProviderInfoForm(request.POST, prefix="provider")
        if patient_form.is_valid() and provider_form.is_valid():
            provider_info = provider_form.save(commit=False)
            provider_info.user = request.user
            provider_info.created_at = timezone.now()
            print(f"Provider Info before save: {provider_info.name}, {provider_info.organization}")
            provider_info.save()
            print(f"Provider Info after save: {provider_info.name}, {provider_info.organization}")

            patient_info = patient_form.save(commit=False)
            patient_info.is_elderly = patient_info.age >= 65  # 노인 여부 설정
            patient_info.provider = provider_info  # provider 설정
            print(f"Patient Info before save: {patient_info.name}, {patient_info.age}, {patient_info.gender}")
            patient_info.save()
            print(f"Patient Info after save: {patient_info.name}, {patient_info.age}, {patient_info.gender}")

            return redirect('step2', patient_id=patient_info.id)  # patient_id 포함
    else:
        patient_form = PatientInfoForm()
        provider_form = ProviderInfoForm(prefix="provider")
    return render(request, 'yak/step1.html', {'patient_form': patient_form, 'provider_form': provider_form})

def step2(request, patient_id):
    patient = get_object_or_404(PatientInfo, id=patient_id)
    medications = patient.medications.all()
    search_results = []

    search_form = ProductSearchForm(request.POST or None)
    
    if request.method == 'POST':
        if 'search' in request.POST:
            if search_form.is_valid():
                product_name = search_form.cleaned_data['product_name']
                search_results = 제품.objects.filter(제품명__icontains=product_name)
        elif 'add' in request.POST:
            dosage = request.POST.get('dosage')
            frequency = request.POST.get('frequency')
            product_code = request.POST.get('product_code')
            product = get_object_or_404(제품, 제품코드=product_code)
            PatientMedication.objects.create(
                patient=patient,
                product=product,
                dosage=dosage,
                frequency=frequency
            )
            return redirect('step2', patient_id=patient.id)

    print(f"Medications: {medications}")
    print(f"Search Results: {search_results}")

    return render(request, 'yak/step2.html', {
        'search_form': search_form,
        'search_results': search_results,
        'medications': medications,
        'patient': patient,
    })
    
def step3(request, patient_id):
    patient = get_object_or_404(PatientInfo, id=patient_id)
    return render(request, 'yak/step3.html', {'patient': patient})

def step4(request, patient_id):
    patient = get_object_or_404(PatientInfo, id=patient_id)
    medications = patient.medications.all()
    
    # Step 2에서 선택된 약물의 제품코드 리스트
    product_codes = medications.values_list('product__제품코드', flat=True)
    
    # 금기코드가 5 또는 9인 제품_금기정보 가져오기
    contraindications = 제품_금기정보.objects.filter(제품코드__in=product_codes, 금기코드__금기코드__in=[5, 9]).select_related('제품코드', '금기코드')

    # 병용금기 상세정보 가져오기
    drug_interaction_details = 병용금기상세정보.objects.filter(
        제품코드__제품코드__in=product_codes, 
        상대제품코드__in=product_codes
    ).select_related('제품코드')

    # 상대제품명 가져오기
    for detail in drug_interaction_details:
        detail.상대제품명 = 제품.objects.get(제품코드=detail.상대제품코드).제품명

    # 효능군중복 상세정보 가져오기
    efficacy_overlap_details = 효능군중복상세정보.objects.filter(
        제품코드__제품코드__in=product_codes
    ).select_related('제품코드')

    # 필터링된 효능군중복상세정보에서 중복 그룹 필터링
    group_dict = {}
    for detail in efficacy_overlap_details:
        group_key = (detail.효능군중복_효능군, detail.효능군중복_Group)
        if group_key not in group_dict:
            group_dict[group_key] = []
        group_dict[group_key].append(detail)

    filtered_efficacy_overlap_details = []
    for group_key, details in group_dict.items():
        if len(details) > 1:
            filtered_efficacy_overlap_details.extend(details)

    return render(request, 'yak/step4.html', {
        'patient': patient,
        'contraindications': contraindications,
        'drug_interaction_details': drug_interaction_details,
        'filtered_efficacy_overlap_details': filtered_efficacy_overlap_details,
    })

def step5(request, patient_id):
    patient = get_object_or_404(PatientInfo, id=patient_id)
    medications = patient.medications.all()
    
    # Step 2에서 선택된 약물의 품목기준코드 리스트
    product_codes = medications.values_list('product__품목기준코드', flat=True)
    
    # 품목기준코드를 사용하여 품목_사용정보 가져오기
    usage_info_list = 품목_사용정보.objects.filter(품목기준코드__in=product_codes)

    # 부작용 정보 처리
    side_effects = []
    for usage_info in usage_info_list:
        products = 제품.objects.filter(품목기준코드=usage_info.품목기준코드)
        for product in products:
            side_effects.append({
                '제품명': product.제품명,
                '부작용': usage_info.부작용 if usage_info.부작용 else '부작용 상세사항없음'
            })

    return render(request, 'yak/step5.html', {
        'patient': patient,
        'side_effects': side_effects,
    })

def step6(request, patient_id):
    patient = get_object_or_404(PatientInfo, id=patient_id)
    medications = patient.medications.all()
    
    # Step 2에서 선택된 약물의 품목기준코드 리스트
    product_codes = medications.values_list('product__품목기준코드', flat=True)
    
    # 품목기준코드를 사용하여 품목_사용정보 가져오기
    usage_info_list = 품목_사용정보.objects.filter(품목기준코드__in=product_codes)

    # 상호작용 정보 처리
    interactions = []
    for usage_info in usage_info_list:
        products = 제품.objects.filter(품목기준코드=usage_info.품목기준코드)
        for product in products:
            interactions.append({
                '제품명': product.제품명,
                '상호작용': usage_info.상호작용 if usage_info.상호작용 else '상호작용 상세사항없음'
            })

    return render(request, 'yak/step6.html', {
        'patient': patient,
        'interactions': interactions,
    })
    
def step7(request, patient_id):
    patient = get_object_or_404(PatientInfo, id=patient_id)
    medications = patient.medications.all()
    
    # Step 2에서 선택된 약물의 품목기준코드 리스트
    product_codes = medications.values_list('product__품목기준코드', flat=True)
    product_codes_list = medications.values_list('product__제품코드', flat=True)
    
    # 품목기준코드를 사용하여 품목_사용정보 가져오기
    usage_info_list = 품목_사용정보.objects.filter(품목기준코드__in=product_codes)

    # 사용법 정보 처리
    usage_methods = []
    for usage_info in usage_info_list:
        products = 제품.objects.filter(품목기준코드=usage_info.품목기준코드)
        for product in products:
            usage_methods.append({
                '제품명': product.제품명,
                '사용법': usage_info.사용법 if usage_info.사용법 else '사용법 상세사항없음'
            })

    # 제품코드를 사용하여 금기코드가 2, 7, 8인 제품_금기정보 가져오기
    contraindications = 제품_금기정보.objects.filter(제품코드__in=product_codes_list, 금기코드__금기코드__in=[2, 7, 8]).select_related('제품코드', '금기코드')

    # 추가 상세정보 처리
    contraindication_details = []
    for contraindication in contraindications:
        detail = {'제품명': contraindication.제품코드.제품명, '금기유형': contraindication.금기코드.금기유형}
        if contraindication.금기코드.금기코드 == 7:
            try:
                duration_info = 투여기간상세정보.objects.get(제품코드=contraindication.제품코드)
                detail.update({
                    '최대투여기간일수': duration_info.최대투여기간일수,
                    '주성분함량': duration_info.주성분함량
                })
            except 투여기간상세정보.DoesNotExist:
                detail.update({
                    '최대투여기간일수': '정보 없음',
                    '주성분함량': '정보 없음'
                })
        elif contraindication.금기코드.금기코드 == 8:
            try:
                dosage_info = 용량주의상세정보.objects.get(제품코드=contraindication.제품코드)
                detail.update({
                    '일일최대투여량': dosage_info.일일최대투여량,
                    '일일최대투여기준량': dosage_info.일일최대투여기준량,
                    '용량주의_상세내용': dosage_info.용량주의_상세내용
                })
            except 용량주의상세정보.DoesNotExist:
                detail.update({
                    '일일최대투여량': '정보 없음',
                    '일일최대투여기준량': '정보 없음',
                    '용량주의_상세내용': '정보 없음'
                })
        contraindication_details.append(detail)

    # 디버그 출력
    print(f"contraindications: {contraindications}")
    print(f"contraindication_details: {contraindication_details}")

    return render(request, 'yak/step7.html', {
        'patient': patient,
        'usage_methods': usage_methods,
        'contraindication_details': contraindication_details,
    })

def step8(request, patient_id):
    patient = get_object_or_404(PatientInfo, id=patient_id)
    medications = patient.medications.all()
    
    # Step 2에서 선택된 약물의 품목기준코드 리스트
    product_codes = medications.values_list('product__품목기준코드', flat=True)
    
    # 품목기준코드를 사용하여 품목_사용정보 가져오기
    usage_info_list = 품목_사용정보.objects.filter(품목기준코드__in=product_codes)

    # 보관법 정보 처리
    storage_methods = []
    for usage_info in usage_info_list:
        products = 제품.objects.filter(품목기준코드=usage_info.품목기준코드)
        for product in products:
            storage_methods.append({
                '제품명': product.제품명,
                '보관법': usage_info.보관법 if usage_info.보관법 else '보관법 상세사항없음'
            })

    return render(request, 'yak/step8.html', {
        'patient': patient,
        'storage_methods': storage_methods,
    })

def step9(request, patient_id):
    patient = get_object_or_404(PatientInfo, id=patient_id)
    return render(request, 'yak/step9.html', {'patient': patient})

def step10(request, patient_id):
    patient = get_object_or_404(PatientInfo, id=patient_id)
    medications = patient.medications.all()
    
    # Step 2에서 선택된 약물의 제품코드 리스트
    product_codes = medications.values_list('product__제품코드', flat=True)
    
    # 제품코드를 사용하여 금기코드가 1, 3, 4, 6인 제품_금기정보 가져오기
    warnings = 제품_금기정보.objects.filter(제품코드__in=product_codes, 금기코드__금기코드__in=[1, 3, 4, 6]).select_related('제품코드', '금기코드')

    # 주의약물 정보 처리
    warning_details = []
    for warning in warnings:
        detail = {'제품명': warning.제품코드.제품명, '금기유형': warning.금기코드.금기유형}
        if warning.금기코드.금기코드 == 3:
            try:
                elderly_info = 노인주의상세정보.objects.get(제품코드=warning.제품코드)
                detail.update({
                    '노인주의_약품상세정보': elderly_info.노인주의_약품상세정보,
                })
            except 노인주의상세정보.DoesNotExist:
                detail.update({
                    '노인주의_약품상세정보': '정보 없음',
                })
        elif warning.금기코드.금기코드 == 4:
            try:
                pregnant_info = 임부금기상세정보.objects.get(제품코드=warning.제품코드)
                detail.update({
                    '임부금기_금기등급': pregnant_info.임부금기_금기등급,
                    '임부금기_상세정보': pregnant_info.임부금기_상세정보,
                })
            except 임부금기상세정보.DoesNotExist:
                detail.update({
                    '임부금기_금기등급': '정보 없음',
                    '임부금기_상세정보': '정보 없음',
                })
        elif warning.금기코드.금기코드 == 6:
            try:
                age_info = 연령별금기상세정보.objects.get(제품코드=warning.제품코드)
                detail.update({
                    '특정연령': age_info.특정연령,
                    '특정연령단위': age_info.특정연령단위,
                    '연령처리조건': age_info.연령처리조건,
                    '상세정보': age_info.상세정보,
                })
            except 연령별금기상세정보.DoesNotExist:
                detail.update({
                    '특정연령': '정보 없음',
                    '특정연령단위': '정보 없음',
                    '연령처리조건': '정보 없음',
                    '상세정보': '정보 없음',
                })
        warning_details.append(detail)

    # 디버그 출력
    print(f"warnings: {warnings}")
    print(f"warning_details: {warning_details}")

    return render(request, 'yak/step10.html', {
        'patient': patient,
        'warning_details': warning_details,
    })

def step11(request, patient_id):
    patient = get_object_or_404(PatientInfo, id=patient_id)
    medications = patient.medications.all()

    return render(request, 'yak/step11.html', {
        'patient': patient,
        'medications': medications,
    })

def download_pdf(request, patient_id):
    patient = get_object_or_404(PatientInfo, id=patient_id)
    medications = patient.medications.all()
    provider_info = patient.provider
    print(f"Provider Info in PDF before rendering: {provider_info.name}, {provider_info.organization}")
    print(f"Patient Info in PDF before rendering: {patient.name}, {patient.age}, {patient.gender}")
    
    # Step 2에서 선택된 약물의 품목기준코드 및 제품코드 리스트
    product_codes = medications.values_list('product__제품코드', flat=True)
    product_criteria_codes = medications.values_list('product__품목기준코드', flat=True)
    
    # 각 스텝의 내용을 수집
    provider_info = patient.provider

    # Step 2 내용
    usage_info_list = 품목_사용정보.objects.filter(품목기준코드__in=medications.values_list('product__품목기준코드', flat=True))

    # Step 4 내용
    contraindications_5_9 = 제품_금기정보.objects.filter(제품코드__in=medications.values_list('product__제품코드', flat=True), 금기코드__금기코드__in=[5, 9]).select_related('제품코드', '금기코드')
    contraindication_details = []
    for contraindication in contraindications_5_9:
        detail = {'제품명': contraindication.제품코드.제품명, '금기유형': contraindication.금기코드.금기유형}
        if contraindication.금기코드.금기코드 == 5:
            details = 병용금기상세정보.objects.filter(제품코드=contraindication.제품코드)
            detail.update({'상세정보': [{'상대제품명': 제품.objects.get(제품코드=d.상대제품코드).제품명, '상세정보': d.상세정보} for d in details]})
        elif contraindication.금기코드.금기코드 == 9:
            overlaps = 효능군중복상세정보.objects.filter(제품코드=contraindication.제품코드)
            detail.update({'상세정보': [{'효능군중복_효능군': o.효능군중복_효능군, '효능군중복_Group': o.효능군중복_Group} for o in overlaps]})
        contraindication_details.append(detail)

    # Step 5 내용
    side_effects = []
    for medication in medications:
        usage_info_list = 품목_사용정보.objects.filter(품목기준코드=medication.product.품목기준코드)
        for usage_info in usage_info_list:
            side_effects.append({
                '제품명': medication.product.제품명,
                '부작용': usage_info.부작용 if usage_info.부작용 else '부작용 상세사항없음'
            })

    # Step 6 내용
    interactions = []
    for medication in medications:
        usage_info_list = 품목_사용정보.objects.filter(품목기준코드=medication.product.품목기준코드)
        for usage_info in usage_info_list:
            interactions.append({
                '제품명': medication.product.제품명,
                '상호작용': usage_info.상호작용 if usage_info.상호작용 else '상호작용 상세사항없음'
            })

    # Step 7 내용
    usage_methods = []
    for medication in medications:
        usage_info_list = 품목_사용정보.objects.filter(품목기준코드=medication.product.품목기준코드)
        for usage_info in usage_info_list:
            usage_methods.append({
                '제품명': medication.product.제품명,
                '사용법': usage_info.사용법 if usage_info.사용법 else '사용법 상세사항없음'
            })

    # Step 8 내용
    storage_methods = []
    for medication in medications:
        usage_info_list = 품목_사용정보.objects.filter(품목기준코드=medication.product.품목기준코드)
        for usage_info in usage_info_list:
            storage_methods.append({
                '제품명': medication.product.제품명,
                '보관법': usage_info.보관법 if usage_info.보관법 else '보관법 상세사항없음'
            })

    # Step 10 내용
    warnings = 제품_금기정보.objects.filter(제품코드__in=medications.values_list('product__제품코드', flat=True), 금기코드__금기코드__in=[1, 3, 4, 6]).select_related('제품코드', '금기코드')
    warning_details = []
    for warning in warnings:
        detail = {'제품명': warning.제품코드.제품명, '금기유형': warning.금기코드.금기유형}
        if warning.금기코드.금기코드 == 3:
            try:
                elderly_info = 노인주의상세정보.objects.get(제품코드=warning.제품코드)
                detail.update({
                    '노인주의_약품상세정보': elderly_info.노인주의_약품상세정보,
                })
            except 노인주의상세정보.DoesNotExist:
                detail.update({
                    '노인주의_약품상세정보': '정보 없음',
                })
        elif warning.금기코드.금기코드 == 4:
            try:
                pregnant_info = 임부금기상세정보.objects.get(제품코드=warning.제품코드)
                detail.update({
                    '임부금기_금기등급': pregnant_info.임부금기_금기등급,
                    '임부금기_상세정보': pregnant_info.임부금기_상세정보,
                })
            except 임부금기상세정보.DoesNotExist:
                detail.update({
                    '임부금기_금기등급': '정보 없음',
                    '임부금기_상세정보': '정보 없음',
                })
        elif warning.금기코드.금기코드 == 6:
            try:
                age_info = 연령별금기상세정보.objects.get(제품코드=warning.제품코드)
                detail.update({
                    '특정연령': age_info.특정연령,
                    '특정연령단위': age_info.특정연령단위,
                    '연령처리조건': age_info.연령처리조건,
                    '상세정보': age_info.상세정보,
                })
            except 연령별금기상세정보.DoesNotExist:
                detail.update({
                    '특정연령': '정보 없음',
                    '특정연령단위': '정보 없음',
                    '연령처리조건': '정보 없음',
                    '상세정보': '정보 없음',
                })
        warning_details.append(detail)

    html_string = render_to_string('yak/report.html', {
        'patient': patient,
        'provider_info': provider_info,
        'medications': medications,
        'contraindications_5_9': contraindication_details,
        'side_effects': side_effects,
        'interactions': interactions,
        'usage_methods': usage_methods,
        'storage_methods': storage_methods,
        'warning_details': warning_details,
        'patient_name': patient.name,
        'provider_name': provider_info.name,
        'provider_affiliation': provider_info.organization,
    })
    
    config = pdfkit.configuration(wkhtmltopdf=settings.PDFKIT_CONFIG['wkhtmltopdf'])
    pdf = pdfkit.from_string(html_string, False, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{patient.id}.pdf"'

    return response