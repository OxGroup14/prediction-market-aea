#!/bin/bash
sleep 5
python aea_server.py & #--addr oef-node --port 10000
sleep 5
python aea_client.py
