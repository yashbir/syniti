# Test the rule engine with test data
from data_helper import DataHelper
from rule_engine import RuleEngine

data = DataHelper.load_data('test.json')
print(data)
invalid_data = RuleEngine.apply_rules(data) 
print('########################### Invalid records ###########################')
for d in invalid_data:
    print(d)