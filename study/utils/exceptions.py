"""
自定义异常处理
"""
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from utils.response import APIResponse


def custom_exception_handler(exc, context):
    """自定义异常处理器"""
    # 调用DRF默认的异常处理
    response = exception_handler(exc, context)
    
    if response is not None:
        # 如果是验证错误
        if isinstance(exc, ValidationError):
            return APIResponse.error(
                message="参数验证失败",
                code=400,
                errors=response.data
            )
        
        # 如果是认证失败
        if isinstance(exc, AuthenticationFailed):
            return APIResponse.unauthorized(message=str(exc))
        
        # 其他错误
        return APIResponse.error(
            message=str(exc),
            code=response.status_code
        )
    
    # 如果不是DRF的异常，返回500错误
    return APIResponse.server_error(message="服务器内部错误")

