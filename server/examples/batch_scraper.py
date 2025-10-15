#!/usr/bin/env python3
"""
Batch scraper for multiple license plates

This script demonstrates how to scrape violations for multiple vehicles
"""

import subprocess
import json
import time
from pathlib import Path


def scrape_license_plate(license_plate, vehicle_type='oto'):
    """
    Scrape a single license plate
    
    Args:
        license_plate: License plate number
        vehicle_type: Vehicle type
        
    Returns:
        dict: Results or None if error
    """
    print(f"Processing: {license_plate} ({vehicle_type})")
    
    # Temporary output file
    temp_output = f"temp_{license_plate.replace(' ', '_')}.json"
    
    cmd = [
        'scrapy', 'crawl', 'csgt',
        '-a', f'license_plate={license_plate}',
        '-a', f'vehicle_type={vehicle_type}',
        '-O', temp_output,
        '--loglevel=ERROR',  # Suppress most logs
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        
        # Read results
        if Path(temp_output).exists():
            with open(temp_output, 'r', encoding='utf-8') as f:
                results = json.load(f)
            
            # Clean up temp file
            Path(temp_output).unlink()
            
            return results[0] if results else None
        else:
            return None
            
    except Exception as e:
        print(f"  Error: {e}")
        return None


def main():
    """Main function for batch scraping"""
    print("=" * 60)
    print("CSGT Batch Scraper")
    print("=" * 60)
    print()
    
    # List of license plates to check
    # Format: (license_plate, vehicle_type)
    license_plates = [
        ("30A12345", "oto"),
        ("51F67890", "oto"),
        ("29X54321", "xemay"),
        # Add more license plates here
    ]
    
    results = []
    
    for plate, vehicle_type in license_plates:
        result = scrape_license_plate(plate, vehicle_type)
        
        if result:
            results.append(result)
            print(f"  ✓ Success")
        else:
            print(f"  ✗ Failed")
        
        # Add delay between requests to be respectful
        time.sleep(3)
        print()
    
    # Save all results
    output_file = "batch_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("=" * 60)
    print(f"Batch scraping completed!")
    print(f"Processed: {len(license_plates)} license plates")
    print(f"Successful: {len(results)}")
    print(f"Results saved to: {output_file}")
    print("=" * 60)


if __name__ == '__main__':
    main()

