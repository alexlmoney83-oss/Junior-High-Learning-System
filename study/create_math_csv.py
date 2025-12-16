"""
从数学PDF自动提取章节信息并生成CSV
"""
import os
import sys
import re
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).parent))

try:
    import pdfplumber
except ImportError:
    print("❌ 请先安装: pip install pdfplumber")
    sys.exit(1)

class MathTextbookExtractor:
    """数学课本内容提取器"""
    
    # PDF文件映射
    PDF_MAP = {
        ('初一', '上'): '7上-沪教版初中数学课本（2024新版）上海.pdf',
        ('初一', '下'): '【沪教版五四制】七年级下册(2025春版)数学电子课本.pdf',
        ('初二', '上'): '【沪教版五四制】八年级上册(2025秋版)数学电子课本.pdf',
    }
    
    def __init__(self):
        self.pdf_base_path = Path(__file__).parent.parent / '课本' / '数学'
        self.output_path = Path(__file__).parent.parent / 'course' / '数学'
    
    def extract_toc_from_pdf(self, pdf_path):
        """从PDF提取目录"""
        
        lessons = []
        seen_lessons = set()
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # 读取前15页，查找目录（数学目录可能比较长）
                for page_num in range(min(15, len(pdf.pages))):
                    page = pdf.pages[page_num]
                    text = page.extract_text()
                    
                    if not text:
                        continue
                    
                    # 只处理包含"目录"或"目 录"或包含章节编号的页面
                    if page_num > 12:
                        continue
                    
                    # 如果不包含"目"字但包含章节编号格式，也处理
                    has_section = bool(re.search(r'\d+\.\d+\s+.+\s+\d+', text))
                    if '目' not in text and not has_section:
                        continue
                    
                    lines = text.split('\n')
                    
                    for line in lines:
                        line = line.strip()
                        
                        # 匹配章节格式: "15.1 不等式及其性质 2"
                        # 或: "第 15 章 一元一次不等式"
                        match1 = re.match(r'^(\d+)\.(\d+)\s+(.+?)\s+\d+$', line)
                        
                        if match1:
                            chapter = match1.group(1)
                            section = match1.group(2)
                            title = match1.group(3).strip()
                            course_num = f"{chapter}.{section}"
                            
                            # 过滤掉非课程内容
                            skip_keywords = ['内容提要', '复习题', '阅读材料', '综合与实践', '附录']
                            
                            if any(kw in title for kw in skip_keywords):
                                continue
                            
                            # 去重
                            lesson_key = f"{course_num}_{title}"
                            if lesson_key in seen_lessons:
                                continue
                            seen_lessons.add(lesson_key)
                            
                            # 生成关键词（简化版，从标题提取）
                            keywords = self.generate_keywords(title)
                            
                            lessons.append({
                                '课程号': course_num,
                                '标题': title,
                                '关键词': keywords
                            })
        
        except Exception as e:
            print(f"  ❌ 提取失败: {e}")
            return []
        
        # 按课程号排序
        lessons.sort(key=lambda x: tuple(map(float, x['课程号'].split('.'))))
        
        return lessons
    
    def generate_keywords(self, title):
        """根据标题生成关键词"""
        # 简化版：直接使用标题作为关键词
        return title
    
    def process_all_textbooks(self):
        """处理所有数学课本"""
        
        print("\n" + "="*80)
        print("  📚 数学课本CSV生成")
        print("="*80 + "\n")
        
        for (grade, semester), pdf_name in self.PDF_MAP.items():
            pdf_path = self.pdf_base_path / pdf_name
            
            if not pdf_path.exists():
                print(f"⚠️  文件不存在: {pdf_name}")
                continue
            
            print(f"\n📖 处理: {grade}{semester}学期")
            print(f"   PDF: {pdf_name}")
            
            # 提取目录
            lessons = self.extract_toc_from_pdf(pdf_path)
            
            if not lessons:
                print(f"   ❌ 未提取到课程信息")
                continue
            
            print(f"   ✅ 提取到 {len(lessons)} 个小节")
            
            # 显示前3个
            for i, lesson in enumerate(lessons[:3], 1):
                print(f"      {i}. {lesson['课程号']} {lesson['标题']}")
            if len(lessons) > 3:
                print(f"      ...")
            
            # 生成CSV
            csv_filename = f"数学-{grade}{semester}.csv"
            csv_path = self.output_path / csv_filename
            
            # 构建DataFrame
            data = []
            for lesson in lessons:
                data.append({
                    '年级': grade,
                    '学期': semester,
                    '学科': '数学',
                    '课程号': lesson['课程号'],
                    '标题': lesson['标题'],
                    '关键词': lesson['关键词']
                })
            
            df = pd.DataFrame(data)
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            
            print(f"   💾 已保存: {csv_filename}\n")
        
        print("\n" + "="*80)
        print("  ✅ CSV生成完成")
        print("="*80)
        print("\n💡 下一步：")
        print("  1. 检查生成的CSV文件")
        print("  2. 如有需要，手动修正标题和关键词")
        print("  3. 运行 batch_import_csv.py 导入数据库\n")

def main():
    extractor = MathTextbookExtractor()
    extractor.process_all_textbooks()

if __name__ == '__main__':
    main()

