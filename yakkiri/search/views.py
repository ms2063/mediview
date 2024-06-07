from django.shortcuts import render
from medicine.models import 제품, 업체, 제품_상세정보, 품목_사용정보
from django.contrib.auth.decorators import login_required

@login_required
def search_products(request):
    query = request.GET.get('q')
    if query:
        results = 제품.objects.filter(제품명__icontains=query).select_related('업체코드')
        detailed_results = []
        for product in results:
            try:
                product_details = 제품_상세정보.objects.get(제품코드=product.제품코드)
            except 제품_상세정보.DoesNotExist:
                product_details = None

            try:
                usage_info = 품목_사용정보.objects.get(품목기준코드=product.품목기준코드)
            except 품목_사용정보.DoesNotExist:
                usage_info = None

            detailed_results.append((product, product_details, usage_info))
    else:
        detailed_results = []

    return render(request, 'search/search_form.html', {'results': detailed_results, 'query': query})
