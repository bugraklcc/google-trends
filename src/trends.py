import time
import pandas as pd
from pytrends.request import TrendReq
from urllib.parse import unquote
import json


def get_google_trends_data(keyword, category, geo, timeframe, search_type):
    pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25), retries=2, backoff_factor=0.1)

    cleaned_keyword = unquote(keyword)
    pytrends.build_payload(kw_list=[cleaned_keyword], timeframe=timeframe, geo=geo)

    try:
        interest_over_time_df = pytrends.interest_over_time()

        if interest_over_time_df.empty:
            raise Exception(f"No data available for {cleaned_keyword} in the specified timeframe.")

        interest_over_time_df['Country'] = geo
        interest_over_time_df['Keyword'] = cleaned_keyword
        interest_over_time_df['Category'] = category
        interest_over_time_df['SearchType'] = search_type
        interest_over_time_df.reset_index(inplace=True)
        interest_over_time_df.rename(columns={'date': 'Date', cleaned_keyword: 'Interest'},
                                     inplace=True)

        print(interest_over_time_df.columns)
        print(interest_over_time_df.head())

        return interest_over_time_df[['Country', 'Keyword', 'Category', 'Date', 'Interest', 'SearchType']]

    except Exception as e:
        raise Exception(f"Error in get_google_trends_data: {e}")


def get_interest_for_keywords(keywords, categories, geo, timeframe, search_types):
    all_data = pd.DataFrame()

    for keyword in keywords:
        for category in categories:
            keyword_data = pd.DataFrame()
            for search_type in search_types:
                try:
                    trends_data = get_google_trends_data(keyword, category, geo, timeframe, search_type)

                    if trends_data is not None:
                        keyword_data = pd.concat([keyword_data, trends_data[['Date', 'Interest']]], axis=1)
                        print(f"{keyword} keyword, {category} category, {search_type} search type successfully added.")

                        keyword_data['Country'] = trends_data['Country'].iloc[0]
                        keyword_data['SearchType'] = trends_data['SearchType'].iloc[0]

                    else:
                        raise Exception(
                            f"No data found for {keyword} keyword, {category} category, {search_type} search type.")

                    time.sleep(90)

                except Exception as inner_exception:
                    raise Exception(
                        f"Error processing {keyword} keyword, {category} category, {search_type} search type: {inner_exception}")

            keyword_data['Keyword'] = keyword
            keyword_data['Category'] = category

            keyword_data = keyword_data[['Country', 'Date', 'Keyword', 'Category', 'SearchType', 'Interest']]

            all_data = pd.concat([all_data, keyword_data], ignore_index=True)

    return all_data

# python3.9 src/main.py