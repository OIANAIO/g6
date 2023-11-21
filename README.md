# gnuboard with python

.env

```
# mysql, postgresql, sqlite3
DB_ENGINE = ""
DB_HOST = ""
DB_PORT = ""
DB_USER = ""
DB_PASSWORD = ""
DB_NAME = ""

# 테이블명 앞에 붙는 이름
# g6_ 로 설정시
# 예) g6_config, g6_member, g6_board
DB_TABLE_PREFIX = "g6_"

SMTP_SERVER="localhost"
SMTP_PORT=25
SMTP_USERNAME="account@your-domain.com" # 메일 테스트시 보내는 사용자 이름 및 이메일 주소 반드시 넣어야 함
SMTP_PASSWORD=""

# 디버그 모드 설정 (True/False)
APP_IS_DEBUG = "False"

# 네이버 메일 설정
# SMTP_SERVER="smtp.naver.com"
# SMTP_PORT=465 # 보안 연결(SSL) 필요
# SMTP_USERNAME="네이버 로그인 아이디"
# SMTP_PASSWORD="네이버 로그인 비밀번호"


# 웹사이트 표시 방법
# "True" (기본값) : 반응형 웹사이트 (참고: 반응형 템플릿만 제공합니다.)
# "False" : 적응형 웹사이트
IS_RESPONSIVE = "False" # 반드시 문자열로 입력해야 합니다.

UPLOAD_IMAGE_RESIZE = "False"  # 이미지 크기변환 여부
UPLOAD_IMAGE_SIZE_LIMIT = 20 # MB 이미지 업로드 용량 (기본값 20MB)
UPLOAD_IMAGE_QUALITY = 80  # (0~100) default 80 이미지 업로드 퀄리티(jpg)

# UPLOAD_IMAGE_RESIZE 가 true 이고 설정된값보다 크면 크기를 변환합니다.
UPLOAD_IMAGE_RESIZE_WIDTH = 1200  # px 이미지 업로드 크기변환 가로 크기 
UPLOAD_IMAGE_RESIZE_HEIGHT = 2800  # px 이미지 업로드 크기변환 세로 크기

# https://developers.popbill.com/guide/sms/python/getting-started/sdk-configration
#팝빌 회원 ID
POPBILL_LINK_ID = ''

#팝빌에서 발급받은 비밀키. 유출에 주의하시기 바랍니다.
POPBILL_SECREKEY = ''

# 연동환경 설정값, 개발용(True), 상업용(False)
POPBILL_IS_TEST = False

# 인증토큰 IP제한기능 사용여부, 권장(True)
POPBILL_IP_RESTRICT_ON_OFF = True

#팝빌 API 서비스 고정 IP 사용여부, true-사용, false-미사용, 기본값(false)
POPBILL_USE_STATIC_IP = False

# 로컬시스템 시간 사용여부
POPBILL_USE_LOCALTIME_YN = True # 기본값 (true)


```

modules_state.json 에 모듈 활성화/비활성화가 기록됩니다.
서버가 실행중일 때는 수정하면 안됩니다.

아직 postgresql, sqlite3 는 정상 작동하지 않음
mysql 관련 코드로 작성하면 안됨. 예) TINYINT
