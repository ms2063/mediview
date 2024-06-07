from django.shortcuts import render, redirect

# Create your views here.
def main(request):
    #요청으로부터 사용자 정보를 가져온다.
    user = request.user
    
    #가져온 사용자가 '로그인 했는지' 여부를 가져온다.
    is_authenticated = user.is_authenticated
    
    #요청에 포함된 사용자가 로그인하지 않은 경우
    if not request.user.is_authenticated:
        return render(request,'main/main_not_user.html')
    return render(request,'main/main.html')
