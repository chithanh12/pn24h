"""
CSGT Traffic Violation Spider

This spider scrapes the Vietnamese traffic police website to check for violations
given a license plate number, vehicle type, and captcha solution.
"""

import scrapy
import base64
import os
from datetime import datetime
from pathlib import Path
from csgt_scraper.items import ViolationItem


class CsgtSpider(scrapy.Spider):
    name = "csgt"
    allowed_domains = ["csgt.vn"]
    start_urls = ["https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html"]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'COOKIES_ENABLED': True,
        'COOKIES_DEBUG': True,  # Enable cookie debugging
        'HTTPCACHE_ENABLED': False,  # Disable cache for this spider
        'CONCURRENT_REQUESTS': 1,  # Process one request at a time to maintain session
    }
    
    def __init__(self, license_plate=None, vehicle_type="oto", max_retries=3, *args, **kwargs):
        """
        Initialize spider with search parameters
        
        Args:
            license_plate: License plate number (e.g., "30A12345")
            vehicle_type: Type of vehicle - "oto" (car), "xemay" (motorcycle), "xedapdien" (electric bike)
            max_retries: Maximum number of captcha retry attempts (default: 3)
        """
        super(CsgtSpider, self).__init__(*args, **kwargs)
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self.max_retries = int(max_retries)
        self.retry_count = 0
        
        # Create directory for captcha images
        self.captcha_dir = Path("captcha_images")
        self.captcha_dir.mkdir(exist_ok=True)
        
        # Validate inputs
        if not self.license_plate:
            self.logger.warning("No license plate provided! Use -a license_plate=<plate>")
    
    def start_requests(self):
        """Override start_requests to explicitly set cookie jar"""
        for url in self.start_urls:
            self.logger.info(f"Starting request to: {url} with cookiejar=1")
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={'cookiejar': 1},  # Explicitly use cookie jar 1 from the start
                dont_filter=True
            )
    
    def parse(self, response):
        """Parse the main search page and extract captcha"""
        self.logger.info(f"Parsing main page: {response.url}")
        
        if not self.license_plate:
            self.logger.error("License plate is required!")
            return
        
        # Extract captcha image
        captcha_url = response.css('img#imgCaptcha::attr(src)').get()
        
        if captcha_url:
            self.logger.info(f"Found captcha image: {captcha_url}")
            
            # If it's a relative URL, make it absolute
            if not captcha_url.startswith('http'):
                captcha_url = response.urljoin(captcha_url)
            
            self.logger.info("IMPORTANT: Maintaining session cookies for captcha validation")
            
            # Download and save captcha image
            # IMPORTANT: We need to maintain the session that was created with the main page
            yield scrapy.Request(
                captcha_url,
                callback=self.save_captcha,
                meta={
                    'main_response': response,  # Store the ENTIRE response object
                    'dont_cache': True,
                    'cookiejar': 1,  # Use cookie jar 1
                },
                dont_filter=True,  # Allow multiple captcha downloads
                priority=10  # High priority
            )
        else:
            self.logger.error("Could not find captcha image!")
            # Try to submit without captcha or with user input
            yield from self.submit_form(response, "")
    
    def save_captcha(self, response):
        """Save captcha image and prompt for manual input"""
        # Save captcha image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        captcha_filename = self.captcha_dir / f"captcha_{timestamp}.png"
        
        with open(captcha_filename, 'wb') as f:
            f.write(response.body)
        
        self.logger.info(f"Captcha saved to: {captcha_filename}")
        self.logger.info("=" * 60)
        self.logger.info("CAPTCHA IMAGE SAVED!")
        self.logger.info(f"Please check: {captcha_filename}")
        
        # Log cookies to verify session is maintained
        cookies = response.headers.getlist('Set-Cookie')
        if cookies:
            self.logger.info(f"Session cookies received from captcha: {len(cookies)} cookie(s)")
            for cookie in cookies:
                self.logger.info(f"  Cookie: {cookie.decode('utf-8')[:100]}")
        
        # Log request cookies
        request_cookies = response.request.headers.getlist('Cookie')
        if request_cookies:
            self.logger.info(f"Request cookies sent to captcha: {len(request_cookies)} cookie(s)")
            for cookie in request_cookies:
                self.logger.info(f"  Request Cookie: {cookie.decode('utf-8')[:100]}")
        
        self.logger.info("=" * 60)
        
        # Try to solve captcha automatically (basic implementation)
        captcha_text = self.solve_captcha(captcha_filename)
        
        if not captcha_text:
            # If automatic solving fails, you can implement manual input here
            self.logger.warning("Automatic captcha solving failed!")
            self.logger.info("You can implement manual captcha input or use OCR")
            captcha_text = ""  # Empty for now
        
        # Get the main page response from meta
        main_response = response.meta.get('main_response')
        
        # IMPORTANT: Submit directly without reloading the page
        # Reloading might refresh the captcha session and invalidate it!
        self.logger.info(f"Submitting form directly with session cookies (not reloading page)")
        
        # Submit the form directly with the captcha text
        yield from self.submit_form(main_response, captcha_text)
    
    def solve_captcha(self, image_path):
        """
        Attempt to solve captcha automatically using OCR with multiple preprocessing methods
        
        Args:
            image_path: Path to captcha image
            
        Returns:
            Captcha text or None if solving fails
        """
        try:
            import pytesseract
            from PIL import Image, ImageEnhance, ImageFilter
            from collections import Counter
            
            img = Image.open(image_path)
            
            # Try multiple preprocessing and OCR configurations
            results = []
            
            # Configuration 1: Original image, PSM 8 (single word)
            try:
                text = pytesseract.image_to_string(
                    img, 
                    config='--psm 8 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                ).strip()
                if text and len(text) >= 4:
                    results.append(text)
                    self.logger.info(f"OCR Config 1 (original, psm 8): {text}")
            except:
                pass
            
            # Configuration 2: Grayscale
            try:
                gray = img.convert('L')
                text = pytesseract.image_to_string(
                    gray,
                    config='--psm 8 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                ).strip()
                if text and len(text) >= 4:
                    results.append(text)
                    self.logger.info(f"OCR Config 2 (grayscale, psm 8): {text}")
            except:
                pass
            
            # Configuration 3: High contrast
            try:
                gray = img.convert('L')
                enhancer = ImageEnhance.Contrast(gray)
                high_contrast = enhancer.enhance(2.5)
                text = pytesseract.image_to_string(
                    high_contrast,
                    config='--psm 8 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                ).strip()
                if text and len(text) >= 4:
                    results.append(text)
                    self.logger.info(f"OCR Config 3 (high contrast, psm 8): {text}")
            except:
                pass
            
            # Configuration 4: Binary threshold
            try:
                gray = img.convert('L')
                binary = gray.point(lambda x: 255 if x > 140 else 0)
                text = pytesseract.image_to_string(
                    binary,
                    config='--psm 8 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                ).strip()
                if text and len(text) >= 4:
                    results.append(text)
                    self.logger.info(f"OCR Config 4 (binary threshold, psm 8): {text}")
            except:
                pass
            
            # Configuration 5: Sharpen image
            try:
                sharpened = img.filter(ImageFilter.SHARPEN)
                text = pytesseract.image_to_string(
                    sharpened,
                    config='--psm 8 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                ).strip()
                if text and len(text) >= 4:
                    results.append(text)
                    self.logger.info(f"OCR Config 5 (sharpened, psm 8): {text}")
            except:
                pass
            
            # Configuration 6: PSM 7 (single line)
            try:
                gray = img.convert('L')
                enhancer = ImageEnhance.Contrast(gray)
                high_contrast = enhancer.enhance(2.0)
                text = pytesseract.image_to_string(
                    high_contrast,
                    config='--psm 7 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                ).strip()
                if text and len(text) >= 4:
                    results.append(text)
                    self.logger.info(f"OCR Config 6 (high contrast, psm 7): {text}")
            except:
                pass
            
            if results:
                # Use voting - most common result
                counter = Counter(results)
                most_common = counter.most_common(1)[0]
                captcha_text = most_common[0]
                confidence = most_common[1] / len(results) * 100
                
                self.logger.info(f"OCR FINAL RESULT: '{captcha_text}' (confidence: {confidence:.1f}%, {most_common[1]}/{len(results)} votes)")
                return captcha_text
            else:
                self.logger.warning("OCR could not extract text from captcha with any configuration")
                return None
                
        except ImportError:
            self.logger.warning("pytesseract not installed. Install with: pip install pytesseract")
            self.logger.warning("Also install Tesseract-OCR on your system")
            return None
        except Exception as e:
            self.logger.error(f"Error solving captcha: {e}")
            return None
    
    def submit_form(self, response, captcha_text):
        """
        Submit the search form with license plate, vehicle type, and captcha via AJAX
        
        Args:
            response: Original response object
            captcha_text: Solved captcha text
        """
        self.logger.info(f"Submitting AJAX request with license_plate={self.license_plate}, vehicle_type={self.vehicle_type}, captcha={captcha_text}")
        
        # Map vehicle types to form values
        vehicle_type_map = {
            'oto': '1',
            'xemay': '2',
            'xedapdien': '3',
            'car': '1',
            'motorcycle': '2',
            'electric_bike': '3'
        }
        
        vehicle_type_value = vehicle_type_map.get(self.vehicle_type.lower(), '1')
        
        # Prepare AJAX data (matching the actual form submission)
        # Note: cUrl should be the current page URL, ipClient can be empty or an IP
        formdata = {
            'BienKS': self.license_plate.upper(),  # Biển kiểm soát
            'Xe': vehicle_type_value,              # Loại phương tiện (1=oto, 2=xemay, 3=xedapdien)
            'captcha': captcha_text,               # Mã bảo mật
            'ipClient': '0.0.0.0',                 # IP client (use placeholder)
            'cUrl': response.url,                  # Current page URL (the page we're on)
        }
        
        # Submit AJAX request to the correct endpoint
        ajax_url = response.urljoin('/?mod=contact&task=tracuu_post&ajax')
        
        # Log the request details
        self.logger.info(f"Submitting to: {ajax_url}")
        self.logger.info(f"Form data: {formdata}")
        
        # Log cookies being sent
        self.logger.info(f"Response URL we're submitting from: {response.url}")
        self.logger.info(f"Cookie jar ID: {response.meta.get('cookiejar', 'default')}")
        
        yield scrapy.FormRequest(
            url=ajax_url,
            formdata=formdata,
            callback=self.parse_ajax_response,
            dont_filter=True,
            method='POST',
            headers={
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': response.url,  # Important: include referer
            },
            meta={
                'license_plate': self.license_plate, 
                'vehicle_type': self.vehicle_type,
                'cookiejar': 1,  # Use the same cookie jar as before
            }
        )
    
    def parse_ajax_response(self, response):
        """Parse the AJAX JSON response and follow redirect URL"""
        self.logger.info(f"Parsing AJAX response from: {response.url}")
        
        try:
            import json
            
            # The response might be text or JSON
            response_text = response.text.strip()
            self.logger.info(f"AJAX Response: {response_text}")
            
            # Check if it's an error response
            if response_text == '404':
                self.retry_count += 1
                self.logger.error(f"Captcha verification failed! (Error 404) - Attempt {self.retry_count}/{self.max_retries}")
                
                # Retry if we haven't exceeded max retries
                if self.retry_count < self.max_retries:
                    self.logger.info(f"Retrying... Getting new captcha (attempt {self.retry_count + 1})")
                    # Start over from the beginning
                    yield scrapy.Request(
                        url=self.start_urls[0],
                        callback=self.parse,
                        meta={'cookiejar': response.meta.get('cookiejar', 1)},
                        dont_filter=True,
                        priority=10
                    )
                    return
                else:
                    self.logger.error(f"Max retries ({self.max_retries}) exceeded. Giving up.")
                    item = ViolationItem()
                    item['license_plate'] = response.meta.get('license_plate', self.license_plate)
                    item['vehicle_type'] = response.meta.get('vehicle_type', self.vehicle_type)
                    item['url'] = response.url
                    item['scraped_at'] = datetime.now().isoformat()
                    item['violation_found'] = False
                    item['status'] = 'error'
                    item['error_message'] = f'Captcha verification failed after {self.max_retries} attempts'
                    yield item
                    return
            
            # Try to parse JSON response
            try:
                # Clean up any extra whitespace
                response_text = response_text.replace('\n', '').replace('\r', '').strip()
                result = json.loads(response_text)
                
                if result.get('success'):
                    # Get the redirect URL
                    redirect_url = result.get('href')
                    if redirect_url:
                        self.logger.info(f"Following redirect to: {redirect_url}")
                        # Follow the redirect URL to get actual results
                        yield scrapy.Request(
                            url=response.urljoin(redirect_url),
                            callback=self.parse_results,
                            dont_filter=True,
                            meta={
                                'license_plate': response.meta.get('license_plate'),
                                'vehicle_type': response.meta.get('vehicle_type'),
                                'cookiejar': 1,  # Continue using same cookie jar
                            }
                        )
                    else:
                        self.logger.error("No redirect URL in success response")
                else:
                    self.logger.error("AJAX request was not successful")
                    self.logger.error(f"Response: {response_text}")
                    
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse JSON response: {e}")
                self.logger.error(f"Response text: {response_text}")
                
        except Exception as e:
            self.logger.error(f"Error parsing AJAX response: {e}")
    
    def parse_results(self, response):
        """Parse the search results page with actual violation data"""
        self.logger.info(f"Parsing results page: {response.url}")
        
        # Create item to store results
        item = ViolationItem()
        item['license_plate'] = response.meta.get('license_plate', self.license_plate)
        item['vehicle_type'] = response.meta.get('vehicle_type', self.vehicle_type)
        item['url'] = response.url
        item['scraped_at'] = datetime.now().isoformat()
        
        # Check for "No results found" or "Không tìm thấy kết quả"
        page_text = response.text.lower()
        if 'không tìm thấy kết quả' in page_text or 'no results' in page_text:
            self.logger.info("No violations found for this license plate")
            item['violation_found'] = False
            item['violation_details'] = []
            item['status'] = 'success'
            yield item
            return
        
        # Extract violation details from the structured data
        # The structure is: <label>Field:</label> followed by <div class="col-md-9">Value</div>
        violation = {}
        
        # Extract license plate
        license_match = response.xpath('//label[contains(.//span/text(), "Biển kiểm soát:")]/following-sibling::div[@class="col-md-9"]/text()').get()
        if license_match:
            violation['license_plate'] = license_match.strip()
            self.logger.info(f"Found license plate: {violation['license_plate']}")
        
        # Extract vehicle color
        color_match = response.xpath('//label[contains(.//span/text(), "Màu biển:")]/following-sibling::div[@class="col-md-9"]/text()').get()
        if color_match:
            violation['vehicle_color'] = color_match.strip()
            self.logger.info(f"Vehicle color: {violation['vehicle_color']}")
        
        # Extract vehicle type
        vehicle_type_match = response.xpath('//label[contains(.//span/text(), "Loại phương tiện:")]/following-sibling::div[@class="col-md-9"]/text()').get()
        if vehicle_type_match:
            violation['vehicle_type'] = vehicle_type_match.strip()
            self.logger.info(f"Vehicle type: {violation['vehicle_type']}")
        
        # Extract violation time
        time_match = response.xpath('//label[contains(.//span/text(), "Thời gian vi phạm")]/following-sibling::div[@class="col-md-9"]/text()').get()
        if time_match:
            violation['violation_time'] = time_match.strip()
            self.logger.info(f"Violation time: {violation['violation_time']}")
        
        # Extract violation location
        location_match = response.xpath('//label[contains(.//span/text(), "Địa điểm vi phạm:")]/following-sibling::div[@class="col-md-9"]/text()').get()
        if location_match:
            violation['violation_location'] = location_match.strip()
            self.logger.info(f"Violation location: {violation['violation_location']}")
        
        # Extract violation type/behavior
        behavior_match = response.xpath('//label[contains(.//span/text(), "Hành vi vi phạm:")]/following-sibling::div[@class="col-md-9"]/text()').get()
        if behavior_match:
            violation['violation_behavior'] = behavior_match.strip()
            self.logger.info(f"Violation behavior: {violation['violation_behavior']}")
        
        # Extract status (might be in a span with class)
        status_match = response.xpath('//label[contains(.//span/text(), "Trạng thái")]/following-sibling::div[@class="col-md-9"]//span/text()').get()
        if not status_match:
            status_match = response.xpath('//label[contains(.//span/text(), "Trạng thái")]/following-sibling::div[@class="col-md-9"]/text()').get()
        if status_match:
            violation['payment_status'] = status_match.strip()
            self.logger.info(f"Payment status: {violation['payment_status']}")
        
        # Extract unit that detected violation
        unit_match = response.xpath('//label[contains(.//span/text(), "Đơn vị phát hiện vi phạm:")]/following-sibling::div[@class="col-md-9"]/text()').get()
        if unit_match:
            violation['detecting_unit'] = unit_match.strip()
            self.logger.info(f"Detecting unit: {violation['detecting_unit']}")
        
        # Extract resolution location
        resolution_match = response.xpath('//label[contains(.//span/text(), "Nơi giải quyết vụ việc:")]/following-sibling::div[@class="col-md-9"]//text()').getall()
        if resolution_match:
            violation['resolution_location'] = ' '.join([t.strip() for t in resolution_match if t.strip()])
            self.logger.info(f"Resolution location: {violation['resolution_location']}")
        
        # Check if we found any violation data
        if violation:
            self.logger.info(f"Successfully extracted violation data: {len(violation)} fields")
            item['violation_found'] = True
            item['violation_details'] = [violation]  # List with one violation record
            item['status'] = 'success'
        else:
            # If no structured data found, save raw HTML for debugging
            self.logger.warning("Could not extract structured violation data, saving raw HTML")
            item['violation_found'] = False
            item['violation_details'] = []
            item['raw_html'] = response.text
            item['status'] = 'partial'
        
        yield item

