#!/usr/bin/env python3
"""通用賽程驗證工具。

用法：
    python3 tools/validate_schedule.py --data examples/cpbl-2027/data --profile examples/cpbl-2027/profile.json

讀取資料夾中的 games.csv、teams.csv（格式見 docs/GUIDE.md 第 3 節），
依 profile.json 的設定逐項檢查，最後印出通過／失敗清單。
有任何「失敗」時以結束碼 1 離開，方便放進自動化流程。

只用 Python 標準函式庫（3.9+）。
"""
import argparse
import csv
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import date

REQUIRED_GAME_COLS = ['game_id', 'date', 'home', 'away']
REQUIRED_TEAM_COLS = ['team_id', 'short_name', 'full_name']

results = []  # (level, message)  level: PASS / FAIL / WARN


def report(ok, msg, warn_only=False):
    results.append(('PASS' if ok else ('WARN' if warn_only else 'FAIL'), msg))


def read_csv(path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


# ---------- 顏色對比（WCAG 2.x） ----------
def _lum(hex_color):
    h = hex_color.lstrip('#')
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(c1, c2):
    a, b = sorted([_lum(c1), _lum(c2)], reverse=True)
    return (a + 0.05) / (b + 0.05)


# ---------- 檢查項目 ----------
def check_structure(games, teams):
    cols = games[0].keys() if games else []
    missing = [c for c in REQUIRED_GAME_COLS if c not in cols]
    report(not missing, f'games.csv 必要欄位齊全 {REQUIRED_GAME_COLS}' + (f'（缺 {missing}）' if missing else ''))
    tcols = teams[0].keys() if teams else []
    tmissing = [c for c in REQUIRED_TEAM_COLS if c not in tcols]
    report(not tmissing, 'teams.csv 必要欄位齊全' + (f'（缺 {tmissing}）' if tmissing else ''))
    if missing or tmissing:
        return False
    ids = [g['game_id'] for g in games]
    dup = [k for k, v in Counter(ids).items() if v > 1]
    report(not dup, f'game_id 不重複' + (f'（重複：{dup[:5]}）' if dup else ''))
    team_ids = {t['team_id'] for t in teams}
    unknown = sorted({g[s] for g in games for s in ('home', 'away')} - team_ids)
    report(not unknown, '所有對戰隊伍都在 teams.csv 中' + (f'（未知：{unknown[:5]}）' if unknown else ''))
    same = [g['game_id'] for g in games if g['home'] == g['away']]
    report(not same, '沒有自己打自己' + (f'（{same[:5]}）' if same else ''))
    bad_dates = []
    for g in games:
        try:
            date.fromisoformat(g['date'])
        except ValueError:
            bad_dates.append(g['game_id'])
    report(not bad_dates, '日期格式皆為 YYYY-MM-DD' + (f'（錯誤：{bad_dates[:5]}）' if bad_dates else ''))
    return not unknown and not bad_dates


def check_dates(games, p):
    if not p.get('season_start') or not p.get('season_end'):
        return
    try:
        s, e = date.fromisoformat(p['season_start']), date.fromisoformat(p['season_end'])
    except ValueError:
        report(False, 'profile 的 season_start / season_end 還沒填成 YYYY-MM-DD，略過日期範圍檢查', warn_only=True)
        return
    out = [g['game_id'] for g in games if not s <= date.fromisoformat(g['date']) <= e]
    report(not out, f'所有比賽都在 {s} ~ {e} 之間' + (f'（超出：{out[:5]}）' if out else ''))


def check_per_day(games, p):
    limit = p.get('max_games_per_team_per_day', 1)
    if limit is None:
        return
    c = Counter()
    for g in games:
        for t in (g['home'], g['away']):
            c[(t, g['date'])] += 1
    over = [(t, d, n) for (t, d), n in c.items() if n > limit]
    report(not over, f'每隊每天最多 {limit} 場' + (f'（超過：{over[:5]}。若是雙重賽，請把 profile 的上限設為 2，並在 note 標示 DH）' if over else ''))


def check_per_week(games, p):
    limit = p.get('max_games_per_team_per_week')
    if not limit:
        return
    missing_week = [g['game_id'] for g in games if not g.get('week')]
    report(not missing_week, '週賽制：每場都有 week 欄位' + (f'（缺：{missing_week[:5]}）' if missing_week else ''))
    c = Counter()
    for g in games:
        for t in (g['home'], g['away']):
            c[(t, g.get('week'))] += 1
    over = [(t, w, n) for (t, w), n in c.items() if n > limit]
    report(not over, f'每隊每週最多 {limit} 場' + (f'（超過：{over[:5]}）' if over else ''))


def check_counts(games, teams, spec, label):
    """spec 可含 total_games、games_per_team、home_games_per_team、pair_games；值為 0 或 null 視為不檢查。"""
    spec = {k: v for k, v in spec.items() if v}
    team_ids = [t['team_id'] for t in teams if t['team_id'] in {g['home'] for g in games} | {g['away'] for g in games}]
    counted = [g for g in games if str(g.get('neutral', '')).lower() != 'true']
    if 'total_games' in spec:
        report(len(games) == spec['total_games'], f'{label}總場數 = {spec["total_games"]}（實際 {len(games)}）')
    if 'games_per_team' in spec:
        per = Counter()
        for g in games:
            per[g['home']] += 1
            per[g['away']] += 1
        bad = {t: per[t] for t in team_ids if per[t] != spec['games_per_team']}
        report(not bad, f'{label}每隊 {spec["games_per_team"]} 場' + (f'（不符：{bad}）' if bad else ''))
    if 'home_games_per_team' in spec:
        home = Counter(g['home'] for g in counted)
        away = Counter(g['away'] for g in counted)
        n = spec['home_games_per_team']
        bad = {t: (home[t], away[t]) for t in team_ids if home[t] != n}
        report(not bad, f'{label}每隊主場 {n} 場' + (f'（不符，主/客：{bad}）' if bad else ''))
    if 'pair_games' in spec:
        pair = Counter(frozenset((g['home'], g['away'])) for g in games)
        bad = {'-'.join(sorted(k)): v for k, v in pair.items() if v != spec['pair_games']}
        report(not bad, f'{label}任兩隊交手 {spec["pair_games"]} 場' + (f'（不符：{dict(list(bad.items())[:5])}）' if bad else ''))


def check_groups(games, teams, p):
    """錦標賽：同組才會在分組賽相遇。"""
    stage = p.get('group_stage_name')
    if not stage:
        return
    grp = {t['team_id']: t.get('group', '') for t in teams}
    bad = [g['game_id'] for g in games if g.get('stage') == stage and grp.get(g['home']) != grp.get(g['away'])]
    report(not bad, f'「{stage}」的對戰都是同組球隊' + (f'（跨組：{bad[:5]}）' if bad else ''))


def check_colors(teams, p):
    min_c = p.get('min_contrast', 4.5)
    for bg, fg, name in (('primary', 'primary_text', '實色'), ('pastel', 'pastel_text', '淡色')):
        if not teams or bg not in teams[0] or fg not in teams[0]:
            continue
        low = []
        for t in teams:
            if t.get(bg) and t.get(fg):
                r = contrast(t[bg], t[fg])
                if r < min_c:
                    low.append(f'{t["short_name"]} {r:.1f}')
        report(not low, f'{name}底與文字對比 ≥ {min_c}:1' + (f'（不足：{low}）' if low else ''), warn_only=True)


def main():
    ap = argparse.ArgumentParser(description='驗證賽程資料')
    ap.add_argument('--data', required=True, help='含 games.csv、teams.csv 的資料夾')
    ap.add_argument('--profile', required=True, help='聯盟設定 profile.json')
    a = ap.parse_args()

    games = read_csv(os.path.join(a.data, 'games.csv'))
    teams = read_csv(os.path.join(a.data, 'teams.csv'))
    with open(a.profile, encoding='utf-8') as f:
        p = json.load(f)

    print(f'== 驗證：{p.get("name", a.data)}（{len(games)} 場、{len(teams)} 隊） ==')
    if check_structure(games, teams):
        check_dates(games, p)
        check_per_day(games, p)
        check_per_week(games, p)
        check_counts(games, teams, p, '全季')
        for stage, spec in (p.get('by_stage') or {}).items():
            sub = [g for g in games if g.get('stage') == stage]
            check_counts(sub, teams, spec, f'[{stage}] ')
        check_groups(games, teams, p)
        check_colors(teams, p)

    for level, msg in results:
        mark = {'PASS': '✓', 'FAIL': '✗', 'WARN': '!'}[level]
        print(f'  {mark} {msg}')
    fails = sum(1 for l, _ in results if l == 'FAIL')
    warns = sum(1 for l, _ in results if l == 'WARN')
    print(f'結果：{len(results) - fails - warns} 通過、{fails} 失敗、{warns} 警告')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
