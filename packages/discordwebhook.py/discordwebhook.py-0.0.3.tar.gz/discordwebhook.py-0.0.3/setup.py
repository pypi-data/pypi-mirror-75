from distutils.core import setup
long_description="""
A simple python package for posting to discord webhooks in python
Has asynchronous and synchronous options
"""
setup(
  name = 'discordwebhook.py',         
  packages = ['discordwebhook'],   
  version = '0.0.3',      
  license='MIT',       
  description = 'Easily using discord webhooks in python - asynchronous and synchronous - currently undocumented',   
  long_description=long_description,
  author = 'Coolo2',                   
  author_email = 'itsxcoolo2@gmail.com',      
  url = 'https://github.com/Coolo22/discordwebhook.py',   
  #download_url = 'none',    
  keywords = ['discord', 'webhook', 'python', 'easy', 'post', 'asynchronous', 'synchronous'],   
  install_requires=['aiohttp', 'requests'],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)