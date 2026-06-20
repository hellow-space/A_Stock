import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from scripts import daily_report


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class FakeSession:
    def get(self, url, params, timeout):
        if url == daily_report.INDEX_URL:
            return FakeResponse(
                {
                    "data": {
                        "diff": [
                            {
                                "f2": 3000.12,
                                "f3": 1.23,
                                "f4": 36.45,
                                "f6": 456_000_000_000,
                                "f12": "000001",
                                "f14": "上证指数",
                            }
                        ]
                    }
                }
            )
        return FakeResponse({"data": {"diff": [{"f3": 5.67, "f14": "测试板块"}]}})


class DailyReportTest(unittest.TestCase):
    def test_generate_report_creates_directory_and_fills_market_data(self):
        generated_at = datetime(2026, 6, 20, 15, 30)

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "nested" / "reports"
            output_path = daily_report.generate_report(
                output_dir=output_dir,
                generated_at=generated_at,
                session=FakeSession(),
            )

            content = output_path.read_text(encoding="utf-8")
            self.assertEqual(output_path.name, "daily-report-2026-06-20.md")
            self.assertIn("每日市场复盘 - 2026-06-20", content)
            self.assertIn("| 上证指数 | 3000.12 | 36.45 | 1.23% | 4560.00亿 |", content)
            self.assertIn("| 1 | 测试板块 | 5.67% | 待核验 | 待核验 |", content)

    def test_extract_rows_rejects_empty_payload(self):
        with self.assertRaisesRegex(ValueError, "未返回有效行情数据"):
            daily_report.extract_rows({"data": {"diff": []}})

    def test_extract_rows_rejects_malformed_items(self):
        with self.assertRaisesRegex(ValueError, "行情数据格式无效"):
            daily_report.extract_rows({"data": {"diff": [None, "invalid"]}})


if __name__ == "__main__":
    unittest.main()
