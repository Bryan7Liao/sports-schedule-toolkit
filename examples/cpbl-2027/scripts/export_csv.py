"""把 schedule_2027.py 的資料匯出成通用格式（games.csv / teams.csv / events.csv）。"""
import csv, os
from datetime import date
from schedule_2027 import rows

OUT = os.path.join(os.path.dirname(__file__), '..', 'data')
TEAMS = [
    # team_id, short_name, full_name, group, primary, primary_text, pastel, pastel_text, source_code
    ('WEI', '味全', '味全龍', '', '#D7261E', '#FFFFFF', '#F6C4C1', '#7A1F1C', '龍'),
    ('CTB', '兄弟', '中信兄弟', '', '#F5C400', '#2B2400', '#FFF0B3', '#5E4B00', '象'),
    ('UNI', '統一', '統一7-ELEVEn獅', '', '#F08A24', '#3A1C00', '#FDD5AE', '#7A3E00', '獅'),
    ('FUB', '富邦', '富邦悍將', '', '#1E4FA0', '#FFFFFF', '#C3D7F2', '#173E73', '悍將'),
    ('RKM', '樂天', '樂天桃猿', '', '#8A1022', '#FFFFFF', '#D9A3AC', '#4A0A14', '桃猿'),
    ('TSG', '台鋼', '台鋼雄鷹', '', '#0E5A3A', '#FFFFFF', '#B7D6C4', '#1E4D33', '雄鷹'),
]
CODE = {t[8]: t[0] for t in TEAMS}

EVENTS = [('2027-04-22', '上半季優先補賽日', 'league'), ('2027-04-29', '上半季優先補賽日', 'league'),
          ('2027-06-04', '上半季優先補賽日', 'league'), ('2027-06-30', '上半季加賽保留日', 'league'),
          ('2027-07-02', '下半季開賽', 'league'), ('2027-07-17', '明星賽', 'league'), ('2027-07-18', '明星賽', 'league'),
          ('2027-09-21', '下半季優先補賽日', 'league'), ('2027-09-22', '下半季優先補賽日', 'league'),
          ('2027-10-06', '下半季加賽保留日', 'league')]
EVENTS += [(f'2027-06-{d:02d}', '補賽預備日', 'league') for d in (22, 23, 24, 25, 26, 27, 29)]
EVENTS += [(d, '補賽預備日', 'league') for d in ('2027-09-29', '2027-09-30', '2027-10-01', '2027-10-02',
                                                 '2027-10-03', '2027-10-04', '2027-10-05')]
EVENTS += [(f'2027-10-{d:02d}', '季後賽預定', 'postseason') for d in (9, 10, 11, 12)]
EVENTS += [(f'2027-10-{d:02d}', '總冠軍賽預定', 'postseason') for d in range(16, 25)]

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, 'teams.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['team_id', 'short_name', 'full_name', 'group', 'primary', 'primary_text', 'pastel', 'pastel_text'])
    for t in TEAMS:
        w.writerow(t[:8])
with open(os.path.join(OUT, 'games.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['game_id', 'date', 'local_time', 'timezone', 'week', 'stage', 'group', 'home', 'away',
                'neutral', 'venue', 'note', 'source'])
    for i, (d, a, h) in enumerate(rows, 1):
        stage = '上半季' if d < date(2027, 7, 1) else '下半季'
        w.writerow([f'2027-{i:03d}', d.isoformat(), '', 'Asia/Taipei', '', stage, '', CODE[h], CODE[a],
                    'false', '', '', 'CPBL 官網公告 2026-11-24'])
with open(os.path.join(OUT, 'events.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['date', 'label', 'scope'])
    for e in sorted(EVENTS):
        w.writerow(e)
print('exported', len(rows), 'games')
