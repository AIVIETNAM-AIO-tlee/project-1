import pandas as pd

def load_data(file):
    return pd.read_csv(file)

def calculate_average_score(data):
    return data['Điểm số'].mean().round(2)

def calculate_median_score(data):
    return data['Điểm số'].median().round(2)

def get_min_max_scores(data):
    return data['Điểm số'].min(), data['Điểm số'].max()

def get_score_distribution(data):
    tags = {'0-4': 0, '5-6': 0, '7-8': 0, '9-10': 0}
    for score in data['Điểm số']:
        if 0 <= score <= 4:
            tags['0-4'] += 1
        elif 5 <= score <= 6:
            tags['5-6'] += 1
        elif 7 <= score <= 8:
            tags['7-8'] += 1
        elif 9 <= score <= 10:
            tags['9-10'] += 1
    return tags
