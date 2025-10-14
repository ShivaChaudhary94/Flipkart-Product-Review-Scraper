from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup 
import logging
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(filename="scrapper.log", level=logging.INFO)



app = Flask(__name__)

@app.route("/", methods=['GET'])
def homepage():
    return render_template("index.html")

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        search_query = request.form['query'].replace(" ", "")
        pages_to_scrape = int(request.form.get('pages', 1)) # default 1 page
        logging.info(f"Scraping query='{search_query}' for {pages_to_scrape} pages")

        
        # Selenium Setup
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no UI)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        

        product_links = []
        # Loop for Multiple Pages 
        for page in range(1, pages_to_scrape + 1):
            url = f"https://www.flipkart.com/search?q={search_query}&page={page}"
            driver.get(url)
            time.sleep(1) #Wait for JavaScript to load
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract Product Links
            for link in soup.find_all("a", href=True):
                if "/p/" in link["href"]:
                    full_link = "https://www.flipkart.com" + link["href"]
                    product_links.append(full_link)


        

        
        # Remove Duplicate links
        product_links = list(set(product_links))
        logging.info(f"Found {len(product_links)} unique product links")
        
        # Extract product Info    
        products = []
        for idx, link in enumerate(product_links, 1):
            try:
                logging.info(f"Processing product {idx}/{len(product_links)}: {link}")

                # Selenium for each product page 
                driver.get(link)
                time.sleep(1)
                prod_soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Product Name
                try:
                    name = prod_soup.find("span", {"class": "VU-ZEz"}).get_text(strip=True)
                except:
                    name = "N/A"
                
                # Rating
                try:
                    rating = prod_soup.find("div", {"class": "XQDdHH Ga3i8K"}).get_text(strip=True)
                except:
                    rating = "N/A"
                
                # Comment Title
                try:
                    comment_head = prod_soup.find("p", {"class": "z9E0IG"}).get_text(strip=True)
                except:
                    comment_head = "N/A"
                
                # Comment
                try:
                    comment = prod_soup.find("div", {"class": "ZmyHeo"}).get_text(strip=True)
                except:
                    comment = "N/A"

                products.append({
                    "Name": name,
                    "Rating": rating,
                    "Comment_Title": comment_head,
                    "Comment": comment,
                    "Link": link
                })
                
            except Exception as e:
                logging.error(f"Error processing product {link}: {e}")
                continue
        
        logging.info(f"Successfully scraped {len(products)} products")
         
         # Close Selenium 
        driver.quit()


        # Save Products Info in Mongodb

        uri = uri = "mongodb+srv://shivachry8_db_user:ShivaChry8@cluster0.oeojmxf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
        try:
            client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
            # Test connection
            client.admin.command('ping')
            logging.info("MongoDB connected successfully")

            #Create Database
            db = client['review_scrap']
            review_col = db['review_scrap_data']
            
            if products:
                for product in products:
                    review_col.update_one(
                        {"Link" : product["Link"]},    # Search by unique link
                        {"$set" : product},            # Update product details 
                        upsert=True)                    # Insert if not found
                logging.info(f"Upserted {len(products)} products to MongoDB (no duplicates!)")

        except Exception as e:
            logging.error(f"MongoDB error: {e}")
        

        return render_template("index.html", products=products, query=search_query)
        
    except Exception as e:
        logging.error(f"Error in scrape route: {e}")
        return render_template("index.html", error=str(e))


if __name__ == '__main__':
    app.run(debug=True)