# Quick Start Guide

Get up and running with the CSGT scraper in 5 minutes!

## Step 1: Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt

# Install Tesseract-OCR (for captcha solving)
# macOS:
brew install tesseract

# Ubuntu/Debian:
# sudo apt-get install tesseract-ocr

# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
```

## Step 2: Run Your First Scrape

### Option A: Interactive Mode
```bash
python examples/run_scraper.py
```

Then follow the prompts to enter:
- License plate number (e.g., `30A12345`)
- Vehicle type (1 for car, 2 for motorcycle, 3 for electric bike)
- Output file name (e.g., `results.json`)

### Option B: Command Line
```bash
scrapy crawl csgt -a license_plate=30A12345 -a vehicle_type=oto -O results.json
```

## Step 3: Handle the Captcha

The scraper will:
1. Download the captcha image to `captcha_images/` folder
2. Try to solve it automatically using OCR
3. If OCR fails, you'll see the saved captcha image path in the logs

**For manual solving:**
1. Open the captcha image
2. Note the text
3. You can modify the spider to accept manual input

## Step 4: View Results

Check the output JSON file:
```bash
cat results.json
# or
python -m json.tool results.json
```

## Common Commands

### Check a single car license plate:
```bash
scrapy crawl csgt -a license_plate=30A12345 -a vehicle_type=oto -O car_results.json
```

### Check a motorcycle:
```bash
scrapy crawl csgt -a license_plate=51F67890 -a vehicle_type=xemay -O bike_results.json
```

### Check an electric bicycle:
```bash
scrapy crawl csgt -a license_plate=29X54321 -a vehicle_type=xedapdien -O ebike_results.json
```

### Run in debug mode (verbose logging):
```bash
scrapy crawl csgt -a license_plate=30A12345 -L DEBUG
```

## Batch Processing Multiple Plates

1. Edit `examples/batch_scraper.py`
2. Add your license plates to the list:
```python
license_plates = [
    ("30A12345", "oto"),
    ("51F67890", "xemay"),
    ("29X54321", "xedapdien"),
]
```
3. Run the batch script:
```bash
python examples/batch_scraper.py
```

## Tips

1. **OCR Not Working?** 
   - Make sure Tesseract is installed: `tesseract --version`
   - Check the captcha image quality in `captcha_images/`

2. **Want Faster Results?**
   - Use batch processing for multiple plates
   - Adjust `DOWNLOAD_DELAY` in settings (but be respectful!)

3. **Need to Debug?**
   - Use `scrapy shell` to test selectors:
     ```bash
     scrapy shell "https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html"
     ```

4. **Customize Output:**
   - JSON: `-O results.json` (overwrites)
   - JSON append: `-o results.json` (appends)
   - CSV: `-O results.csv`
   - XML: `-O results.xml`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Customize the spider in `csgt_scraper/spiders/csgt_spider.py`
- Improve captcha solving in `csgt_scraper/utils/captcha_solver.py`
- Add your own data processing in `csgt_scraper/pipelines.py`

## Need Help?

Check these resources:
- [Scrapy Documentation](https://docs.scrapy.org/)
- [Pytesseract Documentation](https://github.com/madmaze/pytesseract)
- Project README: [README.md](README.md)

Happy scraping! 🚗🔍

