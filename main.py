from data_reader import read_excel
from data_processor import process_data, analyze_batch, calculate_f0
from report_generator import save_excel_report
from graph_generator import plot_temperature
from email_sender import send_email_report
from audit_logger import log_audit, status

# =========================
# CONFIGURATION
# =========================
FILE_PATH = "data/Autoclave Record Sheet.xlsx"
RECEIVER_EMAIL = "receiver_email@gmail.com"


# =========================
# MAIN WORKFLOW
# =========================
def run_pipeline():

    # Step 1: Read Data
    df = read_excel(FILE_PATH)

    # Step 2: Process Data
    results = process_data(df)

    # Step 3: Analyze Batch
    status, deviations = analyze_batch(df)

    # Step 4: Calculate F0
    f0_value = calculate_f0(df)
    f0_status = "PASS" if f0_value >= 12 else "FAIL"

    # =========================
    # OUTPUT (Console)
    # =========================
    print("\n===== AUTOCLAVE REPORT =====")
    print("Batch Status:", status)
    print("F0 Value:", round(f0_value, 2))
    print("F0 Status:", f0_status)

    if deviations:
        print("\nDeviation Report:")
        for d in deviations:
            print("-", d)

    # =========================
    # SAVE REPORT
    # =========================
    print("\nSaving Excel report...")
    save_excel_report(df, results, status, deviations, f0_value)

    # =========================
    # GRAPH
    # =========================
    plot_temperature(df)

    # =========================
    # EMAIL
    # =========================
    send_email_report(RECEIVER_EMAIL)

    print("\nProcess Completed Successfully")


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    run_pipeline()
    log_audit("Report Generated", status)