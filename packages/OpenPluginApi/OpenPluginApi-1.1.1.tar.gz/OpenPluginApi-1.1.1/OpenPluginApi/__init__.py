import OpenPluginApi.asyncSupport
import OpenPluginApi.ApiTemplates
import OpenPluginApi.PluginLoader
import OpenPluginApi.Schedule

def help():
    message = """
OPA:
  ApiTemplates
  PluginLoader
  Schedule
"""
    print(message)
    return message