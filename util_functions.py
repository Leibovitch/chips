import pymongo

def parse_property_key(property_key):
    newsted_key_array = property_key.split()
    full_string = newsted_key_array[0]

    for word in newsted_key_array [1:len(newsted_key_array)]:
        full_string.append('[' + word + ']')

    return full_string

def turn_property_to_array(property_key, mongo_collection):
    cursor = mongo_collection.find({}, {property_key: 1})
    new_prorperty_array = []
    for element in cursor:
        exec('new_prorperty_array.append(' + parse_property_key(property_key) + ')')

    return new_prorperty_array

def haylow():
    print('great sucess!!')


