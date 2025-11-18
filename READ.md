#  Yahoo Finance – Most Active Stocks Scraper  
Automated Web Scraping | Data Cleaning | Excel Export | Selenium | Python

This project extracts **Most Active stocks** from Yahoo Finance using Selenium, processes the data with Pandas/Numpy, and exports a clean Excel file ready for analysis.  
It includes a Jupyter notebook (exploration) and a production-ready Python script.

---

##  Project Overview

Yahoo Finance lists thousands of stocks across multiple pages.  
Manually collecting this data is slow and error-prone.

This scraper:

✔ Automatically navigates Yahoo Finance  
✔ Extracts stock data from **all pages**  
✔ Cleans values (market cap, P/E ratio, %, volume)  
✔ Saves data to Excel (`output/yahoo-stocks-data.xlsx`)  
✔ Provides both **Jupyter notebook** + **production script**


---

##  Key Features

### 🔹 **1. Fully automated web extraction**
- Selenium WebDriver  
- Dynamic page navigation  
- Handles multiple pages  
- Extracts 7+ stock metrics  

### 🔹 **2. Data Cleaning & Standardization**
Using Pandas + Numpy:
- Convert price/change to numeric  
- Convert "M", "B", "T" units properly  
- Handle missing P/E ratios  
- Remove formatting symbols  

### 🔹 **3. Clean Project Structure**

---

## 📊 Extracted Fields

| Field | Description |
|-------|-------------|
| `symbol` | Stock ticker |
| `name` | Full company name |
| `price_usd` | Latest market price |
| `change` | Daily change (%) |
| `volume_M` | Volume in millions |
| `market_cap_B` | Market cap in billions |
| `pe_ratio` | Price-to-earnings ratio |

---

##  Technologies Used

- **Python 3**
- **Selenium** (browser automation)
- **Pandas**
- **Numpy**
- **Chrome WebDriver**
- **OpenPyXL**

---

##  Installation

Clone the repo:

```bash
git clone https://github.com/GauravYadavGit/yahoo-finance-scraper.git
cd yahoo-finance-scraper


