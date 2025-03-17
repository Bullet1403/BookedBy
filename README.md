# **Beauty Retail Shop Transaction Analysis and Recommendation System**

This project analyzes beauty retail shop transaction data to derive insights and build recommendation systems.

---

## **Project Overview**

The project performs the following tasks:

- **Data Analysis**: Basic exploration, identification of top-selling products and categories, and visualization of trends.
- **Customer Segmentation**: Clustering customers based on their purchasing behavior.
- **Seasonal Trend Analysis**: Understanding sales trends across different seasons.
- **Price Sensitivity Analysis**: Examining sales variations during sale and non-sale periods.
- **Weather-Based Analysis**: Grouping products based on weather conditions.
- **Recommendation Systems**: Implementing various recommendation methods, including:
  - **Collaborative Filtering**: "Customers Also Bought This"
  - **Content-Based Filtering**: "Based on Your Past Purchases"
  - **Context-Aware Recommendations**: "Based on the Weather"
  - **Sale-Based Recommendations**: "Steals for You"

---

## **Project Files**

- `Beauty_Retail_Shop_Transactions_Dataset__2024_.csv` - Dataset containing beauty retail shop transaction data.
- `project.ipynb` - Jupyter Notebook for data analysis and recommendation system implementation.
- `requirements.txt` - List of required Python libraries.
- `README.md` - This file, providing an overview of the project.

---

## **Installation & Usage**

### **Requirements**

This project requires **Python 3.8+**. Install the following dependencies:

```plaintext
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
scikit-learn>=1.0.0
sentence-transformers>=2.2.0
scipy>=1.7.0
```

Install dependencies using:

```sh
pip install -r requirements.txt
```

### **Running the Python Notebook**

1. Clone the repository.
2. Install the required libraries.
3. Place the `Beauty_Retail_Shop_Transactions_Dataset__2024_.csv` file in the same directory as `project.ipynb`.
4. Open the Jupyter Notebook and run the cells.

## **Beauty Retail Dashboard**

## How to Run

### Install Dependencies:
```bash
pip install flask pandas scikit-learn scipy StandardScaler
```

### Project Structure:
``` bash
beauty-dashboard/
├── app.py
├── static/
│   └── dashboard.html
└── Beauty_Retail_Shop_Transactions_Dataset__2024_.csv
```

### Start the Server:
```bash
python app.py
```

### Access Dashboard:
Open your browser and navigate to: [http://localhost:5000/dashboard](http://localhost:5000/dashboard)

---

## How It Works

The **Beauty Retail Dashboard** provides insights through a combination of backend analytics and frontend visualizations.

### Backend (Flask)
- Processes retail transaction data using Pandas
- Implements K-means clustering to segment customers
- Provides recommendation algorithms through REST API endpoints
- Generates random monthly sales data for visualization purposes

### Frontend
- Responsive dashboard with interactive charts using Chart.js
- Customer clustering visualization showing spending patterns
- Monthly sales trends displayed as a line chart
- Personalized product recommendations based on customer ID
- Seasonal product recommendations with dropdown selection

---

## Screenshots

![Beauty Retail Dashboard](https://github.com/user-attachments/assets/db137dce-02b2-4026-9696-0177f571a752)

The dashboard displays two main visualizations:

### **Customer Clusters (K-Means)**
- Shows customer segmentation based on spending habits and purchase frequency
- Color-coded clusters representing different customer types

### **Monthly Sales Trends**
- Displays a line chart of sales performance across months

Additional panels allow for interactive product recommendations based on customer ID and seasonal preferences.
---

## **Dataset Description**

The dataset contains the following columns:

- `cust_id` : Customer ID
- `prod_id` : Product ID
- `product_name` : Name of the product
- `category` : Category of the product
- `purchase_amt` : Purchase amount
- `purchase_date` : Date of purchase

---

## **Recommendation System Details**

- **Collaborative Filtering (KNN)**: Finds similar customers based on purchase history and recommends products they bought.
- **Content-Based Filtering**: Recommends products based on categories of previously purchased items.
- **Context-Aware Recommendations**: Suggests products based on seasonal weather patterns.
- **Sale-Based Recommendations**: Highlights products currently on sale.

### **Example Output**

```plaintext
Recommended items using KNN for CUST001: ['Product A', 'Product B', 'Product C']
Recommended items using Content-Based Filtering for CUST001: ['Product D', 'Product E', 'Product F']
Most Popular Products during Sales: ['Product G', 'Product H', 'Product I']
Recommended items based on Winter weather: ['Product J', 'Product K', 'Product L']
```

---

## **Future Improvements**

- Enhance recommendation accuracy by incorporating additional features.
- Implement a user-friendly interface.
- Deploy the recommendation system as a web service.
- Integrate advanced clustering algorithms.
- Introduce evaluation metrics for recommender systems.

---

**Author:** Rishabh Naman Bhargava

---