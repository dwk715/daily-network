import yaml
f = open(r'ping\SH_5525B.yml')
y = yaml.load(f)
ya = y['commonds'][0]
print ya