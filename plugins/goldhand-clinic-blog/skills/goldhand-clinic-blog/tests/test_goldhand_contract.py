from __future__ import annotations

import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_DIR / "scripts"
GPT_IMAGE_FIXTURE = (SKILL_DIR / "assets" / "gpt-image-test-fixture.png").resolve()


def load_module(name: str):
    path = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"goldhand_{name}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"모듈을 불러올 수 없습니다: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


TITLE_VALIDATOR = load_module("validate_title")
ARTICLE_VALIDATOR = load_module("validate_article")
PAGE_BUILDER = load_module("build_naver_copy_page")
HTML_VALIDATOR = load_module("validate_html")
STATE_RECORDER = load_module("record_article_state")
MEDIA_RECOMMENDER = load_module("recommend_media")
OFFICIAL_MEDIA_SYNC = load_module("sync_official_media_assets")
MASTER_SELECTOR = load_module("select_reference_master")
REFERENCE_VALIDATOR = load_module("validate_reference_reconstruction")
EDITORIAL_FIDELITY_VALIDATOR = load_module("validate_editorial_fidelity")
COPY_OVERLAP_VALIDATOR = load_module("validate_copy_overlap")
TOPIC_SELECTOR = load_module("select_topic_idea")
TOPIC_SOURCE_VALIDATOR = load_module("validate_topic_source_library")
EDITORIAL_PROFILE_VALIDATOR = load_module("validate_editorial_master_profiles")
GOLDHAND_VOICE_VALIDATOR = load_module("validate_goldhand_voice")
WIPARK_CONTENT_SELECTOR = load_module("select_wipark_content_reference")

KEYWORD = "동천동 한의원"
TITLE = f"{KEYWORD} 통증이 반복되는 움직임과 생활 기준"
EDITORIAL_TITLE = f"{KEYWORD} 통증이 반복되는 3가지 기준"
QUESTION_TWO = "다른 검사를 먼저 받아야 하는 신호도 있을까요?"
BODY_OPEN = '<section data-reference-role="body">'


def question_markup(text: str) -> str:
    return (
        '<blockquote data-naver-native-component="quotation" data-reference-role="reader-question" '
        'data-question-source="representative-reader-concern" style="text-align:center;" '
        f'>{text}</blockquote>'
    )


def divider_markup() -> str:
    return '<hr data-naver-native-component="divider" data-reference-role="divider">'


def table_markup(purpose: str, rows: list[list[tuple[str, str]]], *, attributes: str = "") -> str:
    cell_contract = "border:1px solid #D6D6D6;text-align:center;vertical-align:middle;"
    clinic_contract = "width:50%;height:64px;line-height:1.8;word-break:keep-all;" if purpose == "clinic-info" else ""
    row_markup = "".join(
        "<tr>" + "".join(f'<td style="{style}{clinic_contract}{cell_contract}">{text}</td>' for text, style in row) + "</tr>"
        for row in rows
    )
    extra = f" {attributes.strip()}" if attributes.strip() else ""
    return (
        '<table data-naver-native-component="table" '
        'data-native-table-preset="naver-table1-default" '
        f'data-native-table-purpose="{purpose}"{extra} '
        'style="width:100%;border-collapse:collapse;margin-left:auto;margin-right:auto;">'
        f'<tbody>{row_markup}</tbody></table>'
    )


def move_credential_table_before(article: str, destination_pattern: str) -> str:
    credential = re.search(
        r'<table\b(?=[^>]*data-native-table-purpose="credential")[^>]*>.*?</table>',
        article,
        flags=re.I | re.S,
    )
    if credential is None:
        raise AssertionError("테스트 원고에 credential 표가 없습니다.")
    credential_html = credential.group(0)
    without_credential = article[:credential.start()] + article[credential.end():]
    destination = re.search(destination_pattern, without_credential, flags=re.I | re.S)
    if destination is None:
        raise AssertionError(f"credential 표 이동 목적지를 찾지 못했습니다: {destination_pattern}")
    return without_credential[:destination.start()] + credential_html + without_credential[destination.start():]


def insert_after_reference_role(article: str, role: str, fragment: str) -> str:
    role_match = re.search(
        rf'<(?P<tag>[a-z][\w:-]*)\b(?=[^>]*data-reference-role="{re.escape(role)}")[^>]*>.*?</(?P=tag)>',
        article,
        flags=re.I | re.S,
    )
    if role_match is None:
        raise AssertionError(f"테스트 원고에 {role} 역할이 없습니다.")
    return article[:role_match.end()] + fragment + article[role_match.end():]


def insert_after_purpose_table(article: str, purpose: str, fragment: str) -> str:
    table = re.search(
        rf'<table\b(?=[^>]*data-native-table-purpose="{re.escape(purpose)}")[^>]*>.*?</table>',
        article,
        flags=re.I | re.S,
    )
    if table is None:
        raise AssertionError(f"테스트 원고에 {purpose} 표가 없습니다.")
    return article[:table.end()] + fragment + article[table.end():]


def move_purpose_table_before(article: str, purpose: str, destination_pattern: str) -> str:
    table = re.search(
        rf'<table\b(?=[^>]*data-native-table-purpose="{re.escape(purpose)}")[^>]*>.*?</table>',
        article,
        flags=re.I | re.S,
    )
    if table is None:
        raise AssertionError(f"테스트 원고에 {purpose} 표가 없습니다.")
    table_html = table.group(0)
    without_table = article[:table.start()] + article[table.end():]
    destination = re.search(destination_pattern, without_table, flags=re.I | re.S)
    if destination is None:
        raise AssertionError(f"{purpose} 표 이동 목적지를 찾지 못했습니다: {destination_pattern}")
    return without_table[:destination.start()] + table_html + without_table[destination.start():]


def move_reference_role_after_purpose_table(article: str, role: str, purpose: str) -> str:
    role_match = re.search(
        rf'<(?P<tag>[a-z][\w:-]*)\b(?=[^>]*data-reference-role="{re.escape(role)}")[^>]*>.*?</(?P=tag)>',
        article,
        flags=re.I | re.S,
    )
    if role_match is None:
        raise AssertionError(f"테스트 원고에 {role} 역할이 없습니다.")
    role_html = role_match.group(0)
    without_role = article[:role_match.start()] + article[role_match.end():]
    table = re.search(
        rf'<table\b(?=[^>]*data-native-table-purpose="{re.escape(purpose)}")[^>]*>.*?</table>',
        without_role,
        flags=re.I | re.S,
    )
    if table is None:
        raise AssertionError(f"테스트 원고에 {purpose} 표가 없습니다.")
    return without_role[:table.end()] + role_html + without_role[table.end():]


def wrap_first_divider_in_structural_section(article: str) -> str:
    divider = re.search(
        r'<hr\b(?=[^>]*data-naver-native-component="divider")[^>]*>',
        article,
        flags=re.I | re.S,
    )
    if divider is None:
        raise AssertionError("테스트 원고에 첫 divider가 없습니다.")
    return (
        article[:divider.start()]
        + '<section data-editorial-beat="first-information-body">'
        + divider.group(0)
        + "</section>"
        + article[divider.end():]
    )


def mobile_markup(text: str, *, first_role: str = "") -> str:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and len("".join(candidate.split())) > 22:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    if len(lines) == 1:
        midpoint = max(1, len(words) // 2)
        lines = [" ".join(words[:midpoint]), " ".join(words[midpoint:])]
    if len("".join(lines[-1].split())) < 4 and len(lines) > 1:
        merged = f"{lines[-2]} {lines[-1]}"
        if len("".join(merged.split())) <= 24:
            lines[-2:] = [merged]

    sizes: list[int] = []
    remaining = len(lines)
    while remaining:
        if remaining in {2, 3}:
            sizes.append(remaining)
            break
        if remaining == 4:
            sizes.extend([2, 2])
            break
        sizes.append(3)
        remaining -= 3

    parts: list[str] = []
    cursor = 0
    for group_index, size in enumerate(sizes):
        role = f' data-reference-role="{first_role}"' if group_index == 0 and first_role else ""
        group = "<br>".join(lines[cursor:cursor + size])
        cursor += size
        parts.append(
            f'<p data-mobile-group="true"{role} style="margin:0;text-align:center;color:#4D4D4D;font-size:16px;line-height:1.9;word-break:keep-all;">{group}</p>'
        )
        parts.append('<p data-preview-gap="true" aria-hidden="true" style="margin:0;text-align:center;color:transparent;">&#8288;</p>')
    return "".join(parts)


def valid_article() -> str:
    paragraphs = [
        "안녕하세요, 금손한의원 박준희 원장입니다.",
        f"{KEYWORD}을 찾는 분 가운데 같은 자리가 자꾸 불편해지는 이유를 몰라 치료 선택을 망설이는 분이 있습니다. 오늘은 아픈 자리만 볼 때 놓치기 쉬운 움직임과 생활 조건, 다른 검사를 먼저 생각할 신호까지 살펴보며 자신의 상태를 구분할 기준을 정리하겠습니다.",
        "통증은 한 지점에 느껴져도 그 부위만의 문제로 단정하기 어렵습니다. 목을 돌리는 범위, 어깨뼈의 움직임, 골반과 발의 지지처럼 주변 관절이 함께 움직이는 방식을 차분히 비교해야 합니다.",
        "불편이 시작된 날의 활동량과 수면, 오래 유지한 자세도 중요한 단서입니다. 평소와 다른 운동을 했는지, 한쪽 손만 반복해 썼는지, 쉬었을 때와 움직일 때 차이가 있는지를 정리하면 설명이 구체적이 됩니다.",
        f"제가 {KEYWORD} 진료에서 먼저 듣는 것은 증상의 이름보다 생활 속 장면입니다. 같은 어깨 불편이라도 팔을 들 때와 가만히 있을 때의 양상이 다르고, 목이나 등 움직임이 함께 제한되는지도 사람마다 다릅니다.",
        "진찰에서는 좌우의 범위와 힘을 비교하고 몸이 특정 방향을 피하는지 확인합니다. 통증이 강하다는 이유만으로 여러 치료를 한꺼번에 권하기보다 현재 상태에서 무엇이 우선인지 설명하는 과정이 필요합니다.",
        "뼈 손상이나 심한 신경 증상이 의심되면 한의원 치료보다 영상 검사나 다른 의료기관의 평가를 먼저 권할 수 있습니다. 이런 경계를 분명히 하는 것도 환자가 자신의 상태를 안전하게 이해하는 데 필요한 정보입니다.",
        f"{KEYWORD}에서 침이나 추나, 약침을 이야기할 때도 시술 이름부터 나열하지 않습니다. 움직임 제한과 긴장 부위, 생활 속 반복 요인을 구분한 뒤 각 방법을 왜 고려하는지와 선택하지 않아도 되는 상황을 함께 설명합니다.",
        "집에서는 통증을 참으며 큰 동작을 반복하기보다 편안한 범위 안에서 움직임을 관찰해 보세요. 앉는 높이와 화면 위치를 바꾸었을 때 차이가 있는지, 짧게 걸은 뒤 몸이 어떻게 반응하는지 기록하면 다음 상담에 도움이 됩니다.",
        "무리한 스트레칭은 오히려 예민한 부위를 자극할 수 있습니다. 반동을 주지 않고 호흡이 편한 범위에서 시작하며, 저림이나 힘 빠짐처럼 평소와 다른 신호가 나타나면 스스로 판단해 운동을 이어가지 않는 편이 좋습니다.",
        f"저는 {KEYWORD}을 알아보는 분께 치료 횟수보다 먼저 자신의 몸에서 반복되는 조건을 찾으시라고 말씀드립니다. 어떤 자세에서 시작되고 무엇을 바꾸면 덜 불편한지 알면 진료실 밖에서도 관리의 기준을 세울 수 있습니다.",
        "침으로 충분하다고 판단되는 상태라면 비급여 치료를 무리하게 더하지 않습니다. 다른 접근이 필요하다면 그 이유와 예상되는 과정을 설명하고 선택은 환자에게 둔다는 원칙을 지키려 합니다.",
        "한 번의 설명으로 원인이 모두 정리되지 않을 때도 있습니다. 치료 뒤 반응이 예상과 다르거나 회복이 더디다면 처음 판단을 고집하지 않고 움직임과 생활 조건을 다시 살펴 방향을 조정합니다.",
        "진료실에서 설명을 들은 뒤에는 자신의 말로 다시 정리해 보는 과정도 유용합니다. 불편한 위치만 기억하기보다 시작 동작과 지속 시간, 쉬었을 때의 변화를 함께 적어 두면 다음 점검에서 달라진 부분을 비교하기 쉽습니다.",
        "관리 방법은 오래 해야 한다는 부담보다 생활에 붙일 수 있는 작은 변화에서 시작하는 편이 낫습니다. 의자에 앉는 위치를 조정하고 한 자세를 오래 유지하지 않으며, 몸이 보내는 신호를 기준으로 활동 강도를 조절해 보세요.",
        f"결국 {KEYWORD} 선택에서 중요한 것은 화려한 시술 목록보다 자신의 질문에 구체적인 답을 들을 수 있는지입니다. 필요한 경우 의료진과 현재 상태를 상의하며 검사와 관리의 순서를 차분히 정해 보셔도 좋습니다.",
        "몸의 신호를 이해하는 데 이 글이 작은 기준이 되었으면 합니다. 문의가 필요하다면 현재 가장 불편한 동작과 시작 시점, 함께 나타나는 증상을 정리해 알려 주시면 상담 내용을 더 분명하게 나눌 수 있습니다.",
    ]
    credential_table = table_markup(
        "credential",
        [
            [
                ("금손한의원 소개", "background-color:#C99F75;color:#FFFFFF;font-weight:700;"),
            ],
            [
                ("11년차 한의사 · 2016년 개원", "color:#4D4D4D;"),
            ],
            [
                ("통증·체형·움직임·생활습관을 함께 확인", "color:#4D4D4D;"),
            ],
            [
                ("필요한 치료만 설명하는 과잉 권유 없는 진료", "color:#4D4D4D;"),
            ],
            [
                ("골타요법 관련 교육 · 한방비만치료 전문가과정 수료", "color:#4D4D4D;"),
            ],
            [
                ("근골격계부터 소화·호흡기·여성·소아·보약까지 진료", "color:#4D4D4D;"),
            ],
            [
                ("월·수·금 야간 · 토·일·공휴일 진료", "color:#4D4D4D;"),
            ],
        ],
        attributes='data-reference-role="credential-proof" data-goldhand-role="proof"',
    )
    body_parts: list[str] = [
        '<p data-reference-role="greeting-authority" style="margin:0;text-align:center;color:#4D4D4D;font-size:16px;line-height:1.9;word-break:keep-all;">안녕하세요, 금손한의원 박준희 원장입니다.</p>',
        '<p data-preview-gap="true" aria-hidden="true" style="margin:0;text-align:center;color:transparent;">&#8288;</p>',
        '<section data-reference-role="solution-preview">',
        mobile_markup(paragraphs[1]),
        '</section>',
        '<p data-preview-gap="true" aria-hidden="true" style="margin:0;text-align:center;color:transparent;">&#8288;</p>',
        credential_table,
        '<p data-preview-gap="true" aria-hidden="true" style="margin:0;text-align:center;color:transparent;">&#8288;</p>',
    ]
    heading_before = {
        2: "통증 부위보다 먼저 볼 것",
        7: "치료 선택을 설명하는 기준",
        12: "경과를 다시 살피는 이유",
    }
    for index, paragraph in enumerate(paragraphs[2:], start=2):
        if index in heading_before:
            body_parts.append(divider_markup())
            body_parts.append(
                f'<h2 data-naver-native-component="subheading" data-reference-role="section-heading" style="text-align:center;">{heading_before[index]}</h2>'
            )
            body_parts.append('<p data-preview-gap="true" aria-hidden="true" style="margin:0;text-align:center;color:transparent;">&#8288;</p>')
        role = "explanation" if index == 2 else "neutral-close" if index == 16 else ""
        body_parts.append(mobile_markup(paragraph, first_role=role))
    body_parts.append(mobile_markup(
        "아픈 자리만 좇기보다 반복되는 움직임과 생활 조건을 함께 살피는 것이 자신의 상태를 설명할 출발점이 됩니다."
    ))
    body_parts.append(
        table_markup(
            "article-summary",
            [
                [
                    ("살필 조건", "background-color:#C99F75;color:#FFFFFF;font-weight:700;text-align:center;"),
                    ("기록할 내용", "background-color:#C99F75;color:#FFFFFF;font-weight:700;text-align:center;"),
                ],
                [
                    ("한 자세", "background-color:#F3E8DD;color:#7A5434;font-weight:700;text-align:center;"),
                    ("유지 시간과 몸의 위치", "color:#4D4D4D;"),
                ],
                [
                    ("피하는 동작", "background-color:#F3E8DD;color:#7A5434;font-weight:700;text-align:center;"),
                    ("멈추는 지점과 좌우 차이", "color:#4D4D4D;"),
                ],
            ],
        )
    )
    body_parts.append('<p data-preview-gap="true" aria-hidden="true" style="margin:0;text-align:center;color:transparent;">&#8288;</p>')
    body = "".join(body_parts)
    body = body.replace(
        "같은 자리가 자꾸<br>불편해지는 이유를 몰라",
        '<span data-goldhand-emphasis="highlight" style="background-color:#FFF2A8;">같은 자리가 자꾸<br>불편해지는 이유</span>를 몰라',
        1,
    ).replace(
        "통증 부위보다 먼저 볼 것",
        '<u data-reference-underline-role="key-point">통증 부위보다 먼저 볼 것</u>',
        1,
    ).replace(
        "치료 선택을 설명하는 기준",
        '<span data-goldhand-emphasis="highlight" style="background-color:#FFF2A8;">치료 선택을 설명하는 기준</span>',
        1,
    ).replace(
        "경과를 다시 살피는 이유",
        '<u data-reference-underline-role="key-point">경과를 다시 살피는 이유</u>',
        1,
    ).replace(
        "아픈 자리만 좇기보다",
        '<span data-goldhand-emphasis="highlight" style="background-color:#FFF2A8;">아픈 자리만 좇기보다</span>',
        1,
    ).replace(
        "영상 검사나 다른 의료기관의 평가",
        '<span data-goldhand-emphasis="red" style="color:#E53935;font-weight:700;">영상 검사나 다른 의료기관의 평가</span>',
        1,
    ).replace(
        "운동을 이어가지 않는 편",
        '<span data-goldhand-emphasis="red" style="color:#E53935;font-weight:700;">운동을 이어가지 않는 편</span>',
        1,
    )
    contact = table_markup(
        "clinic-info",
        [
            [
                ("한의원", "background-color:#F3E8DD;color:#7A5434;font-weight:700;text-align:center;"),
                ("금손한의원", "color:#4D4D4D;"),
            ],
            [
                ("주소", "background-color:#F3E8DD;color:#7A5434;font-weight:700;text-align:center;"),
                ("전남광주통합특별시 서구 유림로98번길 3, 2층", "color:#4D4D4D;"),
            ],
            [
                ("찾아오는 길", "background-color:#F3E8DD;color:#7A5434;font-weight:700;text-align:center;"),
                ("동천파출소·동천동 행정복지센터 건너편", "color:#4D4D4D;"),
            ],
            [
                ("전화", "background-color:#F3E8DD;color:#7A5434;font-weight:700;text-align:center;"),
                ("062-515-7582", "color:#4D4D4D;"),
            ],
            [
                ("문의·예약", "background-color:#F3E8DD;color:#7A5434;font-weight:700;text-align:center;"),
                ("카카오톡에서 @금손한의원 검색 후 채널 문의 · 네이버에서 금손한의원 검색 후 진료 예약", "color:#4D4D4D;"),
            ],
            [
                ("진료시간", "background-color:#F3E8DD;color:#7A5434;font-weight:700;text-align:center;"),
                ("월·수·금 09:30~20:00 · 화·목 09:30~18:00 · 토·일 09:00~13:00 · 공휴일 09:30~18:00 · 설·추석 연휴 휴진", "color:#4D4D4D;"),
            ],
        ],
        attributes='data-goldhand-role="contact" data-reference-role="contact"',
    )
    return f"""
    <article data-goldhand-type="정보전달형" data-master-reference-id="INFO03"
      data-decoration-master-reference-id="INFO03"
      data-reference-source="https://blog.naver.com/wi-parkclinic/224337414108"
      data-goldhand-design-system="goldhand-naver-native-v4"
      style="width:100%;max-width:580px;margin:0 auto;color:#4D4D4D;text-align:center;">
      {question_markup("통증이 반복되는 이유를 아픈 자리에서만 찾아도 될까요?")}
      {question_markup(QUESTION_TWO)}
      {BODY_OPEN}{body}</section>{contact}
    </article>
    """


def editorial_close_article(*, include_summary: bool = True, one_question: bool = False) -> str:
    article = valid_article().replace(
        'data-goldhand-type="정보전달형"',
        'data-goldhand-type="정보전달형" '
        'data-editorial-master-id="BM224231647991" '
        'data-editorial-reference-source="https://blog.naver.com/beomeo_sm/224231647991" '
        'data-editorial-source-role="title-tone-content-sequence-only" '
        'data-editorial-profile-status="ready"',
        1,
    )
    article = article.replace(KEYWORD, "동천동 진료", 2)
    reading_hook = (
        '<p data-reference-role="reading-time-hook" data-reading-minutes="3" data-mobile-group="true" '
        'style="margin:0;text-align:center;color:#4D4D4D;font-size:16px;line-height:1.9;word-break:keep-all;">'
        '팔이 잘 안 올라간다면,<br>딱 3분만 읽어 보세요.</p>'
        '<p data-preview-gap="true" aria-hidden="true" style="margin:0;text-align:center;color:transparent;">&#8288;</p>'
    )
    article = article.replace("</section>", reading_hook + "</section>", 1)
    for index, heading in enumerate(
        ("통증 부위보다 먼저 볼 것", "치료 선택을 설명하는 기준", "경과를 다시 살피는 이유"),
        start=1,
    ):
        article = article.replace(heading, f"{index}. {heading}", 1)
    generated_figure = (
        '<figure data-media-provider="gpt-image" data-image-placement="after-related-paragraph" '
        'data-image-anchor="통증" data-generation-reference-creator="callilife" '
        'data-generation-owner-authorization="user-confirmed" '
        'data-generation-content-preservation="medical-information-layout" '
        'data-generation-variation-mode="person-identity-subtle-variation" '
        'style="text-align:center;">'
        '<img data-media-provider="gpt-image" '
        f'data-local-image="{GPT_IMAGE_FIXTURE}" '
        'data-generation-reference-creator="callilife" '
        'data-generation-reference-url="https://ogqmarket.naver.com/artworks/stockImage/detail?artworkId=623801a0b4e18" '
        'data-generation-owner-authorization="user-confirmed" '
        'data-generation-content-preservation="medical-information-layout" '
        'data-generation-variation-mode="person-identity-subtle-variation" '
        'src="data:," alt="어깨 관절 운동 범위 설명 이미지"></figure>'
    )
    related_paragraph = re.search(
        r'<p\b(?=[^>]*data-mobile-group="true")[^>]*>[^<]*(?:<br>[^<]*)*통증.*?</p>'
        r'\s*<p\b(?=[^>]*data-preview-gap="true")[^>]*>.*?</p>',
        article,
        flags=re.I | re.S,
    )
    if related_paragraph is None:
        raise AssertionError("GPT 이미지 앞에 둘 통증 모바일 문단을 찾지 못했습니다.")
    article = article[:related_paragraph.end()] + generated_figure + article[related_paragraph.end():]
    media_library = json.loads((SKILL_DIR / "assets" / "media-library.json").read_text(encoding="utf-8"))
    media_by_id = {item["id"]: item for item in media_library["assets"]}
    real_photo_slots = (
        ("GH0016", "주변 관절", "원장이 환자에게 침 치료하는 모습"),
        ("GH0017", "활동량", "원장이 환자를 치료하는 모습"),
        ("GH0018", "진찰에서", "원장이 환자와 보호자에게 설명하는 모습"),
        ("GH0020", "뼈 손상", "원장이 환자의 다리 상태를 진찰하는 모습"),
        ("GH0014", "침이나 추나", "원장이 아이의 상태를 살피는 모습"),
        ("GH0015", "한 번의 설명", "원장이 아이와 상담하는 모습"),
    )
    for media_id, anchor, alt_text in real_photo_slots:
        asset = media_by_id[media_id]
        figure = (
            f'<figure data-reference-role="evidence-media" data-goldhand-role="media" '
            f'data-real-photo="true" data-media-origin="goldhand-bundled-official-library" '
            f'data-goldhand-media="{media_id}" data-image-placement="after-related-paragraph" '
            f'data-image-anchor="{anchor}" style="margin:28px auto;text-align:center;max-width:580px;">'
            f'<img src="{asset["url"]}" data-real-photo="true" '
            f'data-media-origin="goldhand-bundled-official-library" data-goldhand-media="{media_id}" '
            f'data-media-sha256="{asset["sha256"]}" '
            f'data-reference-source-url="{asset["url"]}" referrerpolicy="no-referrer" '
            f'alt="{alt_text}" style="display:block;width:100%;height:auto;margin:0 auto;"></figure>'
        )
        paragraph = re.search(
            rf'<p\b(?=[^>]*data-mobile-group="true")[^>]*>.*?{re.escape(anchor)}.*?</p>'
            rf'\s*<p\b(?=[^>]*data-preview-gap="true")[^>]*>.*?</p>',
            article,
            flags=re.I | re.S,
        )
        if paragraph is None:
            raise AssertionError(f"실제 사진 배치 문단을 찾지 못했습니다: {anchor}")
        article = article[:paragraph.end()] + figure + article[paragraph.end():]
    if one_question:
        article = article.replace(question_markup(QUESTION_TWO), "", 1)
    if not include_summary:
        article = re.sub(
            r'<table\b(?=[^>]*data-native-table-purpose="article-summary")[^>]*>.*?</table>',
            "",
            article,
            count=1,
            flags=re.I | re.S,
        )
    return article


def editorial_fidelity_article() -> str:
    beats = [
        "exercise-effort-frustration",
        "exercise-matters-but-is-not-a-direct-calorie-equation",
        "why-weight-loss-can-stall-despite-exercise",
        "exercise-still-matters-for-loss-and-maintenance",
        "practical-management-direction",
    ]
    body = "".join(
        f'<section data-editorial-beat="{beat}">{index}번째 새 금손 설명 문단입니다.</section>'
        for index, beat in enumerate(beats, start=1)
    )
    return (
        '<article data-editorial-master-id="BM224231647991" '
        'data-editorial-reference-source="https://blog.naver.com/beomeo_sm/224231647991" '
        'data-editorial-source-role="title-tone-content-sequence-only" '
        'data-editorial-profile-status="ready" '
        'data-reference-source="https://blog.naver.com/wi-parkclinic/224337414108">'
        f"{body}</article>"
    )


class TitleTests(unittest.TestCase):
    def test_editorial_close_numeric_title_passes(self) -> None:
        result = TITLE_VALIDATOR.validate_title(
            "광주 한의원 추천, 운동해도 살이 안 빠지는 3가지 이유",
            "광주 한의원 추천",
            answer_count=3,
            editorial_close=True,
        )
        self.assertEqual(result["status"], "pass", result)
        self.assertTrue(result["metrics"]["editorialClose"])

    def test_editorial_close_title_without_number_fails(self) -> None:
        result = TITLE_VALIDATOR.validate_title(
            "광주 한의원 추천, 운동하는데 왜 살이 잘 안 빠질까요?",
            "광주 한의원 추천",
            editorial_close=True,
        )
        self.assertIn("title-numeric-hook-missing", {item["code"] for item in result["issues"]})

    def test_valid_title_is_not_blocked(self) -> None:
        evidence = (SKILL_DIR / "references" / "clinic-facts.md").read_text(encoding="utf-8")
        library = json.loads((SKILL_DIR / "assets" / "topic-idea-library.json").read_text(encoding="utf-8"))
        result = TITLE_VALIDATOR.validate_title(
            TITLE,
            KEYWORD,
            evidence=evidence,
            library=library,
            idea_reference_id="WP224205420099",
            pattern_id="how-to-principle",
        )
        self.assertNotEqual(result["status"], "fail", result)

    def test_duplicate_keyword_and_daily_post_fail(self) -> None:
        result = TITLE_VALIDATOR.validate_title(f"{KEYWORD} {KEYWORD} 일상글", KEYWORD)
        codes = {item["code"] for item in result["issues"]}
        self.assertIn("title-keyword-count", codes)
        self.assertIn("daily-post", codes)

    def test_numbered_promise_requires_matching_answer_count(self) -> None:
        title = f"{KEYWORD} 반복 통증을 살피는 세 가지 기준".replace("세 가지", "3가지")
        result = TITLE_VALIDATOR.validate_title(title, KEYWORD, answer_count=2)
        self.assertIn("answer-count-mismatch", {item["code"] for item in result["issues"]})

    def test_reference_business_and_pattern_mismatch_fail(self) -> None:
        library = json.loads((SKILL_DIR / "assets" / "topic-idea-library.json").read_text(encoding="utf-8"))
        result = TITLE_VALIDATOR.validate_title(
            f"{KEYWORD} 위석부부한의원 방식으로 살피는 기준",
            KEYWORD,
            library=library,
            idea_reference_id="WP224205420099",
            pattern_id="warning-consequence",
        )
        codes = {item["code"] for item in result["issues"]}
        self.assertIn("reference-business-leak", codes)
        self.assertIn("title-pattern-mismatch", codes)


class ArticleTests(unittest.TestCase):
    def test_valid_article_passes(self) -> None:
        evidence = (SKILL_DIR / "references" / "clinic-facts.md").read_text(encoding="utf-8")
        result = ARTICLE_VALIDATOR.validate_article(valid_article(), TITLE, KEYWORD, evidence=evidence)
        self.assertEqual(result["status"], "pass", result)
        self.assertEqual(result["metrics"]["bodyKeywordCount"], 5)

    def test_contact_keyword_does_not_change_body_count(self) -> None:
        article = valid_article().replace("금손한의원</td>", f"금손한의원 {KEYWORD}</td>", 1)
        evidence = (SKILL_DIR / "references" / "clinic-facts.md").read_text(encoding="utf-8")
        result = ARTICLE_VALIDATOR.validate_article(article, TITLE, KEYWORD, evidence=evidence)
        self.assertEqual(result["metrics"]["bodyKeywordCount"], 5, result)

    def test_forbidden_claims_fail(self) -> None:
        article = valid_article().replace("작은 기준이 되었으면<br>합니다", "완치를 100% 보장한다고<br>말합니다")
        result = ARTICLE_VALIDATOR.validate_article(article, TITLE, KEYWORD)
        codes = {item["code"] for item in result["issues"]}
        self.assertIn("guarantee", codes)

    def test_beomeo_topic_source_cannot_leak_into_article(self) -> None:
        article = valid_article().replace(
            "몸의 신호",
            "설명한의원 엑소웨이브 https://blog.naver.com/beomeo_sm/224324776990",
            1,
        )
        result = ARTICLE_VALIDATOR.validate_article(article, TITLE, KEYWORD)
        codes = {item["code"] for item in result["issues"]}
        self.assertIn("topic-source-business-leak", codes)
        self.assertIn("topic-source-url-leak", codes)

    def test_duplicate_h1_fails(self) -> None:
        article = valid_article().replace(BODY_OPEN, f"<h1>{TITLE}</h1>{BODY_OPEN}", 1)
        result = ARTICLE_VALIDATOR.validate_article(article, TITLE, KEYWORD)
        self.assertIn("duplicate-title-heading", {item["code"] for item in result["issues"]})

    def test_one_or_four_reader_questions_fail_but_three_passes(self) -> None:
        one = valid_article().replace(
            question_markup(QUESTION_TWO),
            "",
        )
        one_result = ARTICLE_VALIDATOR.validate_article(one, TITLE, KEYWORD)
        self.assertIn("reader-question-count", {item["code"] for item in one_result["issues"]})
        three = valid_article().replace(
            BODY_OPEN,
            question_markup("생활 관리는 어디부터 바꿔야 할까요?") + BODY_OPEN,
            1,
        )
        three_result = ARTICLE_VALIDATOR.validate_article(three, TITLE, KEYWORD)
        self.assertNotIn("reader-question-count", {item["code"] for item in three_result["issues"]})
        four = three.replace(
            BODY_OPEN,
            question_markup("진료 뒤에는 무엇을 기록하면 좋을까요?") + BODY_OPEN,
            1,
        )
        four_result = ARTICLE_VALIDATOR.validate_article(four, TITLE, KEYWORD)
        self.assertIn("reader-question-count", {item["code"] for item in four_result["issues"]})

    def test_solution_preview_is_required_before_body(self) -> None:
        missing = valid_article().replace(' data-reference-role="solution-preview"', "", 1)
        result = ARTICLE_VALIDATOR.validate_article(missing, TITLE, KEYWORD)
        self.assertIn("solution-preview-count", {item["code"] for item in result["issues"]})

    def test_credential_table_is_between_solution_preview_and_first_body_section(self) -> None:
        article = valid_article()
        solution = re.search(
            r'<section\b(?=[^>]*data-reference-role="solution-preview")[^>]*>.*?</section>',
            article,
            flags=re.I | re.S,
        )
        credential = re.search(
            r'<table\b(?=[^>]*data-native-table-purpose="credential")[^>]*>.*?</table>',
            article,
            flags=re.I | re.S,
        )
        first_body_marker = re.search(
            r'<hr\b(?=[^>]*data-naver-native-component="divider")[^>]*>'
            r'|<[a-z][\w:-]*\b(?=[^>]*data-reference-role="section-heading")[^>]*>',
            article,
            flags=re.I | re.S,
        )
        self.assertIsNotNone(solution)
        self.assertIsNotNone(credential)
        self.assertIsNotNone(first_body_marker)
        assert solution is not None and credential is not None and first_body_marker is not None
        self.assertLess(solution.end(), credential.start())
        self.assertLess(credential.end(), first_body_marker.start())
        result = ARTICLE_VALIDATOR.validate_article(article, TITLE, KEYWORD)
        placement_codes = {
            item["code"]
            for item in result["issues"]
            if item["code"].startswith("credential-")
        }
        self.assertEqual(placement_codes, set(), result)
        self.assertEqual(ARTICLE_VALIDATOR.credential_placement_issues(article), [])

    def test_credential_table_before_solution_preview_fails(self) -> None:
        article = move_credential_table_before(
            valid_article(),
            r'<section\b(?=[^>]*data-reference-role="solution-preview")',
        )
        result = ARTICLE_VALIDATOR.validate_article(article, TITLE, KEYWORD)
        self.assertIn("credential-before-solution-preview", {item["code"] for item in result["issues"]})

    def test_credential_table_at_old_end_position_fails(self) -> None:
        article = move_credential_table_before(
            valid_article(),
            r'<table\b(?=[^>]*data-native-table-purpose="clinic-info")',
        )
        result = ARTICLE_VALIDATOR.validate_article(article, TITLE, KEYWORD)
        self.assertIn("credential-after-first-body-marker", {item["code"] for item in result["issues"]})

    def test_credential_gaps_reject_intervening_paragraph_and_image(self) -> None:
        paragraph_article = insert_after_reference_role(
            valid_article(),
            "solution-preview",
            '<p data-mobile-group="true" style="text-align:center;">중간 본문입니다.<br>여기에 오면 안 됩니다.</p>',
        )
        paragraph_result = ARTICLE_VALIDATOR.validate_article(paragraph_article, TITLE, KEYWORD)
        self.assertIn(
            "credential-not-immediately-after-solution-preview",
            {item["code"] for item in paragraph_result["issues"]},
        )

        image_article = insert_after_purpose_table(
            valid_article(),
            "credential",
            '<img src="data:image/png;base64,AA==" alt="중간 이미지">',
        )
        image_result = ARTICLE_VALIDATOR.validate_article(image_article, TITLE, KEYWORD)
        self.assertIn(
            "credential-not-immediately-before-first-body-marker",
            {item["code"] for item in image_result["issues"]},
        )

    def test_intro_role_after_credential_fails(self) -> None:
        for role in ("greeting-authority", "reader-question"):
            with self.subTest(role=role):
                article = move_reference_role_after_purpose_table(
                    valid_article(),
                    role,
                    "credential",
                )
                result = ARTICLE_VALIDATOR.validate_article(article, TITLE, KEYWORD)
                self.assertIn("intro-role-after-credential", {item["code"] for item in result["issues"]})

    def test_empty_structural_wrapper_before_first_divider_is_allowed(self) -> None:
        article = wrap_first_divider_in_structural_section(valid_article())
        result = ARTICLE_VALIDATOR.validate_article(article, TITLE, KEYWORD)
        placement_codes = {
            item["code"]
            for item in result["issues"]
            if item["code"].startswith("credential-") or item["code"] == "intro-role-after-credential"
        }
        self.assertEqual(placement_codes, set(), result)

    def test_reader_questions_are_representative_not_claimed_patient_quotes(self) -> None:
        missing_source = valid_article().replace(
            ' data-question-source="representative-reader-concern"',
            "",
            1,
        )
        result = ARTICLE_VALIDATOR.validate_article(missing_source, TITLE, KEYWORD)
        self.assertIn("reader-question-source-missing", {item["code"] for item in result["issues"]})

    def test_mobile_four_line_group_fails(self) -> None:
        article = valid_article().replace(
            "통증은 한 지점에 느껴져도 그 부위만의 문제로<br>단정하기 어렵습니다. 목을 돌리는 범위, 어깨뼈의",
            "통증은 한 지점에<br>느껴져도 그 부위만의<br>문제로 단정하기 어렵습니다.<br>목을 돌리는 범위, 어깨뼈의",
            1,
        )
        result = ARTICLE_VALIDATOR.validate_article(article, TITLE, KEYWORD)
        self.assertIn("mobile-group-line-count", {item["code"] for item in result["issues"]})

    def test_unmarked_mobile_paragraph_fails(self) -> None:
        article = valid_article().replace(' data-mobile-group="true"', "", 1)
        result = ARTICLE_VALIDATOR.validate_article(article, TITLE, KEYWORD)
        self.assertIn("mobile-group-marker-missing", {item["code"] for item in result["issues"]})

    def test_editorial_close_allows_two_or_three_body_keywords(self) -> None:
        evidence = (SKILL_DIR / "references" / "clinic-facts.md").read_text(encoding="utf-8")
        article = editorial_close_article()
        result = ARTICLE_VALIDATOR.validate_article(
            article,
            EDITORIAL_TITLE,
            KEYWORD,
            evidence=evidence,
            editorial_close=True,
        )
        self.assertEqual(result["status"], "pass", result)
        self.assertEqual(result["metrics"]["bodyKeywordCount"], 3)
        self.assertEqual(result["metrics"]["editorialMasterId"], "BM224231647991")
        self.assertEqual(result["metrics"]["generatedImages"], 1)
        self.assertEqual(result["metrics"]["realPhotos"], 6)

    def test_editorial_close_requires_three_minute_hook(self) -> None:
        article = re.sub(
            r'<p\b(?=[^>]*data-reference-role="reading-time-hook")[^>]*>.*?</p>',
            "",
            editorial_close_article(),
            count=1,
            flags=re.I | re.S,
        )
        result = ARTICLE_VALIDATOR.validate_article(
            article,
            EDITORIAL_TITLE,
            KEYWORD,
            editorial_close=True,
        )
        self.assertIn("reading-time-hook-count", {item["code"] for item in result["issues"]})

    def test_editorial_close_requires_intro_highlight(self) -> None:
        article = editorial_close_article().replace(
            '<span data-goldhand-emphasis="highlight" style="background-color:#FFF2A8;">같은 자리가 자꾸<br>불편해지는 이유</span>',
            "같은 자리가 자꾸<br>불편해지는 이유",
            1,
        )
        result = ARTICLE_VALIDATOR.validate_article(
            article,
            EDITORIAL_TITLE,
            KEYWORD,
            editorial_close=True,
        )
        self.assertIn("intro-highlight-count", {item["code"] for item in result["issues"]})

    def test_editorial_close_rejects_invalid_generated_image_contract(self) -> None:
        article = editorial_close_article().replace(
            'data-generation-owner-authorization="user-confirmed"',
            'data-generation-owner-authorization="missing"',
        ).replace(
            'data-generation-content-preservation="medical-information-layout"',
            'data-generation-content-preservation="missing"',
        ).replace(
            'data-generation-variation-mode="person-identity-subtle-variation"',
            'data-generation-variation-mode="full-replica"',
        )
        result = ARTICLE_VALIDATOR.validate_article(
            article,
            EDITORIAL_TITLE,
            KEYWORD,
            editorial_close=True,
        )
        codes = {item["code"] for item in result["issues"]}
        self.assertIn("generated-owner-authorization-missing", codes)
        self.assertIn("generated-content-preservation-missing", codes)
        self.assertIn("generated-variation-mode-invalid", codes)

    def test_editorial_close_rejects_generated_image_without_related_placement(self) -> None:
        article = editorial_close_article().replace(
            '<figure data-media-provider="gpt-image" data-image-placement="after-related-paragraph" ',
            '<figure data-media-provider="gpt-image" ',
            1,
        ).replace(
            'data-image-anchor="통증"',
            'data-image-anchor="소화"',
            1,
        )
        result = ARTICLE_VALIDATOR.validate_article(
            article,
            EDITORIAL_TITLE,
            KEYWORD,
            editorial_close=True,
        )
        codes = {item["code"] for item in result["issues"]}
        self.assertIn("generated-image-placement-marker", codes)
        self.assertIn("generated-image-anchor-mismatch", codes)

    def test_editorial_close_requires_six_to_twelve_real_photos(self) -> None:
        article = re.sub(
            r'<figure\b(?=[^>]*data-real-photo="true")[^>]*>.*?</figure>',
            "",
            editorial_close_article(),
            count=1,
            flags=re.I | re.S,
        )
        result = ARTICLE_VALIDATOR.validate_article(
            article, EDITORIAL_TITLE, KEYWORD, editorial_close=True,
        )
        self.assertIn("real-photo-count", {item["code"] for item in result["issues"]})

    def test_editorial_close_rejects_real_photo_without_related_placement(self) -> None:
        article = editorial_close_article().replace(
            'data-real-photo="true" data-media-origin="goldhand-bundled-official-library" '
            'data-goldhand-media="GH0016" data-image-placement="after-related-paragraph"',
            'data-real-photo="true" data-media-origin="goldhand-bundled-official-library" '
            'data-goldhand-media="GH0016"',
            1,
        )
        result = ARTICLE_VALIDATOR.validate_article(
            article, EDITORIAL_TITLE, KEYWORD, editorial_close=True,
        )
        self.assertIn("real-photo-placement-marker", {item["code"] for item in result["issues"]})

    def test_editorial_close_rejects_visible_image_caption(self) -> None:
        article = editorial_close_article().replace(
            "</figure>",
            '<figcaption style="text-align:center;">금손한의원 진료 모습</figcaption></figure>',
            1,
        )
        result = ARTICLE_VALIDATOR.validate_article(
            article, EDITORIAL_TITLE, KEYWORD, editorial_close=True,
        )
        self.assertIn("visible-image-caption-forbidden", {item["code"] for item in result["issues"]})

    def test_editorial_close_rejects_one_reader_question(self) -> None:
        evidence = (SKILL_DIR / "references" / "clinic-facts.md").read_text(encoding="utf-8")
        result = ARTICLE_VALIDATOR.validate_article(
            editorial_close_article(one_question=True),
            EDITORIAL_TITLE,
            KEYWORD,
            evidence=evidence,
            editorial_close=True,
        )
        codes = {item["code"] for item in result["issues"]}
        self.assertIn("reader-question-count", codes, result)
        self.assertNotIn("topic-source-url-leak", codes, result)

    def test_editorial_close_requires_declared_editorial_source(self) -> None:
        result = ARTICLE_VALIDATOR.validate_article(
            valid_article().replace(KEYWORD, "동천동 진료", 2),
            EDITORIAL_TITLE,
            KEYWORD,
            editorial_close=True,
        )
        codes = {item["code"] for item in result["issues"]}
        self.assertIn("editorial-master-id-count", codes)
        self.assertIn("editorial-reference-source-count", codes)

    def test_editorial_close_rejects_unreviewed_candidate_status(self) -> None:
        article = editorial_close_article().replace(
            'data-editorial-profile-status="ready"',
            'data-editorial-profile-status="live-source-audit-required"',
            1,
        )
        result = ARTICLE_VALIDATOR.validate_article(
            article,
            EDITORIAL_TITLE,
            KEYWORD,
            editorial_close=True,
        )
        self.assertIn(
            "editorial-profile-status-not-ready",
            {item["code"] for item in result["issues"]},
        )

    def test_editorial_close_accepts_same_source_wipark_master(self) -> None:
        article = editorial_close_article().replace(
            'data-editorial-master-id="BM224231647991"',
            'data-editorial-master-id="WP224337414108"',
            1,
        ).replace(
            'data-editorial-reference-source="https://blog.naver.com/beomeo_sm/224231647991"',
            'data-editorial-reference-source="https://blog.naver.com/wi-parkclinic/224337414108"',
            1,
        )
        result = ARTICLE_VALIDATOR.validate_article(
            article,
            EDITORIAL_TITLE,
            KEYWORD,
            editorial_close=True,
        )
        codes = {item["code"] for item in result["issues"]}
        self.assertNotIn("editorial-master-id-invalid", codes, result)
        self.assertNotIn("editorial-reference-source-invalid", codes, result)
        self.assertNotIn("editorial-reference-source-prefix-mismatch", codes, result)


class ReferenceMasterTests(unittest.TestCase):
    def profiles(self) -> dict[str, dict[str, object]]:
        data = json.loads((SKILL_DIR / "assets" / "reference-master-profiles.json").read_text(encoding="utf-8"))
        return data["profiles"]

    def test_selector_chooses_one_matching_master(self) -> None:
        result = MASTER_SELECTOR.select(
            self.profiles(),
            "정보전달형",
            "광주 한의원 치료받아도 반복되는 생활습관 2가지",
            "치료 지속과 생활습관",
        )
        self.assertEqual(result["selected"]["id"], "INFO01", result)

    def test_selector_rejects_every_other_content_type(self) -> None:
        with self.assertRaises(ValueError):
            MASTER_SELECTOR.select(self.profiles(), "업체소개형", "광주 한의원", "비교")

    def test_reference_reconstruction_passes(self) -> None:
        result = REFERENCE_VALIDATOR.validate(valid_article(), self.profiles(), "INFO03")
        self.assertEqual(result["status"], "pass", result)

    def test_reference_reconstruction_rejects_credential_before_solution_preview(self) -> None:
        article = move_credential_table_before(
            valid_article(),
            r'<section\b(?=[^>]*data-reference-role="solution-preview")',
        )
        result = REFERENCE_VALIDATOR.validate(article, self.profiles(), "INFO03")
        self.assertEqual(result["status"], "fail")
        self.assertIn("해결 방향 예고가 모두 끝난 뒤", " ".join(result["issues"]))

    def test_reference_reconstruction_rejects_credential_at_old_end_position(self) -> None:
        article = move_credential_table_before(
            valid_article(),
            r'<table\b(?=[^>]*data-native-table-purpose="clinic-info")',
        )
        result = REFERENCE_VALIDATOR.validate(article, self.profiles(), "INFO03")
        self.assertEqual(result["status"], "fail")
        self.assertIn("첫 정보 본문 divider·section-heading보다 앞", " ".join(result["issues"]))

    def test_reference_reconstruction_rejects_summary_between_credential_and_body(self) -> None:
        article = move_purpose_table_before(
            valid_article(),
            "article-summary",
            r'<hr\b(?=[^>]*data-naver-native-component="divider")',
        )
        result = REFERENCE_VALIDATOR.validate(article, self.profiles(), "INFO03")
        self.assertEqual(result["status"], "fail")
        self.assertIn("빈 preview-gap 외의 본문·이미지·표", " ".join(result["issues"]))

    def test_reference_reconstruction_allows_empty_editorial_wrapper_before_body(self) -> None:
        result = REFERENCE_VALIDATOR.validate(
            wrap_first_divider_in_structural_section(valid_article()),
            self.profiles(),
            "INFO03",
        )
        self.assertEqual(result["status"], "pass", result)

    def test_reference_reconstruction_allows_three_reader_questions(self) -> None:
        article = valid_article().replace(
            BODY_OPEN,
            question_markup("생활 관리는 어디부터 바꿔야 할까요?") + BODY_OPEN,
            1,
        )
        result = REFERENCE_VALIDATOR.validate(article, self.profiles(), "INFO03")
        self.assertEqual(result["status"], "pass", result)

    def test_mixed_master_and_legacy_template_fail(self) -> None:
        article = valid_article().replace(
            'data-decoration-master-reference-id="INFO03"',
            'data-decoration-master-reference-id="INFO01"',
        ).replace(
            BODY_OPEN,
            '<header>GOLDHAND CLINIC</header>' + BODY_OPEN,
        )
        result = REFERENCE_VALIDATOR.validate(article, self.profiles())
        self.assertEqual(result["status"], "fail")
        joined = " ".join(result["issues"])
        self.assertIn("글쓰기 흐름 마스터", joined)
        self.assertIn("고정 금손 템플릿", joined)

    def test_source_business_and_noncentered_text_fail(self) -> None:
        article = valid_article().replace("몸의 신호", "위석부부한의원의 신호", 1)
        article = article.replace('style="text-align:center;"', 'style="text-align:left;"', 1)
        result = REFERENCE_VALIDATOR.validate(article, self.profiles(), "INFO03")
        self.assertEqual(result["status"], "fail")
        joined = " ".join(result["issues"])
        self.assertIn("레퍼런스 업체 정보", joined)
        self.assertIn("중앙 정렬", joined)

    def test_beomeo_topic_source_is_not_a_structure_reference(self) -> None:
        article = valid_article().replace(
            'data-reference-source="https://blog.naver.com/wi-parkclinic/224337414108"',
            'data-reference-source="https://blog.naver.com/beomeo_sm/224202473239"',
        )
        result = REFERENCE_VALIDATOR.validate(article, self.profiles(), "INFO03")
        self.assertEqual(result["status"], "fail")
        joined = " ".join(result["issues"])
        self.assertIn("선택한 원문 URL", joined)
        self.assertIn("주제 아이디어 전용", joined)

    def test_native_table_palette_cannot_change(self) -> None:
        article = valid_article().replace("#C99F75", "#FF0010", 1)
        result = REFERENCE_VALIDATOR.validate(article, self.profiles(), "INFO03")
        self.assertEqual(result["status"], "fail")
        self.assertIn("허용 팔레트 밖", " ".join(result["issues"]))

    def test_custom_css_card_fails(self) -> None:
        article = valid_article().replace(
            BODY_OPEN,
            '<section data-goldhand-box="fake-card" style="border:1px solid #C99F75;border-radius:12px;">가짜 박스</section>'
            + BODY_OPEN,
            1,
        )
        result = REFERENCE_VALIDATOR.validate(article, self.profiles(), "INFO03")
        self.assertEqual(result["status"], "fail")
        joined = " ".join(result["issues"])
        self.assertIn("data-goldhand-box", joined)
        self.assertIn("border-radius", joined)

    def test_one_cell_fake_table_fails(self) -> None:
        article = valid_article().replace(
            '<td style="background-color:#C99F75;color:#FFFFFF;font-weight:700;text-align:center;border:1px solid #D6D6D6;text-align:center;vertical-align:middle;">기록할 내용</td>',
            '',
            1,
        )
        result = REFERENCE_VALIDATOR.validate(article, self.profiles(), "INFO03")
        self.assertEqual(result["status"], "fail")
        self.assertIn("2~999열", " ".join(result["issues"]))

    def test_missing_table_cell_grid_fails(self) -> None:
        article = valid_article().replace("border:1px solid #D6D6D6;", "", 1)
        result = REFERENCE_VALIDATOR.validate(article, self.profiles(), "INFO03")
        self.assertEqual(result["status"], "fail")
        self.assertIn("회색 구분선", " ".join(result["issues"]))

    def test_non_centered_table_cell_fails(self) -> None:
        article = valid_article().replace("text-align:center;vertical-align:middle;", "text-align:left;vertical-align:top;", 1)
        result = REFERENCE_VALIDATOR.validate(article, self.profiles(), "INFO03")
        self.assertEqual(result["status"], "fail")
        joined = " ".join(result["issues"])
        self.assertIn("가로 중앙 정렬", joined)
        self.assertIn("세로 중앙 정렬", joined)

    def test_unapproved_value_proof_fails(self) -> None:
        article = valid_article().replace("월·수·금 야간 · 토·일·공휴일 진료", "무조건 빠른 치료와 결과 보장", 1)
        result = REFERENCE_VALIDATOR.validate(article, self.profiles(), "INFO03")
        self.assertEqual(result["status"], "fail")
        self.assertIn("후보 선택 없이", " ".join(result["issues"]))

    def test_missing_text_emphasis_fails(self) -> None:
        article = valid_article().replace(
            '<span data-goldhand-emphasis="highlight" style="background-color:#FFF2A8;">',
            "<span>",
            1,
        )
        result = REFERENCE_VALIDATOR.validate(article, self.profiles(), "INFO03")
        self.assertEqual(result["status"], "fail")
        self.assertIn("노란 하이라이트 강조", " ".join(result["issues"]))

    def test_missing_red_safety_emphasis_fails(self) -> None:
        article = valid_article().replace('data-goldhand-emphasis="red"', 'data-goldhand-emphasis="plain"')
        result = REFERENCE_VALIDATOR.validate(article, self.profiles(), "INFO03")
        self.assertEqual(result["status"], "fail")
        self.assertIn("빨간 글씨 강조", " ".join(result["issues"]))

    def test_unequal_clinic_info_columns_fail(self) -> None:
        article = valid_article().replace("width:50%;height:64px;", "width:40%;height:64px;", 1)
        result = REFERENCE_VALIDATOR.validate(article, self.profiles(), "INFO03")
        self.assertEqual(result["status"], "fail")
        self.assertIn("좌우 폭", " ".join(result["issues"]))

    def test_editorial_close_rejects_one_question_even_without_summary(self) -> None:
        article = editorial_close_article(include_summary=False, one_question=True)
        result = REFERENCE_VALIDATOR.validate(
            article,
            self.profiles(),
            "INFO03",
            editorial_close=True,
        )
        self.assertEqual(result["status"], "fail", result)
        self.assertIn("2~3개", " ".join(result["issues"]))

    def test_editorial_close_beomeo_url_is_only_allowed_in_editorial_source(self) -> None:
        allowed = REFERENCE_VALIDATOR.validate(
            editorial_close_article(),
            self.profiles(),
            "INFO03",
            editorial_close=True,
        )
        self.assertNotIn("주제 아이디어 전용", " ".join(allowed["issues"]), allowed)
        leaked = editorial_close_article().replace(
            "몸의 신호",
            "https://blog.naver.com/beomeo_sm/224231647991 몸의 신호",
            1,
        )
        result = REFERENCE_VALIDATOR.validate(
            leaked,
            self.profiles(),
            "INFO03",
            editorial_close=True,
        )
        self.assertIn("주제 아이디어 전용", " ".join(result["issues"]))


class EditorialFidelityTests(unittest.TestCase):
    def profiles(self) -> dict[str, dict[str, object]]:
        return EDITORIAL_FIDELITY_VALIDATOR.load_profiles(
            SKILL_DIR / "assets" / "beomeo-editorial-master-profiles.json"
        )

    def test_required_beats_in_profile_order_pass(self) -> None:
        result = EDITORIAL_FIDELITY_VALIDATOR.validate(
            editorial_fidelity_article(),
            self.profiles(),
            "BM224231647991",
        )
        self.assertEqual(result["status"], "pass", result)
        self.assertEqual(result["metrics"]["beatCount"], 5)

    def test_out_of_order_required_beats_fail(self) -> None:
        article = editorial_fidelity_article()
        left = "exercise-matters-but-is-not-a-direct-calorie-equation"
        right = "why-weight-loss-can-stall-despite-exercise"
        article = article.replace(left, "TEMP-BEAT", 1).replace(right, left, 1).replace("TEMP-BEAT", right, 1)
        result = EDITORIAL_FIDELITY_VALIDATOR.validate(
            article,
            self.profiles(),
            "BM224231647991",
        )
        self.assertEqual(result["status"], "fail")
        self.assertIn("편집 비트 순서", " ".join(result["issues"]))

    def test_beomeo_url_cannot_replace_layout_source(self) -> None:
        article = editorial_fidelity_article().replace(
            'data-reference-source="https://blog.naver.com/wi-parkclinic/224337414108"',
            'data-reference-source="https://blog.naver.com/beomeo_sm/224231647991"',
        )
        result = EDITORIAL_FIDELITY_VALIDATOR.validate(
            article,
            self.profiles(),
            "BM224231647991",
        )
        self.assertEqual(result["status"], "fail")
        self.assertIn("기존 순정 레이아웃 마스터", " ".join(result["issues"]))

    def test_empty_editorial_beat_fails(self) -> None:
        article = editorial_fidelity_article().replace(
            ">5번째 새 금손 설명 문단입니다.</section>",
            "></section>",
            1,
        )
        result = EDITORIAL_FIDELITY_VALIDATOR.validate(
            article,
            self.profiles(),
            "BM224231647991",
        )
        self.assertEqual(result["status"], "fail")
        self.assertIn("실제 본문", " ".join(result["issues"]))


class CopyOverlapTests(unittest.TestCase):
    def test_seven_consecutive_words_fail(self) -> None:
        source = "운동을 시작한 뒤 하루 전체의 식사와 휴식까지 함께 살펴야 합니다."
        draft = "설명 앞부분입니다. 운동을 시작한 뒤 하루 전체의 식사와 휴식까지 함께 살펴야 합니다."
        result = COPY_OVERLAP_VALIDATOR.validate(source, draft)
        self.assertEqual(result["status"], "fail")
        self.assertIn("consecutive-copy-overlap", {item["code"] for item in result["issues"]})

    def test_short_distinctive_source_sentence_copy_fails(self) -> None:
        source = "운동직후의 허기는 저녁식탁의 선택까지 조용히바꿉니다."
        draft = "운동직후의 허기는 저녁식탁의 선택까지 조용히바꿉니다. 다른 설명입니다."
        result = COPY_OVERLAP_VALIDATOR.validate(source, draft)
        self.assertEqual(result["status"], "fail")
        self.assertIn("source-sentence-copy", {item["code"] for item in result["issues"]})

    def test_common_search_phrase_can_be_allowlisted(self) -> None:
        source = "운동을 해도 살이 잘 안 빠지는 이유"
        draft = "운동을 해도 살이 잘 안 빠지는 이유"
        result = COPY_OVERLAP_VALIDATOR.validate(source, draft)
        self.assertEqual(result["status"], "pass", result)


class BuilderTests(unittest.TestCase):
    def test_builder_strips_legacy_visible_image_captions(self) -> None:
        article = editorial_close_article().replace(
            "</figure>",
            '<figcaption style="text-align:center;">금손한의원 건물 외부</figcaption></figure>',
            1,
        )
        cleaned = PAGE_BUILDER.strip_visible_image_captions(article)
        self.assertNotIn("<figcaption", cleaned)
        self.assertNotIn("금손한의원 건물 외부", cleaned)

    def test_builder_preflight_blocks_wrong_credential_position(self) -> None:
        PAGE_BUILDER.validate_credential_placement(valid_article())
        article = move_credential_table_before(
            valid_article(),
            r'<table\b(?=[^>]*data-native-table-purpose="clinic-info")',
        )
        with self.assertRaisesRegex(ValueError, "credential-after-first-body-marker"):
            PAGE_BUILDER.validate_credential_placement(article)

    def test_builder_appends_clickable_blog_photo_and_map_exactly_once(self) -> None:
        article = PAGE_BUILDER.ensure_closing_links(valid_article())
        article = PAGE_BUILDER.ensure_closing_links(article)
        self.assertEqual(article.count('data-goldhand-closing-links="true"'), 1)
        self.assertEqual(article.count('data-goldhand-photo-link="official-blog"'), 1)
        self.assertEqual(article.count('class="se-component se-image'), 1)
        self.assertEqual(article.count('class="se-component se-placesMap'), 1)
        self.assertEqual(article.count('data-module='), 2)
        self.assertEqual(article.count('data-module-v2='), 2)
        self.assertIn("https://blog.naver.com/goldhand7582_", article)
        self.assertIn('data-linktype="img"', article)
        self.assertIn('&quot;linkUse&quot;:&quot;true&quot;', article)
        self.assertIn('&quot;type&quot;:&quot;v2_image&quot;', article)
        self.assertRegex(
            article,
            r'<a\b(?=[^>]*href="https://blog\.naver\.com/goldhand7582_")(?=[^>]*data-linktype="img")[^>]*>\s*<img\b',
        )
        self.assertNotIn("se-oglink", article)
        self.assertNotIn("se-oglink-title", article)
        self.assertNotIn("se-oglink-summary", article)
        self.assertNotIn("se-oglink-url", article)
        self.assertIn("https://map.naver.com/p/entry/place/1598180269", article)
        self.assertIn('data-place-id="1598180269"', article)
        self.assertNotIn("og_270x270.png", article)
        self.assertNotIn("한의원로고", article)
        self.assertRegex(article, r'data-goldhand-closing-links="true"[\s\S]*?</section>\s*</article>$')

    def test_builder_rejects_logo_and_nonperson_actual_photo(self) -> None:
        library = json.loads((SKILL_DIR / "assets" / "media-library.json").read_text(encoding="utf-8"))
        logo = next(item for item in library["assets"] if item["id"] == "GH0069")
        article = valid_article().replace(
            "</article>",
            (
                f'<img data-real-photo="true" data-goldhand-media="{logo["id"]}" '
                f'data-media-sha256="{logo["sha256"]}" '
                f'data-reference-source-url="{logo["url"]}" src="{logo["url"]}"></article>'
            ),
        )
        with self.assertRaisesRegex(ValueError, "원장 치료·진찰·상담 사진이 아니므로"):
            PAGE_BUILDER.validate_person_media_policy(article, library)

    def test_build_page_publishes_local_image_as_https(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            image_path = root / "pixel.png"
            image_path.write_bytes(
                b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
                b"\x00\x00\x00\rIDAT\x08\xd7c\xf8\xcf\xc0\xf0\x1f\x00\x05\x00\x01\xff\x89\x99=\x1d\x00\x00\x00\x00IEND\xaeB`\x82"
            )
            article = valid_article().replace(
                "</article>",
                f'<img src="data:," data-local-image="{image_path}" alt="사용자 이미지" /></article>',
            )
            published = PAGE_BUILDER.publish_local_images(
                article,
                root / "host",
                "https://goldhand-images.example",
                deploy=False,
                verify=False,
            )
            rewritten = PAGE_BUILDER.rewrite_img_tags(article, published)
            self.assertIn("https://goldhand-images.example/media/", rewritten)
            self.assertIn('data-reference-source-url="https://goldhand-images.example/media/', rewritten)
            self.assertNotIn("data:image/png;base64,", rewritten)
            self.assertNotIn("data-local-image", rewritten)
            self.assertEqual(len(list((root / "host" / "media").glob("*.png"))), 1)
            page = PAGE_BUILDER.build_page(TITLE, rewritten)
            self.assertIn("ClipboardItem", page)
            self.assertIn("__goldhandCopyPreview", page)
            result = HTML_VALIDATOR.validate_html(page)
            self.assertEqual(result["status"], "pass", result)

    def test_copy_page_rejects_data_uri_images(self) -> None:
        article = valid_article().replace(
            "</article>",
            '<img src="data:image/png;base64,AA==" alt="지원하지 않는 이미지" /></article>',
        )
        result = HTML_VALIDATOR.validate_html(PAGE_BUILDER.build_page(TITLE, article))
        self.assertIn("naver-rejected-data-image", {item["code"] for item in result["issues"]})

    def test_copy_page_rejects_text_card_or_nonclickable_blog_photo(self) -> None:
        page = PAGE_BUILDER.build_page(TITLE, valid_article())
        nonclickable = page.replace('data-linktype="img"', 'data-linktype="none"', 1)
        nonclickable_result = HTML_VALIDATOR.validate_html(nonclickable)
        self.assertIn(
            "official-blog-photo-link-count",
            {item["code"] for item in nonclickable_result["issues"]},
        )

        text_card = page.replace('class="se-component se-image', 'class="se-component se-oglink', 1)
        text_card = text_card.replace('data-linktype="img"', 'data-linktype="oglink"', 1)
        text_card_result = HTML_VALIDATOR.validate_html(text_card)
        self.assertIn(
            "text-oglink-card-forbidden",
            {item["code"] for item in text_card_result["issues"]},
        )

    def test_editorial_close_page_allows_two_tables_without_summary(self) -> None:
        article = editorial_close_article(include_summary=False).replace(
            '<article data-goldhand-type="정보전달형"',
            '<article data-goldhand-type="정보전달형" data-editorial-mode="close-adaptation"',
            1,
        )
        article = PAGE_BUILDER.rewrite_img_tags(
            article,
            {GPT_IMAGE_FIXTURE: "https://goldhand-images.example/media/gpt.png"},
        )
        page = PAGE_BUILDER.build_page(TITLE, article)
        result = HTML_VALIDATOR.validate_html(page)
        self.assertEqual(result["status"], "pass", result)
        self.assertTrue(result["metrics"]["editorialClose"])

    def test_copy_page_rejects_credential_before_solution_preview(self) -> None:
        article = move_credential_table_before(
            valid_article(),
            r'<section\b(?=[^>]*data-reference-role="solution-preview")',
        )
        result = HTML_VALIDATOR.validate_html(PAGE_BUILDER.build_page(TITLE, article))
        self.assertIn("credential-before-solution-preview", {item["code"] for item in result["issues"]})

    def test_copy_page_rejects_credential_at_old_end_position(self) -> None:
        article = move_credential_table_before(
            valid_article(),
            r'<table\b(?=[^>]*data-native-table-purpose="clinic-info")',
        )
        result = HTML_VALIDATOR.validate_html(PAGE_BUILDER.build_page(TITLE, article))
        self.assertIn("credential-after-first-body-marker", {item["code"] for item in result["issues"]})

    def test_copy_page_rejects_content_in_credential_gaps_and_late_intro(self) -> None:
        mutations = (
            (
                insert_after_reference_role(
                    valid_article(),
                    "solution-preview",
                    '<p data-mobile-group="true" style="text-align:center;">중간 본문입니다.<br>여기에 오면 안 됩니다.</p>',
                ),
                "credential-not-immediately-after-solution-preview",
            ),
            (
                insert_after_purpose_table(
                    valid_article(),
                    "credential",
                    '<img src="data:image/png;base64,AA==" alt="중간 이미지">',
                ),
                "credential-not-immediately-before-first-body-marker",
            ),
            (
                move_purpose_table_before(
                    valid_article(),
                    "article-summary",
                    r'<hr\b(?=[^>]*data-naver-native-component="divider")',
                ),
                "credential-not-immediately-before-first-body-marker",
            ),
            (
                move_reference_role_after_purpose_table(
                    valid_article(),
                    "greeting-authority",
                    "credential",
                ),
                "intro-role-after-credential",
            ),
        )
        for article, expected_code in mutations:
            with self.subTest(expected_code=expected_code):
                result = HTML_VALIDATOR.validate_html(PAGE_BUILDER.build_page(TITLE, article))
                self.assertIn(expected_code, {item["code"] for item in result["issues"]}, result)

    def test_copy_page_allows_empty_editorial_wrapper_before_body(self) -> None:
        article = wrap_first_divider_in_structural_section(valid_article())
        result = HTML_VALIDATOR.validate_html(PAGE_BUILDER.build_page(TITLE, article))
        self.assertEqual(result["status"], "pass", result)


class StateAndMediaTests(unittest.TestCase):
    def test_state_keeps_only_latest_three_without_body(self) -> None:
        state: dict[str, object] = {}
        for index in range(4):
            state = STATE_RECORDER.record(
                state,
                {
                    "title": f"제목{index}",
                    "mainKeyword": f"키워드{index}",
                    "ideaReferenceId": f"WP{index}",
                    "ideaReferenceTitle": f"참고 제목{index}",
                    "ideaReferenceUrl": f"https://blog.naver.com/wi-parkclinic/{index}",
                    "ideaType": "symptom-cause",
                    "titlePatternId": "reason-explained",
                    "writingMasterId": "INFO03",
                    "writingReferenceUrl": "https://blog.naver.com/wi-parkclinic/224337414108",
                    "type": "정보전달형",
                    "writtenAt": f"2026-08-{index + 1:02d}",
                },
            )
        self.assertEqual(len(state["entries"]), 3)
        self.assertNotIn("body", json.dumps(state, ensure_ascii=False))

    def test_state_keeps_editorial_master_provenance(self) -> None:
        entry = {
            "title": "광주 한의원 추천, 운동하는데 왜 살이 잘 안 빠질까요?",
            "mainKeyword": "광주 한의원 추천",
            "ideaReferenceId": "BTI028",
            "ideaReferenceTitle": "운동해도 살이 빠지지 않을 때 생활 점검",
            "ideaReferenceUrl": "https://blog.naver.com/beomeo_sm/224231647991",
            "ideaType": "weight-management",
            "titlePatternId": "natural-question",
            "writingMasterId": "INFO06",
            "writingReferenceUrl": "https://blog.naver.com/wi-parkclinic/224205420099",
            "editorialMasterId": "BM224231647991",
            "editorialReferenceTitle": "대구 린다이어트, 운동을 해도 살이 안 빠지는 이유!",
            "editorialReferenceUrl": "https://blog.naver.com/beomeo_sm/224231647991",
            "editorialSourceRole": "title-tone-content-sequence-only",
            "editorialProfileStatus": "ready",
            "type": "정보전달형",
            "writtenAt": "2026-08-21",
        }
        state = STATE_RECORDER.record({}, entry)
        saved = state["entries"][0]
        self.assertEqual(saved["editorialMasterId"], "BM224231647991")
        self.assertEqual(saved["editorialReferenceUrl"], entry["editorialReferenceUrl"])
        self.assertEqual(saved["editorialSourceRole"], "title-tone-content-sequence-only")

    def test_state_rejects_unreviewed_editorial_candidate(self) -> None:
        entry = {
            "title": "감사 전 후보 글",
            "mainKeyword": "광주 한의원 추천",
            "ideaReferenceId": "BTI011",
            "ideaReferenceTitle": "소화불량 주제",
            "ideaReferenceUrl": "https://blog.naver.com/beomeo_sm/224338019561",
            "ideaType": "symptom-cause",
            "titlePatternId": "natural-question",
            "writingMasterId": "INFO10",
            "writingReferenceUrl": "https://blog.naver.com/wi-parkclinic/224287906098",
            "editorialProfileStatus": "live-source-audit-required",
            "type": "정보전달형",
            "writtenAt": "2026-08-21",
        }
        with self.assertRaisesRegex(ValueError, "감사가 완료되지 않은"):
            STATE_RECORDER.record({}, entry)

    def test_state_removes_legacy_non_information_entries(self) -> None:
        legacy = {
            "entries": [
                {"title": "예전 업체소개형", "type": "업체소개형"},
                {"title": "예전 사례공유형", "type": "사례공유형"},
            ]
        }
        entry = {
            "title": "현재 정보글",
            "mainKeyword": "광주 한의원",
            "ideaReferenceId": "WP224320052203",
            "ideaReferenceTitle": "일자목 거북목",
            "ideaReferenceUrl": "https://blog.naver.com/wi-parkclinic/224320052203",
            "ideaType": "risk-warning",
            "titlePatternId": "reader-commonality-numbered",
            "writingMasterId": "INFO01",
            "writingReferenceUrl": "https://blog.naver.com/wi-parkclinic/224320052203",
            "type": "정보전달형",
            "writtenAt": "2026-08-20",
        }
        result = STATE_RECORDER.record(legacy, entry)
        self.assertEqual([item["type"] for item in result["entries"]], ["정보전달형"])

    def test_state_v3_round_trips_semantic_topic_fields(self) -> None:
        entry = {
            "title": "광주 한의원 추천, 추나요법을 고려하기 전 확인할 기준",
            "mainKeyword": "광주 한의원 추천",
            "ideaReferenceId": "WP224320052203",
            "ideaReferenceTitle": "일자목 거북목",
            "ideaReferenceUrl": "https://blog.naver.com/wi-parkclinic/224320052203",
            "ideaType": "treatment-decision",
            "titlePatternId": "reader-commonality-numbered",
            "writingMasterId": "INFO01",
            "writingReferenceUrl": "https://blog.naver.com/wi-parkclinic/224320052203",
            "type": "정보전달형",
            "writtenAt": "2026-08-20",
            "topicSourceId": "BTI001",
            "topicSourceTitle": "만촌동 한의원, 목·허리 통증, 추나치료가 필요한 경우는 언제일까요?",
            "topicSourceUrl": "https://blog.naver.com/beomeo_sm/224202473239",
            "topicSourceRole": "topic-idea-and-coverage-questions-only",
            "semanticTopicId": "chuna.neck-back-pain.when-to-consider",
            "topicCluster": "chuna",
            "primarySubjectId": "chuna-decision",
            "subjectIds": ["chuna-manual-therapy", "neck-back-pain"],
            "topicIntent": "treatment-decision",
            "dedupeKeys": ["추나요법", "치료선택기준"],
            "realMediaIds": ["GH0001", "GHLABC123"],
            "realMediaHashes": ["abc123"],
        }
        result = STATE_RECORDER.record({}, entry)
        self.assertEqual(result["schemaVersion"], 4)
        self.assertEqual(result["entries"][0]["semanticTopicId"], entry["semanticTopicId"])
        self.assertEqual(result["entries"][0]["subjectIds"], entry["subjectIds"])
        self.assertEqual(result["entries"][0]["realMediaIds"], entry["realMediaIds"])
        self.assertEqual(result["entries"][0]["realMediaHashes"], entry["realMediaHashes"])

    def test_media_never_fills_with_objects_or_duplicate_group(self) -> None:
        library = {
            "assets": [
                {"id": "A", "safeAuto": True, "requiresReview": False, "bundledPath": "assets/gpt-image-test-fixture.png", "sha256": "a", "url": "https://example.com/a.jpg", "sourceTitle": "교통사고 통증", "caption": "ICT 물리치료", "filename": "ICT.jpg", "context": "교통사고", "tokens": ["교통사고"], "tags": ["traffic-accident"], "postOrder": 1, "imageOrder": 1, "sourceLogNo": "1", "duplicateGroup": "same"},
                {"id": "B", "safeAuto": True, "requiresReview": False, "bundledPath": "assets/gpt-image-test-fixture.png", "sha256": "b", "url": "https://example.com/b.jpg", "sourceTitle": "교통사고 통증", "caption": "ICT 물리치료", "filename": "ICT2.jpg", "context": "교통사고", "tokens": ["교통사고"], "tags": ["traffic-accident"], "postOrder": 2, "imageOrder": 1, "sourceLogNo": "2", "duplicateGroup": "same"},
                {"id": "C", "safeAuto": True, "requiresReview": False, "bundledPath": "assets/gpt-image-test-fixture.png", "sha256": "c", "url": "https://example.com/c.jpg", "sourceTitle": "비염", "caption": "보험한약", "filename": "한약.jpg", "context": "비염", "tokens": ["비염"], "tags": ["respiratory"], "postOrder": 3, "imageOrder": 1, "sourceLogNo": "3", "duplicateGroup": ""},
            ]
        }
        result = MEDIA_RECOMMENDER.recommend(
            library,
            topic="교통사고 통증",
            keyword="광주 교통사고 한의원",
            article_type="정보전달형",
            count=6,
            recent_ids=set(),
        )
        self.assertEqual(result["selectedCount"], 0, result)
        self.assertEqual(result["status"], "shortage")

    def test_media_reuses_recent_trust_photos_only_to_reach_six(self) -> None:
        assets = [
            {
                "id": f"T{index}", "safeAuto": True, "requiresReview": False,
                "url": f"https://example.com/trust-{index}.jpg", "sourceTitle": f"원내 신뢰 사진 {index}",
                "caption": f"금손 신뢰 장면 {index}", "filename": f"trust-{index}.jpg", "context": "",
                "tokens": [], "tags": ["clinic-space"], "postOrder": index,
                "imageOrder": 1, "sourceLogNo": str(index), "duplicateGroup": "",
                "bundledPath": "assets/gpt-image-test-fixture.png", "sha256": f"trust-{index}",
                "sceneType": "director-patient-consultation", "personInteraction": True,
                "directorVisible": True, "trustPriority": 100,
            }
            for index in range(1, 8)
        ]
        result = MEDIA_RECOMMENDER.recommend(
            {"assets": assets}, topic="갱년기 증상", keyword="광주 한의원 추천",
            article_type="정보전달형", count=8, recent_ids={"T1", "T2", "T3"},
        )
        self.assertEqual(result["selectedCount"], 6, result)
        self.assertEqual(result["freshCount"], 4, result)
        self.assertEqual(result["fallbackRecentTrustCount"], 2, result)
        self.assertEqual(result["status"], "minimum-complete")
        self.assertTrue(all(item["selectionRole"] == "recent-director-patient-fallback" for item in result["selected"][-2:]))

    def test_media_does_not_reuse_recent_when_six_fresh_photos_exist(self) -> None:
        assets = [
            {
                "id": f"F{index}", "safeAuto": True, "requiresReview": False,
                "url": f"https://example.com/fresh-{index}.jpg", "sourceTitle": f"진료 공간 {index}",
                "caption": f"금손 진료 공간 {index}", "filename": f"fresh-{index}.jpg", "context": "",
                "tokens": [], "tags": ["clinic-space"], "postOrder": index,
                "imageOrder": 1, "sourceLogNo": str(index), "duplicateGroup": "",
                "bundledPath": "assets/gpt-image-test-fixture.png", "sha256": f"fresh-{index}",
                "sceneType": "director-patient-treatment", "personInteraction": True,
                "directorVisible": True, "trustPriority": 100,
            }
            for index in range(1, 9)
        ]
        result = MEDIA_RECOMMENDER.recommend(
            {"assets": assets}, topic="수면 관리", keyword="광주 한의원",
            article_type="정보전달형", count=6, recent_ids={"F1", "F2"},
        )
        self.assertEqual(result["selectedCount"], 6, result)
        self.assertEqual(result["fallbackRecentTrustCount"], 0, result)
        self.assertFalse({"F1", "F2"} & {item["id"] for item in result["selected"]})

    def test_media_prioritizes_director_patient_scenes_over_objects(self) -> None:
        people = [
            {
                "id": f"P{index}", "safeAuto": True, "requiresReview": False,
                "url": f"https://example.com/person-{index}.jpg", "sourceTitle": "방문 진료",
                "caption": "", "filename": f"person-{index}.jpg", "context": "",
                "tokens": [], "tags": ["home-visit"], "postOrder": index,
                "imageOrder": 1, "sourceLogNo": str(index), "duplicateGroup": "",
                "bundledPath": "assets/gpt-image-test-fixture.png", "sha256": f"person-{index}",
                "sceneType": "director-patient-treatment", "personInteraction": True,
                "directorVisible": True, "trustPriority": 100,
            }
            for index in range(1, 7)
        ]
        objects = [
            {
                "id": f"O{index}", "safeAuto": True, "requiresReview": False,
                "url": f"https://example.com/object-{index}.jpg", "sourceTitle": "목 통증 치료",
                "caption": "목 통증 장비", "filename": f"object-{index}.jpg", "context": "목 통증",
                "tokens": ["통증"], "tags": ["physical-therapy"], "postOrder": index + 10,
                "imageOrder": 1, "sourceLogNo": str(index + 10), "duplicateGroup": "",
                "bundledPath": "assets/gpt-image-test-fixture.png", "sha256": f"object-{index}",
            }
            for index in range(1, 7)
        ]
        result = MEDIA_RECOMMENDER.recommend(
            {"assets": people + objects}, topic="목 통증", keyword="광주 한의원 추천",
            article_type="정보전달형", count=6, recent_ids=set(),
        )
        self.assertEqual([item["id"][0] for item in result["selected"]], ["P"] * 6, result)

    def test_all_official_media_is_bundled_inside_plugin(self) -> None:
        library = json.loads((SKILL_DIR / "assets" / "media-library.json").read_text(encoding="utf-8"))
        self.assertEqual(library["schemaVersion"], 2)
        self.assertEqual(library["assetCount"], 113)
        self.assertEqual(library["bundledAssetCount"], 113)
        self.assertEqual(library["safeAutoCount"], 6)
        self.assertEqual(OFFICIAL_MEDIA_SYNC.validate_library(library), [])
        self.assertTrue(all(str(item["bundledPath"]).startswith("assets/official-media/") for item in library["assets"]))
        approved = [item for item in library["assets"] if item.get("safeAuto")]
        self.assertTrue(all(item.get("personInteraction") is True for item in approved))
        self.assertTrue(all(item.get("directorVisible") is True for item in approved))
        self.assertTrue(all(str(item.get("sceneType", "")).startswith("director-patient-") for item in approved))
        self.assertFalse(any(re.search(r"(?:로고|logo)", str(item.get("filename", "")), re.I) for item in approved))


class TopicSourceBoundaryTests(unittest.TestCase):
    def topic_library(self) -> dict[str, object]:
        return json.loads((SKILL_DIR / "assets" / "beomeo-topic-idea-library.json").read_text(encoding="utf-8"))

    def wipark_library(self) -> dict[str, object]:
        return json.loads((SKILL_DIR / "assets" / "topic-idea-library.json").read_text(encoding="utf-8"))

    def editorial_profiles(self) -> dict[str, object]:
        return json.loads((SKILL_DIR / "assets" / "beomeo-editorial-master-profiles.json").read_text(encoding="utf-8"))

    def test_all_69_posts_and_topic_only_boundary_validate(self) -> None:
        library = self.topic_library()
        inventory = TOPIC_SOURCE_VALIDATOR.parse_inventory(SKILL_DIR / "references" / "beomeo-source-inventory.md")
        self.assertEqual(TOPIC_SOURCE_VALIDATOR.validate_library(library, inventory), [])
        self.assertEqual(len(library["sourcePosts"]), 69)
        self.assertEqual(len(library["topicIdeas"]), 29)
        self.assertEqual(
            {item["topicCluster"] for item in library["topicIdeas"]},
            {"chuna", "traffic-accident", "pain", "digestive", "respiratory", "tonic", "growth", "weight-management"},
        )

    def test_topic_source_rejects_structure_fact_and_body_payloads(self) -> None:
        inventory = TOPIC_SOURCE_VALIDATOR.parse_inventory(SKILL_DIR / "references" / "beomeo-source-inventory.md")
        for forbidden_key in ("titlePatternId", "writingMasterId", "bodyText", "claims", "cases", "media"):
            mutated = json.loads(json.dumps(self.topic_library(), ensure_ascii=False))
            mutated["topicIdeas"][0][forbidden_key] = "금지 payload"
            errors = TOPIC_SOURCE_VALIDATOR.validate_library(mutated, inventory)
            self.assertTrue(any(forbidden_key in error for error in errors), (forbidden_key, errors))

    def test_selector_keeps_beomeo_topic_and_wipark_structure_separate(self) -> None:
        result = TOPIC_SELECTOR.select_ideas(
            self.wipark_library(),
            {"entries": []},
            "광주 한의원 추천",
            topic="다이어트 정체기 체성분",
            count=1,
            seed="beomeo-boundary",
            topic_source_library=self.topic_library(),
        )[0]
        self.assertEqual(result["topicSourceBlogId"], "beomeo_sm", result)
        self.assertTrue(result["topicSourceUrl"].startswith("https://blog.naver.com/beomeo_sm/"), result)
        self.assertTrue(result["ideaReferenceUrl"].startswith("https://blog.naver.com/wi-parkclinic/"), result)
        self.assertTrue(result["writingReferenceUrl"].startswith("https://blog.naver.com/wi-parkclinic/"), result)
        self.assertFalse(result["topicSourceControlsTitlePattern"])
        self.assertFalse(result["topicSourceControlsStructure"])

    def test_every_beomeo_topic_is_ready_or_has_one_live_audit_candidate(self) -> None:
        candidates = TOPIC_SELECTOR.external_topic_candidates(self.topic_library())
        statuses = {"ready": 0, "live-source-audit-required": 0}
        for candidate in candidates:
            status = candidate["editorialProfileStatus"]
            self.assertIn(status, statuses)
            statuses[status] += 1
            if status == "ready":
                self.assertTrue(all(candidate[field] for field in (
                    "editorialMasterId",
                    "editorialReferenceTitle",
                    "editorialReferenceUrl",
                    "editorialSourceRole",
                )))
            else:
                self.assertFalse(any(candidate[field] for field in (
                    "editorialMasterId",
                    "editorialReferenceTitle",
                    "editorialReferenceUrl",
                    "editorialSourceRole",
                )))
                self.assertTrue(all(candidate[field] for field in (
                    "editorialCandidateId",
                    "editorialCandidateTitle",
                    "editorialCandidateUrl",
                )))
                self.assertIn(candidate["editorialCandidateId"], candidate["topicSourcePostIds"])
        self.assertEqual(statuses, {"ready": 1, "live-source-audit-required": 28})

    def test_wipark_topic_uses_its_own_same_source_editorial_master(self) -> None:
        library = self.wipark_library()
        source = library["articles"][0]
        candidate = TOPIC_SELECTOR.wipark_topic_candidate(source, library)
        self.assertEqual(candidate["editorialProfileStatus"], "ready")
        self.assertEqual(candidate["editorialMasterId"], source["id"])
        self.assertEqual(candidate["editorialReferenceUrl"], source["sourceUrl"])

    def test_valid_body_reviewed_runtime_profile_promotes_candidate_to_ready(self) -> None:
        topic_library = self.topic_library()
        profiles = self.editorial_profiles()
        runtime = json.loads(json.dumps(profiles, ensure_ascii=False))
        base = json.loads(json.dumps(runtime["profiles"]["BM224231647991"], ensure_ascii=False))
        source = next(item for item in topic_library["sourcePosts"] if item["id"] == "BM224338019561")
        base.update({
            "id": source["id"],
            "sourcePostId": source["sourcePostId"],
            "sourceTitle": source["sourceTitle"],
            "sourceUrl": source["sourceUrl"],
            "appliesToTopicIdeaIds": ["BTI011"],
            "sourceAuditStatus": "body-reviewed",
        })
        runtime["profiles"][source["id"]] = base
        runtime["topicIdeaAssignments"]["BTI011"] = {
            "primaryEditorialSource": source["id"],
            "selectionReason": "실제 본문을 읽고 소화불량 질문과 전개를 확인한 실행용 프로필",
        }
        self.assertEqual(EDITORIAL_PROFILE_VALIDATOR.validate_profiles(runtime, topic_library), [])
        candidate = next(
            item for item in TOPIC_SELECTOR.external_topic_candidates(topic_library, runtime)
            if item["topicSourceId"] == "BTI011"
        )
        self.assertEqual(candidate["editorialProfileStatus"], "ready")
        self.assertEqual(candidate["editorialMasterId"], source["id"])

    def test_profile_without_body_review_status_cannot_promote(self) -> None:
        topic_library = self.topic_library()
        runtime = self.editorial_profiles()
        runtime["profiles"]["BM224231647991"]["sourceAuditStatus"] = "title-only"
        errors = EDITORIAL_PROFILE_VALIDATOR.validate_profiles(runtime, topic_library)
        self.assertTrue(any("sourceAuditStatus=body-reviewed" in error for error in errors), errors)

    def test_legacy_chuna_alias_blocks_chuna_topic(self) -> None:
        candidate = next(
            item
            for item in TOPIC_SELECTOR.external_topic_candidates(self.topic_library())
            if item["topicSourceId"] == "BTI001"
        )
        legacy = {
            "entries": [
                {
                    "title": "광주 한의원 추나 치료를 받아도 다시 아픈 이유",
                    "mainKeyword": "광주 한의원",
                    "topic": "추나 적용과 생활조건",
                    "type": "정보전달형",
                }
            ]
        }
        with self.assertRaisesRegex(ValueError, "no-semantic-fresh-topic"):
            TOPIC_SELECTOR.choose_topic_candidates([candidate], legacy, "광주 한의원", "추나요법", 1, "alias")

    def test_count_three_is_pairwise_semantically_distinct(self) -> None:
        results = TOPIC_SELECTOR.select_ideas(
            self.wipark_library(),
            {"entries": []},
            "광주 한의원 추천",
            count=3,
            seed="semantic-pairwise",
            topic_source_library=self.topic_library(),
        )
        self.assertEqual(len(results), 3)
        for index, left in enumerate(results):
            for right in results[index + 1 :]:
                self.assertFalse(TOPIC_SELECTOR.semantic_overlap(left, right), (left, right))

    def test_same_cluster_different_subject_can_remain_fresh(self) -> None:
        candidates = TOPIC_SELECTOR.external_topic_candidates(self.topic_library())
        left = next(item for item in candidates if item["topicSourceId"] == "BTI021")
        right = next(item for item in candidates if item["topicSourceId"] == "BTI024")
        self.assertEqual(left["topicCluster"], right["topicCluster"])
        self.assertFalse(TOPIC_SELECTOR.semantic_overlap(left, right))


class ReferenceCorpusTests(unittest.TestCase):
    def corpus(self) -> dict[str, object]:
        return json.loads((SKILL_DIR / "assets" / "wipark-reference-corpus.json").read_text(encoding="utf-8"))

    def ideas(self) -> dict[str, object]:
        return json.loads((SKILL_DIR / "assets" / "topic-idea-library.json").read_text(encoding="utf-8"))

    def test_cutoff_audit_is_complete_and_daily_posts_are_excluded(self) -> None:
        corpus = self.corpus()
        self.assertEqual(corpus["sourceBlogId"], "wi-parkclinic")
        self.assertEqual(corpus["cutoffInclusive"], "2024-10-04")
        self.assertEqual(corpus["sourceTotalCount"], 196)
        self.assertEqual(corpus["includedCount"], 130)
        self.assertEqual(corpus["fetchSuccessCount"], 130)
        self.assertEqual(corpus["fetchFailureCount"], 0)
        articles = corpus["articles"]
        self.assertEqual(min(item["publishedAt"] for item in articles), "2024-10-04")
        counts: dict[str, int] = {}
        for item in articles:
            counts[item["contentType"]] = counts.get(item["contentType"], 0) + 1
            self.assertNotIn("bodyText", item)
            self.assertNotIn("sourceHtml", item)
            if item["contentType"] == "제외":
                self.assertFalse(item["eligible"])
        self.assertEqual(
            counts,
            {"정보전달형": 88, "업체소개형": 4, "사례공유형": 4, "스토리텔링형": 2, "제외": 32},
        )

    def test_idea_and_writing_master_roles_are_separate(self) -> None:
        library = self.ideas()
        self.assertEqual(library["sourceArticleCount"], 130)
        self.assertEqual(library["articleCount"], 11)
        self.assertEqual(library["excludedCount"], 119)
        self.assertEqual(library["sourceExcludedCount"], 32)
        self.assertEqual(library["familyFilteredOutCount"], 119)
        self.assertTrue(
            all(
                item["sourceFactsBlocked"]
                and item["sourceSentencesBlocked"]
                and item["sourceMediaBlocked"]
                and item["sourceContentType"] == "정보전달형"
                and item["referenceFamilyId"] == "two-or-three-reader-concern-hooks-solution-preview-info"
                and item["minimumReaderHookCount"] == 2
                and item["maximumReaderHookCount"] == 3
                and item["allowedReaderHookCounts"] == [2, 3]
                and item["requiresSolutionPreviewBeforeBody"]
                for item in library["articles"]
            )
        )
        selections = TOPIC_SELECTOR.select_ideas(
            library,
            {"entries": []},
            "광주 한의원",
            topic="목 통증",
            count=3,
            seed="contract-test",
        )
        self.assertEqual(len(selections), 3)
        self.assertTrue(all(item["sourceContentType"] == "정보전달형" for item in selections))
        self.assertTrue(all(item["ideaReferenceUrl"].startswith("https://blog.naver.com/wi-parkclinic/") for item in selections))
        self.assertTrue(all(item["writingReferenceUrl"].startswith("https://blog.naver.com/wi-parkclinic/") for item in selections))
        self.assertTrue(all("금손한의원 사실" in item["factPolicy"] for item in selections))
        broad = TOPIC_SELECTOR.select_ideas(
            library,
            {"entries": []},
            "광주 한의원",
            count=1,
            seed="broad-clinic-contract",
        )[0]
        self.assertEqual(broad["ideaReferenceId"], "WP224320052203", broad)
        self.assertEqual(broad["writingMasterId"], "INFO01", broad)
        legacy_state = {
            "schemaVersion": 1,
            "entries": [
                {
                    "mainKeyword": "광주 한의원",
                    "ideaReferenceUrl": "https://blog.naver.com/wi-parkclinic/224320052203",
                    "writingMasterId": "INFO01",
                    "topic": "치료받아도 반복되는 생활 조건",
                    "title": "광주 한의원 통증이 반복되는 생활 조건 2가지",
                    "titlePattern": "특징 2가지",
                    "type": "정보전달형",
                }
            ],
        }
        rotated = TOPIC_SELECTOR.select_ideas(
            library,
            legacy_state,
            "광주 한의원",
            count=1,
            seed="legacy-state-contract",
        )[0]
        self.assertNotEqual(rotated["ideaReferenceId"], "WP224320052203", rotated)
        self.assertNotEqual(rotated["writingMasterId"], "INFO01", rotated)

    def test_master_profiles_are_exactly_the_eleven_allowed_information_posts(self) -> None:
        data = json.loads((SKILL_DIR / "assets" / "reference-master-profiles.json").read_text(encoding="utf-8"))
        profiles = data["profiles"]
        self.assertEqual(len(profiles), 11)
        counts: dict[str, int] = {}
        for profile in profiles.values():
            counts[profile["type"]] = counts.get(profile["type"], 0) + 1
            self.assertTrue(profile["sourceUrl"].startswith("https://blog.naver.com/wi-parkclinic/"))
            self.assertIn("maximumCenterRatio", profile["renderContract"])
            self.assertEqual(profile["renderContract"]["nativeDesignSystemId"], "goldhand-naver-native-v4")
            self.assertFalse(profile["renderContract"]["referenceControlsDecoration"])
            self.assertEqual(profile["renderContract"]["minimumCenterRatio"], 1.0)
            self.assertEqual(profile["renderContract"]["maximumCenterRatio"], 1.0)
            self.assertEqual(profile["renderContract"]["requiredUnderlineMinimum"], 2)
            self.assertEqual(profile["referenceFamilyId"], "two-or-three-reader-concern-hooks-solution-preview-info")
            self.assertEqual(profile["renderContract"]["requiredRoleMinimums"]["reader-question"], 2)
            self.assertEqual(profile["renderContract"]["requiredRoleMaximums"]["reader-question"], 3)
            self.assertEqual(profile["renderContract"]["requiredRoleMinimums"]["solution-preview"], 1)
        self.assertEqual(counts, {"정보전달형": 11})
        self.assertNotIn("INFO02", profiles)


class SkillPackageTests(unittest.TestCase):
    def test_required_contract_files_exist(self) -> None:
        for relative in (
            "SKILL.md",
            "agents/openai.yaml",
            "references/clinic-facts.md",
            "references/content-formulas.md",
            "references/two-reader-hooks-reference-audit.md",
            "references/reference-master-library.md",
            "references/reference-exact-reconstruction.md",
            "references/official-blog-inventory.md",
            "references/topic-idea-types.md",
            "references/beomeo-source-inventory.md",
            "references/beomeo-topic-source-policy.md",
            "references/wipark-reference-inventory.md",
            "references/wipark-content-source-policy.md",
            "references/goldhand-official-voice.md",
            "assets/media-library.json",
            "assets/topic-idea-library.json",
            "assets/beomeo-topic-idea-library.json",
            "assets/wipark-reference-corpus.json",
            "assets/reference-master-profiles.json",
            "assets/goldhand-naver-native-design-system.json",
            "assets/goldhand-closing-links.json",
            "assets/callilife-ogq-media-library.json",
            "assets/gpt-image-test-fixture.png",
            "assets/goldhand-value-proof-library.json",
            "assets/two-reader-hooks-reference-family.json",
            "assets/wipark-content-briefs.json",
            "assets/goldhand-official-voice-profile.json",
            "scripts/select_topic_idea.py",
            "scripts/validate_topic_source_library.py",
            "scripts/select_reference_master.py",
            "scripts/validate_reference_reconstruction.py",
            "scripts/select_wipark_content_reference.py",
            "scripts/validate_goldhand_voice.py",
            "scripts/sync_official_media_assets.py",
            "scripts/recommend_media.py",
        ):
            self.assertTrue((SKILL_DIR / relative).is_file(), relative)
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        proof = json.loads((SKILL_DIR / "assets" / "goldhand-value-proof-library.json").read_text(encoding="utf-8"))
        design = json.loads((SKILL_DIR / "assets" / "goldhand-naver-native-design-system.json").read_text(encoding="utf-8"))
        openai_yaml = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertFalse(proof["selectionAllowed"])
        self.assertEqual(len(proof["fixedRows"]), 6)
        self.assertEqual(design["layout"]["bodyTextAlign"], "center")
        self.assertEqual(design["textEmphasis"]["minimumTotalCount"], 6)
        self.assertEqual(design["textEmphasis"]["highlight"]["minimumCount"], 3)
        self.assertEqual(design["retentionHooks"]["readingTime"]["minutes"], 3)
        self.assertEqual(design["generatedReferenceMedia"]["creator"], "callilife")
        self.assertEqual(design["realGoldhandMedia"]["minimumCount"], 6)
        self.assertEqual(design["realGoldhandMedia"]["maximumCount"], 12)
        self.assertTrue(design["realGoldhandMedia"]["recentReuseAllowedOnlyBelowMinimum"])
        self.assertTrue(design["realGoldhandMedia"]["personInteractionRequired"])
        self.assertTrue(design["realGoldhandMedia"]["directorVisibleRequired"])
        self.assertEqual(design["fixedClosingLinks"]["placeId"], "1598180269")
        self.assertEqual(design["fixedClosingLinks"]["order"], ["goldhand-official-blog-linked-photo", "goldhand-naver-place-map"])
        self.assertTrue(design["fixedClosingLinks"]["blogPhotoIsTheLink"])
        self.assertTrue(design["fixedClosingLinks"]["visibleBlogLinkTextForbidden"])
        self.assertEqual(design["generatedReferenceMedia"]["contentPreservation"], "medical-information-layout")
        self.assertEqual(
            design["generatedReferenceMedia"]["allowedVariationModes"],
            ["person-identity-subtle-variation", "nonperson-style-subtle-variation"],
        )
        self.assertEqual(design["tablePurposes"]["clinic-info"]["columnWidth"], "50%")
        self.assertEqual(design["textEmphasis"]["red"]["minimumCount"], 1)
        credential_placement = design["editorialCloseOverrides"]["credentialPlacement"]
        self.assertTrue(credential_placement["appliesToEveryArticle"])
        self.assertEqual(credential_placement["requiredDirectlyAfterCompletedRole"], "solution-preview")
        self.assertEqual(
            credential_placement["requiredImmediatelyBeforeFirstInformationBodyRole"],
            ["divider", "section-heading"],
        )
        self.assertIn("실제 고민을 금손 내용으로 바꿔 2~3개", skill)
        self.assertIn("일상글", skill)
        self.assertIn("fallback 어디에도 넣지 않는다", skill)
        self.assertIn("wipark-content-briefs.json", skill)
        self.assertIn("최근 3개", skill)
        self.assertIn("goldhand-official-voice-v1", skill)
        self.assertIn("위석 원문의 말투·종결어미", skill)
        self.assertIn("validate_goldhand_voice.py", skill)
        self.assertIn("실제 금손한의원 사진을 매 글 6~12장", skill)
        self.assertIn("새 승인 사진이 6장보다 적을 때만", skill)
        self.assertIn("assets/official-media", skill)
        self.assertIn("goldhand-closing-links.json", skill)
        self.assertIn("1598180269", skill)
        self.assertIn("로고·간판·건물 외부·약·환제·탕약·장비·제품·빈 원내 공간", skill)
        self.assertNotIn("Desktop/" + "금손한의원 사진", skill)
        self.assertIn("진료실 발화 가능성 검사", skill)
        self.assertIn("같은 생성 원리에서 나온 문장군", skill)
        self.assertIn("data-question-source", skill)
        self.assertIn("solution-preview", skill)
        self.assertIn("goldhand-naver-native-v4", skill)
        self.assertIn("첫 정보 본문의 구분선·소제목·설명보다 앞", skill)
        self.assertIn("placing the fixed Goldhand credential table after the complete introduction", openai_yaml)
        self.assertIn("Never use a Goldhand logo", openai_yaml)
        self.assertIn("Naver Place map block", openai_yaml)
        self.assertIn("clickable Goldhand director-consultation photo", openai_yaml)
        self.assertIn("data-mobile-group", skill)
        self.assertNotIn("Notion TOP 5", skill)

    def test_official_goldhand_voice_is_required_and_emoticons_fail(self) -> None:
        profile = json.loads((SKILL_DIR / "assets" / "goldhand-official-voice-profile.json").read_text(encoding="utf-8"))
        example = (SKILL_DIR / "examples" / "광주-한의원-네이버-순정-원고.html").read_text(encoding="utf-8")
        passed = GOLDHAND_VOICE_VALIDATOR.validate(example, profile)
        self.assertEqual(passed["status"], "pass", passed)
        failed = GOLDHAND_VOICE_VALIDATOR.validate(example.replace("그런데", "ㅎㅎ 그런데", 1), profile)
        self.assertEqual(failed["status"], "fail", failed)
        self.assertIn("emoticon", {item["code"] for item in failed["issues"]})

    def test_spoken_clinic_gate_rejects_ai_register_not_only_exact_examples(self) -> None:
        profile = json.loads((SKILL_DIR / "assets" / "goldhand-official-voice-profile.json").read_text(encoding="utf-8"))
        example = (SKILL_DIR / "examples" / "광주-한의원-네이버-순정-원고.html").read_text(encoding="utf-8")
        direct = GOLDHAND_VOICE_VALIDATOR.validate(example, profile)
        self.assertEqual(direct["status"], "pass", direct)

        translated = example.replace(
            "혼자 판단해서 운동을 계속하시면 안 됩니다.",
            "혼자 스트레칭을 지속하지 마세요.",
            1,
        )
        translated_result = GOLDHAND_VOICE_VALIDATOR.validate(translated, profile)
        self.assertIn(
            "translated-indirect-safety-command",
            {item["code"] for item in translated_result["issues"]},
        )

        homework = example.replace(
            "진료할 때 같이 말씀해 주세요.",
            "그때의 몸 변화를 기록해 보세요.",
            1,
        )
        homework_result = GOLDHAND_VOICE_VALIDATOR.validate(homework, profile)
        self.assertIn("reader-homework-imperative", {item["code"] for item in homework_result["issues"]})

        poetic = example.replace(
            "진료할 때 같이 말씀해 주세요.",
            "이것이 회복의 첫걸음이 됩니다.",
            1,
        )
        poetic_result = GOLDHAND_VOICE_VALIDATOR.validate(poetic, profile)
        self.assertIn("poetic-abstract-payoff", {item["code"] for item in poetic_result["issues"]})

        softened = example.replace(
            "혼자 판단해서 운동을 계속하시면 안 됩니다.",
            "저림이 있으면 운동을 쉬어 보는 편이 좋습니다.",
            1,
        )
        softened_result = GOLDHAND_VOICE_VALIDATOR.validate(softened, profile)
        self.assertIn("over-softened-medical-guidance", {item["code"] for item in softened_result["issues"]})

        meta = example.replace(
            "제가 진료할 때 먼저 여쭙는 건",
            "이번 글에서는 함께 살펴보겠습니다",
            1,
        )
        meta_result = GOLDHAND_VOICE_VALIDATOR.validate(meta, profile)
        self.assertIn("blog-meta-framing", {item["code"] for item in meta_result["issues"]})

        afterglow = example.replace(
            "진료할 때 같이 말씀해 주세요.",
            "이 내용이 작은 도움이 되었으면 합니다.",
            1,
        )
        afterglow_result = GOLDHAND_VOICE_VALIDATOR.validate(afterglow, profile)
        self.assertIn("lesson-afterglow-ending", {item["code"] for item in afterglow_result["issues"]})

        literary_location = example.replace(
            "아픈 곳만 말씀하지 마시고",
            "아픈 자리만 말씀하지 마시고",
            1,
        )
        literary_location_result = GOLDHAND_VOICE_VALIDATOR.validate(literary_location, profile)
        self.assertIn(
            "literary-body-location",
            {item["code"] for item in literary_location_result["issues"]},
        )

        abstract_gait = example.replace(
            "진료할 때 같이 말씀해 주세요.",
            "걷기가 달라지면 진료할 때 말씀해 주세요.",
            1,
        )
        abstract_gait_result = GOLDHAND_VOICE_VALIDATOR.validate(abstract_gait, profile)
        self.assertIn(
            "abstract-gait-description",
            {item["code"] for item in abstract_gait_result["issues"]},
        )

        abstract_predicate = example.replace(
            "진료할 때 같이 말씀해 주세요.",
            "이 내용이 치료 방향에 차이를 만듭니다.",
            1,
        )
        abstract_predicate_result = GOLDHAND_VOICE_VALIDATOR.validate(abstract_predicate, profile)
        self.assertIn(
            "abstract-editorial-predicate",
            {item["code"] for item in abstract_predicate_result["issues"]},
        )

        natural_gait = example.replace(
            "진료할 때 같이 말씀해 주세요.",
            "평소보다 걷기 힘들다면 진료할 때 말씀해 주세요.",
            1,
        )
        natural_gait_result = GOLDHAND_VOICE_VALIDATOR.validate(natural_gait, profile)
        self.assertEqual(natural_gait_result["status"], "pass", natural_gait_result)

    def test_wipark_controls_content_but_not_voice(self) -> None:
        briefs = json.loads((SKILL_DIR / "assets" / "wipark-content-briefs.json").read_text(encoding="utf-8"))
        profiles = json.loads((SKILL_DIR / "assets" / "reference-master-profiles.json").read_text(encoding="utf-8"))
        selected = WIPARK_CONTENT_SELECTOR.select(
            "광주 한의원", "", briefs, profiles, {"entries": []}, count=1, seed="content-voice-contract"
        )[0]
        self.assertTrue(selected["orderedGeneralInformation"])
        self.assertTrue(selected["sourceToneBlocked"])
        self.assertEqual(selected["voiceProfileId"], "goldhand-official-voice-v1")


if __name__ == "__main__":
    unittest.main()
