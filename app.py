import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="تحليل الأسهم - العرض والطلب", layout="wide")

st.title("📈 تطبيق تحليل الأسهم الذكي")
st.write("هذا التطبيق يساعدك على فهم العرض والطلب والقيمة المتوقعة للسهم بناءً على بيانات السوق.")

# إدخال رمز السهم
symbol = st.text_input("أدخل رمز السهم (مثل: AAPL، TSLA، 2330.TW):", "AAPL")

if symbol:
    try:
        # جلب البيانات من Yahoo Finance
        data = yf.download(symbol, period="6mo", interval="1d")
        
        if not data.empty:
            st.subheader(f"بيانات السهم: {symbol}")
            st.line_chart(data["Close"], use_container_width=True)

            # حساب متوسط العرض والطلب التقريبي
            data["Change"] = data["Close"].pct_change() * 100
            avg_demand = data[data["Change"] > 0]["Change"].mean()
            avg_supply = abs(data[data["Change"] < 0]["Change"].mean())
            trend = "🔺 الطلب أقوى" if avg_demand > avg_supply else "🔻 العرض أقوى"

            st.markdown(f"**تحليل سريع:** {trend}")
            st.write(f"متوسط زيادة السعر اليومية: {avg_demand:.2f}%")
            st.write(f"متوسط انخفاض السعر اليومية: {avg_supply:.2f}%")

            # حساب القيمة المتوقعة بناء على المتوسط
            last_price = data["Close"][-1]
            # تحقق من last_price و avg_demand و avg_supply
if pd.notna(last_price) and pd.notna(avg_demand) and pd.notna(avg_supply):
    expected_value = last_price * (1 + (avg_demand - avg_supply) / 200)
    change_value = expected_value - last_price
else:
    expected_value = last_price if pd.notna(last_price) else 0
    change_value = 0

# عرض القيمة المتوقعة بأمان
st.metric("القيمة المتوقعة للسهم", f"${expected_value:.2f}", f"{change_value:.2f}")
        else:
            st.warning("⚠️ لم يتم العثور على بيانات لهذا الرمز.")
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
