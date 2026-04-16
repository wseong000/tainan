# 台南未來一週天氣與提醒系統

## 專案簡介
這個專案是使用 Python 製作的天氣查詢程式，主要功能是查詢台南未來一週的天氣資訊，並提供穿搭提醒、是否適合運動、空氣品質提醒，同時將資料整理成表格、圖表與 CSV 檔案。

## 功能說明
- 查詢台南未來一週天氣
- 顯示最高溫、最低溫、降雨機率
- 提供穿搭建議與帶傘提醒
- 提供適合運動的建議
- 查詢空氣品質（PM2.5、PM10、AQI）
- 繪製未來一週高低溫變化圖
- 匯出天氣報表 CSV 檔案

## 使用技術
- Python
- requests
- pandas
- matplotlib
- Open-Meteo API

## 執行方式

### 1. 安裝需要的套件
```bash
pip install requests pandas matplotlib

```

### 2. 執行程式
```bash
python tainan.py
```
