from pathlib import Path
import yaml

curpath = Path('.').resolve()
personfile = curpath / 'people' / 'stephen.yaml'

with open(personfile) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    print(yaml.dump(data))


    pass