# ============================================================
# PROJECT 2: EXPLORATORY DATA ANALYSIS (EDA)
# DecodeLabs Internship 2026
# Dataset: Cleaned E-Commerce Orders (1200 rows)
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings("ignore")

# -------------------------------------------------------
# STEP 1: Load Cleaned Dataset
# -------------------------------------------------------
print("=" * 55)
print("PROJECT 2: EXPLORATORY DATA ANALYSIS (EDA)")
print("=" * 55)

# Use cleaned dataset from Project 1 if available
try:
    df = pd.read_excel("cleaned_dataset.xlsx")
    print("\n✅ Loaded: cleaned_dataset.xlsx")
except FileNotFoundError:
    df = pd.read_excel("Dataset for Data Analytics.xlsx")
    df["CouponCode"] = df["CouponCode"].fillna("NO_COUPON")
    df["Date"] = pd.to_datetime(df["Date"])
    print("\n✅ Loaded: Dataset for Data Analytics.xlsx (with basic cleaning)")

print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")

# -------------------------------------------------------
# STEP 2: Basic Descriptive Statistics
# -------------------------------------------------------
print("\n" + "-" * 55)
print("STEP 2: DESCRIPTIVE STATISTICS")
print("-" * 55)

print("\nNumeric Column Summary:")
print(df[["Quantity", "UnitPrice", "TotalPrice", "ItemsInCart"]].describe().round(2))

print("\nKey Stats:")
print(f"  Total Revenue         : Rs {df['TotalPrice'].sum():,.2f}")
print(f"  Average Order Value   : Rs {df['TotalPrice'].mean():,.2f}")
print(f"  Median Order Value    : Rs {df['TotalPrice'].median():,.2f}")
print(f"  Highest Single Order  : Rs {df['TotalPrice'].max():,.2f}")
print(f"  Lowest Single Order   : Rs {df['TotalPrice'].min():,.2f}")
print(f"  Total Orders          : {len(df)}")
print(f"  Unique Customers      : {df['CustomerID'].nunique()}")

# -------------------------------------------------------
# STEP 3: Sales by Product
# -------------------------------------------------------
print("\n" + "-" * 55)
print("STEP 3: SALES BY PRODUCT")
print("-" * 55)

product_revenue = df.groupby("Product")["TotalPrice"].sum().sort_values(ascending=False)
product_orders  = df.groupby("Product")["OrderID"].count().sort_values(ascending=False)

print("\nRevenue by Product:")
for p, v in product_revenue.items():
    print(f"  {p:<12} : Rs {v:>12,.2f}")

print("\nOrder Count by Product:")
for p, v in product_orders.items():
    print(f"  {p:<12} : {v} orders")

# -------------------------------------------------------
# STEP 4: Order Status Distribution
# -------------------------------------------------------
print("\n" + "-" * 55)
print("STEP 4: ORDER STATUS DISTRIBUTION")
print("-" * 55)

status_counts = df["OrderStatus"].value_counts()
print("\nOrder Status Breakdown:")
for s, c in status_counts.items():
    pct = (c / len(df)) * 100
    print(f"  {s:<12} : {c:>4} orders  ({pct:.1f}%)")

# -------------------------------------------------------
# STEP 5: Payment Method Analysis
# -------------------------------------------------------
print("\n" + "-" * 55)
print("STEP 5: PAYMENT METHOD ANALYSIS")
print("-" * 55)

payment_counts = df["PaymentMethod"].value_counts()
payment_revenue = df.groupby("PaymentMethod")["TotalPrice"].sum().sort_values(ascending=False)

print("\nOrders by Payment Method:")
for p, c in payment_counts.items():
    print(f"  {p:<14} : {c} orders")

print("\nRevenue by Payment Method:")
for p, v in payment_revenue.items():
    print(f"  {p:<14} : Rs {v:,.2f}")

# -------------------------------------------------------
# STEP 6: Monthly Sales Trend
# -------------------------------------------------------
print("\n" + "-" * 55)
print("STEP 6: MONTHLY SALES TREND")
print("-" * 55)

df["YearMonth"] = df["Date"].dt.to_period("M")
monthly_sales = df.groupby("YearMonth")["TotalPrice"].sum()

print("\nMonthly Revenue (Top 10):")
for m, v in monthly_sales.sort_values(ascending=False).head(10).items():
    print(f"  {str(m):<10} : Rs {v:>12,.2f}")

# -------------------------------------------------------
# STEP 7: Outlier Detection
# -------------------------------------------------------
print("\n" + "-" * 55)
print("STEP 7: OUTLIER DETECTION (TotalPrice)")
print("-" * 55)

Q1 = df["TotalPrice"].quantile(0.25)
Q3 = df["TotalPrice"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = df[(df["TotalPrice"] < lower) | (df["TotalPrice"] > upper)]
print(f"\n  Q1           : Rs {Q1:,.2f}")
print(f"  Q3           : Rs {Q3:,.2f}")
print(f"  IQR          : Rs {IQR:,.2f}")
print(f"  Lower Fence  : Rs {lower:,.2f}")
print(f"  Upper Fence  : Rs {upper:,.2f}")
print(f"  Outliers     : {len(outliers)} rows ({(len(outliers)/len(df)*100):.1f}%)")

# -------------------------------------------------------
# STEP 8: Referral Source Analysis
# -------------------------------------------------------
print("\n" + "-" * 55)
print("STEP 8: REFERRAL SOURCE ANALYSIS")
print("-" * 55)

referral = df.groupby("ReferralSource")["TotalPrice"].agg(["count", "sum", "mean"])
referral.columns = ["Orders", "Total_Revenue", "Avg_Order"]
referral = referral.sort_values("Total_Revenue", ascending=False)
print("\nReferral Source Performance:")
print(referral.round(2).to_string())

# -------------------------------------------------------
# STEP 9: Visualizations (4 Charts saved as PNG)
# -------------------------------------------------------
print("\n" + "-" * 55)
print("STEP 9: GENERATING CHARTS...")
print("-" * 55)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("DecodeLabs — EDA Dashboard (Project 2)", fontsize=16, fontweight="bold")

# Chart 1: Revenue by Product (Bar)
ax1 = axes[0, 0]
colors1 = ["#2196F3", "#1976D2", "#1565C0", "#0D47A1", "#42A5F5", "#64B5F6", "#90CAF9"]
product_revenue.plot(kind="bar", ax=ax1, color=colors1, edgecolor="white")
ax1.set_title("Revenue by Product", fontweight="bold")
ax1.set_xlabel("Product")
ax1.set_ylabel("Total Revenue (Rs)")
ax1.tick_params(axis="x", rotation=45)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"Rs {x/1000:.0f}K"))

# Chart 2: Order Status (Pie)
ax2 = axes[0, 1]
colors2 = ["#4CAF50", "#2196F3", "#FF9800", "#F44336", "#9C27B0"]
status_counts.plot(kind="pie", ax=ax2, colors=colors2, autopct="%1.1f%%",
                   startangle=90, wedgeprops={"edgecolor": "white"})
ax2.set_title("Order Status Distribution", fontweight="bold")
ax2.set_ylabel("")

# Chart 3: Monthly Sales Trend (Line)
ax3 = axes[1, 0]
monthly_vals = monthly_sales.sort_index()
ax3.plot(range(len(monthly_vals)), monthly_vals.values, color="#2196F3",
         linewidth=2, marker="o", markersize=4)
ax3.set_title("Monthly Sales Trend", fontweight="bold")
ax3.set_xlabel("Month")
ax3.set_ylabel("Revenue (Rs)")
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"Rs {x/1000:.0f}K"))
step = max(1, len(monthly_vals) // 8)
ax3.set_xticks(range(0, len(monthly_vals), step))
ax3.set_xticklabels([str(monthly_vals.index[i]) for i in range(0, len(monthly_vals), step)],
                     rotation=45, ha="right")
ax3.grid(True, alpha=0.3)

# Chart 4: Payment Method (Horizontal Bar)
ax4 = axes[1, 1]
payment_revenue.sort_values().plot(kind="barh", ax=ax4, color="#1976D2", edgecolor="white")
ax4.set_title("Revenue by Payment Method", fontweight="bold")
ax4.set_xlabel("Total Revenue (Rs)")
ax4.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"Rs {x/1000:.0f}K"))

plt.tight_layout()
plt.savefig("eda_dashboard.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n✅ Chart saved as 'eda_dashboard.png'")

# -------------------------------------------------------
# STEP 10: Key Insights Summary
# -------------------------------------------------------
print("\n" + "=" * 55)
print("STEP 10: KEY INSIGHTS SUMMARY")
print("=" * 55)

top_product = product_revenue.idxmax()
top_status  = status_counts.idxmax()
top_payment = payment_revenue.idxmax()
top_referral = referral["Total_Revenue"].idxmax()
best_month  = monthly_sales.idxmax()

print(f"""
  1. Top Revenue Product  : {top_product} (Rs {product_revenue.max():,.2f})
  2. Most Common Status   : {top_status} ({status_counts.max()} orders)
  3. Top Payment Method   : {top_payment} (Rs {payment_revenue.max():,.2f})
  4. Best Referral Source : {top_referral}
  5. Best Sales Month     : {best_month} (Rs {monthly_sales.max():,.2f})
  6. Outliers in TotalPrice: {len(outliers)} high-value orders detected
""")

print("=" * 55)
print("PROJECT 2 COMPLETE ✅")
print("Charts saved to: eda_dashboard.png")
print("=" * 55)
