#!/bin/bash

vpns=$(systemctl list-unit-files --all | egrep "^vpn_" | awk '{print $1}')

for vpn in $vpns; do
  case `systemctl status $vpn | awk '/   Active: / {print $2}'` in
    active)    color="green"; state="up";;
    inactive)  color="red";   state="down";;
  esac

  case $vpn in
    vpn_aq.service)          vpn="AsureQuality";;
    vpn_catalyst.service)    vpn="Catalyst";;
    vpn_greenpeace.service)  vpn="Greenpeace";;
    vpn_loyalty.service)     vpn="Loyalty";;
  esac

  printf '${color}%-15s\t${color %s}%s${color}\n' $vpn $color $state
done

exit
