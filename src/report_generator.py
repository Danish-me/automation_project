import pandas as pd
import os

def save_excel_report(df, results, status, deviations, f0_value, report_id):
    """
    Generate Excel report with:
    - Summary
    - Status
    - Deviations
    - Raw Data
    """

    # Ensure output folder exists
    output_path = "output"
    os.makedirs(output_path, exist_ok=True)

    file_path = os.path.join(output_path, "report.xlsx")
    file_path = f"output/report_{report_id}.xlsx"

    # =========================
    # 📊 SUMMARY DATA
    # =========================
    summary_df = pd.DataFrame({
        "Parameter": [
            "Temperature", "Temperature", "Temperature",
            "Pressure", "Pressure", "Pressure",
            "F0"
        ],
        "Metric": [
            "Min", "Max", "Average",
            "Min", "Max", "Average",
            "Value"
        ],
        "Value": [
            results.get("temp_min"),
            results.get("temp_max"),
            results.get("temp_avg"),
            results.get("press_min"),
            results.get("press_max"),
            results.get("press_avg"),
            round(f0_value, 2)
        ]
    })

    # =========================
    # 📄 STATUS DATA
    # =========================
    remarks = (
        "Cycle completed successfully. All parameters within limits."
        if status == "PASS ✅"
        else "Cycle failed. Deviations detected. Investigation required."
    )

    status_df = pd.DataFrame({
        "Status": [status],
        "F0 Value": [round(f0_value, 2)],
        "Remarks": [remarks]
    })

    # =========================
    # ⚠️ DEVIATIONS DATA
    # =========================
    deviations_df = pd.DataFrame({
        "Deviations": deviations if deviations else ["No deviations"]
    })

    # =========================
    # 💾 WRITE TO EXCEL
    # =========================
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:

        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        status_df.to_excel(writer, sheet_name="Status", index=False)
        deviations_df.to_excel(writer, sheet_name="Deviations", index=False)
        df.to_excel(writer, sheet_name="Raw Data", index=False)

    print(f"✅ Report saved at: {file_path}")