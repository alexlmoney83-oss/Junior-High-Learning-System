"""
从语文PDF自动提取课文信息并生成CSV
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

class ChineseTextbookExtractor:
    """语文课本内容提取器"""
    
    # PDF文件映射
    PDF_MAP = {
        ('初一', '上'): '【人教版五四制】七年级上册(2024秋版)语文电子课本.pdf',
        ('初一', '下'): '【人教版五四制】七年级下册(2025春版)语文电子课本.pdf',
        ('初二', '上'): '【人教版五四制】八年级上册(2025秋版)语文电子课本.pdf',
        ('初二', '下'): '【人教版五四制】八年级下册语文电子课本.pdf',
        ('初三', '上'): '【人教版五四制】九年级上册语文电子课本.pdf',
        ('初三', '下'): '【人教版五四制】九年级下册语文电子课本.pdf',
    }
    
    def __init__(self):
        self.pdf_base_path = Path(__file__).parent.parent / '课本' / '语文'
        self.output_path = Path(__file__).parent.parent / 'course' / '语文'
    
    def extract_toc_from_pdf(self, pdf_path):
        """从PDF提取目录"""
        
        lessons = []
        seen_lessons = set()  # 用于去重
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # 读取前10页，查找目录
                for page_num in range(min(10, len(pdf.pages))):
                    page = pdf.pages[page_num]
                    text = page.extract_text()
                    
                    if not text:
                        continue
                    
                    # 只处理包含"目录"或"目 录"的页面
                    if '目' not in text or page_num > 8:
                        continue
                    
                    lines = text.split('\n')
                    
                    for line in lines:
                        line = line.strip()
                        
                        # 跳过包含"阅 读"这种分开格式的行
                        if '阅 读' in line or '读 第' in line:
                            continue
                        
                        # 先移除"阅读"前缀（连在一起的）
                        line_clean = re.sub(r'^阅读\s+', '', line)
                        
                        # 匹配带作者的格式: "1 标题/作者 页码"
                        match1 = re.match(r'^(\d+)\*?\s+(.+?)\s*/\s*(.+?)(?:\s+\d+)?$', line_clean)
                        # 匹配无作者的格式: "1 标题 页码"
                        match2 = re.match(r'^(\d+)\*?\s+([^/\d]+?)(?:\s+\d+)?$', line_clean)
                        
                        match = match1 or match2
                        
                        if match:
                            lesson_num = match.group(1)
                            title = match.group(2).strip()
                            author = match.group(3).strip() if len(match.groups()) >= 3 and match.group(3) else ''
                            
                            # 过滤掉非课文内容
                            skip_keywords = ['阅读综合实践', '写作', '整本书阅读', '专题学习', 
                                           '课外古诗词', '活动·探究', '任务', '目 录',
                                           '单元', '注：']
                            
                            if any(kw in title for kw in skip_keywords):
                                continue
                            
                            # 过滤太短的标题（可能是误匹配）
                            if len(title) < 2:
                                continue
                            
                            # 处理标题（移除副标题）
                            if '——' in title:
                                title = title.split('——')[0].strip()
                            
                            # 去除标题末尾的页码
                            title = re.sub(r'\s+\d+$', '', title)
                            
                            # 去重：使用课程号+标题作为唯一标识
                            lesson_key = f"{lesson_num}_{title}"
                            if lesson_key in seen_lessons:
                                continue
                            seen_lessons.add(lesson_key)
                            
                            # 生成关键词
                            keywords = self.generate_keywords(title, author)
                            
                            lessons.append({
                                '课程号': lesson_num,
                                '标题': title,
                                '作者': author,
                                '关键词': keywords
                            })
        
        except Exception as e:
            print(f"  ❌ 提取失败: {e}")
            return []
        
        # 按课程号排序
        lessons.sort(key=lambda x: int(x['课程号']))
        
        return lessons
    
    def generate_keywords(self, title, author):
        """根据标题和作者生成关键词"""
        
        keywords = []
        
        # 添加作者
        if author and author != '':
            # 清理作者名（去掉书名号等）
            author_clean = author.replace('《', '').replace('》', '').replace('（', '').replace('）', '')
            keywords.append(author_clean)
        
        # 根据标题判断体裁
        if '诗' in title or '词' in title:
            keywords.append('诗歌')
        elif '文言' in title or any(classic in author for classic in ['资治通鉴', '论语', '孟子', '列子']):
            keywords.append('文言文')
        elif '散文' in title:
            keywords.append('散文')
        elif '小说' in title:
            keywords.append('小说')
        elif '记' in title:
            keywords.append('记叙文')
        elif '说' in title:
            keywords.append('说明文')
        else:
            keywords.append('现代文')
        
        return '|'.join(keywords) if keywords else ''
    
    def process_all_textbooks(self):
        """处理所有语文课本"""
        
        print("\n" + "="*80)
        print("  📚 语文课本CSV生成")
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
                print(f"   ❌ 未提取到课文信息")
                continue
            
            print(f"   ✅ 提取到 {len(lessons)} 篇课文")
            
            # 显示前3篇
            for i, lesson in enumerate(lessons[:3], 1):
                print(f"      {i}. {lesson['标题']} / {lesson['作者']}")
            if len(lessons) > 3:
                print(f"      ...")
            
            # 生成CSV
            csv_filename = f"语文-{grade}{semester}.csv"
            csv_path = self.output_path / csv_filename
            
            # 构建DataFrame
            data = []
            for lesson in lessons:
                data.append({
                    '年级': grade,
                    '学期': semester,
                    '学科': '语文',
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
    extractor = ChineseTextbookExtractor()
    extractor.process_all_textbooks()

if __name__ == '__main__':
    main()

