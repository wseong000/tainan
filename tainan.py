import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
from IPython.display import display

plt.rcParams["font.family"] = "Microsoft JhengHei"
plt.rcParams["axes.unicode_minus"] = False

LATITUDE = 22.9999
LONGITUDE = 120.2270

API_URL = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUDE}"
    f"&longitude={LONGITUDE}"
    "&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max"
    "&timezone=Asia%2FTaipei"
    "&forecast_days=7"
)


def weather_code_to_text(code):
    weather_dict = {
        0: "晴天",
        1: "大致晴朗",
        2: "局部多雲",
        3: "陰天",
        45: "霧",
        48: "霧淞",
        51: "小毛雨",
        53: "毛雨",
        55: "大毛雨",
        56: "凍毛雨",
        57: "強凍毛雨",
        61: "小雨",
        63: "中雨",
        65: "大雨",
        66: "凍雨",
        67: "強凍雨",
        71: "小雪",
        73: "中雪",
        75: "大雪",
        77: "雪粒",
        80: "短暫小雨",
        81: "短暫中雨",
        82: "短暫大雨",
        85: "短暫小雪",
        86: "短暫大雪",
        95: "雷雨",
        96: "雷雨伴隨小冰雹",
        99: "雷雨伴隨大冰雹"
    }
    return weather_dict.get(code, "未知天氣")



# 穿搭與帶傘提醒

def get_outfit_advice(max_temp, min_temp, rain_prob):
    advice = []

    # 穿搭判斷
    if max_temp >= 28:
        advice.append("建議穿短袖，天氣炎熱，要注意防曬與補水喔!才不會中暑!!")
    elif max_temp >= 25:
        advice.append("建議穿短袖或輕便衣物，怕太熱")
    elif max_temp >= 22:
        advice.append("可穿薄長袖或短袖")
    else:
        advice.append("建議穿薄外套或長袖，小心著涼喔")

    # 日夜溫差判斷
    if (max_temp - min_temp) >= 8:
        advice.append("日夜溫差較大，早晚可多帶一件外套，才不會感冒==")

    # 雨傘判斷
    if rain_prob >= 60:
        advice.append("記得帶雨傘，才不會變成落湯雞呦")
    elif rain_prob >= 30:
        advice.append("建議攜帶折傘，以防萬一啦")
    else:
        advice.append("通常不用帶雨傘，免驚啦")

    return "；".join(advice)
def get_exercise_advice(max_temp, min_temp, rain_prob):
    if rain_prob >= 60:
        return "適合室內運動"
    elif rain_prob >= 30:
        return "適合輕度運動"
    else:
        if max_temp >= 28:
            return "適合輕度運動"
        elif max_temp >= 22:
            return "天氣舒適，適合戶外運動"
        else:
            return "天氣較涼，適合散步或慢跑"



# 抓天氣資料

def fetch_weather_data():
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        daily = data["daily"]

        df = pd.DataFrame({
            "日期": daily["time"],
            "天氣代碼": daily["weather_code"],
            "最高溫": daily["temperature_2m_max"],
            "最低溫": daily["temperature_2m_min"],
            "降雨機率": daily["precipitation_probability_max"]
        })

        df["天氣狀況"] = df["天氣代碼"].apply(weather_code_to_text)

        df["提醒"] = df.apply(
            lambda row: get_outfit_advice(
                row["最高溫"],
                row["最低溫"],
                row["降雨機率"]
            ),
            axis=1
        )
        df["適合運動"] = df.apply(
    lambda row: get_exercise_advice(
        row["最高溫"],
        row["最低溫"],
        row["降雨機率"]
    ),
    axis=1
)

        return df

    except requests.exceptions.RequestException as e:
        print("無法取得天氣資料，請檢查網路或 API 狀態。")
        print("錯誤訊息：", e)
        return None



# 顯示天氣資訊

def show_weather(df):
    print("=" * 60)
    print("台南未來一週天氣與穿搭提醒系統")
    print("=" * 60)

    for _, row in df.iterrows():
        print(f"日期：{row['日期']}")
        print(f"天氣：{row['天氣狀況']}")
        print(f"最高溫：{row['最高溫']}°C")
        print(f"最低溫：{row['最低溫']}°C")
        print(f"降雨機率：{row['降雨機率']}%")
        print(f"提醒：{row['提醒']}")
        print(f"適合運動:{row['適合運動']}")
        print("-" * 60)



# 畫圖

def plot_temperature(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df["日期"], df["最高溫"], marker="o", label="最高溫")
    plt.plot(df["日期"], df["最低溫"], marker="o", label="最低溫")

    plt.title("台南未來一週高低溫變化")
    plt.xlabel("日期")
    plt.ylabel("溫度 (°C)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tainan_weather_chart.png")
    plt.show()



# 主程式

def main():
    df = fetch_weather_data()

    if df is not None:
        show_weather(df)

        display(df[["日期", "天氣狀況", "最高溫", "最低溫", "降雨機率", "提醒","適合運動"]])
        plot_temperature(df)

        # 如果你想把資料存成 CSV，可以取消下面註解
        df.to_csv("tainan_weather_report.csv", index=False, encoding="utf-8-sig")
        print("\n已輸出 tainan_weather_report.csv 與 tainan_weather_chart.png")


if __name__ == "__main__":
    main()

# %%



