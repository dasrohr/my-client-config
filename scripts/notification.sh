#!/bin/bash
#

actions=('check_bat')

check_bat(){

  path_ac='/org/freedesktop/UPower/devices/line_power_AC'
  path_bat='/org/freedesktop/UPower/devices/battery_BAT0'
t
  state_ac=$(upower -i $path_ac | awk '/online:/ {print $2}')
  state_bat=$(upower -i $path_bat | awk '/percentage:/ {print $2}' | sed 's/%//')

  if [ "$state_ac" != "yes" ]; then
    if [ $state_bat -le 10 ]; then
      notity
    fi
  fi

}

while :
do

  for action in ${actions[@]}; do
    action
    sleep 2
  done

done
