from twilio.rest import Client

def send_sms(tele_number, message):
    client = Client("AC6fb021795f694c9e6aff2dc9fe475f29", "938f28436651c03314ec96a9ffbf8abd")
    client.messages.create(to=str(tele_number), from_="+12029335545", body=str(message))

    print("Done Send")


# send_sms('+84334535251', 'hello')