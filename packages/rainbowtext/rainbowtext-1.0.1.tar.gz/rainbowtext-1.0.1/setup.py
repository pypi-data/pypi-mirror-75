from distutils.core import setup
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
  name = 'rainbowtext',         # How you named your package folder (MyLib)
  packages = ['rainbowtext'],   # Chose the same as "name"
  version = '1.0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Simple Python Library that allows you to create rainbow colored text',
  long_description=long_description,
  author = 'TheDebianGuy',                   # Type in your name
  author_email = 'debianguy@protonmail.com',      # Type in your E-Mail
  url = 'https://github.com/TheDebianGuy/SPL',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/TheDebianGuy/SPL/raw/master/rainbowtext/rainbowtext.py',    # I explain this later on
  keywords = ['rainbow', 'text', 'rainbowtext', 'python'],   # Keywords that define your package best
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
