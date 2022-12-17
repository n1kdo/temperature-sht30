# Raspberry Pi Pico W Temperature and Humidity

This runs on Raspberry Pi Pico W and uses a SHT30 temperature and humidity sensor.  

It provides the temperature and humidity values on a locally-hosted web page, and through 
the `/api/status` API which returns a JSON document containing timestamp, temperature,
and humidity values.

## hardware

This uses a Raspberry Pi Pico W and a SHT30 sensor (from Amazon?)

The sensor is wired to the Pico W as follows:

| wire color | purpose | pin # | pin label |
|------------|---------|-------|-----------|
| Red        | +v      | 36    | 3v3 out   |
| White      | SDA     | 6     | GP4       |
| Yellow     | SCL     | 7     | GP5       |
| Black      | ground  | 8     | GND       |

Note that both SDA and SCL require 10K pull-up resistors to 3V3 OUT. I put the resistors 
on a small board midway in the wiring between the Pico W and the SHT30.

n1kdo 20221217



