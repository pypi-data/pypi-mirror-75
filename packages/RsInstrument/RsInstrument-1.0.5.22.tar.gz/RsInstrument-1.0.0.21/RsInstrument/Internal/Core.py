import re
from typing import Callable

from . import InstrumentOptions as Options, Conversions as Conv
from .ArgSingle import ArgSingle
from .ArgSingleList import ArgSingleList
from .Conversions import BinFloatFormat, BinIntFormat
from .Instrument import Instrument
from .InstrumentSettings import InstrViClearMode, InstrumentSettings, WaitForOpcMode
from .Utilities import parse_token_to_key_and_value, trim_str_response


class Core(object):
	"""Main driver component. Provides: \n
		- main core constructor
		- 'io' interface for all the write / query operations
		- command parameters string composer for single arguments...
		- link handlers adding / changing / deleting

		Version History:
		0.9.2 (build 24), 13.11.2019 - Added recognition of special values for enum return strings
		0.9.1 - Added read / write to file, refactored internals to work with streams
		0.9.0 - First Version created."""

	driver_version: str = ''
	"""Placeholder for the driver version string."""

	def __init__(
			self,
			resource_name: str,
			id_query: bool = True,
			reset: bool = False,
			driver_options: str = None,
			user_options: str = None,
			direct_session: object = None):
		"""Initializes new driver session. For cleaner code, use the class methods: \n
		- Core.from_existing_session() - initializes a new Core with an existing pyvisa session."""

		self.core_version = '0.9.2'
		self.simulating = False
		self.supported_idn_patterns = []
		self.supported_instr_models = []

		self._args_single_list = ArgSingleList()
		sett_dr = self._parse_init_settings_string(driver_options)
		self._apply_settings_to_core(sett_dr)
		sett_user = self._parse_init_settings_string(user_options)
		self._apply_settings_to_core(sett_user)

		# Typical settings for the Core
		self._instrumentSettings = InstrumentSettings(
			InstrViClearMode.execute_on_all,  # Instrument viClear mode
			False,  # Full model name. True: SMW200A, False: SMW
			0,  # Delay by each write
			0,  # Delay by each read
			100000,  # Max chunk read / write size in bytes
			WaitForOpcMode.stb_poll,  # Waiting for OPC Mode: Status byte polling
			30000,  # OPC timeout
			10000,  # VISA timeout
			60000,  # Self-test timeout
			Options.ParseMode.Auto,  # *OPT? response parsing mode
			BinFloatFormat.Single_4bytes,  # Format for parsing of binary float numbers
			BinIntFormat.Integer32_4bytes,  # Format for parsing of binary integer numbers
			False  # OPC query after each setting
		)

		self._instrumentSettings.apply_option_settings(sett_dr)
		self._instrumentSettings.apply_option_settings(sett_user)

		handle = direct_session
		if handle:
			if hasattr(direct_session, 'get_session_handle'):
				assert hasattr(direct_session, '_core'), f"Direct session is a class type. It must be an instance of the top-level driver class."
				handle = direct_session.get_session_handle()

		self.io = Instrument(resource_name, False, self._instrumentSettings, handle)
		self.io.query_instr_status = True

		self._apply_settings_to_instrument(sett_dr)
		self._apply_settings_to_instrument(sett_user)

		if id_query:
			self.io.fits_idn_pattern(self.supported_idn_patterns, self.supported_instr_models)

		if reset:
			self.io.reset()
		else:
			self.io.check_status()

	@classmethod
	def from_existing_session(cls, session: object, driver_options: str = None) -> 'Core':
		"""Creates a new Core object with the entered 'session' reused."""
		# noinspection PyTypeChecker
		return cls(None, False, False, driver_options, None, session)

	def __str__(self):
		return f"Core session '{self.io.resource_name}'"

	def set_link_handler(self, link_name: str, handler: Callable) -> Callable:
		"""Adds / Updates link handler for the entered link_name.
		Handler API: handler(event_args: ArgLinkedEventArgs)
		Returns the previous registered handler, or None if no handler was registered before."""
		return self.io.set_link_handler(link_name, handler)

	def del_link_handler(self, link_name: str) -> Callable:
		"""Deletes link handler for the link_name.
		Returns the deleted handler, or None if none existed."""
		return self.io.del_link_handler(link_name)

	def del_all_link_handlers(self) -> int:
		"""Deletes all the link handlers.
		Returns number of deleted links."""
		return self.io.del_all_link_handlers()

	# noinspection PyMethodMayBeStatic
	def _parse_init_settings_string(self, text: str) -> dict:
		"""Parses init string to a dictionary of settings: name -> value."""
		tokens = {}
		if not text:
			return tokens

		# Remove all the class-options enclosed by round brackets e.g. "<groupName>=(<groupTokens>)"
		group_pattern = r'(\w+)\s*=\s*\(([^\)]*)\)'
		# Match class-settings, add them as separate keys with groupName_Key
		while True:
			# Group loop
			m = re.search(group_pattern, text)
			if not m:
				break

			text = text.replace(m.group(0), '')
			group_name = m.group(1).upper()
			group_tokens = m.group(2).strip().split(',')
			for token in group_tokens:
				key, value = parse_token_to_key_and_value(token)
				if value:
					tokens[f'{group_name}_{key.upper()}'] = value

		# All groups are removed from the text, now we can use splitting on commas and remove white-space-only elements
		for token in text.split(','):
			key, value = parse_token_to_key_and_value(token)
			if value:
				tokens[key.upper()] = value
		return tokens

	def _apply_settings_to_core(self, settings: dict) -> None:
		"""Applies settings relevant for the Core from the dictionary."""
		value = settings.get('SIMULATE')
		if value:
			self.simulating = Conv.str_to_bool(value)

		value = settings.get('SUPPORTEDINSTRMODELS')
		if value:
			self.supported_instr_models = [*map(trim_str_response, value.split('/'))]

		value = settings.get('SUPPORTEDIDNPATTERNS')
		if value:
			self.supported_idn_patterns = [*map(trim_str_response, value.split('/'))]

	def _apply_settings_to_instrument(self, settings: dict) -> None:
		"""Applies settings relevant for the Instrument from the dictionary."""
		value = settings.get('QUERYINSTRUMENTSTATUS')
		if value:
			self.io.query_instr_status = Conv.str_to_bool(value)

		value = settings.get('SIMULATIONIDNSTRING')
		if value and self.simulating:
			# Use the '*' instead of the ',' in the value to avoid comma as token delimiter
			self.io.idn_string = value.replace('*', ',')

	def compose_cmd_arg_param(
			self, arg1: ArgSingle, arg2: ArgSingle = None, arg3: ArgSingle = None, arg4: ArgSingle = None, arg5: ArgSingle = None, arg6: ArgSingle = None) -> str:
		"""Composes command parameter string based on the single arguments definition."""
		return self._args_single_list.compose_cmd_string(arg1, arg2, arg3, arg4, arg5, arg6)

	def get_session_handle(self):
		"""Returns the underlying pyvisa session."""
		return self.io.get_session_handle()

	def close(self):
		"""Closes the Core session."""
		self.io.close()
		self.io = None
