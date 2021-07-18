# Read json file
# do json_decode if needed and return the data
import json

class DataHelper:
    
    @classmethod
    def load_data(cls, file_path):
        """loads json data from a file

        Args:
            file_path (string): location of file

        Returns:
            dict: decoded json data
        """
        f = open(file_path)
        data = json.load(f)
        f.close()
        return data

    @classmethod
    def index_data(cls, record, data_dict):
        """index data as zip_name_address

        Args:
            record (dict): user data
            data_dict (dict): dict with indexed user data
        """
        data_dict[record['zip'].strip()] = {
            record['name'].strip(): {
                record['address'].strip(): record
            }
        }
