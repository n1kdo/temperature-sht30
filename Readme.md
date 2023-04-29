# Raspberry Pi Pico W Temperature and Humidity

This runs on Raspberry Pi Pico W and uses a SHT30 temperature and humidity sensor.  

It provides the temperature and humidity values on a locally-hosted web page, and through 
the `/api/status` API which returns a JSON document containing timestamp, temperature,
and humidity values.

## hardware

This uses a Raspberry Pi Pico W and a SHT30 sensor (from Amazon).

The sensor is wired to the Pico W as follows:

| wire color | purpose | pin # | pin label |
|------------|---------|-------|-----------|
| Red        | +v      | 36    | 3v3 out   |
| White      | SDA     | 6     | GP4       |
| Yellow     | SCL     | 7     | GP5       |
| Black      | ground  | 8     | GND       |

Note that both SDA and SCL require 10K pull-up resistors to 3V3 OUT. I put the resistors 
on a small board midway in the wiring between the Pico W and the SHT30.

### Other important wiring

| device                         | purpose                   | pin # | pin label |
|--------------------------------|---------------------------|-------|-----------|
| LED to ground through 330 ohms | morse code status message | 4     | GP2       |
| Pushbutton to ground           | select AP mode            | 5     | GP3       |


### setup

1. press the AP mode button and the device will restart in access point mode. 
2. connect to the 'sht30' WiFi network using password 'temperature'.  
3. your phone or tablet may resist staying connected to this network as the internet is unreachable through it. 
   this needs to be dealt with on that device.
4. navigate to http://192.168.4.1 which should show the temperature page.
5. click the 'setup' link in the lower left.
6. set your SSID and password on this page.
7. press 'apply' and then 'restart'.
8. the device should connect to your network.

### software

This uses some of the same software I wrote for my
[Ham-IV Rotator Controller-Controller](https://github.com/n1kdo/rotator-controller-controller).

n1kdo 20221217



