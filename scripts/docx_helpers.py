import os
import sys
import re
import xml.sax.saxutils
import docx
from docx.shared import Cm, Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Thiết lập padding cho ô trong bảng (đơn vị dxa: 20 dxa = 1 pt)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex="FFFFFF"):
    """Tô màu nền cho ô trong bảng (mặc định nền trắng thuần khiết FFFFFF)."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_table_borders(table, color="000000", sz="4"):
    """Đặt đường viền mỏng đen trang trọng cho bảng chữ đen nền trắng."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def set_transparent_borders(table):
    """Đặt bảng hoàn toàn trong suốt không viền (dùng cho thông tin bìa)."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="none"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def make_table_robust(table):
    """Ngăn vỡ dòng giữa các trang và lặp lại tiêu đề bảng ở đầu trang mới."""
    for i, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if i == 0:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

def add_cover_page_border(section):
    """Thêm khung viền trang bìa đôi trang trọng cho duy nhất trang bìa đầu tiên."""
    sectPr = section._sectPr
    pgBorders = parse_xml(
        r'<w:pgBorders %s w:offsetFrom="page" w:display="firstPage">'
        r'<w:top w:val="double" w:sz="18" w:space="24" w:color="000000"/>'
        r'<w:left w:val="double" w:sz="18" w:space="24" w:color="000000"/>'
        r'<w:bottom w:val="double" w:sz="18" w:space="24" w:color="000000"/>'
        r'<w:right w:val="double" w:sz="18" w:space="24" w:color="000000"/>'
        r'</w:pgBorders>' % nsdecls('w')
    )
    sectPr.append(pgBorders)

def add_footer_page_number(run):
    """Chèn trường mã số trang PAGE chuẩn Word OpenXML (chỉ hiển thị số trang)."""
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

# =============================================================================
# BOOKMARK & HYPERLINK HELPERS CHO MỤC LỤC VÀ TÀI LIỆU THAM KHẢO
# =============================================================================
_bm_id_counter = 0

def add_bookmark(paragraph, name):
    """Thêm Bookmark OpenXML vào paragraph để phục vụ liên kết nội bộ trong Word."""
    global _bm_id_counter
    _bm_id_counter += 1
    bm_id = str(_bm_id_counter)
    bm_start = parse_xml(f'<w:bookmarkStart {nsdecls("w")} w:id="{bm_id}" w:name="{name}"/>')
    bm_end = parse_xml(f'<w:bookmarkEnd {nsdecls("w")} w:id="{bm_id}"/>')
    paragraph._p.insert(0, bm_start)
    paragraph._p.append(bm_end)

def get_bookmark_name(text):
    """Ánh xạ tiêu đề chương mục, hình vẽ, bảng biểu sang tên Bookmark chuẩn."""
    text_clean = text.strip()
    if "PHẦN 1" in text_clean: return "part1"
    if "PHẦN 2" in text_clean: return "part2"
    if "PHẦN 3" in text_clean: return "part3"
    if "PHẦN 4" in text_clean: return "part4"
    if "PHẦN 5" in text_clean: return "part5"
    if "PHẦN 6" in text_clean: return "part6"
    if "TÀI LIỆU THAM KHẢO" in text_clean: return "references"
    if "XÁC NHẬN HOÀN THÀNH" in text_clean or "IV. XÁC NHẬN" in text_clean: return "confirmation"
    if "THÔNG TIN SINH VIÊN" in text_clean: return "info_tttn06"
    if "LỜI CẢM ƠN" in text_clean: return "ack"
    if "DANH MỤC CÁC TỪ VIẾT TẮT" in text_clean: return "abbreviations"
    if "DANH MỤC HÌNH VẼ" in text_clean: return "fig_list"
    if "DANH MỤC BẢNG BIỂU" in text_clean: return "tbl_list"
    if "MỤC LỤC" in text_clean: return "toc"

    m3 = re.search(r"(\d+)\.(\d+)\.(\d+)", text_clean)
    if m3:
        return f"sec{m3.group(1)}_{m3.group(2)}_{m3.group(3)}"
    m2 = re.search(r"(\d+)\.(\d+)", text_clean)
    if m2:
        return f"sec{m2.group(1)}_{m2.group(2)}"
    mf = re.search(r"Hình\s+(\d+)\.(\d+)", text_clean)
    if mf:
        return f"fig{mf.group(1)}_{mf.group(2)}"
    mt = re.search(r"Bảng\s+(\d+)(?:\.(\d+))?", text_clean)
    if mt:
        if mt.group(2):
            return f"tbl{mt.group(1)}_{mt.group(2)}"
        return f"tbl{mt.group(1)}"
    return None

def add_hyperlink_tab_entry(doc, label, page_str, bookmark_name, is_bold=False):
    """
    Thêm một dòng trong Mục lục / Danh mục có:
    - Tab Stop lề phải 16.0cm với dấu chấm dẫn hàng (Dot Leader).
    - Toàn bộ dòng được bọc trong Hyperlink nội bộ w:anchor trỏ tới bookmark,
      cho phép người đọc bấm chuột (Ctrl+Click / Click) nhảy trực tiếp đến trang đó.
    """
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.tab_stops.add_tab_stop(Cm(16.0), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)

    escaped_label = xml.sax.saxutils.escape(label)
    bold_xml = "<w:b/>" if is_bold else ""
    hl_xml = f"""
    <w:hyperlink {nsdecls("w")} w:anchor="{bookmark_name}" w:history="1">
        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
                <w:sz w:val="22"/>
                <w:color w:val="000000"/>
                {bold_xml}
            </w:rPr>
            <w:t xml:space="preserve">{escaped_label}</w:t>
        </w:r>
        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
                <w:sz w:val="22"/>
                <w:color w:val="000000"/>
                {bold_xml}
            </w:rPr>
            <w:tab/>
            <w:t>{page_str}</w:t>
        </w:r>
    </w:hyperlink>
    """
    p._p.append(parse_xml(hl_xml))
    return p

def add_external_hyperlink(paragraph, url, text, color="000000", underline=True):
    """Thêm liên kết mạng URL ngoài có thể bấm được trong tài liệu Word."""
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    u_xml = '<w:u w:val="single"/>' if underline else ''
    escaped_text = xml.sax.saxutils.escape(text)
    hl_xml = f"""
    <w:hyperlink {nsdecls("w", "r")} r:id="{r_id}">
        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
                <w:sz w:val="22"/>
                <w:color w:val="{color}"/>
                {u_xml}
            </w:rPr>
            <w:t>{escaped_text}</w:t>
        </w:r>
    </w:hyperlink>
    """
    paragraph._p.append(parse_xml(hl_xml))

print("Enhanced docx_helpers with bookmarks, clickable TOC and external hyperlinks loaded successfully.")
