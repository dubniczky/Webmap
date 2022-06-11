import yaml

config: None|dict = None
with open("config.yml") as f:
    config = yaml.safe_load( f.read() )

ignorelist: None|list(str) = None
with open(config.ignorelist) as f:
    ignorelist = f.readlines()
