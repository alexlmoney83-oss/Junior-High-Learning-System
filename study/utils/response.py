"""
统一API响应格式
"""
from rest_framework.response import Response
from rest_framework import status


class APIResponse:
    """统一API响应格式"""
    
    @staticmethod
    def success(data=None, message="success", code=200):
        """成功响应"""
        return Response({
            'code': code,
            'message': message,
            'data': data
        }, status=status.HTTP_200_OK)
    
    @staticmethod
    def created(data=None, message="创建成功"):
        """创建成功响应"""
        return Response({
            'code': 201,
            'message': message,
            'data': data
        }, status=status.HTTP_201_CREATED)
    
    @staticmethod
    def error(message="操作失败", code=400, errors=None):
        """错误响应"""
        response_data = {
            'code': code,
            'message': message
        }
        if errors:
            response_data['errors'] = errors
        
        return Response(
            response_data,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @staticmethod
    def unauthorized(message="未认证"):
        """未认证响应"""
        return Response({
            'code': 401,
            'message': message
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    @staticmethod
    def forbidden(message="无权限"):
        """无权限响应"""
        return Response({
            'code': 403,
            'message': message
        }, status=status.HTTP_403_FORBIDDEN)
    
    @staticmethod
    def not_found(message="资源不存在"):
        """资源不存在响应"""
        return Response({
            'code': 404,
            'message': message
        }, status=status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    def server_error(message="服务器错误"):
        """服务器错误响应"""
        return Response({
            'code': 500,
            'message': message
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

