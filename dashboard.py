import sys
import streamlit as st
import pandas as pd
import os
import json
import uuid
from datetime import datetime

# ================= PATH SETUP =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# ================= IMPORT MODULES =================
from src.data_reader import read_excel
from src.data_processor import analyze_batch, get_temperature_columns
from src.graph_generator import plot_temperature
from src.report_generator import save_excel_report
from src.email_sender import send_email_report
from src.pdf_generator import generate_pdf_report
from src.audit_logger import log_audit

# ================= CONFIG =================
st.set_page_config(page_title="Autoclave Dashboard", layout="wide")

# ================= LOAD USERS =================
def load_users():
    file_path = os.path.join(BASE_DIR, "users.json")
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as f:
        return json.load(f)

users = load_users()

# ================= LOGIN =================
def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🔐 Login")

        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            if users.get(u) == p:
                st.session_state.logged_in = True
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.stop()

login()

# ================= HEADER =================
col1, col2 = st.columns([8,1])

with col1:
    st.title("Autoclave Validation Dashboard")

with col2:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ================= MODE =================
mode = st.selectbox("Select Mode", ["validation", "routine"])

# ================= FILE UPLOAD =================
uploaded_file = st.file_uploader("Upload Autoclave Excel File", type=["xlsx"])

if uploaded_file:

    os.makedirs("output", exist_ok=True)

    temp_path = os.path.join("output", f"temp_{uuid.uuid4().hex}.xlsx")

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # ================= READ DATA =================
    df = read_excel(temp_path)
    df.columns = df.columns.str.lower()

    # ================= PROCESS DATA =================
    result = analyze_batch(df)

    f0_value = result["f0_value"]
    f0_status = result["f0_status"]
    status = result["final_status"]
    deviations = result["deviations"]

    report_id = f"RPT-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # ================= KPI =================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Batch Status")
        if status == "PASS":
            st.success(status)
        else:
            st.error(status)

    with col2:
        st.subheader("F0 Value")
        if f0_status == "PASS":
            st.success(f0_value)
        else:
            st.error(f0_value)

    with col3:
        st.subheader("Deviations")
        st.warning(len(deviations))

    # ================= SUMMARY =================
    st.subheader("Summary")

    st.json({
        "F0 Value": f0_value,
        "F0 Status": f0_status,
        "Final Status": status,
        "Total Deviations": len(deviations)
    })

    # ================= GRAPH =================
    st.subheader("Temperature Profile")

    fig = plot_temperature(df)
    st.pyplot(fig)

    st.info(f"Detected {len(get_temperature_columns(df))} temperature channels")

    # ================= DEVIATIONS =================
    if deviations:
        st.subheader("⚠ Deviations")
        for d in deviations:
            st.write(f"- {d}")

    # ================= ACTIONS =================
    st.subheader("Actions")

    col1, col2, col3 = st.columns(3)

    # -------- Excel --------
    with col1:
        if st.button("Generate Excel Report"):
            save_excel_report(df, result, status, deviations, f0_value)
            log_audit("Excel Generated", status)
            st.success("Excel Report Generated")

    # -------- PDF --------
    with col2:
        if st.button("Generate PDF Report"):

            report_id = uuid.uuid4().hex[:8]

            pdf_path = generate_pdf_report(
                df=df,
                status=status,
                f0_value=f0_value,
                deviations=deviations,
                report_id=report_id,
                mode=mode
            )

            log_audit("PDF Generated", status)

            if os.path.exists(pdf_path):
                st.success("PDF Generated Successfully")

                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="Download PDF",
                        data=f,
                        file_name=f"{report_id}.pdf",
                        mime="application/pdf"
                    )
            else:
                st.error("PDF not found")

    # -------- EMAIL --------
    with col3:
        if st.button("Send Email Report"):

            send_email_report(
                "receiver_email@gmail.com",
                status,
                f0_value,
                deviations,
                report_id
            )

            log_audit("Email Sent", status)

            st.success("Email Sent Successfully")