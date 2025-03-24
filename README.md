# Review Aggregation Web-Scraping Program

This capstone project is a webscraping tool that gathers reviews for a given restaurant from multiple online platforms and uses machine learning to extract insights. The tool aggregates customer feedback from major platforms in one place, providing a comprehensive view of customer sentiment and experience. Rather than manually checking multiple review sites, the user can utilize this tool to centralize reviews in one interface, saving time and enabling data-driven decisions.

# Features

## Multi-Source Review Aggregation
Scrapes reviews from:
- Google Reviews
- Yelp
- OpenTable
- TripAdvisor

## Automated Web Scraping
Utilizes Python libraries:
- BeautifulSoup for HTML parsing
- Selenium for sites that block scraping activity

## Data Handling
Stores collected reviews in Pandas DataFrames for further analysis.

## Machine Learning Insights
May implement some of the following ML tasks:
- Clustering: Groups similar reviews using unsupervised learning
- Sentiment Analysis: Categorizes reviews as positive or negative
- Topic Modeling: Extracts common themes using natural language processing
- Summarization: Generates concise summaries of customer feedback

## Interactive Web App
User-friendly front-end built with either Flask or Django.

# Planning resources
Flask—(Creating first simple application). (2024, August 18). GeeksforGeeks. https://www.geeksforgeeks.org/flask-creating-first-simple-application/  
Need to Scrape Yelp Reviews? Check Out This Tutorial. (2025, January 9). ScrapeHero. https://www.scrapehero.com/scrape-yelp-reviews/  
Ondiek, E. (2021, September 7). Scraping the Web with Ease: Building a Python Web Scraper with Flask. DEV Community. https://dev.to/ondiek/building-a-python-web-scraper-in-flask-b87  
Web Scraping Google Reviews: A How-to Guide | LinkedIn. (2024, August 27). https://www.linkedin.com/pulse/web-scraping-google-reviews-how-to-guide-scrape-hero-c5dzc/  
