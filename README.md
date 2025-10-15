# CSGT Traffic Violation Scraper

A Python Scrapy-based web scraper for checking traffic violations from the Vietnamese traffic police website (https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html).

## Features

- 🚗 Support for multiple vehicle types (cars, motorcycles, electric bikes)
- 🔍 Automated license plate violation checking
- 🖼️ Captcha handling with OCR support
- 📊 JSON output format
- 🔄 Batch processing capability
- 📝 Detailed logging

## Prerequisites

- Python 3.8 or higher
- Tesseract-OCR (for automatic captcha solving)

### Installing Tesseract-OCR

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

## Installation

1. **Clone or download this repository**

2. **Create a virtual environment (recommended):**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

### Method 1: Using Scrapy Command Line

Basic usage:
```bash
scrapy crawl csgt -a license_plate=30A12345 -a vehicle_type=oto -O results.json
```

Parameters:
- `license_plate`: Vehicle license plate number (required)
- `vehicle_type`: Type of vehicle (optional, default: "oto")
  - `oto` - Car
  - `xemay` - Motorcycle
  - `xedapdien` - Electric bicycle

### Method 2: Using the Example Script

Run the interactive script:
```bash
python examples/run_scraper.py
```

This will prompt you for:
- License plate number
- Vehicle type
- Output file name

### Method 3: Batch Processing

For checking multiple license plates:
```bash
python examples/batch_scraper.py
```

Edit the `license_plates` list in `batch_scraper.py` to add your plates.

## Project Structure

```
scrappy/
├── csgt_scraper/              # Main Scrapy project
│   ├── spiders/
│   │   ├── __init__.py
│   │   └── csgt_spider.py     # Main spider
│   ├── utils/
│   │   ├── __init__.py
│   │   └── captcha_solver.py  # Captcha solving utilities
│   ├── __init__.py
│   ├── items.py               # Data models
│   ├── middlewares.py         # Scrapy middlewares
│   ├── pipelines.py           # Data processing pipelines
│   └── settings.py            # Scrapy settings
├── examples/
│   ├── run_scraper.py         # Example runner script
│   └── batch_scraper.py       # Batch processing script
├── captcha_images/            # Directory for saved captchas
├── scrapy.cfg                 # Scrapy configuration
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Captcha Handling

The scraper includes multiple methods for handling captchas:

### 1. Automatic OCR (Default)
The spider will attempt to solve captchas automatically using Tesseract OCR:
```python
from csgt_scraper.utils.captcha_solver import solve_captcha_ocr

captcha_text = solve_captcha_ocr('captcha_images/captcha.png')
```

### 2. Manual Input
When OCR fails, the captcha image is saved to `captcha_images/` directory. You can:
- Check the image file
- Manually input the captcha text
- Modify the spider to accept manual input

### 3. API Integration (Advanced)
For production use, you can integrate third-party captcha solving services:
- 2Captcha
- Anti-Captcha
- DeathByCaptcha

See `csgt_scraper/utils/captcha_solver.py` for implementation details.

## Output Format

The scraper outputs JSON with the following structure:

```json
[
  {
    "license_plate": "30A12345",
    "vehicle_type": "oto",
    "violation_found": true,
    "violation_details": [
      {
        "date": "2024-01-15",
        "location": "Hanoi",
        "violation_type": "Speeding",
        "fine_amount": "800,000 VND",
        "status": "Unpaid"
      }
    ],
    "scraped_at": "2024-10-15T10:30:00",
    "url": "https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html",
    "status": "success"
  }
]
```

## Configuration

### Scrapy Settings

You can modify settings in `csgt_scraper/settings.py`:

- `DOWNLOAD_DELAY`: Delay between requests (default: 2 seconds)
- `CONCURRENT_REQUESTS`: Number of concurrent requests (default: 1)
- `USER_AGENT`: Browser user agent string
- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING, ERROR)

### Spider Settings

Modify spider behavior in `csgt_scraper/spiders/csgt_spider.py`:

- Captcha solving method
- Form selectors
- Result parsing logic

## Troubleshooting

### Issue: "OCR could not extract text from captcha"
**Solution:** 
- Ensure Tesseract-OCR is properly installed
- Check if the captcha image is saved correctly
- Try manual captcha solving

### Issue: "No results found"
**Solution:**
- Verify the license plate format is correct
- Check if the website structure has changed
- Review the scrapy logs for errors

### Issue: Form submission fails
**Solution:**
- The website may have updated its form structure
- Check the HTML source and update form selectors in the spider
- Ensure cookies are enabled

## Legal & Ethical Considerations

⚠️ **Important:**
- This tool is for educational purposes only
- Respect the website's terms of service
- Use reasonable delays between requests
- Do not overload the server
- Ensure you have the right to access this data

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is provided as-is for educational purposes.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Scrapy documentation: https://docs.scrapy.org/
3. Check pytesseract documentation for OCR issues

## Changelog

### Version 1.0.0 (2024-10-15)
- Initial release
- Basic scraping functionality
- Captcha handling with OCR
- Batch processing support
- JSON output format

## Roadmap

- [ ] Improve OCR accuracy
- [ ] Add GUI interface
- [ ] Support for more vehicle types
- [ ] Database storage option
- [ ] Email notifications for new violations
- [ ] API wrapper

---

**Disclaimer:** This scraper is provided as-is without any warranties. Use at your own risk and responsibility.

