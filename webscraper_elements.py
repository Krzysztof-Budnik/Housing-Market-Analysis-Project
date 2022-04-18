from dataclasses import dataclass


@dataclass
class CssStyle:
    """Css element types."""
    element: str
    class_: str
    
class MarketType:
    """Market types.""" 
    PRIMARY = "pierwotny"
    SECONDARY = "wtorny"
    
@dataclass
class SearchCriteria:
    """Class defines search criteria"""
    market_type: MarketType
    city: str
    limit: int
    
    def generate_url(self, page_number=1) -> str:
        """Method generates a custom url that matches criteria, 
        page_number parameter allows a user to choose the number of result page"""
        
        if self.market_type == "wtorny": mark = "?market=SECONDARY"
        elif self.market_type == "pierwotny": mark = "?market=PRIMARY"
        else: mark=""
        url = f"https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/{self.city}{mark}&limit={self.limit}&page={page_number}"
        return url
    
def get_url_list(search_criteria: SearchCriteria, num_of_pages: int) -> list:
    """Function creates a list of search url that match criteria. 
    Then the result (list) can be used as iterator in webscrapper."""
    
    url_list = []
    for i in list(range(1, num_of_pages + 1)):
        url_list.append(search_criteria.generate_url(i))
    return url_list    