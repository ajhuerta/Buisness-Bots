from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

class EtsyScrapper:
    def __init__(self):
        # constructor variables
        self.path_name = "/Users/anthonyh/Downloads/chromedriver"
        self.base_url = "https://www.etsy.com/market/"
        self.page_url = "?ref=pagination&page="
        self.driver = webdriver.Chrome(self.path_name)

    # This function will search for a specific item and find the corresponding data for ONLY the first page
    def first_page_search(self, item):
        # Checks to see if input is a string
        if type(item) != str:
            raise TypeError("Item must be a string format")

        total = 0
        item_dictionary = {}
        item = item.replace(" ", "_")

        # Creates a new url using the item input by the user
        new_url = self.base_url + item
        self.driver.get(new_url)

        # Collects the prices of every item as well as their name in two seperate lists
        item_prices = list(self.driver.find_elements(By.CLASS_NAME, "currency-value"))
        item_names = list(self.driver.find_elements(By.CLASS_NAME, "wt-mb-xs-0.wt-text-truncate.wt-text-caption.v2-listing-card__title"))

        # Loops through every item, removes any duplicates and organizes each item and it's price in a dictionary
        for x in range(len(item_names)):
            if item_names[x].text not in item_dictionary:
                item_dictionary[item_names[x].text] = item_prices[x].text
                total += float(item_prices[x].text.replace(",", ""))

        # Creates the csv with all of the data that had been scrapped
        with open('Etsy-Bot/output.csv', 'w') as output:
            writer = csv.writer(output)

            writer.writerow(["Category", "Price"])
            for key, value in item_dictionary.items():
                writer.writerow([key,value])
            writer.writerow(["Average Price", total/len(item_prices)])

        self.driver.quit()

    # This function will search for a specific item and find the corresponding data for as many pages specified
    def multi_page_search(self, item):

        if type(item) != str:
            raise TypeError("Item must be a string format")

# Main function
def main():
    instance = EtsyScrapper()
    instance.first_page_search("face oil")

if __name__ == "__main__":
    main()