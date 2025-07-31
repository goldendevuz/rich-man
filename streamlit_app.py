import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(layout="wide")
st.title("💰 Investitsiya Strategiyasi Simulyatori")
st.markdown("Ushbu dastur sizning AD&D aksiyasi va Ko'chmas mulk investitsiya strategiyangizni vizual hisob-kitob qilishga yordam beradi.")

st.header("Umumiy Ma'lumotlar")

adnd_min_price = 20.264
adnd_avg_price = 25.33
adnd_max_price = 30.396
adnd_dividend_rate_per_3_hours = 0.0532

real_estate_income_rate_per_hour = 0.0158

st.write(f"**AD&D Aksiyasi Ma'lumotlari:**")
st.write(f"- Minimal narx: ${adnd_min_price:.2f}")
st.write(f"- O'rtacha narx: ${adnd_avg_price:.2f}")
st.write(f"- Maksimal narx: ${adnd_max_price:.2f}")
st.write(f"- Dividend rentabelligi (har 3 soatda): {adnd_dividend_rate_per_3_hours * 100:.2f}%")

st.write(f"**Ko'chmas mulk Ma'lumotlari:**")
st.write(f"- Soatlik daromad rentabelligi: {real_estate_income_rate_per_hour * 100:.2f}% (Risk-siz, daromad va qiymat o'zgarmas)")

st.markdown("---")

st.header("Sizning Kiritishlaringiz")

current_adnd_price = st.number_input(
    "AD&D Aksiyasining joriy narxini kiriting ($)",
    min_value=float(adnd_min_price),
    max_value=float(adnd_max_price),
    value=27.31,
    step=0.01,
    format="%.2f"
)

investment_amount = st.number_input(
    "Investitsiya qilmoqchi bo'lgan umumiy mablag'ingizni kiriting ($)",
    min_value=100.0,
    value=5350000.0,
    step=1000.0,
    format="%.2f"
)

simulation_hours = st.slider(
    "Simulyatsiya davomiyligi (soatlarda)",
    min_value=1,
    max_value=720,
    value=240,
    step=1
)

st.markdown("---")

st.header("Strategiya Analizi va Tavsiyalar")

col1, col2 = st.columns(2)

with col1:
    st.subheader("AD&D Aksiyasi Strategiyasi")
    buy_price_lower_bound = adnd_min_price
    buy_price_upper_bound = adnd_avg_price

    st.write(f"**Tavsiya etilgan AD&D sotib olish oralig'i:** ${buy_price_lower_bound:.2f} dan ${buy_price_upper_bound:.2f} gacha")

    if current_adnd_price <= buy_price_upper_bound:
        st.success(f"✅ Joriy narx (${current_adnd_price:.2f}) tavsiya etilgan sotib olish oralig'ida. AD&D aksiyasini sotib olishni ko'rib chiqing.")
        actual_buy_price = current_adnd_price
    else:
        st.warning(f"⚠️ Joriy narx (${current_adnd_price:.2f}) tavsiya etilgan sotib olish oralig'idan yuqori. Narx tushishini kuting.")
        actual_buy_price = adnd_avg_price
        st.info(f"Hisob-kitoblar uchun ${actual_buy_price:.2f} (o'rtacha narx) asos qilib olindi.")


    if actual_buy_price > 0:
        num_shares = investment_amount / actual_buy_price
        st.metric("Sotib olinadigan aksiyalar soni (taxminan)", f"{num_shares:,.0f}")

        adnd_hourly_dividend_income = (investment_amount * adnd_dividend_rate_per_3_hours) / 3
        st.metric("AD&D dan soatlik dividend daromadi (taxminan)", f"${adnd_hourly_dividend_income:,.2f}")

        target_sell_price = actual_buy_price * 1.10
        st.metric("Maqsadli sotish narxi (+10% foyda bilan)", f"${target_sell_price:,.2f}")
        st.write(f"Sizning sotib olish narxingiz ${actual_buy_price:.2f} bo'lsa, kamida 10% foyda olish uchun ${target_sell_price:.2f} ga chiqqanda sotishingiz mumkin.")
        st.write(f"AD&D aksiyasining maksimal narxi ${adnd_max_price:.2f} ekanligini unutmang.")
    else:
        st.error("Sotib olish narxi nol bo'lmasligi kerak.")

with col2:
    st.subheader("Ko'chmas mulk Strategiyasi")
    st.write("AD&D aksiyasining narxi tushishini kutayotganingizda, mablag'ingizni Ko'chmas mulkka investitsiya qilishni ko'rib chiqing.")
    st.write("Sizning ma'lumotingizga ko'ra, Ko'chmas mulkning qiymati va ijara daromadi o'yinda butunlay o'zgarmas (risk-siz).")

    real_estate_hourly_income = investment_amount * real_estate_income_rate_per_hour
    st.metric("Ko'chmas mulkdan soatlik daromad", f"${real_estate_hourly_income:,.2f}")

    st.markdown("""
    **Ko'chmas mulk afzalliklari:**
    - **Mutlaq kapital xavfsizligi:** Qiymat o'zgarmasligi sababli yo'qotish xavfi yo'q.
    - **Kafolatlangan daromad:** Doimiy va oldindan aytib bo'ladigan pul oqimi.
    """)

st.markdown("---")

st.header("Simulyatsiya Natijalari")

st.subheader(f"Investitsiya o'sishi ({simulation_hours} soat davomida)")

hours = np.arange(0, simulation_hours + 1, 1)
adnd_accumulated_dividends = []
real_estate_accumulated_income = []

current_adnd_total = investment_amount
current_real_estate_total = investment_amount

for h in hours:
    if h % 3 == 0 and h > 0:
        current_adnd_total += (investment_amount * adnd_dividend_rate_per_3_hours)

    adnd_accumulated_dividends.append(current_adnd_total)

    current_real_estate_total += (investment_amount * real_estate_income_rate_per_hour)
    real_estate_accumulated_income.append(current_real_estate_total)

df_simulation = pd.DataFrame({
    'Soat': hours,
    'AD&D (faqat dividend)': adnd_accumulated_dividends,
    'Ko\'chmas mulk': real_estate_accumulated_income
})

chart = alt.Chart(df_simulation.melt('Soat', value_name='Qiymat', var_name='Investitsiya turi')).mark_line().encode(
    x=alt.X('Soat', title='Vaqt (soatlarda)'),
    y=alt.Y('Qiymat', title='Investitsiya qiymati ($)'),
    color=alt.Color('Investitsiya turi', scale=alt.Scale(range=['#FF4B4B', '#26B2FF']), title='Investitsiya turi')
).properties(
    title='Vaqt o\'tishi bilan investitsiya o\'sishi'
).interactive()

st.altair_chart(chart, use_container_width=True)

st.markdown(f"""
**Simulyatsiya xulosasi ({simulation_hours} soatdan keyin):**
- **AD&D (faqat dividend orqali):** ${adnd_accumulated_dividends[-1]:,.2f}
- **Ko'chmas mulk:** ${real_estate_accumulated_income[-1]:,.2f}

**Eslatma:** Bu simulyatsiya AD&D aksiyasining narx tebranishlarini hisobga olmaydi, faqat dividend daromadini ko'rsatadi. Haqiqiy o'yinda AD&D ning narxi ham o'zgarishi mumkin. Ko'chmas mulk esa sizning ma'lumotingizga ko'ra butunlay barqaror.
""")

st.markdown("---")

st.header("Umumiy Strategiya Xulosasi")
st.markdown("""
1.  **Kutish davrida:** Bo'sh mablag'ingizni **Ko'chmas mulkka** investitsiya qiling. Bu sizga AD&D aksiyasining narxi tushishini kutayotganingizda ham barqaror va risksiz passiv daromad olish imkonini beradi.
2.  **AD&D narxi tushganda:** Narx **$22.00 dan $25.33 gacha** bo'lgan oralig'ida aksiyani sotib oling.
3.  **Ushlab turing va dividend yig'ing:** Aksiyani sotib olganingizdan keyin, narxi ko'tarilishini kutayotganingizda, har 3 soatda 5.32% juda yuqori dividend daromadini olishda davom eting.
4.  **Foyda bilan soting:** Siz sotib olgan narxdan **kamida 10% yuqori bo'lgan narxda** aksiyani soting.
5.  **Takrorlash:** Aksiyani sotgandan so'ng, olingan foydani va asosiy sarmoyani yana Ko'chmas mulkga o'tkazing va AD&D aksiyasining navbatdagi tushishini kuting.
""")
