import streamlit as st
import asyncio
import time
from main import execute_queries
from main import validate_response
from main import enrich_user_query


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


if "validate" not in st.session_state:
    st.session_state.validate = False
if "domain_info" not in st.session_state:
    st.session_state.domain_info = {}

button_placeholder = st.empty()
status_placeholder = st.empty()

# Get me the competitors of motionsociety.com

if st.button("Submit query", disabled=st.session_state.validate):
    status_placeholder.write(f"**TenX is processing your question...**")
    st.session_state.domain_info = asyncio.run(enrich_user_query(question))
    st.session_state.validate = True

if st.session_state.validate:
    status_placeholder.write("")

    if button_placeholder.button("Validate"):
        domain_info = st.session_state.domain_info
        domain_info["description"] = st.session_state.domain_info_desc

        status_placeholder.write(f"**TenX is querying the APIs...**")
        response = asyncio.run(execute_queries(question + ". " + str(domain_info), domain_info["id"]))
        status_placeholder.write("**TenX is looking for competitors...**")

        backend_data = validate_response(question + ". " + str(domain_info), response)
        status_placeholder.write("**TenX is answering your question...**")

        status_placeholder.success("Competitors found!")
        display_competitors(backend_data)

    else:
        st.session_state.domain_info_desc = st.text_area("Validate the company description", value=st.session_state.domain_info["description"])
