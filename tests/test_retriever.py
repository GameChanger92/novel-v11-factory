# tests/test_retriever.py
import pytest
from unittest.mock import patch
from engine.retriever import retrieve_unified_context, _count_tokens


@pytest.fixture
def mock_retrievers():
    """ KG와 RAG 검색 함수를 모킹(가짜 함수로 대체)합니다. """
    with patch('engine.retriever.search_kg_for_character_status') as mock_kg, \
         patch('engine.retriever.search_rag_by_query') as mock_rag:

        # 가짜 반환값 설정
        mock_kg.return_value = "KG: 성훈은 E등급 헌터이다."
        mock_rag.return_value = [
            (0.9, "RAG: 어두운 동굴에서 빛나는 검을 발견했다."),
            (0.8, "RAG: 유진은 성훈을 걱정스럽게 바라보았다."),
            (0.6, "RAG: 이 정보는 점수가 낮아 필터링되어야 함."),  # 0.7 미만
        ]
        yield mock_kg, mock_rag


@pytest.fixture
def mock_retrievers_for_budget():
    """ 토큰 예산 테스트용 mock 데이터 """
    with patch('engine.retriever.search_kg_for_character_status') as mock_kg, \
         patch('engine.retriever.search_rag_by_query') as mock_rag:

        # 더 긴 텍스트로 토큰 예산 테스트
        mock_kg.return_value = ("KG: This is a very long knowledge graph "
                                "result that should consume many tokens when "
                                "counted by the tiktoken library for testing "
                                "purposes.")
        mock_rag.return_value = [
            (0.9, "RAG: This is the first RAG result with moderate "
                  "length text that contains enough words to test token "
                  "counting functionality properly."),
            (0.8, "RAG: This is the second RAG result which is also "
                  "quite lengthy and should add significant tokens to "
                  "the total count."),
            (0.75, "RAG: Third result with additional text content for "
                   "comprehensive token budget testing scenarios."),
        ]
        yield mock_kg, mock_rag


def test_retrieve_unified_context(mock_retrievers):
    """ 통합 리트리버가 결과를 잘 조합하고 정렬하는지 테스트 """
    mock_kg, mock_rag = mock_retrievers

    result = retrieve_unified_context(
        project='TestProject',
        character_name='성훈',
        query='동굴에서 뭘 찾았나?',
        top_k=5
    )

    # 1. 반환된 결과의 개수 확인 (KG 1개 + RAG 2개 = 3개)
    assert len(result) == 3

    # 2. KG 결과가 가장 먼저(가장 중요하므로) 오는지 확인
    assert result[0] == "KG: 성훈은 E등급 헌터이다."

    # 3. 점수가 낮은 RAG 결과가 필터링되었는지 확인
    assert "필터링되어야 함" not in "".join(result)

    # 4. 내부 함수들이 올바른 인자와 함께 호출되었는지 확인
    mock_kg.assert_called_once_with('TestProject', '성훈')
    mock_rag.assert_called_once_with('TestProject', '동굴에서 뭘 찾았나?', k=10)


def test_token_counting():
    """ 토큰 카운팅 함수가 올바르게 작동하는지 테스트 """
    # 간단한 텍스트의 토큰 수 테스트
    text = "Hello world, this is a test."
    token_count = _count_tokens(text)

    # tiktoken을 사용한 토큰 수는 정확해야 함 (대략적인 값 확인)
    assert isinstance(token_count, int)
    assert token_count > 0
    assert token_count < 20  # 이 정도 길이면 20 토큰을 넘지 않을 것


def test_retrieve_unified_context_with_budget(mock_retrievers_for_budget):
    """ 토큰 예산이 적용된 컨텍스트 검색 테스트 """
    mock_kg, mock_rag = mock_retrievers_for_budget

    # 작은 예산으로 제한 테스트 (약 50 토큰)
    small_budget = 50
    result = retrieve_unified_context(
        project='TestProject',
        character_name='성훈',
        query='동굴에서 뭘 찾았나?',
        top_k=5,
        budget=small_budget
    )

    # 1. 결과가 예산 내에서만 반환되는지 확인
    total_tokens = sum(_count_tokens(text) for text in result)
    assert total_tokens <= small_budget

    # 2. 최소한 하나의 결과는 있어야 함 (KG 결과가 예산 내라면)
    assert len(result) >= 1

    # 3. KG 결과가 가장 우선순위가 높으므로 첫 번째로 와야 함
    if result:
        assert "KG:" in result[0]


def test_retrieve_unified_context_without_budget(mock_retrievers):
    """ 예산이 없을 때 기존 로직이 유지되는지 테스트 """
    mock_kg, mock_rag = mock_retrievers

    # 예산 없이 호출
    result_no_budget = retrieve_unified_context(
        project='TestProject',
        character_name='성훈',
        query='동굴에서 뭘 찾았나?',
        top_k=5
    )

    # budget=None으로 명시적 호출
    result_none_budget = retrieve_unified_context(
        project='TestProject',
        character_name='성훈',
        query='동굴에서 뭘 찾았나?',
        top_k=5,
        budget=None
    )

    # 두 결과가 동일해야 함 (기존 로직 유지)
    assert result_no_budget == result_none_budget
