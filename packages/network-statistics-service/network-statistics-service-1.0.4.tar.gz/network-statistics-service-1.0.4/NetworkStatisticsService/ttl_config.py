class TtlConfig(object):
	""" 
	A class used to pass TTL Configuration to the DynamoDB Statistics Uploader.

	...

	Attributes
	----------
	time_in_months : int
		The time in months an object should live in the DB.
	attribute_name : str
		The name of the attribute where the ttl time should be stored.

	"""


	def __init__(self, time_in_months: int, attribute_name: str):
		"""
		Parameters
		----------
		time_in_months : int
			The time in months an object should live in the DB.
		attribute_name : str
			The name of the attribute where the ttl time should be stored.
			"""

		super().__init__()

		if time_in_months is None or attribute_name is None:
			raise ValueError("None of the TTL Config attributes can be none")

		if time_in_months < 0:
			raise ValueError("Time in months must be a positive number")

		if len(attribute_name) == 0:
			raise ValueError("Attribute name cannot be the empty string")

		self.time_in_months = time_in_months
		self.attribute_name = attribute_name