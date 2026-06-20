#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""获取 A 股指数和板块数据，生成每日复盘草稿。"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Any

import requests


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT_DIR / "docs" / "strategy"
DEFAULT_TEMPLATE_PATH = ROOT_DIR / "templates" / "daily-market-template.md"
REQUEST_TIMEOUT = 10

INDEX_URL = "https://push2.eastmoney.com/api/qt/ulist.np/get"
SECTOR_URL = "https://push2.eastmoney.com/api/qt/clist/get"
INDEX_CODES = "1.000001,0.399001,0.399006,1.000300,1.000688"
INDEX_NAMES = {
    "000001": "上证指数",
    "399001": "深证成指",
    "399006": "创业板指",
    "000300": "沪深300",
    "000688": "科创50",
}


def fetch_json(
    session: Any,
    url: str,
    params: dict[str, str | int],
) -> dict[str, Any]:
    """请求并校验 JSON 对象，避免接口异常时生成空白报告。"""
    response = session.get(url, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise ValueError("接口返回内容不是 JSON 对象")
    return payload


def extract_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    data = payload.get("data")
    rows = data.get("diff") if isinstance(data, dict) else None
    if not isinstance(rows, list) or not rows:
        raise ValueError("接口未返回有效行情数据")
    valid_rows = [row for row in rows if isinstance(row, dict)]
    if not valid_rows:
        raise ValueError("接口行情数据格式无效")
    return valid_rows


def format_amount(value: Any) -> str:
    """将以元计的成交额格式化为亿元。"""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return "--"
    return f"{value / 100_000_000:.2f}亿"


def get_index_data(session: Any = requests) -> list[dict[str, Any]]:
    payload = fetch_json(
        session,
        INDEX_URL,
        {
            "fltt": 2,
            "invt": 2,
            "fields": "f2,f3,f4,f6,f12,f14",
            "secids": INDEX_CODES,
        },
    )

    result = []
    for item in extract_rows(payload):
        code = str(item.get("f12", ""))
        result.append(
            {
                "name": INDEX_NAMES.get(code, str(item.get("f14") or code)),
                "close": item.get("f2", "--"),
                "change": item.get("f4", "--"),
                "pct": item.get("f3", "--"),
                "amount": format_amount(item.get("f6")),
            }
        )
    return result


def get_sector_data(session: Any = requests) -> list[dict[str, Any]]:
    payload = fetch_json(
        session,
        SECTOR_URL,
        {
            "pn": 1,
            "pz": 20,
            "po": 1,
            "np": 1,
            "fltt": 2,
            "invt": 2,
            "fid": "f3",
            "fs": "m:90+t:2+f:!50",
            "fields": "f3,f14",
        },
    )

    return [
        {
            "name": item.get("f14", "--"),
            "change": item.get("f3", "--"),
        }
        for item in extract_rows(payload)[:3]
    ]


def render_report(
    template: str,
    index_data: list[dict[str, Any]],
    sector_data: list[dict[str, Any]],
    generated_at: datetime,
) -> str:
    report = template.replace("{{日期}}", generated_at.strftime("%Y-%m-%d"))
    report = report.replace(
        "{{YYYY-MM-DD HH:MM}}", generated_at.strftime("%Y-%m-%d %H:%M")
    )

    for item in index_data:
        pattern = f"| {item['name']} | | | | |"
        replacement = (
            f"| {item['name']} | {item['close']} | {item['change']} | "
            f"{item['pct']}% | {item['amount']} |"
        )
        report = report.replace(pattern, replacement, 1)

    for rank, item in enumerate(sector_data, 1):
        pattern = f"| {rank} | | | | |"
        replacement = f"| {rank} | {item['name']} | {item['change']}% | 待核验 | 待核验 |"
        report = report.replace(pattern, replacement, 1)

    return report


def generate_report(
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    template_path: Path = DEFAULT_TEMPLATE_PATH,
    generated_at: datetime | None = None,
    session: Any = requests,
) -> Path:
    generated_at = generated_at or datetime.now()
    template = template_path.read_text(encoding="utf-8")
    report = render_report(
        template,
        get_index_data(session),
        get_sector_data(session),
        generated_at,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"daily-report-{generated_at:%Y-%m-%d}.md"
    output_path.write_text(report, encoding="utf-8")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="报告输出目录",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=DEFAULT_TEMPLATE_PATH,
        help="复盘模板路径",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        output_path = generate_report(args.output_dir, args.template)
    except (OSError, ValueError, requests.RequestException) as exc:
        print(f"生成失败：{exc}")
        return 1

    print(f"报告已生成：{output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
