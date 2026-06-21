import streamlit as st
import pandas as pd
import os
from agents import AgenticOrchestrator

# Configure layout to be wide-screen and clean
st.set_page_config(page_title="Agentic AI Pipeline Dashboard", layout="wide")

st.title("🤖 Agentic AI-Driven Automated Data Pipeline System")
st.caption("Department of Computer Science and Engineering | Final Year Project")
st.markdown("---")

# Sidebar Configuration for File Uploads
st.sidebar.header("📁 Control Panel")
uploaded_file = st.sidebar.file_uploader("Upload a Dataset (CSV or JSON)", type=["csv", "json"])

# Create a clear two-column layout for the dashboard
col1, col2 = st.columns([1, 1])

if uploaded_file is not None:
    # Save the file temporarily into our workspace directory
    temp_path = os.path.join(uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Left Column: Raw Preview
    with col1:
        st.subheader("📊 Source Data Preview")
        if uploaded_file.name.endswith('.csv'):
            preview_df = pd.read_csv(temp_path)
        else:
            preview_df = pd.read_json(temp_path)
        st.dataframe(preview_df.head(10), use_container_width=True)

    # Sidebar button to execute the pipeline logic
    if st.sidebar.button("Launch Autonomous Agents"):
        orchestrator = AgenticOrchestrator()
        
        with st.spinner("Agents processing data..."):
            final_result, execution_logs = orchestrator.execute_pipeline(temp_path)
            
        # Right Column: Transparent Activity Logs
        with col2:
            st.subheader("📜 Transparent Auditing Layer Logs")
            for log in execution_logs:
                if "❌" in log:
                    st.error(log)
                elif "⚠️" in log:
                    st.warning(log)
                elif "✅" in log:
                    st.success(log)
                else:
                    st.info(log)
                    
        # Display Final Output at the bottom if successful
        if final_result is not None:
            st.markdown("---")
            st.subheader("🎯 Final Standardized Clean Output")
            st.dataframe(final_result, use_container_width=True)
            
            # Provide an instant download button for the jury presentation
            output_csv = final_result.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Processed Dataset", data=output_csv, file_name="pipeline_output.csv", mime="text/csv")
            
    # Remove the temporary file from our directory workspace safely
    if os.path.exists(temp_path):
        os.remove(temp_path)
else:
    st.info("💡 Drop a CSV or JSON file into the sidebar control panel to wake up your AI Agents.")