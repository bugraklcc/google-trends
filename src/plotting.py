import matplotlib.pyplot as plt
import seaborn as sns


def plot_comparison(data, keywords):
    try:
        sns.set(style="whitegrid")
        plt.figure(figsize=(15, 8))
        plt.title('Google Trends Comparison')

        for keyword in keywords:
            keyword_data = data[data['Keyword'] == keyword]
            sns.lineplot(x='Date', y='Interest', label=keyword, data=keyword_data)

        plt.xlabel('Date')
        plt.ylabel('Interest')
        plt.xticks(rotation=45, ha='right')
        plt.legend()

        plt.subplots_adjust(bottom=0.2)

        plt.show()

    except Exception as e:
        raise Exception(f"Error in plot_comparison: {e}")
