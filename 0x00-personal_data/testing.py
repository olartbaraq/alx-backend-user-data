import re
import logging


txt = ["name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;", "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]

x = re.search("password", txt[0])
if x:
    print("YES! We have a match!")
else:
    print("No match")

