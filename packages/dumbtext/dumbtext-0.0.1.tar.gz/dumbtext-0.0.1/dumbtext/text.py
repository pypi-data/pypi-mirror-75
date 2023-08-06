from uuid import uuid4


def save(data, name=None, random_name=False):
    if random_name:
        name = "./" + str(uuid4())[:8] + ".txt"
    elif name is None:
        name = "default.txt"
    try:
        with open(name, 'w') as f:        
            f.writelines(data)
    except:
        pass


def load(name=None):
    if name is None:
        name = "./default.txt"
    try:
        with open(name, 'r') as f:        
            data = f.readlines()
        return data
    except:
        return []
    