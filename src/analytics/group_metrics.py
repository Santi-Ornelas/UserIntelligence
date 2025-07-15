import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from typing import Tuple


def temporal_grouping(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df['review_year'] = df['reviewTime'].dt.year
    df['review_month'] = df['reviewTime'].dt.month
    df['review_month_year'] = df['reviewTime'].dt.to_period('M').astype(str)

    agg_funcs = {
        'overall': 'mean',
        'verified': 'mean',
        'reviewLength': 'mean',
        'asin': 'count'
    }

    reviews_by_year = df.groupby('review_year').agg(agg_funcs).rename(columns={'asin': 'review_count'})
    reviews_by_month = df.groupby('review_month').agg(agg_funcs).rename(columns={'asin': 'review_count'})
    reviews_by_month_year = df.groupby('review_month_year').agg(agg_funcs).rename(columns={'asin': 'review_count'})

    print("\n📆 Global Temporal Grouping Completed:")
    print("Years:\n", reviews_by_year.head(), "\n")
    print("Months:\n", reviews_by_month.head(), "\n")
    print("Month-Year:\n", reviews_by_month_year.head(), "\n")

    return reviews_by_year, reviews_by_month, reviews_by_month_year


def plot_temporal_grouping(month_year_df: pd.DataFrame):
    print("\n📊 Generating global temporal trend plots...")
    plt.figure(figsize=(16, 12))

    plt.subplot(3, 1, 1)
    sns.lineplot(x=month_year_df.index, y=month_year_df['review_count'])
    plt.title('Total Reviews Over Time')
    plt.ylabel('Review Count')
    plt.xticks(rotation=45)

    plt.subplot(3, 1, 2)
    sns.lineplot(x=month_year_df.index, y=month_year_df['overall'])
    plt.title('Average Rating Over Time')
    plt.ylabel('Average Rating')
    plt.xticks(rotation=45)

    plt.subplot(3, 1, 3)
    sns.lineplot(x=month_year_df.index, y=month_year_df['verified'])
    plt.title('% Verified Purchases Over Time')
    plt.ylabel('% Verified')
    plt.xlabel('Month-Year')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def temporal_grouping_per_asin(df: pd.DataFrame) -> pd.DataFrame:
    df['review_month_year'] = df['reviewTime'].dt.to_period('M').astype(str)

    grouped = (
        df.groupby(['asin', 'review_month_year'])
        .agg(
            avg_rating=('overall', 'mean'),
            review_count=('overall', 'count'),
            avg_verified=('verified', 'mean'),
            avg_length=('reviewLength', 'mean')
        )
        .reset_index()
    )

    print("\n📦 Per-ASIN Temporal Grouping (month-year) Sample:")
    print(grouped.head())
    return grouped


def reviewer_segmentation(df: pd.DataFrame, divergence_threshold: float = 1.0) -> pd.DataFrame:
    product_avg = df.groupby('asin')['overall'].mean().rename('product_avg')
    df = df.join(product_avg, on='asin')

    df['rating_diff'] = df['overall'] - df['product_avg']
    reviewer_diff = df.groupby('reviewerID')['rating_diff'].mean().rename('avg_rating_diff')

    reviewer_seg = reviewer_diff.to_frame()
    reviewer_seg['classification'] = reviewer_seg['avg_rating_diff'].apply(
        lambda x: 'divergent' if abs(x) > divergence_threshold else 'aligned'
    )

    print("\n🧑‍⚖️ Reviewer Segmentation Summary:")
    print(reviewer_seg['classification'].value_counts(), "\n")
    print(reviewer_seg.head())

    return reviewer_seg.reset_index()


def plot_reviewer_segmentation(reviewer_df: pd.DataFrame):
    print("\n📊 Plotting reviewer segmentation results...")
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    sns.countplot(x='classification', data=reviewer_df)
    plt.title('Reviewer Classification')
    plt.ylabel('Number of Reviewers')

    plt.subplot(1, 2, 2)
    sns.histplot(data=reviewer_df, x='avg_rating_diff', bins=30, kde=True)
    plt.title('Avg Rating Difference per Reviewer')
    plt.xlabel('Average Rating Difference')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("📁 Loading sample data...")

    file_path = os.path.join("data", "raw", "luxury_beauty_reviews.json")
    cleaned_data = []
    with open(file_path, "r") as f:
        for i, line in enumerate(f):
            try:
                cleaned_data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"⚠️ Skipping malformed line {i}: {e}")

    df = pd.DataFrame(cleaned_data)
    print(f"✅ Cleaned and loaded {len(df)} reviews.")

    df['reviewTime'] = pd.to_datetime(df['reviewTime'], errors='coerce')
    df['reviewLength'] = df['reviewText'].apply(lambda x: len(x.split()) if isinstance(x, str) else 0)

    # Global grouping
    _, _, month_year_df = temporal_grouping(df)
    plot_temporal_grouping(month_year_df)

    # Per-ASIN grouping
    asin_temporal_df = temporal_grouping_per_asin(df)

    # Reviewer segmentation
    reviewer_df = reviewer_segmentation(df)
    plot_reviewer_segmentation(reviewer_df)