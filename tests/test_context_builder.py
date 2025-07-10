# tests/test_context_builder.py
from unittest.mock import patch, MagicMock
from engine.context_builder import build_final_prompt_context


def test_build_final_prompt_context():
    """ ContextBuilder가 retriever 결과를 잘 포맷하는지 테스트 """
    # retrieve_unified_context 함수를 가짜 함수로 대체
    mock_retrieved_data = [
        "1. KG 정보입니다.",
        "2. RAG 정보입니다."
    ]

    # Settings mock 생성
    mock_settings = MagicMock()
    mock_settings.SAFE_TRIM_BUDGET = 200000  # 예시 예산값

    with patch('engine.context_builder.retrieve_unified_context', return_value=mock_retrieved_data) as mock_retrieve, \
         patch('engine.context_builder.get_settings', return_value=mock_settings) as mock_get_settings:

        final_prompt = build_final_prompt_context(
            project='Test',
            episode_id='EP001',
            character_name='테스트캐릭',
            plot_query='테스트쿼리'
        )

        # 1. settings 함수가 호출되었는지 확인
        mock_get_settings.assert_called_once()

        # 2. retriever가 올바른 인자로 호출되었는지 확인 (이제 budget 포함)
        mock_retrieve.assert_called_once_with(
            project='Test',
            character_name='테스트캐릭',
            query='테스트쿼리',
            top_k=5,
            budget=200000
        )

        # 3. 최종 프롬프트에 제목과 내용이 잘 포함되었는지 확인
        assert "[중요 배경 정보]" in final_prompt
        assert "1. KG 정보입니다." in final_prompt
        assert "2. RAG 정보입니다." in final_prompt
