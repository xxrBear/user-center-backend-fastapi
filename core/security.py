import hashlib


def encrypt_with_md5(input_string: str) -> str:
    # 创建 md5 对象
    md5_obj = hashlib.md5()
    # 将字符串转换为字节并更新 md5 对象
    md5_obj.update(input_string.encode('utf-8'))
    # 返回加密后的十六进制字符串
    return md5_obj.hexdigest()
