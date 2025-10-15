# OCR Improvements & Tips

## ✅ What We've Improved

### 1. **Multiple OCR Configurations (6 Methods)**
The spider now tries 6 different preprocessing methods:
- Original image
- Grayscale conversion
- High contrast enhancement (2.5x)
- Binary thresholding
- Image sharpening
- Alternative Tesseract PSM mode

### 2. **Voting System**
- All successful OCR results are collected
- The most common result wins
- Shows confidence percentage

### 3. **Automatic Retry**
- If captcha fails, automatically retries up to 3 times
- Each retry gets a fresh captcha
- Configurable retry limit

## 📊 Expected Improvements

- **Before**: ~50% success rate
- **After**: ~80-90% success rate (with voting + retry)

## 🎯 Usage Examples

### Standard Usage (3 retries)
```bash
scrapy crawl csgt -a license_plate=59C136047 -a vehicle_type=xemay -O results.json
```

### More Retries for Higher Success
```bash
scrapy crawl csgt -a license_plate=59C136047 -a vehicle_type=xemay -a max_retries=5 -O results.json
```

### Single Attempt (No Retry)
```bash
scrapy crawl csgt -a license_plate=59C136047 -a vehicle_type=xemay -a max_retries=1 -O results.json
```

## 📝 What You'll See in Logs

```
[csgt] INFO: OCR Config 1 (original, psm 8): 64pnvp
[csgt] INFO: OCR Config 2 (grayscale, psm 8): 64pnvp
[csgt] INFO: OCR Config 3 (high contrast, psm 8): 64pnvp
[csgt] INFO: OCR Config 4 (binary threshold, psm 8): 64pnvp
[csgt] INFO: OCR Config 5 (sharpened, psm 8): b4pnvp
[csgt] INFO: OCR Config 6 (high contrast, psm 7): 64pnvp
[csgt] INFO: OCR FINAL RESULT: '64pnvp' (confidence: 83.3%, 5/6 votes)
```

If captcha fails:
```
[csgt] ERROR: Captcha verification failed! (Error 404) - Attempt 1/3
[csgt] INFO: Retrying... Getting new captcha (attempt 2)
```

## 🚀 Further Improvements (Optional)

### Option 1: Use Manual Input (100% Accuracy)
```bash
python run_with_manual_captcha.py 59C136047 xemay
```

### Option 2: Use Paid Captcha Services
For production use, consider:
- **2Captcha** (~$3 per 1000 captchas)
- **Anti-Captcha** (~$2 per 1000 captchas)  
- **DeathByCaptcha** (~$1.39 per 1000 captchas)

Update `csgt_scraper/utils/captcha_solver.py` to integrate these services.

### Option 3: Train Custom OCR Model
For very high volume:
1. Collect ~1000 captcha images
2. Manually label them
3. Train a custom Tesseract or TensorFlow model
4. Can achieve 95%+ accuracy

## 💡 Tips for Best Results

1. **Increase Retries for Important Queries**
   ```bash
   scrapy crawl csgt -a license_plate=IMPORTANT123 -a max_retries=5
   ```

2. **Check Logs for Confidence**
   - High confidence (>80%): Very likely correct
   - Low confidence (50-70%): May fail
   - If all configs agree (100%): Almost certainly correct

3. **Manual Fallback**
   - If automated fails after retries, use manual mode
   - Check `captcha_images/` folder for saved images

4. **Batch Processing with Retry**
   - Modify `batch_scraper.py` to retry failed items
   - Keep failed plates in a separate list for manual processing

## 📈 Monitoring Success Rate

Add this to track your success rate:
```python
successes = 0
failures = 0

# After each scrape
if result['status'] == 'success':
    successes += 1
else:
    failures += 1

success_rate = successes / (successes + failures) * 100
print(f"Success Rate: {success_rate:.1f}%")
```

## 🐛 Troubleshooting

### Low Success Rate (<70%)
- Check if Tesseract is properly installed: `tesseract --version`
- Update Tesseract to latest version
- Try increasing `max_retries` to 5 or more

### All OCR Configs Fail
- Captcha images may have changed format
- Check saved images in `captcha_images/`
- May need to adjust thresholds or add new preprocessing

### Retry Not Working
- Check network connection
- Verify cookies are enabled
- Check logs for session errors

