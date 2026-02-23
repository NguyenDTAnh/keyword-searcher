import os
import glob
import re
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

dest_dir = "/Users/dognnguyen/Sites/keyword-searcher/destination"
md_files = glob.glob(os.path.join(dest_dir, "*.md"))

# === Hàm xử lý KD/Comp: bỏ prefix Planner, chuyển tiếng Anh -> tiếng Việt ===
def clean_kd_comp(val):
    v = str(val).lower().strip()
    if 'low' in v: return 'Thấp'
    if 'medium' in v: return 'Trung bình'
    if 'high' in v: return 'Cao'
    if 'trung bình' in v: return 'Trung bình'
    if 'không xác định' in v: return 'Không xác định'
    if 'cao' in v: return 'Cao'
    if 'thấp' in v: return 'Thấp'
    return val

# === Format bid sang VNĐ ===
def format_vnd(val):
    v_str = str(val).strip()
    if v_str == '0' or v_str.lower() in ['n/a', 'nan', 'none', '', '--']:
        return '0 VNĐ'
    try:
        v_int = int(v_str.replace(',', ''))
        return f"{v_int:,}".replace(",", ".") + " VNĐ"
    except:
        pass
    try:
        v_int = int(v_str.replace('.', ''))
        return f"{v_int:,}".replace(",", ".") + " VNĐ"
    except:
        return val

# === Xoá markdown formatting ===
def clean_md(text):
    text = text.replace('**', '')
    text = re.sub(r'`([^`]*)`', r'\1', text)
    text = text.strip()
    return text

# === Parse bảng markdown thành list of dicts ===
def parse_md_table(text, section_marker):
    lines = text.split('\n')
    in_section = False
    table_lines = []
    for line in lines:
        if line.startswith('## '):
            if section_marker in line:
                in_section = True
                continue
            elif in_section:
                break
        if in_section and line.strip().startswith('|'):
            table_lines.append(line.strip())
    if len(table_lines) < 3:
        return [], []
    headers = [col.strip() for col in table_lines[0].strip('|').split('|')]
    data = []
    for line in table_lines[2:]:
        row = [clean_md(col.strip()) for col in line.strip('|').split('|')]
        data.append(row)
    return headers, data

# === Parse phần tổng quan ===
def parse_overview(text):
    lines = text.split('\n')
    result = []
    in_tq = False
    for line in lines:
        if line.startswith('## 1.'):
            in_tq = True
            continue
        elif line.startswith('## 2.'):
            break
        if in_tq and line.strip():
            result.append(clean_md(line))
    return result

# === Lấy tên report từ dòng đầu tiên ===
def get_report_title(text):
    first_line = text.split('\n')[0]
    return clean_md(first_line.replace('# ', ''))

# === Style definitions ===
TITLE_FONT = Font(name='Arial', size=14, bold=True, color='FFFFFF')
TITLE_FILL = PatternFill(start_color='1F4E79', end_color='1F4E79', fill_type='solid')
SECTION_FONT = Font(name='Arial', size=12, bold=True, color='1F4E79')
HEADER_FONT = Font(name='Arial', size=10, bold=True, color='FFFFFF')
HEADER_FILL_A = PatternFill(start_color='2E75B6', end_color='2E75B6', fill_type='solid')
HEADER_FILL_B = PatternFill(start_color='548235', end_color='548235', fill_type='solid')
OVERVIEW_FONT = Font(name='Arial', size=10)
DATA_FONT = Font(name='Arial', size=10)
THIN_BORDER = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)
EVEN_ROW_FILL = PatternFill(start_color='F2F2F2', end_color='F2F2F2', fill_type='solid')

# === Cột cho Group A và Group B ===
COLS_A = ['STT', 'cluster', 'cluster type', 'keyword', 'intent', 'impression', 'clicks', 'source']
COLS_A_IDX = {'STT': 0, 'Cluster': 1, 'Cluster Type': 2, 'Keyword': 3, 'Intent': 4, 'Imp': 5, 'Clicks': 6, 'Source': 7}

COLS_B = ['STT', 'cluster', 'cluster type', 'keyword', 'intent', 'vol', 'YoY', 'KD/comp', 'bid (high)']
COLS_B_IDX = {'STT': 0, 'Cluster': 1, 'Cluster Type': 2, 'Keyword': 3, 'Intent': 4, 'Vol': 5, 'YoY': 6, 'KD/Comp': 7, 'Bid (High)': 8}

# === Xử lý từng file ===
for md_file in md_files:
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            text = f.read()

        title = get_report_title(text)
        overview_lines = parse_overview(text)
        headers_a, data_a = parse_md_table(text, "## 3. NHÓM 1:")
        headers_b, data_b = parse_md_table(text, "## 4. NHÓM 2:")

        wb = Workbook()
        ws = wb.active
        ws.title = "Keyword Planner"

        # Tính max cột = 9 (số cột lớn nhất trong Group B)
        max_col = 9
        current_row = 1

        # ============================
        # PHẦN 1: TITLE + TỔNG QUAN
        # ============================
        # Title row - merge toàn bộ cột
        ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=max_col)
        cell = ws.cell(row=current_row, column=1, value=title)
        cell.font = TITLE_FONT
        cell.fill = TITLE_FILL
        cell.alignment = Alignment(horizontal='center', vertical='center')
        ws.row_dimensions[current_row].height = 30
        current_row += 1

        # Dòng trống
        current_row += 1

        # Section header: Tổng quan
        ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=max_col)
        cell = ws.cell(row=current_row, column=1, value="1. TỔNG QUAN BÁO CÁO")
        cell.font = SECTION_FONT
        current_row += 1

        # Nội dung tổng quan - mỗi dòng 1 row
        for line in overview_lines:
            ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=max_col)
            cell = ws.cell(row=current_row, column=1, value=line)
            cell.font = OVERVIEW_FONT
            cell.alignment = Alignment(wrap_text=True)
            current_row += 1

        # ============================
        # PHẦN 2: NHÓM TỪ KHOÁ A
        # ============================
        current_row += 1  # Dòng trống ngăn cách

        ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=max_col)
        cell = ws.cell(row=current_row, column=1, value="2. NHÓM TỪ KHOÁ A (TỪ KHOÁ CŨ - NATIVE)")
        cell.font = SECTION_FONT
        current_row += 1

        # Header row Group A
        for col_idx, col_name in enumerate(COLS_A, 1):
            cell = ws.cell(row=current_row, column=col_idx, value=col_name)
            cell.font = HEADER_FONT
            cell.fill = HEADER_FILL_A
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = THIN_BORDER
        current_row += 1

        # Data rows Group A
        for row_idx, row_data in enumerate(data_a):
            mapped = {}
            for h_name, h_idx in COLS_A_IDX.items():
                try:
                    pos = headers_a.index(h_name)
                    mapped[h_idx] = row_data[pos]
                except (ValueError, IndexError):
                    mapped[h_idx] = ''

            # Đổi source GSC
            if mapped.get(7, '') == 'data/google_search_console/Queries.csv':
                mapped[7] = 'GSC Vietgoing.com'

            for col_idx in range(len(COLS_A)):
                cell = ws.cell(row=current_row, column=col_idx + 1, value=mapped.get(col_idx, ''))
                cell.font = DATA_FONT
                cell.border = THIN_BORDER
                cell.alignment = Alignment(vertical='center')
                if row_idx % 2 == 1:
                    cell.fill = EVEN_ROW_FILL
            current_row += 1

        # ============================
        # PHẦN 3: NHÓM TỪ KHOÁ B
        # ============================
        current_row += 1  # Dòng trống ngăn cách

        ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=max_col)
        cell = ws.cell(row=current_row, column=1, value="3. NHÓM TỪ KHOÁ B (TỪ KHOÁ MỚI - MỞ RỘNG)")
        cell.font = SECTION_FONT
        current_row += 1

        # Header row Group B
        for col_idx, col_name in enumerate(COLS_B, 1):
            cell = ws.cell(row=current_row, column=col_idx, value=col_name)
            cell.font = HEADER_FONT
            cell.fill = HEADER_FILL_B
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = THIN_BORDER
        current_row += 1

        # Data rows Group B
        for row_idx, row_data in enumerate(data_b):
            mapped = {}
            for h_name, h_idx in COLS_B_IDX.items():
                try:
                    pos = headers_b.index(h_name)
                    mapped[h_idx] = row_data[pos]
                except (ValueError, IndexError):
                    mapped[h_idx] = ''

            # Clean KD/Comp
            if 7 in mapped:
                mapped[7] = clean_kd_comp(mapped[7])

            # Format VNĐ cho bid (high)
            if 8 in mapped:
                mapped[8] = format_vnd(mapped[8])

            for col_idx in range(len(COLS_B)):
                cell = ws.cell(row=current_row, column=col_idx + 1, value=mapped.get(col_idx, ''))
                cell.font = DATA_FONT
                cell.border = THIN_BORDER
                cell.alignment = Alignment(vertical='center')
                if row_idx % 2 == 1:
                    cell.fill = EVEN_ROW_FILL
            current_row += 1

        # ============================
        # AUTO-FIT COLUMN WIDTHS
        # ============================
        col_widths = {
            1: 6,    # STT
            2: 28,   # cluster
            3: 22,   # cluster type
            4: 40,   # keyword
            5: 24,   # intent
            6: 12,   # impression/vol
            7: 10,   # clicks/YoY
            8: 20,   # source/KD/comp
            9: 15,   # bid (high)
        }
        for col, width in col_widths.items():
            ws.column_dimensions[get_column_letter(col)].width = width

        # Freeze panes (không freeze vì layout phức tạp với nhiều section)
        # Lưu file
        xls_path = md_file.replace('.md', '.xlsx')
        wb.save(xls_path)
        print(f"DONE: {os.path.basename(md_file)} -> {os.path.basename(xls_path)}")

    except Exception as e:
        import traceback
        print(f"ERROR processing {os.path.basename(md_file)}:")
        traceback.print_exc()
