
def dirfind(obj, text):
    return list(filter(lambda x: text in x, dir(obj)))