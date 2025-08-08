"""
文档生成服务
处理Word和PDF文档生成
"""
import io
from typing import Dict, Any, Optional, List
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class DocumentGenerator:
    """文档生成器基类"""
    
    def __init__(self, font_paths: List[str] = None):
        self.font_paths = font_paths or []
    
    def _register_font(self, font_name: str, font_path: str) -> bool:
        """注册字体"""
        try:
            pdfmetrics.registerFont(TTFont(font_name, font_path))
            return True
        except Exception:
            return False


class WordGenerator(DocumentGenerator):
    """Word文档生成器"""
    
    def generate_document(self, content: str, filename: str, options: Dict[str, Any]) -> io.BytesIO:
        """生成Word文档"""
        doc = Document()
        
        # 页边距设置
        section = doc.sections[0]
        margins = options.get('margins', {})
        section.left_margin = Cm(margins.get('left', 2.5))
        section.right_margin = Cm(margins.get('right', 2.5))
        section.top_margin = Cm(margins.get('top', 2.5))
        section.bottom_margin = Cm(margins.get('bottom', 2.5))
        
        # 页眉设置
        header_text = options.get('header')
        if header_text:
            hdr = section.header.paragraphs[0]
            hdr.text = header_text
            hdr.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 页脚设置
        footer_text = options.get('footer')
        if footer_text:
            ftr = section.footer.paragraphs[0]
            ftr.text = footer_text
            ftr.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 标题设置
        title = options.get('title', '生成的文档')
        title_p = doc.add_heading(title, 0)
        title_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 标题字体设置
        title_font = options.get('titleFont', 'SimSun')
        title_size = options.get('titleSize', 18)
        for run in title_p.runs:
            run.font.name = title_font
            run.font.size = Pt(title_size)
            run._element.rPr.rFonts.set(qn('w:eastAsia'), title_font)
        
        # 正文段落设置
        body_font = options.get('font', 'SimSun')
        body_size = options.get('fontSize', 12)
        line_spacing = options.get('lineSpacing', 1.5)
        
        align_map = {
            'LEFT': WD_ALIGN_PARAGRAPH.LEFT,
            'CENTER': WD_ALIGN_PARAGRAPH.CENTER,
            'RIGHT': WD_ALIGN_PARAGRAPH.RIGHT,
            'JUSTIFY': WD_ALIGN_PARAGRAPH.JUSTIFY
        }
        align = align_map.get(options.get('align', 'LEFT').upper(), WD_ALIGN_PARAGRAPH.LEFT)
        
        # 添加正文内容
        for line in content.split('\\n'):
            if line.strip():
                p = doc.add_paragraph()
                p.paragraph_format.line_spacing = line_spacing
                p.paragraph_format.space_before = Pt(options.get('spaceBefore', 0))
                p.paragraph_format.space_after = Pt(options.get('spaceAfter', 6))
                p.paragraph_format.alignment = align
                
                run = p.add_run(line)
                run.font.name = body_font
                run.font.size = Pt(body_size)
                run._element.rPr.rFonts.set(qn('w:eastAsia'), body_font)
            else:
                doc.add_paragraph()
        
        # 表格设置
        table_conf = options.get('table')
        if table_conf and table_conf.get('data'):
            data_rows = table_conf.get('data', [])
            style = table_conf.get('style', 'Table Grid')
            
            if data_rows:
                table = doc.add_table(rows=len(data_rows), cols=len(data_rows[0]), style=style)
                table.autofit = False
                
                for i, row in enumerate(data_rows):
                    for j, val in enumerate(row):
                        cell = table.cell(i, j)
                        cell.text = str(val)
                        # 设置表格字体
                        for paragraph in cell.paragraphs:
                            for run in paragraph.runs:
                                run.font.name = body_font
                                run.font.size = Pt(table_conf.get('fontSize', 10))
                                run._element.rPr.rFonts.set(qn('w:eastAsia'), body_font)
        
        # 分页设置
        if options.get('pageBreak'):
            doc.add_page_break()
        
        # 保存到内存
        file_stream = io.BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)
        
        return file_stream


class PDFGenerator(DocumentGenerator):
    """PDF文档生成器"""
    
    def generate_document(self, content: str, filename: str, options: Dict[str, Any]) -> io.BytesIO:
        """生成PDF文档"""
        # 字体注册
        font_name = options.get('font', 'NotoSansCJKsc')
        font_path = options.get('fontPath', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
        
        # 尝试注册中文字体
        if not self._register_font(font_name, font_path):
            # 尝试其他字体路径
            for path in self.font_paths:
                if self._register_font(font_name, path):
                    break
            else:
                # 所有字体都失败时回退到内置字体
                font_name = 'Helvetica'
        
        buffer = io.BytesIO()
        
        # 页面设置
        page_size = A4 if options.get('pageSize', 'A4') == 'A4' else letter
        doc = SimpleDocTemplate(
            buffer,
            pagesize=page_size,
            leftMargin=cm * options.get('marginLeft', 2),
            rightMargin=cm * options.get('marginRight', 2),
            topMargin=cm * options.get('marginTop', 2.5),
            bottomMargin=cm * options.get('marginBottom', 2.5),
        )
        
        # 样式设置
        styles = getSampleStyleSheet()
        
        # 标题样式
        title_style = ParagraphStyle(
            'TitleCN',
            parent=styles['Title'],
            fontName=font_name,
            fontSize=options.get('titleSize', 18),
            alignment=TA_CENTER,
            spaceAfter=12
        )
        
        # 正文样式
        align_map = {
            'LEFT': TA_LEFT, 'CENTER': TA_CENTER,
            'RIGHT': TA_RIGHT, 'JUSTIFY': TA_JUSTIFY
        }
        body_style = ParagraphStyle(
            'BodyCN',
            parent=styles['BodyText'],
            fontName=font_name,
            fontSize=options.get('fontSize', 12),
            leading=options.get('leading', 18),
            alignment=align_map.get(options.get('align', 'LEFT').upper(), TA_LEFT),
            spaceAfter=6
        )
        
        # 构建文档内容
        story = []
        
        # 添加标题
        title = options.get('title', '生成的PDF文档')
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 12))
        
        # 添加正文内容
        for line in content.split('\\n'):
            if line.strip():
                story.append(Paragraph(line, body_style))
            else:
                story.append(Spacer(1, 6))
        
        # 添加表格
        table_conf = options.get('table')
        if table_conf and table_conf.get('data'):
            data_rows = table_conf.get('data', [])
            if data_rows:
                table_style = TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), font_name),
                    ('FONTSIZE', (0, 0), (-1, -1), table_conf.get('fontSize', 10)),
                    ('ALIGN', (0, 0), (-1, -1), table_conf.get('align', 'LEFT')),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ])
                
                t = Table(data_rows, style=table_style)
                story.append(Spacer(1, 12))
                story.append(t)
        
        # 分页设置
        if options.get('pageBreak'):
            story.append(PageBreak())
        
        # 页眉页脚处理函数
        def on_page(canvas_obj, doc_obj):
            canvas_obj.saveState()
            canvas_obj.setFont(font_name, 9)
            
            # 页眉
            header = options.get('header')
            if header:
                canvas_obj.drawString(doc_obj.leftMargin, page_size[1] - doc_obj.topMargin + 15, header)
            
            # 页脚
            footer = options.get('footer', f'第 {doc_obj.page} 页')
            canvas_obj.drawRightString(
                page_size[0] - doc_obj.rightMargin,
                doc_obj.bottomMargin - 15,
                footer
            )
            canvas_obj.restoreState()
        
        # 生成PDF
        doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
        
        buffer.seek(0)
        return buffer
