import yaml

config: None|dict = None
with open('config.yml', 'r', encoding='utf8') as f:
    config = yaml.safe_load( f.read() )
