import datetime

def log_audit(action, status):

    with open("output/audit_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} | {action} | {status}\n")