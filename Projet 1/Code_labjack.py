import u3
import numpy as np

# Define LabJack U3 parameters
d = u3.U3()

# Define analog input and output channels
ain_channel = 0  # AIN0
dac_channel = 5000  # DAC0

# Configure I/O
#d.configIO(FIOAnalog = ain_channel)


# Function to read analog voltage from AIN
def read_analog_voltage():
    voltage = d.readRegister(ain_channel)
    return voltage

# Function to remove constant component and change amplitude
def transform_signal(voltage):
    # Adjust these parameters based on your requirements
    constant_component = 9
    amplitude_factor = 3

    transformed_signal = amplitude_factor * (voltage - constant_component)
    return transformed_signal

# Function to send the transformed signal to DAC0
def send_to_dac(transformed_signal):
    d.writeRegister(dac_channel, transformed_signal)

# Main loop
try:
    while True:
        # Read analog voltage
        raw_voltage = read_analog_voltage()
        # print(raw_voltage)

        # Transform the signal
        transformed_signal = transform_signal(raw_voltage)
        print(transformed_signal)

        # Send the transformed signal to DAC0
        send_to_dac(transformed_signal)

except KeyboardInterrupt:
    pass

finally:
    # Close the connection when done
    d.close()

