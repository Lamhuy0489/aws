#!/usr/bin/env python3
"""
scripts/annotate.py
Cong cu tu dong tim kiem vi tri phan tu tren anh chup man hinh AWS va dong khung vien do chuan xac.
Su dung Apple Vision OCR qua ocr.swift de xac dinh toa do pixel thuc te, tranh hoan toan loi lech toa do.
"""

import sys
import os
import json
import subprocess
import argparse
from PIL import Image, ImageDraw

RED_COLOR = (239, 68, 68)
DEFAULT_LINE_WIDTH = 6
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OCR_SWIFT = os.path.join(SCRIPT_DIR, "ocr.swift")

def run_ocr(image_path):
    """Goi ocr.swift va tra ve danh sach cac phan tu text kem toa do pixel: x, y, w, h."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Khong tim thay anh: {image_path}")
    
    cmd = ["swift", OCR_SWIFT, image_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Loi khi chay OCR: {result.stderr}")
    
    items = []
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            items.append(data)
        except json.JSONDecodeError:
            continue
    return items

def find_text_boxes(ocr_items, keywords, case_sensitive=False):
    """Tim kiem cac phan tu chua tu khoa."""
    matches = []
    for kw in keywords:
        kw_search = kw if case_sensitive else kw.lower()
        for item in ocr_items:
            text = item["text"] if case_sensitive else item["text"].lower()
            if kw_search in text:
                matches.append(item)
    return matches

def find_account_badge(ocr_items, width, height):
    """
    Tim kiem huy hieu tai khoan tren thanh dieu huong tren cung (thuong o goc tren ben phai).
    AWS Account ID (677994024390) hoac ten tai khoan (huylam).
    """
    candidates = []
    for item in ocr_items:
        text = item["text"].lower()
        # Nam o nua tren man hinh va lech phai
        if ("677994024390" in text or "huylam" in text) and item["y"] < height * 0.25 and item["x"] > width * 0.5:
            candidates.append(item)
    
    if not candidates:
        return None
    
    # Gop cac text o gan nhau tao thanh badge hoan chinh
    min_x = min(c["x"] for c in candidates)
    min_y = min(c["y"] for c in candidates)
    max_x = max(c["x"] + c["w"] for c in candidates)
    max_y = max(c["y"] + c["h"] for c in candidates)
    
    # Them padding cho badge dep mat
    pad_x = 16
    pad_y = 10
    return (
        max(0, min_x - pad_x),
        max(0, min_y - pad_y),
        min(width, max_x + pad_x),
        min(height, max_y + pad_y)
    )

def create_padded_box(x, y, w, h, pad_x=12, pad_y=8, max_w=None, max_h=None):
    """Tao hop bounding box co padding."""
    x1 = x - pad_x
    y1 = y - pad_y
    x2 = x + w + pad_x
    y2 = y + h + pad_y
    if max_w:
        x1 = max(0, x1)
        x2 = min(max_w, x2)
    if max_h:
        y1 = max(0, y1)
        y2 = min(max_h, y2)
    return (x1, y1, x2, y2)

def draw_boxes_on_image(image_path, boxes, output_path, line_width=DEFAULT_LINE_WIDTH, color=RED_COLOR):
    """Ve cac hop bounding box len anh va luu ra output_path."""
    im = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(im)
    for box in boxes:
        # box co the la tuple (x1, y1, x2, y2)
        draw.rectangle(box, outline=color, width=line_width)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    im.save(output_path, "PNG", optimize=True)
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Tool khoanh vien do chinh xac dua tren OCR")
    parser.add_argument("--image", required=True, help="Duong dan anh nguon can khoanh")
    parser.add_argument("--out", required=False, help="Duong dan anh ket qua (neu khong truyen se chi in OCR)")
    parser.add_argument("--ocr-only", action="store_true", help="Chi in ra danh sach OCR JSON")
    parser.add_argument("--badge", action="store_true", help="Tu dong tim va khoanh Account Badge goc tren phai")
    parser.add_argument("--find", nargs="+", help="Danh sach tu khoa can tim de khoanh hop")
    parser.add_argument("--pad-x", type=float, default=16, help="Padding truc X cho hop tim thay")
    parser.add_argument("--pad-y", type=float, default=10, help="Padding truc Y cho hop tim thay")
    parser.add_argument("--custom-box", action="append", nargs=4, type=float, metavar=('X1', 'Y1', 'X2', 'Y2'), help="Them hop tuy chinh (x1 y1 x2 y2)")
    
    args = parser.parse_args()
    
    print(f"Dang chay Apple Vision OCR tren: {args.image}...")
    ocr_items = run_ocr(args.image)
    
    im = Image.open(args.image)
    width, height = im.size
    print(f"Kich thuoc anh: {width} x {height} | Tim thay {len(ocr_items)} chuoi van ban.")
    
    if args.ocr_only:
        for item in ocr_items:
            print(f"  [x={item['x']:.1f}, y={item['y']:.1f}, w={item['w']:.1f}, h={item['h']:.1f}] -> {item['text']}")
        return
    
    boxes = []
    
    # 1. Tu dong khoanh badge tai khoan neu co co --badge
    if args.badge:
        badge_box = find_account_badge(ocr_items, width, height)
        if badge_box:
            boxes.append(badge_box)
            print(f"Da tim thay Account Badge tai: {badge_box}")
        else:
            print("Khong tim thay Account Badge theo tu khoa (677994024390 / huylam).")
            
    # 2. Tim theo tu khoa
    if args.find:
        for kw in args.find:
            matches = find_text_boxes(ocr_items, [kw])
            if matches:
                for m in matches:
                    b = create_padded_box(m["x"], m["y"], m["w"], m["h"], args.pad_x, args.pad_y, width, height)
                    boxes.append(b)
                    print(f"Khop tu khoa '{kw}': text='{m['text']}' tai box={b}")
            else:
                print(f"Canh bao: Khong tim thay tu khoa '{kw}' tren anh.")
                
    # 3. Hop tuy chinh
    if args.custom_box:
        for cb in args.custom_box:
            boxes.append(tuple(cb))
            print(f"Them hop tuy chinh: {cb}")
            
    if not boxes:
        print("Khong co hop nao de ve!")
        return
        
    if args.out:
        out = draw_boxes_on_image(args.image, boxes, args.out)
        print(f"Da ve thanh cong {len(boxes)} hop len: {out}")
    else:
        print(f"Cac hop xac dinh duoc ({len(boxes)} hop): {boxes}")

if __name__ == "__main__":
    main()
