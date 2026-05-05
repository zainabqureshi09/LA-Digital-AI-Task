# Google Maps Scraper (Gyms in Karachi)

A beginner-friendly Python script using **Selenium** and **Pandas** to scrape business information from Google Maps. 

## 📋 Features
- Scrapes **Business Name**, **Phone Number**, **Address**, and **Website**.
- Automatically handles scrolling to load multiple results (target: 50+).
- Exports data to a clean **CSV** format.
- Uses `webdriver-manager` to automatically handle ChromeDriver installation.
- Runs in **Headless Mode** (no browser window pops up).

## 🛠️ Prerequisites
- [Python 3.x](https://www.python.org/) installed.
- [Google Chrome](https://www.google.com/chrome/) installed.

## 🚀 Installation

1. **Clone or download** this folder.
2. **Install the required libraries** using pip:

```bash
pip install selenium pandas webdriver-manager
```

## 💻 Usage

Run the script from your terminal or command prompt:

```bash
python gym_scraper.py
```

The script will:
1. Open a background Chrome instance.
2. Search for "gym Karachi" on Google Maps.
3. Scroll through results and extract details for 50 gyms.
4. Save the results to `gyms_karachi.csv`.

## ⚙️ Configuration
You can customize the script by editing the variables at the top of `gym_scraper.py`:

```python
SEARCH_QUERY = "gym Karachi" # Change the city or business type
MAX_RESULTS = 50             # Increase or decrease the target count
OUTPUT_FILE = "gyms.csv"     # Change the output filename
```

## 📝 Notes
- **Instagram Handles**: Google Maps doesn't provide Instagram handles directly. The script extracts the business website; you can usually find their social media links there.
- **Headless Mode**: The script is currently set to `--headless=new`. To see the browser while it works, comment out the line `chrome_options.add_argument("--headless=new")` in the `setup_driver` function.

## ⚖️ Disclaimer
This tool is for educational purposes. Always respect the [Google Maps Terms of Service](https://www.google.com/help/terms_maps/) and use web scraping responsibly.
