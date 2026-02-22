The [RaspiBlitz](https://github.com/rootzoll/raspiblitz) is a DIY Bitcoin full node running together with a Lightning node on a Raspberry Pi with a touchscreen display for easy setup & monitoring.

Components
- [SanDisk SSD PLUS 1TB Internal SSD](https://www.amazon.com/gp/product/B07D998212)
- [UGREEN 2.5" Hard Drive Enclosure](https://www.amazon.com/gp/product/B06XWRRMYX)
- MicroSD Card 32GB
- Waveshare [3.5inch RPi LCD](https://www.waveshare.com/wiki/3.5inch_RPi_LCD_(B))
- [Raspberry Pi 4 Official PSU](https://www.amazon.com/dp/B07W8XHMJZ) (or any 15W USB-C power supply)
- [RaspberryPi 4](https://www.amazon.com/dp/B07TC2BK1X) 4GB (or 8GB)
- [Dual Fan Heatsink Case](https://www.amazon.com/dp/B07VWM4J4L) for Raspberry Pi 4
- [40 Pin Stacking Female Header Kit for Raspberry Pi](https://www.aliexpress.com/item/1005002288358695.html), 8;6mm
- [USB 3.0 Micro-B Ribbon Flat Cable](https://www.aliexpress.com/item/4001289178964.html), S3-W7 (USB A Male Down, Micro-B Up), 0.1m
- [UPS Lite 18650](https://www.aliexpress.com/item/32955634965.html) ([GitHub](https://github.com/linshuqin329/UPS-18650-Lite))
- 4010 Cooling Fan 40MM
- Micro Mini JST 2.0 PH Connectors, Male & Female, 3 & 4 pin
- 12mm LED Momentary Switches 6V Yellow
- 30 & 24 AWG Flexible Silicone Wire Cables (multiple colors)

Follow the RaspiBlitz [setup instructions](https://docs.raspiblitz.org/docs/setup/intro).


## Power-on/reset switch

Connect a momentary switch between GPIO3 and GND.
Use a switch with an integrated LED for the activity indicator.


## Activity LED

Connect LED to GPIO16 via 220 ohm resistor.
Add `dtparam=act_led_gpio=16` to `/boot/config.txt`.


## Fan control (optional)

Add to `/boot/config.txt`:
```
dtoverlay=gpio-fan,gpiopin=14,temp=60000
```

Connect GPIO14 via 1k resistor to a BC547 transistor to control fans (in the heatsink case or an additional external one).
See the [connections schematic](raspiblitz-barracuda-connections.pdf).


## LCD

Follow the [Waveshare setup instructions](https://www.waveshare.com/wiki/3.5inch_RPi_LCD_(B)#Software_Settings).

### LCD Backlight Brightness

1. Short the jumper as instructed in the [Waveshare documentation](https://www.waveshare.com/wiki/3.5inch_RPi_LCD_(B)#Control_Backlight_Brightness_Using_GPIO).
2. Use [brightness.sh](brightness.sh) to control brightness, use a value between 0 to 1024, e.g. `./brightness.sh 800`.


## UPS Lite 

In the custom encoluse, the UPS Lite is not connected as a HAT.
You can wire the connections (GPIO2,3 for reading state via I2C, GPIO4 for external power detection). See [here](UPS-18650-Lite/UPS-18650-Lite-Connections.jpg).

### External power detection

Short the jumper as instructed [in the documentation](UPS-18650-Lite/Instructions for UPS-18650-Lite V1.2.pdf).
The indication can be read via GPIO4.

### Auto Shutdown

It is recommended to trigger a shutdown when the battery capacity reaches 1% to avoid data corruption before the hardware protection cuts power.

1. Enable I2C
- Add or uncomment `dtparam=i2c_arm=on` to `/boot/config.txt`
- Add `i2c-dev` to `/etc/modules` if it's not already there
- Reboot
- Install i2c-tools: `sudo apt install -y i2c-tools`
- Scan the bus `sudo i2cdetect -y 1` - you should see 0x62 for the UPS CW2015 interface
- You can optionally run the script in the UPS Lite docs to see the reported status
2. Put `ups_shutdown.py` under `/home/pi`
3. Put `ups_monitor.service` under `/etc/systemd/system/`
4. Reload the systemd daemon: `sudo systemctl daemon-reload`
5. Enable the service: `sudo systemctl enable ups_monitor.service`
6. Start the service: `sudo systemctl start ups_monitor.service`
7. Verify it is active: `sudo systemctl status ups_monitor.service`
8. View the service logs: `sudo journalctl -u ups_monitor.service -n 50`
