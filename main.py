from dataclasses import is_dataclass, dataclass


@dataclass
class Data:
    """

    Data

    The `Data` class is a data container that allows easy manipulation and conversion between dictionary and
     object-like access.

    Methods:
    - `__init__(self, **kwargs)`: Constructor method that initializes the `Data` object with provided key-value pairs.
    - `from_dict(cls, data_dict)`: Class method that creates a `Data` object from a dictionary.
    - `to_dict(self)`: Instance method that converts the `Data` object to a dictionary.
    - `_convert_dataclasses_to_dict(self, data)`: Internal method that converts dataclasses nested within the
     `Data` object to dictionaries.
    - `__getattr__(self, attr)`: Method that allows attribute access to the data stored in the `Data` object.
    - `__setattr__(self, attr, value)`: Method that allows setting attributes of the `Data` object.
    - `flatten_dict(self, data)`: Method that flattens a nested dictionary.
    - `_set_default_values(self)`: Internal method that sets default values for certain keys in the `_data` dictionary.
    - `__dir__(self)`: Method that returns the list of available attributes for the `Data` object.

    Note: This class uses the `is_dataclass` decorator and the `dataclass` decorator from the `dataclasses`
     module for additional functionality.

    """
    def __init__(self, **kwargs):
        """
        Initialize a Data instance.

        :param kwargs: Keyword arguments representing data attributes.
                       The keyword is the attribute name, and the value is the attribute value.

        Example:
            To create a Data instance with attributes 'name' and 'age'::

                data = Data(name='John', age=25)

        Raises:
            None.

        """
        self._data = kwargs
        self._set_default_values()

    @classmethod
    def from_dict(cls, data_dict):
        """
        Converts a dictionary into an instance of the `Data` class.

        :param data_dict: A dictionary containing the data to be converted.
        :return: An instance of the `Data` class.
        """
        return cls(**data_dict)

    def to_dict(self):
        """
        Represents a data class.

        Methods:
            to_dict: Convert the data class to a dictionary.

        """
        return self._convert_dataclasses_to_dict(self._data)

    def _convert_dataclasses_to_dict(self, data):
        """
        Convert dataclasses and nested dataclasses to dictionaries recursively.

        :param data: The data to be converted.
        :type data: Any
        :return: The converted dictionary.
        :rtype: dict
        """
        result = {}
        for key, value in data.items():
            if is_dataclass(value):
                result[key] = value.to_dict()
            elif isinstance(value, dict):
                result[key] = self._convert_dataclasses_to_dict(value)
            else:
                result[key] = value
        return result

    def __getattr__(self, attr):
        """
        :param attr: The attribute name to access.
        :return: The value of the attribute or None if attribute does not exist.

        The `__getattr__` method allows access to the attributes of instances of the `Data` class.
        It is called when an attribute is not found through normal attribute lookup.

        If the attribute exists in the `_data` dictionary of the instance, the corresponding value is returned.
        If the value is a dictionary, a new `Data` instance is created using the dictionary as input,
        and assigned as the value of the attribute.

        If the attribute starts with '_' (underscore), attribute lookup is redirected to `super().__getattribute__`,
        allowing access to private attributes and avoiding infinite recursion.

        If the attribute does not exist in the `_data` dictionary, the dictionary is flattened using `flatten_dict` function,
        and the attribute is looked up from the flattened dictionary. The value is returned if found, otherwise None is returned.

        Example usage:
            data = Data()
            value = data.some_attribute  # Accessing an attribute

            if value is not None:
                # Attribute exists, do something with the value
                pass
            else:
                # Attribute does not exist
                pass
        """
        if attr in self._data:
            value = self._data[attr]
            if isinstance(value, dict):
                self._data[attr] = Data(**value)
            return self._data[attr]
        elif attr.startswith('_'):
            return super().__getattribute__(attr)
        else:
            flatten_data = self.flatten_dict(self._data)
            return flatten_data.get(attr, None)

    def __setattr__(self, attr, value):
        """
        Sets the value of an attribute in the Data class.

        :param attr: The name of the attribute.
        :param value: The value to be assigned to the attribute.
        :return: None

        """
        if attr == '_data':
            super().__setattr__(attr, value)
        else:
            self._data[attr] = value

    def flatten_dict(self, data):
        """
        Flatten a nested dictionary.

        :param data: The nested dictionary to be flattened.
        :type data: dict
        :return: The flattened dictionary.
        :rtype: dict
        """
        items = []
        for key, value in data.items():
            if isinstance(value, dict):
                items.extend(self.flatten_dict(value).items())
            items.append((key, value))
        return dict(items)

    def _set_default_values(self):
        """
        Sets default values for metadata system if they are not already present.

        This method checks if the "metadata" key exists in the "_data" attribute of the Data object.
        If not, it creates a new "metadata" key and sets its value to an empty dictionary.

        Then, it checks if the "system" key exists in the "metadata" dictionary.
        If not, it creates a new "system" key and sets its value to an empty dictionary.

        Finally, it sets default values for the "height" and "size" keys in the "system" dictionary,
        if they are not already present, using the setdefault() method.

        :return: None
        """
        if "metadata" not in self._data:
            self._data["metadata"] = {}
        metadata = self._data["metadata"]
        if "system" not in metadata:
            metadata["system"] = {}
        system = metadata["system"]
        system.setdefault("height", 100)
        system.setdefault("size", 10)

    def __dir__(self):
        """
        Method to return a list of valid attributes for the object.

        :return: A list of valid attributes for the object.
        """
        return list(self._data.keys()) + list(super().__dir__())


# Example usage:
data = {
    "id": "1",
    "name": "first",
    "metadata": {
        "system": {
            "size": 10.7,
            "height": 11
        },
        "user": {
            "batch": 1121
        }
    }
}

# load from dict
my_inst_1 = Data.from_dict(data)

# load from inputs
my_inst_2 = Data(name="my")

# reflect inner value
print(my_inst_1.height)
print(my_inst_2.height)
