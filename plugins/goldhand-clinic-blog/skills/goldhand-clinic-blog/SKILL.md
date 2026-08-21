---
name: goldhand-clinic-blog
description: 금손한의원 정보형 네이버 블로그 글을 만든다. 2024-10-04 이후 직접 본문까지 검토한 위석부부한의원 정보글 11편 중 최근 3개와 겹치지 않는 한 편에서 주제·독자 고민·핵심 일반 정보·정보 공개 순서만 가져오고, 말투는 2026-08-21 현재 금손 공식 블로그 공개 글 74편을 전수 분석한 `goldhand-official-voice-v1`로만 쓴다. 위석 말투·문장·업체 사실·경력·사례·성과 수치는 쓰지 않는다. 제목에는 본문이 실제로 답하는 개수 숫자를 사용하고, 도입에는 3분 읽기 안내와 핵심 하이라이트를 둔다. 시각 자료는 사용자 소유 callilife 작품을 참고한 GPT Image 1~3장과 플러그인 `assets/official-media`에 내장된 실제 금손 사진 6~12장을 함께 사용한다. 실제 사진은 원장이 환자를 치료·진찰·상담하는 장면을 최우선으로 고르고 이미지 아래 보이는 캡션은 쓰지 않는다. 최근 3개 글의 실제 사진은 먼저 제외하고 새 안전 사진이 6장보다 적을 때만 신뢰 사진을 최소 수량까지 재사용한다. `ㅎㅎ`, `ㅠㅠ`, `^^`, 이모지뿐 아니라 실제 진료실에서 말하지 않을 AI 번역투·작문체·감성적 행동 유도 문장군을 차단한다. 꾸밈은 중앙 정렬·네이버 순정 인용구·구분선·표1·고정 가치입증·50:50 운영정보의 `goldhand-naver-native-v4`로 고정하고 제목 키워드 1회·본문 2~3회, 1,400~1,800자, 모바일 2~3줄을 적용해 바탕화면에 복사용 HTML을 저장한다.
---

# 금손한의원 블로그 자동화

금손한의원 박준희 원장이 환자 한 명에게 차분히 설명하는 정보 글을 만든다. 내부 기획 라벨, 레퍼런스 ID, SEO 횟수, 검수표, 이미지 지시는 완성 본문에 노출하지 않는다.

## 절대 계약

1. 작성 형식은 정보 본문형 하나뿐이며 HTML 유형 값은 `정보전달형`이다. 일상글은 말투 분석 자료일 뿐 생성하지 않는다.
2. 도입의 대표 독자 고민은 선택한 위석 정보글 한 편의 실제 고민을 금손 내용으로 바꿔 2~3개 둔다. 같은 뜻을 늘려 개수를 맞추지 않는다.
3. 마지막 고민 뒤, 첫 정보 소제목 전에 독자가 헷갈리는 이유와 이번 글에서 풀 범위·금손의 설명 기준·읽고 얻게 될 판단을 예고한다. 이 부분은 배경·테두리가 없는 일반 산문 문단으로 쓴다.
4. 업체소개형·사례공유형·스토리텔링형·일상글·공지·이벤트는 자동 선택, 최근 이력 회전, 무작위 선택, 기본값, 자료 부족 fallback 어디에도 넣지 않는다.
5. 자동 주제는 `assets/wipark-content-briefs.json`의 본문 검토 완료 11편에서만 고른다. 최근 3개와 같은 레퍼런스·핵심 대상·검색 의도는 후보에서 제외한다.
6. 한 글에서는 주제를 가져온 위석 원문 한 편을 `content reference`로 고정한다. 그 글의 주제·독자 고민·핵심 일반 정보·정보 공개 순서를 사용하며 여러 글을 섞지 않는다.
7. 위석 원문의 말투·종결어미·문장 호흡·고유 문장·비유는 사용하지 않는다. 업체명·지역·원장·경력·환자 수·성과·프로그램·장비·사진·연락처도 가져오지 않는다.
8. 모든 완성 문장은 `assets/goldhand-official-voice-profile.json`과 `references/goldhand-official-voice.md`의 박준희 원장 말투로 새로 쓴다. 의료 답은 검토된 일반 정보, 금손 최신 사실, 필요한 권위 자료가 결정한다.
9. 꾸밈은 편집 마스터와 무관하게 `goldhand-naver-native-v4`로 고정한다. 네이버 순정 인용구·구분선·표1 외의 CSS 카드, 둥근 박스, 그림자, 왼쪽·위쪽 강조선, 1행×1열 가짜 표는 쓰지 않는다.
10. 인용구 2~3개는 실제 환자 발화라고 주장하지 않는다. 확인된 직접 인용이 아니라 검색 독자를 대표하는 고민으로 쓴다.
11. 기본 화자는 박준희 원장이다. `안녕하세요, 금손한의원 박준희 원장입니다.`를 정확히 한 번 쓴다. 인용구 2~3개를 이 인사 앞이나 뒤에 둔다.
12. 이모지, `^^`, `ㅎㅎ`, `ㅠㅠ`, 하트, 해시태그 장식, 강한 내원 유도, 치료 보장을 쓰지 않는다.
13. 예시 금지어만 피해 비슷한 문장으로 바꾸지 않는다. `조금 더 분명히 구분할 수 있습니다`, `차분히 살펴보겠습니다`, `구체적인 단서가 될 수 있습니다`를 포함해 번역투 명령문, 독자에게 기록·관찰·정리를 숙제처럼 시키는 문장, 감성적 여운을 위한 추상 결론을 만드는 생성 방식 자체를 쓰지 않는다. `판단·기준·구분·확인`은 실제 동작보다 많이 반복하지 않는다.
14. 문법적으로 자연스러운 것만으로 통과시키지 않는다. 지나치게 완곡하게 돌려 말하는 안내, 독자에게 교훈을 주거나 여운을 남기는 결말, 실제 대화보다 블로그 작문을 위해 만든 티가 나는 문장도 실패다. 말투를 부드럽게 만들려고 의미를 흐리지 말고 필요한 내용은 단정적이고 명확하게 말한다.
15. 완성물은 항상 `제목 + 본문 + 네이버 복사용 HTML`이다. 사용자가 HTML을 명시적으로 제외한 경우에만 파일을 생략한다.
16. 인용구·인사·해결 방향·소제목·일반 본문·표를 포함한 모든 글은 중앙 정렬한다. 왼쪽 정렬을 섞지 않는다.
17. 핵심 결론에는 노란 하이라이트 정확히 3개, 실제로 필요한 구체적 행동에는 네이버 순정 밑줄 2~3개, 중단·검사·주의 같은 안전 경계에는 빨간 글씨 1~2개를 넣되 합계는 6~8개다. 밑줄 개수를 맞추려고 기록·관찰·회상 숙제를 만들지 않는다.
18. 가치입증은 후보나 주제별 선택이 아니다. `assets/goldhand-value-proof-library.json`의 고정 6행을 모든 글에서 같은 문구·순서로 사용한다.
19. `금손한의원 소개` 가치입증 표는 모든 글에서 도입 질문·인사·`solution-preview`가 모두 끝난 직후, 첫 정보 본문의 구분선·소제목·설명보다 앞에 둔다.
20. 제목에는 확인된 업체 실적을 꾸며 넣지 않는다. 대신 본문에서 실제로 서로 다른 답을 설명하는 개수를 `2가지`, `3가지`처럼 숫자로 약속하고 같은 개수의 번호 소제목으로 답한다.
21. `solution-preview` 안에는 `data-reference-role="reading-time-hook" data-reading-minutes="3"` 문단을 정확히 한 번 둔다. `팔이 잘 안 올라간다면, 딱 3분만 읽어 보세요.`처럼 짧고 직접적으로 말하며 레퍼런스 문장을 그대로 복사하지 않는다.
22. 도입에서 오십견 핵심 또는 독자의 불편을 설명하는 한 구절을 노란색으로 표시한다. 노란 하이라이트 3개 가운데 1개는 반드시 `solution-preview`에, 나머지 2개는 서로 다른 본문 구간에 둔다.
23. 시각 자료는 사용자가 본인 소유라고 확인한 [네이버 OGQ마켓 callilife](https://ogqmarket.naver.com/creators/callilife?type=STOCK_IMAGE)에서 주제와 직접 맞는 작품 1~3개를 찾는다. 작품마다 내장 GPT Image를 별도로 호출한다. 인물 중심 그림은 동작·자세·구도·화살표·각도·표기·그림체를 유지하고 얼굴형·이목구비·헤어·피부색·의상 색이나 디테일 가운데 2~3개만 미세하게 바꾼다. 비인물 중심 그림은 핵심 사물·정보·구도·표기를 유지하고 선 굵기·채색·명암·질감 가운데 1~2개만 살짝 바꾼다.
24. 원고 article에는 OGQ 미리보기나 원본을 넣지 않고 GPT Image 생성본의 절대 로컬 경로만 넣는다. 빌드할 때는 생성본을 금손 전용 HTTPS 이미지 호스트에 게시하고, 청년통신 복사 페이지와 동일하게 공개 HTTPS 주소를 `<img src>`와 `data-reference-source-url`에 넣는다. 네이버가 제외하는 `data:image/...;base64`는 만들지 않는다. 실제 사진과 GPT 이미지 모두 `<figcaption>`이나 이미지 아래 설명 문단을 만들지 않는다. 작품 상세 URL·사용자 소유 확인·의학 정보 및 배치 보존·허용된 변형 모드는 보이지 않는 검수용 `data-*`와 `alt`에만 남기며 네이버 복사 본문에서는 내부 `data-*`를 제거한다. 인물 중심 그림의 그림체 변경, 비인물 중심 그림의 내용·배치 변경은 실패다. 구매·가격 확인·라이선스 요청 단계는 없다.
25. 생성한 이미지는 별도 첨부로 끝내지 않고 최종 `<article>`과 네이버 복사용 HTML 안에 반드시 삽입한다. 각 이미지는 그 그림이 직접 설명하는 증상·동작·치료 원칙을 적은 모바일 문단 바로 뒤에 한 장씩 둔다. 도입과 본문 사이, 소제목 직후, 관련 없는 문단 뒤, 글 끝에 여러 장을 몰아넣는 배치는 금지한다. `<figure>`에는 `data-image-placement="after-related-paragraph"`와 직전 문단에서 실제로 확인되는 `data-image-anchor`를 둔다.
26. GPT Image 1~3장과 별도로 실제 금손한의원 사진을 매 글 6~12장 넣는다. 공식 블로그에서 수집한 113장 전부는 플러그인 `assets/official-media`에 들어 있으며, `assets/media-library.json`에서 `safeAuto: true`와 번들 파일·해시가 확인된 사진만 자동 선택한다. 사용자 바탕화면이나 개인별 사진 폴더를 요구하지 않는다.
27. 실제 사진은 `원장이 환자를 치료하는 장면 → 원장이 환자를 진찰·상담·설명하는 장면 → 그 밖의 사람 대 사람 진료 장면 → 주제 일치 치료 사진 → 치료 재료·한약·원내 공간` 순으로 선택한다. 로고·건물·약·장비·공간은 안전한 사람 중심 장면만으로 수량을 채울 수 없을 때만 fallback으로 쓴다. 최근 3개 글에서 쓴 ID·파일 해시는 먼저 제외한다. 새 안전 사진이 6장보다 적을 때만 최근의 안전한 신뢰 사진을 재사용해 최소 6장을 맞추고, 6장 이상이면 최근 사진으로 목표 수량을 더 채우지 않는다.
28. 환자·가족 얼굴, 이름, 연락처, 차트, 처방전, 검사결과가 식별되거나 시각 검수를 통과하지 않은 내장 사진은 어떤 경우에도 사용하지 않는다. 번들에 저장돼 있다는 사실만으로 자동 사용 승인이 되지 않는다. 안전한 사진을 최근 재사용해도 6장이 안 되면 무관하거나 위험한 사진을 넣지 않고 발행을 중단한다.

## 필요한 자료만 읽기

- 금손 사실·운영·진료 태도: [references/clinic-facts.md](references/clinic-facts.md)
- 단일 글 구조와 문장 역할: [references/content-formulas.md](references/content-formulas.md)
- 주제·일반 정보·내용 순서: [references/wipark-content-source-policy.md](references/wipark-content-source-policy.md), `assets/wipark-content-briefs.json`, [references/reference-master-library.md](references/reference-master-library.md)
- 금손 공식 말투: [references/goldhand-official-voice.md](references/goldhand-official-voice.md), `assets/goldhand-official-voice-profile.json`
- 레퍼런스 역할·복사 거리 대조: [references/reference-exact-reconstruction.md](references/reference-exact-reconstruction.md)
- 치료·인증·수치·의학 표현: [references/medical-writing-guardrails.md](references/medical-writing-guardrails.md)
- 모바일 문단·네이버 순정 꾸밈: [references/mobile-readability-and-brand-boxes.md](references/mobile-readability-and-brand-boxes.md), `assets/goldhand-naver-native-design-system.json`
- 고정 가치입증 6행: `assets/goldhand-value-proof-library.json`을 그대로 사용하며 선택·교체·순서 변경 금지
- HTML·이미지: [references/visual-and-media.md](references/visual-and-media.md)
- 사용자 소유 callilife 작품 후보·GPT 재현 상태: `assets/callilife-ogq-media-library.json`
- 모드·검수·저장: [references/workflow-and-output.md](references/workflow-and-output.md)
- 금손 공식 글 조사 범위·이미지: [references/official-blog-inventory.md](references/official-blog-inventory.md)

## 실행 모드

사용자가 모드를 말하지 않았다면 다른 질문을 섞지 말고 다음 한 문장만 묻는다.

`1. 자동모드  2. 정밀작성모드`

이미 모드가 명시되면 반복하지 않는다.

### 자동모드

메인키워드가 없으면 `메인키워드를 입력해 주세요.`만 출력한다.

메인키워드를 받으면 추가 확인 없이 끝까지 진행한다.

1. 입력한 메인키워드의 띄어쓰기와 표기를 정확히 고정한다.
2. `scripts/select_wipark_content_reference.py`로 본문 검토 완료 위석 정보글 11편 중 한 편을 고른다. 최근 3개와 같은 레퍼런스·핵심 대상·검색 의도는 후보에서 제외하며 새 후보가 없으면 중복으로 되돌아가지 않는다.
3. `광주 한의원`, `광주 한의원 추천`처럼 포괄적인 지역·업종 키워드는 SEO 앵커일 뿐 글의 주제가 아니다. 선택된 위석 글의 실제 건강 문제를 주제로 쓴다.
4. 선택 결과의 `topic`, `readerConcerns`, `orderedGeneralInformation`, `blockedFromSource`를 한 묶음으로 고정한다. 제목만 빌리고 다른 내용을 쓰거나 여러 글의 내용을 섞지 않는다.
5. 위석 원문 말투를 지운다. `sourceToneBlocked=true`와 `voiceProfileId=goldhand-official-voice-v1`을 확인한 뒤에만 초안을 쓴다.
6. `원문 일반 정보 → 금손의 새 설명` 대응표를 만든다. 원문 문장·업체 사실·프로그램·사례·수치·사진·종결어미는 대응값으로 쓰지 않는다.
7. 본문 답 개수를 정하고 그 숫자를 제목에 넣은 뒤 `scripts/validate_title.py --editorial-close --answer-count N`으로 검사한다. 레퍼런스의 환자 수·경력·성과 숫자는 가져오지 않는다.
8. `orderedGeneralInformation`과 같은 순서로 쓰되, 모든 문장은 금손 공식 말투로 새로 쓴다. 도입에 3분 읽기 안내와 핵심 하이라이트를 넣고 정확 키워드를 본문 2~3회만 넣은 뒤 모바일 줄바꿈과 순정 꾸밈을 후처리한다.
9. callilife에서 주제에 맞는 작품 1~3개를 고르고 작품 상세 미리보기를 생성 레퍼런스로 확보한다. 각 작품이 인물 중심인지 비인물 중심인지 먼저 분류한다. 인물 중심이면 표현·그림체를 유지하고 인물만 미세하게 바꾸며, 비인물 중심이면 내용·배치를 유지하고 그림체만 미세하게 바꾼다. 생성본만 로컬에 저장하고, 각 생성본이 설명하는 핵심 단어가 실제로 들어간 모바일 문단 바로 뒤에 한 장씩 삽입한다. 생성만 하고 HTML에서 누락하거나 글 끝에 모아 두지 않는다. 구매·가격·라이선스 선택은 묻지 않는다.
10. `recommend_media.py --count 8`로 플러그인 내장 라이브러리에서 실제 사진을 고른다. `bundledPath`·SHA256·공식 원본 URL이 모두 일치하고 시각 검수 승인된 사진만 후보로 삼는다. 주제 일치 새 사진과 새 신뢰 사진으로 6~12장을 먼저 만들고, 6장 미만일 때만 최근 3개 글의 안전한 신뢰 사진을 최소 6장까지 재사용한다.
11. 실제 사진과 GPT Image를 각각 관련 모바일 문단 바로 뒤에 한 장씩 분산한다. 실제 사진은 `data-real-photo="true"`, 정확한 origin·ID 또는 해시를 표시하되 화면에 보이는 캡션은 만들지 않는다. 생성본과 실제 사진을 연속으로 몰아넣지 않는다.
12. `validate_reference_reconstruction.py --editorial-close`, `validate_copy_overlap.py`, `validate_goldhand_voice.py`, `validate_article.py --editorial-close`를 모두 통과한 원고만 완성한다. 최근 3개 이력에는 선택한 위석 레퍼런스와 의미 주제뿐 아니라 실제 사진 ID·파일 해시도 기록한다.
13. 제목의 실제 답을 만들 필수 사실이 없을 때만 필요한 값 하나를 짧게 묻는다. 다른 유형으로 대체하지 않는다.

자동모드 완성 글은 지역명·상호·운영정보를 가려도 독자가 가져갈 수 있는 원인 설명, 자가 점검, 생활관리, 치료·검사 판단이 남아야 한다. `한의원 고르는 법`, `추천하는 이유`, `선택 기준`, `잘하는 곳의 조건`처럼 업체 선택을 본문 주제로 삼지 않는다. 포괄 키워드를 받았다는 이유로 업체소개형이나 병원 비교형으로 전환하지 않는다.

자동모드의 정보 주제는 증상형에만 고정하지 않는다. 주제 후보가 치료 적용·중단·시기·주의를 묻는 글이면, 금손에서 실제 사용하는 치료 또는 독자가 이미 사용 중이라고 가정할 수 없는 일반 의료 주제를 중심으로 `무엇을 위한 치료인가 → 어떤 상태를 먼저 구분하는가 → 언제 고려하는가 → 치료만으로 부족할 수 있는 조건 → 다른 검사·치료가 먼저인 경계`를 설명한다. 추나요법의 적용 기준·치료 뒤 관리뿐 아니라 위고비·마운자로 사용 중단 뒤 체중관리처럼 독자 판단에 실제 도움이 되는 주제도 포함할 수 있다. 다만 금손한의원이 해당 약을 처방하거나 특정 장비·프로그램을 제공한다고 쓰지 않는다. 최근 글이 한 축에 치우쳤다면 가능한 범위에서 다른 핵심 대상과 검색 의도로 회전한다.

### 정밀작성모드

한 번에 하나만 질문하며 이미 답한 값은 다시 묻지 않는다.

1. 메인키워드
2. `select_wipark_content_reference.py --count 3`으로 최근 3개와 겹치지 않는 주제 후보 3개를 고른다. 각 후보에는 주제·핵심 내용·정보 순서를 가져올 `콘텐츠 레퍼런스` 링크 한 편을 표시한다. 말투는 후보와 무관하게 금손 공식 말투로 고정한다.
3. 후보 중 최종 제목
4. 글에 추가할 사실·원장 판단·실제 장면. 없으면 내장 사실만 사용
5. 플러그인 `assets/official-media`의 공식 블로그 내장 사진 가운데 시각 검수 승인 사진을 자동 사용한다. 이미지 방식이나 사용자 로컬 폴더는 묻지 않는다.

글 유형은 묻지 않는다. 항상 정보형이다. 확정한 원문 한 편에서 주제·질문·핵심 내용·정보 순서만 가져오고 실제 문장과 말투는 금손 공식 글 기준으로 새로 쓴다. 꾸밈은 네이버 순정 시스템을 쓴다.

## 제목 계약

- 정확 메인키워드는 제목에 한 번만 넣고 가능한 앞부분에 자연스럽게 둔다.
- 공백 제외 22~40자를 권장하고 50자를 넘으면 발행하지 않는다.
- 제목은 본문이 실제로 답할 구체적인 원인·기준·주의점·시기·원칙을 약속한다.
- 제목에는 숫자 후킹을 하나 둔다. 기본값은 본문에서 실제로 설명하는 `2가지` 또는 `3가지`이며 같은 개수의 번호 소제목으로 답한다.
- 레퍼런스의 `29,000명` 같은 환자 수·성과 수치는 가져오지 않는다. 금손에서 확인된 실적 수치가 없다면 답 개수 외의 성과 숫자를 만들지 않는다.
- `11년차`는 원장 경력에만 연결한다. 누적환자, 누적추나, 만족도, 재방문율, 지역 1위는 쓰지 않는다.
- 레퍼런스 제목의 흔한 검색 표현과 질문형·이유형 문법은 유지할 수 있다. 경력·수치·업체명·지역·치료 성과·고유 프로그램은 금손 표현으로 바꾸어 옮기지 않는다.
- `살이 안 빠진다`처럼 사람이 흔히 쓰는 말을 표절 회피 목적으로 `체중이 그대로라면 먼저 볼 기록` 같은 추상어로 치환하지 않는다.
- 후보마다 독자가 얻을 판단을 한 문장으로 답할 수 없으면 폐기한다.
- 포괄적인 지역·업종 키워드가 들어와도 제목의 실제 약속은 구체적인 증상·원인·생활 조건 또는 특정 치료의 원리·적용 기준·효과가 더딘 조건·주의점이어야 한다. 한의원 자체를 고르는 법이나 추천 이유를 제목의 답으로 삼지 않는다.
- 최종 제목은 `scripts/validate_title.py`를 통과시킨다.

## 작성 순서

아래 단계의 작업 흐름은 유지하되 내용은 모두 금손 계약으로 수행한다.

1. **단일 콘텐츠 레퍼런스 선택**: 최근 3개와 겹치지 않는 검토 완료 위석 정보글 한 편을 고정한다.
2. **내용 지도 작성**: 주제, 독자 고민, 핵심 일반 정보, 정보 공개 순서만 적는다. 위석 말투·문장·고유 사실은 적지 않는다.
3. **사실 팩 작성**: 금손 사실, 권위 있는 일반 의학 설명, 예외, 자가관리, 금지 주장을 분리한다. 의료 답은 원문이 아니라 이 사실 팩에서만 가져온다.
4. **제목 생성·검증**: 실제 답 개수를 정하고 숫자 약속을 제목에 담아 `--editorial-close --answer-count N`으로 검사한다.
5. **도입 작성**: 선택 글의 독자 고민을 금손 맥락으로 바꿔 2~3개와 해결 방향 예고를 배치한다. 공감 또는 핵심 문구 한 곳을 노란색으로 강조하고 3분 읽기 안내를 짧게 덧붙인다.
6. **1:1 내용 대응표 작성**: `orderedGeneralInformation` 각 항목에 금손 사실과 필요한 일반 의학 설명을 대응한다.
7. **금손 말투 초안 작성**: `제가·저는·저도`, 독자 질문, 구체적 생활 장면, `사실·그런데·하지만·그래서`, `~죠·~거든요·~세요`를 억지 없이 섞는다. 위석 말투는 쓰지 않는다.
8. **진료실 발화 가능성 검사**: 문장마다 `박준희 원장이 환자를 앞에 두고 실제로 이렇게 말할까?`를 묻는다. 입으로 말하면 어색한 번역투·작문체·감성 문장은 의미를 유지한 채 짧고 직접적인 한국어 구어체로 다시 쓴다. 안전 경계는 `혼자 판단해서 운동을 계속하시면 안 됩니다`처럼 분명하게 말하고, 관찰 정보가 필요하면 `어떤 동작에서 다시 아픈지 진료할 때 말씀해 주세요`처럼 실제 진료 행동으로 연결한다.
9. **독립 검수**: 제목, 사실 팩, 선택 콘텐츠 브리프, 금손 말투 프로필, 초안만 새 패스에서 읽는다. 특정 금지 문구뿐 아니라 같은 생성 원리에서 나온 문장군을 찾는다.
10. **부분 수정**: 실패 문장과 필요한 앞뒤 문장만 고친다.
11. **SEO·모바일·이미지·순정 컴포넌트·HTML 후처리**: 자연스러운 글을 먼저 완성한 뒤 정확 키워드를 2~3회 넣고, 완성 문장의 표현을 바꾸지 않은 채 모바일 시각 줄로 나눈다. GPT Image 생성본 1~3장과 플러그인 내장 승인 실제 사진 6~12장을 관련 문단 뒤에 한 장씩 분산한다. 실제 사진은 새 사진 우선이며, 새 안전 사진이 6장 미만일 때만 최근 신뢰 사진을 최소 수량까지 재사용한다. 모든 글을 중앙 정렬하고 필요한 순정 컴포넌트를 배치한다.
12. **발행 게이트·이력 기록**: 내용 순서, 금손 말투, 진료실 발화 가능성, 원문 문장 중복, 의료·업체 사실, 실제 사진 6~12장과 GPT Image 1~3장, HTML을 검사한 뒤 제목·키워드·주제·콘텐츠 레퍼런스·실제 사진 ID·해시를 최근 3개 이력에 기록한다.

## 본문과 SEO 계약

- 제목과 실제 본문을 합쳐 공백 제외 1,400~1,800자다.
- 정확 메인키워드는 제목 1회, 일반 본문 2회 또는 3회다.
- 표, 이미지 `alt`, 고정 운영정보, 연락처, CTA는 키워드 횟수에서 제외한다.
- 한 문단에는 정확 키워드를 한 번만 쓰며 도입·중반·후반 중 자연스러운 2~3곳에 분산한다.
- 키워드 수를 맞추려고 의미 없는 문장이나 요약 블록을 덧붙이지 않는다.
- 일반 본문은 `data-mobile-group="true"` 한 묶음에 시각 줄 2개 또는 3개를 두고 `<br>`로 나눈다.
- 한 시각 줄은 공백 제외 10~20자를 목표로 하고 4~24자를 벗어나지 않는다. 글자 수보다 조사·체언·서술어가 어색하게 끊기지 않는 것이 우선이다.
- 모든 일반 본문 묶음 뒤에 `data-preview-gap="true"` 빈 줄을 한 개 둔다.
- 모든 일반 본문과 고정 인사도 `text-align:center`로 출력한다.
- 노란 하이라이트는 `<span data-goldhand-emphasis="highlight" style="background-color:#FFF2A8;">짧은 핵심 결론</span>`, 밑줄은 `<u data-reference-underline-role="key-point">짧은 행동 기준</u>`, 빨간 글씨는 `<span data-goldhand-emphasis="red" style="color:#E53935;font-weight:700;">짧은 안전 경계</span>`만 사용한다.
- 노란 하이라이트는 3개를 사용한다. 1개는 도입의 공감·핵심 문구, 2개는 서로 떨어진 본문 핵심 문구에 둔다.
- 도입의 3분 안내는 구조 숫자이므로 의료 성과 수치가 아니다. `3분만 집중해서 읽어 보시길 권합니다`를 그대로 복사하지 말고 금손 말투로 짧게 다시 쓴다.
- 빨간 글씨는 중단·검사·주의 같은 안전 경계에만 쓰고 치료 효과, 가치입증, 예약 유도에는 쓰지 않는다.
- 같은 증상도 원인이 다를 수 있음을 설명하고, 필요하면 다른 검사·기관을 먼저 권하는 경계를 함께 쓴다.
- 시술명을 나열하기 전에 왜 반복되는지, 무엇을 구분하는지, 집에서 무엇을 살필지 설명한다.
- 독자에게 무언가를 시킬 때는 실제 치료·안전·진료에 필요한 행동만 말한다. `스스로 운동을 이어가지 마세요`처럼 번역한 듯 완곡하게 말하지 않고 `혼자 판단해서 운동을 계속하시면 안 됩니다`처럼 바로 알아듣게 쓴다.
- `다시 아파지는 순간을 적어보세요. 그게 다음 실마리가 됩니다`처럼 기록을 권한 뒤 추상적 보상을 붙이지 않는다. 정보가 필요하면 `언제, 어떤 동작에서 다시 아픈지 진료할 때 말씀해 주세요`처럼 왜 필요한지 드러나는 실제 말로 바꾼다.
- 문단마다 독자에게 `적어 보세요·떠올려 보세요·살펴보세요`라고 숙제를 주지 않는다. 꼭 기록이 필요한 주제라도 기록 방법과 사용 목적이 구체적일 때만 한 번 설명한다.
- 합성 환자 사례, 허위 직접 인용, 근거 없는 수치, 결과 보장을 만들지 않는다.
- 강한 예약 유도 대신 필요한 경우 현재 상태를 의료진과 상의해도 좋다는 정도로 끝낸다.

## 이미지와 HTML 계약

- 의료 개념·동작 설명 이미지는 사용자 소유 callilife OGQ 작품을 레퍼런스로 우선한다. `assets/callilife-ogq-media-library.json`에서 주제와 직접 연결된 작품 1~3개를 고르고 `safeAuto=true`와 `ownershipBasis=user-confirmed-2026-08-21`을 확인한다.
- 작품 미리보기는 GPT Image 입력에만 사용한다. 최종 원고에는 `data-media-provider="gpt-image"`, 생성본 `data-local-image`, callilife 작품 상세 URL, `data-generation-owner-authorization="user-confirmed"`, `data-generation-content-preservation="medical-information-layout"`, 그리고 `data-generation-variation-mode="person-identity-subtle-variation"` 또는 `nonperson-style-subtle-variation`을 가진 이미지 1~3개만 넣는다.
- 각 GPT Image `<figure>`에는 `data-image-placement="after-related-paragraph"`와 `data-image-anchor="핵심어1|핵심어2"`를 둔다. 직전의 `data-mobile-group="true"` 문단에는 anchor 가운데 하나가 실제로 있어야 한다. 생성본은 이 figure로 최종 article에 들어가야 하며 별도 파일 링크만 전달하면 실패다.
- `build_naver_copy_page.py`는 `~/.codex/state/goldhand-clinic-blog/image-host.json`의 금손 전용 호스트 설정을 읽어 로컬 생성본을 콘텐츠 해시 파일명으로 게시한다. 게시된 각 URL이 HTTP 200·이미지 MIME인지 확인한 뒤에만 HTML을 저장하며, 게시 실패 시 base64로 우회하지 않고 빌드를 중단한다.
- GPT Image와 별도로 실제 금손 사진 6~12장을 항상 사용한다. `scripts/recommend_media.py`가 플러그인 `assets/official-media` 내장본 중 `safeAuto: true`이며 파일·해시·원본 URL이 모두 일치하는 사진만 선택한다.
- 실제 사진은 `personInteraction: true`이면서 `sceneType`이 원장-환자 치료·진찰·상담으로 검수된 장면을 가장 먼저 사용한다. 안전한 사람 중심 장면이 부족할 때만 주제 일치 사물 사진과 약·장비·원내 공간을 fallback으로 쓴다.
- 실제 사진과 GPT 이미지 모두 이미지 아래에 보이는 설명, 출처, `AI 생성 이미지`, 장면 이름을 쓰지 않는다. `<figcaption>`이 하나라도 있으면 발행하지 않는다. 장면 의미와 출처는 `alt`와 검수용 `data-*`로만 관리한다.
- 최근 3개 글의 실제 사진 ID·해시는 새 사진 선택에서 제외한다. 새 안전 사진이 6장보다 적을 때만 최근 신뢰 사진을 최소 6장까지 재사용한다. 이미 6장 이상이면 최근 사진으로 8장·10장 같은 선호 수량을 채우지 않는다.
- 최근 신뢰 사진까지 써도 6장이 안 되면 무관한 이미지·미검수 이미지·개인정보 위험 이미지로 채우지 않고 발행을 중단한다.
- 식별 가능한 환자·가족 얼굴, 이름, 차트, 연락처가 보이는 공식 이미지는 자동 사용하지 않는다.
- 선택한 위석 블로그 본문의 사진 URL은 복사하지 않는다. 필요한 시각 자료는 callilife 본인 작품 목록에서 별도로 찾고 GPT Image로 재생성한다.
- `<article>` 안에는 제목 `h1`, 영문 브랜드 띠, 고정 원장 카드가 없어야 한다.
- `<article>`에는 `data-goldhand-type="정보전달형"`, `data-editorial-mode="content-reference-goldhand-voice"`, 선택한 한 편의 `data-editorial-master-id`, `data-content-reference-source`, `data-editorial-reference-source`, `data-editorial-source-role="topic-reader-concerns-general-information-sequence-only"`, `data-goldhand-voice-profile="goldhand-official-voice-v1"`를 둔다. 레퍼런스는 말투를 통제하지 않는다.
- `<article>`에 `data-goldhand-design-system="goldhand-naver-native-v4"`을 정확히 한 번 둔다. `data-decoration-master-reference-id`는 레퍼런스의 논리 배치 대조용일 뿐 꾸밈을 바꾸지 않는다.
- 독자 고민 2~3개는 각각 `<blockquote data-reference-role="reader-question" data-question-source="representative-reader-concern" data-naver-native-component="quotation" style="text-align:center;">`로 만든다. blockquote에는 중앙 정렬 외의 배경·테두리·padding 스타일을 넣지 않는다.
- 해결 방향 예고는 `data-reference-role="solution-preview"`가 붙은 무배경 산문 블록을 정확히 한 번 둔다.
- 소제목은 `h2` 또는 `p`에 `data-reference-role="section-heading" data-naver-native-component="subheading"`을 두고, 앞뒤에 필요한 네이버 순정 `<hr data-naver-native-component="divider">`를 사용한다.
- 표는 실제 행·열 관계가 있는 정보에만 쓰고, 세 표 모두 `data-naver-native-component="table" data-native-table-preset="naver-table1-default"`를 둔다. 표 자체는 `width:100%;border-collapse:collapse;margin-left:auto;margin-right:auto`로 중앙 배치한다.
- 모든 `td`·`th`에 `border:1px solid #D6D6D6;text-align:center;vertical-align:middle`을 빠짐없이 적용한다. 표 안의 라벨·설명·운영정보도 예외 없이 가로·세로 중앙 정렬한다.
- `credential` 가치입증 표를 정확히 한 번 둔다. 첫 행은 “금손한의원 소개” 골드 제목 한 칸, 다음 6행은 `assets/goldhand-value-proof-library.json`의 짧은 경력·강점 문구를 같은 순서로 넣는다. 후보 선택, 주제별 교체, 문장 확장은 금지한다. 위치는 완성된 `solution-preview` 직후이자 첫 `divider`·`section-heading`·정보 설명 문단 직전으로 고정한다.
- `article-summary` 정보표는 행·열 비교가 산문보다 분명할 때만 한 번 둔다. 사용한다면 2열 이상이며 첫 행만 금손 골드 셀 배경과 흰 글자를 쓴다. 고정 운영정보는 `clinic-info` 2열 표로 마지막에 정확히 한 번 두며, 모든 셀에 `width:50%;height:64px;line-height:1.8;word-break:keep-all`을 넣어 좌우 50:50과 중앙 정렬을 고정한다.
- 가치입증처럼 실제 여러 사실을 한 행씩 구분하는 1열 다행 표는 허용한다. 1행×1열 가짜 표, 등록되지 않은 가치입증 문구, 표와 산문의 장황한 중복은 금지한다.
- `data-goldhand-box`, `border-radius`, `box-shadow`, 표 밖의 `border`·임의 왼쪽/위쪽 선·배경색을 쓰지 않는다. `border`는 순정 표의 셀 구분선에만 허용한다.
- 선택 원문의 다른 역할에는 `data-reference-role`을 붙이고 네이버 내부 `se-*` 클래스는 복사하지 않는다. 복사 단계에서는 내부 `data-*`를 제거하고 순정 구조 태그만 네이버로 보낸다.
- 기본 저장 폴더는 `~/Desktop/금손한의원 블로그`, 파일명은 `금손한의원_{제목}.html`이며 충돌 시 `_2`, `_3`을 붙인다.

## 고정 운영정보

고유 결론 뒤에 부담 없는 문의 안내와 아래 정보를 한 번만 둔다. 이 블록은 일반 본문 SEO 횟수 계산에서 제외한다.

- 금손한의원
- 전남광주통합특별시 서구 유림로98번길 3, 2층
- 동천파출소·동천동 행정복지센터 건너편
- 전화 062-515-7582
- 카카오톡에서 `@금손한의원` 검색 후 채널 문의
- 네이버에서 `금손한의원` 검색 후 진료 예약
- 월·수·금 09:30~20:00
- 화·목 09:30~18:00
- 토·일 09:00~13:00
- 공휴일 09:30~18:00
- 설·추석 연휴 휴진

`365일 진료`를 단독으로 쓰지 않는다. 카카오 채널을 비대면 진료·치료로 표현하지 않는다. 임시휴진·원장 휴가는 고정 블록에 넣지 않는다.

## 검증 명령

```bash
python3 scripts/select_wipark_content_reference.py --keyword "정확 메인키워드" --topic "희망 주제"
python3 scripts/validate_title.py --title "확정 제목" --keyword "정확 메인키워드" --editorial-close --json
python3 scripts/validate_article.py --input article.html --title "확정 제목" --keyword "정확 메인키워드" --editorial-close
python3 scripts/validate_reference_reconstruction.py --input article.html --profile "선택한 INFO 마스터 ID" --editorial-close
python3 scripts/validate_goldhand_voice.py --input article.html --json
python3 scripts/validate_copy_overlap.py --input article.html --source-text "원문 추출 텍스트"
python3 scripts/sync_official_media_assets.py --verify-only
python3 scripts/recommend_media.py --topic "확정 주제" --keyword "정확 메인키워드" --type "정보전달형" --count 8 --json
python3 scripts/build_naver_copy_page.py --title "확정 제목" --article-html article.html
python3 scripts/validate_html.py --input "생성된 HTML 경로"
python3 scripts/record_article_state.py --title "확정 제목" --keyword "정확 메인키워드" --topic-source-id "선택 INFO ID" --topic-source-title "콘텐츠 레퍼런스 제목" --topic-source-url "콘텐츠 레퍼런스 URL" --topic-source-blog-id "wi-parkclinic" --topic-source-role "topic-reader-concerns-general-information-sequence-only" --topic-idea "선택 주제" --writing-master-id "선택 INFO ID" --writing-reference-url "콘텐츠 레퍼런스 URL" --editorial-master-id "선택 INFO ID" --editorial-reference-title "콘텐츠 레퍼런스 제목" --editorial-reference-url "콘텐츠 레퍼런스 URL" --editorial-source-role "topic-reader-concerns-general-information-sequence-only" --editorial-profile-status "ready" --real-media-id "GH0001" --real-media-hash "로컬 파일 SHA256" --type "정보전달형"
```

모든 제목의 숫자 약속에 `validate_title.py --answer-count N`을 사용한다. 하나라도 실패하면 완성본처럼 제시하지 않는다.

## 발행 차단 조건

- 독자 고민 인용이 선택 원문의 실제 고민과 다르거나 2~3개 범위를 벗어남
- 인용 고민들이 제목과 연결되지 않거나 같은 뜻을 반복함
- 해결 방향 예고가 없거나 첫 정보 본문 뒤에 나옴
- 최근 3개 글 중 하나와 `semanticTopicId` 또는 핵심 대상이 같거나, 같은 대상·검색 의도 또는 동의어 키가 겹치는 주제
- 선택한 위석 한 편과 다른 글의 주제·독자 고민·핵심 내용·정보 순서를 혼합함
- 선택 레퍼런스의 `orderedGeneralInformation`을 빼거나 순서를 임의로 뒤섞음
- 위석 말투·종결어미·고유 문장·질문·사례·비유를 복사하거나 7어절 이상 연속 일치함
- `goldhand-official-voice-v1` 누락, 1인칭·대화형 종결·솔직한 연결·생활 장면 부족
- `ㅎㅎ`, `ㅠㅠ`, `^^`, 이모지 또는 등록된 AI 템플릿 문장 사용
- 실제 원장이 환자에게 입으로 말하지 않을 번역투 명령문, 독자 숙제형 행동 유도, 감성적·은유적 결론, 추상 명사로 마무리하는 작문체 사용
- 예시 문구만 다른 단어로 치환하고 `기록·관찰·회상 권유 → 실마리·단서·출발점·첫걸음 같은 추상 보상` 구조를 그대로 유지함
- 필요한 지시를 `~하는 편이 좋습니다`, `~해 보셔도 좋습니다`, `하나의 방법입니다`처럼 지나치게 완곡하게 만들어 환자가 무엇을 해야 하는지 흐림
- `이번 글에서는`, `이 글을 통해`, `함께 살펴보겠습니다`처럼 실제 진료 대화가 아니라 블로그 형식을 설명하는 문장으로 내용을 시작하거나 끝냄
- `기억해 주세요`, `잊지 마세요`, `도움이 되었으면 합니다`처럼 교훈·다짐·여운을 만들기 위한 결말
- 레퍼런스 업체명·프로그램·경력·성과·고유 수치·사진·연락처를 옮김
- 업체소개형·사례공유형·스토리텔링형·일상글·공지
- 레퍼런스 업체 사실·문장·사례·사진·연락처 혼입
- 금손 사실과 사용자 최신 정정 위반
- 합성 사례·허위 환자 발화·효과 보장·강한 내원 유도
- 제목 약속과 실제 답 불일치
- 제목에 실제 답 개수 숫자가 없거나, 숫자와 번호 소제목 개수가 다름
- `solution-preview`의 3분 읽기 안내 또는 도입 하이라이트 누락
- callilife 주제 일치 작품 검색 누락, GPT Image 생성본 1~3개 누락, OGQ 미리보기·원본을 완성 글에 직접 사용, 생성본 절대 경로·작품 상세 URL·사용자 소유 확인·의학 정보 및 배치 보존·허용 변형 모드 누락, 인물 중심 그림의 그림체를 바꾸거나 비인물 중심 그림의 핵심 내용·배치를 바꿈
- GPT Image 생성본을 최종 article·복사용 HTML에서 누락하거나, 복사용 HTML에 HTTPS 게시 URL 대신 로컬 경로·`data:image`를 남기거나, `data-image-placement`·`data-image-anchor` 없이 소제목 직후·관련 없는 문단 뒤·글 끝에 몰아서 배치함
- 실제 금손 사진이 6장 미만 또는 12장 초과, 안전한 원장-환자 치료·진찰·상담 장면이 있는데 로고·건물·약·장비·공간을 먼저 사용, 최근 3개 사진을 새 안전 사진보다 먼저 사용, 새 사진이 6장 이상인데 최근 사진으로 더 채움, 실제 사진 ID·해시·시각 검수·관련 문단 배치 누락
- 실제 사진이나 GPT 이미지 아래에 `<figcaption>` 또는 별도 설명·출처 문단을 표시함
- 지역·업종 키워드를 글의 주제로 오인해 한의원 선택법·추천 이유·업체 비교를 설명하거나, 지역명·상호를 가렸을 때 실질적인 건강 정보가 남지 않음
- 1,400~1,800자 또는 제목 1회·본문 2~3회 SEO 실패
- 일반 본문이 2~3줄 묶음이 아니거나, 한 줄이 공백 제외 24자를 초과하거나, 묶음 뒤의 빈 줄이 누락됨
- 인용구·인사·소제목·본문 중 하나라도 중앙 정렬이 아님
- 노란 하이라이트 정확히 3개, 밑줄 2~3개, 빨간 글씨 1~2개, 합계 6~8개 계약 위반 또는 강조 효과 중첩
- 가치입증 6행의 문구·순서 변경 또는 주제별 후보 선택
- `금손한의원 소개` 가치입증 표가 `solution-preview`보다 앞에 있거나 첫 정보 본문의 구분선·소제목·설명 뒤에 있음
- `goldhand-naver-native-v4` 속성 누락, CSS 카드 흔적, 1행×1열 가짜 표, 표 구분선·중앙 정렬 누락, `clinic-info` 50:50 폭 누락, 순정 컴포넌트·표1 계약 위반, 허용 팔레트 밖의 색상 혼입
- 고정 운영정보 누락이나 제작 지시·출처 목록 노출

## 완료 보고

최종 응답에는 제목, `콘텐츠 레퍼런스` 링크 한 편, 금손 공식 말투 검수, 최근 3개 주제·실제 사진 중복 검사, 실제 금손 사진 수와 최근 신뢰 사진 fallback 수, GPT Image 수, 공백 제외 글자 수, 제목·본문 키워드 횟수, 내용 순서·복사 거리, 전 문단 중앙 정렬, 노란 하이라이트·밑줄·주의용 빨간 글씨, 고정 가치입증 6행, 50:50 운영정보 표, 모바일 2~3줄 문단·네이버 순정 컴포넌트, 의료·사실·HTML 검사 결과와 저장 경로를 간단히 적는다.
