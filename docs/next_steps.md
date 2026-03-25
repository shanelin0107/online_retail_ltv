# 下一步（Next Steps）

以下是把這個專案從「完整骨架」推進到「可面試展示成品」的建議順序。

## 1) 接入真實資料並完成首版可重現流程（優先）
- 將原始交易資料放入 `data/raw/`（或建立資料庫連線）。
- 依據實際欄位名稱調整 `sql/customer_ltv_analysis.sql` 與 `scripts/data_preparation.py`。
- 輸出 `data/processed/customer_ltv_dataset.csv`，並確認欄位與資料型態一致。

## 2) 明確定義清洗規則（避免面試時被追問）
- 決定負數數量、零價格、取消訂單是否排除。
- 在 README 與 docs 中補上「排除筆數與原因」摘要表。
- 保留一個 `data_quality_log.csv`（可選）記錄每類異常筆數。

## 3) 完成 Tableau 儀表板成品
- 將 `dashboards/tableau/online_retail_ltv_dashboard.twbx` 連到 processed dataset。
- 完成 5 個視覺元件：KPI、Top 20、Frequency vs AOV、LTV 分布、年度篩選。
- 匯出高解析截圖到 `dashboards/screenshots/dashboard_overview.png`。

## 4) 用實際數字替換敘事文字
- 將 README 與 `docs/dashboard_story.md` 中的洞察改成「量化陳述」
  - 例如：Repeat LTV 比整體平均高出 X%。
  - Top 10% 客戶貢獻總營收 Y%。

## 5) 提升作品集說服力（加分項）
- 增加 Pareto 圖與 Top 10% 貢獻卡。
- 增加客群分層（VIP / High / Mid / Low）。
- 新增 1 頁 `case_study.md`：商業背景 → 分析 → 行動 → 影響。

## 6) 發佈與面試準備
- 在 GitHub Releases 或 README 放上儀表板預覽圖。
- 準備 60 秒版本口頭敘事（問題、方法、洞察、建議、影響）。

---

## 建議本週執行清單（簡版）
1. 接資料 + 跑出 customer_ltv_dataset.csv
2. 完成 Tableau 成品並輸出截圖
3. 用真實數字更新 README 洞察
4. 增加 Pareto / Top 10% 指標
