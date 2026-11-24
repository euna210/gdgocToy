import json
import sys
from pathlib import Path
from services.posting import analyze_text

BASE = Path(__file__).parent
DEFAULT = BASE / "data" / "samples" / "01.txt"

path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
if not path.exists():
    raise SystemExit(f"공고 파일이 없어요: {path}\n사용법: python run_sample.py 파일경로")

text = path.read_text(encoding="utf-8")
print(json.dumps(analyze_text(text), ensure_ascii=False, indent=2))