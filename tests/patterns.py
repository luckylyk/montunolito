import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


from montunolito.core.pattern import (
    get_new_pattern, append_fingerstates_indexes, append_quarter_row,
    delete_fingerstates_indexes, set_behavior_value, set_relationship_value)


pattern = get_new_pattern()
append_quarter_row(pattern)
append_quarter_row(pattern)
append_quarter_row(pattern)
append_quarter_row(pattern)
fingerstates_indexes = (0, 1, 2, 7)
row = 0
append_fingerstates_indexes(pattern, fingerstates_indexes, 1)
append_fingerstates_indexes(pattern, fingerstates_indexes, 1)
append_fingerstates_indexes(pattern, fingerstates_indexes, 0)
append_fingerstates_indexes(pattern, fingerstates_indexes, 0)
append_fingerstates_indexes(pattern, fingerstates_indexes, 2)
append_fingerstates_indexes(pattern, fingerstates_indexes, 2)
append_fingerstates_indexes(pattern, fingerstates_indexes, 2)
append_fingerstates_indexes(pattern, fingerstates_indexes, 2)
append_fingerstates_indexes(pattern, fingerstates_indexes, 3)
append_fingerstates_indexes(pattern, fingerstates_indexes, 3)
append_fingerstates_indexes(pattern, fingerstates_indexes, 2)
delete_fingerstates_indexes(pattern, (2, 1))
delete_fingerstates_indexes(pattern, (3, 0))
set_relationship_value(pattern, (0, 1), (1, 1), 5)
set_relationship_value(pattern, (1, 1), (2, 2), 3)
set_relationship_value(pattern, (2, 2), (3, 0), 1)
set_relationship_value(pattern, (0, 1), (1, 0), 2)
set_relationship_value(pattern, (0, 1), (1, 1), 10)
print ("")
print ("Quarters")
for qindexes in pattern["quarters"]:
    print("  -->", qindexes, sep=" ")
print ("")

print ("Behaviors")
for k in sorted(pattern["behaviors"].keys()):
    print("  --> {}: {}".format(k, pattern["behaviors"][k]))
print ("")

print ("Relationships")
for k in sorted(pattern["relationships"].keys()):
    print("  --> {}: {}".format(k, pattern["relationships"][k]))
print ("")
