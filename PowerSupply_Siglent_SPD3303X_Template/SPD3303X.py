# SPD3303X.py

import pyvisa #pip install pyvisa
from time import sleep

idn1 = 'Siglent Technologies,SPD3303X,SPD3XJGC900207,1.01.01.03.11R1,V6.2' # change this as every device has an unique identifier

def find_PSU():
    global rm, PSU
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()
    for res in resources:
        try:
            PSU = rm.open_resource(res)
            response = PSU.query('*IDN?')
            # print(response) # TEST CONNECTION
            if response.strip() == idn1:
                # print(response) # TEST CONNECTION
                # print(PSU) # TEST CONNECTION
                # print(res) # TEST CONNECTION
                return res  # 🎯 Return the VISA address if match
        except Exception:
            pass  # Ignore any devices that don't respond
    return None  # ❌ Not found

# find_PSU() # TEST CONNECTION


def PSU_Chan_Volt_Amp(ch_number, ch_voltage, ch_current):
    global PSU
    PSU.write(f'CH{ch_number}:VOLT {ch_voltage}')
    PSU.write(f'CH{ch_number}:CURR {ch_current}')



def PSU_Measure_Volt(ch_number):
    global PSU
    voltage = PSU.query(f'MEAS:VOLT? CH{ch_number}').strip()
    voltage = float(voltage)

    return voltage

def PSU_Measure_Amps(ch_number):
    global PSU
    amperage = PSU.query(f'MEAS:CURR? CH{ch_number}').strip()
    amperage = float(amperage)

    return amperage

def PSU_Chan_State(ch_number, ch_state):
    global PSU
    PSU.write(f'OUTP CH{ch_number},{ch_state}')



def PSU_Chan_All_Off():
    global PSU
    PSU_Chan_Volt_Amp(1, 0.000, 0.000)
    PSU.write('OUTP CH1,OFF')
    PSU_Chan_Volt_Amp(2, 0.000, 0.000)
    PSU.write('OUTP CH2,OFF')
    PSU.write('OUTP CH3,OFF') # Fixed 5V output for MEGA Relays


def close_PSU():
    global PSU
    PSU.close()