import yaml

def loadConfig():
    with open("config.yaml", "r") as f:
      config = yaml.safe_load(f)
      return config