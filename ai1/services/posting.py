import os
from datetime import date
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import ValidationError
from schemas import PostingOut
import time
from google.genai import errors

BASE = Path(__file__).parent.parent  # ai1 폴더
load_dotenv(BASE / ".env")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
PROMPT = (BASE / "prompts" / "posting_extract_v1.txt").read_text(encoding="utf-8")
MAX_TRY = 3  # 첫 시도 + 재시도 2회

def _call_llm(contents):
    """서버 혼잡(503 등)일 때만 최대 3번까지 간격을 두고 재시도"""
    for attempt in range(1, 4):
        try:
            return client.models.generate_content(
                model=MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=PostingOut,
                    temperature=0,
                ),
            )
        except errors.APIError as e:
            if e.code not in (429, 500, 503, 504) or attempt == 3:
                raise
            print(f"서버 응답 지연({e.code}), {5 * attempt}초 뒤 재시도 ({attempt}/3)")
            time.sleep(5 * attempt)

def analyze_text(text: str, link: str | None = None, source_format: str = "text") -> dict:
    prompt = PROMPT.replace("{today}", date.today().isoformat())
    contents = f'{prompt}\n\n[공고 본문]\n"""\n{text[:20000]}\n"""'

    last_error = None
    for _ in range(MAX_TRY):
        response = _call_llm(contents)
        try:
            result = PostingOut.model_validate_json(response.text)
            data = result.model_dump()
            extra = result.extra.model_dump(exclude_none=True) if result.extra else {}
            data["extra"] = extra or None
            data["link"] = link
            data["source_format"] = source_format
            return data
        except (ValidationError, ValueError, TypeError) as e:
            last_error = e  # 형식 오류면 다시 시도
    raise ValueError(f"추출 실패: {last_error}")