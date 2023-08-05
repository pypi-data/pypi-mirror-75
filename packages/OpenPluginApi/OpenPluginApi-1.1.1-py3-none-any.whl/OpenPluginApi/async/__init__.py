import OpenPluginApi.async
import OpenPluginApi.async.PluginLoader
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