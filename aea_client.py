from typing import List

from oef.agents import OEFAgent
from oef.schema import DataModel, AttributeSchema
from oef.query import Query, Constraint, Eq


# Uncomment the following lines if you want more output
# import logging
# from oef.logger import set_logger
# set_logger("oef", logging.DEBUG)


class EchoClientAgent(OEFAgent):
    """
    The class that defines the behaviour of the echo client agent.
    """

    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        print("[{}]: Received message: msg_id={}, dialogue_id={}, origin={}, content={}"
              .format(self.public_key, msg_id, dialogue_id, origin, content))
        print("[{}]: Stopping...".format(self.public_key))
        self.stop()

    def on_search_result(self, search_id: int, agents: List[str]):
        if len(agents) > 0:
            print("[{}]: search_id={}. Agents found: {}".format(self.public_key, search_id, agents))
            msg = b"hello"
            for agent in agents:
                print("[{}]: Sending {} to {}".format(self.public_key, msg, agent))
                self.send_message(0, 0, agent, msg)
        else:
            print("[{}]: No agent found. Stopping...".format(self.public_key))
            self.stop()


if __name__ == '__main__':

    # define an OEF Agent
    client_agent = EchoClientAgent("echo_client", oef_addr="127.0.0.1", oef_port=3333)

    # connect it to the OEF Node
    client_agent.connect()

    # create a query for the echo data model
    echo_feature = AttributeSchema("does_echo", bool, True, "Whether the service agent can do echo.")
    echo_model = DataModel("echo", [echo_feature], "echo service.")
    echo_query = Query([Constraint("does_echo", Eq(True))], echo_model)

    print("[{}]: Make search to the OEF".format(client_agent.public_key))
    client_agent.search_services(0, echo_query)

    # wait for events
    try:
        client_agent.run()
    finally:
        print("[{}]: Disconnecting...".format(client_agent.public_key))
        client_agent.stop()
        client_agent.disconnect()
