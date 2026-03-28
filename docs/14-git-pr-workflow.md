# Git And PR Workflow

## 목표

- 무인 자동화 중에도 packet 단위 작업 이력이 git과 PR 산출물로 남아야 한다.
- 사람이 매 packet마다 승인하지 않아도, 나중에 GitHub PR 히스토리나 로컬 산출물을 보고 무슨 작업이 있었는지 추적 가능해야 한다.
- 제목, 본문, 리뷰 코멘트 규격은 한글로 일관되게 유지한다.

## 기본 규칙

- 저장소 이름은 영어 kebab-case를 사용한다.
- 기본 브랜치는 `main` 이다.
- packet 브랜치는 `packet/<packet-id-lower>-<packet-slug>` 규칙을 사용한다.
- repair loop는 별도 브랜치를 만들지 않고 같은 packet 브랜치에서 이어간다.
- 논리적 PR 작성자는 `claude-programmer` 이다.
- 최종 승인자와 병합 주체는 `codex` 이다.

## 무인 운영 해석

- Claude 프로그래밍 담당 subagent가 packet 브랜치에서 구현과 문서, 테스트, 산출물을 갱신한다.
- Claude 내 보안/성능/문서/review 역할은 병렬 레인으로 결과를 모은다.
- Codex는 병합 직전 검토와 승인 결정을 담당한다.
- 실제 git commit author는 자동화 계정일 수 있지만, PR 본문에는 논리적 작성자와 승인자를 명시한다.

## 병렬 처리 기준

- 구현이 시작되면 아래 레인은 병렬 처리 대상이다.
- 보안 검토
- 성능 검토
- 문서 정리
- 독립 코드 리뷰

다만 아래는 순차 조건을 둔다.

- research -> architecture -> implementation 은 의존성이 크므로 기본은 순차 처리
- independent review 는 구현 산출물이 나온 뒤 시작
- Codex 최종 승인과 merge 는 review 결과가 모인 뒤 실행

## 한글 PR 규격

PR 본문은 반드시 아래 섹션을 포함한다.

- 작업 제목
- 작업 이유
- 작업 목표
- 변경 범위
- 검증 결과
- 위험 및 후속 작업
- 논리적 작성자
- 최종 승인자

Codex 리뷰 코멘트는 최소 아래를 포함한다.

- 리뷰 결론
- 주요 판단 근거
- 확인한 항목
- 후속 조치

## merge 규칙

- Codex verdict가 `pending` 이 아니고 packet 상태가 `completed` 여야 merge 가능하다.
- approval pause가 걸린 packet은 `resolve-approval-pause --decision approved` 이후에만 merge 한다.
- merge 전략은 기본 `merge commit` 이다.
- merge 후 packet 브랜치는 삭제한다.

## GitHub 브리지

- 이 문서의 로컬 PR 산출물은 향후 GitHub PR 생성 시 그대로 재사용하는 원본이다.
- 네트워크 기반 GitHub 발행은 `team/policies/github-bridge.yaml` 이 허용할 때만 활성화한다.
- 기본 secret source는 repo 내부가 아니라 `~/.config/agent-bootstrap/github-author.env`, `~/.config/agent-bootstrap/github-reviewer.env` 같은 machine-global env file 이다.
- 실제 GitHub 계정 분리는 서로 다른 `GH_TOKEN` 으로 강제한다.
- repo-local `team/policies/github-author.env.local`, `team/policies/github-reviewer.env.local` 은 선택적 override 로만 사용한다.
- background service 나 outer runner 는 `ABI_GITHUB_AUTHOR_TOKEN`, `ABI_GITHUB_REVIEWER_TOKEN`, `ABI_GITHUB_AUTHOR_ENV_FILE`, `ABI_GITHUB_REVIEWER_ENV_FILE` 로 service-level override 를 줄 수 있다.
- 작성자 계정은 PR 생성 또는 수정만 담당한다.
- 승인자 계정은 `Approve review` 와 `merge` 만 담당한다.
- `require_distinct_accounts: true` 일 때 두 env가 같은 GitHub 로그인으로 해석되면 fail-closed 한다.
- 완전 무인 자동화에서는 `enabled: true` 와 `auto_publish_completed_packets: true` 를 함께 사용한다.
- 이 경우 packet closeout 또는 approval resolution 의 승인 경계에서 로컬 merge 대신 GitHub PR 발행, 승인, 병합이 수행된다.
- 수동 점검이 필요하면 `github-pr-preflight`, `github-sync-packet-pr` 명령으로 현재 packet 기준 상태를 확인할 수 있다.
