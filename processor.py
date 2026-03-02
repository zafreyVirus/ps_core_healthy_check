import pandas as pd


class DataProcessor:

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        """Load Huawei U2020 CSV properly (skip metadata lines)"""

        # Find the line number where actual header starts
        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        header_line_index = None
        for i, line in enumerate(lines):
            if line.startswith('"Start Time"'):
                header_line_index = i
                break

        if header_line_index is None:
            raise Exception("Could not find data header in CSV file.")

        # Now read CSV starting from header line
        self.df = pd.read_csv(
            self.file_path,
            skiprows=header_line_index,
            engine='python'
        )

        # Convert Start Time to datetime
        self.df['Start Time'] = pd.to_datetime(self.df['Start Time'])

        return self.df

    def filter_by_date(self, start_date, end_date):
        """Filter dataframe by selected date range"""
        mask = (
            (self.df['Start Time'] >= pd.to_datetime(start_date)) &
            (self.df['Start Time'] <= pd.to_datetime(end_date))
        )
        self.df = self.df.loc[mask]
        return self.df

    def pivot_kpi(self, column_name):
        """
        Pivot data so LMB and LLG become columns
        """
        pivot_df = self.df.pivot(
            index='Start Time',
            columns='NE Name',
            values=column_name
        )

        pivot_df = pivot_df.sort_index()

        return pivot_df

    def calculate_summary(self, column_name):
        """
        Calculate max, min, avg and corresponding timestamps
        """
        summary = {}

        for node in self.df['NE Name'].unique():
            node_df = self.df[self.df['NE Name'] == node]

            max_value = node_df[column_name].max()
            min_value = node_df[column_name].min()
            avg_value = node_df[column_name].mean()

            max_time = node_df.loc[node_df[column_name].idxmax()]['Start Time']
            min_time = node_df.loc[node_df[column_name].idxmin()]['Start Time']

            summary[node] = {
                "max_value": max_value,
                "max_time": max_time,
                "min_value": min_value,
                "min_time": min_time,
                "avg_value": avg_value
            }

        return summary