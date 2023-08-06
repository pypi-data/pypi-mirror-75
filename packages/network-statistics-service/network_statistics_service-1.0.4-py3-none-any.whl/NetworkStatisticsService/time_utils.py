import time


class TimeUtils(object):
	""" 
	A class used to hold various util mthods for working with strings.

	...

	Methods
	-------
	get_current_timestamp(return_as_dict, dict_key)
		Returns the current timestamp in unix time
	"""

	@staticmethod
	def get_current_timestamp(return_as_dict=True, dict_key='Timestamp'):
		"""Returns the current timestamp in unix time.

		Parameters
		----------
		return_as_dict : bool
			Wether to return the timestamp as a dictionary or as a value (default True)
		dict_key : str
			If the result is returned as a dictionary, this is the key used
		"""

		secondsSinceEpoch = round(time.time())
		if return_as_dict:
			return {dict_key: secondsSinceEpoch}
		else:
			return secondsSinceEpoch

	@staticmethod
	def get_timestamp_months_in_future(reference_timestamp, number_of_months):
		"""Returns the timestamp a certain number of months in the future from the reference timestamp.

		Parameters
		----------
		reference_timestamp: float
			The timestamp from which two months should be computed
		number_of_months: int
			The number of months in the future the timestamp returned should be. A month is a 31 day period.
		"""
		return reference_timestamp + (number_of_months * 2678400)
