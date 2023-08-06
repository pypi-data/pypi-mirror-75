# cfcompare: Access CF Standard Names

## What does the package do?
**cfcompare** lets you access CF Standard Names defined at http://cfconventions.org/.

## Installation
```python
pip install cfcompare as cf
```

## Getting help
```python
help(cf) # Read complete documentation of the package

# Documentation surrounding individual functions can be accessed using
help(cf.function_name)
```

## Overview

### See version details.
```python
cf.version() # Defaults to current version
# 'Version: 72,  released on 2020-03-10T11:52:02Z by Centre for Environmental Data Analysis. Contact: support@ceda.ac.uk'

cf.version(71) # Fetch details for an older version
# 'Version: 71,  released on 2020-02-04T12:00Z by Centre for Environmental Data Analysis. Contact: support@ceda.ac.uk'
```

**_Note_**: All functions within the package exhibit similar behavior in terms of arguments passed. If run without an argument, all information is fetched from the current version of CF Standard Names. If information from a previous version is required, users can pass that version number as an argument.

### Get Standard Names, Decription, Units of Measurements etc.
```python
standard_names = cf.standardnames() # Returns a list of all standard names from the current version

sn_descriptions = cf.descriptions() # Returns a list of all standard name descriptions from the current version

sn_uom = cf.uom() # Returns a list of all standard name unit of measure (Canonical Units) from the current version

sn_grib = cf.grib() # Returns a list of grib tag values for each CF Standard Name.

sn_amip = cf.amip() # Returns a list of amip tag values for each CF Standard Name.
```

### Get all data in one go
```python
sn_data = cf.getcf()

# Returns a dictionary:
		# CF Standard Name as the key.
		# A list of Canonical Units, GRIB, AMIP and Description as the value.

sn_data['altitude'] # Fetch details from the dictionary
> ['m', '8', '8', 'Altitude is the (geometric) height above the geoid, which is the reference geopotential surface. The geoid is similar to mean sea level.']

```

### Get CF Standard Name Aliases
```python
sn_aliases = cf.aliases() # Return a dictionary with CF Standard Name as the key and cooresponding alias(es) as values.

sn_aliases['longwave_radiance']
> ['isotropic_longwave_radiance_in_air'] # Alias of the term
```

### Compare two CF versions
```python
sn_compare = cf.compare(65, v = 'current', tag = None) # Compare all data of version 65 to the current version
# Returns a ductionary object with differences across CF Standard names, Descriptions, Units of Measure, AMIP and GRIB tag values.

sn_compare = cf.compare(65, 70, tag = 'description') # Compare CF Standard Names and Descriptions of version 65 and 70

sn_compare = cf.compare(65, 66, tag = 'units') # Compare CF Standard Names and Units of version 65 and 70
```

### Access details of a specific CF Standard Name
```python
cf_altitude = cf.cfname('altitude') # Returns a dictionary with each tag of the CF Standard Name and its value

cf_altitude['entry'] # Access the Standard Name
> 'altitude'

cf_altitude['description'] # Access the description
> 'An altimeter operates by sending out a short pulse of radiation and measuring the time required for the pulse to return from the sea surface; this measurement is used to calculate the distance between the instrument and the sea surface.  That measurement is called the "altimeter range" and does not include any range corrections.'
```

### Search for a CF Standard Name
```python
search_alt= cf.find('altitude') # Search for all standard names that exactly or partially match this keyword. Can pass multiple keywords as a list.
# Returns a dictionary object if a single keyword is passed or a list of dictionaries if multiple keywords are passed.

search_alt['exactMatch']
> 'altitude'

search_alt['partialMatch'] # Returns a list of all CF Standard Names partially matching the keyword
> ['altitude_at_top_of_atmosphere_model', 'altitude_at_top_of_dry_convection', 'barometric_altitude', 'bedrock_altitude', 'bedrock_altitude_change_due_to_isostatic_adjustment', 'cloud_base_altitude', 'cloud_top_altitude', 'convective_cloud_base_altitude', 'convective_cloud_top_altitude', 'equilibrium_line_altitude', 'freezing_level_altitude', 'ground_level_altitude', 'surface_altitude', 'tendency_of_bedrock_altitude', 'tropopause_altitude', 'water_surface_reference_datum_altitude']
```

## Origins
This package originated out of a discussion during the 2020 CF Workshop held virtually (thank you COVID!) from June 9-11. The original requirment was to give users the ability to track changes across different version of CF Standard Names. This package provides that functionality along with several other additions.

**_Note_**: This package is a personal project by the author and is in no way sponsored, or recommended for use by the CF Governance Committee.