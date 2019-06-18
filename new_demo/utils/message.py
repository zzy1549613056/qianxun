from aliyunsdkcore.request import RpcRequest
from aliyunsdkcore.client import AcsClient
import uuid,json
from aliyunsdkcore.profile import region_provider



class SendSmsRequest(RpcRequest):
	def __init__(self):
		RpcRequest.__init__(self, 'Dysmsapi', '2017-05-25', 'SendSms')

	def set_TemplateCode(self,TemplateCode):
		self.add_query_param('TemplateCode',TemplateCode)

	def set_PhoneNumbers(self,PhoneNumbers):
		self.add_query_param('PhoneNumbers',PhoneNumbers)

	def set_SignName(self,SignName):
		self.add_query_param('SignName',SignName)

	def set_ResourceOwnerAccount(self,ResourceOwnerAccount):
		self.add_query_param('ResourceOwnerAccount',ResourceOwnerAccount)

	def set_TemplateParam(self,TemplateParam):
		self.add_query_param('TemplateParam',TemplateParam)

	def set_ResourceOwnerId(self,ResourceOwnerId):
		self.add_query_param('ResourceOwnerId',ResourceOwnerId)

	def set_OwnerId(self,OwnerId):
		self.add_query_param('OwnerId',OwnerId)

	def set_SmsUpExtendCode(self,SmsUpExtendCode):
		self.add_query_param('SmsUpExtendCode',SmsUpExtendCode)

	def set_OutId(self,OutId):
		self.add_query_param('OutId',OutId)

class MessageAPI():
	KEY_ID = "MESSAGE_KEY_ID"
	KEY_SECRET = "MESSAGE_KEY_SECRET"
	SIGN_NAME = "MESSAGE_SIGN_NAME"
	TEMPLATE_CODE = "MESSAGE_TEMPLATE_CODE"
	REGION = "cn-hangzhou"
	PRODUCT_NAME = "Dysmsapi"
	DOMAIN = "dysmsapi.aliyuncs.com"

	def __init__(self,app=None):
		if app:
			self.init_app(app)

	def init_app(self,app):
		config = app.config
		self.acs_client = AcsClient(config[self.KEY_ID],config[self.KEY_SECRET],self.REGION)
		region_provider.add_endpoint(self.PRODUCT_NAME, self.REGION, self.DOMAIN)
		self.template_code = config[self.TEMPLATE_CODE]
		self.sign_code = config[self.SIGN_NAME]


	def send_sms(self, phone_numbers,**template_param):
		_business_id = uuid.uuid1()
		smsRequest = SendSmsRequest()
		# 申请的短信模板编码,必填
		smsRequest.set_TemplateCode(self.template_code)
		# 短信模板变量参数
		if template_param is not None:
			smsRequest.set_TemplateParam(template_param)
		# 设置业务请求流水号，必填。
		smsRequest.set_OutId(_business_id)
		# 短信签名
		smsRequest.set_SignName(self.sign_code)
		# 短信发送的号码列表，必填。
		smsRequest.set_PhoneNumbers(phone_numbers)
		# 调用短信发送接口，返回json
		smsResponse = self.acs_client.do_action_with_exception(smsRequest)
		return json.loads(smsResponse.decode())


if __name__ == '__main__':

	class APP():
		config = {
			"MESSAGE_KEY_ID":"LTAIMhcythNhohBA",
			"MESSAGE_KEY_SECRET":"wgwVsNf8ryzsIPk65XZHHyZWGJeGnR",
			"MESSAGE_SIGN_NAME":"个人flask论坛",
			"MESSAGE_TEMPLATE_CODE":"SMS_137160152"
		}
	app = APP()
	message = MessageAPI(app)
	res = message.send_sms("13008335626",code="1234")
	print(res)


