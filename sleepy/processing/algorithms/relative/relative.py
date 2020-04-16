
from sleepy.processing.processor import Algorithm
from sleepy.processing.parameter import Parameter
import numpy as np

class Relative(Algorithm):

	def __init__(self):

		self.name = "Relative Amplitude"

		self.durationLow = Parameter(
			title = "Lower bound for duration interval [sec]",
			fieldType = float,
			default = 0.8
		)

		self.durationHigh = Parameter(
			title = "Higher bound for duration interval [sec]",
			fieldType = float,
			default = 2.0
		)

		self.scalingAmplitude = Parameter(
			title = "Scaling factor for SO amplitude",
			fieldType = float,
			default = 2/3
		)

		self.scalingNegPeak = Parameter(
			title = "Scaling factor for SO negative peak",
			fieldType = float,
			default = 2/3
		)

	def compute(self, signal):

		intervals = signal.findWaves()

		def isEvent(interval):

			currDuration = interval[1] - interval[0]

			if currDuration >= self.durationLow * signal.samplingRate:
					if currDuration <= self.durationHigh * signal.samplingRate:
						
						return True
			
			return False

		return np.array([ interval for interval in intervals if isEvent(interval) ])

	def filter(self, events, data):

		neg_threshold = 0
		amplitude_threshold = 0
		idx = 0

		for event in events:
			neg_threshold = neg_threshold + event.minVoltage
			amplitude_threshold = amplitude_threshold + event.maxVoltage - event.minVoltage
			idx += 1

		neg_threshold = neg_threshold / idx
		neg_threshold = self.scalingNegPeak * neg_threshold

		amplitude_threshold = amplitude_threshold / idx
		amplitude_threshold = self.scalingAmplitude * amplitude_threshold

		final_events = []
		idx = 0
		for event in events:
			if event.minVoltage <= neg_threshold:
				if event.maxVoltage - event.minVoltage >= amplitude_threshold:
					final_events.append(event)
			idx += 1

		return final_events
