#!/bin/bash
sleep 15
python aea_server.py & #--addr oef-node --port 10000
sleep 15
python aea_client.py
