import streamlit as st
import pandas as pd
import joblib
import time

# ==========================
# PAGE CONFIGURATION
# ==========================

st.set_page_config(
    page_title="Smart Lead Scoring System",
    page_icon="📊",
    layout="wide"
)

# ==========================
# LOAD MODEL
# ==========================

model = joblib.load(
    r"D:\Data science project\Smart lead scoring System\lead_scoring_model.pkl"
)

encoders = joblib.load(
    r"D:\Data science project\Smart lead scoring System\encoders.pkl"
)

# ==========================
# CUSTOM CSS
# ==========================

st.markdown("""
<style>

.main{
    background-color:#f5f7fa;
}

h1{
    color:#0A66C2;
    text-align:center;
}

.stButton > button{
    background-color:#0A66C2;
    color:white;
    border-radius:10px;
    height:50px;
    width:100%;
    font-size:18px;
}

.stButton > button:hover{
    background-color:#004182;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("📌 Project Information")

st.sidebar.success("Model Loaded Successfully")

st.sidebar.write("""
### Technologies Used

- Python
- Pandas
- Scikit-Learn
- Random Forest
- Streamlit
- Joblib

### Algorithms Tested

✔ Logistic Regression

✔ Random Forest

✔ XGBoost
""")

# ==========================
# TITLE
# ==========================

st.title("📊 Smart Lead Scoring System")

st.markdown("""
### AI Powered Customer Conversion Prediction

This application predicts whether a lead has:

✅ High Chance of Conversion

❌ Low Chance of Conversion
""")

# ==========================
# INPUT SECTION
# ==========================

st.header("📝 Enter Lead Details")

col1, col2 = st.columns(2)

# LEFT SIDE

with col1:
    
    name = st.text_input(
    "👤 Name"
)

    company = st.text_input(
    "🏢 Company"
)

    industry = st.selectbox(
        "🏭 Industry",
        list(encoders['Industry'].classes_)
    )

    region = st.selectbox(
        "🌍 Region",
        list(encoders['Region'].classes_)
    )

    company_size = st.selectbox(
        "🏢 Company Size",
        list(encoders['Company Size'].classes_)
    )

    traffic_source = st.selectbox(
        "📈 Traffic Source",
        list(encoders['Traffic Source'].classes_)
    )

# RIGHT SIDE

with col2:

    site_visits = st.slider(
        "🌐 Site Visits",
        0,
        100,
        10
    )

    session_duration = st.slider(
        "⏱ Session Duration",
        0,
        200,
        20
    )

    emails_opened = st.slider(
        "📧 Emails Opened",
        0,
        50,
        5
    )

    demo_requested = st.selectbox(
        "🎯 Demo Requested",
        [0, 1]
    )

    days_since_first_interaction = st.number_input(
        "📅 Days Since First Interaction",
        min_value=0,
        value=5
    )

    engagement_score = st.number_input(
        "🔥 Engagement Score",
        min_value=0.0,
        value=50.0
    )

    source_impact_score = st.number_input(
        "⭐ Source Impact Score",
        min_value=0.0,
        value=10.0
    )

# ==========================
# EXTRA SETTINGS
# ==========================

st.subheader("⚙ Additional Settings")

send_email = st.checkbox(
    "📨 Send Marketing Email"
)

lead_priority = st.selectbox(
    "🚀 Lead Priority",
    ["Low", "Medium", "High"]
)

communication_channels = st.multiselect(
    "📱 Preferred Communication Channels",
    ["Email", "Phone", "WhatsApp", "LinkedIn"]
)

# ==========================
# PREDICTION BUTTON
# ==========================

if st.button("🔍 Predict Lead"):

    # Progress Bar

    progress = st.progress(0)

    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)
        
        

    # Encoding

    industry_encoded = encoders[
        "Industry"
    ].transform([industry])[0]

    region_encoded = encoders[
        "Region"
    ].transform([region])[0]

    company_size_encoded = encoders[
        "Company Size"
    ].transform([company_size])[0]

    traffic_source_encoded = encoders[
        "Traffic Source"
    ].transform([traffic_source])[0]

    # Create DataFrame

    input_data = pd.DataFrame({

        "Industry":[industry_encoded],

        "Region":[region_encoded],

        "Company Size":[company_size_encoded],

        "Traffic Source":[traffic_source_encoded],

        "Site Visits":[site_visits],

        "Session Duration":[session_duration],

        "Emails Opened":[emails_opened],

        "Demo Requested":[demo_requested],

        "Days Since First Interaction":
        [days_since_first_interaction],

        "Engagement Score":
        [engagement_score],

        "Source Impact Score":
        [source_impact_score]

    })
    
    
    
    

    # Prediction

    prediction = model.predict(
        input_data
    )

    prediction_proba = model.predict_proba(
        input_data
    )

    probability = round(
        prediction_proba[0][1] * 100,
        2
    )



    from sqlalchemy import create_engine, text

    engine = create_engine(
        "mysql+mysqlconnector://root:Tejas%401234@localhost/lead_scoring_db"
    )

    with engine.begin() as conn:

        conn.execute(
            text("""
            INSERT INTO lead_data
            (
                Name,
                Company,
                Industry,
                Region,
                `Company Size`,
                traffic_source,
                `Site Visits`,
                `Session Duration`,
                `Emails Opened`,
                `Demo Requested`,
                `Days Since First Interaction`,
                Converted
            )
            VALUES
            (
                :name,
                :company,
                :industry,
                :region,
                :company_size,
                :traffic_source,
                :site_visits,
                :session_duration,
                :emails_opened,
                :demo_requested,
                :days_since_first_interaction,
                :converted
            )
            """),
            {
                "name": name,
                "company": company,
                "industry": industry,
                "region": region,
                "company_size": company_size,
                "traffic_source": traffic_source,
                "site_visits": site_visits,
                "session_duration": session_duration,
                "emails_opened": emails_opened,
                "demo_requested": demo_requested,
                "days_since_first_interaction":
                    days_since_first_interaction,
                "converted":
                    int(prediction[0])
            }
        )






    # ==========================
    # RESULT
    # ==========================

    st.header("📊 Prediction Result")

    if prediction[0] == 1:

        st.success(
            "✅ High Chance Lead"
        )

        st.balloons()

    else:

        st.error(
            "❌ Low Chance Lead"
        )

    # Probability

    st.metric(
        "Conversion Probability",
        f"{probability}%"
    )

    # Lead Information

    st.subheader("📋 Lead Summary")

    st.write(f"Industry: {industry}")
    st.write(f"Region: {region}")
    st.write(f"Company Size: {company_size}")
    st.write(f"Traffic Source: {traffic_source}")

    # Data Table

    st.subheader("📑 Model Input Data")

    st.dataframe(input_data)

    # Marketing Info

    if send_email:

        st.info(
            "📨 Marketing Email Scheduled"
        )

    st.success(
        "Prediction Completed Successfully"
    )







# ==========================
# FOOTER
# ==========================

st.markdown("---")

st.markdown("""
### 🚀 Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-Learn
- Random Forest
- Joblib
- Machine Learning
""")

st.caption(
    "Created by Tejas Bhoyarkar | Smart Lead Scoring Project"
)


st.success("Data Saved To Database")