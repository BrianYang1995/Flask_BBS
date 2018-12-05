from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider


class AlidayuAPI(object):

    REGION = "cn-hangzhou"
    PRODUCT_NAME = "Dysmsapi"
    DOMAIN = "dysmsapi.aliyuncs.com"

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):

        config = app.config

        self.access_key_id = config.get('ACCESS_KEY_ID')
        self.access_key_secret = config.get('ACCESS_KEY_SECRET')
        self.sign_name= config.get('SIGN_NAME')
        self.template_code = config.get('TEMPLATE_CODE')

        if not all([self.access_key_id, self.access_key_secret, self.sign_name, self.template_code]):
            raise Exception('ACCESS Fail')

        self.acs_client = AcsClient(self.access_key_id, self.access_key_secret, self.REGION)
        region_provider.add_endpoint(self.PRODUCT_NAME, self.REGION, self.DOMAIN)

    def send_sms(self, phone_numbers, **template_param):

        smsRequest = SendSmsRequest.SendSmsRequest()
        # 申请的短信模板编码,必填
        smsRequest.set_TemplateCode(self.template_code)

        # 短信模板变量参数
        if template_param is not None:
            smsRequest.set_TemplateParam(template_param)

        # 设置业务请求流水号，必填。
        __business_id = uuid.uuid1()
        smsRequest.set_OutId(__business_id)

        # 短信签名
        smsRequest.set_SignName(self.sign_name)

        # 短信发送的号码列表，必填。
        smsRequest.set_PhoneNumbers(phone_numbers)

        # 调用短信发送接口，返回json
        smsResponse = self.acs_client.do_action_with_exception(smsRequest)

        # TODO 业务处理

        return smsResponse