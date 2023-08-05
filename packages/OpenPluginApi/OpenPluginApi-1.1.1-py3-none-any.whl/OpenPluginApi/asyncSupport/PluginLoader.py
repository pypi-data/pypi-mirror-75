import asyncio
import aiofiles
import aiohttp
import os

async def help(output = True):
    message = """
Loads Plugins
"""
    if output: print(message)
    return message

async def load(FileName: str, globals, locals):
    with aiofiles.open(FileName, mode = 'r') as f:
        exec(f.read(),globals, locals)

async def loadFolder(FolderName: str, globals, locals, recursive = False):
    files = os.listdir(FolderName)
    for file in files:
        if ".py" in file:
            with aiofiles.open(FolderName+'/'+file, mode = 'r') as f:
                exec(f.read(),globals, locals)
        elif recursive == True:
            await loadFolder(FolderName+'/'+file, globals, locals, recursive = True)

async def httpLoad(url: str, globals, locals):
   async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            if r.status == 200:
                data = await r.text()
                exec(data,globals, locals)
                return True
            else:
                return False
