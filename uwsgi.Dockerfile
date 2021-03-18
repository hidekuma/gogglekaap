FROM python:3.8

# 유저를 추가, 패스워드 입력하지 않고 홈 디렉토리를 생성
RUN adduser --disabled-password python

# 생성된 유저로 전환 (root -> python)
USER python

# 파이썬 의존성 패키지 파일 복사
COPY ./requirements.txt /tmp/requirements.txt

# Python 유저로 의존성 패키지 설치
RUN pip install --user -r /tmp/requirements.txt
# uwsgi 설치
RUN pip install --user uwsgi==2.0.19.1

# 프로젝트 디렉토리 복사
COPY --chown=python:python ./ /var/www/gogglekaap

# 프로젝트 디렉토리로 이동
WORKDIR /var/www/gogglekaap

# 설치한 패키지 명령어 사용을 위해 환경변수등록
ENV PATH="/home/python/.local/bin:${PATH}"

# 8080 포트 노출
EXPOSE 8080

# 엔트리포인트 실행권한 추가
RUN chmod +x ./etc/uwsgi.docker-entrypoint.sh

# uwsgi 실행
#CMD ["uwsgi", "./etc/uwsgi/uwsgi.ini"]
