#!/usr/bin/env python3
"""Список тегов (country_code) из GeoSite .dat без protoc — только wire-формат protobuf.

Запуск:
  python list_geosite_tags.py [путь/к/файлу.dat]

Без аргумента ищет рядом с собой: GeoSite.dat, geosite_v2fly.dat, zkeen.dat, zkeenip.dat.
"""
from __future__ import annotations

import sys
from pathlib import Path


def read_varint(buf: bytes, pos: int) -> tuple[int, int]:
    r = 0
    s = 0
    while pos < len(buf):
        b = buf[pos]
        pos += 1
        r |= (b & 0x7F) << s
        if (b & 0x80) == 0:
            return r, pos
        s += 7
    raise ValueError("truncated varint")


def skip_field(buf: bytes, pos: int, wire: int) -> int:
    if wire == 0:
        _, pos = read_varint(buf, pos)
    elif wire == 1:
        pos += 8
    elif wire == 2:
        ln, pos = read_varint(buf, pos)
        pos += ln
    elif wire == 5:
        pos += 4
    else:
        raise ValueError(f"unsupported wire type {wire}")
    return pos


def first_string_field1(chunk: bytes) -> str | None:
    """В сообщении GeoSite первое поле 1 — строка country_code."""
    pos = 0
    while pos < len(chunk):
        tag, pos = read_varint(chunk, pos)
        field = tag >> 3
        wire = tag & 7
        if wire == 2:
            ln, pos = read_varint(chunk, pos)
            raw = chunk[pos : pos + ln]
            pos += ln
            if field == 1:
                return raw.decode("utf-8", errors="replace")
        else:
            pos = skip_field(chunk, pos, wire)
    return None


def list_geosite_tags(path: Path) -> list[str]:
    data = path.read_bytes()
    tags: list[str] = []
    pos = 0
    while pos < len(data):
        tag, pos = read_varint(data, pos)
        field = tag >> 3
        wire = tag & 7
        if field == 1 and wire == 2:
            ln, pos = read_varint(data, pos)
            chunk = data[pos : pos + ln]
            pos += ln
            code = first_string_field1(chunk)
            if code:
                tags.append(code)
        else:
            pos = skip_field(data, pos, wire)
    return tags


def main() -> None:
    root = Path(__file__).resolve().parent
    if len(sys.argv) > 1:
        p = Path(sys.argv[1])
        if not p.is_file():
            p = root / sys.argv[1]
        if not p.is_file():
            print(f"Файл не найден: {sys.argv[1]}", file=sys.stderr)
            sys.exit(1)
    else:
        for name in ("GeoSite.dat", "geosite_v2fly.dat", "zkeen.dat", "zkeenip.dat"):
            cand = root / name
            if cand.is_file():
                p = cand
                break
        else:
            print(
                "Укажите путь к .dat: python list_geosite_tags.py geosite_v2fly.dat",
                file=sys.stderr,
            )
            sys.exit(1)
    tags = sorted(set(list_geosite_tags(p)))
    print(f"File: {p.name}  unique tags: {len(tags)}")
    for t in tags:
        print(t)


if __name__ == "__main__":
    main()
