#!/bin/bash
cd /etc/sen3-pi
/usr/bin/python3 main.py >/etc/sen3-pi/log/sen3.main.log &
/usr/bin/python3 rule1.py >/etc/sen3-pi/log/sen3.rule1.log &
