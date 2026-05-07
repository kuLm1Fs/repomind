from dataclasses import asdict, is_dataclass
from datetime import datetime
import json
from pathlib import Path
from uuid import uuid4

def save_trace(trace_dir : str, data: dict) -> Path:
    Path(trace_dir).mkdir(parents=True, exist_ok= True)

    trace_path = Path(trace_dir) / f"{datetime.now().strftime('%Y%m%d-%H%M%S')} - {uuid4().hex[:8]}.json"

    trace_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, default=_json_default),
        encoding="utf-8",
    )

    return trace_path

def _json_default(value):
    if is_dataclass(value):
        return asdict(value)
    
    if isinstance(value, Path):
        return str(value)

    raise TypeError(f"Object of type {type(value).__name__} is not Json serializable")