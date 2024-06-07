<h1 align="center">
        <samp> 약끼리
        </samp>
</h1>

</h1>
<h1 align="left">
프로젝트의 목적
</h1>
 <p>
한국은 고령화가 빠르게 진행되고 있으며, 이에 따라 다제약물 복용자의 수가 증가하고 있습니다. 다제약물 복용은 여러 약물을 동시에 복용하는 것을 의미하며, 이는 약물 간 상호작용 및 부작용의 위험을 높여 건강 문제와 재입원율을 증가시킵니다. 특히, 10개 이상의 약물을 60일 이상 복용하는 초고위험 다제약물 복용자가 급증하고 있어 체계적인 관리가 필요합니다. 국민건강보험공단에서 다제약물 관리사업을 시행하고 있지만, 약사 인력 부족으로 인해 효율적인 관리가 어려운 상황입니다.<br>

저희는 이러한 어려움을 해결하고자 ‘약끼리’ 서비스를 개발하고자 합니다. ‘약끼리’는 약사들이 다제약물 관리 서비스에서 복약상담 계획서를 쉽게 작성할 수 있도록 지원하는 플랫폼입니다. 이를 통해 복약상담의 절차를 간소화하고 인적 자원을 효율적으로 활용할 수 있도록 돕습니다. 또한, 환자와의 복약상담 시 필요한 체크리스트와 교육자료 제공, 복약상담 결과지 작성 기능을 지원하여 약물 관리의 효율성을 높이고 환자들의 건강 증진에 기여하고자 합니다.
</p>
     
<h1 align="left">
  팀원 소개 및 역할
</h1>
<p>
• <a target="_blank" href="https://github.com/ghkstod">나한울 팀장</a> - 웹 개발
<br>
• <a target="_blank" href="https://github.com/suhyeon0325">김수현 팀원</a> - 기획 및 데이터 분석
<br>
• <a target="_blank" href="https://github.com/Kongalmengi">송민 팀원</a> - 웹 개발
<br>
• <a target="_blank" href="https://github.com/Kongalmengi">송준호 팀원</a> - 데이터 분석
<br>
• <a target="_blank" href="">양인선 팀원</a> - 데이터 분석
<br>
• <a target="_blank" href="https://github.com/Ju0s">정주영 팀원</a> - 기획 및 데이터 분석
<br>
• <a target="_blank" href="https://github.com/roklp">한대희 팀원</a> - 데이터 분석
</p>

<h1 align="left">
  주요 개발환경
</h1>
  • 프로그래밍 언어 : Python
  <br>
  • 웹 프레임워크 : Django
  <br>
  • IDE : Visual Studio, Jupyter lab

<h2 align="left">
  주요 라이브러리
</h2>
  • <a target="_blank" href="yakkiri/requirements.txt">requirements.txt</a> 파일 참조

## 테스트 준비 및 방법

- 원격 저장소의 주소를 복사한 다음 로컬 환경에 복제합니다.

```bash
git clone <https://github.com/ms2063/mediview.git>
```

- https://github.com/ms2063/mediview.git 폴더 yakkiri 경로에서 가상환경을 설치합니다.

```bash
pip install virtualenv #기존에 설치한 가상환경이 있다면 생략 가능
virtualenv venv
```

- 가상환경에 접속합니다.

```bash
# mediview/yakkiri/
# Windows OS
source venv/Scripts/activate

# Mac OS
source venv/bin/activate
```

- 라이브러리를 설치합니다.

```bash
# mediview/yakkiri/
pip install -r requirements.txt
```

- MYSQL 사용시, `mediview/.env` 파일을 생성하여 로컬 서버와 데이터베이스를 설정합니다.

```bash
# mediview/.env
# .env
DB_DATABASE = "your_mysql_schemaname"
DB_USER = "your_mysql_username"
DB_PASSWORD = "your_mysql_password"
DB_HOST = "127.0.0.1"
```

- SQLite 사용시, `mediview/config/settings.py`의 DATABASES를 수정합니다.

```bash
# mediview/config/settings.py
#기존 코드
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get('DB_DATABASE'),
        "USER":os.environ.get('DB_USER'),
        "PASSWORD":os.environ.get('DB_PASSWORD'),
        "HOST":os.environ.get('DB_HOST'),
        "PORT":"3306",
    }
}
#변경 코드
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

- Django 마이그레이션

```bash
# mediview/yakkiri/
python manage.py makemigrations
python manage.py migrate
```

- CSV 파일을 보유할 경우, CSV파일을 데이터베이스에 넣는 방법

```bash
#'csv' 폴더를 mediview/csv/ 에 위치
# mediview
python manage.py import_products
```

- Django 서버 실행

```bash
# mediview/yakkiri
python manage.py runserver
```

- 웹 브라우저에 `127.0.0.1:8000/` 실행합니다.
- 정상적으로 서버가 실행된 경우 다음과 같은 화면이 보입니다.

![https://github.com/ms2063/convenience_insights/assets/157222473/29095fd0-cc0d-4ba9-8173-5912ebc89a54](https://raw.githubusercontent.com/ms2063/mediview/main/img/server.png)

# 데모페이지
- Streamlit에서 구현한 Demo는 다음과 같습니다.
  + https://_______.streamlit.app/

<h1 align="left">
  활용 데이터
</h1>

• 의약품 DUR 데이터 (건강보험심사평가원 제공)
<p>활용 정보 : 노인주의, 임부 금기, 병용 금기 등<br>
복용 상담 계획서 작성 및 약품 체크에 활용</p>

• e약은요 데이터 (식품의약안전처 제공)
<p>활용 정보 : 효능, 주의 사항, 상호 작용, 부작용 등<br>
복용 상담 계획서 작성 및 약물 검색창에 활용</p>

<h1 align="left">
  주요 기능
</h1>
주요 기능은 다음과 같습니다.<br>

- 약끼리 체크
<p>
   약물 간의 상호작용 및 다양한 금기사항을 체크할 수 있습니다. 약물이 함께 복용될 때 발생할 수 있는 부작용이나 위험 요소를 미리 확인하여 안전한 복용을 돕습니다. 예를 들어, 두 약물이 함께 복용될 때 생길 수 있는 상호작용, 특정 건강 상태에서 금기인 약물, 그리고 알레르기 반응 가능성을 상세히 확인할 수 있습니다. 이를 통해 약물 복용의 안전성을 높이고, 예상치 못한 부작용을 방지할 수 있습니다.
</p>

- 약물 검색창
<p>
    제품명을 입력하여 다양한 약물 정보를 검색할 수 있습니다. 사용자는 특정 약물의 성분, 효능, 부작용, 복용 방법 등을 쉽게 찾아볼 수 있습니다. 또한, 약물의 제조사 등의 추가 정보도 제공됩니다. 약물 검색을 통해 환자는 자신의 약물에 대해 더 잘 이해하고, 약사의 상담 시 필요한 정보를 미리 파악할 수 있습니다.
</p>

- 복약상담계획서
<p>
    약사가 환자의 건강 정보 및 현재 복용 중인 약물을 입력하면, DUR과 e약은요 정보를 기반으로 복약상담 이전에 필요한 상담 계획서를 제공합니다. ‘약끼리’가 제공하는 복약상담 계획서는 환자가 복용 중인 약물에 대한 기본 정보를 제공할 뿐만 아니라 약사의 검토가 필요한 약물에 대한 정보를 상세히 기술합니다. 이는 약사가 약물에 대한 정보를 일일히 찾아보지 않아도 적절하게 복약 상담 계획을 수립할 수 있도록 돕습니다.
</p>

- 문의사항
<p>
    사용자는 약물에 대한 궁금한 점이나 복용 방법, 부작용 등에 대한 질문을 이 섹션을 통해 제출할 수 있습니다. 전문 약사나 관련 전문가가 신속하고 정확하게 답변을 제공하여 사용자의 궁금증을 해소합니다. 이를 통해 사용자는 약물에 대한 이해를 높이고, 올바른 복약 방법을 따를 수 있습니다.
</p>

- FAQ
<p>
    사용자들이 자주 묻는 질문과 그에 대한 답변을 한눈에 볼 수 있도록 정리된 섹션입니다. 약물 복용에 대한 기본적인 정보, 상호작용, 부작용, 복약 상담 등 다양한 주제에 대한 답변이 제공됩니다. 이 섹션을 통해 사용자는 빠르게 궁금한 점을 해결하고, 필요한 정보를 얻을 수 있습니다.
</p>

<h1 align="left">


## 코드 에러 문의 
- 메뉴 `Issues`-`New Issues`-`메모 남기기`-`Submit new issue`

<h1 align="left">
  발표자료 PDF
</h1>
<p>
• 발표 자료는 해당 링크를 통해 확인 가능합니다:
</p>
<p>
<a target="_blank" href="pdf">한국어 PDF</a>
</p>


# 배포

<h1 align="left">
License
</h1>

• [MIT Licence](LICENSE)

