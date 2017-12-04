# RPi-Temp-Sensor
Monitor ambient temperature and send SMS temperature notifications from a Raspberry Pi

This program monitors ambient temperature using a Raspberry Pi and a DS18B20 temperature sensor that communicates over a 1-Wire bus.
If the ambient temperature goes above 76*F, the program will send a text message to a chosen recipient using GMail's SMTP server.

This project was created to monitor temperatures in a data center remotely and send early warning alerts to identify and resolve high ambient temperatures before it becomes a problem.

The program supports multiple DS18B20 sensors in parasite power mode.

To get started:

1. Edit server.login(<email address>, <email password>) to include your email and password
2. Edit server.sendmail() to include your carrier-specific SMS gateway
3. Find the address of each connected sensor (In terminal use command "cd /sys/bus/w1/devices" then "ls" to get a list of addresses)
4. Instantiate your sensor objects with a name and their w1 address
5. Edit the temperature threshold if necessary
