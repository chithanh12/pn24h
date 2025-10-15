#!/usr/bin/env python3
"""
Script to run the CSGT scraper with manual captcha input

This script downloads the captcha, shows it to you, and lets you input it manually
for better accuracy than OCR.
"""

import sys
import os
import subprocess
import tempfile
import json
from pathlib import Path

# Add the project to path
sys.path.insert(0, str(Path(__file__).parent))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from csgt_scraper.spiders.csgt_spider import CsgtSpider


def run_scraper_with_manual_captcha(license_plate, vehicle_type='xemay'):
    """
    Run scraper with manual captcha solving
    
    Args:
        license_plate: License plate number
        vehicle_type: Vehicle type (oto, xemay, xedapdien)
    """
    print("=" * 60)
    print("CSGT Scraper with Manual Captcha Input")
    print("=" * 60)
    print(f"License Plate: {license_plate}")
    print(f"Vehicle Type: {vehicle_type}")
    print()
    
    # Create a custom spider that pauses for manual input
    class ManualCaptchaSpider(CsgtSpider):
        """Spider with manual captcha input"""
        
        def solve_captcha(self, image_path):
            """Override to use manual input"""
            print("\n" + "=" * 60)
            print(f"CAPTCHA IMAGE SAVED: {image_path}")
            print("=" * 60)
            
            # Try to open the image
            try:
                import platform
                system = platform.system()
                
                if system == 'Darwin':  # macOS
                    subprocess.run(['open', str(image_path)])
                elif system == 'Windows':
                    os.startfile(str(image_path))
                elif system == 'Linux':
                    subprocess.run(['xdg-open', str(image_path)])
                    
                print("✓ Captcha image opened in default viewer")
            except Exception as e:
                print(f"Could not open image automatically: {e}")
                print(f"Please open it manually: {image_path}")
            
            print()
            print("Please look at the captcha image and enter the text below:")
            captcha_text = input("Enter captcha: ").strip()
            
            if captcha_text:
                print(f"✓ Using captcha: {captcha_text}")
                return captcha_text
            else:
                print("⚠ No captcha entered!")
                return None
    
    # Run the spider
    settings = get_project_settings()
    settings.set('FEEDS', {
        'results_manual.json': {
            'format': 'json',
            'encoding': 'utf-8',
            'overwrite': True,
        }
    })
    
    process = CrawlerProcess(settings)
    process.crawl(
        ManualCaptchaSpider,
        license_plate=license_plate,
        vehicle_type=vehicle_type
    )
    process.start()
    
    print("\n" + "=" * 60)
    print("Scraping completed!")
    print("Results saved to: results_manual.json")
    print("=" * 60)


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python run_with_manual_captcha.py <license_plate> [vehicle_type]")
        print()
        print("Examples:")
        print("  python run_with_manual_captcha.py 59C136047 xemay")
        print("  python run_with_manual_captcha.py 30A12345 oto")
        print()
        print("Vehicle types: oto (car), xemay (motorcycle), xedapdien (electric bike)")
        sys.exit(1)
    
    license_plate = sys.argv[1]
    vehicle_type = sys.argv[2] if len(sys.argv) > 2 else 'xemay'
    
    run_scraper_with_manual_captcha(license_plate, vehicle_type)


if __name__ == '__main__':
    main()

