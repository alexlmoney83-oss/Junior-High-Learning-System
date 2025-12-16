"""
批量导入CSV课程数据
支持按学科批量导入
"""

import os
import sys
import django
import pandas as pd
from pathlib import Path

# 设置Django环境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'middle_school_system.settings')
django.setup()

from apps.courses.models import Subject, Course

def import_single_csv(csv_file):
    """
    从CSV导入课程
    
    CSV格式：
    年级,学期,学科,课程号,标题,关键词
    初一,上,英语,1,Unit 1 School life,school|daily routine
    """
    
    df = pd.read_csv(csv_file, encoding='utf-8-sig')
    
    print(f"\n📄 处理文件: {os.path.basename(csv_file)}")
    print("-" * 60)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for idx, row in df.iterrows():
        try:
            # 获取学科
            subject_name = row['学科']
            subject_map = {'数学': 'math', '语文': 'chinese', '英语': 'english'}
            subject_code = subject_map.get(subject_name, 'math')
            
            subject, _ = Subject.objects.get_or_create(
                code=subject_code,
                defaults={'name': subject_name, 'is_active': True}
            )
            
            # 年级映射
            grade_map = {
                '初一': 'grade1', '七年级': 'grade1',
                '初二': 'grade2', '八年级': 'grade2',
                '初三': 'grade3', '九年级': 'grade3'
            }
            grade = grade_map.get(row['年级'], 'grade1')
            
            # 学期映射
            semester_map = {
                '上': 'first',
                '下': 'second',
                '全': 'all'
            }
            semester = semester_map.get(row['学期'], 'first')
            
            # 处理关键词（可能为空）
            keywords = row.get('关键词', '')
            if pd.isna(keywords):
                keywords = ''
            
            # 创建课程（使用semester作为unique_together的一部分）
            course, created = Course.objects.get_or_create(
                subject=subject,
                grade=grade,
                semester=semester,
                course_number=str(row['课程号']),
                defaults={
                    'title': row['标题'],
                    'keywords': keywords,
                    'outline': f"{row['标题']} - 知识点待AI生成",
                    'difficulty': 'basic',
                    'is_active': True,
                    'content': '',  # 留空，后续用extract_all_pdf_content.py提取
                    'pdf_source': '',  # 留空
                    'pdf_page_range': ''  # 留空
                }
            )
            
            if created:
                success_count += 1
                print(f"  ✅ [{success_count:2d}] {row['年级']}{row['学期']} 第{row['课程号']:2}课 - {row['标题']}")
            else:
                skip_count += 1
                print(f"  ⏭️  跳过（已存在）：{row['标题']}")
                
        except Exception as e:
            error_count += 1
            print(f"  ❌ 导入失败（第{idx+2}行）：{str(e)}")
            continue
    
    return success_count, skip_count, error_count


def batch_import_from_directory(directory):
    """
    批量导入指定目录下的所有CSV文件
    """
    
    print("=" * 60)
    print("  📚 批量课程导入")
    print("=" * 60)
    
    csv_files = list(Path(directory).glob('*.csv'))
    
    if not csv_files:
        print(f"\n❌ 在目录 {directory} 中没有找到CSV文件")
        return
    
    print(f"\n找到 {len(csv_files)} 个CSV文件：")
    for csv_file in csv_files:
        print(f"  - {csv_file.name}")
    
    total_success = 0
    total_skip = 0
    total_error = 0
    
    for csv_file in csv_files:
        success, skip, error = import_single_csv(str(csv_file))
        total_success += success
        total_skip += skip
        total_error += error
    
    print("\n" + "=" * 60)
    print("  📊 导入统计")
    print("=" * 60)
    print(f"  ✅ 成功导入: {total_success} 门课程")
    print(f"  ⏭️  跳过重复: {total_skip} 门课程")
    print(f"  ❌ 导入失败: {total_error} 门课程")
    print("=" * 60)
    
    if total_success > 0:
        print("\n💡 下一步：")
        print("  1. 运行 extract_all_pdf_content.py 从PDF提取实际课程内容")
        print("  2. 在Streamlit前端访问这些课程")
        print("  3. 配置AI API Key，生成知识点总结和练习题")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("\n用法：")
        print("  python batch_import_csv.py <CSV文件路径>           # 导入单个CSV")
        print("  python batch_import_csv.py <目录路径>             # 批量导入目录下所有CSV")
        print("\n示例：")
        print("  python batch_import_csv.py ../course/英语/英语-初一上.csv")
        print("  python batch_import_csv.py ../course/英语/")
    else:
        target_path = sys.argv[1]
        
        if os.path.isfile(target_path):
            # 单个文件导入
            success, skip, error = import_single_csv(target_path)
            print("\n" + "=" * 60)
            print(f"✅ 成功: {success} | ⏭️  跳过: {skip} | ❌ 失败: {error}")
            print("=" * 60)
        elif os.path.isdir(target_path):
            # 批量目录导入
            batch_import_from_directory(target_path)
        else:
            print(f"❌ 路径不存在: {target_path}")



