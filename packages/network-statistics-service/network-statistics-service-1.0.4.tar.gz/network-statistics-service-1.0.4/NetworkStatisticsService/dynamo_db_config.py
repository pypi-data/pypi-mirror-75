class DynamoDBConfig(object):
	""" 
	A class used to pass DynamoDB configuration to the Statistics Service.

	...

	Attributes
	----------
	aws_profile : str
		The AWS profile from the credential files to use (default 'default')
	aws_region : str
		The AWS region where the DynamoDB tables reside
	stats_table : str
		The name of the table where your statistics should be uplaoded
	logs_table : str
		The name of the table where error logs should be uplaoded
	ttl_config : TtlConfig
		Time to live config for DynamoDB tables.

	Methods
	-------
	is_valid(check_for_stats)
		Verifies if the given configuration is valid for the upload type
	"""


	def __init__(self, aws_profile = 'default', aws_region = None, stats_table = None, logs_table = None, ttl_config = None):
		"""
		Parameters
		----------
		aws_profile : str
			The AWS profile from the credential files to use (default 'default')
		aws_region : str
			The AWS region where the DynamoDB tables reside
		stats_table : str
			The name of the table where your statistics should be uplaoded
		logs_table : str
			The name of the table where error logs should be uplaoded
		ttl_config : TtlConfig
			Time to live config for DynamoDB tables.
		"""

		super().__init__()
		self.aws_profile = aws_profile
		self.aws_region = aws_region
		self.stats_table = stats_table
		self.logs_table = logs_table
		self.ttl_config = ttl_config
	
	
	def is_valid(self, check_for_stats):
		"""Verifies if the given configuration is valid for the upload type.

		If check_for_stats is True, the configuration is checked for statistics upload. If it 
		is false, the configuration is checked for error logs upload.

		Parameters
		----------
		check_for_stats : bool
			Whether the configuration should be validated for statistc upload
		"""
		
		if self.aws_region is None:
			return False
		if check_for_stats and self.stats_table is None:
			return False
		if not check_for_stats and self.logs_table is None:
			return False
		return True