import time
import logging
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class StocksScraper:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout=timeout)
        self.data = []
        logger.info("StocksScraper initialized")

    def wait_for_page_to_load(self):
        page_title = self.driver.title
        try:
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            logger.info(f"Page loaded: {page_title}")
        except Exception as e:
            logger.info(f"Page load timeout: {page_title} | Error: {e}")

    def access_url(self, url):
        logger.info(f"Opening URL: {url}")
        self.driver.get(url)
        self.wait_for_page_to_load()

    def access_most_active_stocks(self):
        logger.info("Navigating to Most Active Stocks section")
        actions = ActionChains(self.driver)

        markets_menu = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="navigation-container"]/ol/li[3]/a/div'))
        )
        actions.move_to_element(markets_menu).perform()

        stocks_menu = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="navigation-container"]/ol/li[3]/ol/li[1]/a/span'))
        )
        actions.move_to_element(stocks_menu).perform()

        trending_menu = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="navigation-container"]/ol/li[3]/ol/li[1]/ol/li[4]/a/span'))
        )
        trending_menu.click()

        self.wait_for_page_to_load()

        most_active = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-most-active"]'))
        )
        most_active.click()

        self.wait_for_page_to_load()
        logger.info("Most Active Stocks table loaded")

    def extract_stocks_data(self):
        logger.info("Extracting stocks data")
        while True:
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            rows = self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

            for row in rows:
                values = row.find_elements(By.TAG_NAME, "td")
                if len(values) < 10:
                    continue
                stock = {
                    "name": values[1].text,
                    "symbol": values[0].text,
                    "price": values[3].text,
                    "change": values[4].text,
                    "volume": values[6].text,
                    "market_cap": values[8].text,
                    "pe_ratio": values[9].text,
                }
                self.data.append(stock)

            logger.info(f"Rows extracted so far: {len(self.data)}")

            try:
                next_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="main-content-wrapper"]/section[1]/div/div[4]/div[3]/button[3]'))
                )
            except:
                logger.info("Reached last page")
                break
            else:
                next_button.click()
                time.sleep(1)

    def clean_and_save_data(self, filename="temp"):
        logger.info("Cleaning extracted data")

        stocks_df = pd.DataFrame(self.data)

        stocks_df = stocks_df.apply(
            lambda col: col.str.strip() if col.dtype == "object" else col
        )

        stocks_df["price"] = stocks_df["price"].astype(float)

        stocks_df["change"] = (
            stocks_df["change"]
            .str.replace("+", "", regex=False)
            .astype(float)
        )

        stocks_df["volume"] = (
            stocks_df["volume"]
            .apply(lambda x: x.replace("M", ""))
            .astype(float)
        )

        def convert_mc(x):
            try:
                if "B" in x:
                    return float(x.replace("B", ""))
                if "T" in x:
                    return float(x.replace("T", "")) * 1000
                return np.nan
            except:
                return np.nan

        stocks_df["market_cap"] = stocks_df["market_cap"].apply(convert_mc)

        stocks_df["pe_ratio"] = (
            stocks_df["pe_ratio"]
            .astype(str)
            .str.strip()
            .replace(["--", "-", "", "None", "nan", "NaN", "N/A", "—"], np.nan)
            .str.replace(",", "", regex=False)
            .pipe(lambda col: pd.to_numeric(col, errors="coerce"))
        )

        stocks_df.rename(
            columns={"price": "price_usd", "volume": "volume_M", "market_cap": "market_cap_B"},
            inplace=True
        )

        stocks_df.to_excel(f"{filename}.xlsx", index=False)
        logger.info(f"Saved cleaned file to {filename}.xlsx")


if __name__ == "__main__":
    chrome_version = "142.0.7444.176"

    logger.info("Starting ChromeDriver")
    service = Service(ChromeDriverManager(driver_version=chrome_version).install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()


    scraper = StocksScraper(driver, 5)

    scraper.access_url("https://finance.yahoo.com/")
    scraper.access_most_active_stocks()
    scraper.extract_stocks_data()
    scraper.clean_and_save_data("output/yahoo_finance-stocks")

    driver.quit()
    logger.info("Scraper run completed")
