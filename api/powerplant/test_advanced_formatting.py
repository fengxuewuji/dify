#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试段落级格式控制和编号功能
"""

import requests
import json

BASE_URL = "http://localhost:6002"

def test_advanced_word_formatting():
    """测试Word文档的高级段落格式"""
    url = f"{BASE_URL}/generate/word"
    
    data = {
        "filename": "高级格式文档.docx",
        "content": "",  # 使用paragraphs配置时content可为空
        "options": {
            "title": "设备技术文档",
            "titleFont": "SimSun",
            "titleSize": 20,
            "header": "技术部 • 内部文档",
            "footer": "机密资料 • 请勿外传",
            "margins": {"left": 3, "right": 3, "top": 2.5, "bottom": 2.5},
            
            # 段落级配置
            "paragraphs": [
                {
                    "content": "1. 概述",
                    "style": "heading", 
                    "level": 1,
                    "font": "SimHei",
                    "fontSize": 16
                },
                {
                    "content": "本文档描述了设备运行的技术规范和操作要求。文档内容包括设备参数、运行标准、维护要求等重要信息。",
                    "align": "JUSTIFY",
                    "fontSize": 12,
                    "lineSpacing": 1.5,
                    "spaceAfter": 12
                },
                {
                    "content": "1.1 设备基本信息",
                    "style": "heading",
                    "level": 2, 
                    "font": "SimHei",
                    "fontSize": 14
                },
                {
                    "content": "设备型号：XXX-2000",
                    "numbered": True,
                    "fontSize": 11,
                    "leftIndent": 1
                },
                {
                    "content": "额定功率：600MW",
                    "numbered": True,
                    "fontSize": 11,
                    "leftIndent": 1
                },
                {
                    "content": "投运日期：2020年12月",
                    "numbered": True,
                    "fontSize": 11,
                    "leftIndent": 1
                },
                {
                    "content": "2. 技术参数",
                    "style": "heading",
                    "level": 1,
                    "font": "SimHei",
                    "fontSize": 16
                },
                {
                    "content": "主要技术参数如下所列：",
                    "align": "JUSTIFY",
                    "fontSize": 12,
                    "spaceAfter": 6
                },
                {
                    "content": "锅炉效率 ≥ 92%",
                    "bulleted": True,
                    "fontSize": 11,
                    "color": "#2E7D32"
                },
                {
                    "content": "汽轮机效率 ≥ 89%",
                    "bulleted": True,
                    "fontSize": 11,
                    "color": "#2E7D32"
                },
                {
                    "content": "发电效率 ≥ 45%",
                    "bulleted": True,
                    "fontSize": 11,
                    "color": "#2E7D32"
                },
                {
                    "content": "3. 重要说明",
                    "style": "heading",
                    "level": 1,
                    "font": "SimHei",
                    "fontSize": 16
                },
                {
                    "content": "注意：本文档包含敏感技术信息，请严格按照保密规定执行。",
                    "align": "CENTER",
                    "fontSize": 12,
                    "bold": True,
                    "color": "#D32F2F",
                    "spaceBefore": 12,
                    "spaceAfter": 12
                }
            ]
        }
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        with open("/tmp/advanced_word.docx", "wb") as f:
            f.write(response.content)
        print("✅ 高级Word文档生成成功！保存到 /tmp/advanced_word.docx")
        print("   - 支持多级标题")
        print("   - 支持编号段落")
        print("   - 支持项目符号")
        print("   - 支持不同字体和颜色")
    else:
        print(f"❌ 高级Word文档生成失败: {response.text}")

def test_advanced_pdf_formatting():
    """测试PDF文档的高级段落格式"""
    url = f"{BASE_URL}/generate/pdf"
    
    data = {
        "filename": "高级格式文档.pdf",
        "content": "",
        "options": {
            "title": "设备运行分析报告",
            "font": "NotoSansCJKsc",
            "pageSize": "A4",
            "marginLeft": 2.5,
            "marginRight": 2.5,
            "header": "技术分析部 • 2025年报告",
            "footer": "第 {page} 页 • 保密文档",
            
            # 段落级配置
            "paragraphs": [
                {
                    "content": "一、执行摘要",
                    "style": "heading",
                    "level": 1,
                    "fontSize": 16,
                    "bold": True
                },
                {
                    "content": "本报告分析了设备在2025年第一季度的运行情况。通过数据分析和现场检查，设备整体运行状态良好，各项指标均在设计范围内。",
                    "align": "JUSTIFY",
                    "fontSize": 12,
                    "leading": 18,
                    "spaceAfter": 12
                },
                {
                    "content": "二、数据分析",
                    "style": "heading",
                    "level": 1,
                    "fontSize": 16,
                    "bold": True
                },
                {
                    "content": "2.1 效率分析",
                    "style": "heading",
                    "level": 2,
                    "fontSize": 14,
                    "spaceBefore": 8
                },
                {
                    "content": "锅炉效率达到92.5%，超过设计值0.5个百分点",
                    "numbered": True,
                    "fontSize": 11,
                    "leftIndent": 20
                },
                {
                    "content": "汽轮机效率为89.3%，处于正常运行范围",
                    "numbered": True,
                    "fontSize": 11,
                    "leftIndent": 20
                },
                {
                    "content": "综合发电效率达到45.2%，优于行业平均水平",
                    "numbered": True,
                    "fontSize": 11,
                    "leftIndent": 20
                },
                {
                    "content": "2.2 关键指标",
                    "style": "heading",
                    "level": 2,
                    "fontSize": 14,
                    "spaceBefore": 8
                },
                {
                    "content": "运行小时数：2160小时",
                    "bulleted": True,
                    "fontSize": 11,
                    "leftIndent": 20,
                    "color": "#1976D2"
                },
                {
                    "content": "平均负荷率：85.5%",
                    "bulleted": True,
                    "fontSize": 11,
                    "leftIndent": 20,
                    "color": "#1976D2"
                },
                {
                    "content": "非计划停机次数：0次",
                    "bulleted": True,
                    "fontSize": 11,
                    "leftIndent": 20,
                    "color": "#388E3C"
                },
                {
                    "content": "三、结论和建议",
                    "style": "heading",
                    "level": 1,
                    "fontSize": 16,
                    "bold": True
                },
                {
                    "content": "设备运行状态优良，建议继续保持当前运行模式。同时，需要关注以下几个方面的维护工作，确保设备长期稳定运行。",
                    "align": "JUSTIFY",
                    "fontSize": 12,
                    "leading": 18
                },
                {
                    "content": "重要提醒：本报告数据来源于自动监测系统，已通过人工核验。报告结论仅供内部决策参考。",
                    "align": "CENTER",
                    "fontSize": 10,
                    "italic": True,
                    "color": "#666666",
                    "spaceBefore": 20,
                    "spaceAfter": 10
                }
            ]
        }
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        with open("/tmp/advanced_pdf.pdf", "wb") as f:
            f.write(response.content)
        print("✅ 高级PDF文档生成成功！保存到 /tmp/advanced_pdf.pdf")
        print("   - 支持多级标题")
        print("   - 支持自动编号")
        print("   - 支持项目符号")
        print("   - 支持富文本格式（粗体、斜体、颜色）")
    else:
        print(f"❌ 高级PDF文档生成失败: {response.text}")

def test_mixed_format_document():
    """测试混合格式文档"""
    url = f"{BASE_URL}/generate/word"
    
    data = {
        "filename": "混合格式报告.docx",
        "content": "",
        "options": {
            "title": "设备巡检报告",
            "paragraphs": [
                {
                    "content": "检查日期：2025年8月8日",
                    "align": "RIGHT",
                    "fontSize": 10,
                    "italic": True
                },
                {
                    "content": "一、巡检概况",
                    "style": "heading",
                    "level": 1
                },
                {
                    "content": "本次巡检按照标准程序执行，检查了设备的各个关键部位。",
                    "fontSize": 12,
                    "firstLineIndent": 2
                },
                {
                    "content": "二、检查项目",
                    "style": "heading", 
                    "level": 1
                },
                {
                    "content": "主设备检查",
                    "numbered": True,
                    "bold": True,
                    "fontSize": 12
                },
                {
                    "content": "辅助设备检查", 
                    "numbered": True,
                    "bold": True,
                    "fontSize": 12
                },
                {
                    "content": "安全系统检查",
                    "numbered": True,
                    "bold": True,
                    "fontSize": 12
                },
                {
                    "content": "三、检查结果",
                    "style": "heading",
                    "level": 1
                },
                {
                    "content": "设备运行正常",
                    "bulleted": True,
                    "color": "#4CAF50",
                    "fontSize": 11
                },
                {
                    "content": "无异常声响",
                    "bulleted": True, 
                    "color": "#4CAF50",
                    "fontSize": 11
                },
                {
                    "content": "温度在正常范围",
                    "bulleted": True,
                    "color": "#4CAF50", 
                    "fontSize": 11
                },
                {
                    "content": "检查员：张三    审核员：李四",
                    "align": "RIGHT",
                    "fontSize": 10,
                    "spaceBefore": 20
                }
            ]
        }
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        with open("/tmp/mixed_format.docx", "wb") as f:
            f.write(response.content)
        print("✅ 混合格式文档生成成功！保存到 /tmp/mixed_format.docx")
    else:
        print(f"❌ 混合格式文档生成失败: {response.text}")

if __name__ == "__main__":
    print("🚀 开始测试高级段落格式功能...")
    
    print("\n📝 测试Word文档高级段落格式...")
    test_advanced_word_formatting()
    
    print("\n📋 测试PDF文档高级段落格式...")
    test_advanced_pdf_formatting()
    
    print("\n🎨 测试混合格式文档...")
    test_mixed_format_document()
    
    print("\n✨ 测试完成！请检查 /tmp/ 目录下的生成文件。")
