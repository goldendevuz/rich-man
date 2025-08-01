import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Dastur sarlavhasi
st.set_page_config(layout="wide") # Kengroq sahifa tartibi
st.title("💰 Investitsiya Strategiyasi Simulyatori")
st.markdown("Ushbu dastur sizning AD&D aksiyasi, XonMobyil, Exxes, Dogecoin va Ko'chmas mulk investitsiya strategiyangizni vizual hisob-kitob qilishga yordam beradi.")

# --- Umumiy Investitsiya Ma'lumotlari ---
st.header("Umumiy Ma'lumotlar")

# AD&D aksiyasi doimiy ma'lumotlari
adnd_min_price = 20.04
adnd_max_price = 30.396
adnd_avg_price = (adnd_min_price + adnd_max_price) / 2 # Qayta hisoblangan o'rtacha
adnd_dividend_rate_per_3_hours = 0.0532 # 5.32%

# XonMobyil aksiyasi doimiy ma'lumotlari
xonmobyil_min_price = 49.59
xonmobyil_max_price = 75.072
xonmobyil_avg_price = (xonmobyil_min_price + xonmobyil_max_price) / 2 # Qayta hisoblangan o'rtacha
xonmobyil_dividend_rate_per_3_hours = 0.045 # 4.5%

# Ko'chmas mulk doimiy ma'lumotlari
real_estate_min_price = 42500
real_estate_income_rate_per_hour = 0.0158 # 1.58%

# Exxes Kriptovalyuta doimiy ma'lumotlari
# exxes_min_price = 346050.00
# exxes_avg_price = 384500.00
# exxes_max_price = 422950.00
# exxes_percentage_deviation = 10 # ±10% Foizli og'ish

# Dogecoin Kriptovalyuta doimiy ma'lumotlari
dogecoin_min_price = 0.0273
dogecoin_avg_price = 0.07
dogecoin_max_price = 0.1127
dogecoin_percentage_deviation = 61 # ±61% Foizli og'ish

# Ma'lumotlarni yangi tartibda ko'rsatish
st.write(f"**AD&D Stock Information:**")
st.write(f"- Minimum price: ${adnd_min_price:.2f}")
st.write(f"- Average price: ${adnd_avg_price:.2f}")
st.write(f"- Maximum price: ${adnd_max_price:.2f}")
st.write(f"- Dividend yield (per 3 hours): {adnd_dividend_rate_per_3_hours * 100:.2f}%")

st.write(f"**XonMobyil Stock Information:**")
st.write(f"- Minimum price: ${xonmobyil_min_price:.2f}")
st.write(f"- Average price: ${xonmobyil_avg_price:.2f}")
st.write(f"- Maximum price: ${xonmobyil_max_price:.2f}")
st.write(f"- Dividend yield (per 3 hours): {xonmobyil_dividend_rate_per_3_hours * 100:.2f}%")

# Exxes Cryptocurrency Information kommentga olindi
# st.write(f"**Exxes Cryptocurrency Information:**")
# st.write(f"- Minimum price: ${exxes_min_price:,.2f}")
# st.write(f"- Average price: ${exxes_avg_price:,.2f}")
# st.write(f"- Maximum price: ${exxes_max_price:,.2f}")
# st.write(f"- Percentage deviation: ±{exxes_percentage_deviation:.0f}% (High volatility)")

st.write(f"**Dogecoin Cryptocurrency Information:**")
st.write(f"- Minimum price: ${dogecoin_min_price:.4f}")
st.write(f"- Average price: ${dogecoin_avg_price:.2f}")
st.write(f"- Maximum price: ${dogecoin_max_price:.4f}")
st.write(f"- Percentage deviation: ±{dogecoin_percentage_deviation:.0f}% (High volatility)")

# Ko'chmas mulk ma'lumotlari endi 5-o'rinda
st.write(f"**Real Estate Information:**")
st.write(f"- Minimum price: ${real_estate_min_price:,.2f}")
st.write(f"- Hourly income yield: {real_estate_income_rate_per_hour * 100:.2f}% (Risk-free, income and value unchanging)")

st.markdown("---")

# --- Foydalanuvchi Kiritishlari ---
st.header("Sizning Kiritishlaringiz")

# Joriy investitsiya narxlarini kiritish
current_adnd_price = st.number_input(
    "AD&D Aksiyasining joriy narxini kiriting ($)",
    min_value=float(adnd_min_price),
    max_value=float(adnd_max_price),
    value=25.33,
    step=0.01,
    format="%.2f"
)

current_xonmobyil_price = st.number_input(
    "XonMobyil Aksiyasining joriy narxini kiriting ($)",
    min_value=float(xonmobyil_min_price),
    max_value=float(xonmobyil_max_price),
    value=62.56,
    step=0.01,
    format="%.2f"
)

# Exxes Kriptovalyutasini kiritish qismi kommentga olindi
# current_exxes_price = st.number_input(
#     "Exxes Kriptovalyutasining joriy narxini kiriting ($)",
#     min_value=float(exxes_min_price),
#     max_value=float(exxes_max_price),
#     value=exxes_avg_price,
#     step=100.00,
#     format="%.2f"
# )

current_dogecoin_price = st.number_input(
    "Dogecoin Kriptovalyutasining joriy narxini kiriting ($)",
    min_value=float(dogecoin_min_price),
    max_value=float(dogecoin_max_price),
    value=dogecoin_avg_price,
    step=0.001,
    format="%.3f"
)

investment_amount = st.number_input(
    "Investitsiya qilmoqchi bo'lgan umumiy mablag'ingizni kiriting ($)",
    min_value=100.0,
    value=5350000.0,
    step=1000.0,
    format="%.2f"
)

# Simulyatsiya davomiyligi
simulation_hours = st.slider(
    "Simulyatsiya davomiyligi (soatlarda)",
    min_value=1,
    max_value=720, # 30 kun * 24 soat
    value=240, # 10 kun
    step=1
)

st.markdown("---")

# --- Strategiya Analizi ---
st.header("Strategiya Analizi va Tavsiyalar")

# Beshta ustun yaratildi
col1, col2, col3, col4, col5 = st.columns(5) 

# Yangi strategiya logikasi
st.subheader("Hozirgi bozor sharoitida investitsiya tavsiyasi:")
if current_adnd_price <= adnd_avg_price:
    st.success(f"✅ AD&D Aksiyasi o'rtacha narxdan (${adnd_avg_price:.2f}) arzon yoki teng (${current_adnd_price:.2f}). **AD&D Aksiyasini sotib oling!**")
    recommended_buy = "AD&D"
elif current_xonmobyil_price <= xonmobyil_avg_price:
    st.success(f"✅ XonMobyil Aksiyasi o'rtacha narxdan (${xonmobyil_avg_price:.2f}) arzon yoki teng (${current_xonmobyil_price:.2f}). **XonMobyil Aksiyasini sotib oling!**")
    recommended_buy = "XonMobyil"
# Exxes Kriptovalyutasini hisoblovchi qism kommentga olindi
# elif current_exxes_price <= exxes_avg_price:
#     st.success(f"✅ Exxes Kriptovalyutasi o'rtacha narxdan (${exxes_avg_price:,.2f}) arzon yoki teng (${current_exxes_price:,.2f}). **Exxes Kriptovalyutasini sotib oling!**")
#     recommended_buy = "Exxes"
elif current_dogecoin_price <= dogecoin_avg_price:
    st.success(f"✅ Dogecoin Kriptovalyutasi o'rtacha narxdan (${dogecoin_avg_price:.2f}) arzon yoki teng (${current_dogecoin_price:.2f}). **Dogecoinni sotib oling!**")
    recommended_buy = "Dogecoin"
else:
    st.info(f"ℹ️ Yuqori riskli aktivlar o'rtacha narxdan arzon emas. **Ko'chmas mulkni sotib oling!**")
    recommended_buy = "Real Estate"

st.markdown("---")

# Ustunlar tarkibi
with col1: # AD&D uchun ustun
    st.subheader("AD&D Aksiyasi")
    buy_price_lower_bound = adnd_min_price
    buy_price_upper_bound = adnd_avg_price

    st.write(f"**Tavsiya etilgan sotib olish oralig'i:** ${buy_price_lower_bound:.2f} dan ${buy_price_upper_bound:.2f} gacha")

    if recommended_buy == "AD&D":
        st.success(f"✅ Joriy narx (${current_adnd_price:.2f}) tavsiya etilgan sotib olish oralig'ida.")
        actual_adnd_buy_price = current_adnd_price
        if actual_adnd_buy_price > 0:
            num_shares = investment_amount / actual_adnd_buy_price
            st.metric("Sotib olinadigan aksiyalar soni (taxminan)", f"{num_shares:,.0f}")
            adnd_hourly_dividend_income = (investment_amount * adnd_dividend_rate_per_3_hours) / 3
            st.metric("Soatlik dividend daromadi", f"${adnd_hourly_dividend_income:,.2f}")
            target_sell_price_adnd = actual_adnd_buy_price * 1.10
            st.metric("Maqsadli sotish narxi (+10% foyda)", f"${target_sell_price_adnd:,.2f}")
        else:
            st.error("Sotib olish narxi nol bo'lmasligi kerak.")
    else:
        st.info(f"⚠️ Joriy narx (${current_adnd_price:.2f}) yuqori yoki boshqa aktivlar tavsiya etilgan.")


with col2: # XonMobyil uchun ustun
    st.subheader("XonMobyil Aksiyasi")
    buy_price_lower_bound = xonmobyil_min_price
    buy_price_upper_bound = xonmobyil_avg_price

    st.write(f"**Tavsiya etilgan sotib olish oralig'i:** ${buy_price_lower_bound:.2f} dan ${buy_price_upper_bound:.2f} gacha")

    if recommended_buy == "XonMobyil":
        st.success(f"✅ Joriy narx (${current_xonmobyil_price:.2f}) tavsiya etilgan sotib olish oralig'ida.")
        actual_xonmobyil_buy_price = current_xonmobyil_price
        if actual_xonmobyil_buy_price > 0:
            num_shares = investment_amount / actual_xonmobyil_buy_price
            st.metric("Sotib olinadigan aksiyalar soni (taxminan)", f"{num_shares:,.0f}")
            xonmobyil_hourly_dividend_income = (investment_amount * xonmobyil_dividend_rate_per_3_hours) / 3
            st.metric("Soatlik dividend daromadi", f"${xonmobyil_hourly_dividend_income:,.2f}")
            target_sell_price_xonmobyil = actual_xonmobyil_buy_price * 1.10
            st.metric("Maqsadli sotish narxi (+10% foyda)", f"${target_sell_price_xonmobyil:,.2f}")
        else:
            st.error("Sotib olish narxi nol bo'lmasligi kerak.")
    else:
        st.info(f"⚠️ Joriy narx (${current_xonmobyil_price:.2f}) yuqori yoki boshqa aktivlar tavsiya etilgan.")


with col3: # Exxes uchun ustun
    # st.subheader("Exxes Kriptovalyuta")
    # st.write(f"**Tavsiya etilgan sotib olish oralig'i:** ${exxes_min_price:,.2f} dan ${exxes_avg_price:,.2f} gacha")

    # if recommended_buy == "Exxes":
    #     st.success(f"✅ Joriy narx (${current_exxes_price:,.2f}) tavsiya etilgan sotib olish oralig'ida.")
    #     actual_exxes_buy_price = current_exxes_price
    #     if actual_exxes_buy_price > 0:
    #         num_exxes_units = investment_amount / actual_exxes_buy_price
    #         st.metric("Sotib olinadigan Exxes soni (taxminan)", f"{num_exxes_units:,.2f}")
    #         target_sell_price_exxes = actual_exxes_buy_price * 1.10
    #         st.metric("Maqsadli sotish narxi (+10% foyda)", f"${target_sell_price_exxes:,.2f}")
    #     else:
    #         st.error("Exxes sotib olish narxi nol bo'lmasligi kerak.")
    # else:
    #     st.info(f"⚠️ Joriy narx (${current_exxes_price:,.2f}) yuqori yoki boshqa aktivlar tavsiya etilgan.")
    st.subheader("Exxes Kriptovalyuta")
    st.info("Bu bo'lim foydalanuvchi talabiga binoan vaqtincha faoliyatini to'xtatgan.")


with col4: # Dogecoin uchun ustun
    st.subheader("Dogecoin Kriptovalyuta")
    st.write(f"**Tavsiya etilgan sotib olish oralig'i:** ${dogecoin_min_price:.4f} dan ${dogecoin_avg_price:.2f} gacha")

    if recommended_buy == "Dogecoin":
        st.success(f"✅ Joriy narx (${current_dogecoin_price:.4f}) tavsiya etilgan sotib olish oralig'ida.")
        actual_dogecoin_buy_price = current_dogecoin_price
        if actual_dogecoin_buy_price > 0:
            num_dogecoin_units = investment_amount / actual_dogecoin_buy_price
            st.metric("Sotib olinadigan Dogecoin soni (taxminan)", f"{num_dogecoin_units:,.0f}")
            target_sell_price_dogecoin = actual_dogecoin_buy_price * 1.10
            st.metric("Maqsadli sotish narxi (+10% foyda)", f"${target_sell_price_dogecoin:,.2f}")
        else:
            st.error("Dogecoin sotib olish narxi nol bo'lmasligi kerak.")
    else:
        st.info(f"⚠️ Joriy narx (${current_dogecoin_price:.4f}) yuqori yoki boshqa aktivlar tavsiya etilgan.")

with col5: # Ko'chmas mulk
    st.subheader("Ko'chmas mulk")
    if recommended_buy == "Real Estate":
        st.success("✅ Hech bir yuqori riskli aktiv o'rtacha narxda emas. **Ko'chmas mulk** tavsiya etiladi.")
        real_estate_hourly_income = investment_amount * real_estate_income_rate_per_hour
        st.metric("Ko'chmas mulkdan soatlik daromad", f"${real_estate_hourly_income:,.2f}")
        st.markdown("""
        **Afzalliklari:**
        - **Mutlaq kapital xavfsizligi:** Qiymat o'zgarmas.
        - **Kafolatlangan daromad:** Doimiy pul oqimi.
        """)
        st.markdown(f"**Eng past narx:** ${real_estate_min_price:,.2f}")
        
        st.markdown("---")
        st.subheader("Mavjud Mulklar Ro'yxati")
        
        residential_buildings_data = {
          "Global Percentage Income": 1.58,
          "Buildings": [
            { "Building": "Abu Dhabi,United Arab Emirates (Residental)", "Price": 766000000, "Rental income (per hour)": 12102800 },
            { "Building": "Ankara,Turkey", "Price": 2500000, "Rental income (per hour)": 39500 },
            { "Building": "Barcelona,Spain", "Price": 30000000, "Rental income (per hour)": 474000 },
            { "Building": "Berlin,Germany", "Price": 3800000, "Rental income (per hour)": 60040 },
            { "Building": "Burlington,Canada", "Price": 74000, "Rental income (per hour)": 1169.2 },
            { "Building": "Florida ,USA", "Price": 660000, "Rental income (per hour)": 10428 },
            { "Building": "French Riviera,France", "Price": 900000000, "Rental income (per hour)": 14220000 },
            { "Building": "Gelendzhik,Russia", "Price": 1500000000, "Rental income (per hour)": 23700000 },
            { "Building": "Helsinki,Finland", "Price": 1800000, "Rental income (per hour)": 28440 },
            { "Building": "Ibiza,Spain", "Price": 6300000, "Rental income (per hour)": 99540 },
            { "Building": "Istanbul,Turkey", "Price": 40000000, "Rental income (per hour)": 632000 },
            { "Building": "Karlstad,Sweden", "Price": 10850000, "Rental income (per hour)": 171430 },
            { "Building": "Kon Tum,Vietnam", "Price": 18000000, "Rental income (per hour)": 284400 },
            { "Building": "Liverpool,UK", "Price": 20000000, "Rental income (per hour)": 316000 },
            { "Building": "London,UK 1", "Price": 105000, "Rental income (per hour)": 1659 },
            { "Building": "London,UK_", "Price": 12350000, "Rental income (per hour)": 195130 },
            { "Building": "Los Angeles,USA 1", "Price": 55000000, "Rental income (per hour)": 869000 },
            { "Building": "Los Angeles,USA 2", "Price": 70000000, "Rental income (per hour)": 1106000 },
            { "Building": "Los Angeles,USA 3", "Price": 150000000, "Rental income (per hour)": 2370000 },
            { "Building": "Lublin,Poland", "Price": 32000, "Rental income (per hour)": 505.6 },
            { "Building": "Lyon,France", "Price": 168000, "Rental income (per hour)": 2654.4 },
            { "Building": "Manchester,UK", "Price": 7700000, "Rental income (per hour)": 121660 },
            { "Building": "Mexico City,Mexico", "Price": 9500000, "Rental income (per hour)": 150100 },
            { "Building": "Molokai,Hawaii", "Price": 8750000, "Rental income (per hour)": 138250 },
            { "Building": "Monte-Carlo,Monaco", "Price": 90000000, "Rental income (per hour)": 1422000 },
            { "Building": "Montreal,Canada", "Price": 5000000, "Rental income (per hour)": 79000 },
            { "Building": "Moscow,Russia 1", "Price": 725000, "Rental income (per hour)": 11455 },
            { "Building": "Moscow,Russia 2", "Price": 1350000, "Rental income (per hour)": 21330 },
            { "Building": "New Mexico,USA", "Price": 11300000, "Rental income (per hour)": 178540 },
            { "Building": "New Plymouth,New Zealand", "Price": 17445000, "Rental income (per hour)": 275631 },
            { "Building": "New York,USA 1", "Price": 100000000, "Rental income (per hour)": 1580000 },
            { "Building": "Nuremberg,Germany", "Price": 210000, "Rental income (per hour)": 3318 },
            { "Building": "Nuuk,Greenland", "Price": 16050000, "Rental income (per hour)": 253590 },
            { "Building": "Pisa,Italy", "Price": 8200000, "Rental income (per hour)": 129560 },
            { "Building": "Porvoo,Finland", "Price": 990000, "Rental income (per hour)": 15642 },
            { "Building": "Saint-Petersburg,Russia", "Price": 10450000, "Rental income (per hour)": 165110 },
            { "Building": "Stavropol,Russia", "Price": 55000, "Rental income (per hour)": 869 },
            { "Building": "Stavropol,Russia", "Price": 480000, "Rental income (per hour)": 7584 },
            { "Building": "Stavropol,Russia", "Price": 1880000, "Rental income (per hour)": 29704 },
            { "Building": "Sydney,Australia", "Price": 7150000, "Rental income (per hour)": 112970 },
            { "Building": "Tijuana,Mexico", "Price": 15000000, "Rental income (per hour)": 237000 },
            { "Building": "Toronto,Canada (Residental)", "Price": 3080000, "Rental income (per hour)": 48664 },
            { "Building": "Valencia,Spain", "Price": 4555000, "Rental income (per hour)": 71969 },
            { "Building": "Washington,USA (Residental)", "Price": 13750000, "Rental income (per hour)": 217250 }
          ]
        }
        
        df_residential_buildings = pd.DataFrame(residential_buildings_data["Buildings"])
        
        # Narx va daromadni formatlash
        df_residential_buildings['Price'] = df_residential_buildings['Price'].apply(lambda x: f"${x:,.0f}")
        df_residential_buildings['Rental income (per hour)'] = df_residential_buildings['Rental income (per hour)'].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(df_residential_buildings, height=300)
    else:
        st.info("Boshqa aktivlar tavsiya etilgan.")


st.markdown("---")

# --- Simulyatsiya Natijalari ---
st.header("Simulyatsiya Natijalari")

st.subheader(f"Investitsiya o'sishi ({simulation_hours} soat davomida)")

hours = np.arange(0, simulation_hours + 1, 1)
adnd_accumulated_dividends = []
xonmobyil_accumulated_dividends = []
real_estate_accumulated_income = []

current_adnd_total = investment_amount
current_xonmobyil_total = investment_amount
current_real_estate_total = investment_amount

for h in hours:
    if h % 3 == 0 and h > 0:
        current_adnd_total += (investment_amount * adnd_dividend_rate_per_3_hours)
        current_xonmobyil_total += (investment_amount * xonmobyil_dividend_rate_per_3_hours)

    adnd_accumulated_dividends.append(current_adnd_total)
    xonmobyil_accumulated_dividends.append(current_xonmobyil_total)

    current_real_estate_total += (investment_amount * real_estate_income_rate_per_hour)
    real_estate_accumulated_income.append(current_real_estate_total)

df_simulation = pd.DataFrame({
    'Soat': hours,
    'AD&D (faqat dividend)': adnd_accumulated_dividends,
    'XonMobyil (faqat dividend)': xonmobyil_accumulated_dividends,
    'Ko\'chmas mulk': real_estate_accumulated_income
})

chart = alt.Chart(df_simulation.melt('Soat', value_name='Qiymat', var_name='Investitsiya turi')).mark_line().encode(
    x=alt.X('Soat', title='Vaqt (soatlarda)'),
    y=alt.Y('Qiymat', title='Investitsiya qiymati ($)'),
    color=alt.Color('Investitsiya turi', scale=alt.Scale(range=['#FF4B4B', '#FFD700', '#26B2FF']), title='Investitsiya turi')
).properties(
    title='Vaqt o\'tishi bilan investitsiya o\'sishi'
).interactive()

st.altair_chart(chart, use_container_width=True)

# Kriptovalyutalarning potentsial foydasi
# Exxes hisob-kitobi kommentga olindi
# total_potential_exxes_profit = 0
# if current_exxes_price > 0:
#     num_exxes_units_for_summary = investment_amount / current_exxes_price
#     potential_profit_per_unit_summary = exxes_max_price - current_exxes_price
#     total_potential_exxes_profit = num_exxes_units_for_summary * potential_profit_per_unit_summary

total_potential_dogecoin_profit = 0
if current_dogecoin_price > 0:
    num_dogecoin_units_for_summary = investment_amount / current_dogecoin_price
    potential_profit_per_unit_summary = dogecoin_max_price - current_dogecoin_price
    total_potential_dogecoin_profit = num_dogecoin_units_for_summary * potential_profit_per_unit_summary

st.markdown(f"""
**Simulyatsiya xulosasi ({simulation_hours} soatdan keyin):**
- **AD&D (faqat dividend orqali):** ${adnd_accumulated_dividends[-1]:,.2f}
- **XonMobyil (faqat dividend orqali):** ${xonmobyil_accumulated_dividends[-1]:,.2f}
- **Ko'chmas mulk:** ${real_estate_accumulated_income[-1]:,.2f}

**Kriptovalyutalar bo'yicha qo'shimcha eslatma:**
- Yuqoridagi grafik doimiy daromadli aktivlarni ko'rsatadi. Kriptovalyutalarning daromadi esa narx o'zgarishlariga bog'liq bo'lib, bir martalik savdo siklidan olinadi.
- **Bir Dogecoin savdo siklidan kutilayotgan potentsial foyda (joriy narxda sotib olib, maksimal narxda sotilganda):** ${total_potential_dogecoin_profit:,.2f} (Sizning ${investment_amount:,.2f} sarmoyangiz uchun)

**Eslatma:** Bu simulyatsiya narx tebranishlarini hisobga olmaydi, faqat dividend/ijara daromadini ko'rsatadi. Haqiqiy o'yinda narxlar o'zgarishi mumkin.
""")

st.markdown("---")

# --- Umumiy Strategiya Xulosasi ---
st.header("Umumiy Strategiya Xulosasi")
st.markdown("""
1.  **Kutish davrida (Kam risk):** Bo'sh mablag'ingizni **Ko'chmas mulkka** investitsiya qiling. Bu sizga yuqori riskli aktivlarning narxi tushishini kutayotganingizda ham barqaror va risksiz passiv daromad olish imkonini beradi.
2.  **AD&D va XonMobyil aksiyalari (O'rta risk/Yuqori passiv daromad):** Narxlar o'rtacha narxdan past bo'lganida aksiyalarni sotib oling. Ushlab turganingizda yuqori dividend daromadini oling va narx sotib olganingizdan kamida 10% yuqoriga chiqqanda soting.
3.  **Exxes va Dogecoin Kriptovalyutalari (Yuqori risk/Yuqori potentsial foyda):**
    * Agar siz **yuqori riskni qabul qilishga tayyor bo'lsangiz** va tezroq, bir martalik katta foyda olishni istasangiz, ularni ko'rib chiqing.
    * Ularni **minimal narxga yaqin** bo'lganida sotib olishni maqsad qiling.
    * Narxi **maksimal narxga yaqin** bo'lganida soting.
    * **Tavsiya:** Kriptovalyutalarga investitsiya qilishdan oldin, aksiyalar yoki Ko'chmas mulkdan olingan foydani ishlatishni ko'rib chiqing, chunki bu o'z sarmoyangizni xavf ostiga qo'ymaslikka yordam beradi.
4.  **Takrorlash:** Har bir investitsiya turidan foyda olgandan so'ng, mablag'ni qayta taqsimlash va strategiyani takrorlashni ko'rib chiqing.
""")
