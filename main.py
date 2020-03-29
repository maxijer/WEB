from zipfile import ZipFile
import json


def make_reserve_arc():
    count = 0
    with ZipFile('input.zip') as myzip:
        for i in myzip.namelist():
            if '.json' in i:
                with myzip.open(f'{i}', 'r') as file:
                    mast = json.loads(file.read())
                    if mast["city"] == "Москва":
                        count += 1
    return count


print(make_reserve_arc())
