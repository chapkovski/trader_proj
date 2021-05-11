#!/bin/bash
#pkill -f otree
#rm -rf db.sqli*
#od &
#pid=$!
#sleep 5
#kill $pid
otree mocking_data baseline 10 &&
otree mocking_data fin 10 &&
otree mocking_data gamified 10 &&
otree mocking_data full 10 &&
od


