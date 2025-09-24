import streamlit as st

st.title("On-Spot Rooftop Rainwater Harvesting Assessment 🏠💧")

st.header("Enter Details")
area = st.number_input("Rooftop Area (sqm)", min_value=10.0, value=50.0)
rainfall = st.number_input("Annual Rainfall for region (mm)", min_value=0.0, value=800.0)
runoff_coefficient = st.slider("Runoff Coefficient (0-1)", min_value=0.0, max_value=1.0, value=0.8)

if st.button("Calculate Harvest Potential"):
    # Formula: Q = C * I * A
    Q = runoff_coefficient * rainfall * area  # Litres/year
    Q_kl = Q / 1000
    st.success(f"Potential Rainwater Harvest: **{Q_kl:.1f} kilolitres/year**")
    st.info("You can improve this further by fetching area from image, rainfall from API, or adding recharge suggestions!")

st.markdown("Upgrade this prototype with weather/global data and federated learning for your SIH solution!")
