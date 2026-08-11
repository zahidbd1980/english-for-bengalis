# Theme update failed — fixed files

Blogger "Update failed" was likely caused by unsafe edits (invalid height min, custom fonts in Variables, head link tags, @import).

## Try in this order

### 1) MINIMAL (সবচেয়ে নিরাপদ)
File: `themeCode-MINIMAL.txt`  
Change: শুধু PageList `visible='true'` (মেনু দেখানো)

### 2) SAFE (রঙ + মেনু CSS)
File: `themeCode-SAFE.txt` (same as updated `themeCode.txt`)  
Changes: teal colors + menu visible + small CSS  
No custom font Variables, no head `<link>`, no @import

## How to paste
1. Theme → Backup  
2. Edit HTML → select all → delete  
3. Paste **one** file → Save  

First use **themeCode-MINIMAL.txt**.  
If that saves, then try **themeCode-SAFE.txt**.

If MINIMAL also fails, the problem is paste/ truncation — paste from Notepad carefully, or use Theme → Restore upload if Blogger allows XML restore.
