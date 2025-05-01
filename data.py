import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cache data loading/generation for performance
@st.cache_data
def load_data():
    np.random.seed(42)
    countries = ['Germany', 'Romania', 'Tunisia', 'Latvia', 'Albania']
    location_types = ['Urban', 'Rural']
    age_groups = ['13-17', '18-24', '25-35']
    interests = ['Tech', 'Sports', 'Arts', 'Social Causes', 'Gaming']
    engagement_rating = [1, 2, 3, 4, 5]

    n_samples = 300  # total per country
    data = {
        'Country': np.random.choice(countries, n_samples * len(countries)),
        'AgeGroup': np.random.choice(age_groups, n_samples * len(countries)),
        'LocationType': np.random.choice(location_types, n_samples * len(countries)),
        'TopInterest': np.random.choice(interests, n_samples * len(countries)),
        'CurrentPlatformParticipation': np.random.choice(['Yes', 'No'], n_samples * len(countries)),
        'WillingnessToJoinNewPlatform': np.random.choice(engagement_rating, n_samples * len(countries))
    }
    return pd.DataFrame(data)

# Load the survey data
df = load_data()

# Sidebar filters
st.sidebar.title("Filters")
country_filter = st.sidebar.multiselect(
    "Select Countries", options=sorted(df['Country'].unique()), default=sorted(df['Country'].unique())
)
age_filter = st.sidebar.multiselect(
    "Select Age Groups", options=sorted(df['AgeGroup'].unique()), default=sorted(df['AgeGroup'].unique())
)

df_filtered = df[
    (df['Country'].isin(country_filter)) &
    (df['AgeGroup'].isin(age_filter))
]

# Main dashboard
st.title("🌍 Youth Community Survey Dashboard")

st.markdown("---")
st.header("Survey Responses Preview")
st.dataframe(df_filtered.head(50))

st.markdown("---")
st.header("Urban vs Rural Distribution by Country")
pivot_loc = df_filtered.pivot_table(
    index='Country', columns='LocationType', aggfunc='size', fill_value=0
)
st.bar_chart(pivot_loc)

st.markdown("---")
st.header("Overall Top Interest Distribution")
interest_counts = df_filtered['TopInterest'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(
    interest_counts.values,
    labels=interest_counts.index,
    autopct='%1.1f%%',
    startangle=90
)
ax1.axis('equal')
st.pyplot(fig1)

st.markdown("---")
st.header("Willingness to Join New Platform by Country")
fig2, ax2 = plt.subplots()
df_filtered.boxplot(
    column='WillingnessToJoinNewPlatform',
    by='Country',
    ax=ax2
)
ax2.set_ylabel("Willingness Rating (1-5)")
st.pyplot(fig2)

st.markdown("---")
st.write("""
**Instructions:** Save this file as `streamlit_dashboard.py` and run:
```
# Install dependencies if needed
pip install streamlit pandas matplotlib

# Run the app
streamlit run streamlit_dashboard.py
```
""")
