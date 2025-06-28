# Mentor-Mentee Frontend

## 소개
- 파스텔 보라색 계열의 미니멀하고 UX 친화적인 멘토-멘티 매칭 웹앱 프론트엔드
- Next.js 기반 SSR/CSR 혼합, styled-components 테마, 반응형, 접근성, 글로벌 스타일
- 주요 기능: 회원가입/로그인, 프로필 등록/수정, 멘토 목록(필터/정렬/검색), 매칭 요청/수락/거절/취소, API 연동

## 실행 방법

```bash
cd frontend
npm install
npm run dev
```

- 개발 서버: http://localhost:3000
- 백엔드 API: http://localhost:8080/api

## 주요 폴더 구조
- src/pages: 라우트/페이지
- src/components: 공통 컴포넌트
- src/theme: 테마/팔레트
- src/api: API 연동
- src/global.css: 글로벌 스타일

## 테마
- 메인 컬러: 파스텔 보라 (#b39ddb)
- 미니멀, 깔끔, 부드러운 UX

## 참고
- OpenAPI 명세 기반 API 연동
- JWT 인증, 프로필 이미지 업로드, 검색/정렬/필터, 반응형 지원
