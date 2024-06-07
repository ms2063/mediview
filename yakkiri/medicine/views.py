import json
import logging
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

@login_required
def search(request):
    query = request.GET.get('q')
    search_by = request.GET.get('search_by', '제품명')
    results = []

    if query:
        if search_by == '제품명':
            results = 제품.objects.filter(제품명__icontains=query).select_related('업체코드')
        elif search_by == '주성분코드':
            results = 제품.objects.filter(주성분코드__icontains=query).select_related('업체코드')
        elif search_by == '업체명':
            results = 제품.objects.filter(업체코드__업체명__icontains=query).select_related('업체코드')

    금기유형_list = 금기정보.objects.values_list('금기유형', flat=True).distinct()

    context = {
        'query': query,
        'search_by': search_by,
        'results': results,
        '금기유형_list': 금기유형_list,
    }
    return render(request, 'medicine/search_results.html', context)

@login_required
def get_contraindications(request, 제품코드):
    제품_instance = 제품.objects.get(제품코드=제품코드)
    contraindications = 제품_금기정보.objects.filter(제품코드=제품코드).select_related('금기코드')
    
    data = []
    selected_products = get_selected_products_from_request(request)
    
    logger.debug(f"Selected products: {selected_products}")

    for ci in contraindications:
        detail_info = []
        logger.debug(f"Processing contraindication: {ci.금기코드.금기코드}")
        if ci.금기코드.금기코드 == 1:
            detail_info = [{'상세정보': '상세정보 없음'}]
        elif ci.금기코드.금기코드 == 3:
            detail_info = list(노인주의상세정보.objects.filter(제품코드=제품코드).values().distinct())
        elif ci.금기코드.금기코드 == 4:
            detail_info = list(임부금기상세정보.objects.filter(제품코드=제품코드).values().distinct())
        elif ci.금기코드.금기코드 == 5:
            병용금기 = 병용금기상세정보.objects.filter(제품코드=제품코드)
            logger.debug(f"Drug interaction info: {병용금기}")
            for item in 병용금기:
                logger.debug(f"Checking item: {item}")
                if str(item.상대제품코드) in selected_products and item.상세정보:
                    try:
                        상대제품 = 제품.objects.get(제품코드=item.상대제품코드)
                        detail_info.append({
                            '상대제품명': 상대제품.제품명,
                            '상세정보': item.상세정보
                        })
                    except 제품.DoesNotExist:
                        detail_info.append({
                            '상대제품명': '제품명 없음',
                            '상세정보': item.상세정보
                        })
        elif ci.금기코드.금기코드 == 6:
            detail_info = list(연령별금기상세정보.objects.filter(제품코드=제품코드).values().distinct())
        elif ci.금기코드.금기코드 == 7:
            detail_info = list(투여기간상세정보.objects.filter(제품코드=제품코드).values().distinct())
        elif ci.금기코드.금기코드 == 8:
            detail_info = list(용량주의상세정보.objects.filter(제품코드=제품코드).values().distinct())
        elif ci.금기코드.금기코드 == 9:
            효능군중복 = 효능군중복상세정보.objects.filter(제품코드=제품코드).distinct()
            logger.debug(f"Efficacy overlap info: {효능군중복}")
            overlapping_products = set()
            for item in 효능군중복:
                for selected_product in selected_products:
                    selected_product_eff_overlap = 효능군중복상세정보.objects.filter(
                        제품코드=selected_product,
                        효능군중복_효능군=item.효능군중복_효능군,
                        효능군중복_Group=item.효능군중복_Group
                    ).distinct()
                    if selected_product_eff_overlap.exists():
                        overlapping_products.add(selected_product)
            if overlapping_products:
                overlapping_product_names = [제품.objects.get(제품코드=code).제품명 for code in overlapping_products]
                detail_info = [{'효능군중복_효능군': item.효능군중복_효능군, '효능군중복_Group': item.효능군중복_Group}]
                제품_instance.제품명 = ', '.join(overlapping_product_names)
        elif ci.금기코드.금기코드 == 10:
            동일성분주의 = 제품.objects.filter(주성분코드=제품_instance.주성분코드).exclude(제품코드=제품코드).values('주성분코드').distinct()
            detail_info = [{'주성분코드': item['주성분코드']} for item in 동일성분주의 if item['주성분코드']]
        else:
            detail_info = [{'상세정보': '상세정보 없음'}]
        
        logger.debug(f"Detail info: {detail_info}")

        unique_detail_info = {frozenset(item.items()): item for item in detail_info}.values()
        
        if unique_detail_info:  # Only add if there is detail info
            data.append({
                '제품명': 제품_instance.제품명,
                '금기코드': ci.금기코드.금기코드,
                '금기유형': ci.금기코드.금기유형,
                '상세정보': list(unique_detail_info),
            })

    return JsonResponse(data, safe=False)

@login_required
def get_selected_products_from_request(request):
    selected_products = request.GET.get('selected_products', '[]')
    return json.loads(selected_products)
