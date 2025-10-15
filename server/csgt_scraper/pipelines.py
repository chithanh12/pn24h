# Define your item pipelines here

from datetime import datetime
import json


class CsgtScraperPipeline:
    """Pipeline to process scraped violation items"""
    
    def open_spider(self, spider):
        """Initialize pipeline when spider opens"""
        spider.logger.info("Pipeline opened")
        
    def close_spider(self, spider):
        """Cleanup when spider closes"""
        spider.logger.info("Pipeline closed")
        
    def process_item(self, item, spider):
        """Process each scraped item"""
        # Add timestamp if not present
        if 'scraped_at' not in item:
            item['scraped_at'] = datetime.now().isoformat()
        
        # Log the result
        spider.logger.info(f"Processed item for license plate: {item.get('license_plate', 'N/A')}")
        
        return item

