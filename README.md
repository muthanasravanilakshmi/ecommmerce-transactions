# ecommmerce-transactions

# E-Commerce Transaction Data Analysis Dashboard

An interactive data analytics dashboard built using **Python, Streamlit, Pandas, NumPy, and Plotly** to analyze e-commerce transaction data from 2022 to 2025.

The dashboard provides insights into sales performance, customer behavior, merchant performance, product categories, payment methods, and transaction trends.

## Features

- **Executive Overview** – Key business KPIs and overall transaction performance.
- **Sales Analytics** – Revenue, transaction volume, and sales trends.
- **Customer Analytics** – Customer activity and purchasing behavior.
- **Merchant Analytics** – Merchant-wise transaction and revenue analysis.
- **Category Analytics** – Category-wise sales performance.
- **Payment Analytics** – Payment method and transaction status analysis.
- **Time Series Analysis** – Daily, monthly, and yearly transaction trends.

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Plotly

## Project Structure

```text
ecommerce-transactions/
│
├── app.py
├── requirements.txt
├── README.md
│
└── data/
    ├── transactions.csv
    ├── customer.csv
    ├── merchants.csv
    └── categories.csv
```

## Dataset Information

The project uses four CSV files:

| Dataset | Records |
|---|---:|
| Transactions | 60,000 |
| Customers | 20,000 |
| Merchants | 15,000 |
| Categories | 12,000 |
| **Total** | **107,000** |

**Transaction data coverage:** January 2022 – August 2025.

**Currency:** Indian Rupees (INR).

Transaction statuses include:
- SUCCESS
- REFUNDED
- FAILED
- PENDING
- CHARGEBACK

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd ecommerce-transactions
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the Streamlit Application

```bash
python -m streamlit run app.py
```

The dashboard will open in your browser, usually at:

```text
http://localhost:8501
```

## Requirements

The required Python libraries are listed in `requirements.txt`:

```text
streamlit>=1.40.0
pandas>=2.2.0
numpy>=1.26.0
plotly>=5.24.0
```

## Dashboard Design

The dashboard uses a **Blue and Cream** color theme with:

- Clean and professional layout.
- Interactive Plotly charts.
- KPI cards for important metrics.
- Sidebar navigation.
- Responsive visual elements.
- Easy-to-read data visualizations.

## Troubleshooting

**Streamlit module not found:**

```bash
python -m pip install streamlit
```

**Missing dependencies:**

```bash
python -m pip install -r requirements.txt
```

**CSV file not found:**

Make sure all four CSV files are placed inside the `data/` directory.

**Port already in use:**

```bash
python -m streamlit run app.py --server.port 8502
```
Live Demo : https://ecommmerce-transactions.streamlit.app/
## Author

**Sravani Muthana**

---

© 2026 Sravani Muthana. All rights reserved.
