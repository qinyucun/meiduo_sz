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
        # 加载fdfs的客户端配置文件来创建出一个fdfs客户端
        # client = Fdfs_client('meiduo_mall/utils/fastdfs/client.conf')
        # client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        client = Fdfs_client(self.client_conf)

        # 下面这种上传方式需要知道当前要上传文件的本地路径
        # ret = client.upload_by_filename('/Users/chao/Desktop/01.jpg')  此方法上传到storage中的文件会有后缀
        ret = client.upload_appender_by_buffer(content.read())  # 此方法上传的文件无后缀

        # 判断文件是否上传成功
        status = ret.get('Status')  # 取出当前图片上传后响应的状态
        if status != 'Upload successed.':
            raise Exception('Upload file failed')  # 文件上传失败
        # 如果能执行到这里,说明文件上传成功了
        file_id = ret.get('Remote file_id')
        return file_id

    def exists(self, name):
        """
        判断文件是否存在,FastDFS可以自行解决重名问题
        所以此处返回False,告诉Django上传的都是新文件
        :param name: 文件名
        :return: False
        """

    def url(self, name):
        """
        返回完整的url路径
        :param name: 数据库中保存的文件名
        :return: 完整的url
        """
        return settings.FDFS_BASE_URL + name
