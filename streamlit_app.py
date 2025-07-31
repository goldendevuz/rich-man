import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Dastur sarlavhasi
st.set_page_config(layout="wide") # Kengroq sahifa tartibi
st.title("💰 Investitsiya Strategiyasi Simulyatori")
st.markdown("Ushbu dastur sizning AD&D aksiyasi, Ko'chmas mulk va Kriptovalyuta investitsiya strategiyangizni vizual hisob-kitob qilishga yordam beradi.")

# --- Umumiy Investitsiya Ma'lumotlari ---
st.header("Umumiy Ma'lumotlar")

# AD&D aksiyasi doimiy ma'lumotlari
adnd_min_price = 20.264
adnd_avg_price = 25.33
adnd_max_price = 30.396
adnd_dividend_rate_per_3_hours = 0.0532 # 5.32%

# Ko'chmas mulk doimiy ma'lumotlari
real_estate_income_rate_per_hour = 0.0158 # 1.58%

# Exxes Kriptovalyuta doimiy ma'lumotlari (oldingi suhbatlardan)
exxes_min_price = 346050.00
exxes_avg_price = 384500.00
exxes_max_price = 422950.00
exxes_percentage_deviation = 10 # ±10% Foizli og'ish

st.write(f"**AD&D Stock Information:**")
st.write(f"- Minimum price: ${adnd_min_price:.2f}")
st.write(f"- Average price: ${adnd_avg_price:.2f}")
st.write(f"- Maximum price: ${adnd_max_price:.2f}")
st.write(f"- Dividend yield (per 3 hours): {adnd_dividend_rate_per_3_hours * 100:.2f}%")

st.write(f"**Real Estate Information:**")
st.write(f"- Hourly income yield: {real_estate_income_rate_per_hour * 100:.2f}% (Risk-free, income and value unchanging)")

st.write(f"**Exxes Cryptocurrency Information:**")
st.write(f"- Minimum price: ${exxes_min_price:,.2f}")
st.write(f"- Average price: ${exxes_avg_price:,.2f}")
st.write(f"- Maximum price: ${exxes_max_price:,.2f}")
st.write(f"- Percentage deviation: ±{exxes_percentage_deviation:.0f}% (High volatility)")


st.markdown("---")

# --- Foydalanuvchi Kiritishlari ---
st.header("Sizning Kiritishlaringiz")

# Joriy AD&D aksiya narxini kiritish
current_adnd_price = st.number_input(
    "AD&D Aksiyasining joriy narxini kiriting ($)",
    min_value=float(adnd_min_price),
    max_value=float(adnd_max_price),
    value=27.31, # Screenshotdagi joriy narx
    step=0.01,
    format="%.2f"
)

# Joriy Exxes kriptovalyuta narxini kiritish
current_exxes_price = st.number_input(
    "Exxes Kriptovalyutasining joriy narxini kiriting ($)",
    min_value=float(exxes_min_price),
    max_value=float(exxes_max_price),
    value=384500.00, # O'rtacha narx
    step=100.00,
    format="%.2f"
)

# Investitsiya miqdorini kiritish
investment_amount = st.number_input(
    "Investitsiya qilmoqchi bo'lgan umumiy mablag'ingizni kiriting ($)",
    min_value=100.0,
    value=5350000.0, # Oldingi misoldagi summa
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

col1, col2, col3 = st.columns(3) # Uchta ustun yaratildi

# Yangi strategiya logikasi
st.subheader("Hozirgi bozor sharoitida investitsiya tavsiyasi:")
if current_adnd_price <= adnd_avg_price: # <= ga o'zgartirildi
    st.success(f"✅ AD&D Aksiyasi o'rtacha narxdan (${adnd_avg_price:.2f}) arzon yoki teng (${current_adnd_price:.2f}). **AD&D Aksiyasini sotib oling!**")
    recommended_buy = "AD&D"
elif current_exxes_price <= exxes_avg_price: # <= ga o'zgartirildi
    st.success(f"✅ Exxes Kriptovalyutasi o'rtacha narxdan (${exxes_avg_price:,.2f}) arzon yoki teng (${current_exxes_price:,.2f}). **Exxes Kriptovalyutasini sotib oling!**")
    recommended_buy = "Exxes"
else:
    st.info(f"ℹ️ AD&D va Exxes o'rtacha narxdan arzon emas. **Ko'chmas mulkni sotib oling!**")
    recommended_buy = "Real Estate"

st.markdown("---") # Ajratuvchi chiziq

# Ustunlarni qayta tartiblash
# col1 endi Ko'chmas mulk uchun
# col2 endi AD&D uchun
# col3 Exxes uchun

with col1: # Bu endi Ko'chmas mulk ustuni
    st.subheader("Ko'chmas mulk Strategiyasi")
    if recommended_buy == "Real Estate":
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
        st.subheader("Mavjud Ko'chmas Mulklar Ro'yxati")
        
        # Residential buildings data from the JSON provided by the user
        residential_buildings_data = {
          "Global Percentage Income": 1.58,
          "Buildings": [
            {
              "Building": "Abu Dhabi,United Arab Emirates (Residental)",
              "Price": 766000000,
              "Rental income (per hour)": 12102800
            },
            {
              "Building": "Ankara,Turkey",
              "Price": 2500000,
              "Rental income (per hour)": 39500
            },
            {
              "Building": "Barcelona,Spain",
              "Price": 30000000,
              "Rental income (per hour)": 474000
            },
            {
              "Building": "Berlin,Germany",
              "Price": 3800000,
              "Rental income (per hour)": 60040
            },
            {
              "Building": "Burlington,Canada",
              "Price": 74000,
              "Rental income (per hour)": 1169.2
            },
            {
              "Building": "Florida ,USA",
              "Price": 660000,
              "Rental income (per hour)": 10428
            },
            {
              "Building": "French Riviera,France",
              "Price": 900000000,
              "Rental income (per hour)": 14220000
            },
            {
              "Building": "Gelendzhik,Russia",
              "Price": 1500000000,
              "Rental income (per hour)": 23700000
            },
            {
              "Building": "Helsinki,Finland",
              "Price": 1800000,
              "Rental income (per hour)": 28440
            },
            {
              "Building": "Ibiza,Spain",
              "Price": 6300000,
              "Rental income (per hour)": 99540
            },
            {
              "Building": "Istanbul,Turkey",
              "Price": 40000000,
              "Rental income (per hour)": 632000
            },
            {
              "Building": "Karlstad,Sweden",
              "Price": 10850000,
              "Rental income (per hour)": 171430
            },
            {
              "Building": "Kon Tum,Vietnam",
            "Price": 18000000,
              "Rental income (per hour)": 284400
            },
            {
              "Building": "Liverpool,UK",
              "Price": 20000000,
              "Rental income (per hour)": 316000
            },
            {
              "Building": "London,UK 1",
              "Price": 105000,
              "Rental income (per hour)": 1659
            },
            {
              "Building": "London,UK_",
              "Price": 12350000,
              "Rental income (per hour)": 195130
            },
            {
              "Building": "Los Angeles,USA 1",
              "Price": 55000000,
              "Rental income (per hour)": 869000
            },
            {
              "Building": "Los Angeles,USA 2",
              "Price": 70000000,
              "Rental income (per hour)": 1106000
            },
            {
              "Building": "Los Angeles,USA 3",
              "Price": 150000000,
              "Rental income (per hour)": 2370000
            },
            {
              "Building": "Lublin,Poland",
              "Price": 32000,
              "Rental income (per hour)": 505.6
            },
            {
              "Building": "Lyon,France",
              "Price": 168000,
              "Rental income (per hour)": 2654.4
            },
            {
              "Building": "Manchester,UK",
              "Price": 7700000,
              "Rental income (per hour)": 121660
            },
            {
              "Building": "Mexico City,Mexico",
              "Price": 9500000,
              "Rental income (per hour)": 150100
            },
            {
              "Building": "Molokai,Hawaii",
              "Price": 8750000,
              "Rental income (per hour)": 138250
            },
            {
              "Building": "Monte-Carlo,Monaco",
              "Price": 90000000,
              "Rental income (per hour)": 1422000
            },
            {
              "Building": "Montreal,Canada",
              "Price": 5000000,
              "Rental income (per hour)": 79000
            },
            {
              "Building": "Moscow,Russia 1",
              "Price": 725000,
              "Rental income (per hour)": 11455
            },
            {
              "Building": "Moscow,Russia 2",
              "Price": 1350000,
              "Rental income (per hour)": 21330
            },
            {
              "Building": "New Mexico,USA",
              "Price": 11300000,
              "Rental income (per hour)": 178540
            },
            {
              "Building": "New Plymouth,New Zealand",
              "Price": 17445000,
              "Rental income (per hour)": 275631
            },
            {
              "Building": "New York,USA 1",
              "Price": 100000000,
              "Rental income (per hour)": 1580000
            },
            {
              "Building": "Nuremberg,Germany",
              "Price": 210000,
              "Rental income (per hour)": 3318
            },
            {
              "Building": "Nuuk,Greenland",
              "Price": 16050000,
              "Rental income (per hour)": 253590
            },
            {
              "Building": "Pisa,Italy",
              "Price": 8200000,
              "Rental income (per hour)": 129560
            },
            {
              "Building": "Porvoo,Finland",
              "Price": 990000,
              "Rental income (per hour)": 15642
            },
            {
              "Building": "Saint-Petersburg,Russia",
              "Price": 10450000,
              "Rental income (per hour)": 165110
            },
            {
              "Building": "Stavropol,Russia",
              "Price": 55000,
              "Rental income (per hour)": 869
            },
            {
              "Building": "Stavropol,Russia",
              "Price": 480000,
              "Rental income (per hour)": 7584
            },
            {
              "Building": "Stavropol,Russia",
              "Price": 1880000,
              "Rental income (per hour)": 29704
            },
            {
              "Building": "Sydney,Australia",
              "Price": 7150000,
              "Rental income (per hour)": 112970
            },
            {
              "Building": "Tijuana,Mexico",
              "Price": 15000000,
              "Rental income (per hour)": 237000
            },
            {
              "Building": "Toronto,Canada (Residental)",
              "Price": 3080000,
              "Rental income (per hour)": 48664
            },
            {
              "Building": "Valencia,Spain",
              "Price": 4555000,
              "Rental income (per hour)": 71969
            },
            {
              "Building": "Washington,USA (Residental)",
              "Price": 13750000,
              "Rental income (per hour)": 217250
            }
          ]
        }
        
        df_residential_buildings = pd.DataFrame(residential_buildings_data["Buildings"])
        
        # Narx va daromadni formatlash
        df_residential_buildings['Price'] = df_residential_buildings['Price'].apply(lambda x: f"${x:,.0f}")
        df_residential_buildings['Rental income (per hour)'] = df_residential_buildings['Rental income (per hour)'].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(df_residential_buildings, height=300) # Ko'chmas mulk ro'yxatini ko'rsatish
        
    else:
        st.info("Ko'chmas mulk tavsiya etilmagan, chunki AD&D yoki Exxes o'rtacha narxdan arzon.")


with col2: # Bu endi AD&D ustuni
    st.subheader("AD&D Aksiyasi Strategiyasi")
    # Sotib olish narxi oralig'ini aniqlash
    buy_price_lower_bound = adnd_min_price
    buy_price_upper_bound = adnd_avg_price

    st.write(f"**Tavsiya etilgan AD&D sotib olish oralig'i:** ${buy_price_lower_bound:.2f} dan ${buy_price_upper_bound:.2f} gacha")

    if current_adnd_price <= buy_price_upper_bound:
        st.success(f"✅ Joriy narx (${current_adnd_price:.2f}) tavsiya etilgan sotib olish oralig'ida.")
        actual_adnd_buy_price = current_adnd_price
        if actual_adnd_buy_price > 0:
            num_shares = investment_amount / actual_adnd_buy_price
            st.metric("Sotib olinadigan aksiyalar soni (taxminan)", f"{num_shares:,.0f}")

            adnd_hourly_dividend_income = (investment_amount * adnd_dividend_rate_per_3_hours) / 3
            st.metric("AD&D dan soatlik dividend daromadi (taxminan)", f"${adnd_hourly_dividend_income:,.2f}")

            target_sell_price_adnd = actual_adnd_buy_price * 1.10
            st.metric("Maqsadli sotish narxi (+10% foyda bilan)", f"${target_sell_price_adnd:,.2f}")
            st.write(f"Sizning sotib olish narxingiz ${actual_adnd_buy_price:.2f} bo'lsa, kamida 10% foyda olish uchun ${target_sell_price_adnd:.2f} ga chiqqanda sotishingiz mumkin.")
            st.write(f"AD&D aksiyasining maksimal narxi ${adnd_max_price:.2f} ekanligini unutmang.")
        else:
            st.error("Sotib olish narxi nol bo'lmasligi kerak.")
    else:
        st.warning(f"⚠️ Joriy narx (${current_adnd_price:.2f}) tavsiya etilgan sotib olish oralig'idan yuqori. Sotib olish ma'lumotlari ko'rsatilmaydi, chunki bu havfli.")
        actual_adnd_buy_price = adnd_avg_price # Hisob-kitoblar uchun
        st.info(f"Hisob-kitoblar uchun ${actual_adnd_buy_price:.2f} (o'rtacha narx) asos qilib olindi.")


with col3: # Bu Exxes ustuni
    st.subheader("Exxes Kriptovalyuta Strategiyasi")
    st.write(f"**Tavsiya etilgan Exxes sotib olish oralig'i:** ${exxes_min_price:,.2f} dan ${exxes_avg_price:,.2f} gacha")

    if current_exxes_price <= exxes_avg_price:
        st.success(f"✅ Joriy narx (${current_exxes_price:,.2f}) tavsiya etilgan sotib olish oralig'ida.")
        actual_exxes_buy_price = current_exxes_price
        if actual_exxes_buy_price > 0:
            num_exxes_units = investment_amount / actual_exxes_buy_price
            st.metric("Sotib olinadigan Exxes soni (taxminan)", f"{num_exxes_units:,.2f}")

            target_sell_price_exxes = actual_exxes_buy_price * 1.10
            st.metric("Maqsadli sotish narxi (+10% foyda bilan)", f"${target_sell_price_exxes:,.2f}")
            st.write(f"Sizning sotib olish narxingiz ${actual_exxes_buy_price:,.2f} bo'lsa, kamida 10% foyda olish uchun ${target_sell_price_exxes:,.2f} ga chiqqanda sotishingiz mumkin.")
            st.write(f"Exxes Kriptovalyutasining maksimal narxi ${exxes_max_price:,.2f} ekanligini unutmang.")
        else:
            st.error("Exxes sotib olish narxi nol bo'lmasligi kerak.")
    else:
        st.warning(f"⚠️ Joriy narx (${current_exxes_price:,.2f}) tavsiya etilgan sotib olish oralig'idan yuqori. Sotib olish ma'lumotlari ko'rsatilmaydi, chunki bu havfli.")
        actual_exxes_buy_price = exxes_avg_price # Hisob-kitoblar uchun
        st.info(f"Hisob-kitoblar uchun ${actual_exxes_buy_price:,.2f} (o'rtacha narx) asos qilib olindi.")

st.markdown("---")

# --- Simulyatsiya Natijalari ---
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
    color=alt.Color('Investitsiya turi', scale=alt.Scale(range=['#FF4B4B', '#26B2FF']), title='Investitsiya turi') # Qizil va ko'k ranglar
).properties(
    title='Vaqt o\'tishi bilan investitsiya o\'sishi'
).interactive()

st.altair_chart(chart, use_container_width=True)

# Exxes potentsial foydasi faqat shu yerda ko'rsatiladi, agar joriy narx > 0 bo'lsa
total_potential_exxes_profit = 0
if current_exxes_price > 0:
    num_exxes_units_for_summary = investment_amount / current_exxes_price
    potential_profit_per_unit_summary = exxes_max_price - current_exxes_price
    total_potential_exxes_profit = num_exxes_units_for_summary * potential_profit_per_unit_summary

st.markdown(f"""
**Simulyatsiya xulosasi ({simulation_hours} soatdan keyin):**
- **AD&D (faqat dividend orqali):** ${adnd_accumulated_dividends[-1]:,.2f}
- **Ko'chmas mulk:** ${real_estate_accumulated_income[-1]:,.2f}

**Exxes Kriptovalyutasi bo'yicha qo'shimcha eslatma:**
- Yuqoridagi grafik AD&D va Ko'chmas mulkning doimiy daromadini ko'rsatadi. Exxesning daromadi esa narx o'zgarishlariga bog'liq bo'lib, bir martalik savdo siklidan olinadi.
- **Bir Exxes savdo siklidan kutilayotgan potentsial foyda (joriy narxda sotib olib, maksimal narxda sotilganda):** ${total_potential_exxes_profit:,.2f} (Sizning ${investment_amount:,.2f} sarmoyangiz uchun)

**Eslatma:** Bu simulyatsiya AD&D aksiyasining narx tebranishlarini hisobga olmaydi, faqat dividend daromadini ko'rsatadi. Haqiqiy o'yinda AD&D ning narxi ham o'zgarishi mumkin. Ko'chmas mulk esa sizning ma'lumotingizga ko'ra butunlay barqaror.
""")

st.markdown("---")

# --- Umumiy Strategiya Xulosasi ---
st.header("Umumiy Strategiya Xulosasi")
st.markdown("""
1.  **Kutish davrida (Kam risk):** Bo'sh mablag'ingizni **Ko'chmas mulkka** investitsiya qiling. Bu sizga AD&D aksiyasining narxi tushishini kutayotganingizda ham barqaror va risksiz passiv daromad olish imkonini beradi.
2.  **AD&D narxi tushganda (O'rta risk/Yuqori passiv daromad):** Narx **$22.00 dan $25.33 gacha** bo'lgan oralig'ida aksiyani sotib oling. Ushlab turganingizda yuqori dividend daromadini oling. Narx sotib olganingizdan kamida 10% yuqoriga chiqqanda soting.
3.  **Exxes Kriptovalyutasi (Yuqori risk/Yuqori potentsial foyda):**
    * Agar siz **yuqori riskni qabul qilishga tayyor bo'lsangiz** va tezroq, bir martalik katta foyda olishni istasangiz, Exxesni ko'rib chiqing.
    * Exxesni **minimal narxga yaqin** bo'lganida sotib olishni maqsad qiling ($346,050).
    * Narxi **maksimal narxga yaqin** bo'lganida soting ($422,950).
    * **Tavsiya:** Exxesga investitsiya qilishdan oldin, AD&D yoki Ko'chmas mulkdan olingan foydani ishlatishni ko'rib chiqing, chunki bu o'z sarmoyangizni xavf ostiga qo'ymaslikka yordam beradi.
4.  **Takrorlash:** Har bir investitsiya turidan foyda olgandan so'ng, mablag'ni qayta taqsimlash va strategiyani takrorlashni ko'rib chiqing.
""")
