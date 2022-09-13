
from itunes_app_scraper.scraper import AppStoreScraper

scraper = AppStoreScraper()
results = scraper.get_app_details(app_id=458066754, country="be")

app_details = scraper.get_multiple_app_details(similar)
print(list(app_details))

