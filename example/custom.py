import time
from smsactivateru import Sms, SmsTypes, SmsService, GetBalance, GetFreeSlots, GetNumber, SetStatus, GetStatus

"""
create wrapper with secret api-key
search here: http://sms-activate.ru/index.php?act=profile)
"""
wrapper = Sms('API KEY')

# getting balance
balance = GetBalance().request(wrapper)
# show balance
print(f'На счету {balance} руб.')

# getting free slots (count available phone numbers for each services)
available_phones = GetFreeSlots(
	country=SmsTypes.Country.RU
).request(wrapper)
# show for vk.com, whatsapp and youla.io)
print(f'vk.com: {available_phones.VkCom.count} номеров')
print(f'whatsapp: {available_phones.Whatsapp.count} номеров')
print(f'youla.io: {available_phones.Youla.count} номеров')

# try get phone for youla.io
activation = GetNumber(
	service=SmsService().Youla,
	country=SmsTypes.Country.RU,
	operator=SmsTypes.Operator.Beeline
).request(wrapper)
# show activation id and phone for reception sms
print(f'id: {str(activation.id)} phone: {str(activation.phone_number)}')

# getting and show current activation status
response = GetStatus(id=activation.id).request(wrapper)
print(response)

# .. send phone number to you service
user_action = input('Press enter if you sms was sent or type "cancel": ')
if user_action == 'cancel':
	set_as_cancel = SetStatus(
		id=activation.id,
		status=SmsTypes.Status.Cancel
	).request(wrapper)
	print(set_as_cancel)
	exit(1)

# set current activation status as SmsSent (code was sent to phone)
set_as_sent = SetStatus(
	id=activation.id,
	status=SmsTypes.Status.SmsSent
).request(wrapper)
print(set_as_sent)

# .. wait code
while True:
	time.sleep(1)
	response = GetStatus(id=activation.id).request(wrapper)
	if response['code']:
		print(f"Your code:{response['code']}")
		break

# set current activation status as End (you got code and it was right)
set_as_end = SetStatus(
	id=activation.id,
	status=SmsTypes.Status.End
).request(wrapper)
print(set_as_end)
