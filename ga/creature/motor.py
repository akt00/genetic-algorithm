from enum import Enum
import numpy as np


class MotorType(Enum):
    PULSE = 1
    SINE = 2


class Motor:
    def __init__(self, control_waveform: float, control_amp: float, control_freq: float):
        """
        :param control_waveform:
        :param control_amp:
        :param control_freq:
        """
        self.motor_type = MotorType.PULSE if control_waveform <= .5 else MotorType.SINE
        self.amp = control_amp
        self.freq = control_freq
        self.phase = 0

    def get_output(self):
        """
        :return:
        """
        self.phase = (self.phase + self.freq) % (np.pi * 2)
        match self.motor_type:
            case MotorType.PULSE:
                output = 1 if self.phase < np.pi else -1
            case MotorType.SINE:
                output = np.sin(self.phase)
            case _:
                output = 0
        return output
