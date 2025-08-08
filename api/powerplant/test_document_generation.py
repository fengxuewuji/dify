#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文档生成API的排版功能
"""

import requests
import json

# API基础URL
BASE_URL = "http://localhost:6002"

def test_word_generation():
    """测试Word文档生成"""
    url = f"{BASE_URL}/generate/word"
    
    # 测试数据
    data = {
        "filename": "设备运行报告.docx",
        "content": "这是第一段内容，包含了设备运行的基本信息。\n\n这是第二段内容，描述了运行状态分析。\n\n这是第三段内容，提供了详细的数据解读。",
        "options": {
            "title": "设备运行周报",
            "titleFont": "SimSun",
            "titleSize": 20,
            "font": "SimSun", 
            "fontSize": 12,
            "lineSpacing": 1.5,
            "align": "JUSTIFY",
            "margins": {
                "left": 2.5,
                "right": 2.5, 
                "top": 2.5,
                "bottom": 2.5
            },
            "header": "机组四值 • 内部资料",
            "footer": "保密文档 - 请勿外传",
            "spaceBefore": 0,
            "spaceAfter": 6,
            "table": {
                "data": [
                    ["指标名称", "数值", "单位", "状态"],
                    ["锅炉效率", "92.5", "%", "正常"],
                    ["汽轮机效率", "89.3", "%", "正常"],
                    ["发电功率", "600", "MW", "满负荷"]
                ],
                "style": "Table Grid",
                "fontSize": 10
            }
        }
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        with open("/tmp/test_word.docx", "wb") as f:
            f.write(response.content)
        print("✅ Word文档生成成功！保存到 /tmp/test_word.docx")
    else:
        print(f"❌ Word文档生成失败: {response.text}")

def test_pdf_generation():
    """测试PDF文档生成"""
    url = f"{BASE_URL}/generate/pdf"
    
    # 测试数据
    data = {
        "filename": "设备运行报告.pdf",
        "content": "这是第一段内容，包含了设备运行的基本信息。\n\n这是第二段内容，描述了运行状态分析。\n\n这是第三段内容，提供了详细的数据解读和建议措施。",
        "options": {
            "title": "设备运行周报",
            "font": "NotoSansCJKsc",
            "fontPath": "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "fontSize": 12,
            "titleSize": 18,
            "leading": 18,
            "align": "LEFT",
            "pageSize": "A4",
            "marginLeft": 2,
            "marginRight": 2,
            "marginTop": 2.5,
            "marginBottom": 2.5,
            "header": "设备部 • 2025年度报告",
            "footer": "版权所有 © 发电厂",
            "table": {
                "data": [
                    ["指标名称", "数值", "单位", "状态"],
                    ["锅炉效率", "92.5", "%", "正常"],
                    ["汽轮机效率", "89.3", "%", "正常"],
                    ["发电功率", "600", "MW", "满负荷"],
                    ["排烟温度", "125", "℃", "正常"]
                ],
                "fontSize": 10,
                "align": "CENTER"
            }
        }
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        with open("/tmp/test_pdf.pdf", "wb") as f:
            f.write(response.content)
        print("✅ PDF文档生成成功！保存到 /tmp/test_pdf.pdf")
    else:
        print(f"❌ PDF文档生成失败: {response.text}")

def test_simple_generation():
    """测试简单文档生成（不带格式参数）"""
    # 简单Word
    word_data = {
        "filename": "简单文档.docx",
        "content": "这是一个简单的Word文档，使用默认格式。"
    }
    
    response = requests.post(f"{BASE_URL}/generate/word", json=word_data)
    if response.status_code == 200:
        with open("/tmp/simple_word.docx", "wb") as f:
            f.write(response.content)
        print("✅ 简单Word文档生成成功！")
    
    # 简单PDF
    pdf_data = {
        "filename": "简单文档.pdf", 
        "content": "这是一个简单的PDF文档，使用默认格式。"
    }
    
    response = requests.post(f"{BASE_URL}/generate/pdf", json=pdf_data)
    if response.status_code == 200:
        with open("/tmp/simple_pdf.pdf", "wb") as f:
            f.write(response.content)
        print("✅ 简单PDF文档生成成功！")

if __name__ == "__main__":
    print("🚀 开始测试文档生成API...")
    
    print("\n📄 测试简单文档生成...")
    test_simple_generation()
    
    print("\n📝 测试Word文档高级格式...")
    test_word_generation()
    
    print("\n📋 测试PDF文档高级格式...")
    test_pdf_generation()
    
    print("\n✨ 测试完成！请检查 /tmp/ 目录下的生成文件。")
