import streamlit as st
import pandas as pd
from lead_gen import generate_leads
import base64

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions here
    href = f'<a href="data:file/csv;base64,{b64}" download="leads.csv">Download CSV File</a>'
    return href

st.set_page_config(page_title="AI Lead Generator", page_icon="🚀")

st.title("🚀 AI Lead Generator")
st.write("Find potential business leads in seconds!")

with st.sidebar:
    st.header("Search Parameters")
    niche = st.text_input("Niche (e.g., Plumbers, Dentists)", "Roofers")
    location = st.text_input("Location (e.g., London, New York)", "Miami")
    num_leads = st.slider("Number of leads to fetch", 5, 50, 10)

    generate_btn = st.button("Generate Leads")

if generate_btn:
    st.info(f"Searching for {niche} in {location}...")

    with st.spinner("Scraping websites..."):
        leads = generate_leads(niche, location, num_results=num_leads)

    if leads:
        df = pd.DataFrame(leads)
        st.success(f"Found {len(df)} potential leads!")

        # UI for leads
        st.dataframe(df, use_container_width=True)

        st.markdown(get_table_download_link(df), unsafe_allow_html=True)

        # Placeholder for AI Score
        st.subheader("AI Lead Qualification (Preview)")
        st.write("Coming soon: AI-powered qualification based on website content!")
    else:
        st.warning("No leads found. Try a different niche or location.")

st.divider()
st.caption("Built with Python & Streamlit")
