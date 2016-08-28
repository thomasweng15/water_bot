from datetime import datetime
import twilio.rest as twilio

class TwilioClient:
	def __init__(self, account_sid, auth_token):
		self.client = twilio.TwilioRestClient(
			account_sid,
			auth_token
		)

	def send(self, to, from_, body):
		try: 
			message = self.client.messages.create(
				to = to,
				from_ = from_,
				body = body
			)
		
			print datetime.now().time()
			print "to:" + to
			print "from:" + from_ 
			print "body:" + body
		except twilio.exceptions.TwilioRestException as e:
			print e

