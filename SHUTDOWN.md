# Shutdown Raspberry Pi with a Single Button

Connect [Boot Button](https://pinout.xyz/pinout/pin5_gpio3#) via a momentary switch to GND:
- Physical/Board pin 5 - GPIO/BCM pin 3 (this is [I2C](https://pinout.xyz/pinout/i2c#)1/SCL, so I2C will be disturbed by a button press)
- GND pin 6

## Boot Overlay

In system version 225 and above, power-down and power-up is possible via shorting [GPIO3 (pin 5)](https://pinout.xyz/pinout/pin5_gpio3#). 
This functionality is enabled by adding the following line to `/boot/config.txt` and restarting:

```
dtoverlay=gpio-shutdown,gpio_pin=3
```

Note: the qualifier `gpio_pin=3` is redundant since this pin is the default.

GPIO3 has an external pull-up, so shorting to ground briefly will initiate a shutdown.  
A subsequent short to ground (provided power is still applied) will power-on the system.

The [boot overlay documentation](https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README) for this function is as follows:

```
Name:   gpio-shutdown
Info:   Initiates a shutdown when GPIO pin changes. The given GPIO pin
        is configured as an input key that generates KEY_POWER events.

        This event is handled by systemd-logind by initiating a
        shutdown. Systemd versions older than 225 need an udev rule
        enable listening to the input device:

                ACTION!="REMOVE", SUBSYSTEM=="input", KERNEL=="event*", \
                        SUBSYSTEMS=="platform", DRIVERS=="gpio-keys", \
                        ATTRS{keys}=="116", TAG+="power-switch"

        Alternatively this event can be handled also on systems without
        systemd, just by traditional SysV init daemon. KEY_POWER event
        (keycode 116) needs to be mapped to KeyboardSignal on console
        and then kb::kbrequest inittab action which is triggered by
        KeyboardSignal from console can be configured to issue system
        shutdown. Steps for this configuration are:

            Add following lines to the /etc/console-setup/remap.inc file:

                # Key Power as special keypress
                keycode 116 = KeyboardSignal

            Then add following lines to /etc/inittab file:

                # Action on special keypress (Key Power)
                kb::kbrequest:/sbin/shutdown -t1 -a -h -P now

            And finally reload configuration by calling following commands:

                # dpkg-reconfigure console-setup
                # service console-setup reload
                # init q

        This overlay only handles shutdown. After shutdown, the system
        can be powered up again by driving GPIO3 low. The default
        configuration uses GPIO3 with a pullup, so if you connect a
        button between GPIO3 and GND (pin 5 and 6 on the 40-pin header),
        you get a shutdown and power-up button. Please note that
        Raspberry Pi 1 Model B rev 1 uses GPIO1 instead of GPIO3.
Load:   dtoverlay=gpio-shutdown,<param>=<val>
Params: gpio_pin                GPIO pin to trigger on (default 3)
                                For Raspberry Pi 1 Model B rev 1 set this
                                explicitly to value 1, e.g.:

                                    dtoverlay=gpio-shutdown,gpio_pin=1

        active_low              When this is 1 (active low), a falling
                                edge generates a key down event and a
                                rising edge generates a key up event.
                                When this is 0 (active high), this is
                                reversed. The default is 1 (active low).

        gpio_pull               Desired pull-up/down state (off, down, up)
                                Default is "up".

                                Note that the default pin (GPIO3) has an
                                external pullup. Same applies for GPIO1
                                on Raspberry Pi 1 Model B rev 1.

        debounce                Specify the debounce interval in milliseconds
                                (default 100)
```
