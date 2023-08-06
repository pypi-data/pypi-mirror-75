#!/usr/bin/env python3

from .iniparser import IniParser

import os

def array2Dict(array):
	lst = list()
	for l in array:
		d = dict()
		d["section"] = l[0]
		d["key"]     = l[1]
		d["default"] = l[2]
		d["options"] = l[3]
		lst.append(d)

	return lst


class ConfigParser():

	def __init__(self, iniFilepath="setup.ini", defaults=None):

		# Validate user input
		if iniFilepath is None:
			raise Exception("Invalid iniFilepath")

		# User input
		self.iniFilepath = os.path.abspath(iniFilepath)
		self.defaults = defaults

		# Write defaults values
		if self.defaults is not None:
			parser = IniParser(self.iniFilepath)
			for d in self.defaults:
				parser.write(d["section"], d["key"], d["default"], update=False)


	def read(self, section, key):
		parser = IniParser(self.iniFilepath)
		rv = parser.read(section, key)

		return rv


	def write(self, section, key, value):

		# We do not update on None
		if value is None:
			return

		# Find options
		options = None
		if self.defaults is not None:
			for d in self.defaults:
				status = False
				if d["section"] == section and d["key"] == key:
					status = False
					options = d["options"]

		# Validate
		isValid = False
		if options is not None:
			print(f"[{section}][{key}] found with options = {options}")
			for o in options:
				if o == value:
					isValid = True
					break

			if isValid is False:
				raise Exception(f"Ignoring invalid config for [{section}][{key}]: '{value}'")

		# Write config
		parser = IniParser(self.iniFilepath)
		parser.write(section, key, value)



	def __str__(self):
		parser = IniParser(self.iniFilepath)
		rv = parser.__str__()
		return rv


	def setenv(self):
		"""Set all configs into environment variables"""
		for el in self.get():
			key   = el["key"]
			value = el["value"]
			# Set enironment variable
			os.environ[key] = value
			# Verify
			if os.environ[key] != value:
				raise ConfigError("Failed to set environment variable '{key}'")


	def get(self):
		parser = IniParser(self.iniFilepath)

		lst = list()
		for el in parser.get():
			section = el["section"]
			key = el["key"]
			value = parser.read(section, key)

			d = dict()
			d["section"] = section
			d["key"]     = key
			d["value"]   = value
			lst.append(d)

		return lst


def main():

	iniFilepath = "/tmp/configparser/test.ini"

	if os.path.exists(iniFilepath):
		os.remove(iniFilepath)

	##########################################
	# Write values
	def getDefaults():
		lst = list()
		defaults = [
			# Section    Key      Default  Options
			["MAKE",    "PORT",   "posix", {"posix", "stm32f072rb"} ],
			["MAKE",    "TARGET", "dbg",   {"dbg",   "rel"}         ],

			["INVALID", "String", "apple", {"banana", "orange"}     ]
		]

		for el in defaults:
			d = dict()
			d["section"] = el[0]
			d["key"]     = el[1]
			d["default"] = el[2]
			d["options"] = el[3]
			lst.append(d)

		return lst

	parser = ConfigParser(iniFilepath=iniFilepath, defaults=getDefaults())

	##########################################
	# Write non default/new values

	def getExtra():
		extra = [
			# Section      Key            Value         Update
			#["MAKE",       "PORT",       "win32",       True  ],
			#["MAKE",       "TARGET",     "prod",        True  ],

			["NONDEFAULT", "Keepme",     "I kept you!", True  ],

			["UNIQUE",     "Override1",  "Original",    True  ],
			["UNIQUE",     "Override1",  "Updated",     False ],

			["UNIQUE",     "Override2",  "Original",    False ],
			["UNIQUE",     "Override2",  "Updated",     False ]
		]
		col = 4

		return col, extra

	col, defaults = getExtra()
	for line in defaults:
		if len(line) == col:
			section = line[0]
			key     = line[1]
			value   = line[2]
			parser.write(section, key, value)

	parser.setenv()
	print(parser)
	col, defaults = getExtra()
	for line in defaults:
		section = line[0]
		key     = line[1]
		value   = os.getenv(key)

		print(f"ENV: {key}: {value}")

	##########################################
	# Delete ini file

	if os.path.exists(iniFilepath):
		os.remove(iniFilepath)


if __name__ == "__main__":
	main()
