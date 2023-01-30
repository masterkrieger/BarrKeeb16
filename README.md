# BarrKeeb16
 This is a 16 key macro keypad with a rotary encoder, OLED display and under-glow RGB. BarrKeeb16 is running KMK firmware on the Seeed XIAO RP2040.
 
![BarrKeeb16_1](https://user-images.githubusercontent.com/1848365/215525772-2e19a67b-24e5-490f-b6b9-0f2c315ed285.jpg)
![BarrKeeb16_2](https://user-images.githubusercontent.com/1848365/215525108-cd2773e8-b6eb-42d3-a489-ce489db9ac39.jpg)

# Parts
1. BarrKeeb16 custom PCB. [JLCPCB](https://jlcpcb.com/)
2. Seeed XIAO RP2040. [Digikey](https://www.digikey.com/en/products/detail/seeed-technology-co-ltd/102010428/14672129?s=N4IgTCBcDaIB4EsCGB7ABAJwA5gAwBZcQBdAXyA) ― [SeeedStudio](https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html)
3. 16 × Diodes (SOD-123) [Digikey](https://www.digikey.ca/en/products/detail/smc-diode-solutions/1N4148W/6022450)
4. 16 × Cherry MX style switches. [Digikey](https://www.digikey.ca/en/products/detail/adafruit-industries-llc/4952/14113453) ― [Adafruit](https://www.adafruit.com/product/4952)
5. 16 × DSA style keycaps. [Digikey](https://www.digikey.ca/en/products/detail/adafruit-industries-llc/4998/14552195) ― [Adafruit](https://www.adafruit.com/product/4998)
6. 1 × Encoder (PEC11R). [Digikey](https://www.digikey.ca/en/products/detail/bourns-inc/PEC11R-4215F-S0024/4499665) ― [Adafruit](https://www.adafruit.com/product/377)
7. 4 × Neopixel 5050 (SK6812 or WS2812 _ 5mm × 5mm) [Digikey](https://www.digikey.ca/en/products/detail/adafruit-industries-llc/1655/5154679) ― [Adafruit](https://www.adafruit.com/product/1655)
8. 4 × 0.1 µF Capacitors 0603 (1608 Metric). [Digikey](https://www.digikey.ca/en/products/detail/samsung-electro-mechanics/CL10B104KB8NNNL/3894274)
9. 1 × Level shifter SOT-23-5. [Digikey](https://www.digikey.ca/en/products/detail/texas-instruments/74AHCT1G125DBVTG4/1687957)
10. 1 × PCF8574 IO Expander. [Digikey](https://www.digikey.ca/en/products/detail/nxp-usa-inc/PCF8574T-3-512/735690)
10. 1 × 10 kOhms Resistor 0805 (2012 Metric). [Digikey](https://www.digikey.ca/en/products/detail/stackpole-electronics-inc/RMCF0805JG10K0/1757769)
10. 1 × 4.7 kOhms Resistor 0805 (2012 Metric). [Digikey](https://www.digikey.ca/en/products/detail/stackpole-electronics-inc/RMCF0805JT4K70/1757774)
11. 5 × Screws (M2 × 2.5mm)
12. 4 × Rubber Bumper Feet. [Adafruit](https://www.adafruit.com/product/550)

# OLED Image
 If you want to replace the BarrKeeb16_screenlogo bitmap, create any black and white 128x64 pixel image and rename as 'BarrKeeb16_screenlogo.bmp' or 'BarrKeeb16_screenlogo_inverted.bmp' or modify the image filename in [display_logo.py](https://github.com/masterkrieger/BarrKeeb16/blob/main/Firmware/display_logo.py).
