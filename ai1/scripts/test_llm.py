import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

load_dotenv(Path(__file__).parent.parent / ".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise SystemExit(".env에서 GEMINI_API_KEY를 읽지 못했어요. 파일 위치와 내용을 확인하세요.")

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=30000),  # 30초 (밀리초 단위)
)

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
PROMPT = "이 문장에서 마감일만 알려줘: 접수 기간은 12월 1일부터 12월 20일 18시까지입니다."

print("사용 모델:", MODEL)

for attempt in range(1, 4):
    print(f"{attempt}번째 호출 시작...")
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=PROMPT,
            config=types.GenerateContentConfig(max_output_tokens=1024),
        )
        print("응답:", response.text)
        break
    except Exception as e:
        print(f"{attempt}번째 실패: {type(e).__name__}: {e}")
        if attempt < 3:
            time.sleep(5 * attempt)