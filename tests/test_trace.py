import json
import unittest
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

from repomind.runtime.trace import save_trace


@dataclass
class FakeTraceItem:
    path: str
    score: int


class TestTrace(unittest.TestCase):
    def test_save_trace_writes_json_file(self):
        with TemporaryDirectory() as tmp:
            path = save_trace(
                tmp,
                {
                    "question": "登录功能怎么实现？",
                    "answer": "涉及文件：auth.py",
                },
            )

            self.assertTrue(path.exists())
            self.assertEqual(path.parent, Path(tmp))

            data = json.loads(path.read_text(encoding="utf-8"))

            self.assertEqual(data["question"], "登录功能怎么实现？")
            self.assertEqual(data["answer"], "涉及文件：auth.py")

    def test_save_trace_serializes_dataclasses_and_paths(self):
        with TemporaryDirectory() as tmp:
            source_path = Path(tmp) / "auth.py"

            path = save_trace(
                tmp,
                {
                    "item": FakeTraceItem(path="auth.py", score=3),
                    "source_path": source_path,
                },
            )

            data = json.loads(path.read_text(encoding="utf-8"))

            self.assertEqual(data["item"], {"path": "auth.py", "score": 3})
            self.assertEqual(data["source_path"], str(source_path))
