# Tasks: LLM 新闻分析与股票推荐

**Input**: Design documents from `/specs/001-llm-news-analysis/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/cli-interface.md ✅

**Tests**: Tests are included as they are essential for ensuring code quality per Constitution Principle X.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `llm-analysis/src/`, `llm-analysis/tests/` at repository root
- Paths shown below follow the structure defined in plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create llm-analysis directory structure per implementation plan
- [x] T002 Initialize Python 3.12 project with uv in llm-analysis/pyproject.toml
- [x] T003 [P] Add production dependencies (openai, pydantic, python-dotenv, httpx) to llm-analysis/pyproject.toml
- [x] T004 [P] Add development dependencies (pytest, pytest-asyncio, pytest-mock, pytest-cov) to llm-analysis/pyproject.toml
- [x] T005 [P] Create .env.example file in llm-analysis/.env.example with OpenAI API key template
- [x] T006 [P] Create README.md in llm-analysis/README.md with project overview
- [x] T007 Create src/llm_analysis/__init__.py in llm-analysis/src/llm_analysis/__init__.py
- [x] T008 Create tests/__init__.py in llm-analysis/tests/__init__.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T009 Create llm-analysis/tests/conftest.py with pytest configuration and common fixtures
- [x] T010 [P] Implement date validation utility in llm-analysis/src/llm_analysis/utils/date_utils.py
- [x] T011 [P] Implement text processing utility in llm-analysis/src/llm_analysis/utils/text_utils.py
- [x] T012 [P] Implement validators module in llm-analysis/src/llm_analysis/utils/validators.py
- [x] T013 [P] Create utils/__init__.py in llm-analysis/src/llm_analysis/utils/__init__.py
- [x] T014 Implement environment configuration management using python-dotenv in llm-analysis/src/llm_analysis/config.py
- [x] T015 Implement error handling and logging infrastructure in llm-analysis/src/llm_analysis/utils/logger.py
- [x] T016 Create storage directory structure in llm-analysis/src/llm_analysis/storage/__init__.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1, 2, 3 - 核心分析功能 (Priority: P1) 🎯 MVP

**Goal**: 实现核心的新闻分析功能，包括读取新闻、调用LLM分析、生成包含市场情绪和经济发展趋势的分析报告

**Independent Test**: 给定当日新闻Markdown文件，系统能够生成包含市场情绪分析和经济发展趋势的完整分析报告，并保存为JSON文件。可以通过CLI命令验证分析结果。

### Tests for User Stories 1-3 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T017 [P] [US1] Unit test for MarketSentiment model validation in llm-analysis/tests/unit/test_models.py
- [ ] T018 [P] [US1] Unit test for EconomicTrends model validation in llm-analysis/tests/unit/test_models.py
- [ ] T019 [P] [US1] Unit test for NewsAnalysisReport model validation in llm-analysis/tests/unit/test_models.py
- [ ] T020 [P] [US1] Unit test for news reader service in llm-analysis/tests/unit/test_services.py
- [ ] T021 [P] [US1] Unit test for LLM client with mock OpenAI API in llm-analysis/tests/unit/test_services.py
- [ ] T022 [US1] Integration test for complete analysis flow in llm-analysis/tests/integration/test_analyzer.py
- [ ] T023 [US1] Contract test for OpenAI API interaction in llm-analysis/tests/contract/test_openai_api.py

### Implementation for User Stories 1-3

- [x] T024 [P] [US1] Create MarketSentiment model in llm-analysis/src/llm_analysis/models/sentiment.py
- [x] T025 [P] [US1] Create EconomicTrends model in llm-analysis/src/llm_analysis/models/trend.py
- [x] T026 [P] [US1] Create NewsAnalysisReport model in llm-analysis/src/llm_analysis/models/analysis.py
- [x] T027 [P] [US1] Create models/__init__.py exporting all models in llm-analysis/src/llm_analysis/models/__init__.py
- [x] T028 [US1] Implement news reader service to parse Markdown files in llm-analysis/src/llm_analysis/services/news_reader.py
- [x] T029 [US1] Implement OpenAI API client with error handling and retry logic in llm-analysis/src/llm_analysis/services/llm_client.py
- [x] T030 [US1] Implement sentiment analyzer service using LLM in llm-analysis/src/llm_analysis/services/sentiment_analyzer.py
- [x] T031 [US1] Implement trend analyzer service using LLM in llm-analysis/src/llm_analysis/services/trend_analyzer.py
- [x] T032 [US1] Implement main analyzer service orchestrating sentiment and trend analysis in llm-analysis/src/llm_analysis/services/analyzer.py
- [x] T033 [US1] Implement file storage service for saving analysis results in llm-analysis/src/llm_analysis/storage/file_storage.py
- [x] T034 [US1] Implement index manager for tracking analysis history in llm-analysis/src/llm_analysis/storage/index_manager.py
- [x] T035 [US1] Create services/__init__.py in llm-analysis/src/llm_analysis/services/__init__.py
- [x] T036 [US1] Implement analyze command CLI entry point in llm-analysis/scripts/analyze_news.py

**Checkpoint**: At this point, User Stories 1-3 should be fully functional and testable independently. Users can analyze news and get sentiment + trend reports.

---

## Phase 4: User Story 4 - 股票推荐建议 (Priority: P2)

**Goal**: 基于市场情绪和经济发展趋势分析，生成股票投资建议和行业推荐

**Independent Test**: 给定已生成的分析报告（包含市场情绪和趋势），系统能够生成股票推荐建议，包括推荐行业、推荐理由、风险等级和免责声明。可以通过CLI命令验证推荐结果。

### Tests for User Story 4 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T037 [P] [US4] Unit test for StockRecommendation model validation in llm-analysis/tests/unit/test_models.py
- [ ] T038 [P] [US4] Unit test for recommendation engine service in llm-analysis/tests/unit/test_services.py
- [ ] T039 [US4] Integration test for recommendation generation flow in llm-analysis/tests/integration/test_recommendation.py

### Implementation for User Story 4

- [x] T040 [P] [US4] Create StockRecommendation model in llm-analysis/src/llm_analysis/models/recommendation.py
- [x] T041 [US4] Update NewsAnalysisReport model to include recommendations list in llm-analysis/src/llm_analysis/models/analysis.py
- [x] T042 [US4] Implement recommendation engine service using LLM in llm-analysis/src/llm_analysis/services/recommendation_engine.py
- [x] T043 [US4] Update analyzer service to include recommendation generation in llm-analysis/src/llm_analysis/services/analyzer.py
- [x] T044 [US4] Update analyze command to include recommendations in output in llm-analysis/scripts/analyze_news.py

**Checkpoint**: At this point, User Stories 1-4 should all work independently. Users can get complete analysis reports with recommendations.

---

## Phase 5: User Story 5 - 历史查询和对比 (Priority: P3)

**Goal**: 支持查询历史分析记录，对比不同日期的分析结果，导出分析报告

**Independent Test**: 用户可以查询任意历史日期的分析报告，对比多个日期的市场情绪和趋势变化，并导出为不同格式（JSON、CSV、Markdown）。可以通过CLI命令验证查询、对比和导出功能。

### Tests for User Story 5 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T045 [P] [US5] Unit test for AnalysisIndex model validation in llm-analysis/tests/unit/test_models.py
- [ ] T046 [P] [US5] Unit test for query command functionality in llm-analysis/tests/unit/test_cli.py
- [ ] T047 [P] [US5] Unit test for compare command functionality in llm-analysis/tests/unit/test_cli.py
- [ ] T048 [P] [US5] Unit test for export command functionality in llm-analysis/tests/unit/test_cli.py
- [ ] T049 [US5] Integration test for query command end-to-end in llm-analysis/tests/integration/test_query.py
- [ ] T050 [US5] Integration test for compare command end-to-end in llm-analysis/tests/integration/test_compare.py
- [ ] T051 [US5] Integration test for export command end-to-end in llm-analysis/tests/integration/test_export.py

### Implementation for User Story 5

- [ ] T052 [P] [US5] Create AnalysisIndex model in llm-analysis/src/llm_analysis/models/analysis.py
- [x] T053 [US5] Implement query command CLI handler in llm-analysis/scripts/analyze_news.py
- [x] T054 [US5] Implement list command CLI handler in llm-analysis/scripts/analyze_news.py
- [x] T055 [US5] Implement compare command CLI handler in llm-analysis/scripts/analyze_news.py
- [x] T056 [US5] Implement export command CLI handler in llm-analysis/scripts/analyze_news.py
- [ ] T057 [US5] Implement text formatter for query output in llm-analysis/src/llm_analysis/utils/formatters.py
- [ ] T058 [US5] Implement markdown formatter for query output in llm-analysis/src/llm_analysis/utils/formatters.py
- [ ] T059 [US5] Implement CSV exporter for export command in llm-analysis/src/llm_analysis/utils/exporters.py
- [ ] T060 [US5] Implement JSON exporter for export command in llm-analysis/src/llm_analysis/utils/exporters.py
- [ ] T061 [US5] Update index manager to support query operations in llm-analysis/src/llm_analysis/storage/index_manager.py

**Checkpoint**: All user stories should now be independently functional. Users can analyze, query, compare, and export analysis reports.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T062 [P] Add comprehensive docstrings to all public functions per Constitution Principle IV
- [ ] T063 [P] Add type hints to all functions per Constitution Principle II
- [ ] T064 [P] Update README.md with usage examples and troubleshooting guide
- [ ] T065 [P] Add error handling improvements across all services per Constitution Principle I
- [ ] T066 [P] Add logging statements for key operations per Constitution Principle IX
- [ ] T067 [P] Add additional unit tests to reach 80% code coverage target
- [ ] T068 [P] Run quickstart.md validation to ensure all examples work
- [ ] T069 Code cleanup and refactoring for code quality
- [ ] T070 Performance optimization for large news content handling
- [ ] T071 Add input validation for all CLI commands per Constitution Principle II
- [ ] T072 Add timeout handling for all LLM API calls per Constitution Principle V
- [ ] T073 Create .gitignore file for Python project artifacts in llm-analysis/.gitignore

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories 1-3 (Phase 3)**: Depends on Foundational phase completion - MVP functionality
- **User Story 4 (Phase 4)**: Depends on Phase 3 completion (needs analysis results)
- **User Story 5 (Phase 5)**: Depends on Phase 3 completion (needs stored analysis results)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Stories 1-3 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Depends on User Stories 1-3 - Needs analysis results to generate recommendations
- **User Story 5 (P3)**: Depends on User Stories 1-3 - Needs stored analysis results to query and compare

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before CLI handlers
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, User Stories 1-3 can start
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on sequentially (due to dependencies)

---

## Parallel Example: User Stories 1-3

```bash
# Launch all model tests together:
Task: "Unit test for MarketSentiment model validation in llm-analysis/tests/unit/test_models.py"
Task: "Unit test for EconomicTrends model validation in llm-analysis/tests/unit/test_models.py"
Task: "Unit test for NewsAnalysisReport model validation in llm-analysis/tests/unit/test_models.py"

# Launch all model implementations together:
Task: "Create MarketSentiment model in llm-analysis/src/llm_analysis/models/sentiment.py"
Task: "Create EconomicTrends model in llm-analysis/src/llm_analysis/models/trend.py"
Task: "Create NewsAnalysisReport model in llm-analysis/src/llm_analysis/models/analysis.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1-3 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Stories 1-3
4. **STOP and VALIDATE**: Test User Stories 1-3 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Stories 1-3 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 4 → Test independently → Deploy/Demo
4. Add User Story 5 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Sequential Implementation Strategy

Due to dependencies between stories:
1. Team completes Setup + Foundational together
2. Complete User Stories 1-3 (MVP) → Test → Deploy
3. Add User Story 4 → Test → Deploy
4. Add User Story 5 → Test → Deploy
5. Polish phase → Final release

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All tasks include exact file paths for clarity
- Follow Constitution principles throughout implementation

---

## Task Summary

- **Total Tasks**: 73
- **Setup Tasks**: 8 (T001-T008)
- **Foundational Tasks**: 8 (T009-T016)
- **User Stories 1-3 Tasks**: 20 (T017-T036) - MVP
- **User Story 4 Tasks**: 8 (T037-T044)
- **User Story 5 Tasks**: 17 (T045-T061)
- **Polish Tasks**: 12 (T062-T073)

**Parallel Opportunities**: 
- Setup phase: 5 parallel tasks
- Foundational phase: 5 parallel tasks
- User Stories 1-3: Multiple parallel model and test tasks
- Polish phase: 11 parallel tasks

**MVP Scope**: User Stories 1-3 (Phases 1-3) - Complete analysis functionality with sentiment and trend analysis
