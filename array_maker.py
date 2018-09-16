def turn_property_to_array(property_key, mongo_collection):
    cursor = mongo_collection.find({}, {property_key: 1})
    new_prorperty_array = []
    for element in cursor:
        new_prorperty_array.append(element[property_key])

    return new_prorperty_array
