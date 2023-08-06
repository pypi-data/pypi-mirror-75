# Vulture
Data Collector and Management Tools for PSF Data. It has three major components to it as follow:

## Components:
### 1. DeltaMetaData: A data managment tool that interacts with the following Data Sources:
**DataBase:**
1. MongoDB
2. Postgres

**IndexingEngine:**
1. ElasticSearch

### 2. Web Scrappers
1. Website Scrapper: 
    - Menu Links Scrapper
    - Content Scrapper 
2. Linkedin Company Page Scrapper
3. NAICS Website Scrapper
4. PSC Tool Scrapper

### 3. Reporting tool
Build using flask admin that can be used to export the following reports
1. Data Stats
2. Keywords
3. Similar Suppliers

## Technologies:
1. Postgres
2. MongoDB
3. ElasticSearch
4. Celery
5. Flask + Flask Admin
6. Gunicorn
