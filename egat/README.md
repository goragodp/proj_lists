# Electricity Generating Authority of Thailand (EGAT)
> The program is a part of larger system which was develop for EGAT. These 2 modules is my responsible
###  1. Data collection program
>The program collect the neccessary data from API of the another system to create a dataset for AI. The program utilize threading and built-in linux command called 'cron' to create schedule collection
- Framework : requests, threading, cron
- language  : python

###  2. RL for learning with custom environment
>The program create a simulated system of power plant as a environment for the agent to interface with specific rules.
- Framework : stable-baseline3
- language  : python

