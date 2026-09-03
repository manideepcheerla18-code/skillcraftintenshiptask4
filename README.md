# 🛒 Next-Level Product Scraper

A modern and professional **standalone Product Scraper desktop application** built with Python and Tkinter. The application allows users to enter multiple product URLs and automatically extract useful product information such as title, price, rating, description, image URL, and source URL.

The project features a colorful dark/neon interface with search, filtering, sorting, export options, progress tracking, and light/dark theme support.

---

## ✨ Features

* 🔗 Scrape multiple product URLs
* 🏷️ Extract product title
* 💰 Extract product price
* ⭐ Extract product rating
* 📝 Extract product description
* 🖼️ Extract product image URL
* 🌐 Store product source URL
* 🔍 Search and filter scraped products
* ↕️ Sort products by price
* 📊 Live scraping progress
* 📋 Copy selected product information
* 🗑️ Delete selected products
* 🧹 Clear all results
* 🌐 Open product website
* 📄 Export data to CSV
* 📊 Export data to Excel
* 🌙 Dark/Light theme
* 🧵 Background scraping using threads
* 🕐 Live clock and status bar
* 🎨 Modern colorful desktop interface

---

## 🖥️ Interface

The application provides a professional desktop interface containing:

* URL input section
* Multiple URL queue
* Scraping controls
* Statistics panel
* Search toolbar
* Product results table
* Progress bar
* Status information
* Theme switcher

---

## 🛠️ Technologies Used

* **Python 3.14**
* **Tkinter** – Desktop GUI
* **Requests** – Sending HTTP requests
* **BeautifulSoup4** – HTML parsing
* **OpenPyXL** – Excel file generation
* **CSV** – Data export
* **Threading** – Background scraping

---

## 📁 Project Structure

```text
Product-Scraper/
│
├── app.py
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

### 1. Install Python

Make sure Python 3.14 is installed on your computer.

Check your Python version:

```bash
python --version
```

or:

```bash
py --version
```

---

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/product-scraper.git
```

Move into the project folder:

```bash
cd product-scraper
```

---

### 3. Install Required Libraries

```bash
pip install requests beautifulsoup4 openpyxl
```

If your system uses `py`:

```bash
py -m pip install requests beautifulsoup4 openpyxl
```

---

## ▶️ Run the Application

Run:

```bash
python app.py
```

or:

```bash
py app.py
```

The Product Scraper desktop application will open automatically.

---

## 🔗 How to Use

### Step 1

Enter a product URL into the URL field.

### Step 2

Click **Add URL**.

### Step 3

Add additional product URLs if required.

### Step 4

Click **Start Scraping**.

### Step 5

The application extracts available product information.

### Step 6

Use the search and sorting tools to organize your results.

### Step 7

Export your results using:

* **Export CSV**
* **Export Excel**

---

## 📊 Extracted Information

The scraper attempts to collect:

| Information  | Description                   |
| ------------ | ----------------------------- |
| Product Name | Name/title of the product     |
| Price        | Available product price       |
| Rating       | Product rating when available |
| Description  | Product description           |
| Image URL    | Main product image URL        |
| Source URL   | Original product webpage      |

---

## 📤 Export Options

The application supports exporting scraped information into:

### CSV

```text
products.csv
```

### Excel

```text
products.xlsx
```

This makes the collected information easy to analyze or use in other applications.

---

## 🎨 UI Features

The application uses a modern **dark/neon-inspired interface** with:

* Colorful buttons
* Modern panels
* Statistics cards
* Product table
* Progress indicator
* Light/Dark theme
* Responsive controls

---

## ⚠️ Important Notes

This project uses normal HTTP requests and HTML parsing.

Some websites may:

* Block automated requests
* Require JavaScript to display product information
* Use dynamically generated content
* Require authentication
* Have anti-bot protection

Therefore, the scraper may not work correctly with every website.

Use the application only on websites where automated access and scraping are permitted.

---

## 🚀 Future Improvements

Possible future upgrades include:

* 🖼️ Display product images inside the application
* 🤖 JavaScript-rendered page support
* 📈 Price history tracking
* 🔔 Price-drop notifications
* 🗄️ SQLite database integration
* 🔎 Advanced product search
* 📊 Price comparison dashboard
* 📥 Automatic scheduled scraping
* 🧠 AI-based product analysis
* 📱 Responsive web version
* 📦 Standalone `.exe` version

---

## 🎯 Project Purpose

This project was created to demonstrate practical Python programming concepts including:

* GUI development
* Web scraping
* HTML parsing
* HTTP requests
* Multithreading
* Data processing
* File handling
* CSV/Excel generation
* User interface design

