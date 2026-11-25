# 運動賽程整理工具包

把官方公布的運動賽程，整理成**驗證過的資料檔**、**Google Sheet 賽程表**與**各隊賽程圖**的流程、範本與工具。

一開始是為中華職棒 2027 球季做的，之後歸納成通用流程，可以套用到 MLB、NFL、日本職棒、韓國職棒，以及 WBC、世界盃這類國際賽。

---

## 可以做出什麼

| 成果 | 說明 |
|---|---|
| 通用資料檔 | `games.csv`、`teams.csv`、`events.csv`，所有表格與圖都從這裡產生 |
| 自動驗證 | 檢查總場數、主客場、交手數、日期、重複排程、顏色對比 |
| Google Sheet | 明細表、聯盟日曆或週次表、各隊日曆，依主場球隊自動上色 |
| 賽程圖 | 每隊一張直式海報，可匯出圖片貼到社群 |

## 文件

| 文件 | 內容 |
|---|---|
| [docs/GUIDE.md](docs/GUIDE.md) | **通用手冊**：賽制分類、資料格式、取得資料、驗證、版面、配色、圖片、時區、上手清單 |
| [docs/LEAGUES.md](docs/LEAGUES.md) | 各聯盟與賽事的賽制、場數、官方資料來源與特有狀況 |
| [examples/cpbl-2027/README.md](examples/cpbl-2027/README.md) | 完整範例：中華職棒 2027（從讀圖到 15 個分頁與 6 張海報） |

## 支援的賽制

| 類型 | 代表賽事 | 主要呈現 |
|---|---|---|
| A. 聯盟日賽制 | 中華職棒、日本職棒、韓國職棒、MLB | 月曆 |
| B. 週賽制 | NFL、足球聯賽 | 週次表 |
| C. 國際錦標賽 | WBC、世界盃足球、奧運 | 分組表＋賽程樹 |

## 快速開始

```bash
# 1. 建立新賽事資料夾，複製範本
mkdir -p examples/mlb-2027
cp templates/*.csv examples/mlb-2027/
cp templates/profile_league.json examples/mlb-2027/profile.json

# 2. 填好 teams.csv、games.csv、profile.json（格式見 docs/GUIDE.md 第 3 節）

# 3. 驗證，全部通過才往下做
python3 tools/validate_schedule.py --data examples/mlb-2027 --profile examples/mlb-2027/profile.json
```

用中華職棒範例試跑：

```bash
python3 tools/validate_schedule.py --data examples/cpbl-2027/data --profile examples/cpbl-2027/profile.json
```

需要 Python 3.9 以上，只用標準函式庫。

## 專案結構

```
.
├── README.md
├── docs/
│   ├── GUIDE.md                  通用手冊
│   └── LEAGUES.md                各聯盟資料表
├── templates/
│   ├── games.csv / teams.csv / events.csv
│   └── profile_league.json / profile_weekly.json / profile_tournament.json
├── tools/
│   └── validate_schedule.py      通用驗證工具
└── examples/
    └── cpbl-2027/                中華職棒 2027 完整範例
        ├── README.md
        ├── profile.json
        ├── data/                 360 場資料（通用格式）
        └── scripts/              轉錄資料、產生表格與海報的腳本
```

## 新增一個賽事

1. 照 [GUIDE.md 第 10 節](docs/GUIDE.md#10-新賽事上手清單) 的清單做。
2. 在 `examples/<賽事>-<年度>/` 放資料、`profile.json` 與一份 README，記下這個賽事特有的狀況。
3. 如果是新聯盟，在 [LEAGUES.md](docs/LEAGUES.md) 補一段。

## 注意事項

- 賽程會變動（延賽、改時間、彈性排程），每份成果都要標注資料來源與日期，並寫「實際賽程以官方公告為準」。
- 隊徽、吉祥物、字標是商標，不要自行繪製或放進圖片。
- 詳見 [GUIDE.md 第 11 節](docs/GUIDE.md#11-版權與資料使用)。
