import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google.genai import errors
from services.extract import extract_from_url

load_dotenv(Path(__file__).parent / ".env")

from schemas import AnalyzeRequest, PostingResponse
from services.posting import analyze_text

app = FastAPI(title="공고 분석 API (AI 1)")
MOCK = os.getenv("AI_MOCK", "false").lower() == "true"

MOCK_RESULT = {
    "type": "공모전",
    "title": "2026 SW 아이디어 공모전 (샘플)",
    "organizer": "한국정보산업협회",
    "apply_start": "2026-11-01",
    "deadline": "2026-12-31",
    "deadline_type": "날짜",
    "deadline_note": "18시까지",
    "tags": ["IT/개발"],
    "summary": "대학생 대상 SW 아이디어 공모전 (가짜 데이터)",
    "eligibility_text": ["대학(원)생", "팀 구성 가능(최대 4인)"],
    "min_grade": None,
    "allowed_majors": [],
    "preferred": ["관련 수상 경력자"],
    "required_documents": ["참가신청서", "기획서"],
    "benefits": "대상 500만원",
    "activity_period": None,
    "extra": {"prize_detail": "대상 500만원", "theme": "AI 활용 캠퍼스 서비스"},
    "link": "https://example.com/contest/123",
    "source_format": "text",
}


@app.get("/health")
def health():
    return {"status": "ok", "mock": MOCK}


@app.post("/analyze", response_model=PostingResponse)
def analyze(req: AnalyzeRequest):
    if not req.text and not req.url:
        raise HTTPException(status_code=400, detail="url 또는 text가 필요합니다")

    if MOCK:
        return MOCK_RESULT

    link = req.url if req.url and req.url.startswith(("http://", "https://")) else None

    text = req.text
    source_format = "text"
    if not text:
        if not link:
            raise HTTPException(status_code=400, detail="올바른 url 또는 text가 필요합니다")
        try:
            text = extract_from_url(link)
            source_format = "url"
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
        except Exception:
            raise HTTPException(status_code=422, detail="주소에 접속할 수 없습니다")

    try:
        return analyze_text(text, link=link, source_format=source_format)  # ← 바뀜
    except errors.APIError as e:
        raise HTTPException(status_code=503, detail=f"AI 서비스 일시 오류({e.code})")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"분석 결과 형식 오류: {str(e)[:100]}")
    except Exception:
        raise HTTPException(status_code=500, detail="분석 실패")