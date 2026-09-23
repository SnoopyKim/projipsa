---
id: area.project-memory-references
type: area
status: active
confidence: inferred
updated: 2026-09-23
sources:
  - research/2026-09-23-github-memory-snapshot.json
  - https://gittrend.io/trending/ai-memory
  - https://github.com/akitaonrails/ai-memory
  - https://github.com/thedotmack/claude-mem
  - https://github.com/volcengine/OpenViking
  - https://github.com/vectorize-io/hindsight
  - https://github.com/mem0ai/mem0
  - https://github.com/getzep/graphiti
  - https://github.com/basicmachines-co/basic-memory
  - https://github.com/MemTensor/MemOS
  - https://github.com/NevaMind-AI/memU
  - plugins/projipsa/shared/projipsa.md
  - plugins/projipsa/codex-skills/projipsa/references/operations.md
related:
  - project.current-state
  - decision.project-memory-focus.2026-09-23
  - area.project-knowledge-views
  - decision.evidence-aware-context.2026-09-23
---

# 2026년 9월 프로젝트 메모리 오픈소스 조사

## 조사 목적과 결론

Projipsa를 프로젝트 메모리 담당자로 집중시키기 위한 설계 참고 자료다.
관심 신호가 있는 저장소를 찾고 실제 소스의 저장·조회·갱신 경로를 읽어,
현재 Markdown 기반 플러그인에 적용할 수 있는 요소를 추렸다.

우선순위는 **관련 기억을 잘 찾기 → 새 근거와 기존 이해를 조정하기 →
사용 결과로 기록을 수정하기**다. Projipsa는 이 과정의 판단을 현재 호스트
에이전트에 맡기고, Markdown과 Git을 지속 가능한 원본으로 유지할 수 있다.
별도 메모리 서버·그래프 DB·임베딩은 검색 실패가 실제로 확인될 때 검토한다.

여기서 외부 구현의 존재는 소스 관찰이며, Projipsa 적용 우선순위는 설계 제안이다.
벤치마크 우위나 담당자 이상의 판단 능력을 검증한 보고서는 아니다.

사용자가 추가로 지정한 Understand-Anything과 Archify의 관계 추출·근거 검증·
설명 뷰는 [별도 추가 조사](project-knowledge-views.md)에 기록했다.
아래 원래 열 개 후보 및 관측 집계에는 합산하지 않는다.

## 기간과 관심도 근거

- 대상 기간: **2026-09-01~2026-09-23**, 월말까지의 전체 9월이 아니다.
- GitHub API에서 10개 저장소의 메타데이터와 커밋을 조회했다. 아래 숫자는
  9월 23일 관측한 **누적 stars**다.
- GitTrend의 **9월 21일 AI Memory 카테고리 일별 목록**을 관심 신호로 사용했다.
  이 목록은 GitHub 공식 Trending 월간 순위가 아니다.
- 정확한 9월 신규 stars 집계를 시도했으나 stargazer 페이지가 HTTP 404를
  반환하여 확보하지 못했다. 최근 30일 수치를 9월 증가량으로 바꾸어 쓰지 않았다.
- Graphiti·Basic Memory·MemOS·memU는 구조 비교를 위해 추가했다. 이번 조사에서
  9월 급상승을 입증한 후보로 분류하지 않는다.

| 프로젝트 | 9/23 누적 stars | 9월 관심 신호 / 선정 이유 | 조사 깊이 |
|---|---:|---|---|
| claude-mem | 94,506 | 9/21 목록, 당일 +69 | 훅·컨텍스트 예산·검색 소스 |
| mem0 | 65,860 | 9/21 목록, 당일 +76 | 현재 Python 저장 파이프라인 |
| codebase-memory-mcp | 44,244 | 9/21 목록, 당일 +115 | README로 인접 영역 선별 |
| OpenViking | 38,501 | 9/21 목록, 당일 +132 | 단계별 읽기·병합·경험 연결 소스 |
| Graphiti | 31,086 | 시간에 따른 사실 변경 비교 | 관계 모델·추출 소스 |
| Hindsight | 25,322 | 9/21 목록, 당일 +655 | 근거 통합·철회·문서 갱신 소스 |
| memU | 14,426 | 호스트 에이전트가 기억을 정리하는 방식 | prepare/commit 소스 |
| MemOS | 11,541 | 사용 결과와 피드백 연결 비교 | 로컬 플러그인 피드백 소스 |
| ai-memory | 8,128 | 9/21 목록, 당일 +372 | 수집 정책·정리 작업·조회 지침 |
| Basic Memory | 4,027 | Markdown 원본 유지 비교 | 파일 저장·체크섬 소스 |

관심 신호: [GitTrend의 날짜가 표시된 목록](https://gittrend.io/trending/ai-memory).
GitHub 원시 관측값, 커밋 SHA, 검토한 21개 핵심 소스의 경로·해시·영구 링크는
[관측 스냅샷](../../research/2026-09-23-github-memory-snapshot.json)에 보존했다.
수집한 외부 프로그램은 설치하거나 실행하지 않았다.

## 1. ai-memory — 프로젝트별 기록과 검색의 연결

**소스에서 확인한 내용.** Markdown/Git 원본과 파생 검색 인덱스를 분리한다.
수집 정책에는 저장소 단위 allowlist/denylist가 있고, 세션 정리 작업은
세대 번호와 작업 점유를 사용해 중복 실행과 오래된 완료 요청을 구분한다.
조회 지침은 짧은 검색 결과에서 전체 페이지로 이동하고, superseded 기록을
현재 사실과 구분하며, 도움이 됨·불필요함·오래됨·틀림 피드백을 다룬다.

**Projipsa에 적용.** 현재 작업의 영역과 이전 결정을 먼저 검색하고, 관련
페이지를 읽은 뒤 지금도 유효한지 확인한다. 실제 작업에서 발견한 오류와
유효 범위를 기존 페이지에 반영한다. 검색 결과의 존재나 반복 횟수만으로
사실의 신뢰도를 올리지 않는다.

**도입 비용.** 수집 훅과 백그라운드 큐를 가져오면 호스트별 이벤트, 중복 처리,
프로젝트 식별까지 운영해야 한다. 초기에는 워크플로만 적용한다.
README의 무 LLM 기본 경로와 별도로, 살펴본 `Consolidator`는 LLM을 호출한다.
이를 모든 정리가 무 LLM이라는 설명으로 일반화하지 않는다.

근거: [조회 및 피드백 지침](https://github.com/akitaonrails/ai-memory/blob/f0bfaeb3fb10f6cbe3031a52e97bb80eeb6a9c78/crates/ai-memory-core/src/routing_skills/ai-memory-retrieval/SKILL.md), [수집 범위 정책](https://github.com/akitaonrails/ai-memory/blob/f0bfaeb3fb10f6cbe3031a52e97bb80eeb6a9c78/crates/ai-memory-hooks/src/capture_policy.rs#L32-L63), [세션 정리 작업 점유](https://github.com/akitaonrails/ai-memory/blob/f0bfaeb3fb10f6cbe3031a52e97bb80eeb6a9c78/crates/ai-memory-store/src/session_consolidation.rs), [LLM 정리 경로](https://github.com/akitaonrails/ai-memory/blob/f0bfaeb3fb10f6cbe3031a52e97bb80eeb6a9c78/crates/ai-memory-consolidate/src/consolidator.rs#L112-L159).

## 2. claude-mem — 수집 시점과 읽기 비용을 명시

**소스에서 확인한 내용.** Codex용 훅은 SessionStart, UserPromptSubmit,
PostToolUse, Stop에 연결된다. `ContextBuilder`는 출력 한도에 맞게 관측과
요약을 줄이고, 통계도 실제로 전달한 부분을 기준으로 계산한다.
`SearchManager`는 간단한 검색 결과, 주변 timeline, 세부 관측 조회를 나누며
검색 경로와 fallback을 드러낸다.

**Projipsa에 적용.** index/current-state는 빠른 진입점으로 유지하고,
관련 결정·영역 페이지, 근거 순서로 펼친다. 나중에 검색 도구를 추가한다면
결과 ID·제목·짧은 설명·출처를 먼저 돌려주고 본문은 선택적으로 읽는다.

**도입 비용.** 자동 세션 수집은 별도의 관측·저장·재시도 경로다. 스킬에
“항상 기억하라” 한 줄을 넣는 것과 같은 기능으로 설명할 수 없다.
이번 변경에는 훅과 worker service를 추가하지 않았다.

근거: [Codex 훅](https://github.com/thedotmack/claude-mem/blob/4520de9e0f8d6cdc20597520e383d8b51d93137f/plugin/hooks/codex-hooks.json), [컨텍스트 한도 적용](https://github.com/thedotmack/claude-mem/blob/4520de9e0f8d6cdc20597520e383d8b51d93137f/src/services/context/ContextBuilder.ts#L262-L296), [검색과 timeline](https://github.com/thedotmack/claude-mem/blob/4520de9e0f8d6cdc20597520e383d8b51d93137f/src/services/worker/SearchManager.ts).

## 3. OpenViking — 계층별 읽기와 경험의 사용 결과 연결

**소스에서 확인한 내용.** `tiers.py`는 abstract/overview/full을 구분하고
모든 단계에 URI를 유지한다. 문서 개요는 헤딩과 첫 문단, 기억 개요는 요약
영역을 활용한다. 병합 지침은 유사도를 후보 탐색에만 사용하고 같은 대상을
뜻하는지 별도로 판단하도록 한다. `experience_lineage.py`는 성공적으로
읽은 경험의 URI와 작업 결과(success/failure/partial/unknown/unfinished)를
연결할 수 있는 표식을 만든다.

**Projipsa에 적용.** 폴더별 검색 범위와 단계별 읽기를 사용한다. 중요한
결정이나 절차를 재사용했을 때 결과가 달랐다면, 적용 조건과 근거를 갱신한다.
문장이 비슷하다는 이유로 다른 상황의 결정을 합치지 않는다.

**도입 비용.** 모든 페이지에 세 가지 요약 파일을 만들면 동기화 부담이
늘어난다. 지금은 기존 index → 페이지 → 근거의 읽기 경로로 충분하다.
경험을 읽었다는 사실은 그 경험이 성공을 일으켰다는 인과 증거가 아니다.

근거: [읽기 단계](https://github.com/volcengine/OpenViking/blob/03391bae4335eacf440a62d942f3951de6a63cbe/openviking/retrieve/context_assembler/tiers.py), [병합 판단 정책](https://github.com/volcengine/OpenViking/blob/03391bae4335eacf440a62d942f3951de6a63cbe/openviking/session/memory/merge_policy.py), [경험 사용 흔적](https://github.com/volcengine/OpenViking/blob/03391bae4335eacf440a62d942f3951de6a63cbe/openviking/session/memory/experience_lineage.py).

## 4. Hindsight — 근거 변화에 따라 이해를 다시 정리

**소스에서 확인한 내용.** 통합 프롬프트는 같은 대상·측면의 새 근거를
기존 observation에 합치고, source fact ID와 변경 이유를 요구한다.
한 사실의 변경이 여러 관측에 영향을 주면 함께 갱신하도록 한다.
`retractions.py`는 문서가 인용한 근거의 철회와 조회 불능을 구분하며,
`mental_model_refresh.py`는 갱신 근거·철회·변경 연산의 흔적을 표현한다.

**Projipsa에 적용.** “이 프로젝트에서 배포할 때 주의할 점은 무엇인가” 같은
반복 질문의 답을 area/procedure 페이지에 유지한다. 근거가 바뀌면 해당
페이지와 연결된 현재 상태를 검토한다. 찾을 수 없는 링크 하나를 근거로
기존 결론을 자동 삭제하지 않는다.

**도입 비용.** 상시 reflect/consolidation은 추가 모델 호출과 운영을 요구한다.
우선 새 근거가 들어왔을 때 영향받은 문서를 확인하는 Update/Lint에 적용한다.
여러 요약이 같은 원문을 인용한다고 독립된 증거가 늘어나는 것은 아니다.

근거: [근거 통합](https://github.com/vectorize-io/hindsight/blob/12f2d54f643baddacb98cd547c89b1a50c5c3dcc/hindsight-api-slim/hindsight_api/engine/consolidation/prompts.py), [근거 철회](https://github.com/vectorize-io/hindsight/blob/12f2d54f643baddacb98cd547c89b1a50c5c3dcc/hindsight-api-slim/hindsight_api/engine/reflect/retractions.py), [문서 갱신 흔적](https://github.com/vectorize-io/hindsight/blob/12f2d54f643baddacb98cd547c89b1a50c5c3dcc/hindsight-api-slim/hindsight_api/engine/mental_model_refresh.py).

## 5. Graphiti — 기록한 때와 사실이 유효한 때를 구분

**소스에서 확인한 내용.** 관계 `EntityEdge`에 근거 episode 목록과
`valid_at`, `invalid_at`, `expired_at`, `reference_time`이 있다.
추출 경로는 원래 사건 시점과 시스템이 관계를 만든 시점을 따로 다룬다.

**Projipsa에 적용.** `updated` 날짜만으로 “현재 확인됨”을 뜻하게 하지 않는다.
예를 들어 설치 버전은 관측 날짜·호스트·세션 범위를, 결정은 적용 조건과
대체 결정을 본문에 남긴다. 새 증거가 과거 사건을 설명하는 경우에도
파일 수정 시점과 사건 시점을 구분한다.

**도입 비용.** 이 의미를 표현하기 위해 그래프 DB를 도입할 필요는 없다.
모든 페이지에 여러 날짜 필드를 강제하기보다 변동성이 높은 주장부터 적용한다.

근거: [관계의 시간 필드](https://github.com/getzep/graphiti/blob/16cdf7045378c8d53ae01f94e2fa60d238cb0f68/graphiti_core/edges.py#L263-L282), [관계 추출](https://github.com/getzep/graphiti/blob/16cdf7045378c8d53ae01f94e2fa60d238cb0f68/graphiti_core/utils/maintenance/edge_operations.py).

## 6. mem0 — 현재 구현을 직접 읽어야 하는 사례

**소스에서 확인한 내용.** 확인한 Python `_add_to_vector_store`의 추론 경로는
최근 메시지와 기존 기억을 가져와 한 번의 추출 호출에 전달하고, 배치 임베딩,
해시 중복 제거, 삽입 및 ADD 이력을 처리한다. 소스에는 V3 additive pipeline로
표시되어 있다. 명시적 update 함수도 있지만 이 경로를 과거의
ADD/UPDATE/DELETE 자동 분류 도식으로 설명하면 부정확하다.

**Projipsa에 적용.** 새 자료만 보고 새 페이지를 만들지 말고 기존 지식을
같이 검토한다. 반복 수집은 중복으로 처리하고, 중요한 결과에는 근거를 남긴다.
외부 도구에 대한 기존 기억도 버전이 바뀌면 실제 구현과 대조한다.

**도입 비용.** Projipsa는 독립적인 사실 조각뿐 아니라 결정의 맥락을 보존해야
한다. 모든 문서를 벡터 저장소의 작은 사실 행으로 바꾸는 방식은 채택하지 않는다.
해시 일치는 같은 내용임을 보여주지만 의미상 중복이나 동일한 사건을 보장하지 않는다.

근거: [현재 저장 파이프라인](https://github.com/mem0ai/mem0/blob/f8082a7345dadd9e042ebbc40b57b1498c8f6d63/mem0/memory/main.py#L879-L1090).

## 7. Basic Memory — 파일 원본과 파생 저장의 일관성

**소스에서 확인한 내용.** Markdown 파일이 사용자와 에이전트가 공유하는
원본이다. `FileService`는 원자적 파일 쓰기와 실제 저장된 내용의 체크섬을
다룬다. 별도로 살펴본 `MarkdownProcessor`의 expected-checksum 검사는
import용 경로이므로 모든 쓰기가 같은 충돌 방지를 제공한다고 일반화하지 않는다.

**Projipsa에 적용.** 사람의 Markdown 편집이 그대로 유효하도록 유지한다.
나중에 검색 인덱스를 만들면 파일로 재생성할 수 있어야 하고, 체크섬은 인덱스
재생성이나 변경 감지의 근거로 사용한다. 현재는 Git과 단일 작성자 규칙을 유지한다.

**도입 비용.** MCP·DB는 선택 가능한 접근 수단이다. 이를 추가하기 전에는
현재 파일 탐색이 어떤 실제 질문을 놓치는지 측정한다.

근거: [현재 파일 저장 경로](https://github.com/basicmachines-co/basic-memory/blob/321cda71385652d30c62161cb5ea12ff90f56c37/src/basic_memory/services/file_service.py), [import용 파일 처리](https://github.com/basicmachines-co/basic-memory/blob/321cda71385652d30c62161cb5ea12ff90f56c37/src/basic_memory/markdown/markdown_processor.py).

## 8. MemOS — 수정 피드백을 근거와 연결

**소스에서 확인한 내용.** 조사한 범위는 MemOS 전체 서버가 아니라
`apps/memos-local-plugin/core/feedback`이다. `runRepair`는 같은 세션의
실행 흔적을 모으고, 가치 차이 및 분류된 피드백으로 수정을 판단한다.
저장되는 repair record에는 high/low-value trace ID와 `validated: false`가 있다.

**Projipsa에 적용.** 사용자의 정정이나 재현된 실패가 나오면 어느 기억을
어떤 근거로 수정했는지 남긴다. 자동 추론으로 제안한 절차와 실제로 확인된
프로젝트 규칙을 구분한다.

**도입 비용.** 실패 횟수나 문구 분류만으로 일반 규칙을 만들지 않는다.
처음에는 기존 결정·절차 페이지의 근거와 적용 범위를 고치는 것으로 충분하다.

근거: [runRepair와 근거 기록](https://github.com/MemTensor/MemOS/blob/a7367d07e55db61099f7b4e2c1108bc5831a24f3/apps/memos-local-plugin/core/feedback/feedback.ts).

## 9. memU — 기억 정리를 호스트 에이전트에 맡기기

**소스에서 확인한 내용.** 현재 README는 개인 기억을 Wiki로 보존하고,
호스트 에이전트가 기억·스킬 Markdown을 작성한다고 설명한다.
`prepare_memorize`는 작업용 자료와 지침을 준비하고,
`commit_memorize`는 변경된 recall file을 찾아 backend에 전달한다.
이 경로는 별도 모델 서비스에서 정리를 완결하는 방식과 다르다.

**Projipsa에 적용.** 이미 프로젝트 맥락을 가진 호스트 에이전트가 이번 작업의
지속할 가치가 있는 지식을 정리하도록 한다. 저장 도구는 필요할 때 변경 감지,
검증, 검색 같은 기계적인 역할을 담당할 수 있다.

**도입 비용.** 모든 경험을 자동으로 Skill이나 AGENTS.md 규칙으로 승격하지 않는다.
프로젝트 기억, 재사용 절차, 전역 개인 선호는 범위가 다르다.

근거: [현재 아키텍처 설명](https://github.com/NevaMind-AI/memU/blob/2c050bc9681a4c0aff1af211a000e73d14f33356/README.md), [prepare/commit](https://github.com/NevaMind-AI/memU/blob/2c050bc9681a4c0aff1af211a000e73d14f33356/src/memu/app/memorize/lifecycle.py), [세션 자료 준비](https://github.com/NevaMind-AI/memU/blob/2c050bc9681a4c0aff1af211a000e73d14f33356/src/memu/app/memorize/materialize.py).

## 인접 영역: codebase-memory-mcp

README로 선별한 코드 구조·관계 검색 도구다. 구현 구조를 빠르게 찾는 기능은
프로젝트 결정과 이력을 설명하는 기억을 보완할 수 있다. Projipsa가 동일한
코드 인덱서를 직접 만들기보다 기존 도구의 결과와 정확한 코드 경로를 근거로
연결하는 후보로 남긴다. 내부 검색 엔진은 이번 조사에서 분석하지 않았다.

근거: [코드 검색 도구 소개](https://github.com/DeusData/codebase-memory-mcp/blob/e783f73d752f83b689451e3a7e48061cda1202f7/README.md).

## Projipsa 적용 정리

| 요소 | 현재 반영 범위 | 추가 구현을 검토할 조건 |
|---|---|---|
| 메모리 전담 역할 | outsource와 실행 계약 제거, 3개 Skill로 축소 | 이번 변경에 포함 |
| 작업별 관련 기억 탐색 | 제목·짧은 발췌 → 관련 페이지 → 근거, 검색 미스 재탐색 | 실제 질문에서 파일 검색 누락이 반복될 때 인덱스 |
| 근거와 기존 이해 조정 | 지지·확장·정정·대체·충돌 구분을 Ingest/Update에 추가 | 영향받는 페이지 누락이 반복될 때 역참조 도구 |
| 결과가 남는 결정 기록 | 관측 결과·적용 조건·재검토 조건을 선택적으로 기록 | 별도 학습 점수 체계는 아직 필요성 미검증 |
| 변동성 높은 사실 검증 | 작업에 영향이 있으면 현재 코드·환경·외부 소스와 대조 | revision/hash 기반 stale 후보 검출 |
| 일상적인 갱신 | 이미 승인된 프로젝트 관리 범위를 재사용 | 자동 훅은 호스트별 누락·중복 평가 후 |
| 사람이 편집할 수 있는 원본 | Markdown/Git 유지 | 파생 인덱스가 생겨도 원본 권한 유지 |

현재 반영한 것은 지침과 템플릿 수준이다. 자동 수집·백그라운드 정리·새 검색
엔진·실행 결과 계측·모델 기반 평가기는 이번 패키지에 구현하지 않았다.

후속 범위 확정: 사용자가 0.6.0 배포에 추가 기능을 포함하도록 요청하여
명시적 관계·역참조, 로컬 근거 변경 비교, 발췌 브리핑과 Mermaid 뷰를 구현했다.
위 조사 시점의 적용 표와 구분하며, 현재 범위는
[구현 결정](../decisions/2026-09-23-evidence-aware-context.md)을 따른다.

## 다음 검증: 기록이 다음 작업에 도움이 되는가

동일 모델·도구·작업 예산으로 **기본 에이전트 / 기존 Projipsa /
개선된 Projipsa**를 비교한다. 첫 세션에서 작업하고 새 세션에서 이어가는
동일한 시나리오를 여러 번 실행한다. 샘플 수와 통과 기준은 실행 전에 정한다.

| 시나리오 | 확인할 결과 |
|---|---|
| 과거에 배제한 설계 재등장 | 이전 근거를 찾아 현재 조건과 비교하는가 |
| 기억에 적힌 설치 버전과 실제 환경 불일치 | 기억을 그대로 답하지 않고 차이를 발견하는가 |
| 같은 자료를 두 번 수집 | 중복 페이지·독립 증거 수가 늘지 않는가 |
| 실패했던 접근이 다른 조건에서 성공 | 적용 범위를 수정하고 과거 실패도 보존하는가 |
| 근거 철회 또는 링크 접근 실패 | 철회와 접근 불능을 구분하는가 |
| 사용자가 Markdown을 직접 고침 | 다음 조회에 반영되고 에이전트가 덮어쓰지 않는가 |
| 승인된 갱신 범위 / 읽기 전용 조회 | 필요한 쓰기는 마무리하고 조회만 한 경우에는 쓰지 않는가 |
| 과거 delivery 페이지를 가진 프로젝트 업그레이드 | 기존 지식과 링크가 유지되는가 |

측정할 항목은 답의 정확성·출처 적합성·오래된 사실 채택·반복 질문·필요한
기억 누락·기억 읽기에 쓴 토큰과 시간이다. 형식 검증 통과와 실제 지식 활용
효과를 구분한다. 현재 행동 비교 결과는 없다.
