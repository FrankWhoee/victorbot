import requests

names = []
rangemax = 899
progresslevel = 0
for i in range(1, rangemax):
    try:
        compare = requests.get("https://pokeapi.co/api/v2/pokemon/" + str(i)).json()
    except:
        continue
    names.append(compare["name"])
    print(str(i) + ":" + compare["name"])
for i in range(10001, 10221):
    try:
        compare = requests.get("https://pokeapi.co/api/v2/pokemon/" + str(i)).json()
    except:
        continue
    names.append(compare["name"])
    print(str(i) + ":" + compare["name"])

print(names)
