# whatsapp_msg_cm.com

This libray helps you to send messages on whatsapp via cm.com

mesgclient = cm_whatsapp.MessagingClient(product_token="90C21844-AA70-4E92-AEE3-6BB948D9C761",name_space="96962ea1_cb2b_4990_8503_087573a9a406")
#number must be in the format example 00919582676681 -> 00 ->country code 91 -> mobile_number 9582676681
mesgclient.sendTextmessage(message="Hello world",to_numbers=["00919582676681"]) 
