from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from users.forms import LoginForm, SignupForm
from users.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

# Create your views here.
def login_view(request):
    #이미 로그인 되어 있다면
    if request.user.is_authenticated:
        return redirect('/main/main/')
    if request.method == 'POST':
        #LoginForm 인스턴스 생성, 입력 데이터는 request.POST 사용
        form = LoginForm(data=request.POST)
        
        #LoginForm에 전달된 데이터가 유효하면
        if form.is_valid():
            #username과 password값을 가져와 변수에 할당
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            #username, password에 해당하는 사용자가 있는지 검사
            user = authenticate(username=username, password=password)
            
            #해당 사용자가 존재한다면
            if user:
                #로그인 처리 후 ask 페이지로
                login(request, user)
                return redirect('/main/main/')
            #사용자가 존재하지 않을 경우 실패 로그 출력
            else:
                form.add_error(None, '사용자 또는 비밀번호가 틀렸습니다.')
        
        #유효성 검사 이후에는 cleaned_data에서 데이터를 가져와서 사용
        context = {'form':form}
        return render(request, 'users/login.html',context)
    else:
        #로그인 폼 인스턴스 생성
        form = LoginForm()
        context = {
            'form' : form,
        }
        return render(request,'users/login.html',context)
    
def logout_view(request):
    logout(request)
    return redirect('/main/main/')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # 사용자 객체를 데이터베이스에 저장
            # 폼에서 제공받은 비밀번호로 사용자를 인증
            username = user.username
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # 사용자 로그인 처리
                return redirect('/main/main/')  # 로그인 후 리디렉션
    else:
        form = SignupForm()

    return render(request, 'users/signup.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # 비밀번호 변경 후 세션 유지
            messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
            return redirect('profile')
    else:
        password_form = PasswordChangeForm(request.user)
    
    return render(request, 'users/profile.html', {
        'user': request.user,
        'password_form': password_form
    })
