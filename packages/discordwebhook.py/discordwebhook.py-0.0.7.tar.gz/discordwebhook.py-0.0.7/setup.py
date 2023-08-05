from distutils.core import setup
long_description="""
| A simple python package for posting to discord webhooks in python
| Has asynchronous and synchronous options

Example

.. code-block:: python 

  from discordwebhook import create # Import discordwebhook create

  webhook = create.Webhook() # Create Webhook object
  embed = create.Embed() # Create embed object

  webhook.username("Example Webhook") # Override webhook username as 'Example Webhook'
  webhook.message("Hello! This is a message from an example webhook with the `discordwebhook.py` library!") # Message to go with the embed

  embed.title("Github Logo") # Embed title as 'Github Logo'
  embed.image(url="https://image.flaticon.com/icons/png/512/25/25231.png") # Embed image as github logo
  embed.color(0x808080) # Gray embed color

  webhook.send("WEBHOOK_URL", embed=embed) #Send webhook to given link with the embed

**0.0.7 Changelog**

 | Added discordwebhook.discordwebhook
 | `discordwebhook.fetch.Webhook()` now supports a Webhook() object instead of just string
 | Changed `discordwebhook.discordwebhook.version.recent` to `current` with alias `recent`
 | When using webhooks set information is stored in variables and can be accessed later by using (webhook).(setData), for example webhook.message
 | Added message and tts kwarg to .send to allow for one line webhook sends
 | Added kwargs to embed creation to create an experience identical to discord.py
 | Added docstrings at the top of files
 | Started error handling for embeds, checks on send to keep projects working

"""
version = "0.0.7"
setup(
  name = 'discordwebhook.py',         
  packages = ['discordwebhook'],   
  version = version,     
  license='MIT',       
  description = 'Easily using discord webhooks in python - asynchronous and synchronous - documented at https://discordwebhook.readthedocs.io/en/latest/', 
  documentation_url="https://discordwebhook.readthedocs.io/en/latest/",  
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Coolo2',                   
  author_email = 'itsxcoolo2@gmail.com',      
  url = 'https://github.com/Coolo22/discordwebhook.py',   
  download_url = 'https://github.com/Coolo22/discordwebhook.py/raw/master/Archive/discordwebhook.py-' + version + '.tar.gz',    
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
    'Programming Language :: Python :: 3.8',
  ],
)