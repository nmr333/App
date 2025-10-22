# تحقق من last_price و avg_demand و avg_supply
if pd.notna(last_price) and pd.notna(avg_demand) and pd.notna(avg_supply):
    expected_value = last_price * (1 + (avg_demand - avg_supply) / 200)
    change_value = expected_value - last_price
else:
    expected_value = last_price if pd.notna(last_price) else 0
    change_value = 0

# عرض القيمة المتوقعة بأمان
st.metric("القيمة المتوقعة للسهم", f"${expected_value:.2f}", f"{change_value:.2f}")
