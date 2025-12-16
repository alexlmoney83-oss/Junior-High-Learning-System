"""
Django后端API客户端
用于前端调用后端接口获取真实数据
"""

import requests
from typing import Dict, List, Optional
import streamlit as st


class APIClient:
    """Django后端API客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        """
        初始化API客户端
        
        Args:
            base_url: Django后端API基础URL
        """
        self.base_url = base_url
        self.token = None
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        headers = {
            "Content-Type": "application/json"
        }
        
        # 如果有token，添加到请求头
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        return headers
    
    def register(self, username: str, email: str, password: str, grade: str, school: str = '') -> Dict:
        """
        用户注册
        
        Args:
            username: 用户名
            email: 邮箱
            password: 密码
            grade: 年级
            school: 学校名称（可选）
        
        Returns:
            注册响应数据
        """
        url = f"{self.base_url}/users/register/"
        data = {
            "username": username,
            "email": email,
            "password": password,
            "password_confirm": password,
            "grade": grade
        }
        
        # 如果提供了学校名称，添加到请求数据中
        if school:
            data["school"] = school
        
        try:
            response = requests.post(url, json=data, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            return {
                'code': 500,
                'message': f'注册失败: {str(e)}',
                'data': None
            }
    
    def login(self, username: str, password: str) -> Dict:
        """
        用户登录
        
        Args:
            username: 用户名
            password: 密码
        
        Returns:
            登录响应数据
        """
        url = f"{self.base_url}/users/login/"
        data = {
            "username": username,
            "password": password
        }
        
        try:
            response = requests.post(url, json=data, headers=self._get_headers())
            response.raise_for_status()
            
            result = response.json()
            
            # 保存token
            if result.get('code') == 200:
                self.token = result['data']['access_token']
                # 保存到session state
                st.session_state['api_token'] = self.token
            
            return result
        
        except requests.exceptions.RequestException as e:
            return {
                'code': 500,
                'message': f'登录失败: {str(e)}',
                'data': None
            }
    
    def get_subjects(self) -> Dict:
        """
        获取学科列表
        
        Returns:
            学科列表数据
        """
        url = f"{self.base_url}/courses/subjects/"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            return {
                'code': 500,
                'message': f'获取学科列表失败: {str(e)}',
                'data': []
            }
    
    def get_courses(self, subject_code: str = None, grade: str = None) -> Dict:
        """
        获取课程列表
        
        Args:
            subject_code: 学科代码（chinese/math/english）
            grade: 年级（grade1/grade2/grade3）
        
        Returns:
            课程列表数据
        """
        url = f"{self.base_url}/courses/courses/"
        
        # 构建查询参数
        params = {}
        if subject_code:
            params['subject'] = subject_code
        if grade:
            params['grade'] = grade
        
        try:
            response = requests.get(url, params=params, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            return {
                'code': 500,
                'message': f'获取课程列表失败: {str(e)}',
                'data': []
            }
    
    def get_course_detail(self, course_id: int) -> Dict:
        """
        获取课程详情
        
        Args:
            course_id: 课程ID
        
        Returns:
            课程详情数据
        """
        url = f"{self.base_url}/courses/courses/{course_id}/"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            return {
                'code': 500,
                'message': f'获取课程详情失败: {str(e)}',
                'data': None
            }
    
    def generate_knowledge_summary(self, course_id: int) -> Dict:
        """
        生成知识点总结
        
        Args:
            course_id: 课程ID
        
        Returns:
            知识点总结数据
        """
        url = f"{self.base_url}/courses/courses/{course_id}/generate-summary/"
        
        try:
            response = requests.post(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            return {
                'code': 500,
                'message': f'生成知识点总结失败: {str(e)}',
                'data': None
            }
    
    def generate_exercises(self, course_id: int, count: int = 25) -> Dict:
        """
        生成练习题
        
        Args:
            course_id: 课程ID
            count: 题目数量
        
        Returns:
            练习题数据
        """
        url = f"{self.base_url}/exercises/generate/"
        data = {
            "course_id": course_id,
            "count": count
        }
        
        try:
            response = requests.post(url, json=data, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            return {
                'code': 500,
                'message': f'生成练习题失败: {str(e)}',
                'data': None
            }
    
    def submit_answer(self, exercise_id: int, user_answer: str) -> Dict:
        """
        提交答案并批改
        
        Args:
            exercise_id: 题目ID
            user_answer: 用户答案
        
        Returns:
            批改结果
        """
        url = f"{self.base_url}/exercises/submit/"
        data = {
            "exercise_id": exercise_id,
            "user_answer": user_answer
        }
        
        try:
            response = requests.post(url, json=data, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            return {
                'code': 500,
                'message': f'提交答案失败: {str(e)}',
                'data': None
            }


# 创建全局API客户端实例
def get_api_client() -> APIClient:
    """获取API客户端实例（单例模式）"""
    if 'api_client' not in st.session_state:
        st.session_state['api_client'] = APIClient()
    
    # 如果session中有token，恢复token
    if 'api_token' in st.session_state:
        st.session_state['api_client'].token = st.session_state['api_token']
    
    return st.session_state['api_client']
