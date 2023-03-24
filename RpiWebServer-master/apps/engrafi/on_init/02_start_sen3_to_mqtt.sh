#!/bin/bash
cd /etc/sen3-pi
/usr/bin/python3 sen3a.py >/etc/sen3-pi/log/sen3.tomqtt.log &
