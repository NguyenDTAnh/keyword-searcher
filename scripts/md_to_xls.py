#!/usr/bin/env python3
"""
Script chuyển đổi file Markdown keyword report sang Excel (.xlsx)
- Parse tất cả bảng markdown trong mỗi file
- Mỗi file .md -> 1 file .xlsx tương ứng
- Giữ nguyên cấu trúc: mỗi section (nhóm bảng) thành 1 sheet riêng
- Format đẹp: header bold, auto-width columns, màu sắc
"""

import os
import re
import glob
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter


def parse_markdown_tables(md_content):
    """
    Parse nội dung markdown, trích xuất các section và bảng tương ứng.
    Trả về list các dict: {title, headers, rows}
    """
    lines = md_content.split('\n')
    sections = []
    current_section_title = ""
    current_headers = None
    current_rows = []
    in_table = False

    for line in lines:
        stripped = line.strip()

        # Bắt section header (## hoặc ###)
        if stripped.startswith('## '):
            # Lưu section trước đó nếu có data
            if current_headers and current_rows:
                sections.append({
                    'title': sanitize_sheet_name(current_section_title),
                    'headers': current_headers,
                    'rows': current_rows
                })
            current_section_title = stripped.lstrip('#').strip()
            current_headers = None
            current_rows = []
            in_table = False
            continue

        # Phát hiện dòng bảng markdown (bắt đầu bằng |)
        if stripped.startswith('|') and stripped.endswith('|'):
            cells = [c.strip() for c in stripped.split('|')[1:-1]]

            # Bỏ qua dòng separator (| :--- | :--- |)
            if all(re.match(r'^:?-+:?$', c) for c in cells):
                continue

            # Dòng đầu tiên của bảng = headers
            if not in_table:
                current_headers = cells
                current_rows = []
                in_table = True
            else:
                # Làm sạch bold markers **text** -> text
                cleaned_cells = [re.sub(r'\*\*(.*?)\*\*', r'\1', c) for c in cells]
                current_rows.append(cleaned_cells)
        else:
            # Nếu ra khỏi bảng, lưu lại section
            if in_table and current_headers and current_rows:
                sections.append({
                    'title': sanitize_sheet_name(current_section_title),
                    'headers': current_headers,
                    'rows': current_rows
                })
                current_headers = None
                current_rows = []
            in_table = False

    # Lưu section cuối cùng
    if current_headers and current_rows:
        sections.append({
            'title': sanitize_sheet_name(current_section_title),
            'headers': current_headers,
            'rows': current_rows
        })

    return sections


def sanitize_sheet_name(name):
    """
    Excel sheet name có giới hạn 31 ký tự và không chứa ký tự đặc biệt.
    Cắt và làm sạch tên sheet.
    """
    invalid_chars = ['\\', '/', '*', '?', ':', '[', ']']
    for ch in invalid_chars:
        name = name.replace(ch, '')
    return name[:31] if name else "Sheet1"


def create_excel(sections, output_path, report_title=""):
    """
    Tạo file Excel từ danh sách sections đã parse.
    Mỗi section -> 1 sheet trong workbook.
    """
    wb = Workbook()
    wb.remove(wb.active)

    # Style definitions
    header_font = Font(name='Arial', bold=True, size=11, color='FFFFFF')
    header_fill = PatternFill(start_color='2E86AB', end_color='2E86AB', fill_type='solid')
    header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    data_font = Font(name='Arial', size=10)
    data_alignment = Alignment(vertical='center', wrap_text=True)

    even_fill = PatternFill(start_color='F0F8FF', end_color='F0F8FF', fill_type='solid')

    thin_border = Border(
        left=Side(style='thin', color='D3D3D3'),
        right=Side(style='thin', color='D3D3D3'),
        top=Side(style='thin', color='D3D3D3'),
        bottom=Side(style='thin', color='D3D3D3'),
    )

    for idx, section in enumerate(sections):
        title = section['title'] or f"Sheet{idx + 1}"
        sheet_names = [ws.title for ws in wb.worksheets]
        if title in sheet_names:
            title = f"{title[:28]}_{idx}"

        ws = wb.create_sheet(title=title)

        if report_title:
            ws.append([report_title])
            ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(section['headers']))
            title_cell = ws.cell(row=1, column=1)
            title_cell.font = Font(name='Arial', bold=True, size=14, color='1A1A2E')
            title_cell.alignment = Alignment(horizontal='center', vertical='center')
            ws.append([])

        start_row = ws.max_row + 1
        for col_idx, header in enumerate(section['headers'], 1):
            cell = ws.cell(row=start_row, column=col_idx, value=header)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
            cell.border = thin_border

        for row_idx, row_data in enumerate(section['rows']):
            current_row = start_row + row_idx + 1
            for col_idx, value in enumerate(row_data, 1):
                cell = ws.cell(row=current_row, column=col_idx, value=try_convert_number(value))
                cell.font = data_font
                cell.alignment = data_alignment
                cell.border = thin_border
                if row_idx % 2 == 0:
                    cell.fill = even_fill

        for col_idx in range(1, len(section['headers']) + 1):
            max_width = 0
            col_letter = get_column_letter(col_idx)
            for row in ws.iter_rows(min_col=col_idx, max_col=col_idx, min_row=start_row, max_row=ws.max_row):
                for cell in row:
                    if cell.value:
                        cell_len = len(str(cell.value))
                        max_width = max(max_width, cell_len)
            adjusted_width = min(max(max_width + 2, 10), 50)
            ws.column_dimensions[col_letter].width = adjusted_width

        ws.freeze_panes = ws.cell(row=start_row + 1, column=1)

    if not wb.worksheets:
        ws = wb.create_sheet(title="No Data")
        ws.append(["Không tìm thấy bảng dữ liệu trong file markdown"])

    wb.save(output_path)
    return output_path


def try_convert_number(value):
    if not value or not isinstance(value, str):
        return value
    cleaned = value.strip()
    if cleaned.endswith('%'):
        return cleaned
    if cleaned.upper() == 'N/A':
        return cleaned
    try:
        if re.match(r'^-?[\d,]+$', cleaned):
            return int(cleaned.replace(',', ''))
    except ValueError:
        pass
    try:
        if re.match(r'^-?[\d.]+$', cleaned):
            return float(cleaned)
    except ValueError:
        pass
    return value


def main():
    # Use absolute paths based on working directory
    base_dir = "/Users/dognnguyen/Sites/keyword-searcher"
    source_dir = os.path.join(base_dir, 'destination')
    output_dir = os.path.join(base_dir, 'destination_xls')

    os.makedirs(output_dir, exist_ok=True)
    md_files = glob.glob(os.path.join(source_dir, '*.md'))

    if not md_files:
        print("❌ Không tìm thấy file .md nào!")
        return

    for md_file in sorted(md_files):
        filename = os.path.basename(md_file)
        output_filename = filename.replace('.md', '.xlsx')
        output_path = os.path.join(output_dir, output_filename)

        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            report_title = title_match.group(1) if title_match else filename
            sections = parse_markdown_tables(content)
            if not sections: continue
            create_excel(sections, output_path, report_title)
            print(f"✅ {filename} -> {output_filename}")
        except Exception as e:
            print(f"❌ {filename}: {e}")

if __name__ == '__main__':
    main()
