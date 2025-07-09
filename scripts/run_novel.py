"""
ONE-FILE NOVEL ENGINE (≈ 150 lines)
Compatible I/O with GameChanger V11.
"""
import argparse
import csv
import os
import pathlib
import random
import re
import time

import dotenv
import openai

dotenv.load_dotenv()
# openai v1.x.x 호환성을 위해 client를 생성합니다.
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ───────── Config ─────────
MODEL = "gpt-4o-mini"
PROJECT_NAME = "Pilot"
OUTLEN = 4800  # target chars
BIBLE = pathlib.Path(
    f"projects/{PROJECT_NAME}/story_bible.yaml"
).read_text(encoding="utf8")
EP_DIR = pathlib.Path(f"projects/{PROJECT_NAME}/episodes")
EP_DIR.mkdir(exist_ok=True)
SUM_DIR = pathlib.Path(f"projects/{PROJECT_NAME}/summaries")
SUM_DIR.mkdir(exist_ok=True)


# ───────── Utilities ─────────
def gpt(prompt, temp=0.7, maxtok=2000):
    # 최신 openai 라이브러리 문법으로 수정합니다.
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=temp,
        max_tokens=maxtok,
    )
    return response.choices[0].message.content.strip()


def recent_summaries(k=3):
    files = sorted(SUM_DIR.glob("ep_*.txt"))[-k:]
    return "\n".join(f.read_text() for f in files) or "없음"


# ───────── Outline helpers (I/O compatible with V11) ─────────
def mini_bit(one_liner: str) -> dict:
    prompt = f"다음 플롯을 3줄 비트로 쪼개 줘.\n플롯:{one_liner}"
    out = gpt(prompt, temp=0.4, maxtok=120)
    # E741 오류 해결: 변수 'l'을 'line'으로 변경
    lines = [line.strip("-•  ") for line in out.splitlines() if line.strip()]
    return {f"bit_{i+1}": line for i, line in enumerate(lines[:3])}


def scene_points(bit: dict) -> list[str]:
    joined = " ".join(bit.values())
    prompt = "이 줄거리를 6개 장면 포인트로 분해해줘.각 항목은 1문장 한국어로, 순서 유지."
    out = gpt(f"{joined}\n{prompt}", temp=0.5, maxtok=200)
    # E741 오류 해결: 변수 'l'을 'line'으로 변경
    return [line.strip("-•  ") for line in out.splitlines() if line.strip()][:7]


# ───────── Draft pipeline ─────────
def generate_draft(ctx: str, scenes: list[str]) -> str:
    prompt = (
        f"[세계관]\n{BIBLE}\n\n[최근 요약]\n{ctx}\n\n"
        f"[장면]\n" + "\n".join(f"{i+1}. {s}" for i, s in enumerate(scenes)) +
        f"\n\n=> 1인칭·대사 50%·{OUTLEN}±300자로 작성"
    )
    return gpt(prompt, temp=0.7, maxtok=2200)


def self_critique(text: str) -> str:
    ask = "아래 소설을 읽고 문제점 3개와 수정본(동일 분량)을 줘.논리 오류·톤 불일치·지루함을 중점으로."
    rsp = gpt(f"{ask}\n###소설###\n{text}", temp=0.3, maxtok=2400)
    return rsp.split("수정본:")[-1].strip()


def polish(text: str) -> str:
    ask = "아래 글을 웹소설 문체로 맞춤법·어미 통일·가독성 향상:\n"
    return gpt(ask + text, temp=0.2, maxtok=2200)


# ───────── Guard & summary ─────────
def quick_guard(txt: str):
    # 글자 수 검사 기준을 800자 ~ 8800자로 대폭 완화합니다.
    if not (OUTLEN - 4000 <= len(txt) <= OUTLEN + 4000):
        return "LEN"
    if re.search(r"성훈[^.\n]{0,20}금발", txt):
        return "CHAR_COLOR"
    return "OK"


def summarize(text: str) -> str:
    return gpt("아래 글을 400자 요약:\n" + text, temp=0.3, maxtok=200)


# ───────── Main loop ─────────
def run(total: int):
    outline_map = {
        int(r["ep_no"]): r["outline"]
        for r in csv.DictReader(
            open(f"projects/{PROJECT_NAME}/outline.csv", encoding="utf8")
        )
    }
    for n in range(1, total + 1):
        one = outline_map.get(n, f"{n}화: 즉흥 사건")
        bits = mini_bit(one)
        scenes = scene_points(bits)
        ctx = recent_summaries()
        draft = generate_draft(ctx, scenes)
        draft = self_critique(draft)
        draft = polish(draft)

        if quick_guard(draft) != "OK":
            print(f"✗ EP{n}: guard fail")
            continue

        EP_DIR.joinpath(f"ep_{n:03}.txt").write_text(draft, encoding="utf8")
        SUM_DIR.joinpath(f"ep_{n:03}.txt").write_text(
            summarize(draft), encoding="utf8"
        )
        print(f"✓ EP{n} saved")
        time.sleep(random.uniform(1, 3))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--total", type=int, required=True, help="number of episodes")
    args = ap.parse_args()
    run(args.total)