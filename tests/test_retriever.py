# tests/test_retriever.py
import pytest
from unittest.mock import patch
from engine.retriever import retrieve_unified_context

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
            (0.6, "RAG: 이 정보는 점수가 낮아 필터링되어야 함."), # 0.7 미만
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