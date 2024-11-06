import os


def clear_temp_dir(temp_dir):
    """清理临时目录

    Args:
        temp_dir (str): 临时目录路径

    Returns:
        bool: True 表示删除成功，False 表示删除失败
    """
    if not os.path.exists(temp_dir):
        return True

    try:
        for file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file)
            os.remove(file_path)
        return True
    except Exception as e:
        print(e)
        return False
