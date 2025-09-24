import streamlit as st
import requests
import datetime
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="HydroYield: Rooftop Rainwater Harvesting", 
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark background compatibility
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Main container styling */
    .main {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Header styling - bright colors for dark backgrounds */
    .main-header {
        background: linear-gradient(135deg, #00d4ff 0%, #5b73ff 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 212, 255, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
        color: #ffffff;
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.95;
        color: #e8f4ff;
    }
    
    /* Card styling - high contrast for dark backgrounds */
    .info-card {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(91, 115, 255, 0.1) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 212, 255, 0.3);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.2);
        border-left: 5px solid #00d4ff;
        color: #ffffff;
    }
    
    .success-card {
        background: linear-gradient(135deg, rgba(0, 255, 127, 0.1) 0%, rgba(46, 213, 115, 0.1) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 127, 0.3);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0, 255, 127, 0.2);
        border-left: 5px solid #00ff7f;
        color: #ffffff;
    }
    
    .warning-card {
        background: linear-gradient(135deg, rgba(255, 159, 64, 0.1) 0%, rgba(255, 206, 84, 0.1) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 159, 64, 0.3);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(255, 159, 64, 0.2);
        border-left: 5px solid #ff9f40;
        color: #ffffff;
    }
    
    .metric-container {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        text-align: center;
        margin: 1rem 0;
        border-top: 4px solid #00d4ff;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #00d4ff;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }
    
    .metric-label {
        font-size: 1rem;
        color: #ffffff;
        font-weight: 400;
    }
    
    /* Button styling - bright for dark backgrounds */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #5b73ff 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 212, 255, 0.4);
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0, 212, 255, 0.6);
        background: linear-gradient(135deg, #1ae1ff 0%, #7086ff 100%);
    }
    
    /* Section headers - bright colors for dark backgrounds */
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #00d4ff;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #00d4ff;
        display: inline-block;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00d4ff 0%, #5b73ff 100%);
    }
    
    /* Sidebar styling for dark compatibility */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(0, 0, 0, 0.3) 0%, rgba(0, 0, 0, 0.1) 100%);
        backdrop-filter: blur(10px);
    }
    
    /* Animation for cards */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animated-card {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Custom selectbox and input styling for dark backgrounds */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 2px solid rgba(0, 212, 255, 0.3);
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #00d4ff;
        box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.2);
        background: rgba(255, 255, 255, 0.15);
    }
    
    .stTextInput > div > div {
        border-radius: 8px;
        border: 2px solid rgba(0, 212, 255, 0.3);
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div:focus-within {
        border-color: #00d4ff;
        box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.2);
        background: rgba(255, 255, 255, 0.15);
    }
    
    /* Ensure text is visible on dark backgrounds */
    .stMarkdown, .stText, p, div, span {
        color: inherit;
    }
    
    /* Sidebar content styling for dark backgrounds */
    .css-1d391kg .stMarkdown {
        color: #ffffff;
    }
    
    .css-1d391kg h3 {
        color: #00d4ff !important;
        text-shadow: 0 0 8px rgba(0, 212, 255, 0.3);
    }
    
    /* DataFrame styling for dark backgrounds */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        border: 1px solid rgba(0, 212, 255, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Header section
st.markdown("""
<div class="main-header animated-card">
    <div class="main-title">🌊 RainSmart</div>
    <div class="main-subtitle">Intelligent Rooftop Rainwater Harvesting & Recharge Estimator</div>
</div>
""", unsafe_allow_html=True)

# --- Helper Function ---
def get_rainfall(city, api_key):
    """Fetch approximate annual rainfall (mm) for a city using OpenWeatherMap 5-day forecast."""
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    try:
        r = requests.get(url)
        data = r.json()
        if r.status_code != 200 or "list" not in data:
            return None
        total_rain = 0
        for entry in data["list"]:
            rain = entry.get("rain", {}).get("3h", 0)
            total_rain += rain
        # Scale up to annual estimate (very rough!): 5 days * 73 = 365 days
        annual_rain = total_rain * 73
        return round(annual_rain, 1)
    except Exception:
        return None

def create_gauge_chart(value, max_value, title):
    """Create a beautiful gauge chart"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 20}},
        gauge = {
            'axis': {'range': [None, max_value], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#667eea"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, max_value*0.5], 'color': '#f8f9fa'},
                {'range': [max_value*0.5, max_value*0.8], 'color': '#e9ecef'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value*0.9}}))
    
    fig.update_layout(
        height=300,
        font={'color': "#333", 'family': "Poppins"},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# Sidebar for additional info
with st.sidebar:
    st.markdown('<h3 style="color: #00d4ff; text-shadow: 0 0 8px rgba(0, 212, 255, 0.3);">📊 Quick Facts</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(91, 115, 255, 0.1) 100%); 
                border: 1px solid rgba(0, 212, 255, 0.3); 
                padding: 1rem; 
                border-radius: 8px; 
                color: #ffffff;
                border-left: 4px solid #00d4ff;">
        💡 <strong>Did you know?</strong> A 100 sq.m roof can harvest ~75,000 liters annually with 750mm rainfall!
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h3 style="color: #00ff7f; text-shadow: 0 0 8px rgba(0, 255, 127, 0.3); margin-top: 1.5rem;">🌍 Environmental Impact</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(0, 255, 127, 0.1) 0%, rgba(46, 213, 115, 0.1) 100%); 
                border: 1px solid rgba(0, 255, 127, 0.3); 
                padding: 1rem; 
                border-radius: 8px; 
                color: #ffffff;
                border-left: 4px solid #00ff7f;">
        🌱 Every liter harvested reduces groundwater depletion
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h3 style="color: #ff9f40; text-shadow: 0 0 8px rgba(255, 159, 64, 0.3); margin-top: 1.5rem;">📈 Benefits</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(255, 159, 64, 0.1) 0%, rgba(255, 206, 84, 0.1) 100%); 
                border: 1px solid rgba(255, 159, 64, 0.3); 
                padding: 1rem; 
                border-radius: 8px; 
                color: #ffffff;
                border-left: 4px solid #ff9f40;">
        • Reduces water bills<br>
        • Prevents flooding<br>
        • Recharges groundwater<br>
        • Sustainable water source
    </div>
    """, unsafe_allow_html=True)

# Main content in columns
col1, col2 = st.columns([2, 1])

with col1:
    # Section 1: Input details
    st.markdown('<p class="section-header">🏠 Rooftop & Location Details</p>', unsafe_allow_html=True)
    
    # Input fields in columns
    input_col1, input_col2 = st.columns(2)
    
    with input_col1:
        area = st.number_input(
            "🏘️ Rooftop Area (sq.m)", 
            min_value=1.0, 
            step=1.0, 
            value=50.0,
            help="Enter your rooftop area in square meters"
        )
    
    with input_col2:
        surface_type = st.selectbox(
            "🏗️ Rooftop Surface Type", 
            ["Concrete", "Tile", "Metal", "Other"],
            help="Different surfaces have different runoff coefficients"
        )
    
    runoff_dict = {"Concrete": 0.85, "Tile": 0.75, "Metal": 0.68, "Other": 0.55}
    runoff_coef = runoff_dict[surface_type]
    
    st.markdown(f"""
    <div class="info-card animated-card">
        <strong>📋 Surface Analysis:</strong><br>
        Selected Surface: <strong>{surface_type}</strong><br>
        Runoff Coefficient: <strong>{runoff_coef}</strong> ({int(runoff_coef*100)}% water collection efficiency)
    </div>
    """, unsafe_allow_html=True)
    
    city = st.text_input(
        "🌍 Enter City Name", 
        value="Delhi",
        placeholder="e.g., Mumbai, Bangalore, Chennai"
    )

with col2:
    # Display metrics
    if area and surface_type:
        st.markdown(f"""
        <div class="metric-container animated-card">
            <div class="metric-value">{area}</div>
            <div class="metric-label">Square Meters</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-container animated-card">
            <div class="metric-value">{int(runoff_coef*100)}%</div>
            <div class="metric-label">Collection Efficiency</div>
        </div>
        """, unsafe_allow_html=True)

# Section 2: Rainfall data
st.markdown('<p class="section-header">🌧️ Rainfall Data Collection</p>', unsafe_allow_html=True)

if city:
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🔄 Fetch Rainfall Data", help="Get real-time rainfall data for your city"):
            with st.spinner("🌐 Fetching rainfall data..."):
                try:
                    API_KEY = st.secrets["openweather"]["api_key"]
                    rainfall = get_rainfall(city, API_KEY)
                    if rainfall:
                        st.session_state["rainfall"] = rainfall
                        st.session_state["city_name"] = city
                    else:
                        st.error("Could not fetch rainfall data. Please check city name.")
                except Exception as e:
                    st.error("API key not configured. Please check your secrets configuration.")
    
    with col2:
        if "rainfall" in st.session_state and st.session_state.get("city_name") == city:
            rainfall = st.session_state["rainfall"]
            st.markdown(f"""
            <div class="success-card animated-card">
                <h4>✅ Rainfall Data Retrieved</h4>
                <p><strong>📍 Location:</strong> {city}</p>
                <p><strong>🌧️ Estimated Annual Rainfall:</strong> {rainfall} mm</p>
                <p><strong>📅 Data Source:</strong> OpenWeatherMap API</p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="warning-card animated-card">
        <h4>⚠️ City Name Required</h4>
        <p>Please enter your city name to fetch rainfall data.</p>
    </div>
    """, unsafe_allow_html=True)

# Section 3: Calculation and Results
st.markdown('<p class="section-header">⚡ Harvest Potential Calculator</p>', unsafe_allow_html=True)

if st.button("🧮 Calculate Harvest Potential", help="Estimate your rainwater harvesting potential"):
    if not city:
        st.markdown("""
        <div class="warning-card animated-card">
            <h4>⚠️ Missing Information</h4>
            <p>Please enter city name and fetch rainfall data first.</p>
        </div>
        """, unsafe_allow_html=True)
    elif "rainfall" not in st.session_state:
        st.markdown("""
        <div class="warning-card animated-card">
            <h4>⚠️ No Rainfall Data</h4>
            <p>Please fetch rainfall data first by clicking the 'Fetch Rainfall Data' button.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        rainfall = st.session_state["rainfall"]
        Q = runoff_coef * rainfall * area  # litres/year
        Q_kl = Q / 1000  # kilolitres/year
        
        # Display results in an attractive format
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-container animated-card">
                <div class="metric-value">{Q_kl:.1f}</div>
                <div class="metric-label">Kilolitres/Year</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            daily_harvest = Q_kl * 1000 / 365
            st.markdown(f"""
            <div class="metric-container animated-card">
                <div class="metric-value">{daily_harvest:.0f}</div>
                <div class="metric-label">Liters/Day</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            monthly_harvest = Q_kl * 1000 / 12
            st.markdown(f"""
            <div class="metric-container animated-card">
                <div class="metric-value">{monthly_harvest:.0f}</div>
                <div class="metric-label">Liters/Month</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Recommendations based on harvest potential
        if Q_kl > 30:
            recharge_suggestion = "🏆 Excellent! Ideal for large tank storage and groundwater recharge pit."
            suggestion_type = "success"
        elif Q_kl > 10:
            recharge_suggestion = "👍 Good potential! Try recharge pit or trench system."
            suggestion_type = "info"
        else:
            recharge_suggestion = "💡 Moderate potential. Small tank or direct garden use recommended."
            suggestion_type = "warning"
        
        if suggestion_type == "success":
            card_class = "success-card"
        else:
            card_class = "info-card"
        
        st.markdown(f"""
        <div class="{card_class} animated-card">
            <h4>💧 Harvest Analysis Complete</h4>
            <p><strong>Total Annual Potential:</strong> {Q_kl:.1f} kilolitres</p>
            <p><strong>Recommendation:</strong> {recharge_suggestion}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create visualization
        col1, col2 = st.columns(2)
        
        with col1:
            # Gauge chart for harvest potential
            gauge_fig = create_gauge_chart(Q_kl, 100, "Harvest Potential (kL/year)")
            st.plotly_chart(gauge_fig, use_container_width=True)
        
        with col2:
            # Bar chart comparing with benchmarks
            benchmark_data = {
                'Category': ['Your Harvest', 'Small Home (25kL)', 'Medium Home (50kL)', 'Large Home (75kL)'],
                'Value': [Q_kl, 25, 50, 75],
                'Color': ['#667eea', '#95a5a6', '#95a5a6', '#95a5a6']
            }
            
            fig_bar = px.bar(
                x=benchmark_data['Category'],
                y=benchmark_data['Value'],
                title="Harvest Potential Comparison",
                color=benchmark_data['Color'],
                color_discrete_map="identity"
            )
            fig_bar.update_layout(
                showlegend=False,
                font_family="Poppins",
                title_font_size=16,
                height=300
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Log the calculation
        if "log" not in st.session_state:
            st.session_state["log"] = []
        
        st.session_state["log"].append({
            "date": str(datetime.date.today()),
            "city": city,
            "area": area,
            "surface": surface_type,
            "rainfall": rainfall,
            "potential_kl": Q_kl
        })
        
        # Display calculation log
        st.markdown('<p class="section-header">📋 Your Calculation History</p>', unsafe_allow_html=True)
        
        if st.session_state["log"]:
            df_log = pd.DataFrame(st.session_state["log"])
            st.dataframe(
                df_log,
                use_container_width=True,
                height=200
            )
            
            # Federated Learning Section
            st.markdown('<p class="section-header">🤝 Community Data Sharing</p>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🌐 Share with Community", help="Upload your results to help improve recommendations"):
                    df = pd.DataFrame(st.session_state["log"])
                    csv_file = "central_server_results.csv"
                    
                    if os.path.exists(csv_file):
                        df_central = pd.read_csv(csv_file)
                        df_all = pd.concat([df_central, df], ignore_index=True)
                    else:
                        df_all = df
                    
                    df_all.to_csv(csv_file, index=False)
                    
                    st.markdown("""
                    <div class="success-card animated-card">
                        <h4>✅ Data Shared Successfully!</h4>
                        <p>Thank you for contributing to our community knowledge base.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.session_state["shared"] = True
            
            with col2:
                if st.session_state.get("shared", False):
                    if st.button("📊 View Community Insights"):
                        if os.path.exists("central_server_results.csv"):
                            df_all = pd.read_csv("central_server_results.csv")
                            
                            st.markdown("""
                            <div class="info-card animated-card">
                                <h4>🌍 Community Analytics</h4>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                avg_harvest = df_all['potential_kl'].mean()
                                st.markdown(f"""
                                <div class="metric-container">
                                    <div class="metric-value">{avg_harvest:.1f}</div>
                                    <div class="metric-label">Avg. Community Harvest (kL)</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col2:
                                total_users = len(df_all)
                                st.markdown(f"""
                                <div class="metric-container">
                                    <div class="metric-value">{total_users}</div>
                                    <div class="metric-label">Contributing Users</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col3:
                                total_potential = df_all['potential_kl'].sum()
                                st.markdown(f"""
                                <div class="metric-container">
                                    <div class="metric-value">{total_potential:.0f}</div>
                                    <div class="metric-label">Total Community Potential (kL)</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            # Community data visualization
                            fig_community = px.histogram(
                                df_all, 
                                x='potential_kl', 
                                nbins=20,
                                title="Community Harvest Distribution",
                                labels={'potential_kl': 'Harvest Potential (kL/year)', 'count': 'Number of Users'}
                            )
                            fig_community.update_layout(
                                font_family="Poppins",
                                height=400
                            )
                            st.plotly_chart(fig_community, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="info-card animated-card" style="text-align: center;">
    <h4>🎯 About HydroYield</h4>
    <p>This is a prototype for SIH presentation demonstrating federated learning concepts in environmental applications. 
    The system helps communities optimize rainwater harvesting through collaborative data sharing.</p>
    <p><strong>Technologies:</strong> Streamlit • OpenWeatherMap API • Plotly • Federated Learning Simulation</p>
    <p><em>For production deployment, implement secure aggregation protocols and backend infrastructure.</em></p>
</div>
""", unsafe_allow_html=True)
