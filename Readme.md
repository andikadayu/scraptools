# Information
Tools for Crawling Shopee Product

# Requirements
| Name                       | Version         |
| -------------------------- | --------------- |
| Python                     | 3.10.5 / latest |
| Chrome/Chromium            | build 103+      |
| Text Editor(Notepad++,etc) | any             |

# Installation
1. Install all requirements packages
   ```bash
    pip install -r requirements.txt
   ```
2. Launch App by open terminal/cmd
   ```bash
    python apps.py
   ```

# Configuration
1. Open settings.json on settings/settings.json using any Text Editor
2. Change the setting if you want
   ```json
    "version": "2.0",
    "delay_time": 3,
    "export_file_name": "shopee",
    "chromedriver_path": "./chromedriver",
    "lang": "en"
   ```
   1. version 
      1. 1.0 for export link of product (txt file)
      2. 2.0 for export data of product (json file)
   2. delay time for delay each crawling times 3 (ex 3 = 9 seconds)
   3. export file name for change the name of file export
   4. chromedriverpath for specify path of chromedriver location
   5. lang for setting language apps

# How to Use
1. Lauch App first
2. Insert a multiple link shop id separate by comma
    ```
    https://shopee.co.id/fengyadiaoju1.id
    ```
3. click button process and wait
4. the result on exports folder