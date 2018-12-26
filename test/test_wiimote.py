
import cwiid, time

''' 
This script is to test the WiiMote connection and button presses.
WiiMote is connected by pressing 1 + 2 together to connect via 
bluetooth.  To disconnect, press - and + together.  The remote will
rumble and the program will stop.  Holding in the Home button will 
print the gyroscope values.
'''
button_delay = 0.1

print 'Please press buttons 1 + 2 on your Wiimote now ...'
time.sleep(1)

# This code attempts to connect to your Wiimote and if it fails the program quits
try:
  wii=cwiid.Wiimote()
except RuntimeError:
  print "Cannot connect to your Wiimote. Run again and make sure you are holding buttons 1 + 2!"
  quit()


print 'Wiimote connection established!\n'
print 'Go ahead and press some buttons\n'
print 'Press PLUS and MINUS together to disconnect and quit.\n'

time.sleep(2)

wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_NUNCHUK | cwiid.RPT_MOTIONPLUS | cwiid.RPT_IR | cwiid.RPT_CLASSIC

print dir(cwiid)


while True:

  buttons = wii.state['buttons']

  # Detects whether + and - are held down and if they are it quits the program
  if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
    print '\nClosing connection ...'
    # NOTE: This is how you RUMBLE the Wiimote
    wii.rumble = 1
    time.sleep(1)
    wii.rumble = 0
    exit(wii)
 
  print wii.state
  #print wii.state['buttons']
  time.sleep(.1)
  # {'acc': (111, 106, 138), 'led': 0, 'rpt_mode': 22, 'ext_type': 1, 'buttons': 0, 'rumble': 0, 'error': 0, 'nunchuk': {'acc': (177, 136, 147), 'buttons': 0, 'stick': (128, 128)}, 'battery': 173}


