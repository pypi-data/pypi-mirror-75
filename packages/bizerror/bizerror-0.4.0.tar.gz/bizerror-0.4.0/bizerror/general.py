# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import
from bizerror.base import BizErrorBase
from bizerror.base import set_error_info

# Created: 2020-07-26 11:16:20.522000
# WARNING! All changes made in this file will be lost!


class OK(BizErrorBase):
    pass
set_error_info("en", "OK", 0, "OK")
set_error_info("zh-hans", "OK", 0, "正常。")

class BizError(BizErrorBase):
    pass
set_error_info("en", "BizError", 1, "BizError")
set_error_info("zh-hans", "BizError", 1, "异常！")

class SysError(BizErrorBase):
    pass
set_error_info("en", "SysError", 1001000000, "System Error")
set_error_info("zh-hans", "SysError", 1001000000, "系统异常")

class UndefinedError(SysError):
    pass
set_error_info("en", "UndefinedError", 1001000001, "Unknown Error")
set_error_info("zh-hans", "UndefinedError", 1001000001, "未定义的异常")

class DatabaseError(SysError):
    pass
set_error_info("en", "DatabaseError", 1001000002, "System Error")
set_error_info("zh-hans", "DatabaseError", 1001000002, "服务器异常")

class CacheError(SysError):
    pass
set_error_info("en", "CacheError", 1001000003, "System Error")
set_error_info("zh-hans", "CacheError", 1001000003, "服务器异常")

class MessageQueueError(SysError):
    pass
set_error_info("en", "MessageQueueError", 1001000004, "System Error")
set_error_info("zh-hans", "MessageQueueError", 1001000004, "服务器异常")

class AnotherServiceError(SysError):
    pass
set_error_info("en", "AnotherServiceError", 1001000005, "System Error")
set_error_info("zh-hans", "AnotherServiceError", 1001000005, "服务器异常")

class HttpError(BizErrorBase):
    pass
set_error_info("en", "HttpError", 1001010000, "Http Error.")
set_error_info("zh-hans", "HttpError", 1001010000, "HTTP请求相关异常。")

class RequestExpired(HttpError):
    pass
set_error_info("en", "RequestExpired", 1001010001, "Request expired.")
set_error_info("zh-hans", "RequestExpired", 1001010001, "请求已过期！")

class NotSupportedHttpMethod(HttpError):
    pass
set_error_info("en", "NotSupportedHttpMethod", 1001010002, "Not supported http method.")
set_error_info("zh-hans", "NotSupportedHttpMethod", 1001010002, "不支持的请求方法！")

class ConfigError(BizErrorBase):
    pass
set_error_info("en", "ConfigError", 1001020000, "Config error.")
set_error_info("zh-hans", "ConfigError", 1001020000, "配置相关异常。")

class MissingConfigItem(ConfigError):
    pass
set_error_info("en", "MissingConfigItem", 1001020001, "Missing config item: {item}.")
set_error_info("zh-hans", "MissingConfigItem", 1001020001, "缺少必要的配置项：{item}。")

class DataError(BizErrorBase):
    pass
set_error_info("en", "DataError", 1001030000, "Data error.")
set_error_info("zh-hans", "DataError", 1001030000, "数据相关异常。")

class TargetNotFound(DataError):
    pass
set_error_info("en", "TargetNotFound", 1001030001, "Target not found.")
set_error_info("zh-hans", "TargetNotFound", 1001030001, "没有找到目标对象！")

class AuthError(BizErrorBase):
    pass
set_error_info("en", "AuthError", 1001040000, "Auth error.")
set_error_info("zh-hans", "AuthError", 1001040000, "认证相关异常。")

class AccountLockedError(AuthError):
    pass
set_error_info("en", "AccountLockedError", 1001040001, "Account locked.")
set_error_info("zh-hans", "AccountLockedError", 1001040001, "帐号被锁定，请联系管理员！")

class AccountTemporaryLockedError(AuthError):
    pass
set_error_info("en", "AccountTemporaryLockedError", 1001040002, "Account temporary locked.")
set_error_info("zh-hans", "AccountTemporaryLockedError", 1001040002, "登录失败次数超过上限，帐号被临时锁定！")

class UserPasswordError(AuthError):
    pass
set_error_info("en", "UserPasswordError", 1001040003, "User not exist or wrong password.")
set_error_info("zh-hans", "UserPasswordError", 1001040003, "帐号或密码错误，请重试！")

class AppAuthFailed(AuthError):
    pass
set_error_info("en", "AppAuthFailed", 1001040004, "App auth failed.")
set_error_info("zh-hans", "AppAuthFailed", 1001040004, "应用认证失败！")

class TsExpiredError(AuthError):
    pass
set_error_info("en", "TsExpiredError", 1001040005, "Timestamp expired.")
set_error_info("zh-hans", "TsExpiredError", 1001040005, "时间戳已失效。")

class AccountDisabledError(AuthError):
    pass
set_error_info("en", "AccountDisabledError", 1001040006, "Account disabled.")
set_error_info("zh-hans", "AccountDisabledError", 1001040006, "帐号已禁用，请联系管理员！")

class AccountStatusError(AuthError):
    pass
set_error_info("en", "AccountStatusError", 1001040007, "Bad account status.")
set_error_info("zh-hans", "AccountStatusError", 1001040007, "帐号状态异常，请联系管理员处理！")

class AccountRemovedError(AuthError):
    pass
set_error_info("en", "AccountRemovedError", 1001040008, "Account removed.")
set_error_info("zh-hans", "AccountRemovedError", 1001040008, "帐号已删除！")

class LoginRequired(AuthError):
    pass
set_error_info("en", "LoginRequired", 1001040009, "Login required.")
set_error_info("zh-hans", "LoginRequired", 1001040009, "请先登录！")

class AccessDenied(AuthError):
    pass
set_error_info("en", "AccessDenied", 1001040010, "Access denied.")
set_error_info("zh-hans", "AccessDenied", 1001040010, "禁止访问！")

class TypeError(BizErrorBase):
    pass
set_error_info("en", "TypeError", 1001050000, "Type error.")
set_error_info("zh-hans", "TypeError", 1001050000, "数据类型相关异常。")

class CastToIntegerFailed(TypeError):
    pass
set_error_info("en", "CastToIntegerFailed", 1001050001, "Cast to integer value failed on field {field}.")
set_error_info("zh-hans", "CastToIntegerFailed", 1001050001, "字段{field}转化整数型数据失败！")

class CastToFloatFailed(TypeError):
    pass
set_error_info("en", "CastToFloatFailed", 1001050002, "Cast to float value failed on field {field}.")
set_error_info("zh-hans", "CastToFloatFailed", 1001050002, "字段{field}转化浮点数型数据失败！")

class CastToNumbericFailed(TypeError):
    pass
set_error_info("en", "CastToNumbericFailed", 1001050003, "Cast to numberic value failed on field {field}.")
set_error_info("zh-hans", "CastToNumbericFailed", 1001050003, "字段{field}转化数值型数据失败！")

class CastToBooleanFailed(TypeError):
    pass
set_error_info("en", "CastToBooleanFailed", 1001050004, "Cast to boolean value failed on field {field}.")
set_error_info("zh-hans", "CastToBooleanFailed", 1001050004, "字段{field}转化布尔型数据失败！")

class CastToStringFailed(TypeError):
    pass
set_error_info("en", "CastToStringFailed", 1001050005, "Cast to string value failed on field {field}.")
set_error_info("zh-hans", "CastToStringFailed", 1001050005, "字段{field}转化字符串型数据失败！")

class ParseJsonError(TypeError):
    pass
set_error_info("en", "ParseJsonError", 1001050006, "Parse json error.")
set_error_info("zh-hans", "ParseJsonError", 1001050006, "Json转化异常！")

class NotSupportedTypeToCast(TypeError):
    pass
set_error_info("en", "NotSupportedTypeToCast", 1001050007, "Not supported type to cast.")
set_error_info("zh-hans", "NotSupportedTypeToCast", 1001050007, "该类型不支持转化！")

class ParamError(BizErrorBase):
    pass
set_error_info("en", "ParamError", 1001060000, "Param error.")
set_error_info("zh-hans", "ParamError", 1001060000, "参数相关异常。")

class MissingParameter(ParamError):
    pass
set_error_info("en", "MissingParameter", 1001060001, "Missing parameter: {parameter}.")
set_error_info("zh-hans", "MissingParameter", 1001060001, "必要参数缺失：{parameter}。")

class BadParameter(ParamError):
    pass
set_error_info("en", "BadParameter", 1001060002, "Bad parameter: {parameter}.")
set_error_info("zh-hans", "BadParameter", 1001060002, "参数值有误：{parameter}。")

class BadParameterType(ParamError):
    pass
set_error_info("en", "BadParameterType", 1001060003, "Bad parameter type: {parameter}.")
set_error_info("zh-hans", "BadParameterType", 1001060003, "参数类型有误：{parameter}。")

class FormError(BizErrorBase):
    pass
set_error_info("en", "FormError", 1001070000, "Form error.")
set_error_info("zh-hans", "FormError", 1001070000, "表单相关异常。")

class CaptchaOnlyAllowedOnce(FormError):
    pass
set_error_info("en", "CaptchaOnlyAllowedOnce", 1001070001, "Captcha only allowed one time use.")
set_error_info("zh-hans", "CaptchaOnlyAllowedOnce", 1001070001, "验证码不允许重复使用！")

class CaptchaValidateFailed(FormError):
    pass
set_error_info("en", "CaptchaValidateFailed", 1001070002, "Captcha validate failed.")
set_error_info("zh-hans", "CaptchaValidateFailed", 1001070002, "图片验证码校验失败！")

class RepeatedlySubmitForm(FormError):
    pass
set_error_info("en", "RepeatedlySubmitForm", 1001070003, "Please do not submit a form repeatedly.")
set_error_info("zh-hans", "RepeatedlySubmitForm", 1001070003, "请不要重复提交表单！")

class LogicError(BizErrorBase):
    pass
set_error_info("en", "LogicError", 1001080000, "Logic error.")
set_error_info("zh-hans", "LogicError", 1001080000, "业务逻辑相关异常。")
