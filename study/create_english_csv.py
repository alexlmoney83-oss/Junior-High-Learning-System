"""
读取所有英语教材PDF，提取单元信息，生成CSV导入文件
"""
import os
import sys
import re
from pathlib import Path
import pdfplumber

def extract_english_units(pdf_path):
    """
    从英语PDF提取单元信息
    英语教材的特点：目录页包含所有Unit信息
    """
    units = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # 读取前15页寻找单元信息
            for page_num in range(min(15, len(pdf.pages))):
                page = pdf.pages[page_num]
                text = page.extract_text()
                
                if not text:
                    continue
                
                # 如果这页包含"UNIT"或"Unit"关键词，可能是目录页
                if 'Unit' in text or 'UNIT' in text:
                    lines = text.split('\n')
                    
                    for i, line in enumerate(lines):
                        line_clean = line.strip()
                        
                        # 匹配 "Unit 1", "Unit 2", "1 " (后面跟单元名) 等格式
                        # 格式1: "Unit 1 Language Learning"
                        match1 = re.match(r'^Unit\s+(\d+)\s+(.+)$', line_clean, re.IGNORECASE)
                        # 格式2: "1 Language Learning" (数字开头)
                        match2 = re.match(r'^(\d+)\s+([A-Z][^0-9]+)$', line_clean)
                        
                        if match1:
                            unit_num = match1.group(1)
                            unit_title = match1.group(2).strip()
                            full_title = f"Unit {unit_num} {unit_title}"
                            
                            # 避免重复，且标题要有实际内容
                            if full_title not in [u['title'] for u in units] and len(unit_title) > 3:
                                units.append({
                                    'number': int(unit_num),
                                    'title': full_title
                                })
                                print(f"  找到: {full_title}")
                        
                        elif match2 and int(match2.group(1)) <= 15:  # 假设最多15个单元
                            unit_num = match2.group(1)
                            unit_title = match2.group(2).strip()
                            
                            # 检查是否像单元标题（大写开头，不是页码说明等）
                            if unit_title and not any(word in unit_title.lower() for word in ['page', 'topic', 'function', 'grammar']):
                                full_title = f"Unit {unit_num} {unit_title}"
                                
                                if full_title not in [u['title'] for u in units]:
                                    units.append({
                                        'number': int(unit_num),
                                        'title': full_title
                                    })
                                    print(f"  找到: {full_title}")
    
    except Exception as e:
        print(f"  ❌ 读取失败: {e}")
    
    # 按单元号排序
    units.sort(key=lambda x: x['number'])
    
    return units

def parse_filename(filename):
    """解析文件名获取年级和学期"""
    info = {}
    
    if '七年级' in filename:
        info['grade'] = '初一'
    elif '八年级' in filename:
        info['grade'] = '初二'
    elif '九年级' in filename:
        info['grade'] = '初三'
    else:
        info['grade'] = '未知'
    
    if '上册' in filename:
        info['semester'] = '上'
    elif '下册' in filename:
        info['semester'] = '下'
    else:
        info['semester'] = '全'
    
    return info

def create_csv_for_textbook(pdf_path, output_dir):
    """为单本教材创建CSV文件"""
    pdf_name = pdf_path.name
    print(f"\n处理: {pdf_name}")
    
    # 解析文件名
    info = parse_filename(pdf_name)
    grade = info['grade']
    semester = info['semester']
    
    # 提取单元
    units = extract_english_units(pdf_path)
    
    if not units:
        print(f"  ❌ 未找到单元信息，需要手动创建CSV")
        return None
    
    # 生成CSV文件名
    csv_filename = f"英语-{grade}{semester}.csv"
    csv_path = output_dir / csv_filename
    
    # 写入CSV
    with open(csv_path, 'w', encoding='utf-8-sig') as f:
        f.write('年级,学期,学科,课程号,标题,关键词\n')
        
        for unit in units:
            # 生成关键词（从标题中提取）
            keywords = unit['title'].replace('Unit', '').strip().replace(str(unit['number']), '').strip()
            
            f.write(f'{grade},{semester},英语,{unit["number"]},{unit["title"]},{keywords}\n')
    
    print(f"  ✅ 生成: {csv_filename} ({len(units)}个单元)")
    return csv_path

def main():
    """主函数"""
    print("\n" + "="*80)
    print("  📚 读取所有英语教材并生成CSV")
    print("="*80)
    
    # 英语教材目录
    textbook_dir = Path(__file__).parent.parent / '课本' / '英语'
    output_dir = Path(__file__).parent.parent / 'course' / '英语'
    
    if not textbook_dir.exists():
        print(f"❌ 目录不存在: {textbook_dir}")
        return
    
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    
    # 获取所有PDF
    pdf_files = sorted(textbook_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ 未找到PDF文件")
        return
    
    print(f"\n找到 {len(pdf_files)} 本英语教材\n")
    
    csv_files = []
    failed_files = []
    
    for pdf_file in pdf_files:
        csv_path = create_csv_for_textbook(pdf_file, output_dir)
        if csv_path:
            csv_files.append(csv_path)
        else:
            failed_files.append(pdf_file.name)
    
    print("\n" + "="*80)
    print("  ✨ 完成")
    print("="*80)
    print(f"\n✅ 成功生成 {len(csv_files)} 个CSV文件:")
    for csv_file in csv_files:
        print(f"  - {csv_file.name}")
    
    if failed_files:
        print(f"\n❌ 以下 {len(failed_files)} 本需要手动创建CSV:")
        for failed_file in failed_files:
            print(f"  - {failed_file}")
        print("\n💡 建议：手动打开PDF查看目录，创建对应的CSV文件")
    
    print()

if __name__ == '__main__':
    main()

