from twilio.rest import Client


account_sid = 'AC4f48f2ecb88fb26a8df6bacaf3782b86'
auth_token = '44b4331d10baf78bd4c816d713af357a'
    
client = Client(account_sid, auth_token)

message = client.messages.create(
    body="testing",
    from_="+12029295842",
    to='+17864060440',
)


print(message.sid)