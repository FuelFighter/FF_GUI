import string
from car import Car_c
from car_calculations import *


CANID = {
	'Brake':0x110,
	'Encoder':0x220,
	'Steering Wheel':0x230,
	'Dashboard':0x310,
	'BMS Cell V 1-4':0x440,
	'BMS Cell V 5-8':0x441,
	'BMS Cell V 9-12':0x442,
	'BMS Cell Temp':0x443,
	'BMS Volt Current':0x444,
	'BMS State':0x448,
	'BMS Error Flags':0x449,
	'Motor 1 Status':0x450,
	'Motor 2 Status':0x460,
	'Front Lights Status':0x470,
	'Back Lights Status':0x480
}

def updateCarValues(line, Car):
	if ('[' not in line) | (']' not in line):
		return 'Invalid Message'

	line = line[line.find('[')+1:line.find(']')]
	lineArray = line.split(':')

	ID = int('0x' + lineArray[0],16)
	Length = int('0x' + lineArray[1],16)
	Data = []

	for pos in range(0,Length):
		Data.append(lineArray[2][(2*pos):(2*pos+2)])

	for d in Data:
 		if d == '':
 			error = 'No Data'
 			return error

	if ID == CANID['Brake']:
		if int('0x' + Data[0],16) == 1:
			Car.Brake = True
		else:
			Car.Brake = False

	elif ID == CANID['Encoder']:
		Car.Motor1.RPM = int('0x' + Data[0] + Data[1], 16)
		Car.Motor2.RPM = int('0x' + Data[2] + Data[3], 16)
		Car.RPM = int('0x' + Data[4] + Data[5], 16)
		Car.Velocity = calculateVelocity(Car.RPM)		

	elif ID == CANID['Steering Wheel']:
		Car.Throttle = int('0x' + Data[3], 16)
		throttleLeft = int('0x' + Data[2], 16)
		if throttleLeft > 50:	
			Car.Deadmanswitch = True
		else:
			Car.Deadmanswitch = False
		 
	elif ID == CANID['Dashboard']:
		pass

	elif ID == CANID['BMS Cell V 1-4']:
		Car.Battery.Cell_Voltage[0] = int('0x' + Data[0] + Data[1], 16)
		Car.Battery.Cell_Voltage[1] = int('0x' + Data[2] + Data[3], 16)
		Car.Battery.Cell_Voltage[2] = int('0x' + Data[4] + Data[5], 16)
		Car.Battery.Cell_Voltage[3] = int('0x' + Data[6] + Data[7], 16)
		pass

	elif ID == CANID['BMS Cell V 5-8']:
		Car.Battery.Cell_Voltage[4] = int('0x' + Data[0] + Data[1], 16)
		Car.Battery.Cell_Voltage[5] = int('0x' + Data[2] + Data[3], 16)
		Car.Battery.Cell_Voltage[6] = int('0x' + Data[4] + Data[5], 16)
		Car.Battery.Cell_Voltage[7] = int('0x' + Data[6] + Data[7], 16)
		pass

	elif ID == CANID['BMS Cell V 9-12']:
		Car.Battery.Cell_Voltage[8] = int('0x' + Data[0] + Data[1], 16)
		Car.Battery.Cell_Voltage[9] = int('0x' + Data[2] + Data[3], 16)
		Car.Battery.Cell_Voltage[10] = int('0x' + Data[4] + Data[5], 16)
		Car.Battery.Cell_Voltage[11] = int('0x' + Data[6] + Data[7], 16)
		pass

	elif ID == CANID['BMS Cell Temp']:	
		Car.Battery.Cell_Temp[0] = int('0x' + Data[0] + Data[1], 16)
		Car.Battery.Cell_Temp[1] = int('0x' + Data[2] + Data[3], 16)
		Car.Battery.Cell_Temp[2] = int('0x' + Data[4] + Data[5], 16)
		Car.Battery.Cell_Temp[3] = int('0x' + Data[6] + Data[7], 16)
		pass

	elif ID == CANID['BMS Volt Current']:
		Car.Battery.Current = int('0x' + Data[0] + Data[1], 16)
		Car.Battery.Voltage = int('0x' + Data[2] + Data[3], 16)
		pass

	elif ID == CANID['BMS State']:
		State = int('0x' + Data[0], 16)
		if State == 0:
			Car.Battery.State = "Idle"
		elif State == 1:
			Car.Battery.State = "PreCharge"
		elif State == 2: 
			Car.Battery.State = "Battery Active"
		elif State == 3:
			Car.Battery.State = "Error"
		pass

	elif ID == CANID['BMS Error Flags']:
		print(Data)
		errorFlag = int('0x' + Data[0] + Data[1], 16)

		if errorFlag & 0b1:
			Car.Battery.Error_PreChargeTimeout = True
		else:
			Car.Battery.Error_PreChargeTimeout = False
		if errorFlag & 0b10:
			Car.Battery.Error_LTC_LossOfSignal = True
		else:
			Car.Battery.Error_LTC_LossOfSignal = False
		if errorFlag & 0b100:
			Car.Battery.Error_OverVoltage = True
		else:
			Car.Battery.Error_OverVoltage = False
		if errorFlag & 0b1000:
			Car.Battery.Error_UnderVoltage = True
		else:
			Car.Battery.Error_UnderVoltage = False
		if errorFlag & 0b10000:
			Car.Battery.Error_OverCurrent = True
		else:
			Car.Battery.Error_OverCurrent = False
		if errorFlag & 0b100000:
			Car.Battery.Error_OverTemp = True
		else:
			Car.Battery.Error_OverTemp = False
		if errorFlag & 0b1000000:
			Car.Battery.Error_NoDataOnStartup = True
		else:
			Car.Battery.Error_NoDataOnStartup = False
		pass

	elif ID == CANID['Motor 1 Status']:
		Car.Motor1.Current = int('0x' + Data[1] + Data[2], 16)
		Car.Motor1.PWM = int('0x' + Data[3] + Data[4], 16)
		Car.Motor1.Throttle = int('0x' + Data[5], 16)
		pass

	elif ID == CANID['Motor 2 Status']:
		Car.Motor2.Current = int('0x' + Data[1] + Data[2], 16)
		Car.Motor2.PWM = int('0x' + Data[3] + Data[4], 16)
		Car.Motor2.Throttle = int('0x' + Data[5], 16)
		pass

	elif ID == CANID['Front Lights Status']:
		pass

	else:
		pass

	return ''