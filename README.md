## E-Bike Power & Range Calculator

This Python command-line utility acts as an electric bike speed, power, and mileage calculator. It helps e-bike builders and riders estimate real-world performance metrics based on empirical calibration data.

### Features

* **Calculate Range:** Estimates your maximum range (in km) based on your riding speed and battery capacity.
* **Calculate Required Capacity:** Determines the battery capacity needed to achieve a specific target range at a given speed.
* **Calculate Average Speed:** Estimates the average speed required to reach a target range with a specific battery capacity.
* **Flexible Inputs:** Accepts battery capacity in total Watt-hours (Wh) or as a Voltage multiplied by Amp-hours format (e.g., `48*15`).

### How It Works

The calculator uses several assumptions and mathematical models to provide realistic estimates:
* **Usable Battery Limit:** It factors in an 85% depth (configurable value) of discharge limit to represent usable capacity and preserve battery cycle life.
* **Empirical Data:** Power requirements for specific speeds (ranging from 20 km/h to 80 km/h) are based on third-party empirical measurement data sourced from `e4bike.ru`.
* **Linear Interpolation:** The script dynamically calculates power and speed requirements between the fixed calibration points using linear interpolation.

### Credits & License

* **Author:** Vibecoded in Gemini 3.1 Pro by s0me0ne-25.
* **License:** Non-Copyright: AI Work / Licensed under Creative Commons CC0.
