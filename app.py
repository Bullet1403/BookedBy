from flask import Flask, jsonify, request
import pandas as pd
from collections import defaultdict
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

app = Flask(__name__)

# Load and preprocess data (run once at startup)
beauty_data = pd.read_csv('Beauty_Retail_Shop_Transactions_Dataset__2024_.csv')

# Create necessary data structures
customer_product_matrix = beauty_data.pivot_table(
    index='cust_id', 
    columns='product_name', 
    values='purchase_amt', 
    aggfunc='sum', 
    fill_value=0
)
sparse_matrix = csr_matrix(customer_product_matrix)

# Initialize KNN model
model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
model_knn.fit(sparse_matrix)

# Preprocess seasonal data
beauty_data['month'] = pd.to_datetime(beauty_data['purchase_date']).dt.month
season_mapping = {12: "Winter", 1: "Winter", 2: "Winter", 
                  3: "Spring", 4: "Spring", 5: "Spring",
                  6: "Summer", 7: "Summer", 8: "Summer",
                  9: "Autumn", 10: "Autumn", 11: "Autumn"}
beauty_data['season'] = beauty_data['month'].map(season_mapping)

@app.route('/test', methods=['GET'])
def test_endpoint():
    return jsonify({"status": "success", "message": "API is working!"})

# Add to your Flask app (app.py)
@app.route('/dashboard')
def dashboard():
    return app.send_static_file('dashboard.html')

@app.route('/analysis/monthly-sales', methods=['GET'])
def get_monthly_sales():
    beauty_data['month'] = pd.to_datetime(beauty_data['purchase_date']).dt.month
    monthly_data = beauty_data.groupby('month').agg(total_sales=('purchase_amt', 'sum'))
    # Convert to a format that's easier for JavaScript to process
    result = {
        "months": monthly_data.index.tolist(),
        "sales": monthly_data.total_sales.tolist()
    }
    return jsonify(result)

@app.route('/analysis/clusters-visual', methods=['GET'])
def get_cluster_visualization():
    customer_summary = beauty_data.groupby('cust_id').agg({
        'purchase_amt': 'sum',
        'product_name': 'count'
    })
    
    scaler = StandardScaler()
    features = scaler.fit_transform(customer_summary)
    
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(features)
    
    return jsonify({
        "x": features[:,0].tolist(),
        "y": features[:,1].tolist(),
        "clusters": clusters.tolist(),
        "centroids": kmeans.cluster_centers_.tolist()
    })


@app.route('/recommend/knn/<customer_id>', methods=['GET'])
def knn_recommendations(customer_id):
    if customer_id not in customer_product_matrix.index:
        return jsonify({"error": "Customer not found"}), 404
    
    recommendations = recommend_products_knn(customer_id)
    return jsonify({
        "customer_id": customer_id,
        "recommendations": recommendations
    })

@app.route('/recommend/content-based/<customer_id>', methods=['GET'])
def content_based_recommendations(customer_id):
    if customer_id not in beauty_data['cust_id'].unique():
        return jsonify({"error": "Customer not found"}), 404
    
    recommendations = recommend_products_content_based(customer_id)
    return jsonify({
        "customer_id": customer_id,
        "recommendations": recommendations
    })

@app.route('/recommend/seasonal/<season>', methods=['GET'])
def seasonal_recommendations(season):
    valid_seasons = ["Winter", "Spring", "Summer", "Autumn"]
    if season not in valid_seasons:
        return jsonify({"error": "Invalid season"}), 400
    
    recommendations = recommend_weather_based(season)
    return jsonify({
        "season": season,
        "recommendations": recommendations
    })

@app.route('/recommend/sale', methods=['GET'])
def sale_recommendations():
    recommendations = recommend_sale_products()
    return jsonify({
        "sale_recommendations": recommendations
    })

# Add analysis endpoints
@app.route('/analysis/clusters', methods=['GET'])
def get_clusters():
    customer_summary = beauty_data.groupby('cust_id').agg({
        'purchase_amt': 'sum',
        'product_name': 'count'
    }).rename(columns={'purchase_amt': 'total_spending', 'product_name': 'total_purchases'})
    
    return jsonify({
        "customer_clusters": customer_summary.to_dict(orient='index')
    })

@app.route('/analysis/seasonal-sales', methods=['GET'])
def get_seasonal_sales():
    seasonal_data = beauty_data.groupby("season").agg(total_sales=("purchase_amt", "sum"))
    return jsonify(seasonal_data.to_dict())

@app.route('/analysis/sale-periods', methods=['GET'])
def get_sale_periods():
    sale_data = beauty_data.groupby("sale_period").agg(total_sales=("purchase_amt", "sum"))
    return jsonify(sale_data.to_dict())

# Original recommendation functions (keep implementation same)
def recommend_products_knn(customer_id, n_recommendations=3):
    if customer_id not in customer_product_matrix.index:
        return "Customer not found."
    customer_index = customer_product_matrix.index.get_loc(customer_id)
    distances, indices = model_knn.kneighbors(customer_product_matrix.iloc[customer_index, :].values.reshape(1, -1), n_neighbors=4)
    similar_customers = [customer_product_matrix.index[i] for i in indices.flatten()][1:]
    recommended_products = defaultdict(int)
    for sim_cust in similar_customers:
        top_products = beauty_data[beauty_data['cust_id'] == sim_cust]['product_name'].value_counts().head(n_recommendations)
        for product in top_products.index:
            recommended_products[product] += top_products[product]
    sorted_recommendations = sorted(recommended_products.items(), key=lambda x: x[1], reverse=True)
    return [product for product, count in sorted_recommendations[:n_recommendations]]

## "Based on Your Past Purchases" (Content-Based Filtering)
def recommend_products_content_based(customer_id, n_recommendations=3):
    if customer_id not in beauty_data['cust_id'].unique():
        return "Customer not found."
    purchased_products = beauty_data[beauty_data['cust_id'] == customer_id]['product_name'].unique()
    category = beauty_data[beauty_data['product_name'].isin(purchased_products)]['category'].mode()[0]
    similar_products = beauty_data[beauty_data['category'] == category]['product_name'].value_counts().index[:n_recommendations].tolist()
    return similar_products

def recommend_weather_based(season, n_recommendations=3):
    top_products = beauty_data[beauty_data['season'] == season]['product_name'].value_counts().head(n_recommendations).index.tolist()
    return top_products

def recommend_sale_products(n_recommendations=3):
    return beauty_data[beauty_data['sale_period'] == 'Sale']['product_name'].value_counts().index[:n_recommendations].tolist()

if __name__ == '__main__':
    app.run(debug=True,port=5000)
