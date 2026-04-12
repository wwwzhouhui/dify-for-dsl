#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发票申请单处理系统 - 完整增强版
基于LangGPT提示词专家的智能发票处理系统
支持多发票预览、数据导出、打印功能
"""

import gradio as gr
import json
import zipfile
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Tuple
import tempfile
import os
from datetime import datetime
import re

class EnhancedInvoiceProcessor:
    """增强版发票申请单处理器"""
    
    def __init__(self):
        self.current_applications = []
        self.processing_stats = {
            "total_files": 0,
            "total_invoices": 0,
            "total_items": 0,
            "total_amount": 0.0
        }
    
    def read_excel_data(self, file_path: str) -> List[List[str]]:
        """读取Excel文件数据"""
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_file:
                shared_strings = []
                try:
                    with zip_file.open('xl/sharedStrings.xml') as f:
                        tree = ET.parse(f)
                        root = tree.getroot()
                        for si in root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
                            t = si.find('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
                            if t is not None:
                                shared_strings.append(t.text)
                except Exception:
                    pass
                
                with zip_file.open('xl/worksheets/sheet1.xml') as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    
                    rows_data = []
                    rows = root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row')
                    for row in rows:
                        cells = row.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c')
                        row_data = []
                        for cell in cells:
                            v = cell.find('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                            if v is not None:
                                if cell.get('t') == 's':
                                    try:
                                        idx = int(v.text)
                                        if idx < len(shared_strings):
                                            row_data.append(shared_strings[idx])
                                        else:
                                            row_data.append(v.text)
                                    except Exception:
                                        row_data.append(v.text)
                                else:
                                    row_data.append(v.text)
                            else:
                                row_data.append('')
                        if any(row_data):
                            rows_data.append(row_data)
                    
                    return rows_data
                    
        except Exception as e:
            raise Exception(f"读取Excel文件时出错: {e}")
    
    def extract_invoice_applications(self, rows_data: List[List[str]]) -> List[Dict[str, Any]]:
        """从行数据中提取发票申请单信息"""
        applications = []
        current_app = None
        i = 0
        
        # 保存第一张发票的付款单位信息，用于补全后续发票
        first_invoice_payment_info = {
            "公司名称": "",
            "税务登记号": "",
            "地址电话": "",
            "开户行账号": ""
        }
        
        while i < len(rows_data):
            row = rows_data[i]
            
            if len(row) > 0 and row[0] == "发票申请单":
                if current_app:
                    applications.append(current_app)
                
                current_app = {
                    "id": len(applications) + 1,
                    "申请日期": "",
                    "申请人": "",
                    "发票类别": "",
                    "开票公司": "",
                    "付款单位": {
                        "公司名称": "",
                        "税务登记号": "",
                        "地址电话": "",
                        "开户行账号": ""
                    },
                    "商品明细": [],
                    "合计金额": 0.0,
                    "合计税额": 0.0,
                    "价税合计": 0.0,
                    "备注": "",
                    "状态": "待处理"
                }
                
                i += 1
                while i < len(rows_data):
                    row = rows_data[i]
                    
                    if len(row) > 6 and row[0] == "申请日期:":
                        if len(row) > 6:
                            current_app["申请人"] = row[6] if len(row) > 6 else ""
                    
                    elif len(row) > 6 and row[0] == "开票公司名称":
                        current_app["开票公司"] = row[1] if len(row) > 1 else ""
                        current_app["发票类别"] = row[6] if len(row) > 6 else ""
                    
                    elif len(row) > 5 and row[0] == "公司名称":
                        company_name = row[1] if len(row) > 1 else ""
                        tax_id = row[5] if len(row) > 5 else ""
                        
                        current_app["付款单位"]["公司名称"] = company_name
                        current_app["付款单位"]["税务登记号"] = tax_id
                        
                        # 保存第一张发票的信息
                        if len(applications) == 0:  # 这是第一张发票
                            first_invoice_payment_info["公司名称"] = company_name
                            first_invoice_payment_info["税务登记号"] = tax_id
                    
                    elif len(row) > 5 and row[0] == "地址及电话":
                        address_phone = row[1] if len(row) > 1 else ""
                        bank_account = row[5] if len(row) > 5 else ""
                        
                        current_app["付款单位"]["地址电话"] = address_phone
                        current_app["付款单位"]["开户行账号"] = bank_account
                        
                        # 保存第一张发票的信息
                        if len(applications) == 0:  # 这是第一张发票
                            first_invoice_payment_info["地址电话"] = address_phone
                            first_invoice_payment_info["开户行账号"] = bank_account
                    
                    elif len(row) > 7 and row[0] == "应税劳务名称":
                        i += 1
                        while i < len(rows_data):
                            row = rows_data[i]
                            
                            if len(row) > 0 and row[0] == "合计":
                                try:
                                    current_app["合计金额"] = float(row[5]) if len(row) > 5 and row[5] else 0.0
                                except Exception:
                                    pass
                                break
                            
                            if len(row) > 0 and row[0] == "发票申请单":
                                i -= 1
                                break
                            
                            if len(row) > 7 and row[0] and not row[0].startswith(("合计", "财务负责人", "开票日期", "注:")):
                                try:
                                    item = {
                                        "应税劳务名称": row[0] if len(row) > 0 else "",
                                        "规格型号": row[1] if len(row) > 1 else "",
                                        "单位": row[2] if len(row) > 2 else "",
                                        "数量": float(row[3]) if len(row) > 3 and row[3] else 0,
                                        "单价": float(row[4]) if len(row) > 4 and row[4] else 0,
                                        "金额": float(row[5]) if len(row) > 5 and row[5] else 0,
                                        "税率": float(row[6]) if len(row) > 6 and row[6] else 0,
                                        "税额": float(row[7]) if len(row) > 7 and row[7] else 0
                                    }
                                    current_app["商品明细"].append(item)
                                except (ValueError, IndexError):
                                    pass
                            
                            i += 1
                        break
                    
                    i += 1
                    
                    if i < len(rows_data) and len(rows_data[i]) > 0 and rows_data[i][0] == "发票申请单":
                        i -= 1
                        break
            
            i += 1
        
        if current_app:
            applications.append(current_app)
        
        # 补全缺失的付款单位信息
        if len(applications) > 1:
            for app in applications[1:]:  # 从第二张发票开始
                payment_info = app["付款单位"]
                
                # 检查并补全公司名称
                if not payment_info["公司名称"].strip():
                    payment_info["公司名称"] = first_invoice_payment_info["公司名称"]
                
                # 检查并补全税务登记号
                if not payment_info["税务登记号"].strip():
                    payment_info["税务登记号"] = first_invoice_payment_info["税务登记号"]
                
                # 检查并补全地址及电话
                if not payment_info["地址电话"].strip():
                    payment_info["地址电话"] = first_invoice_payment_info["地址电话"]
                
                # 检查并补全开户行及账号
                if not payment_info["开户行账号"].strip():
                    payment_info["开户行账号"] = first_invoice_payment_info["开户行账号"]
        
        # 计算合计信息和统计数据
        total_amount = 0
        total_items = 0
        
        for app in applications:
            app_total_amount = sum(item["金额"] for item in app["商品明细"])
            app_total_tax = sum(item["税额"] for item in app["商品明细"])
            app["合计金额"] = app_total_amount
            app["合计税额"] = app_total_tax
            app["价税合计"] = app_total_amount + app_total_tax
            
            total_amount += app["价税合计"]
            total_items += len(app["商品明细"])
        
        # 更新统计信息
        self.processing_stats.update({
            "total_files": self.processing_stats["total_files"] + 1,
            "total_invoices": len(applications),
            "total_items": total_items,
            "total_amount": total_amount
        })
        
        return applications
    
    def process_uploaded_file(self, file) -> Tuple[str, List[Dict], str]:
        """处理上传的Excel文件"""
        if file is None:
            return "请上传Excel文件", [], ""
        
        try:
            rows_data = self.read_excel_data(file.name)
            applications = self.extract_invoice_applications(rows_data)
            
            if not applications:
                return "未找到有效的发票申请单数据", [], ""
            
            self.current_applications = applications
            
            # 生成处理报告
            stats_report = f"""
            📊 **处理统计报告**
            
            - 📁 处理文件: {os.path.basename(file.name)}
            - 🧾 提取发票: {len(applications)} 张
            - 📦 商品明细: {self.processing_stats['total_items']} 项
            - 💰 总金额: ¥{self.processing_stats['total_amount']:,.2f}
            
            ✅ 处理完成，请查看右侧预览
            """
            
            result_msg = f"✅ 成功提取到 {len(applications)} 张发票申请单"
            return result_msg, applications, stats_report
            
        except Exception as e:
            return f"❌ 处理文件时出错: {str(e)}", [], ""

def format_item_name(name: str) -> Tuple[str, str]:
    """格式化应税劳务名称，提取分类和描述"""
    if '*' in name:
        parts = name.split('*')
        if len(parts) >= 3:
            category = parts[1]
            description = parts[2]
            return category, description
    return "", name

def create_enhanced_invoice_preview(applications: List[Dict]) -> str:
    """创建增强版发票预览HTML"""
    if not applications:
        return """
        <div class="no-data-message">
            <div class="no-data-icon">📄</div>
            <div>暂无发票数据</div>
            <div style="font-size: 14px; margin-top: 10px; opacity: 0.7;">请上传发票申请单文件</div>
        </div>
        """
    
    # 读取CSS样式
    css_content = ""
    try:
        with open("fapiaosqd.css", "r", encoding="utf-8") as f:
            css_content = f.read()
    except Exception:
        pass
    
    html_content = f"""
    <style>
    {css_content}
    </style>
    
    <div class="invoice-preview-container">
    """
    
    # 添加隐藏的radio按钮来控制切换
    if len(applications) > 1:
        for i, app in enumerate(applications):
            checked = "checked" if i == 0 else ""
            html_content += f'<input type="radio" id="invoice-radio-{i}" name="invoice-tabs" style="display: none;" {checked}>'
        
        # 添加发票选项卡
        html_content += '<div class="invoice-tabs">'
        for i, app in enumerate(applications):
            html_content += f'''
            <label for="invoice-radio-{i}" class="tab-button">
                发票 {i+1} - {app['发票类别']}
            </label>
            '''
        html_content += '</div>'
    
    # 添加发票卡片容器
    html_content += '<div class="invoice-cards">'
    
    # 生成每张发票的HTML
    for i, app in enumerate(applications):
        html_content += f'''
        <div class="invoice-card" id="invoice-{i}">
            <div class="invoice-header">
                增值税{app['发票类别']}
                <div class="invoice-number">No. {app['id']:04d}</div>
            </div>
            
            <div class="invoice-body">
                <div class="company-info-section">
                    <div class="company-info-card">
                        <div class="company-info-header">🏢 购买方信息</div>
                        <div class="company-info-content">
                            <div class="info-item">
                                <span class="info-label">名称:</span>
                                <span class="info-value">{app['付款单位']['公司名称']}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">税号:</span>
                                <span class="info-value">{app['付款单位']['税务登记号']}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">地址:</span>
                                <span class="info-value">{app['付款单位']['地址电话'][:80]}{'...' if len(app['付款单位']['地址电话']) > 80 else ''}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">账号:</span>
                                <span class="info-value">{app['付款单位']['开户行账号'][:50]}{'...' if len(app['付款单位']['开户行账号']) > 50 else ''}</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="company-info-card">
                        <div class="company-info-header">🏪 销售方信息</div>
                        <div class="company-info-content">
                            <div class="info-item">
                                <span class="info-label">名称:</span>
                                <span class="info-value">{app['开票公司']}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">申请人:</span>
                                <span class="info-value">{app['申请人']}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">日期:</span>
                                <span class="info-value">{app['申请日期'] or datetime.now().strftime('%Y-%m-%d')}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">状态:</span>
                                <span class="info-value">🟡 {app['状态']}</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="items-section">
                    <table class="items-table">
                        <thead>
                            <tr>
                                <th style="width: 25%;">货物或应税劳务、服务名称</th>
                                <th style="width: 12%;">规格型号</th>
                                <th style="width: 8%;">单位</th>
                                <th style="width: 8%;">数量</th>
                                <th style="width: 12%;">单价</th>
                                <th style="width: 12%;">金额</th>
                                <th style="width: 8%;">税率</th>
                                <th style="width: 12%;">税额</th>
                            </tr>
                        </thead>
                        <tbody>
        '''
        
        for item in app['商品明细']:
            category, description = format_item_name(item['应税劳务名称'])
            formatted_name = f'<span class="item-category">*{category}*</span>{description}' if category else item['应税劳务名称']
            
            html_content += f'''
                            <tr>
                                <td class="item-name">{formatted_name}</td>
                                <td>{item['规格型号']}</td>
                                <td>{item['单位']}</td>
                                <td>{item['数量']}</td>
                                <td>¥{item['单价']:,.2f}</td>
                                <td>¥{item['金额']:,.2f}</td>
                                <td>{item['税率']*100:.0f}%</td>
                                <td>¥{item['税额']:,.2f}</td>
                            </tr>
            '''
        
        html_content += f'''
                        </tbody>
                    </table>
                </div>
                
                <div class="total-section">
                    <div class="total-details">
                        <div class="total-item">
                            <div class="total-label">不含税金额</div>
                            <div class="total-value">¥{app['合计金额']:,.2f}</div>
                        </div>
                        <div class="total-item">
                            <div class="total-label">税额合计</div>
                            <div class="total-value">¥{app['合计税额']:,.2f}</div>
                        </div>
                    </div>
                    <div class="grand-total">
                        <div class="grand-total-label">价税合计</div>
                        <div class="grand-total-value">¥{app['价税合计']:,.2f}</div>
                    </div>
                </div>
                
                <div class="invoice-footer">
                    <div class="footer-item">
                        <div class="footer-label">👤 开票人</div>
                        <div class="footer-value">{app['申请人']}</div>
                    </div>
                    <div class="footer-item">
                        <div class="footer-label">✅ 复核人</div>
                        <div class="footer-value">待指定</div>
                    </div>
                    <div class="footer-item">
                        <div class="footer-label">💰 收款人</div>
                        <div class="footer-value">待指定</div>
                    </div>
                </div>
            </div>
        </div>
        '''
    
    # 关闭发票卡片容器
    html_content += '</div>'
    
    # 添加CSS控制的切换逻辑
    if len(applications) > 1:
        html_content += """
    <style>
    /* 默认隐藏所有发票卡片 */
    .invoice-card {
        display: none;
    }
    
    /* 显示选中的发票卡片 */"""
        
        for i in range(len(applications)):
            html_content += f"""
    #invoice-radio-{i}:checked ~ .invoice-cards #invoice-{i} {{
        display: block !important;
    }}
    #invoice-radio-{i}:checked ~ .invoice-tabs label[for="invoice-radio-{i}"] {{
        background: #3498db !important;
        color: white !important;
        border-color: #2980b9 !important;
    }}"""
        
        html_content += """
    </style>
    """
    
    html_content += """
    </div>
    """
    
    return html_content

def create_gradio_interface():
    """创建增强版Gradio界面"""
    processor = EnhancedInvoiceProcessor()
    
    def process_file_and_preview(file):
        """处理文件并生成预览"""
        if file is None:
            return (
                "请上传Excel文件", 
                "<div class='no-data-message'><div class='no-data-icon'>📄</div><div>请先上传发票申请单文件</div></div>",
                ""
            )
        
        message, applications, stats = processor.process_uploaded_file(file)
        preview_html = create_enhanced_invoice_preview(applications)
        
        return message, preview_html, stats
    
    def export_json_data():
        """导出JSON数据"""
        if not processor.current_applications:
            return None
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8')
        export_data = {
            "export_time": datetime.now().isoformat(),
            "statistics": processor.processing_stats,
            "invoices": processor.current_applications
        }
        json.dump(export_data, temp_file, ensure_ascii=False, indent=2)
        temp_file.close()
        
        return temp_file.name
    
    def reset_system():
        """重置系统"""
        processor.current_applications = []
        processor.processing_stats = {
            "total_files": 0,
            "total_invoices": 0,
            "total_items": 0,
            "total_amount": 0.0
        }
        return (
            "系统已重置",
            "<div class='no-data-message'><div class='no-data-icon'>🔄</div><div>系统已重置，请重新上传文件</div></div>",
            ""
        )
    
    # 创建Gradio界面
    with gr.Blocks(
        title="智能发票申请单处理系统",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1400px !important;
        }
        .upload-area {
            border: 2px dashed #3498db;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background: #f8f9fa;
        }
        """
    ) as demo:
        
        gr.Markdown("""
        # 🧾 智能发票申请单处理系统
        
        **基于LangGPT提示词专家的智能发票处理系统** | 支持多发票预览、数据导出、批量处理
        
        ---
        """)
        
        with gr.Row():
            # 左侧控制面板
            with gr.Column(scale=1, min_width=350):
                gr.Markdown("### 📁 文件上传与处理")
                
                file_upload = gr.File(
                    label="📤 上传发票申请单 (Excel格式)",
                    file_types=[".xlsx", ".xls"],
                    type="filepath",
                    elem_classes=["upload-area"]
                )
                
                with gr.Row():
                    process_btn = gr.Button("🔄 处理申请单", variant="primary", scale=2)
                    reset_btn = gr.Button("🔄 重置系统", variant="secondary", scale=1)
                
                status_output = gr.Textbox(
                    label="📊 处理状态",
                    placeholder="等待文件上传...",
                    interactive=False,
                    lines=2
                )
                
                gr.Markdown("### 📈 统计信息")
                stats_display = gr.Markdown("暂无统计数据")
                
                gr.Markdown("### 🛠️ 数据操作")
                
                with gr.Row():
                    export_btn = gr.Button("💾 导出数据", variant="secondary")
                    print_btn = gr.Button("🖨️ 打印预览", variant="secondary")
                
                download_file = gr.File(label="📥 下载文件", visible=False)
                
                gr.Markdown("""
                ### 📋 功能特点
                
                ✨ **智能提取**: 基于LangGPT提示词专家技术  
                📄 **多发票支持**: 一次处理多张申请单  
                🎯 **数据验证**: 自动验证金额和税额计算  
                📱 **响应式界面**: 适配各种屏幕尺寸  
                💾 **数据导出**: 支持JSON格式导出  
                🖨️ **打印友好**: 优化的打印样式  
                
                ### 📖 使用说明
                
                1. **上传文件**: 选择Excel格式的发票申请单
                2. **自动处理**: 系统自动提取和验证数据
                3. **预览发票**: 在右侧查看生成的发票预览
                4. **导出数据**: 可导出结构化的JSON数据
                5. **打印发票**: 支持打印预览功能
                """)
            
            # 右侧预览面板
            with gr.Column(scale=2):
                gr.Markdown("### 📋 发票预览")
                
                preview_html = gr.HTML(
                    value="<div class='no-data-message'><div class='no-data-icon'>📄</div><div>请先上传发票申请单文件</div></div>",
                    label="发票预览",
                    elem_id="invoice-preview"
                )
        
        # 事件绑定
        process_btn.click(
            fn=process_file_and_preview,
            inputs=[file_upload],
            outputs=[status_output, preview_html, stats_display]
        )
        
        reset_btn.click(
            fn=reset_system,
            outputs=[status_output, preview_html, stats_display]
        )
        
        export_btn.click(
            fn=export_json_data,
            outputs=[download_file]
        ).then(
            lambda: gr.update(visible=True),
            outputs=[download_file]
        )
        
        # 文件上传时自动处理
        file_upload.change(
            fn=process_file_and_preview,
            inputs=[file_upload],
            outputs=[status_output, preview_html, stats_display]
        )
        
        # 打印功能
        print_btn.click(
            fn=lambda: "请使用浏览器的打印功能 (Ctrl+P) 来打印发票预览",
            outputs=[status_output]
        )
    
    return demo

if __name__ == "__main__":
    print("🚀 启动智能发票申请单处理系统...")
    print("📍 系统特点:")
    print("   - 基于LangGPT提示词专家技术")
    print("   - 支持多发票预览和批量处理")
    print("   - 智能数据提取和验证")
    print("   - 响应式界面设计")
    print("   - 数据导出和打印功能")
    print()
    
    demo = create_gradio_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=15601,
        share=False,
        show_error=True
    )