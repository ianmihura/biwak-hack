import streamlit as st
import asyncio
import time
from main import main as backend


def humanize(s: str) -> str:
    if len(s):
        return s[0].upper() + s[1:]
    else:
        return ""

st.set_page_config(layout="wide")
# Application title
st.markdown(""" 
    <h1 style="color: #1f77b4;">TenX</h1> 
    <h3>The only AI productivity tool needed for VCs</h3>
    <p style="font-size: 25px;">AI-copilot to transform your questions into concrete answers.</p>
""", unsafe_allow_html=True)

# Card for features
with st.expander("How does it work?", expanded=True):
    st.markdown("""
        <div style="border: 1px solid #1f77b4; border-radius: 10px; padding: 15px; background-color: #f9f9f9; color: #000000; margin-bottom: 20px;">
            <h4 style="font-size: 18px;">Features:</h4>
            <ul style="font-size: 14px;">
                <li><strong>Simplify access to complex data:</strong> Speak in natural language, and we handle the rest.</li>
                <li><strong>APIs at your service:</strong> Take advantage of a vast library of documented APIs, ready to meet your needs.</li>
                <li><strong>Precise and tailored answers:</strong> Harness the power of our tools to achieve reliable and fast results.</li>
                <li><strong>Save time and energy:</strong> Reduce your searches and maximize your efficiency.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)


question = st.text_input("Ask a question:", placeholder="E.g., Who are Google.com competitors? - What is the typical headcount of content creators companies?")


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

    # Define the new header
    header = ["Name", "Description", "Headcount", "Stage", "Id", "Tags_v2", "Funding", "Accuracy_descr", "Accuracy"]
    # Display the table with the new header
    st.markdown("""
        <style>
            td {  min-width: 300px; }
            .table-container { width: 100%; overflow-x: auto; }
            table { width: 100%; }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="table-container ">', unsafe_allow_html=True)  # Add a container for the table
    st.table(table_data)
    st.markdown('</div>', unsafe_allow_html=True)  # Close the container



# Button to submit the question
if st.button("Submit Question", key="submit"):
    if question:
        st.write(f"**TenX is processing your question...**")

        # Simulating the thinking process
        time.sleep(2)

        st.write("**TenX is querying the APIs...**")

        # Simulate querying Harmonic with a delay
        time.sleep(2)

        st.write("**TenX is looking for competitors...**")

        # Simulate the response return from Harmonic with a delay
        time.sleep(2)

        st.write("**TenX is answering your question...**")

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
