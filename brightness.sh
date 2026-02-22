#!/bin/bash

BRIGHTNESS=${1:-512}

gpio pwm-ms
gpio pwmr 1024
gpio pwmc 16
gpio -g mode 18 pwm
gpio -g pwm 18 $BRIGHTNESS
