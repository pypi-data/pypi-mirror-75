import os

def help():
    message = """
Loads Plugins
"""
    print(message)
    return message

def load(FileName: str, globals, locals):
    with open(FileName) as f:
        exec(f.read(),globals, locals)

def loadFolder(FolderName: str, globals, locals, recursive = False):
    files = os.listdir(FolderName)
    for file in files:
        if ".py" in file:
            with open(FolderName+'/'+file) as f:
                exec(f.read(),globals, locals)
        elif recursive == True:
            loadFolder(FolderName+'/'+file, globals, locals, recursive = True)
