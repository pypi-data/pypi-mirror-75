import requests
import xml.etree.ElementTree as ET

def getResponse(v): # v is an integer (version#) or "current"
		url = "http://cfconventions.org/Data/cf-standard-names/{}/src/cf-standard-name-table.xml".format(v)
		return requests.get(url)

def getRoot(r):
		if r.status_code != 200:
			return None
		return ET.fromstring(r.content)

def getTags(root): # Returns all child tags (at first nested position only, which is ideal)
		tags = []
		for child in root:
			tags.append(child.tag)
		return tags

def getStart(tags, value):
		for i,v in enumerate(tags):
			if v == value:
				return i

def getLast(tags, value):
		for i,v in enumerate(reversed(tags)):
			if v == value:
				return len(tags)-i

def getStandardNamePositions(tags): # First and last occurence of standard name entry
		return [getStart(tags, "entry"), getLast(tags, "entry")]

def getAliasNamesPositions(tags): # First and last occurence of alias entry
	return [getStart(tags, "alias"), getLast(tags, "alias")]


def version(v = "current"): # Call
	"""
	SUMMARY:
	Shows the version number and the release date of the version.

	PARAMETERS:
	v (int, default = "current"): 
		An integer/string representing the CF Standard Name version. eg. 66 or '66'
		If left blank, it defaults to the latest (current) version.

	RETURNS:
	A string of the form: Version: ## released on YYYY-MM-DDTHH:MM:SSZ by INSTITUTE. Contact: email.
	"""

	root = getRoot(getResponse(v))
	if root is None:
		raise Exception("This version was not found on the CF Standard Name Webpage. Please verify the version number again.")

	return "Version: {},  released on {} by {}. Contact: {}".format(root[0].text, root[1].text, root[2].text, root[3].text)

def standardnames(v = "current"): # Call
	"""
	SUMMARY:
	Shows the CF Standard Names in this version.

	PARAMETERS:
	v (int, default = "current"): 
		An integer/string representing the CF Standard Name version. eg. 66 or '66'
		If left blank, it defaults to the latest (current) version.

	RETURNS:
	A list of strings representing the CF Standard Names.
	"""
	root = getRoot(getResponse(v))
	if root is None:
		raise Exception("This version was not found on the CF Standard Name Webpage. Please verify the version number again.")

	positions = getStandardNamePositions(getTags(root))
	standardNames = []
	for i in range(positions[0], positions[1]):
		standardNames.append(root[i].attrib['id'])
	return standardNames

def descriptions(v = "current"): # Call
	"""
	SUMMARY:
	Shows all descriptions in this version of the CF Standard Names.

	PARAMETERS:
	v (int, default = "current"): 
		An integer/string representing the CF Standard Name version. eg. 66 or '66'
		If left blank, it defaults to the latest (current) version.

	RETURNS:
	A list of strings representing the descriptions for each CF Standard Name.
	"""
	root = getRoot(getResponse(v))
	if root is None:
		raise Exception("This version was not found on the CF Standard Name Webpage. Please verify the version number again.")

	positions = getStandardNamePositions(getTags(root))
	descriptions = []
	for i in range(positions[0], positions[1]):
		descriptions.append(root[i][3].text)
	return descriptions

def uom(v = "current"): # Call
	"""
	SUMMARY:
	Shows all Unit of Measures in this version of the CF Standard Names.

	PARAMETERS:
	v (int, default = "current"): 
		An integer/string representing the CF Standard Name version. eg. 66 or '66'
		If left blank, it defaults to the latest (current) version.

	RETURNS:
	A list of strings representing the Unit of Measure for each CF Standard Name.
	"""
	root = getRoot(getResponse(v))
	if root is None:
		raise Exception("This version was not found on the CF Standard Name Webpage. Please verify the version number again.")

	positions = getStandardNamePositions(getTags(root))
	units = []
	for i in range(positions[0], positions[1]):
		units.append(root[i][0].text)
	return units

def grib(v = "current"): # Call
	"""
	SUMMARY:
	Shows all grib tag values in this version of the CF Standard Names.

	PARAMETERS:
	v (int, default = "current"): 
		An integer/string representing the CF Standard Name version. eg. 66 or '66'
		If left blank, it defaults to the latest (current) version.

	RETURNS:
	A list of strings representing the grib tag values for each CF Standard Name.
	"""
	root = getRoot(getResponse(v))
	if root is None:
		raise Exception("This version was not found on the CF Standard Name Webpage. Please verify the version number again.")

	positions = getStandardNamePositions(getTags(root))
	grib = []
	for i in range(positions[0], positions[1]):
		grib.append(root[i][1].text)
	return grib

def amip(v = "current"): # Call
	"""
	SUMMARY:
	Shows all amip tag values in this version of the CF Standard Names.

	PARAMETERS:
	v (int, default = "current"): 
		An integer/string representing the CF Standard Name version. eg. 66 or '66'
		If left blank, it defaults to the latest (current) version.

	RETURNS:
	A list of strings representing the amip tag values for each CF Standard Name.
	"""
	root = getRoot(getResponse(v))
	if root is None:
		raise Exception("This version was not found on the CF Standard Name Webpage. Please verify the version number again.")

	positions = getStandardNamePositions(getTags(root))
	amip = []
	for i in range(positions[0], positions[1]):
		amip.append(root[i][1].text)
	return amip

def aliases(v = "current"): # Call
	"""
	SUMMARY:
	Shows all alias terms in this version of the CF Standard Names.

	PARAMETERS:
	v (int, default = "current"): 
		An integer/string representing the CF Standard Name version. eg. 66 or '66'
		If left blank, it defaults to the latest (current) version.

	RETURNS:
	dict object with CF Standard Name as the key and cooresponding alias(es) as values.
	"""
	root = getRoot(getResponse(v))
	if root is None:
		raise Exception("This version was not found on the CF Standard Name Webpage. Please verify the version number again.")

	positions = getAliasNamesPositions(getTags(root))
	aliasID = []
	aliasEntries = []
	for i in range(positions[0], positions[1]):
		aliasID.append(root[i].attrib['id'])
		aliasEntries.append(root[i][0].text)
	return {aliasID[i]: [aliasEntries[i]] for i in range(len(aliasID))}

def getcf(v = "current"): # Call
	"""
	SUMMARY:
	Gets all CF Standard names along with related data. Aliases not included.

	PARAMETERS:
	v (int, default = "current"): 
		An integer/string representing the CF Standard Name version. eg. 66 or '66'
		If left blank, it defaults to the latest (current) version.
	
	RETURNS:
	dict object:
		CF Standard Name as the key.
		A list of Canonical Units, GRIB, AMIP and Description as the value.
	"""
	cfnames = standardnames(v)
	cfdescription = descriptions(v)
	cfuom = uom(v)
	cfgrib = grib(v)
	cfamip = amip(v)
	
	cfdict = {cfnames[i]: [cfuom[i], cfgrib[i], cfamip[i], cfdescription[i]] for i in range(len(cfnames))} 

	return cfdict


def compareWrapper(v, ov, tag):

	mapTag = {
		"canonical_units": 0,
		"units": 0,
		"grib": 1,
		"amip": 2,
		"description": 3
	}

	if tag not in mapTag.keys():
		raise Exception("The provided tag is not valid. Please read the documentation 'help(cf.compare)' for valid tags.")

	index = mapTag[tag]

	vDict = getcf(v)
	ovDict = getcf(ov)

	newNames = []
	udpateFor = []
	oldValue = []
	newValue = []
	for key in vDict:
		if key not in ovDict:
			newNames.append(key)
		elif key in ovDict:
			if vDict[key][index] != ovDict[key][index]:
				udpateFor.append(key) # The key for which the tag got updated
				oldValue.append(ovDict[key][index])
				newValue.append(vDict[key][index])

	metadata =	"{} new CF Standard Names have been added in {} version, since version #{}.\nThe {} tag was updated for {} existing terms.".format(len(newNames), v, ov, tag, len(udpateFor))

	updateDict = {
		"metadata": metadata,
		"newCFNames": newNames,
		"tagUpdatedFor": udpateFor,
		"oldTagValues": oldValue,
		"newTagValues": newValue
	}

	return updateDict

def compare(ov, v = "current", tag = None): # Call
	"""
	SUMMARY:
	Compares two versions of CF Standard Names

	PARAMETERS:
	ov (int): 
		An integer/string representing the older version. eg: 65 or '65'
	
	v (int, default = "current"): 
		An integer/string representing the newer version. eg. 66 or '66'
		If left blank, it defaults to the latest (current) version.

	tag (string, default = None):
		A string representing the tag name to be compared along with the Standard Name.
		Either "canonical_units" ("units" is also accepted), "grib", "amip", or "description".
		The provided tag will be compared across the two versions along with the Standard term.
		If the provided tag is None (default), all tags will be compared.
	
	RETURNS:
	dict object with the following keys:
		metadata: A summary of changes
		newCFNames: New CF Names added in the newer version
		tagUpdatedFor: The existing CF Names for which the provided tag value was updated.
		oldTagValues: Tag values in the older version.
		newTagValues: Tag values in the newer version.
	"""

	if ov == 'current':
		raise Exception("The older version cannot be 'current', please provide a valid older version.")

	if v != 'current':
		if int(v) <= int(ov):
			raise Exception("The older version (ov) should be smaller than the newer version (v). Please re-enter valid version numbers.")

	if tag is not None:
		comparison = compareWrapper(v, ov, tag)
	else:
		comparison = []
		for tag in ["units", "grib", "amip", "description"]:
			comparison.append(compareWrapper(v, ov, tag))
			## NEEDS SOME WORK

	return comparison

def cfname(standardName, v = "current"):
	"""
	SUMMARY:
	Get all details corresponding to a CF Standard Name from a specific version.

	PARAMETERS:
	standardName (string): 
		A string representing the CF Standard Name.
	
	v (int, default = "current"): 
		An integer/string representing the CF Standard Name version. eg. 66 or '66'
		If left blank, it defaults to the latest (current) version.
	
	RETURNS:
	dict object with the following keys:
		entry: CF Standard Name
		canonical_units: Value of the <canonical_units> XML tag
		grib: Value of the <grib> XML tag
		amip: Value of the <amip> XML tag
		description: Value of the <description> XML tag
	"""
	cfnames = standardnames(v)
	
	if standardName not in cfnames:
		raise Exception("The provided standard name does not exist in this version of CF Standard Names.")

	index = cfnames.index(standardName)

	root = getRoot(getResponse(v))

	cfdict = {
		"entry": standardName,
		"canonical_units": root[index][0].text,
		"grib": root[index][1].text,
		"amip": root[index][2].text,
		"description": root[index][3].text
	}

	return cfdict

def find(keywords, v = "current"):
	"""
	SUMMARY:
	Find if a standard name exists in the provided version of CF Standard Names.
	If not an exact match, get all closely matching standard names.

	PARAMETERS:
	keywords (string or list of strings): 
		A keyword or list of keywords which will be matched to a standard name.
	
	v (int, default = "current"): 
		An integer representing the newer version. eg. 66
		If left blank, it defaults to the latest (current) version.

	RETURNS:
	A list of dict objects. Each dict object has the following keys:
		key: The keyword provided
		exactMatch: A string of the CF Standard Name if an exact match is found. None if no exact match.
		partialMatch: A list of strings partially matching the keyword. None if no partial match.
	"""
	cfnames = standardnames(v)

	if type(keywords) != list:
		keywords = [keywords]

	def searchkey(key):
		exactMatch = None
		partialMatch = []
		for cfn in cfnames:
			if key == cfn:
				exactMatch = cfn
			elif key in cfn:
				partialMatch.append(cfn)

		if len(partialMatch) < 1:
			partialMatch = None

		matchDict = {
			"key": key,
			"exactMatch": exactMatch,
			"partialMatch": partialMatch
		}

		return matchDict

	if len(keywords) == 1:
		return searchkey(keywords[0])
	else:
		matched = []
		for key in keywords:
			matched.append(searchkey(key))
		return matched