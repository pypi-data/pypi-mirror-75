from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
import threading

message = ''
my_listener = SubscribeListener()


def receive(channel):
    while 1:
        result = my_listener.wait_for_message_on(str(channel))
        global message
        message = str(result.message)


class MessageManager:
    pkey = None
    skey = None
    dId = None
    cN = None
    pubnub = None
    global message
    global my_listener

    def __init__(self, publish_key, subscribe_key, device_id, channel_name):
        self.pkey = publish_key
        self.skey = subscribe_key
        self.dId = device_id
        self.cN = channel_name
        pnconfig = PNConfiguration()

        pnconfig.publish_key = str(self.pkey)
        pnconfig.subscribe_key = str(self.skey)

        self.pubnub = PubNub(pnconfig)

        global my_listener
        my_listener = SubscribeListener()
        self.pubnub.add_listener(my_listener)

        self.pubnub.subscribe().channels(str(self.cN)).execute()
        my_listener.wait_for_connect()

    def start_listening(self):
        x = threading.Thread(target=receive, args=(self.cN,))
        x.start()

    def get_message(self):
        global message
        if message != '' and message is not None:
            try:
                pos = message.index(' ')
                if message[0:pos] != str(self.dId):
                    identification = str(message[0:pos])
                    m = str(message[pos+1:])
                    message = ''
                    return identification, m
                else:
                    return None, None
            except ValueError:
                return None, None
        else:
            return None, None

    def publish_message(self, msg):
        self.pubnub.publish().channel(self.cN).message(str(self.dId) + ' ' + str(msg)).sync()



