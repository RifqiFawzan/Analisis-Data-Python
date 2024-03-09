# Impor library yang diperlukan
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Membuat fungsi untuk memuat data
@st.cache_resource
def load_data(file_path):
    data = pd.read_csv('Dicoding/Dashboard/all_data.csv')
    return data
# def create_all_data():
#     df_customers = pd.read_csv('Dataset/olist_customers_dataset.csv')
#     df_order_items = pd.read_csv('Dataset/olist_order_items_dataset.csv')
#     df_orders = pd.read_csv('Dataset/olist_orders_dataset.csv')
#     df_order_reviews = pd.read_csv('Dataset/olist_order_reviews_dataset.csv')
#     df_products = pd.read_csv('Dataset/olist_products_dataset.csv')
#     df_payments = pd.read_csv('Dataset/olist_order_payments_dataset.csv')
#     df_product_categories = pd.read_csv('Dataset/product_category_name_translation.csv')

#     all_data = pd.merge(df_orders, df_customers, on='customer_id', how='inner')
#     all_data = pd.merge(all_data, df_order_items, on='order_id', how='inner')
#     all_data = pd.merge(all_data, df_products, on='product_id', how='inner')
#     all_data = pd.merge(all_data, df_order_reviews, on='order_id', how='left')
#     all_data = pd.merge(all_data, df_payments, on='order_id', how='left')
#     all_data = pd.merge(all_data, df_product_categories, on='product_category_name', how='left')
    
#     return all_data

all_data = create_all_data()

# Menyiapkan sidebar
st.sidebar.header("Opsi Analisis Data E-Commerce")
st.header('Dicoding E-Commerce:')
st.subheader('Preview Dataset:')
st.write(all_data.head())

# Memuat dataset
# Analisis dan Visualisasi Data

if st.sidebar.checkbox("Tampilkan Analisis Produk Terlaris dan Terendah"):
    st.subheader("Produk Terlaris dan Terendah")
    sum_df_order_items_df = all_data.groupby("product_category_name_english")["product_id"].count().reset_index()
    sum_df_order_items_df = sum_df_order_items_df.rename(columns={"product_id": "products"})
    sum_df_order_items_df = sum_df_order_items_df.sort_values(by="products", ascending=False)
    sum_df_order_items_df = sum_df_order_items_df.head(10)
    
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
    colors = ["#068DA9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(x="products", y="product_category_name_english", data=sum_df_order_items_df.head(5), palette=colors, ax=ax[0])
    ax[0].set_title("Produk paling banyak terjual", loc="center", fontsize=18)
    sns.barplot(x="products", y="product_category_name_english", data=sum_df_order_items_df.sort_values(by="products", ascending=True).head(5), palette=colors, ax=ax[1])
    ax[1].invert_xaxis()
    ax[1].set_title("Produk paling sedikit terjual", loc="center", fontsize=18)
    plt.suptitle("Produk paling banyak dan paling sedikit terjual", fontsize=20)
    st.pyplot(fig)

# Visualisasi Pengeluaran Pelanggan
  
if st.sidebar.checkbox("Tampilkan Pengeluaran Pelanggan"):
    st.subheader("Pengeluaran Pelanggan")  
    all_data['order_approved_at'] = pd.to_datetime(all_data['order_approved_at'])
    monthly_spend_df = all_data.set_index('order_approved_at').resample('M').agg({"payment_value":"sum"}).reset_index()
    monthly_spend_df['order_approved_at'] = monthly_spend_df['order_approved_at'].dt.strftime('%B %Y')
    
    plt.figure(figsize=(10, 5))
    plt.plot(monthly_spend_df["order_approved_at"], monthly_spend_df["payment_value"], marker='o', linewidth=2, color="#068DA9")
    plt.title("Total Pengeluaran Pelanggan per Bulan", loc="center", fontsize=20)
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.xlabel("Bulan", fontsize=12)
    plt.ylabel("Total Pengeluaran", fontsize=12)
    st.pyplot(plt)

# Analisis Tingkat Kepuasan Pelanggan

if st.sidebar.checkbox("Tampilkan Analisis Kepuasan Pelanggan"):
    st.subheader("Tingkat Kepuasan Pelanggan")
    review_scores = all_data['review_score'].value_counts().sort_values(ascending=False)
    most_common_score = review_scores.idxmax()
    sns.set(style="darkgrid")
    plt.figure(figsize=(10, 5))
    sns.barplot(x=review_scores.index, y=review_scores.values, order=review_scores.index, palette=["#068DA9" if score == most_common_score else "#D3D3D3" for score in review_scores.index])
    plt.title("Tingkat Kepuasan Pelanggan", fontsize=15)
    plt.xlabel("Rating")
    plt.ylabel("Count")
    plt.xticks(fontsize=12)
    st.pyplot(plt)
