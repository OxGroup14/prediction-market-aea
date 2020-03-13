from oef.agents import OEFAgent
from oef.schema import DataModel, Description, AttributeSchema


# Uncomment the following lines if you want more output
# import logging
# from oef.logger import set_logger
# set_logger("oef", logging.DEBUG)


class EchoServiceAgent(OEFAgent):
    """
    The class that defines the behaviour of the echo service agent.
    """

    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        print("[{}]: Received message: msg_id={}, dialogue_id={}, origin={}, content={}"
              .format(self.public_key, msg_id, dialogue_id, origin, content))
        print("[{}]: Sending {} back to {}".format(self.public_key, content, origin))
        self.send_message(1, dialogue_id, origin, content)


if __name__ == '__main__':

    # create agent and connect it to OEF
    server_agent = EchoServiceAgent("echo_server", oef_addr="127.0.0.1", oef_port=3333)
    server_agent.connect()

    # register a service on the OEF
    echo_feature = AttributeSchema("does_echo", bool, True, "Whether the service agent can do echo or not.")
    echo_model = DataModel("echo", [echo_feature], "echo service.")
    echo_description = Description({"does_echo": True}, echo_model)

    msg_id = 22
    server_agent.register_service(msg_id, echo_description)

    # run the agent
    print("[{}]: Waiting for messages...".format(server_agent.public_key))
    try:
        server_agent.run()
    finally:
        print("[{}]: Disconnecting...".format(server_agent.public_key))
        server_agent.stop()
        server_agent.disconnect()