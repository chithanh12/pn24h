# Define here the models for your scraped items

import scrapy


class ViolationItem(scrapy.Item):
    """Item for storing traffic violation information"""
    
    # Input fields
    license_plate = scrapy.Field()
    vehicle_type = scrapy.Field()
    
    # Output fields
    violation_found = scrapy.Field()
    violation_details = scrapy.Field()
    scraped_at = scrapy.Field()
    raw_html = scrapy.Field()
    
    # Metadata
    url = scrapy.Field()
    status = scrapy.Field()
    error_message = scrapy.Field()

