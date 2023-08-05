import setuptools
with open('README.md','r') as fh:
    long_description = fh.read()
setuptools.setup(
  name = 'OpenPluginApi',         # How you named your package folder (MyLib)
  packages = setuptools.find_packages(),   # Chose the same as "name"
  version = '1.1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Allows you to easily create a full plugin system for your project.',   # Give a short description about your library
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  author = 'Benjamin Tyler Austin Jr',                   # Type in your name
  author_email = 'BTAustin1122@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/spidertyler2005/openPluginApi',   # Provide either the link to your github or to your website
  keywords = ['OPA', 'Plugin', 'PluginApi', 'Plugin Api Creator', 'Open Plugin Api'],   # Keywords that define your package best
  python_requires = '>=3.6',
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
)