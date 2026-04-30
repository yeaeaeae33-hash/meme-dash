#!/usr/bin/env python3
"""
매주 월요일 14:00 (KST) 자동 실행되는 밈 트렌드 수집 스크립트
Anthropic API + 웹 검색으로 최신 밈 수집 후 memes.json에 누적 저장
"""

import json
import os
from datetime import datetime, timezone, timedelta
import anthropic

# 한국 시간대 설정
KST = timezone(timedelta(hours=9))

def get_week_id():
    """이번 주 월요일 날짜를 week_id로 반환"""
    now = datetime.now(KST)
    monday = now - timedelta(days=now.weekday())
    return monday.strftime("%Y-%m-%d")

def get_week_label():
    """'2026년 5월 1주차' 형식 레이블 반환"""
    now = datetime.now(KST)
    monday = now - timedelta(days=now.weekday())
    month = monday.month
    # 해당 월의 몇 번째 주인지 계산
    week_of_month = (monday.day - 1) // 7 + 1
    return f"{monday.year}년 {month}월 {week_of_month}주차"

def collect_memes_with_api():
    """Anthropic API + 웹 검색으로 최신 밈 수집"""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    
    today = datetime.now(KST).strftime("%Y년 %m월 %d일")
    
    prompt = f"""오늘은 {today}입니다.
지금 이 순간 한국과 해외에서 가장 유행하는 최신 밈 트렌드를 웹 검색으로 조사해주세요.

다음 JSON 형식으로만 응답해주세요. 다른 텍스트나 마크다운 없이 순수 JSON만:

{{
  "domestic": [
    {{
      "rank": 1,
      "name": "밈 이름",
      "short": "한 줄 설명 (30자 이내)",
      "origin": "출처/시작점",
      "status": "new 또는 trending 또는 fading",
      "platforms": ["플랫폼1", "플랫폼2"],
      "marketing_tip": "마케터를 위한 활용 팁 (50자 이내)",
      "detail": {{
        "origin_story": "탄생 배경 (100자 이내)",
        "why_viral": "왜 유행했는지 (80자 이내)",
        "usage": "실제 사용 예시"
      }}
    }}
  ],
  "global": [
    {{
      "rank": 1,
      "name": "밈 이름",
      "short": "한 줄 설명 (30자 이내)",
      "origin": "출처/시작점",
      "status": "new 또는 trending 또는 fading",
      "platforms": ["플랫폼1", "플랫폼2"],
      "marketing_tip": "마케터를 위한 활용 팁 (50자 이내)",
      "detail": {{
        "origin_story": "탄생 배경 (100자 이내)",
        "why_viral": "왜 유행했는지 (80자 이내)",
        "usage": "실제 사용 예시"
      }}
    }}
  ]
}}

- domestic: 현재 한국에서 유행 중인 밈 5개 (SNS, 틱톡, X 등 기반으로 최신 것)
- global: 현재 해외(미국, 일본, 동남아 등)에서 유행 중인 밈 5개
- status: new(이번 주 새로 등장), trending(계속 유행 중), fading(유행이 사그라드는 중)
- 반드시 {today} 기준 최신 데이터로 작성
- JSON 외 다른 텍스트 절대 포함하지 말 것"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}]
    )
    
    # 응답에서 텍스트 추출
    result_text = ""
    for block in response.content:
        if block.type == "text":
            result_text += block.text
    
    # JSON 파싱
    result_text = result_text.strip()
    if result_text.startswith("```"):
        lines = result_text.split("\n")
        result_text = "\n".join(lines[1:-1])
    
    return json.loads(result_text)

def update_memes_json(new_data):
    """memes.json에 이번 주 데이터 누적 추가"""
    json_path = "data/memes.json"
    
    # 기존 데이터 로드
    with open(json_path, "r", encoding="utf-8") as f:
        existing = json.load(f)
    
    week_id = get_week_id()
    
    # 이미 이번 주 데이터가 있으면 업데이트, 없으면 추가
    existing_ids = [w["week_id"] for w in existing["weeks"]]
    
    now_kst = datetime.now(KST)
    
    week_entry = {
        "week_id": week_id,
        "week_label": get_week_label(),
        "collected_at": now_kst.isoformat(),
        "domestic": [
            {**item, "weeks_trending": item.get("weeks_trending", 1)}
            for item in new_data["domestic"]
        ],
        "global": [
            {**item, "weeks_trending": item.get("weeks_trending", 1)}
            for item in new_data["global"]
        ]
    }
    
    # 이전 주 데이터와 비교해서 weeks_trending 계산
    if existing["weeks"]:
        prev_week = existing["weeks"][-1]
        prev_domestic_names = {item["name"]: item.get("weeks_trending", 1) for item in prev_week["domestic"]}
        prev_global_names = {item["name"]: item.get("weeks_trending", 1) for item in prev_week["global"]}
        
        for item in week_entry["domestic"]:
            if item["name"] in prev_domestic_names:
                item["weeks_trending"] = prev_domestic_names[item["name"]] + 1
        
        for item in week_entry["global"]:
            if item["name"] in prev_global_names:
                item["weeks_trending"] = prev_global_names[item["name"]] + 1
    
    if week_id in existing_ids:
        idx = existing_ids.index(week_id)
        existing["weeks"][idx] = week_entry
        print(f"✅ {week_id} 데이터 업데이트 완료")
    else:
        existing["weeks"].append(week_entry)
        print(f"✅ {week_id} 새 주차 데이터 추가 완료")
    
    # 메타 정보 업데이트
    existing["meta"]["last_updated"] = week_id
    existing["meta"]["total_weeks"] = len(existing["weeks"])
    
    # 저장
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
    
    print(f"📊 총 {existing['meta']['total_weeks']}주 데이터 누적됨")

def main():
    print(f"🔍 밈 트렌드 수집 시작 - {datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S KST')}")
    
    try:
        print("📡 Anthropic API로 최신 밈 검색 중...")
        new_data = collect_memes_with_api()
        print(f"✅ 국내 밈 {len(new_data['domestic'])}개, 해외 밈 {len(new_data['global'])}개 수집 완료")
        
        update_memes_json(new_data)
        print("🎉 memes.json 업데이트 완료!")
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON 파싱 오류: {e}")
        raise
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        raise

if __name__ == "__main__":
    main()
