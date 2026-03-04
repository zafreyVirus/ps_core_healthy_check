# from processor import DataProcessor

# file_path = "./PS Data traffic.csv"

# processor = DataProcessor(file_path)

# processor.load_data()

# processor.filter_by_date("2026-03-01", "2026-03-02")

# pivot_data = processor.pivot_kpi("4G Data traffic VDGW(CLOUD) (MB)")

# summary = processor.calculate_summary("4G Data traffic VDGW(CLOUD) (MB)")

# print(pivot_data.head())
# print(summary)

# # ==============================
# # MODULE 2 – HEALTH EVALUATION
# # ==============================

# CAPACITY_MB = 20000000  # Assumed capacity per hour

# def evaluate_health(max_value, capacity):
#     utilization = (max_value / capacity) * 100
    
#     if utilization < 70:
#         status = "HEALTHY"
#     elif utilization <= 85:
#         status = "WARNING"
#     else:
#         status = "CRITICAL"
        
#     return round(utilization, 2), status


# health_report = {}

# for ne, stats in results.items():
#     utilization, status = evaluate_health(stats['max_value'], CAPACITY_MB)
    
#     health_report[ne] = {
#         "Peak Traffic (MB)": float(stats['max_value']),
#         "Peak Time": stats['max_time'],
#         "Utilization %": utilization,
#         "Health Status": status
#     }

# print("\n=== HEALTH REPORT ===")
# for ne, report in health_report.items():
#     print(f"\nNE: {ne}")
#     for k, v in report.items():
#         print(f"{k}: {v}")


from processor import DataProcessor

# ==============================
# MODULE 1 – DATA PROCESSING
# ==============================

file_path = "./PS Data traffic.csv"

processor = DataProcessor(file_path)

processor.load_data()

processor.filter_by_date("2026-03-01", "2026-03-02")

pivot_data = processor.pivot_kpi("4G Data traffic VDGW(CLOUD) (MB)")

summary = processor.calculate_summary("4G Data traffic VDGW(CLOUD) (MB)")

print(pivot_data.head())
print(summary)


# ==============================
# MODULE 2 – HEALTH EVALUATION
# ==============================

CAPACITY_MB = 20000000  # Assumed capacity per hour


def evaluate_health(max_value, capacity):
    utilization = (max_value / capacity) * 100

    if utilization < 70:
        status = "HEALTHY"
    elif utilization <= 85:
        status = "WARNING"
    else:
        status = "CRITICAL"

    return round(utilization, 2), status


health_report = {}

# IMPORTANT FIX → using "summary" instead of "results"
for ne, stats in summary.items():

    utilization, status = evaluate_health(stats['max_value'], CAPACITY_MB)

    health_report[ne] = {
        "Peak Traffic (MB)": float(stats['max_value']),
        "Peak Time": stats['max_time'],
        "Minimum Traffic (MB)": float(stats['min_value']),
        "Minimum Time": stats['min_time'],
        "Average Traffic (MB)": round(float(stats['avg_value']), 2),
        "Utilization %": utilization,
        "Health Status": status
    }

print("\n=== HEALTH REPORT ===")

for ne, report in health_report.items():
    print(f"\nNE: {ne}")
    for k, v in report.items():
        print(f"{k}: {v}")

# ==============================
# MODULE 3 – EMAIL REPORT
# ==============================

# from emailer import EmailReport

# SENDER_EMAIL = "frasermsusa@gmail.com"
# SENDER_PASSWORD = "ejcmrkbcpxflkwxn"
# TEST_RECIPIENT = "frasermsusa@gmail.com"

# email_report = EmailReport(SENDER_EMAIL, SENDER_PASSWORD)

# email_report.send_email(TEST_RECIPIENT, health_report)

# ==============================
# MODULE 4 – PROFESSIONAL EMAIL
# ==============================

from emailer import EmailReport

SENDER_EMAIL = "frasermsusa@gmail.com"
SENDER_PASSWORD = "ejcmrkbcpxflkwxn"

RECIPIENTS = ["frasermsusa@gmail.com"]  # can add more later

email_report = EmailReport(SENDER_EMAIL, SENDER_PASSWORD)

email_report.send_email(
    RECIPIENTS,
    health_report,
    pivot_data,
    file_path
)