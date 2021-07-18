# Read rules from rules.json
# apply rules on the given data
# Return invalid data
import constants
import re
from data_helper import DataHelper

class RuleEngine:

    valid_check = 'VALID'

    @classmethod
    def apply_rules(cls, data):
        """Apply rules on the given data

        Args:
            data (list): list of user data dictionaries

        Returns:
            set: set of invalid record IDs
        """
        invalid_data = set()
        valid_indexed_data = {}
        rules = cls.load_rules()
        for d in data:
            data_check = True
            for r in rules:
                validator = getattr(cls, r)
                result = validator(d, valid_indexed_data)
                if result is not cls.valid_check:
                    for invalid_entry in result:
                        invalid_data.add(invalid_entry['id'])
                    data_check = False
                    break
            
            if data_check:
                DataHelper.index_data(d, valid_indexed_data)

        return invalid_data


    @classmethod
    def load_rules(cls):
        return DataHelper.load_data(constants.rules_file_path)

    @classmethod
    def validate_duplicates(cls, record, valid_indexed_data):
        """Check duplicates in the data

        Args:
            record (dict): user data dictionary
            valid_indexed_data (dict): valid indexed data

        Returns:
            list or string: list if duplicates exist else VALID
        """
        zip = record['zip'].strip()
        name = record['name'].strip()
        address = record['address'].strip()
        if zip in valid_indexed_data:
            if name in valid_indexed_data[zip]:
                if address in valid_indexed_data[zip][name]:
                    return [record, valid_indexed_data[zip][name][address]]
        
        return cls.valid_check

    @classmethod
    def is_valid_attribute(cls, key, record):
        """Checks if attribute is valid in the data

        Args:
            key (string): key in data
            record (dict): user data dictionary

        Returns:
            boolean: True if valid key else False
        """
        if key not in record or record[key] is None or len(record[key].strip()) == 0:
            return False
        
        return True

    @classmethod
    def validate_name(cls, record, valid_indexed_data):
        return cls.valid_check if cls.is_valid_attribute('name', record) else [record]
    
    @classmethod
    def validate_address(cls, record, valid_indexed_data):
        return cls.valid_check if cls.is_valid_attribute('address', record) else [record]
    
    @classmethod
    def validate_zipcode(cls, record, valid_indexed_data):
        if not cls.is_valid_attribute('zip', record):
            return [record]

        # Regex to check if zip is valid US zipcode
        pattern = re.compile('(^\d{5}$)|(^\d{5}-\d{4}$)')
        if pattern.search(record['zip'].strip()) is None:
            return [record]
        
        return cls.valid_check

