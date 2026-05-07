import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from repomind.runtime.trace import save_trace


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
