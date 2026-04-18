from data_reader import read_excel
from data_processor import process_data, analyze_batch
from report_generator import save_excel_report
from graph_generator import plot_temperature
from email_sender import send_email_report

file_path = "data/Autoclave Record Sheet.xlsx"

# Step 1: Read
df = read_excel(file_path)

# Step 2: Process
results = process_data(df)

# Step 3: Analyze (single source of truth)
status, deviations = analyze_batch(df)

# Output
print("Batch Status:", status)

if status == "FAIL ❌":
    print("\nDeviation Report:")
    for d in deviations:
        print("-", d)

print("Saving Excel report...")

# Save report
save_excel_report(df, results, status, deviations)
plot_temperature(df)
send_email_report("receiver_email@gmail.com")                                                                                                                                                                                                                                                                                                                                                                                                                                                          