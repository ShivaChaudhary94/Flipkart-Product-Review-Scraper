# Flipkart-Product-Review-Scraper

A web scraping and Flask application to collect Flipkart product reviews, ratings, and comments, store them in MongoDB, and provide a simple web interface for querying products. This project demonstrates data collection, data cleaning, database integration, and basic web development.


# 🛠️ Features

~Scrape product links, names, ratings, and reviews from Flipkart.

~Handle multiple pages of search results dynamically.

~Remove duplicate entries automatically.

~Store data in MongoDB with upsert to prevent duplicates.

~Simple Flask web interface to input search queries and view results.

~Robust logging and error handling for easier debugging.



# ⚡ Technologies Used

~Python 3.13.1

~Flask – for the web application

~Requests & BeautifulSoup – for fast web scraping

~Selenium – for pages requiring JavaScript rendering

~MongoDB – for storing scraped data

~Webdriver Manager – to automatically handle ChromeDriver

~Logging – track scraping progress and errors




# ⚙️ Usage

~Enter a product search query (e.g., mobile phone) in the input box.

~Optionally, specify the number of pages to scrape.

~Click Scrape, and the app will fetch product links, names, ratings, and reviews.

~Results are displayed on the web page and saved to MongoDB.
