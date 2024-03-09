import pandas as pd
from src.trends import get_google_trends_data, get_interest_for_keywords
from src.plotting import plot_comparison
import json


def write_to_excel(data, file_name):
    try:
        data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')
        data.to_excel(file_name, index=False, header=True)
        print(f"Data successfully written to the Excel file: {file_name}")
    except Exception as e:
        raise Exception(f"Error writing to Excel: {e}")

def read_config():
    try:
        with open("src/config/config.json", "r", encoding="utf-8") as file:
            config_data = json.load(file)
        return config_data
    except FileNotFoundError:
        raise FileNotFoundError("Config file not found.")
def main():
    try:
        config = read_config()

        if config is not None:
            keywords = [keyword for keyword in config.get("keywords", []) if keyword in ["Vans", "Nike"]]
            categories = [category for category in config.get("categories", []) if category in ["Alışveriş"]]
            geo = config.get("geo", "TR")
            timeframe = config.get("timeframe", "today 1-m")
            search_types = [search_type for search_type in config.get("search_types", []) if search_type in ["Google Web Arama"]]

            all_data = get_interest_for_keywords(keywords, categories, geo, timeframe, search_types)

            if all_data is not None and not all_data.empty:
                excel_file_name = "src/write_data/google_trends_data_monthly_overall.xlsx"
                write_to_excel(all_data, excel_file_name)

                plot_comparison(all_data, keywords)
            else:
                raise Exception("No data to process.")
        else:
            raise Exception("Error reading config. Check error log for details.")

    except Exception as main_exception:
        print(f"An unexpected error occurred in the main script: {main_exception}")

if __name__ == "__main__":
    main()