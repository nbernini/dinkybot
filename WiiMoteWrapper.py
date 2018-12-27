
import cwiid
import time
import datetime
from pprint import pprint
from wii_util import buttons

class WiiMoteWrapper(object):
	def __init__(self):
		
		self._wii = None
		self._button_mapping = buttons
		self._rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_NUNCHUK | cwiid.RPT_IR 
				
	def connect(self, attempts = 5, rumble = True):
		''' Connects Controller '''
		print 'Please press buttons 1 + 2 on your Wiimote now ...'
		time.sleep(2)
		i = 0
		while not self._wii:
			try:
				self._wii = cwiid.Wiimote()
				print 'Wiimote Connected'
				if rumble:
					self.rumble(times = 2, duration = 0.3)
				self._wii.rpt_mode = self._rpt_mode # reporting modes
				
			except RuntimeError: 
				if (i > attempts): 
					quit() 
					break 
				print "Error opening wiimote connection" 
				print "attempt " + str(i+1) 
				i +=1 
		
	def disconnect(self, rumble = True):
		''' Disconnects Controller '''
		print '\nClosing connection ...'
		if rumble:
			self.rumble()
		exit(self._wii)
	
	def get_button_list(self):
		''' Returns list of available buttons '''
		return self._button_mapping.keys()
		
	def rumble(self, times = 1, duration = 1):
		''' Turns on/off rumbles for a given number of times, each 
				of length duration in seconds
		'''
		for t in xrange(times):
			self._wii.rumble = 1
			time.sleep(duration)
			self._wii.rumble = 0
			time.sleep(duration)
					
	def led(self, led_state = [0, 0, 0, 0]):
		''' Turns on/off LEDs '''
		
		# Check that 4 parameters as passed and are 1/0's
		if len(led_state) != 4:
			print 'Number of parameters must be 4 for led_state'
			return None
		for l in led_state:
			if l not in [1,0]:
				print 'LED values are either 0 (off) or 1 (on)'
				return None
				
		# Convert to String
		led_state = [str(l) for l in led_state]
		led_str = ''.join(led_state)[::-1] # reverse order
		
		# Convert to Integer
		led_int = int(led_str,2)
		
		# Activate LEDs
		self._wii.led = led_int
		
	def check_button(self, buttons = []):
		''' Returns boolean if list of buttons are passed.  If checking
			only one button, can pass string instead of list
		'''
		
		#print 'input: {}'.format(buttons)
		
		# Convert to list
		if isinstance(buttons,str) or isinstance(buttons,unicode):
			buttons = [buttons]
		
		# Check for valid buttons
		for b in buttons:
			if not self._parse_button(b):
				print "'{}' is not a valid button.".format(b)
				return False
				
		# Create Button total
		total = sum([self._parse_button(b) for b in buttons])
		
		# Check Total against buttons pressed
		return total == self.read_state()['buttons']
		
	def read_state(self, verbose = False):
		if verbose:
			pprint(self._wii.state)
		
		return self._wii.state
	
	def read_buttons(self):
		return self.read_state['buttons']
		
	def read_accelerometer(self):
		return self.read_state(verbose = False)['acc']
		

	def record_gesture(self):
		''' Returns array of accelerometer data for gesture '''
					
	
	

	#############################
	## Private
	#############################
	def _parse_button(self,b):
		''' Returns cwiid button code, else None '''
		try:
			return self._button_mapping[b.lower()]
		except KeyError:
			return None
		except AttributeError:
			return None
