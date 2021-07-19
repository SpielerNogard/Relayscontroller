USB_PORT = "/dev/ttyACM0"  # Arduino Uno WiFi Rev2
# Imports
import serial

# Connect to USB serial port at 9600 baud
try:
   usb = serial.Serial(USB_PORT, 9600, timeout=2)
except:
   print("ERROR - Could not open USB serial port.  Please check your port name and permissions.")
   print("Exiting program.")
   exit()
# Send commands to Arduino
print("Enter a command from the keyboard to send to the Arduino.")
print_commands()
while True:
   command = input("Enter command: ")
   if command == "a":  # read Arduino A0 pin value
      usb.write(b'read_a0')  # send command to Arduino
      line = usb.readline()  # read input from Arduino
      line = line.decode()  # convert type from bytes to string
      line = line.strip()  # strip extra whitespace characters
      if line.isdigit():  # check if line contains only digits
         value = int(line)  # convert type from string to int
      else:
         print("Unknown value '" + line + "', setting to 0.")
         value = 0
      print("Arduino A0 value:", value)
   elif command == "l":  # turn on Arduino LED
      usb.write(b'eins_on')  # send command to Arduino
      print("Arduino LED turned on.")
   elif command == "k":  # turn off Arduino LED
      usb.write(b'eins_off')  # send command to Arduino
      print("Arduino LED turned off.")
   elif command == "x":  # exit program
      print("Exiting program.")
      exit()
   else:  # unknown command
      print("Unknown command '" + command + "'.")
      print_commands()
