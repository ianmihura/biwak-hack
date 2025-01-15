import streamlit as st
import random
from backend import start_backend

# Application title
st.markdown("""
    <h1 style="color: #1f77b4;">TenX</h1> 
    <h3>The only AI productivity tool needed for VCs</h3>
    <p>Enter a company name to analyze the competition.</p>
""", unsafe_allow_html=True)

# User input for company name
company_name = st.text_input("Enter the company name:", placeholder="E.g., Google")

def display_competitors(competitors):
    """Displays the list of competitors in a structured format."""
    st.subheader("Competitors Found:")
    for competitor in competitors:
        with st.expander(competitor['name'], expanded=False):  # Create an expander for each competitor
            st.write(f"**Accuracy:** {competitor['accuracy']}")  # Access the 'accuracy' key
            st.write(f"**Website:** [Link]({competitor['website']})")  # Access the 'website' key
            st.write(f"**Description:** {competitor['description']}")  # Access the 'description' key
            st.write(f"**Headcount:** {competitor['headcount']}")  # Access the 'headcount' key

# Button to analyze competitors
if st.button("Analyze Competition", key="analyze"):
    if company_name:
        st.write(f"Searching for competitors for **{company_name}**...")

        # Call start_backend with the company_name
        backend_data = start_backend(company_name)  # Pass company_name as an argument
        
        if isinstance(backend_data, list):  # Check if backend_data is a list
            st.success("Competitors found!")
            display_competitors(backend_data)  # Use the backend data directly
            
        else:
            st.warning("Unexpected data format received from the backend.")
    else:
        st.warning("Please enter a company name.")
