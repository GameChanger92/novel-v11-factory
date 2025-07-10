# tests/test_context_builder.py
from unittest.mock import patch
from engine.context_builder import build_final_prompt_context

def test_build_final_prompt_context():
    """ ContextBuilder가 retriever 결과를 잘 포맷하는지 테스트 """
    # retrieve_unified_context 함수를 가짜 함수로 대체
    mock_retrieved_data = [
        "1. KG 정보입니다.",
        "2. RAG 정보입니다."
    ]
    with patch('engine.context_builder.retrieve_unified_context', return_value=mock_retrieved_data) as mock_retrieve:
        
        final_prompt = build_final_prompt_context(
            project='Test',
            episode_id='EP001',
            character_name='테스트캐릭',
            plot_query='테스트쿼리'
        )
        
        # 1. retriever가 올바른 인자로 호출되었는지 확인
        mock_retrieve.assert_called_with(
            project='Test',
            character_name='테스트캐릭',
            query='테스트쿼리',
            top_k=5
        )
        
        # 2. 최종 프롬프트에 제목과 내용이 잘 포함되었는지 확인
        assert "[중요 배경 정보]" in final_prompt
        assert "1. KG 정보입니다." in final_prompt
        assert "2. RAG 정보입니다." in final_prompt