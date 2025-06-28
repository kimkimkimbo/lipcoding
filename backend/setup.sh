#!/bin/bash
# 백엔드 개발 환경 자동 세팅 스크립트
# 실행 방법: bash setup.sh

set -e

# 1. 가상환경 생성
python3 -m venv venv

# 2. 가상환경 활성화
source venv/bin/activate

# 3. 패키지 설치
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ 가상환경 및 패키지 설치 완료!"
echo "(venv 활성화 상태에서 python app.py로 서버 실행)"
