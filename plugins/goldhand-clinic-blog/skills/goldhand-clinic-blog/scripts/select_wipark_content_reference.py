#!/usr/bin/env python3
"""Select one reviewed Wipark post for topic/content, never for voice."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_BRIEFS = SKILL_DIR / "assets" / "wipark-content-briefs.json"
DEFAULT_PROFILES = SKILL_DIR / "assets" / "reference-master-profiles.json"
VOICE_PROFILE_ID = "goldhand-official-voice-v1"


def default_state_path() -> Path:
    override = os.environ.get("GOLDHAND_STATE_FILE", "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return Path.home() / ".codex" / "state" / "goldhand-clinic-blog" / "recent-articles.json"


def tokens(value: str) -> set[str]:
    stop = {"광주", "한의원", "금손한의원", "추천", "정보", "관련", "가지"}
    return {
        item
        for item in re.findall(r"[0-9A-Za-z가-힣]{2,}", value.lower())
        if item not in stop
    }


def recent_master_ids(state: dict[str, Any]) -> set[str]:
    entries = state.get("entries", [])
    if not isinstance(entries, list):
        return set()
    result: set[str] = set()
    for item in entries[:3]:
        if not isinstance(item, dict):
            continue
        for key in ("editorialMasterId", "writingMasterId", "topicSourceId"):
            value = str(item.get(key, ""))
            match = re.search(r"(?:INFO\d+|WP\d{12})", value)
            if not match:
                continue
            found = match.group(0)
            if found.startswith("WP"):
                result.add(found.replace("WP", "INFO", 1))
            else:
                result.add(found)
    return result


def select(
    keyword: str,
    topic: str,
    briefs: dict[str, Any],
    profiles: dict[str, Any],
    state: dict[str, Any],
    *,
    count: int = 1,
    seed: str = "",
) -> list[dict[str, Any]]:
    query_tokens = tokens(f"{keyword} {topic}")
    recent = recent_master_ids(state)
    candidates: list[tuple[int, int, str, dict[str, Any]]] = []
    for master_id, brief in briefs.get("briefs", {}).items():
        if master_id in recent or master_id not in profiles.get("profiles", {}):
            continue
        profile = profiles["profiles"][master_id]
        haystack = " ".join(
            [
                str(brief.get("topic", "")),
                *[str(value) for value in brief.get("readerConcerns", [])],
                *[str(value) for value in brief.get("orderedGeneralInformation", [])],
                *[str(value) for value in profile.get("selectionTags", [])],
            ]
        )
        overlap = len(query_tokens & tokens(haystack))
        broad_bonus = 2 if not query_tokens and master_id == "INFO01" else 0
        stable = int(hashlib.sha256(f"{seed}|{keyword}|{topic}|{master_id}".encode()).hexdigest(), 16)
        candidates.append((overlap + broad_bonus, -stable, master_id, brief))
    candidates.sort(reverse=True)
    selected: list[dict[str, Any]] = []
    for _, _, master_id, brief in candidates[:count]:
        profile = profiles["profiles"][master_id]
        post_id = re.search(r"/(\d{12})$", str(brief["sourceUrl"]))
        selected.append(
            {
                "masterId": master_id,
                "editorialMasterId": f"WP{post_id.group(1)}" if post_id else "",
                "sourceTitle": profile["sourceTitle"],
                "sourceUrl": brief["sourceUrl"],
                "sourceBlogId": "wi-parkclinic",
                "sourceRole": "topic-reader-concerns-general-information-sequence-only",
                "topic": brief["topic"],
                "readerConcerns": brief["readerConcerns"],
                "orderedGeneralInformation": brief["orderedGeneralInformation"],
                "blockedFromSource": brief["blockedFromSource"],
                "sourceToneBlocked": True,
                "voiceProfileId": VOICE_PROFILE_ID,
                "voiceAuthority": "goldhand7582_ official 74-post voice corpus",
                "designSystemId": "goldhand-naver-native-v4",
            }
        )
    return selected


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keyword", required=True)
    parser.add_argument("--topic", default="")
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--seed", default="")
    parser.add_argument("--briefs", type=Path, default=DEFAULT_BRIEFS)
    parser.add_argument("--profiles", type=Path, default=DEFAULT_PROFILES)
    parser.add_argument("--state", type=Path, default=default_state_path())
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        briefs = json.loads(args.briefs.read_text(encoding="utf-8"))
        profiles = json.loads(args.profiles.read_text(encoding="utf-8"))
        state = json.loads(args.state.read_text(encoding="utf-8")) if args.state.exists() else {"entries": []}
        results = select(
            args.keyword,
            args.topic,
            briefs,
            profiles,
            state,
            count=max(1, min(args.count, 3)),
            seed=args.seed,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError) as exc:
        print(f"레퍼런스 선택 실패: {exc}")
        return 2
    if not results:
        print(json.dumps({"status": "blocked", "reason": "최근 3개와 겹치지 않는 검토 완료 정보글이 없습니다."}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(results[0] if len(results) == 1 else results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
