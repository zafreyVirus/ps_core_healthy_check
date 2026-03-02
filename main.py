from processor import DataProcessor

file_path = "./PS Data traffic.csv"

processor = DataProcessor(file_path)

processor.load_data()

processor.filter_by_date("2026-03-01", "2026-03-02")

pivot_data = processor.pivot_kpi("4G Data traffic VDGW(CLOUD) (MB)")

summary = processor.calculate_summary("4G Data traffic VDGW(CLOUD) (MB)")

print(pivot_data.head())
print(summary)