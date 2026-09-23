---
id: area.project-knowledge-views
type: area
status: active
confidence: inferred
updated: 2026-09-23
sources:
  - research/2026-09-23-project-knowledge-views-snapshot.json
  - https://github.com/Egonex-AI/Understand-Anything/tree/6df3065f1d8ddc2ce3615314d1d493f36d6b1c80
  - https://github.com/tt-a1i/archify/tree/8809b273c278a813a47fa37698864779c0d4cf08
  - plugins/projipsa/shared/projipsa.md
  - plugins/projipsa/codex-skills/projipsa/references/page-types.md
  - plugins/projipsa/codex-skills/projipsa/scripts/memory_context.py
related:
  - area.project-memory-references
  - project.current-state
  - decision.project-memory-focus.2026-09-23
  - decision.evidence-aware-context.2026-09-23
---

# 프로젝트 지식의 관계와 설명 뷰

## 조사 범위

사용자가 지정한 Understand-Anything과 Archify의 기능 및 구현을 확인한
2026-09-23 추가 조사다. 아래 구현 관찰과 Projipsa 설계 제안은 구분한다.
이번 후보 선정은 9월 인기 순위나 증가량에 근거하지 않는다.

| 대상 | 확인한 커밋 | 이 조사에서 다룬 기능 |
|---|---|---|
| Understand-Anything | `6df3065f1d8d` | Wiki 파싱·추론 관계·업무 도메인·코드 그래프 갱신 |
| Archify | `8809b273c278` | 도식 입력·출처 검증·산출물 검증·구조 변화 비교 |

12개 주요 경로의 커밋·해시와 읽기 전용 호환성 확인 결과는
[별도 관측 스냅샷](../../research/2026-09-23-project-knowledge-views-snapshot.json)에 보존했다.
외부 플러그인을 설치하거나 전체 파이프라인·모델 분석·뷰어를 실행하지 않았다.
원래 [메모리 조사](project-memory-references.md)의 관측 스냅샷은 변경하지 않았다.

## Understand-Anything의 구현 관찰

### 명시적 구조와 추론을 나누는 Wiki 그래프

`understand-knowledge`는 LLM Wiki를 입력받는다. Python 파서가 문서와
`[[wikilink]]`, `index.md`의 분류, 역링크를 추출하고, 모델 분석 단계가
엔티티·주장·암묵적 관계를 추가한다. 분석 배치가 실패해도 파싱 결과로
진행하도록 지침이 작성되어 있다. 결과는 `.ua/knowledge-graph.json`에 저장한다.

파서는 `raw/` 파일을 이름·종류·크기로 나타낸다. 원문 PDF 등의 내용을
검증하는 기능으로 해석할 수 없다. 문서 내용은 모델 전달용 필드에서 앞
3,000자로 제한되므로 뒷부분의 조건이나 정정을 놓칠 가능성이 있다.

근거: [Wiki 워크플로](https://github.com/Egonex-AI/Understand-Anything/blob/6df3065f1d8ddc2ce3615314d1d493f36d6b1c80/understand-anything-plugin/skills/understand-knowledge/SKILL.md), [파서](https://github.com/Egonex-AI/Understand-Anything/blob/6df3065f1d8ddc2ce3615314d1d493f36d6b1c80/understand-anything-plugin/skills/understand-knowledge/parse-knowledge-base.py).

### 주장과 문서 사이의 관계

모델 지침은 `builds_on`, `contradicts`, `exemplifies`, `cites` 등의 관계를
명확한 텍스트 근거가 있을 때 추출하도록 한다. 병합기는 관계 종류를
정규화하고, 없는 노드를 가리키는 연결을 버리며, 이름을 정규화해 엔티티를
중복 제거한다. 분류와 읽기 순서에 따른 투어도 만든다.

검토한 `GraphEdge`에는 source/target/type/direction/description/weight가
있지만 근거 구절·추출 방식·유효기간을 필수로 기록하는 계약은 없다.
관계별 weight는 분석 지침이 지정한 값이며, 정답 확률로 보정된 confidence가
아니다. 스키마와 참조의 유효성은 관계 해석의 정확성을 입증하지 않는다.

근거: [분석 지침](https://github.com/Egonex-AI/Understand-Anything/blob/6df3065f1d8ddc2ce3615314d1d493f36d6b1c80/understand-anything-plugin/agents/article-analyzer.md), [병합기](https://github.com/Egonex-AI/Understand-Anything/blob/6df3065f1d8ddc2ce3615314d1d493f36d6b1c80/understand-anything-plugin/skills/understand-knowledge/merge-knowledge-graph.py), [그래프 타입](https://github.com/Egonex-AI/Understand-Anything/blob/6df3065f1d8ddc2ce3615314d1d493f36d6b1c80/understand-anything-plugin/packages/core/src/types.ts).

### 업무 도메인과 구현의 연결

도메인 분석 지침은 `domain → flow → step`으로 업무를 표현하고, 업무 규칙,
주요 엔티티, 시작점, 구현 파일을 연결한다. 이미 만들어진 그래프가 있으면
요약과 관계를 바탕으로 분석하는 경로도 있으므로 모든 결과가 원본 코드를
직접 재검증했다고 볼 수는 없다.

Projipsa의 area 페이지에 적용할 수 있는 구조는 **영역의 목적 → 업무 흐름 →
제약과 규칙 → 관련 결정 → 구현 근거**다. 이는 코드 파일 목록만으로 남기기
어려운 프로젝트 지식을 정리하는 제안이며, 현재 적용된 새 템플릿은 아니다.

근거: [도메인 분석 지침](https://github.com/Egonex-AI/Understand-Anything/blob/6df3065f1d8ddc2ce3615314d1d493f36d6b1c80/understand-anything-plugin/agents/domain-analyzer.md).

### 갱신 성공과 기준점 이동의 순서

코드 그래프의 `finalize-incremental.mjs`는 분석 대상 파일의 누락, 필요한
레이어·투어의 누락, 해결되지 않은 심볼 손실을 검사한다. 그래프를 저장한 뒤
fingerprint와 meta의 기준점을 갱신한다. 분석 실패를 성공한 새 기준점으로
덮지 않으려는 순서다. 이것은 코드 그래프 경로의 관찰이며, Wiki의 모든
주장에 같은 증분 검증이 적용된다는 뜻은 아니다. 여러 파일 전체의 원자적
트랜잭션을 입증한 것도 아니다.

근거: [증분 갱신 완료 처리](https://github.com/Egonex-AI/Understand-Anything/blob/6df3065f1d8ddc2ce3615314d1d493f36d6b1c80/understand-anything-plugin/skills/understand/finalize-incremental.mjs).

### Projipsa 문서와의 실제 호환성

위 커밋의 파서를 읽은 뒤 `parse_wiki(docs)` 함수를 직접 호출했다. CLI의
파일 저장 진입점은 실행하지 않았다. 추가 조사 페이지를 쓰기 전 작업 트리에서
**문서 12개, 분류 4개, wikilink 0개, 연결 0개**가 나왔다.

이유는 문서가 없어서가 아니다. Projipsa는 일반 Markdown 링크와 YAML의
`sources`, `related`, `supersedes`를 사용하지만 이 파서는 그 의미를 관계로
변환하지 않는다. `logs/YYYY-MM.md`와 `research/`도 각각 `log.md`, `raw/`
형식으로 자동 해석되지 않는다. 포맷 감지 성공과 의미 있는 통합은 다르다.

따라서 Projipsa의 문서 형식을 바꾸기 전에, 기존 메타데이터를 읽는 얇은
변환기를 검토한다. 이것은 제안이며 이번 조사에서 어댑터는 구현하지 않았다.

## Archify의 구현 관찰

### 구조화한 명세에서 설명용 산출물 생성

Archify는 architecture/workflow/sequence/dataflow/lifecycle JSON을 받아
독립 HTML과 inline SVG로 만든다. 모델은 의미와 구조를 작성하고 렌더러는
표현과 검증을 담당한다. Mermaid 입력 역시 의미를 읽어 JSON을 새로 작성하는
워크플로다. 프로젝트의 의사결정 기록을 자동 수집하는 메모리 시스템과는
담당 범위가 다르다.

근거: [Archify 지침](https://github.com/tt-a1i/archify/blob/8809b273c278a813a47fa37698864779c0d4cf08/archify/SKILL.md).

### 출처를 고정하고 검사하는 방식

architecture 모드의 선택적 repository evidence는 저장소 URL, 전체 커밋 SHA,
컴포넌트의 파일 경로와 선택적 행 범위를 받는다. 검증기는 로컬 Git의 origin,
커밋 존재, 해당 커밋의 blob 및 행 범위를 검사하고 고정된 출처 링크를 만든다.
작업 트리의 변경 내용 대신 Git 객체를 읽으며 replacement refs도 끈다.

검증 범위는 **가리킨 소스가 해당 버전에 존재하는가**다. 그 코드가 도식의
설명을 실제로 뒷받침하는지, 모든 관계가 표현되었는지를 증명하지 않는다.
검토한 구현에서 출처 검증은 architecture 모드에 해당한다.

근거: [repository evidence 검증기](https://github.com/tt-a1i/archify/blob/8809b273c278a813a47fa37698864779c0d4cf08/archify/renderers/shared/repository-evidence.mjs).

### 무엇을 검사했는지 분리하는 기록

`deliver` 구현은 입력 bytes를 한 번 읽어 별도 후보에 고정하고, 렌더링 및
산출물 검사를 통과한 경우 최종 HTML을 교체한다. 입력과 출력의 SHA-256 및
크기를 결과에 기록한다. 검증 실패한 후보로 이전 정상 결과를 대체하지 않는다.

전달 계약은 결정적 산출물 검사, 실제 브라우저 측정, 사람 또는 이미지 모델의
시각적 판단을 구분한다. 하나의 통과로 다른 검증까지 통과했다고 표현하지 않는다.
Projipsa에도 문서 형식 검사·출처 존재 확인·주장 내용 확인·실제 작업 결과를
구별하는 원칙을 적용할 수 있다. 대규모 실행 계약을 되살릴 필요는 없다.

근거: [deliver 구현](https://github.com/tt-a1i/archify/blob/8809b273c278a813a47fa37698864779c0d4cf08/archify/bin/archify.mjs#L859), [검증 범위 계약](https://github.com/tt-a1i/archify/blob/8809b273c278a813a47fa37698864779c0d4cf08/archify/references/delivery-contract.md).

### 변경 종류의 구분

architecture 비교기는 안정된 ID를 기준으로 구조·의미·근거·배치 변경을
분류한다. 파일 출처 변경과 노드 위치 이동을 의미 변경과 구분할 수 있다.
비교 대상은 작성된 JSON이며, 런타임 영향·인과관계·위험을 추론하지 않는다고
결과의 limitations에 명시한다. 코드에서 아키텍처 변화를 자동 복원한 결과로
해석하면 안 된다.

근거: [architecture 비교기](https://github.com/tt-a1i/archify/blob/8809b273c278a813a47fa37698864779c0d4cf08/archify/delta/architecture-delta.mjs#L139).

## Projipsa의 후속 설계 제안

후속 구현: 사용자가 아래 방향을 0.6.0에 포함하도록 요청하여, 명시적 관계와
역참조, 로컬 근거 해시 기반 재검토 후보, 작업별 발췌 브리핑, Mermaid 뷰를
구현했다. [구현 범위와 한계](../decisions/2026-09-23-evidence-aware-context.md)를
참조한다. 아래 조사 시점 제안 중 모델 추론 관계와 원격 내용의 자동 검증은
구현 범위에 포함되지 않는다.

Markdown·증거·이력을 원본으로 유지하고, 필요할 때 관계 인덱스와 설명 뷰를
재생성하는 현재 역할 구분을 사용한다. 아래는 도입 결정이나 구현 완료 기록이 아니다.

| 순서 | 제안 | 확인할 효과 |
|---|---|---|
| 1 | 기존 stable ID, sources, related, supersedes와 Markdown 링크에서 관계·역참조 추출 | 결정의 근거와 영향을 받는 페이지를 빠짐없이 찾는가 |
| 2 | 근거 revision/hash의 변화로 재검토 후보 표시 | 오래된 근거를 발견하되 문장을 자동으로 거짓 처리하지 않는가 |
| 3 | 추론 관계에는 원문 위치·추출 방식·검토 상태 연결 | 추론이 확인된 사실로 재사용되는 것을 구별하는가 |
| 4 | 목적·업무 흐름·규칙·결정·구현을 연결하는 영역 설명 | 새 세션이 프로젝트 용어와 설계 이유를 설명하는가 |
| 5 | 작업별 읽기 경로와 요청 시 생성하는 관계도·변경도 | 필요한 기억을 읽는 비용과 사람이 검토하는 비용이 줄어드는가 |

예를 들어 Query는 변경할 영역의 관련 결정, 현재 규칙, 실패 기록, 재검토
후보를 짧게 묶어 보여줄 수 있다. 사람에게 구조 설명이 필요하면 같은 근거를
도식으로 표현한다. 그래프 DB나 상시 대시보드는 이 효과를 얻는 필수 조건이 아니다.

판단의 이유는 코드 구조만으로 복원할 수 없으므로 실제 결정 시점의 맥락,
배제한 대안, 관측 결과를 계속 남겨야 한다. 담당자 수준의 지식 활용 여부는
원래 조사에서 제안한 다중 세션 질문으로 평가해야 한다.
