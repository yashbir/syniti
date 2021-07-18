# Read data into the application
# pass json data to rule executor
# return result
import constants
from data_helper import DataHelper
from rule_engine import RuleEngine

data = DataHelper.load_data(constants.data_file_path)
invalid_data = RuleEngine.apply_rules(data) 
for d in invalid_data:
    print(d)
