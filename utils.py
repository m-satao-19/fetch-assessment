import re
import json
import math
from datetime import date, time

import logging
logger = logging.getLogger("fetch")

class Receipt_item:
    shortDescription: str
    price: float

    def __init__(self, shortDescription:str, price:str) -> None:
        self.shortDescription = shortDescription
        self.price = float(price)


    def points_description(self) -> int:

        if len(self.shortDescription.strip())%3==0:
            return math.ceil(self.price*0.2)

        return 0


class Receipt:
    retailer: str
    purchaseDate: str
    purchaseTime: str
    items: list
    total: float

    def __init__(self, retailer:str,purchaseDate:str,purchaseTime:str,total:str,items:list) -> None:
        self.retailer = retailer
        self.purchaseDate = purchaseDate
        self.purchaseTime = purchaseTime
        self.total = float(total)
        self.items = items


    def points_retailer(self) -> int:

        points = len(re.sub("[^a-zA-Z0-9]","",self.retailer))

        logger.info(f"Calculated {points} points for retailer name")

        return points
    

    def points_total(self) -> int:

        points = 0

        if self.total.is_integer():
            points += 50

        if self.total%0.25==0:
            points += 25

        logger.info(f"Calculated {points} points for total amount")

        return points
    

    def points_items(self) -> int:

        points = 0

        for item in self.items:

            item = Receipt_item(shortDescription=item["shortDescription"],price=item["price"])

            points += item.points_description()

        logger.info(f"Calculated {points} points for description of items")

        return points


    def points_length(self) -> int:

        points = (len(self.items)//2)*5

        logger.info(f"Calculated {points} points for items, 5 for every 2")
        return points
    

    def points_purchaseDate(self) -> int:
        
        d = date.fromisoformat(self.purchaseDate)

        points =  6 if d.day%2==1 else 0

        logger.info(f"Calculated {points} points for odd day in the date")

        return points
        
    
    def points_purchaseTime(self) -> int:

        t = time.fromisoformat(self.purchaseTime)

        points = 10 if (14<=t.hour and t.hour<=16) else 0

        logger.info(f"Calculated {points} points for time between 2 and 4 pm")

        return points

        
def calculate_points(receipt) -> int:

    receipt = Receipt(**receipt)

    points =  receipt.points_retailer() + receipt.points_total() + receipt.points_length() + receipt.points_items() + receipt.points_purchaseDate() + receipt.points_purchaseTime()

    logger.info(f"Calculated {points} points total")

    return points