import sys
import streamlit as st
import pandas as pd
import os
import json
import uuid
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from src.data_reader import read_excel
from data_processor import process_data, analyze_batch, calculate_f0, get_temperature_columns
from graph_generator import plot_temperature
from report_generator import save_excel_report
from email_sender import send_email_report
from pdf_generator import generate_pdf_report
from audit_logger import log_audit


# ================= CONFIG =================
st.set_page_config(page_title="Autoclave Dashboard", layout="wide")


# ================= USERS =================
def load_users():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "users.json")

    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r") as f:
        return json.load(f)


users = load_users()


# ================= LOGIN =================
def login(users):

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🔐 Login")
        st.info("Demo → Username: demo_user | Password: demo123")

        u = st.text_input("Username", key="user")
        p = st.text_input("Password", type="password", key="pass")

        if st.button("Login", key="login_btn"):
            if users.get(u) == p:
                st.session_state.logged_in = True
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.stop()


login(users)


# ================= HEADER =================
col1, col2 = st.columns([8,1])

with col1:
    st.title("🔥 Autoclave Validation Dashboard")

with col2:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()


# ================= FILE UPLOAD =================
uploaded_file = st.file_uploader("Upload Autoclave Excel File", type=["xlsx"])


if uploaded_file:

    os.makedirs("output", exist_ok=True)

    temp_path = os.path.join("output", f"temp_{uuid.uuid4().hex}.xlsx")

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # ================= PROCESS =================
    df = read_excel(temp_path)

    results = process_data(df)
    status, deviations = analyze_batch(df)
    f0_value = calculate_f0(df)

    report_id = f"RPT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"


    # ================= KPI =================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Batch Status")
        st.success(status) if status == "PASS" else st.error(status)

    with col2:
        st.subheader("F0 Value")
        st.success(round(f0_value,2)) if f0_value >= 12 else st.error(round(f0_value,2))

    with col3:
        st.subheader("Deviations")
        st.warning(len(deviations))


    # ================= SUMMARY =================
    st.subheader("📊 Summary")
    st.json(results)


    # ================= GRAPH =================
    st.subheader("📈 Temperature Profile")

    fig = plot_temperature(df)
    st.pyplot(fig)

    st.info(f"Detected {len(get_temperature_columns(df))} temperature channels")


    # ================= DEVIATIONS =================
    if deviations:
        st.subheader("⚠ Deviations")
        for d in deviations:
            st.write(f"- {d}")


    # ================= ACTIONS =================
    st.subheader("📤 Actions")

    col1, col2, col3 = st.columns(3)


    # -------- Excel --------
    with col1:
        if st.button("Generate Excel Report"):
            save_excel_report(df, results, status, deviations, f0_value)
            log_audit("Excel Generated", status)
            st.success("Excel Report Generated")


    # -------- PDF --------
    with col2:
        if st.button("Generate PDF Report"):

            pdf_path = generate_pdf_report(df, status, f0_value, deviations, report_id)

            log_audit("PDF Generated", status)

            if os.path.exists(pdf_path):
                st.success("PDF Generated")

                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "⬇ Download PDF",
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