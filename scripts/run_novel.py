# scripts/run_novel.py
"""
E2E (End-to-End) Pilot Runner for GameChanger V11.
This script integrates all core engine components to generate episodes.
"""
import argparse
import os
import pathlib
import time
import random
import csv

# --- 1. 우리가 만든 engine 모듈들을 임포트합니다 ---
# 이제 모든 핵심 기능은 engine 폴더에서 가져옵니다.
from engine.context_builder import build_final_prompt_context
from engine.config import get_settings

# OpenAI 클라이언트 초기화는 그대로 유지합니다.
import openai
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# ---------------------------------------------------

# --- 2. 설정은 이제 config.py에서 가져옵니다 ---
settings = get_settings()
MODEL = "gpt-4o-mini" # 이 부분도 나중에는 settings에서 가져올 수 있습니다.
OUTLEN = 4800
# -----------------------------------------------

# --- 3. 기존의 유틸리티 함수들은 대부분 유지합니다 ---
# 하지만 이제 gpt 함수는 조금 더 안정적으로 만듭니다.
def gpt(prompt, temp=0.7, maxtok=2000):
    """A robust wrapper for the OpenAI API call."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a world-class web novel writer."},
                {"role": "user", "content": prompt},
            ],
            temperature=temp,
            max_tokens=maxtok,
        )
        content = response.choices[0].message.content
        return content.strip() if content else ""
    except Exception as e:
        print(f"❌ GPT API Error: {e}")
        # 오류 발생 시 빈 문자열을 반환하여 파이프라인이 멈추지 않게 합니다.
        return ""

def self_critique_and_refine(text: str) -> str:
    """LLM을 이용해 초고를 스스로 비평하고 개선합니다."""
    ask = "아래 소설 초고를 읽고, 논리적 오류, 캐릭터 붕괴, 또는 지루한 부분을 찾아 전문가처럼 수정해줘. 분량은 원본과 비슷하게 유지해줘."
    prompt = f"{ask}\n\n[초고]\n{text}\n\n[전문가 수정본]\n"
    # self-critique는 품질에 중요하므로 더 좋은 모델을 쓸 수도 있습니다.
    return gpt(prompt, temp=0.4, maxtok=4000)

def summarize(text: str) -> str:
    """생성된 에피소드를 요약합니다."""
    return gpt("아래 글을 400자 내외로 핵심 사건 위주로 요약해줘:\n" + text, temp=0.3, maxtok=400)
# ---------------------------------------------------

# --- 4. 메인 실행 루프를 대대적으로 수정합니다 ---
def run_pilot(project_name: str, total_episodes: int, start_from: int = 1):
    """
    V11 엔진의 모든 구성 요소를 통합하여 파일럿 에피소드를 생성합니다.
    """
    # 프로젝트 경로 설정
    project_dir = pathlib.Path(f"projects/{project_name}")
    ep_dir = project_dir / "episodes"
    sum_dir = project_dir / "summaries"
    ep_dir.mkdir(exist_ok=True)
    sum_dir.mkdir(exist_ok=True)

    # 아웃라인 로드
    outline_path = project_dir / "outline.csv"
    if not outline_path.exists():
        print(f"❌ Error: outline.csv not found for project '{project_name}'")
        return
        
    outline_map = {
        int(r["ep_no"]): r["outline"]
        for r in csv.DictReader(open(outline_path, encoding="utf8"))
    }

    print(f"🚀 Starting 10-episode pilot run for project: '{project_name}'")
    print(f"   - Context Token Budget: {settings.CTX_TOKEN_BUDGET}")
    print("-" * 50)

    for n in range(start_from, total_episodes + 1):
        print(f"🔥 Generating EP{n:03}...")
        
        # 현재 에피소드의 한 줄 줄거리 가져오기
        plot_query = outline_map.get(n, f"{n}화: 시스템의 도움으로 위기를 극복한다.")
        print(f"  - Plot Query: {plot_query}")

        # 1. 새로운 Context Builder 호출!
        # KG와 RAG를 모두 사용하여 지능적인 컨텍스트를 생성합니다.
        print("  - Building context from KG and RAG...")
        context = build_final_prompt_context(
            project=project_name,
            episode_id=f"EP{n:03}",
            character_name="성훈", # 주인공 이름은 나중에 설정에서 가져오도록 개선 가능
            plot_query=plot_query
        )
        print("  - Context built successfully.")

        # 2. 초고 생성
        # 이제 generate_draft 함수가 따로 필요 없고, gpt 함수에 직접 프롬프트를 만듭니다.
        draft_prompt = (
            f"{context}\n\n"
            f"[이번 화 줄거리]: {plot_query}\n\n"
            f"=> 위의 배경 정보와 줄거리를 바탕으로, 주인공 '성훈'의 시점에서 흥미진진한 에피소드 한 편을 약 {OUTLEN}자 분량으로 작성해줘."
            "독자가 다음 화를 결제하고 싶게 만들어야 해. 대화 비중은 50% 정도로 해줘."
        )
        print("  - Generating draft...")
        draft = gpt(draft_prompt, temp=0.7, maxtok=4000)

        if not draft:
            print(f"  - ❌ Draft generation failed for EP{n:03}. Skipping.")
            continue
        print(f"  - Draft generated. (Length: {len(draft)})")
        
        # 3. 편집 및 요약 (기존과 유사)
        print("  - Refining and summarizing...")
        refined_draft = self_critique_and_refine(draft)
        summary = summarize(refined_draft)
        print("  - Refinement and summary complete.")

        # (참고: quick_guard는 아직 너무 단순하여 잠시 비활성화. 나중에 Consistency Guard로 대체)

        # 4. 파일 저장
        (ep_dir / f"EP{n:03}.md").write_text(refined_draft, encoding="utf8")
        (sum_dir / f"EP{n:03}.txt").write_text(summary, encoding="utf8")

        print(f"✅ EP{n:03} saved successfully!")
        print("-" * 50)
        time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run E2E pilot for GameChanger V11.")
    parser.add_argument("--project", type=str, required=True, help="The name of the project.")
    parser.add_argument("--total", type=int, required=True, help="Total number of episodes to generate.")
    args = parser.parse_args()
    
    run_pilot(project_name=args.project, total_episodes=args.total)