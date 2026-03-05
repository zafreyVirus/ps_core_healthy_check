from processor import DataProcessor
from emailer import EmailReport
from excel_report import ExcelReport


file_path = "./PS Data traffic LMB.csv"

processor = DataProcessor(file_path)

processor.load_data()

print(processor.df.columns)

processor.filter_by_date("2026-03-01", "2026-03-05")

pivot_data = processor.pivot_kpi("4G Data traffic VDGW(CLOUD) (MB)")

summary = processor.calculate_summary("4G Data traffic VDGW(CLOUD) (MB)")

print(pivot_data.head())
print(summary)


CAPACITY_MB = 20000000


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


# ===== GENERATE CHARTS =====

processor.plot_kpi(
    "PGW-U 2/3G Gi traffic in MB (MB)",
    "chart_gi.png"
)

processor.plot_kpi(
    "4G Data traffic VDGW(CLOUD) (MB)",
    "chart_4g.png"
)

processor.plot_kpi(
    "PGW-U 2/3G Gn peak throughput in MB/s (MB/s)",
    "chart_gn.png"
)

processor.plot_kpi(
    "User Plane SGi downlink user traffic peak throughput in MB/s (MB/s) (MB/s)",
    "chart_sgi.png"
)


# ===== SEND EMAIL =====

SENDER_EMAIL = "frasermsusa@gmail.com"
SENDER_PASSWORD = "ejcmrkbcpxflkwxn"

RECIPIENTS = ["frasermsusa@gmail.com"]

email_report = EmailReport(SENDER_EMAIL, SENDER_PASSWORD)

email_report.send_email(
    RECIPIENTS,
    health_report,
    processor,
    file_path
)


# ===== CREATE EXCEL REPORT =====

excel = ExcelReport("Fraser Msusa")

chart_paths = [
    "chart_gi.png",
    "chart_4g.png",
    "chart_gn.png",
    "chart_sgi.png"
]

excel.create_report(
    chart_paths,
    health_report,
    "PS_Core_Health_Report.xlsx"
)