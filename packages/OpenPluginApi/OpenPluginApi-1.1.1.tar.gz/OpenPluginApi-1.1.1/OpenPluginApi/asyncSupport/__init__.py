import OpenPluginApi.asyncSupport
import OpenPluginApi.asyncSupport.PluginLoader
def help():
    message = """
REQUIREMENTS:
  aiofiles
  asyncio
  aiohttp
OPA.async:
  PluginLoader
"""
    print(message)
    return message