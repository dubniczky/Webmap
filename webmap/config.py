import yaml

config: None|dict = None
with open("config.yml") as f:
    config = yaml.safe_load( f.read() )
