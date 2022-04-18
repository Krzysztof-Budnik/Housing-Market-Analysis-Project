from bs4 import BeautifulSoup
from bs4 import ResultSet, Tag
import requests
from webscraper_elements import CssStyle


### defining css properties ### 
"""otodom.pl website changes frequently. This means the structure of html is modified, 
and therefore its necessary to change CSS element descriptions. Defining these elements at the beginnig
allows quicker adjustments"""

LISTING = CssStyle("li", "css-p74l73 es62z2j17")
TITLE = CssStyle("div", "css-jeloly es62z2j12")
PRICE = CssStyle("span", "css-rmqm02 eclomwz0")
LOCATION = CssStyle("span", "css-17o293g es62z2j9")
GRID = CssStyle("div", "css-1qzszy5 estckra8")


### webscrapper functions ###
def page_offer_list(url: str) -> ResultSet:
    """Function scrapes data from otodom.pl and gathers html code containing
    list of offers on given result page"""
    
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    listings = soup.find_all(LISTING.element, class_=LISTING.class_)
    return listings


def main_info(list_element: Tag) -> dict:
    """Function extracts main info from a list element 
    (that is a part of all listings on given page). Returning dict with title and price"""
    
    title = list_element.find(TITLE.element, class_=TITLE.class_).text
    price = list_element.find(PRICE.element, class_=PRICE.class_).text
    main_info = {"Tytuł": title, "Cena": price}
    return main_info


def location_info(list_element: Tag) -> dict:
    """Functions finds listings's location. Location elements such as 
    city, district and street are separated by coma. Location_info function
    extracts each element and stores the values in dictionary"""
    
    location = list_element.find(LOCATION.element, class_=LOCATION.class_).text
    location_split = location.split(",")
    
    # try-except structere is required becouse 
    # locations don't neccesarily have to contain all described elemnts
    try: city = location_split[0]
    except IndexError: city = "NA"
    
    try: district = location_split[1].strip()
    except IndexError: district = "NA"

    try: street = location_split[2].strip()
    except IndexError: street = "NA"
    
    location_info = {"Miasto": city, "Dzielnica": district, "Ulica": street}
    return location_info


def offer_url_generator(list_element: Tag) -> str:
    """Function extracts the link form particular listing, allowing the programme 
    to acess additional info. """
    
    offer_link = list_element.find('a', href=True)['href'] 
    offer_url = f"https://www.otodom.pl{offer_link}"
    return offer_url


def offer_id_generator(offer_url: str) -> str:
    """Function finds offer id, which is contained in the last link
    seven characters of an offer url"""
    return offer_url[-7:]


def offer_page_content(offer_url: str) -> BeautifulSoup:
    """Function acesses html code of specific offer page"""
    offer_page = requests.get(offer_url)
    offer_soup = BeautifulSoup(offer_page.content, 'html.parser')
    return offer_soup


def detailed_info(offer_soup: ResultSet) -> dict:
    """Function extracts data form grid and table layout on specific offer page.
    Then cateory and values are appended to appropriate lists. The last step is matching
    category - value pairs in a dictionary format"""
    
    grid = offer_soup.find_all(GRID.element, class_=GRID.class_)
    categories = []
    values = []
    for index, item in enumerate(grid):
        if index % 2 == 0:
            categories.append(item.text)
        else: 
            values.append(item.text)

    offer_data = {}
    for cat, val in zip(categories, values):
          offer_data[cat] = val

    return offer_data
    
    
def gather_offer_data(main_info: dict, location_info: dict, detailed_info: dict, id: str) -> list: 
    """Function is responsible for gathering all the data. Try-except structure is required 
    to ensure there are no errors when information about specific category is not provided on the offer page. 
    In case there is no relevant data from some category, "NA" value are inputted. 
    During the last step, function summarizes the data in a list (later it is simple to add 
    individial lists as separate records to csv file)"""
    
    # source: main_info()
    try: title = main_info["Tytuł"]
    except KeyError: title = "NA"
    
    try: price = main_info["Cena"]
    except KeyError: price = "NA"

    
    # source: location_info()
    try: city = location_info["Miasto"]
    except KeyError: city = "NA"
    
    try: district = location_info["Dzielnica"]
    except KeyError: district = "NA"

    try: street = location_info["Ulica"]
    except KeyError: street = "NA"
    
    
    # source: detailed_info
    try: area = detailed_info["Powierzchnia"] 
    except KeyError: area = "NA"
    
    try: rooms = detailed_info["Liczba pokoi"] 
    except KeyError: rooms = "NA"
    
    try: rent = detailed_info["Czynsz"]
    except KeyError: rent = "NA"
    
    try: floor = detailed_info["Piętro"]
    except KeyError: floor = "NA"

    try: year = detailed_info["Rok budowy"]
    except KeyError: year = "NA"

    try: balcony = detailed_info["Balkon / ogród / taras"]
    except KeyError: balcony = "NA"
    
    try: garage = detailed_info["Miejsce parkingowe"]
    except KeyError: garage = "NA"
    
    try: elevator = detailed_info["Winda"]
    except KeyError: elevator = "NA"

    try: furnishing = detailed_info["Wyposażenie"] 
    except KeyError: furnishing = "NA"
    
    try: extra_info = detailed_info["Informacje dodatkowe"] 
    except KeyError: extra_info = "NA"
    
    try: seller_type = detailed_info["Typ ogłoszeniodawcy"]
    except KeyError: seller_type = "NA"
    
    try: market = detailed_info["Rynek"] 
    except KeyError: market = "NA"

    try: ownership = detailed_info["Forma własności"]
    except KeyError: ownership = "NA"
    
    
    all_offer_data = [id, title, price, city, district, street, 
                      area, rooms, rent, floor, year, 
                      balcony, garage, elevator, furnishing, extra_info,
                      seller_type, market, ownership]
                      
    return all_offer_data