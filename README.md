[](https://github.com/user-attachments/assets/af210934-4651-4c5d-a316-91d5e0f595a6)

# RaspiBlitz Barracuda

A custom-built [RaspiBlitz](https://github.com/rootzoll/raspiblitz) — a DIY Bitcoin full node running together with a Lightning node on a Raspberry Pi — housed in a 3D-printed chassis with UPS battery backup, fan control, and an LCD touchscreen.

## Components

| Component | Notes |
|-----------|-------|
| [Raspberry Pi 4](https://www.amazon.com/dp/B07TC2BK1X) (4GB or 8GB) | Main board |
| [SanDisk SSD PLUS 1TB](https://www.amazon.com/gp/product/B07D998212) | Blockchain storage |
| [UGREEN 2.5" Hard Drive Enclosure](https://www.amazon.com/gp/product/B06XWRRMYX) | SSD enclosure |
| MicroSD Card 32GB | Boot drive |
| Waveshare [3.5" RPi LCD (B)](https://www.waveshare.com/wiki/3.5inch_RPi_LCD_(B)) | Touchscreen display |
| [Raspberry Pi 4 Official PSU](https://www.amazon.com/dp/B07W8XHMJZ) | 15W USB-C power supply |
| [Dual Fan Heatsink Case](https://www.amazon.com/dp/B07VWM4J4L) | Cooling |
| [UPS Lite 18650](https://www.aliexpress.com/item/32955634965.html) ([GitHub](https://github.com/linshuqin329/UPS-18650-Lite)) | Battery backup |
| [40 Pin Stacking Header](https://www.aliexpress.com/item/1005002288358695.html) (8.6mm) | LCD clearance over heatsink |
| [USB 3.0 Micro-B Ribbon Cable](https://www.aliexpress.com/item/4001289178964.html) (S3-W7, 0.1m) | SSD connection |
| 4010 Cooling Fan 40mm | Additional cooling |
| Micro Mini JST 2.0 PH Connectors (3 & 4 pin) | UPS / fan wiring |
| 12mm LED Momentary Switch (6V, Yellow) | Power/reset button |
| 30 & 24 AWG Flexible Silicone Wire | Internal wiring |

## Setup

Follow the RaspiBlitz [setup instructions](https://docs.raspiblitz.org/docs/setup/intro) to install the software, then apply the hardware customizations below.

A full [connections schematic](raspiblitz-barracuda-connections.pdf) is included in the repo.

## 3D-Printed Chassis

Print files are in the [`chassis/`](chassis/) directory:

- `chassis.3mf` — main enclosure
- `cover.3mf` — top cover
- `lightning-bolt.3mf` — decorative emblem
- `barracuda.f3d` — Fusion 360 source

## Power-On / Reset Switch

Connect a momentary switch between **GPIO3** and **GND**. Use a switch with an integrated LED for the activity indicator.

## Activity LED

1. Connect an LED to **GPIO16** via a 220 ohm resistor.
2. Add to `/boot/config.txt`:
   ```
   dtparam=act_led_gpio=16
   ```

## Fan Control

Connect **GPIO14** via a 1k ohm resistor to a BC547 transistor to switch the fans (heatsink case fans or an additional external one).

Add to `/boot/config.txt`:
```
dtoverlay=gpio-fan,gpiopin=14,temp=60000
```

## LCD

Follow the [Waveshare setup instructions](https://www.waveshare.com/wiki/3.5inch_RPi_LCD_(B)#Software_Settings).

### Backlight Brightness

1. Short the jumper as described in the [Waveshare documentation](https://www.waveshare.com/wiki/3.5inch_RPi_LCD_(B)#Control_Backlight_Brightness_Using_GPIO).
2. Use [`brightness.sh`](brightness.sh) to set brightness (0–1024):
   ```bash
   ./brightness.sh 800
   ```

## UPS Lite 18650

In this build the UPS Lite is **not** mounted as a HAT — it is wired directly:

- **GPIO2 / GPIO3 (I2C)** — battery state readout
- **GPIO4** — external power detection

See the [wiring photo](UPS-18650-Lite/UPS-18650-Lite-Connections.jpg).

### External Power Detection

Short the jumper as described in the [UPS Lite documentation](UPS-18650-Lite/Instructions%20for%20UPS-18650-Lite%20V1.2.pdf). The external power state can be read via **GPIO4**.

### Auto Shutdown

A systemd service monitors battery capacity and triggers a safe shutdown at 1% to prevent data corruption before the hardware protection cuts power.

#### Setup

1. **Enable I2C:**
   ```bash
   # Add or uncomment in /boot/config.txt:
   dtparam=i2c_arm=on

   # Add to /etc/modules (if not already present):
   echo "i2c-dev" | sudo tee -a /etc/modules

   sudo reboot
   ```
2. **Verify I2C** (should show `0x36` for the MAX17040G fuel gauge):
   ```bash
   sudo apt install -y i2c-tools
   sudo i2cdetect -y 1
   ```
3. **Install the monitor service:**
   ```bash
   cp UPS-18650-Lite/ups_shutdown.py /home/pi/
   sudo cp UPS-18650-Lite/ups_monitor.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now ups_monitor.service
   ```
4. **Verify:**
   ```bash
   sudo systemctl status ups_monitor.service
   sudo journalctl -u ups_monitor.service -n 50
   ```
