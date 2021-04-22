import yaml

def readYaml(filename):
    with open(filename) as f:
        data = yaml.safe_load(f)
    return data

def writeYaml(a, filename):
    to_yaml = {'stocks': []}
    for a_ in a:
        to_yaml['stocks'].append(a_)
    with open(filename, 'w') as f:
        yaml.dump(to_yaml, f, default_flow_style=False)

if __name__ == '__main__':
    data = readYaml("config.yaml")
    for stock in data['stocks']:
        print(stock)
    a = ['1C', 'Tesla']
    writeYaml(a, "config.yaml")