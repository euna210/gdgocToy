from typing import Literal, Optional
from pydantic import BaseModel

Tag = Literal["IT/개발", "디자인", "마케팅", "경영/창업", "공학", "인문/사회", "예술/콘텐츠", "기타"]

class Extra(BaseModel):
    prize_detail: Optional[str] = None
    theme: Optional[str] = None
    work_location: Optional[str] = None
    work_schedule: Optional[str] = None
    pay: Optional[str] = None
    amount: Optional[str] = None
    selection_count: Optional[int] = None
    gpa_requirement: Optional[str] = None

class PostingOut(BaseModel):
    type: Literal["공모전", "인턴십", "장학금", "대외활동"]
    title: str
    organizer: Optional[str] = None
    apply_start: Optional[str] = None
    deadline: Optional[str] = None
    deadline_type: Literal["날짜", "상시", "미정"]
    deadline_note: Optional[str] = None
    tags: list[Tag] = []
    summary: Optional[str] = None
    eligibility_text: list[str] = []
    min_grade: Optional[int] = None
    allowed_majors: list[str] = []
    preferred: list[str] = []
    required_documents: list[str] = []
    benefits: Optional[str] = None
    activity_period: Optional[str] = None
    extra: Optional[Extra] = None