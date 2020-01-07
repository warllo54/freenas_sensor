# Freenas Sensor

This will create a sensor to monitor the status of your freenas box via the freenas api.

### Installation

Copy this folder to `<config_dir>/custom_components/freenas_sensor/`.

Add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
sensor:
  - platform: freenas_sensor
    host: IP Address of FreeNAS box
    password: Password of FreeNAS box
    port: 80
    username: Freenas username
    method: http
    name: give the sensor a descriptive name
```
