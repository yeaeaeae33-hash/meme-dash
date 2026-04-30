# 🔥 밈 트렌드 위클리 대시보드

매주 월요일 오후 2시(KST)에 Anthropic Claude API가 자동으로 최신 밈을 수집하고 대시보드를 업데이트합니다.

---

## 🚀 세팅 방법 (딱 5단계)

### Step 1. 이 저장소를 본인 GitHub에 업로드
1. GitHub에서 새 저장소(Repository) 생성
   - Repository name: `meme-dashboard` (원하는 이름 OK)
   - **Public** 선택 (GitHub Pages 무료 사용)
   - "Create repository" 클릭

2. 아래 방법 중 하나로 파일 업로드:
   - **간단한 방법**: GitHub 웹에서 파일 직접 드래그&드롭 업로드
   - **Git 사용**: `git push` 로 업로드

### Step 2. Anthropic API 키 발급
1. https://console.anthropic.com 접속
2. API Keys 메뉴 → "Create Key"
3. 키 복사 (sk-ant-... 형식)

### Step 3. GitHub Secrets에 API 키 등록
1. 저장소 → **Settings** 탭
2. 좌측 메뉴 → **Secrets and variables** → **Actions**
3. **"New repository secret"** 클릭
4. Name: `ANTHROPIC_API_KEY`
5. Value: 복사한 API 키 붙여넣기
6. "Add secret" 클릭

### Step 4. GitHub Pages 활성화
1. 저장소 → **Settings** 탭
2. 좌측 메뉴 → **Pages**
3. Source: **Deploy from a branch**
4. Branch: **main** / **/ (root)** 선택
5. "Save" 클릭
6. 잠시 후 URL 발급됨: `https://[내GitHub아이디].github.io/meme-dashboard/`

### Step 5. 첫 번째 수동 실행 (테스트)
1. 저장소 → **Actions** 탭
2. "Weekly Meme Trend Collector" 클릭
3. **"Run workflow"** → "Run workflow" 클릭
4. 완료 후 GitHub Pages URL 접속하면 대시보드 확인!

---

## 📅 자동 실행 일정
- **매주 월요일 오후 2시 (KST)** 자동 실행
- GitHub Actions가 깨어나 → Python 스크립트 실행 → API로 밈 수집 → memes.json 업데이트 → 자동 배포

## 🔗 공유 방법
- `https://[내GitHub아이디].github.io/meme-dashboard/` URL을 공유
- 누구나 같은 URL로 접속하면 항상 최신 데이터 확인 가능
- **새로고침만 하면 최신 데이터** 자동 반영

## 💡 파일 구조
```
meme-dashboard/
├── index.html                    ← 대시보드 메인 페이지
├── data/
│   └── memes.json               ← 주차별 누적 밈 데이터
├── scripts/
│   └── collect_memes.py         ← 자동 수집 Python 스크립트
└── .github/
    └── workflows/
        └── update.yml           ← GitHub Actions 자동화 설정
```

## ❓ 자주 묻는 질문

**Q. 비용이 드나요?**
- GitHub Actions: 무료 (월 2,000분 제공, 실행당 약 1~2분 소요)
- GitHub Pages: 무료
- Anthropic API: 1회 실행당 약 $0.01~0.03 수준 (매우 저렴)

**Q. 로컬에서 HTML 파일을 열면 왜 안 되나요?**
- `fetch('./data/memes.json')`은 로컬 파일 시스템에서 CORS 오류가 발생해요.
- 반드시 GitHub Pages URL로 접속해야 합니다.

**Q. 수동으로 업데이트하고 싶으면?**
- Actions 탭 → "Run workflow" 버튼으로 언제든 수동 실행 가능
