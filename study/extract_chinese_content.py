"""
语文课程内容提取脚本
从PDF中提取内容并更新到数据库
"""
import os
import sys
import django
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'middle_school_system.settings')
django.setup()

try:
    import pdfplumber
except ImportError:
    print("❌ 请先安装: pip install pdfplumber")
    sys.exit(1)

from apps.courses.models import Course, Subject

class ChineseContentExtractor:
    """语文课程内容提取器"""
    
    # PDF文件名映射
    PDF_MAP = {
        ('grade1', 'first'): '【人教版五四制】七年级上册(2024秋版)语文电子课本.pdf',
        ('grade1', 'second'): '【人教版五四制】七年级下册(2025春版)语文电子课本.pdf',
        ('grade2', 'first'): '【人教版五四制】八年级上册(2025秋版)语文电子课本.pdf',
        ('grade2', 'second'): '【人教版五四制】八年级下册语文电子课本.pdf',
        ('grade3', 'first'): '【人教版五四制】九年级上册语文电子课本.pdf',
        ('grade3', 'second'): '【人教版五四制】九年级下册语文电子课本.pdf',
    }
    
    def __init__(self):
        self.pdf_base_path = Path(__file__).parent.parent / '课本' / '语文'
        self.pdf_contents = {}  # 缓存PDF内容
    
    def extract_full_pdf_text(self, pdf_filename):
        """提取整本PDF的文本内容"""
        
        if pdf_filename in self.pdf_contents:
            return self.pdf_contents[pdf_filename]
        
        pdf_path = self.pdf_base_path / pdf_filename
        
        if not pdf_path.exists():
            print(f"  ❌ PDF文件不存在: {pdf_path}")
            return None
        
        print(f"\n  📖 正在读取PDF: {pdf_filename}")
        
        content_parts = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                print(f"     总页数: {total_pages}")
                
                for i, page in enumerate(pdf.pages):
                    try:
                        text = page.extract_text()
                        if text:
                            content_parts.append(text)
                        
                        # 每20页显示一次进度
                        if (i + 1) % 20 == 0:
                            print(f"     进度: {i + 1}/{total_pages} 页")
                    except Exception as e:
                        continue
                
                print(f"     ✅ 提取完成: {len(''.join(content_parts))} 字符")
        
        except Exception as e:
            print(f"  ❌ PDF读取失败：{e}")
            return None
        
        full_content = '\n\n'.join(content_parts)
        self.pdf_contents[pdf_filename] = full_content
        return full_content
    
    def update_course_content(self, course, pdf_content):
        """更新课程内容"""
        
        # 存储整本书的内容到每个课文
        # LLM有完整上下文，可以根据课文标题自动定位相关内容
        
        course.content = pdf_content
        course.pdf_source = self.PDF_MAP.get((course.grade, course.semester), '')
        course.save()
        
        content_preview = pdf_content[:150].replace('\n', ' ')
        print(f"  ✅ [{course.course_number}] {course.title}")
        print(f"     预览: {content_preview}...")
    
    def extract_all_chinese_courses(self):
        """提取所有语文课程内容"""
        
        print("\n" + "="*80)
        print("  📚 语文课程内容提取")
        print("="*80)
        
        # 获取语文学科
        try:
            subject = Subject.objects.get(code='chinese')
        except Subject.DoesNotExist:
            print("\n❌ 未找到语文学科")
            return
        
        # 获取所有语文课程
        courses = Course.objects.filter(subject=subject).order_by('grade', 'semester', 'course_number')
        total = courses.count()
        
        if total == 0:
            print("\n❌ 未找到任何语文课程")
            return
        
        print(f"\n找到 {total} 门语文课程\n")
        
        success_count = 0
        fail_count = 0
        
        # 按学期分组处理
        current_key = None
        pdf_content = None
        
        for course in courses:
            course_key = (course.grade, course.semester)
            
            # 如果切换到新学期，重新加载PDF
            if course_key != current_key:
                current_key = course_key
                pdf_filename = self.PDF_MAP.get(course_key)
                
                if not pdf_filename:
                    print(f"\n⚠️  未找到PDF映射: {course.get_grade_display()} {course.get_semester_display()}")
                    fail_count += 1
                    continue
                
                print(f"\n{'='*80}")
                print(f"  📚 {course.get_grade_display()} {course.get_semester_display()}")
                print(f"{'='*80}")
                
                pdf_content = self.extract_full_pdf_text(pdf_filename)
                
                if not pdf_content:
                    print(f"  ❌ PDF内容提取失败")
                    fail_count += 1
                    continue
            
            # 更新课程内容
            try:
                self.update_course_content(course, pdf_content)
                success_count += 1
            except Exception as e:
                print(f"  ❌ [{course.course_number}] {course.title} - 更新失败: {e}")
                fail_count += 1
        
        # 汇总统计
        print("\n" + "="*80)
        print("  ✨ 提取完成")
        print("="*80)
        print(f"\n总课程数：{total}")
        print(f"✅ 成功：{success_count}")
        print(f"❌ 失败：{fail_count}\n")
        
        if success_count > 0:
            print("💡 下一步：")
            print("  1. 启动Streamlit前端")
            print("  2. 访问语文课程")
            print("  3. 点击'生成知识点总结'，LLM会根据课文标题和PDF内容生成")
            print("  4. 点击'生成练习题'，LLM会自动生成习题\n")

def main():
    extractor = ChineseContentExtractor()
    extractor.extract_all_chinese_courses()

if __name__ == '__main__':
    main()



