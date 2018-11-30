from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from fdfs_client.client import Fdfs_client


class FastDFSStorage(Storage):
    def __init__(self, base_url=None, client_conf=None):
        """
        初始化
        :param base_url: 用于构建图片的完整路径使用,图片服务器的域名
        :param client_conf: 客户端配置路径
        """
        self.client_conf = client_conf or settings.FDFS_CLIENT_CONF  # 如果传入的有值就用,没有就用默认的
        self.base_url = base_url or settings.FDFS_BASE_URL  # 同上
        pass

    def _open(self, name, mode='rb'):
        """
        打开文件
        :param name:
        :param mode:
        :return:
        """
        pass

    def _save(self, name, content):
        """
        在FastDFS中保存文件
        :param name: 传入的文件名
        :param content: 文件内容
        :return: 保存到数据库中的文件名
        """
        pass

    def url(self, name):
        """
        返回完整的url路径
        :param name: 数据库中保存的文件名
        :return: 完整的url
        """
        return self.client_conf + name

    def exists(self, name):
        """
        判断文件是否存在,FastDFS可以自行解决重名问题
        所以此处返回False,告诉Django上传的都是新文件
        :param name: 文件名
        :return: False
        """
