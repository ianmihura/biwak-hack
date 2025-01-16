import streamlit as st
from backend import start_backend
import asyncio
import time
from happy import main as backend


def humanize(s: str) -> str:
    if len(s):
        return s[0].upper() + s[1:]
    else:
        return ""

# Application title
st.markdown(""" 
    <h1 style="color: #1f77b4;">TenX</h1> 
    <h3>The only AI productivity tool needed for VCs</h3>
    <p>Ask a question to analyze the competition.</p>
""", unsafe_allow_html=True)

# User input for the question
question = st.text_input("Ask a question:", placeholder="E.g., Who are Google's competitors?")


def display_competitors(competitors):
    """Displays the list of competitors in a structured table format."""
    st.subheader("Competitors Found:")

    # Prepare data for the table
    table_data = []
    for competitor in competitors:

        data = {}
        for c in competitor.keys():
            data[humanize(c)] = competitor[c]
        table_data.append(data)
    
    # Sort the table data by accuracy in descending order
    # table_data.sort(key=lambda x: x['accuracy'], reverse=True)



# Button to submit the question
if st.button("Submit Question", key="submit"):
    if question:
        st.write(f"**TenX is thinking for query...**")

        # Simulating the thinking process
        time.sleep(2)

        st.write("**Now querying Harmonic...**")

        # Simulate querying Harmonic with a delay
        time.sleep(2)

        st.write("**Harmonic return to company...**")

        # Simulate the response return from Harmonic with a delay
        time.sleep(2)

        st.write("**TenX is validating results...**")

        # Simulate the validation process with a delay
        time.sleep(2)

        # Call start_backend with the company_name
        backend_data= asyncio.run(backend(question)) # Pass company_name as an argument

        if isinstance(backend_data, list):  # Check if backend_data is a list
            st.success("Competitors found!")
            display_competitors(backend_data)  # Use the backend data directly

        else:
            st.warning("Unexpected data format received from the backend.")
    else:
        st.warning("Please enter a question.")
