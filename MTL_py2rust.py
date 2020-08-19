import re

with open("data.txt","r") as fh:
    for line in fh:
        a = fh.read()
### Replacing triple quotes with double quotes
a = re.sub(r'\'\'\'',r'"',a)
### Reformatting location brackets
a = re.sub(r'Location\s*\(',r'Location {',a)
a = re.sub(r'(month = .+\n)\)',r'\1};',a)
### Adding let
a = re.sub(r'(loc[0-9]+ =)',r'let \1',a)

### Reformatting name data
a = re.sub(r'name =\s("[^"]+")', r'name : String::from(\1)',a)
### Reformatting longitude, latitude, year, and month data
a = re.sub(r'long =', r'long :',a)
a = re.sub(r'lat =', r'lat :',a)
a = re.sub(r'year =', r'year :',a)
a = re.sub(r'month =', r'month :',a)

### Reformatting quatier data
a = re.sub(r'quartier =\s("[^"]+")', r'quartier: String::from(\1)',a)
### Reformatting story data
a = re.sub(r'story =\n    \"([^\"]*)"', r'story: String::from("\1")',a)
### Reformat final vector
a = re.sub(r'locations = (\[[^\]]*\])',r'let data = vec!\1;',a)
### Verify that it looks good
print(a)
### Write to file
with open("data_converted.txt","w") as fh:
    for line in a:
        fh.write(line)
