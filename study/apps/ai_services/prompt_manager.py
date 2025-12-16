"""
Prompt模板管理器
"""
from typing import Dict, Any
from .models import PromptTemplate


class PromptManager:
    """Prompt模板管理器"""
    
    @staticmethod
    def get_template(template_type: str, subject: str) -> PromptTemplate:
        """
        获取Prompt模板
        
        Args:
            template_type: 模板类型
            subject: 学科代码
            
        Returns:
            PromptTemplate对象
        """
        template = PromptTemplate.objects.filter(
            template_type=template_type,
            subject=subject,
            is_active=True
        ).order_by('-version').first()
        
        if not template:
            # 如果没有找到特定学科的模板，尝试获取通用模板
            template = PromptTemplate.objects.filter(
                template_type=template_type,
                subject='all',
                is_active=True
            ).order_by('-version').first()
        
        if not template:
            raise Exception(f"未找到模板: {template_type} - {subject}")
        
        return template
    
    @staticmethod
    def render_template(template: PromptTemplate, **kwargs) -> str:
        """
        渲染Prompt模板
        
        Args:
            template: PromptTemplate对象
            **kwargs: 模板变量
            
        Returns:
            渲染后的提示词
        """
        try:
            return template.render(**kwargs)
        except ValueError as e:
            raise Exception(str(e))
    
    @staticmethod
    def get_and_render(template_type: str, subject: str, **kwargs) -> str:
        """
        获取并渲染Prompt模板（便捷方法）
        
        Args:
            template_type: 模板类型
            subject: 学科代码
            **kwargs: 模板变量
            
        Returns:
            渲染后的提示词
        """
        template = PromptManager.get_template(template_type, subject)
        return PromptManager.render_template(template, **kwargs)

