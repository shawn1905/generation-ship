#!/usr/bin/env python3
"""
generation-ship / 视觉资产工具：全网参考图以图搜图与出处溯源
用于在视觉资产构建、硬科幻飞船构型参考、三维模型/概念设计溯源时，检索图片的首发出处、作者与创作背景。
"""

import os
import io
import json
import argparse
import requests
from PIL import Image

SERPAPI_KEY = os.environ.get("SERPAPI_API_KEY", "")

def compress_image_if_needed(image_path: str, max_size_kb: int = 450) -> bytes:
    """压缩本地图片至 500KB 以内以满足 SerpApi /image 接口限制"""
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        quality = 85
        out_bytes = io.BytesIO()
        img.save(out_bytes, format="JPEG", quality=quality)
        while out_bytes.tell() > max_size_kb * 1024 and quality > 20:
            out_bytes = io.BytesIO()
            quality -= 15
            img.save(out_bytes, format="JPEG", quality=quality)
        return out_bytes.getvalue()

def trace_image(image_input: str, hl: str = "zh-cn") -> dict:
    """
    图片全网溯源入口：支持本地路径或网络 URL
    """
    endpoint = "https://serpapi.com/search.json"
    
    if image_input.startswith("http://") or image_input.startswith("https://"):
        params = {
            "engine": "google_lens",
            "url": image_input,
            "api_key": SERPAPI_KEY,
            "hl": hl
        }
        res = requests.get(endpoint, params=params, timeout=30)
        return res.json()
    else:
        upload_url = "https://serpapi.com/image"
        img_data = compress_image_if_needed(image_input)
        files = {"image": ("target_image.jpg", img_data, "image/jpeg")}
        params = {"api_key": SERPAPI_KEY}
        
        up_res = requests.post(upload_url, files=files, params=params, timeout=30)
        if up_res.status_code != 200:
            raise RuntimeError(f"图片上传失败: {up_res.status_code} - {up_res.text}")
            
        image_id = up_res.json().get("image_id")
        
        search_params = {
            "engine": "google_lens",
            "image_id": image_id,
            "api_key": SERPAPI_KEY,
            "hl": hl
        }
        search_res = requests.get(endpoint, params=search_params, timeout=30)
        return search_res.json()

def main():
    parser = argparse.ArgumentParser(description="世代飞船视觉资产溯源工具")
    parser.add_argument("image", help="本地图片路径或图片 URL")
    parser.add_argument("--output", "-o", help="结果保存的 JSON 文件路径", default=None)
    args = parser.parse_args()
    
    print(f"[*] 正在通过 Google Lens 检索图片: {args.image} ...")
    data = trace_image(args.image)
    
    if "visual_matches" in data:
        matches = data["visual_matches"]
        print(f"[+] 检索成功！共找到 {len(matches)} 个视觉匹配来源。")
        print("=" * 60)
        for idx, item in enumerate(matches[:8], 1):
            print(f"{idx}. [{item.get('source', 'Unknown')}] {item.get('title', 'No Title')}")
            print(f"   链接: {item.get('link')}")
            if item.get("image"):
                print(f"   原图: {item.get('image')}")
            print("-" * 60)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[+] 完整检索结果已保存至: {args.output}")

if __name__ == "__main__":
    main()
