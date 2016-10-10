import uuid


######################
##### Generators #####
######################

# compress UUID
# UUID to more compact form (string of 22 characters)
def uuid2compact(uuid):
	return uuid.bytes.encode('base64'.rstrip('=\n').replace('/','_'))

# decompress UUID
# from string of 22 characters to UUID
def compact2uuid(uuid_compact):
	return str(uuid.UUID(bytes=(uuid_compact + '==').replace('_','/').decode('base64')))

# generate unique id's using python's uuid module
# uuid4(): generates unique uuid from random number
# returns unique userid or transferid as str
def id_generator():
	return str(uuid.uuid4())
#	return uuid2compact(uuid.uuid4())

