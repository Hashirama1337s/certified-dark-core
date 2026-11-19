#!/bin/sh
cd code/r3
unset WSU
MC="python"
mkdir -p logs
NT="n1597 n1600 n1605 n1612 n1625 n1650 n1675 n1700 n1725 n1750 n1775 n1800 n1825 n1850 n1875 n1900 n1925 n1950 n1962 n1970 n1976 n1980 n1983"
for t in $NT; do echo "sealed 5e6d7bfed0" > SEALED-$t.ok; done
for i in $(seq 1 22); do c=$(printf 'c%02d' $i); echo "sealed 5e6d7bfed0" > SEALED-$c.ok; done
date
$MC verdict_w.py controls > logs/W_controls_presealrun.log 2>&1; grep -o '"all_pass": *[a-z]*' logs/W_controls_presealrun.log
for t in $NT; do echo "N:$t"; done | xargs -P 2 -I{} sh -c 'j="{}"; f=$(echo "$j" | tr ":" "_"); '"$MC"' -u assemble_w.py "$j" > logs/$f.log 2>&1; echo "$j exit $? $(date +%T)"'
date
for i in $(seq 1 22); do printf 'C:c%02d\n' $i; done | xargs -P 2 -I{} sh -c 'j="{}"; f=$(echo "$j" | tr ":" "_"); '"$MC"' -u assemble_w.py "$j" > logs/$f.log 2>&1; echo "$j exit $? $(date +%T)"'
date
$MC verdict_w.py window > logs/W_window_verdict.log 2>&1; echo "window verdict exit $?"
date
