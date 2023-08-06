# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel


class Config(TeaModel):
    """
    Model for initing client
    """
    def __init__(self, access_key_id=None, access_key_secret=None, security_token=None, protocol=None, read_timeout=None, connect_timeout=None, http_proxy=None, https_proxy=None, endpoint=None, no_proxy=None, max_idle_conns=None, user_agent=None, socks_5proxy=None, socks_5net_work=None):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.security_token = security_token
        self.protocol = protocol
        self.read_timeout = read_timeout
        self.connect_timeout = connect_timeout
        self.http_proxy = http_proxy
        self.https_proxy = https_proxy
        self.endpoint = endpoint
        self.no_proxy = no_proxy
        self.max_idle_conns = max_idle_conns
        self.user_agent = user_agent
        self.socks_5proxy = socks_5proxy
        self.socks_5net_work = socks_5net_work

    def validate(self):
        pass

    def to_map(self):
        result = {}
        result['accessKeyId'] = self.access_key_id
        result['accessKeySecret'] = self.access_key_secret
        result['securityToken'] = self.security_token
        result['protocol'] = self.protocol
        result['readTimeout'] = self.read_timeout
        result['connectTimeout'] = self.connect_timeout
        result['httpProxy'] = self.http_proxy
        result['httpsProxy'] = self.https_proxy
        result['endpoint'] = self.endpoint
        result['noProxy'] = self.no_proxy
        result['maxIdleConns'] = self.max_idle_conns
        result['userAgent'] = self.user_agent
        result['socks5Proxy'] = self.socks_5proxy
        result['socks5NetWork'] = self.socks_5net_work
        return result

    def from_map(self, map={}):
        self.access_key_id = map.get('accessKeyId')
        self.access_key_secret = map.get('accessKeySecret')
        self.security_token = map.get('securityToken')
        self.protocol = map.get('protocol')
        self.read_timeout = map.get('readTimeout')
        self.connect_timeout = map.get('connectTimeout')
        self.http_proxy = map.get('httpProxy')
        self.https_proxy = map.get('httpsProxy')
        self.endpoint = map.get('endpoint')
        self.no_proxy = map.get('noProxy')
        self.max_idle_conns = map.get('maxIdleConns')
        self.user_agent = map.get('userAgent')
        self.socks_5proxy = map.get('socks5Proxy')
        self.socks_5net_work = map.get('socks5NetWork')
        return self


class NameValuePair(TeaModel):
    # 键名
    # 键值
    def __init__(self, name=None, value=None):
        self.name = name
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = {}
        result['name'] = self.name
        result['value'] = self.value
        return result

    def from_map(self, map={}):
        self.name = map.get('name')
        self.value = map.get('value')
        return self


class InvokerInfo(TeaModel):
    # 调用渠道
    # 渠道的用户id
    # 8位金融云租户ID
    # 调用者用户金融云id
    def __init__(self, invoke_channel=None, invoke_channel_uid=None, invoke_tenant=None, invoke_user_id=None):
        self.invoke_channel = invoke_channel
        self.invoke_channel_uid = invoke_channel_uid
        self.invoke_tenant = invoke_tenant
        self.invoke_user_id = invoke_user_id

    def validate(self):
        pass

    def to_map(self):
        result = {}
        result['invoke_channel'] = self.invoke_channel
        result['invoke_channel_uid'] = self.invoke_channel_uid
        result['invoke_tenant'] = self.invoke_tenant
        result['invoke_user_id'] = self.invoke_user_id
        return result

    def from_map(self, map={}):
        self.invoke_channel = map.get('invoke_channel')
        self.invoke_channel_uid = map.get('invoke_channel_uid')
        self.invoke_tenant = map.get('invoke_tenant')
        self.invoke_user_id = map.get('invoke_user_id')
        return self


class CreateNtcloudGatewayxBizeventMessageRequest(TeaModel):
    # 业务消息内容，json格式
    # 消费方id，例如appId，tenantId，可以多个，多个之间使用","分割
    # 消费者类型，例如TENANT, APP
    # 消息发送过程中的唯一ID
    # 消息事件编码
    # 消息类型，1：点对点，2: 广播消息
    # 二级消息主题,订阅方可以过滤消息
    # 日期对应的timestamp
    def __init__(self, auth_token=None, product_instance_id=None, region_name=None, biz_content=None, consumer_id=None, consumer_type=None, msg_id=None, msg_key=None, msg_type=None, tags=None, utc_timestamp=None):
        self.auth_token = auth_token
        self.product_instance_id = product_instance_id
        self.region_name = region_name
        self.biz_content = biz_content
        self.consumer_id = consumer_id
        self.consumer_type = consumer_type
        self.msg_id = msg_id
        self.msg_key = msg_key
        self.msg_type = msg_type
        self.tags = tags
        self.utc_timestamp = utc_timestamp

    def validate(self):
        pass

    def to_map(self):
        result = {}
        result['auth_token'] = self.auth_token
        result['product_instance_id'] = self.product_instance_id
        result['region_name'] = self.region_name
        result['biz_content'] = self.biz_content
        result['consumer_id'] = self.consumer_id
        result['consumer_type'] = self.consumer_type
        result['msg_id'] = self.msg_id
        result['msg_key'] = self.msg_key
        result['msg_type'] = self.msg_type
        result['tags'] = self.tags
        result['utc_timestamp'] = self.utc_timestamp
        return result

    def from_map(self, map={}):
        self.auth_token = map.get('auth_token')
        self.product_instance_id = map.get('product_instance_id')
        self.region_name = map.get('region_name')
        self.biz_content = map.get('biz_content')
        self.consumer_id = map.get('consumer_id')
        self.consumer_type = map.get('consumer_type')
        self.msg_id = map.get('msg_id')
        self.msg_key = map.get('msg_key')
        self.msg_type = map.get('msg_type')
        self.tags = map.get('tags')
        self.utc_timestamp = map.get('utc_timestamp')
        return self


class CreateNtcloudGatewayxBizeventMessageResponse(TeaModel):
    def __init__(self, req_msg_id=None, result_code=None, result_msg=None):
        self.req_msg_id = req_msg_id
        self.result_code = result_code
        self.result_msg = result_msg

    def validate(self):
        pass

    def to_map(self):
        result = {}
        result['req_msg_id'] = self.req_msg_id
        result['result_code'] = self.result_code
        result['result_msg'] = self.result_msg
        return result

    def from_map(self, map={}):
        self.req_msg_id = map.get('req_msg_id')
        self.result_code = map.get('result_code')
        self.result_msg = map.get('result_msg')
        return self


class CreateNtcloudGatewayxFileUploadRequest(TeaModel):
    # 产品方的api归属集群，即productInstanceId
    # 上传文件作用的openapi method
    # 文件标签，多个标签;分割
    # 自定义的文件元数据
    # 文件名，不传则随机生成文件名
    # 文件的多媒体类型
    def __init__(self, auth_token=None, product_instance_id=None, region_name=None, api_cluster=None, api_code=None, file_label=None, file_metadata=None, file_name=None, mime_type=None):
        self.auth_token = auth_token
        self.product_instance_id = product_instance_id
        self.region_name = region_name
        self.api_cluster = api_cluster
        self.api_code = api_code
        self.file_label = file_label
        self.file_metadata = file_metadata
        self.file_name = file_name
        self.mime_type = mime_type

    def validate(self):
        if self.file_label:
            self.validate_max_length(self.file_label, 'file_label', 100)
        if self.file_metadata:
            self.validate_max_length(self.file_metadata, 'file_metadata', 1000)
        if self.file_name:
            self.validate_max_length(self.file_name, 'file_name', 100)

    def to_map(self):
        result = {}
        result['auth_token'] = self.auth_token
        result['product_instance_id'] = self.product_instance_id
        result['region_name'] = self.region_name
        result['api_cluster'] = self.api_cluster
        result['api_code'] = self.api_code
        result['file_label'] = self.file_label
        result['file_metadata'] = self.file_metadata
        result['file_name'] = self.file_name
        result['mime_type'] = self.mime_type
        return result

    def from_map(self, map={}):
        self.auth_token = map.get('auth_token')
        self.product_instance_id = map.get('product_instance_id')
        self.region_name = map.get('region_name')
        self.api_cluster = map.get('api_cluster')
        self.api_code = map.get('api_code')
        self.file_label = map.get('file_label')
        self.file_metadata = map.get('file_metadata')
        self.file_name = map.get('file_name')
        self.mime_type = map.get('mime_type')
        return self


class CreateNtcloudGatewayxFileUploadResponse(TeaModel):
    # 上传有效期
    # 32位文件唯一id
    # 放入http请求头里
    # 文件上传地址
    def __init__(self, req_msg_id=None, result_code=None, result_msg=None, expired_time=None, file_id=None, upload_headers=None, upload_url=None):
        self.req_msg_id = req_msg_id
        self.result_code = result_code
        self.result_msg = result_msg
        self.expired_time = expired_time
        self.file_id = file_id
        self.upload_headers = []
        self.upload_url = upload_url

    def validate(self):
        if self.expired_time:
            self.validate_pattern(self.expired_time, 'expired_time', '\\d{4}[-]\\d{1,2}[-]\\d{1,2}[T]\\d{2}:\\d{2}:\\d{2}[Z]')
        if self.upload_headers:
            for k in self.upload_headers:
                if k :
                    k.validate()

    def to_map(self):
        result = {}
        result['req_msg_id'] = self.req_msg_id
        result['result_code'] = self.result_code
        result['result_msg'] = self.result_msg
        result['expired_time'] = self.expired_time
        result['file_id'] = self.file_id
        result['upload_headers'] = []
        if self.upload_headers is not None:
            for k in self.upload_headers:
                result['upload_headers'].append(k.to_map() if k else None)
        else:
            result['upload_headers'] = None
        result['upload_url'] = self.upload_url
        return result

    def from_map(self, map={}):
        self.req_msg_id = map.get('req_msg_id')
        self.result_code = map.get('result_code')
        self.result_msg = map.get('result_msg')
        self.expired_time = map.get('expired_time')
        self.file_id = map.get('file_id')
        self.upload_headers = []
        if map.get('upload_headers') is not None:
            for k in map.get('upload_headers'):
                temp_model = NameValuePair()
                temp_model = temp_model.from_map(k)
                self.upload_headers.append(temp_model)
        else:
            self.upload_headers = None
        self.upload_url = map.get('upload_url')
        return self


class GetNtcloudGatewayxFileDownloadRequest(TeaModel):
    # 文件唯一id
    def __init__(self, auth_token=None, product_instance_id=None, region_name=None, file_id=None):
        self.auth_token = auth_token
        self.product_instance_id = product_instance_id
        self.region_name = region_name
        self.file_id = file_id

    def validate(self):
        pass

    def to_map(self):
        result = {}
        result['auth_token'] = self.auth_token
        result['product_instance_id'] = self.product_instance_id
        result['region_name'] = self.region_name
        result['file_id'] = self.file_id
        return result

    def from_map(self, map={}):
        self.auth_token = map.get('auth_token')
        self.product_instance_id = map.get('product_instance_id')
        self.region_name = map.get('region_name')
        self.file_id = map.get('file_id')
        return self


class GetNtcloudGatewayxFileDownloadResponse(TeaModel):
    # 创建文件使用的apiCode
    # 文件下载地址
    # 下载超时时间
    # 文件标签
    # 请求上传时的自定义元数据
    # 文件名
    # 文件路径
    # 文件大小
    # 上传的调用者信息
    def __init__(self, req_msg_id=None, result_code=None, result_msg=None, api_code=None, download_url=None, expired_time=None, file_label=None, file_metadata=None, file_name=None, file_path=None, file_size=None, upload_invoker=None):
        self.req_msg_id = req_msg_id
        self.result_code = result_code
        self.result_msg = result_msg
        self.api_code = api_code
        self.download_url = download_url
        self.expired_time = expired_time
        self.file_label = file_label
        self.file_metadata = file_metadata
        self.file_name = file_name
        self.file_path = file_path
        self.file_size = file_size
        self.upload_invoker = upload_invoker

    def validate(self):
        if self.expired_time:
            self.validate_pattern(self.expired_time, 'expired_time', '\\d{4}[-]\\d{1,2}[-]\\d{1,2}[T]\\d{2}:\\d{2}:\\d{2}[Z]')
        if self.upload_invoker:
            self.upload_invoker.validate()

    def to_map(self):
        result = {}
        result['req_msg_id'] = self.req_msg_id
        result['result_code'] = self.result_code
        result['result_msg'] = self.result_msg
        result['api_code'] = self.api_code
        result['download_url'] = self.download_url
        result['expired_time'] = self.expired_time
        result['file_label'] = self.file_label
        result['file_metadata'] = self.file_metadata
        result['file_name'] = self.file_name
        result['file_path'] = self.file_path
        result['file_size'] = self.file_size
        if self.upload_invoker is not None:
            result['upload_invoker'] = self.upload_invoker.to_map()
        else:
            result['upload_invoker'] = None
        return result

    def from_map(self, map={}):
        self.req_msg_id = map.get('req_msg_id')
        self.result_code = map.get('result_code')
        self.result_msg = map.get('result_msg')
        self.api_code = map.get('api_code')
        self.download_url = map.get('download_url')
        self.expired_time = map.get('expired_time')
        self.file_label = map.get('file_label')
        self.file_metadata = map.get('file_metadata')
        self.file_name = map.get('file_name')
        self.file_path = map.get('file_path')
        self.file_size = map.get('file_size')
        if map.get('upload_invoker') is not None:
            temp_model = InvokerInfo()
            self.upload_invoker = temp_model.from_map(map['upload_invoker'])
        else:
            self.upload_invoker = None
        return self
