# Design Notes

System summary:
- Automatic regulation: water-level and temperature are maintained by pumping water from a maintenance tank into pool and vice-versa.
- Alerts: turbidity, chlorine, humidity, and sensor failure trigger immediate alerts (buzzer + email).
- Data storage: ThingSpeak used for cloud logging and visualization.

Safety:
- Always drive pumps via appropriate relays/motor drivers; never directly from MCU pins.
- Use opto-isolated relay modules and fuses for the pump supply.
- Make sure to use proper waterproof sensors and cable glands.

Calibration:
- pH: calibrate with buffer solutions (pH 4, 7, 10).
- Turbidity / Chlorine: use calibration samples / standards and perform linear/regression mapping from ADC to real units.
