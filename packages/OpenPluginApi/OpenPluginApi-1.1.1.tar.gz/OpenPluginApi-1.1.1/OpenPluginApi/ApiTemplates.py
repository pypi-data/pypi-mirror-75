def help():
    message = """
Api Templates.
templates:
  BlankApi
  EnableDisableApi
"""
    print(message)
    return message

class BlankApi:
    def __init__(self, version  = "0.0.1", name = "My Plugin"):
        self.INFO = {'type':'blank', 'version':version, 'name':name}
    
    def start(self):
        None

class EnableDisableApi:
    def __init__(self, version  = "0.0.1", name = "My Plugin"):
        self.INFO = {'type':'Enable-Disable', 'version':version, 'name':name}
        self.FUNCS = {}
    def start(self):
        None
    def Enable(self, func):
        self.FUNCS['ENABLE'] = func
    def Disable(self, func):
        self.FUNCS['DISABLE'] = func