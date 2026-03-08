import streamlit as st
from groq import Groq

# --- CONFIG ---
# Groq Console (https://console.groq.com/) se apni key yahan lagayein
GROQ_API_KEY = "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"

# Page Settings
st.set_page_config(page_title="Zakat AI | Hafiz Saad Qamar", page_icon="🌙")

# Function: Groq AI for Islamic Questions
def ask_groq_scholar(prompt):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an Islamic scholar assistant. Help with Zakat rules in Urdu/English. Keep answers precise and authentic."},
                {"role": "user", "content": prompt}
            ],
        )
        return completion.choices[0].message.content
    except:
        return "Groq Key error! Please check your API Key."

# --- UI HEADER ---
st.title("🌙 Simple Zakat Calculator & Guide")
st.markdown(f"#### Developed by **Hafiz Saad Qamar**")
st.divider()

# --- SIDEBAR: MANUAL RATES ---
st.sidebar.header("📊 Market Rates (Manual)")
curr = st.sidebar.selectbox("Select Currency", ["PKR", "USD", "INR", "SAR", "AED"])
gold_rate = st.sidebar.number_input(f"Gold Rate (1g 24K) in {curr}", min_value=0.0, value=22000.0)
silver_rate = st.sidebar.number_input(f"Silver Rate (1g) in {curr}", min_value=0.0, value=250.0)

# Nisab info
nisab_limit = silver_rate * 612.36
st.sidebar.info(f"**Silver Nisab:** {curr} {nisab_limit:,.2f}")

# --- MAIN CALCULATOR ---
st.subheader("📝 Calculation Details")
with st.container(border=True):
    c1, c2 = st.columns(2)
    with c1:
        cash = st.number_input("Cash & Savings", min_value=0.0, step=1000.0)
        gold_gms = st.number_input("Gold Grams", min_value=0.0, step=0.1)
    with c2:
        investments = st.number_input("Stocks/Business Goods", min_value=0.0, step=1000.0)
        silver_gms = st.number_input("Silver Grams", min_value=0.0, step=0.1)

debts = st.number_input("Minus: Debts & Liabilities", min_value=0.0, step=500.0)

# Totaling
total_assets = cash + investments + (gold_gms * gold_rate) + (silver_gms * silver_rate)
net_wealth = total_assets - debts

st.divider()

# Result Display
if net_wealth >= nisab_limit:
    zakat_payable = net_wealth * 0.025
    st.success(f"### Total Zakat Payable: {curr} {zakat_payable:,.2f}")
    st.balloons()
else:
    st.info(f"### No Zakat Due\nNet Wealth ({curr} {net_wealth:,.2f}) is below Nisab.")

# --- GROQ AI ASSISTANT ---
st.divider()
st.subheader("🤖 Zakat AI Scholar (Groq)")
st.write("Ask any question about Zakat rules (e.g., 'Is Zakat due on jewelry used daily?')")
user_q = st.text_input("Apna sawal yahan likhein:")

if st.button("Ask AI"):
    if user_q:
        with st.spinner("Hafiz Saab, AI jawab likh raha hai..."):
            answer = ask_groq_scholar(user_q)
            st.info(answer)
    else:
        st.warning("Pehle sawal toh likhein!")

# --- FOOTER ---
st.markdown("---")
st.markdown(f"<h3 style='text-align: center;'>Made by <b>Hafiz Saad Qamar</b></h3>", unsafe_allow_html=True)
