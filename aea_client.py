#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#
#   Copyright 2018 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------


"""
Echo client agent
~~~~~~~~~~~~~~~~~
This script belongs to the ``echo`` example of OEF Agent development, and implements the echo client agent.
It assumes that an instance of the OEF Node is running at ``127.0.0.1:3333``.
The script does the following:
1. Instantiate a ``EchoClientAgent``
2. Connect the agent to the OEF Node.
3. Make a query on ``echo`` services via the ``search_services`` method.
4. Run the agent, waiting for messages from the OEF.
The class ``EchoClientAgent`` define the behaviour of the echo client agent.
* when the agent receives a search result from the OEF (see ``on_search_result``), it sends an "hello" message to
  every agent found.
* once he receives a message (see ``on_message`` method), he stops.
Other methods (e.g. ``on_cfp``, ``on_error`` etc.) are omitted, since not needed.
"""
from typing import List

from oef.agents import OEFAgent
from oef.schema import DataModel, AttributeSchema
from oef.query import Query, Constraint, Eq
import asyncio

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
    client_agent = EchoClientAgent("echo_client", oef_addr="oef-node", oef_port=10000, loop = asyncio.get_event_loop())

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
