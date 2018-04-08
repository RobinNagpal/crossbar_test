from crochet import run_in_reactor, setup, wait_for

setup()

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp import PublishOptions
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.component import Component

PRINCIPAL = 'notification_service'
PRINCIPAL_TICKET = 'secret-secret-service'


class WampClientSession(ApplicationSession):

    def onConnect(self):
        print("Client session connected. Starting WAMP-Ticket authentication on realm '{}' as principal '{}' ..".format(
            self.config.realm, PRINCIPAL))
        self.join(self.config.realm, [u"ticket"], PRINCIPAL)

    def onChallenge(self, challenge):
        if challenge.method == u"ticket":
            print("WAMP-Ticket challenge received: {}".format(challenge))
            return PRINCIPAL_TICKET
        else:
            raise Exception("Invalid authmethod {}".format(challenge.method))

    @inlineCallbacks
    def onJoin(self, details):
        print("Client session joined: {}".format(details))
        self._parent = self.config.extra['parent']
        self._parent.started(self)
        yield "sss"

        # counter = 0
        # while True:
        #     msg = u'counter is at {}'.format(counter)
        #     pub = yield self.publish(u'com.crossbar_test.notification', msg, options=PublishOptions(exclude_me=False, acknowledge=True))
        #     self.log.info('event published: {pub}', pub=pub)
        #     counter += 1
        #     yield sleep(1)

    def onLeave(self, details):
        print("Client session left: {}".format(details))
        self.disconnect()

    def onDisconnect(self):
        print("Client session disconnected.")


def callback(arg):
    print("Started NotificationService WAMP Client", arg)


component = Component()


class NotificationService(ApplicationSession):

    # def start(self):
    #     self._runner = ApplicationRunner(url=u'ws://localhost:8080/ws',
    #                                      realm=u"realm1",
    #                                      extra=dict(parent=self))
    #     self._runner.run(WampClientSession, log_level='info')

    def __init__(self):
        @run_in_reactor
        def start_wamp():
            # self.wapp = Application()
            self._runner = ApplicationRunner(url=u'ws://localhost:8080/ws',
                                             realm=u"realm1",
                                             extra=dict(parent=self))
            self.wapp = self._runner.run(WampClientSession, log_level='debug', start_reactor=False)

            # self.wapp.run(u"ws://127.0.0.1:8080/ws", u"realm1", start_reactor=False)

        start_wamp()

    def started(self, client):
        print("Started NotificationService WAMP Client", client)
        self.wamp_client = client
        # try:
        #     print("Okay")
        #     return_val = client.publish("com.crossbar_test.notification", "hello",
        #                                 options=PublishOptions(acknowledge=True))
        #     return_val.addCallback(callback)
        #     return_val.addErrback(callback)
        #     print("ok, event published to topic {}".format("com.crossbar_test.notification"), return_val)
        # except Exception as e:
        #     print("publication to topic {} failed (this is expected!) {}".format("com.crossbar_test.notification", e))

    @wait_for(timeout=3)
    def publish_message(self, user_id, message):
        print("will try to send message")
        try:
            print("Okay")
            return_val = self.wamp_client.publish(
                "com.crossbar_test.notification",
                "hello",
                options=PublishOptions(
                    acknowledge=True,
                    eligible_authid=user_id
                )
            )
            return_val.addCallback(callback)
            return_val.addErrback(callback)
            print("ok, event published to topic {}".format("com.crossbar_test.notification"), return_val)
        except Exception as e:
            print("publication to topic {} failed (this is expected!) {}".format("com.crossbar_test.notification", e))

        # try:
        #     yield self.wamp_client.publish(
        #         "com.crossbar_test.notification",
        #         message,
        #         options=PublishOptions(
        #             acknowledge=True,
        #             eligible_authid=user_id
        #         )
        #     )
        #     print("ok, event published to topic {}".format("com.crossbar_test.notification"))
        # except Exception as e:
        #     print("publication to topic {} failed (this is expected!) {}".format("com.crossbar_test.notification", e))
        # "sent message"
