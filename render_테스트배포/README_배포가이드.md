# Render 테스트 배포 가이드 (3국 담당자 테스트용)

> 목적: 로그인 없이 **빠르게 동작/사용성 테스트**. 실데이터 금지, 더미만.

## 0. 준비물
- 깃헙(GitHub) 계정 1개
- Render 계정 1개 (깃헙으로 가입 가능)
- 이 폴더(render_pkg)의 모든 파일

## 1. 깃헙에 올리기 (웹 화면만으로, 명령어 불필요)
1. github.com 로그인 → 우상단 **+** → **New repository**
2. Repository name: 예 `ogk-merge-test`
3. **Private** 선택(권장) → **Create repository**
4. 만들어진 페이지에서 **uploading an existing file** 링크 클릭
   (또는 **Add file → Upload files**)
5. 이 폴더 안의 항목을 **통째로 드래그**해서 올린다:
   `app.py`, `merge_engine.py`, `requirements.txt`, `render.yaml`,
   `.gitignore`, `templates/`, `assets/`, `data/`, `샘플업로드/`
   - 폴더째 드래그하면 하위 파일까지 같이 올라감
   - `.gitignore`가 안 보이면 그냥 나머지만 올려도 됨
6. 아래 **Commit changes** 클릭

## 2. Render에 연결 (자동 배포)
1. render.com 로그인 → **New +** → **Blueprint**
2. 방금 만든 깃헙 저장소 선택 → Render가 `render.yaml`을 자동 인식
3. **Apply / Deploy** 클릭 → 3~5분 빌드
4. 완료되면 상단에 주소가 생김: `https://ogk-merge-test.onrender.com`
   (이름은 다를 수 있음)

> Blueprint가 안 보이면: **New + → Web Service** → 깃헙 저장소 선택 →
> Build: `pip install -r requirements.txt`
> Start: `gunicorn -b 0.0.0.0:$PORT -w 2 -t 180 app:app` → Create

## 3. 3국 담당자에게 테스트 안내
- 접속 주소: 위 Render 주소
- 각자 **자기 법인 이름을 파일명에 넣어** 업로드 (예: `KOGK_경영위.xlsx`)
  - `샘플업로드` 폴더의 파일을 받아 법인명만 바꿔 쓰면 편함
- 카드별로 칩이 초록으로 바뀌고, 모두 차면 자동 병합 → **최종본 다운로드** 버튼 활성

## 4. 주의 (꼭)
- **실제 재무데이터 절대 금지.** 화면 상단 빨간 배너대로 더미만.
- 무료 플랜은 15분 미사용 시 잠자기 → 다음 접속 시 30초쯤 깨어남(정상).
- 업로드/병합본은 재시작 시 사라짐(테스트용이므로 무방).
- 중국 담당자 접속이 느리거나 막히면, 그게 바로 "공개 클라우드는 한계" 라는 증거 → 실운영은 나스로.

## 5. 테스트 후
- 사용성 피드백 수집 → 로그인 기능 검토 → 나스(Docker) 실배포로 전환
- Render 서비스는 삭제하면 끝(흔적 없음).
