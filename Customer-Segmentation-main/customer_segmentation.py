"""
=============================================================================
Customer Segmentation using K-Means Clustering Algorithm
=============================================================================
This script performs customer segmentation using K-Means clustering.
It includes data loading, preprocessing, optimal cluster selection via
the Elbow Method, clustering, visualization, and interpretation.

Author  : Customer Analytics Team
Date    : 2026-05-05
Python  : 3.8+
=============================================================================
"""

# ─── 1. Import Libraries ─────────────────────────────────────────────────────
import os
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving plots
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

# ─── 2. Configuration ────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'customers.csv')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── 3. Data Collection ──────────────────────────────────────────────────────
print("=" * 60)
print("  CUSTOMER SEGMENTATION USING K-MEANS CLUSTERING")
print("=" * 60)

print("\n Step 1: Loading Dataset...")
df = pd.read_csv(DATA_PATH)

print(f"   ✅ Dataset loaded successfully!")
print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"\n   First 5 rows:")
print(df.head().to_string(index=False))

# ─── 4. Exploratory Data Analysis ────────────────────────────────────────────
print("\n" + "─" * 60)
print(" Step 2: Exploratory Data Analysis")
print("─" * 60)

print("\n   Dataset Info:")
print(f"   Columns: {list(df.columns)}")
print(f"\n   Statistical Summary:")
print(df.describe().to_string())

print(f"\n   Missing Values:")
missing = df.isnull().sum()
print(missing.to_string())

print(f"\n   Gender Distribution:")
print(df['Gender'].value_counts().to_string())

# ─── 5. Data Preprocessing ───────────────────────────────────────────────────
print("\n" + "─" * 60)
print(" Step 3: Data Preprocessing")
print("─" * 60)

# Handle missing values (if any)
df = df.dropna()
print(f"   ✅ Missing values handled. Remaining rows: {df.shape[0]}")

# Encode Gender
le = LabelEncoder()
df['Gender_Encoded'] = le.fit_transform(df['Gender'])
print(f"   ✅ Gender encoded: Male=1, Female=0")

# ─── 6. Feature Selection ────────────────────────────────────────────────────
print("\n" + "─" * 60)
print(" Step 4: Feature Selection")
print("─" * 60)

features = ['Annual_Income', 'Spending_Score']
print(f"   Selected features: {features}")

X = df[features].values

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print(f"   ✅ Features standardized using StandardScaler")

# ─── 7. Elbow Method ─────────────────────────────────────────────────────────
print("\n" + "─" * 60)
print(" Step 5: Finding Optimal Clusters (Elbow Method)")
print("─" * 60)

wcss = []
silhouette_scores = []
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=300,
                    n_init=10, random_state=42)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)
    sil_score = silhouette_score(X_scaled, kmeans.labels_)
    silhouette_scores.append(sil_score)
    print(f"   K={k}: WCSS={kmeans.inertia_:.2f}, Silhouette Score={sil_score:.4f}")

# Plot Elbow Method
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# WCSS Plot
axes[0].plot(list(K_range), wcss, 'bo-', linewidth=2, markersize=8)
axes[0].set_xlabel('Number of Clusters (K)', fontsize=12)
axes[0].set_ylabel('WCSS (Within-Cluster Sum of Squares)', fontsize=12)
axes[0].set_title('Elbow Method - WCSS', fontsize=14, fontweight='bold')
axes[0].grid(True, alpha=0.3)

# Silhouette Score Plot
axes[1].plot(list(K_range), silhouette_scores, 'rs-', linewidth=2, markersize=8)
axes[1].set_xlabel('Number of Clusters (K)', fontsize=12)
axes[1].set_ylabel('Silhouette Score', fontsize=12)
axes[1].set_title('Silhouette Score Analysis', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'elbow_method.png'), dpi=150, bbox_inches='tight')
plt.close()
print(f"\n   ✅ Elbow plot saved to output/elbow_method.png")

# Determine optimal K
optimal_k = 5  # Based on elbow method analysis
best_sil_k = list(K_range)[np.argmax(silhouette_scores)]
print(f"\n   Best K by Silhouette Score: {best_sil_k}")
print(f"   Selected K (Elbow Method): {optimal_k}")

# ─── 8. K-Means Clustering ───────────────────────────────────────────────────
print("\n" + "─" * 60)
print(" Step 6: Applying K-Means Clustering (K={})".format(optimal_k))
print("─" * 60)

kmeans_final = KMeans(n_clusters=optimal_k, init='k-means++', max_iter=300,
                       n_init=10, random_state=42)
df['Cluster'] = kmeans_final.fit_predict(X_scaled)

# Get centroids (inverse transform to original scale)
centroids_scaled = kmeans_final.cluster_centers_
centroids_original = scaler.inverse_transform(centroids_scaled)

print(f"   ✅ Clustering complete!")
print(f"\n   Cluster Distribution:")
print(df['Cluster'].value_counts().sort_index().to_string())

# ─── 9. Cluster Analysis & Interpretation ────────────────────────────────────
print("\n" + "─" * 60)
print(" Step 7: Cluster Analysis & Interpretation")
print("─" * 60)

cluster_summary = df.groupby('Cluster').agg({
    'Age': ['mean', 'min', 'max'],
    'Annual_Income': ['mean', 'min', 'max'],
    'Spending_Score': ['mean', 'min', 'max'],
    'Purchase_Frequency': ['mean', 'min', 'max'],
    'Customer_ID': 'count'
}).round(2)

cluster_summary.columns = [
    'Avg_Age', 'Min_Age', 'Max_Age',
    'Avg_Income', 'Min_Income', 'Max_Income',
    'Avg_Spending', 'Min_Spending', 'Max_Spending',
    'Avg_Purchases', 'Min_Purchases', 'Max_Purchases',
    'Count'
]

print("\n   Cluster Summary:")
print(cluster_summary.to_string())

# Interpret clusters
cluster_labels = {}
for i in range(optimal_k):
    avg_income = cluster_summary.loc[i, 'Avg_Income']
    avg_spending = cluster_summary.loc[i, 'Avg_Spending']
    
    if avg_income > 120000 and avg_spending > 60:
        label = " Premium Customers (High Income, High Spending)"
    elif avg_income > 120000 and avg_spending <= 60:
        label = " Affluent & Careful (High Income, Low Spending)"
    elif avg_income <= 60000 and avg_spending > 60:
        label = " Enthusiastic Shoppers (Low Income, High Spending)"
    elif avg_income <= 60000 and avg_spending <= 60:
        label = " Budget Conscious (Low Income, Low Spending)"
    else:
        label = " Moderate Customers (Average Income & Spending)"
    
    cluster_labels[i] = label
    print(f"\n   Cluster {i}: {label}")
    print(f"     • Avg Income: ₹{avg_income:,.0f}")
    print(f"     • Avg Spending Score: {avg_spending:.1f}")
    print(f"     • Avg Age: {cluster_summary.loc[i, 'Avg_Age']:.1f}")
    print(f"     • Customers: {cluster_summary.loc[i, 'Count']}")

# ─── 10. Visualization ───────────────────────────────────────────────────────
print("\n" + "─" * 60)
print(" Step 8: Generating Visualizations")
print("─" * 60)

colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
          '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9']

# Plot 1: Main Cluster Scatter Plot (Income vs Spending Score)
fig, ax = plt.subplots(figsize=(12, 8))
for i in range(optimal_k):
    cluster_data = df[df['Cluster'] == i]
    ax.scatter(cluster_data['Annual_Income'], cluster_data['Spending_Score'],
               c=colors[i], s=100, alpha=0.7, edgecolors='white',
               linewidth=1.5, label=f'Cluster {i}')

# Plot centroids
ax.scatter(centroids_original[:, 0], centroids_original[:, 1],
           c='black', s=300, marker='X', edgecolors='gold',
           linewidth=2, label='Centroids', zorder=5)

ax.set_xlabel('Annual Income (₹)', fontsize=14, fontweight='bold')
ax.set_ylabel('Spending Score (1-100)', fontsize=14, fontweight='bold')
ax.set_title('Customer Segmentation\nAnnual Income vs Spending Score',
             fontsize=16, fontweight='bold')
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'cluster_scatter.png'), dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ Cluster scatter plot saved")

# Plot 2: Cluster Distribution (Bar Chart)
fig, ax = plt.subplots(figsize=(10, 6))
cluster_counts = df['Cluster'].value_counts().sort_index()
bars = ax.bar(cluster_counts.index, cluster_counts.values,
              color=colors[:optimal_k], edgecolor='white', linewidth=2)
for bar, count in zip(bars, cluster_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
            str(count), ha='center', va='bottom', fontweight='bold', fontsize=13)
ax.set_xlabel('Cluster', fontsize=14, fontweight='bold')
ax.set_ylabel('Number of Customers', fontsize=14, fontweight='bold')
ax.set_title('Customer Distribution Across Clusters', fontsize=16, fontweight='bold')
ax.set_xticks(range(optimal_k))
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'cluster_distribution.png'), dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ Cluster distribution chart saved")

# Plot 3: Age Distribution by Cluster
fig, ax = plt.subplots(figsize=(10, 6))
for i in range(optimal_k):
    cluster_data = df[df['Cluster'] == i]
    ax.hist(cluster_data['Age'], bins=15, alpha=0.5, color=colors[i],
            label=f'Cluster {i}', edgecolor='white')
ax.set_xlabel('Age', fontsize=14, fontweight='bold')
ax.set_ylabel('Frequency', fontsize=14, fontweight='bold')
ax.set_title('Age Distribution by Cluster', fontsize=16, fontweight='bold')
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'age_distribution.png'), dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ Age distribution chart saved")

# Plot 4: Gender Distribution by Cluster
fig, ax = plt.subplots(figsize=(10, 6))
gender_cluster = df.groupby(['Cluster', 'Gender']).size().unstack(fill_value=0)
gender_cluster.plot(kind='bar', ax=ax, color=['#FF6B6B', '#4ECDC4'],
                     edgecolor='white', linewidth=1.5)
ax.set_xlabel('Cluster', fontsize=14, fontweight='bold')
ax.set_ylabel('Count', fontsize=14, fontweight='bold')
ax.set_title('Gender Distribution by Cluster', fontsize=16, fontweight='bold')
ax.legend(fontsize=11)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'gender_distribution.png'), dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ Gender distribution chart saved")

# Plot 5: Boxplots for Key Features by Cluster
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
features_to_plot = ['Annual_Income', 'Spending_Score', 'Age']
titles = ['Annual Income by Cluster', 'Spending Score by Cluster', 'Age by Cluster']

for idx, (feature, title) in enumerate(zip(features_to_plot, titles)):
    bp = df.boxplot(column=feature, by='Cluster', ax=axes[idx],
                     patch_artist=True, return_type='dict')
    for patch_idx, patch in enumerate(bp[feature]['boxes']):
        patch.set_facecolor(colors[patch_idx % len(colors)])
        patch.set_alpha(0.7)
    axes[idx].set_title(title, fontsize=14, fontweight='bold')
    axes[idx].set_xlabel('Cluster', fontsize=12)
    axes[idx].set_ylabel(feature, fontsize=12)

plt.suptitle('')  # Remove auto-generated title
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'boxplots.png'), dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ Boxplots saved")

# Plot 6: Heatmap of Cluster Means
fig, ax = plt.subplots(figsize=(10, 6))
cluster_means = df.groupby('Cluster')[['Age', 'Annual_Income', 'Spending_Score',
                                         'Purchase_Frequency']].mean()
sns.heatmap(cluster_means.T, annot=True, fmt='.1f', cmap='YlOrRd',
            linewidths=2, linecolor='white', ax=ax)
ax.set_title('Cluster Feature Means (Heatmap)', fontsize=16, fontweight='bold')
ax.set_xlabel('Cluster', fontsize=14)
ax.set_ylabel('Feature', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'heatmap.png'), dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ Heatmap saved")

# Plot 7: 3D Scatter (Income, Spending, Age)
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
for i in range(optimal_k):
    cluster_data = df[df['Cluster'] == i]
    ax.scatter(cluster_data['Annual_Income'], cluster_data['Spending_Score'],
               cluster_data['Age'], c=colors[i], s=60, alpha=0.7,
               label=f'Cluster {i}')
ax.set_xlabel('Annual Income (₹)')
ax.set_ylabel('Spending Score')
ax.set_zlabel('Age')
ax.set_title('3D Customer Segmentation', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'scatter_3d.png'), dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ 3D scatter plot saved")

# ─── 11. Export Results ───────────────────────────────────────────────────────
print("\n" + "─" * 60)
print(" Step 9: Exporting Results")
print("─" * 60)

# Save clustered data
df.to_csv(os.path.join(OUTPUT_DIR, 'clustered_customers.csv'), index=False)
print("   ✅ Clustered data saved to output/clustered_customers.csv")

# Save cluster summary
cluster_summary.to_csv(os.path.join(OUTPUT_DIR, 'cluster_summary.csv'))
print("   ✅ Cluster summary saved to output/cluster_summary.csv")

# Save results as JSON for dashboard
dashboard_data = {
    "total_customers": int(df.shape[0]),
    "num_clusters": optimal_k,
    "features_used": features,
    "silhouette_score": float(silhouette_score(X_scaled, df['Cluster'])),
    "elbow_data": {
        "k_values": list(range(2, 11)),
        "wcss": [round(w, 2) for w in wcss],
        "silhouette_scores": [round(s, 4) for s in silhouette_scores]
    },
    "clusters": [],
    "scatter_data": []
}

for i in range(optimal_k):
    cluster_data = df[df['Cluster'] == i]
    cluster_info = {
        "id": i,
        "label": cluster_labels[i],
        "count": int(cluster_data.shape[0]),
        "percentage": round(cluster_data.shape[0] / df.shape[0] * 100, 1),
        "avg_age": round(cluster_data['Age'].mean(), 1),
        "avg_income": round(cluster_data['Annual_Income'].mean(), 0),
        "avg_spending": round(cluster_data['Spending_Score'].mean(), 1),
        "avg_purchases": round(cluster_data['Purchase_Frequency'].mean(), 1),
        "centroid": {
            "income": round(float(centroids_original[i][0]), 0),
            "spending": round(float(centroids_original[i][1]), 1)
        },
        "gender_split": {
            "male": int(cluster_data[cluster_data['Gender'] == 'Male'].shape[0]),
            "female": int(cluster_data[cluster_data['Gender'] == 'Female'].shape[0])
        }
    }
    dashboard_data["clusters"].append(cluster_info)

# Scatter data for dashboard
for _, row in df.iterrows():
    dashboard_data["scatter_data"].append({
        "id": int(row['Customer_ID']),
        "age": int(row['Age']),
        "gender": row['Gender'],
        "income": int(row['Annual_Income']),
        "spending": int(row['Spending_Score']),
        "purchases": int(row['Purchase_Frequency']),
        "cluster": int(row['Cluster'])
    })

with open(os.path.join(OUTPUT_DIR, 'dashboard_data.json'), 'w') as f:
    json.dump(dashboard_data, f, indent=2)
print("   ✅ Dashboard data saved to output/dashboard_data.json")

# ─── 12. Final Summary ───────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  ✅ CUSTOMER SEGMENTATION COMPLETE!")
print("=" * 60)
print(f"\n  Total Customers Analyzed: {df.shape[0]}")
print(f"  Number of Clusters: {optimal_k}")
print(f"  Silhouette Score: {silhouette_score(X_scaled, df['Cluster']):.4f}")
print(f"\n  Output Files:")
print(f"     • output/elbow_method.png")
print(f"     • output/cluster_scatter.png")
print(f"     • output/cluster_distribution.png")
print(f"     • output/age_distribution.png")
print(f"     • output/gender_distribution.png")
print(f"     • output/boxplots.png")
print(f"     • output/heatmap.png")
print(f"     • output/scatter_3d.png")
print(f"     • output/clustered_customers.csv")
print(f"     • output/cluster_summary.csv")
print(f"     • output/dashboard_data.json")
print(f"\n  Open dashboard/index.html to view interactive dashboard!")
print("=" * 60)
