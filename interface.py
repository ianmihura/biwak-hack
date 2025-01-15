import streamlit as st
import random

# Application title
st.markdown("""
    <h1 style="color: #1f77b4;">TenX</h1> 
    <h3>The only AI productivity tool needed for VCs</h3>
    <p>Enter a company name to analyze the competition.</p>
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
    except Exception as e:  # Handle exceptions
        print(f"An error occurred: {e}")

# Simulated backend status check
def check_backend_status():
    # Simulate backend status check (random condition here)
    return random.choice([True, False])  # Randomly returns True or False for testing

# User input for company name
company_name = st.text_input("Enter the company name:", placeholder="E.g., Google")

def display_competitors(competitors):
    """Displays the list of competitors in a structured format."""
    st.subheader("Competitors Found:")
    for competitor in competitors:
        st.write(f"- {competitor}")

# Button to analyze competitors
if st.button("Analyze Competition", key="analyze"):
    if company_name:
        st.write(f"Searching for competitors for **{company_name}**...")

        # Check if the backend is operational (simulated here)
        if check_backend_status():
            data = query_backend_simulated(company_name)

            if "error" in data:
                st.warning(data["error"])  # Display an error message if the API fails
            else:
                st.success("Competitors found!")
                display_competitors(data["competitors"])  # Use the new function to display competitors
        else:
            st.warning("The backend is currently unavailable. Displaying simulated data.")
            display_competitors(["Microsoft", "Amazon", "Apple"])  # Use the new function
    else:
        st.warning("Please enter a company name.")

# Option to view competitor details
if company_name:
    with st.expander("View Competitor Details"):
        st.write("Additional details about competitors here...")
        # You can add links, charts, etc.
