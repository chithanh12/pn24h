"""
Captcha Solver Utility

This module provides various methods to solve captchas:
1. OCR using Tesseract
2. Manual input
3. Third-party API integration (placeholder)
"""

import os
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract


class CaptchaSolver:
    """Class to handle captcha solving using various methods"""
    
    def __init__(self, method='ocr'):
        """
        Initialize captcha solver
        
        Args:
            method: 'ocr', 'manual', or 'api'
        """
        self.method = method
    
    def solve(self, image_path):
        """
        Solve captcha using the configured method
        
        Args:
            image_path: Path to captcha image
            
        Returns:
            Captcha text
        """
        if self.method == 'ocr':
            return self.solve_with_ocr(image_path)
        elif self.method == 'manual':
            return self.solve_manually(image_path)
        elif self.method == 'api':
            return self.solve_with_api(image_path)
        else:
            raise ValueError(f"Unknown method: {self.method}")
    
    def preprocess_image(self, image_path):
        """
        Preprocess captcha image to improve OCR accuracy
        
        Args:
            image_path: Path to captcha image
            
        Returns:
            Preprocessed PIL Image
        """
        img = Image.open(image_path)
        
        # Convert to grayscale
        img = img.convert('L')
        
        # Increase contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
        
        # Apply threshold to get binary image
        threshold = 128
        img = img.point(lambda x: 255 if x > threshold else 0)
        
        # Apply filters to reduce noise
        img = img.filter(ImageFilter.MedianFilter(size=3))
        
        return img
    
    def solve_with_ocr(self, image_path):
        """
        Solve captcha using Tesseract OCR
        
        Args:
            image_path: Path to captcha image
            
        Returns:
            Captcha text or None if OCR fails
        """
        try:
            # Preprocess image
            img = self.preprocess_image(image_path)
            
            # Try different OCR configurations
            configs = [
                '--psm 8 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
                '--psm 7 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
                '--psm 6',
            ]
            
            for config in configs:
                text = pytesseract.image_to_string(img, config=config)
                text = text.strip()
                
                if text and len(text) >= 4:  # Assuming captcha is at least 4 characters
                    return text
            
            return None
            
        except Exception as e:
            print(f"OCR Error: {e}")
            return None
    
    def solve_manually(self, image_path):
        """
        Solve captcha by asking for manual input
        
        Args:
            image_path: Path to captcha image
            
        Returns:
            User-provided captcha text
        """
        print(f"\nCaptcha image saved at: {image_path}")
        print("Please open the image and enter the captcha text below.")
        
        # Try to open image in default viewer
        try:
            if os.name == 'nt':  # Windows
                os.startfile(image_path)
            elif os.name == 'posix':  # macOS and Linux
                os.system(f'open "{image_path}"' if os.uname().sysname == 'Darwin' else f'xdg-open "{image_path}"')
        except:
            pass
        
        captcha_text = input("Enter captcha text: ").strip()
        return captcha_text
    
    def solve_with_api(self, image_path):
        """
        Solve captcha using a third-party API service
        
        Note: This is a placeholder. You would need to implement
        integration with services like:
        - 2Captcha
        - Anti-Captcha
        - DeathByCaptcha
        
        Args:
            image_path: Path to captcha image
            
        Returns:
            Captcha text from API
        """
        raise NotImplementedError("API captcha solving not implemented yet")


def get_manual_captcha_input(image_path):
    """
    Helper function to get manual captcha input
    
    Args:
        image_path: Path to captcha image
        
    Returns:
        User-provided captcha text
    """
    solver = CaptchaSolver(method='manual')
    return solver.solve(image_path)


def solve_captcha_ocr(image_path):
    """
    Helper function to solve captcha using OCR
    
    Args:
        image_path: Path to captcha image
        
    Returns:
        OCR-detected captcha text
    """
    solver = CaptchaSolver(method='ocr')
    return solver.solve(image_path)

