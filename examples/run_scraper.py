#!/usr/bin/env python3
"""
Example script to run the CSGT scraper

This script demonstrates how to run the scraper programmatically
"""

import subprocess
import sys
from pathlib import Path


def run_scraper(license_plate, vehicle_type='oto', output_file='results.json'):
    """
    Run the CSGT scraper with specified parameters
    
    Args:
        license_plate: License plate number (e.g., "30A12345")
        vehicle_type: Vehicle type - 'oto', 'xemay', or 'xedapdien'
        output_file: Output JSON file path
    """
    print(f"Scraping violations for license plate: {license_plate}")
    print(f"Vehicle type: {vehicle_type}")
    print(f"Output will be saved to: {output_file}")
    print("-" * 60)
    
    # Build scrapy command
    cmd = [
        'scrapy', 'crawl', 'csgt',
        '-a', f'license_plate={license_plate}',
        '-a', f'vehicle_type={vehicle_type}',
        '-O', output_file,
    ]
    
    # Run the command
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print("-" * 60)
        print(f"✓ Scraping completed! Check {output_file} for results.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error running scraper: {e}")
        return False
    except FileNotFoundError:
        print("✗ Scrapy not found! Make sure you have installed requirements:")
        print("  pip install -r requirements.txt")
        return False


def main():
    """Main function"""
    print("=" * 60)
    print("CSGT Traffic Violation Scraper")
    print("=" * 60)
    print()
    
    # Example: Check violations for a sample license plate
    # Replace with your actual license plate
    license_plate = input("Enter license plate number (e.g., 30A12345): ").strip()
    
    if not license_plate:
        print("No license plate provided!")
        return
    
    print()
    print("Select vehicle type:")
    print("1. Ô tô (Car)")
    print("2. Xe máy (Motorcycle)")
    print("3. Xe đạp điện (Electric bike)")
    
    choice = input("Enter choice (1-3) [default: 1]: ").strip() or "1"
    
    vehicle_type_map = {
        '1': 'oto',
        '2': 'xemay',
        '3': 'xedapdien'
    }
    
    vehicle_type = vehicle_type_map.get(choice, 'oto')
    
    print()
    output_file = input("Output file [default: results.json]: ").strip() or "results.json"
    
    print()
    
    # Run the scraper
    success = run_scraper(license_plate, vehicle_type, output_file)
    
    if success:
        print()
        print("NOTE: If captcha was downloaded, you may need to:")
        print("1. Check the captcha_images/ directory")
        print("2. Manually solve the captcha")
        print("3. Modify the spider to accept manual captcha input")
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

