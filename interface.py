import streamlit as st
import random

# Application title
st.markdown("""
    <h1 style="color: #1f77b4;">TenX</h1> <h3>The only AI productivity tool needed for VCs</h3>
""", unsafe_allow_html=True)

# Simulated function to fetch competitors
def query_backend_simulated(company_name):
    try:
        # Simulates calling a backend to fetch competitors
        # Here, we generate mock competitors based on the company name
        competitors = [
            f"{company_name} Competitor A",
            f"{company_name} Competitor B",
            f"{company_name} Competitor C"
        ]
        return {"competitors": competitors}
    except Exception as e:
        # Return an error message in case of an exception
        return {"error": f"Error fetching competitors: {str(e)}"}

# Simulated backend status check
def check_backend_status():
    # Simulate backend status check (random condition here)
    return random.choice([True, False])  # Randomly returns True or False for testing

# User input for company name
company_name = st.text_input("Enter your instruction:", placeholder="E.g., Google")

# Button to analyze competitors
if st.button("Run"):
    if company_name:
        st.write(f"Searching for competitors for **{company_name}**...")

        # Check if the backend is operational (simulated here)
        if check_backend_status():
            # Simulate calling the backend to fetch competitors
            data = query_backend_simulated(company_name)

            if "error" in data:
                st.warning(data["error"])  # Display an error message if the API fails
            else:
                st.success("Competitors found!")
                for competitor in data["competitors"]:
                    st.write(f"- {competitor}")
        else:
            st.warning("The backend is currently unavailable. Displaying simulated data.")
            # Display simulated data if the backend is unavailable
            st.write("- Competitor 1: Microsoft")
            st.write("- Competitor 2: Amazon")
            st.write("- Competitor 3: Apple")
    else:
        st.warning("Please enter a company name.")

# Option to view competitor details
if company_name:
    with st.expander("View Competitor Details"):
        st.write("Additional details about competitors here...")
        # You can add links, charts, etc.
