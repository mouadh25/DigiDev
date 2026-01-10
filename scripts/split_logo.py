import os
from PIL import Image

def split_logo(filename, output_prefix):
    path = os.path.join("public", filename)
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    img = Image.open(path).convert("RGBA")
    width, height = img.size
    
    # Get bounding box of content
    bbox = img.getbbox()
    if not bbox:
        print(f"Empty image: {filename}")
        return
        
    left, top, right, bottom = bbox
    
    # Scan for vertical gap
    # We sum alpha values for each row
    rows_with_content = []
    for y in range(top, bottom):
        has_content = False
        for x in range(left, right):
            pixel = img.getpixel((x, y))
            if pixel[3] > 0: # Alpha > 0
                has_content = True
                break
        if has_content:
            rows_with_content.append(y)
    
    if not rows_with_content:
        return

    # Find the largest gap in consecutive rows with content
    # This gap separates the Logo Symbol (top) from Text (bottom)
    largest_gap = 0
    split_y = -1
    
    # We look for a gap of at least, say, 10 pixels to be safe?
    # Or just the largest gap.
    
    last_y = rows_with_content[0]
    for y in rows_with_content:
        gap = y - last_y
        if gap > largest_gap:
            largest_gap = gap
            split_y = last_y + (gap // 2) # Middle of the gap
        last_y = y
        
    if split_y == -1 or largest_gap < 5:
        print(f"Vertical split failed for {filename} (Gap: {largest_gap}). Trying Horizontal split...")
        
        # Scan for horizontal gap (Vertical columns)
        cols_with_content = []
        for x in range(left, right):
            has_content = False
            for y in range(top, bottom):
                pixel = img.getpixel((x, y))
                if pixel[3] > 0:
                    has_content = True
                    break
            if has_content:
                cols_with_content.append(x)
        
        if not cols_with_content:
            return

        largest_x_gap = 0
        split_x = -1
        last_x = cols_with_content[0]
        for x in cols_with_content:
            gap = x - last_x
            if gap > largest_x_gap:
                largest_x_gap = gap
                split_x = last_x + (gap // 2)
            last_x = x
            
        if split_x != -1 and largest_x_gap > 5:
             print(f"Splitting {filename} horizontally at x={split_x} (Gap size: {largest_x_gap})")
             # Crop Symbol (Left)
             symbol_img = img.crop((0, 0, split_x, height))
             symbol_bbox = symbol_img.getbbox()
             if symbol_bbox:
                symbol_img = symbol_img.crop(symbol_bbox)
                symbol_out = os.path.join("public", f"{output_prefix}_symbol.png")
                symbol_img.save(symbol_out)
                print(f"Saved {symbol_out}")
             
             # Crop Text (Right)
             text_img = img.crop((split_x, 0, width, height))
             text_bbox = text_img.getbbox()
             if text_bbox:
                text_img = text_img.crop(text_bbox)
                text_out = os.path.join("public", f"{output_prefix}_text_graphic.png")
                text_img.save(text_out)
                print(f"Saved {text_out}")
             return

        print(f"Could not find a clear split in {filename}.")
        return

    print(f"Splitting {filename} vertically at y={split_y} (Gap size: {largest_gap})")
    
    # Crop Symbol (Top)
    # Refine top crop to just the content bounding box above split_y
    symbol_img = img.crop((0, 0, width, split_y))
    symbol_bbox = symbol_img.getbbox()
    if symbol_bbox:
        symbol_img = symbol_img.crop(symbol_bbox)
        symbol_out = os.path.join("public", f"{output_prefix}_symbol.png")
        symbol_img.save(symbol_out)
        print(f"Saved {symbol_out}")
        
    # Crop Text (Bottom)
    text_img = img.crop((0, split_y, width, height))
    text_bbox = text_img.getbbox()
    if text_bbox:
        text_img = text_img.crop(text_bbox)
        text_out = os.path.join("public", f"{output_prefix}_text_graphic.png")
        text_img.save(text_out)
        print(f"Saved {text_out}")

if __name__ == "__main__":
    split_logo("logo.png", "logo")
    split_logo("logo_dark.png", "logo_dark")
