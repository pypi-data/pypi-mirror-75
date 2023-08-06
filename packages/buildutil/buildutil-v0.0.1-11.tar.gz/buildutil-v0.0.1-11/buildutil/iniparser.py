#!/usr/bin/env python3


import configparser
import os


class IniParser():

	def __init__(self, iniPathFile=None):
		"""Create (if not present) an inifile"""
		# Validate user input
		if iniPathFile is None:
			raise Exception("IniPathFile is None")

		self.iniPathFile = os.path.abspath(iniPathFile)
		ini = configparser.ConfigParser()
		ini.optionxform = str
		ini.read(self.iniPathFile)

		# Create directory if it does not exist
		iniDirpath = os.path.dirname(self.iniPathFile)
		if os.path.isdir(iniDirpath) == False:
			os.makedirs(iniDirpath)

		# Create ini file if it does not exist
		try:
			with open(self.iniPathFile, 'w') as configfile:
				ini.write(configfile)
		except:
			raise Exception(f"Could not create '{self.iniPathFile}'")


	def read(self, section, key):
		"""Acquire the value of a sector key pair or None"""
		# Read ini file
		ini = configparser.ConfigParser()
		ini.optionxform = str
		ini.read(self.iniPathFile)

		# Validate
		if section == "" or section is None:
			section = "DEFAULT"

		if key == "" or key is None:
			return

		# Get configuration
		rv = None
		try:
			rv = ini.get(section, key)
		except Exception as e:
			rv = None


		# Translate value
		if rv == "True":
			rv = True
		elif rv == "False":
			rv = False
		else:
			try:
				return int(rv)
			except Exception:
				pass

			try:
				return float(rv)
			except Exception:
				pass

		return rv


	def write(self, section, key, value, update=True):
		"""Write a value to a sector key pair"""
		# Read ini file
		ini = configparser.ConfigParser()
		ini.optionxform = str
		ini.read(self.iniPathFile)

		# Validate
		if section == "" or section is None:
			section = "DEFAULT"

		if key == "" or key is None:
			return

		# No need to write file when file value equals the new value
		rv = self.read(section, key)
		if value == rv:
			return

		# Update
		if update is False and rv != None:
			return

		# Prepare value
		if value is None:
			return
		value = str(value)

		# Set configuration
		if ini.has_section(section) is False and section != "DEFAULT":
			ini.add_section(section)

		try:
			ini.set(section, key, value)
		except:
			raise Exception(f"Could not write [{section}][{key}] = {value}")

		# Write ini file
		try:
			with open(self.iniPathFile, 'w') as configfile:
				ini.write(configfile)
		except:
			raise Exception(f"Could not write to '{self.iniPathFile}'")

		#print(f"Wrote: [{section_key}] = '{value}")


	def __str__(self):
		rv = f"From Ini file: '{self.iniPathFile}'\n"
		for d in self.get():
			section = d["section"]
			key     = d["key"]
			value   = d["value"]
			rv += f"[{section}][{key}] = '{value}'\n"

		return rv


	def get(self):
		ini = configparser.ConfigParser(default_section=None)
		ini.optionxform = str
		ini.read(self.iniPathFile)

		lst = list()

		sections = ini.sections()
		for section in sections:
			keys = ini.options(section)
			for key in keys:
				value = self.read(section, key)
				d = dict()
				d["section"] = section
				d["key"]     = key
				d["value"]   = value
				lst.append(d)

		return lst



def main():

	iniFilepath = "/tmp/test.ini"

	# Create ini parser
	parser = IniParser(iniFilepath)

	# Write
	section = "section"
	key = "key"
	value = "value"
	parser.write(None,       None,   "SilentIgnore1", update=False)
	parser.write("IGNOREME", None,   "SilentIgnore2", update=False)
	parser.write(section,    key,    value,           update=False)
	parser.write(None,       "key1", "default",       update=False)
	parser.write("Sec1",     "key1", "value1",        update=False)
	parser.write("sec2",     "key2", "value2",        update=False)

	# Read back
	rv = parser.read(section, key)

	# Validate
	if rv != value:
		raise Exception("FAILLURE!!")

	# See results
	print(parser)

	# Delete ini file
	import os
	if os.path.exists(iniFilepath):
		os.remove(iniFilepath)


if __name__ == "__main__":
	main()
