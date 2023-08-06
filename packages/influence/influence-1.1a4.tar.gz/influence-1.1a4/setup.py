from setuptools import setup

md = []
with open('/Users/SchoolOfficial/Desktop/influence/README.rst', 'r') as f:
    for line in f:
        md.append(str(line))
ld = ''
for i in md:
    ld += i + "\n"

setup(
  name = 'influence',         # How you named your package folder (MyLib)
  packages = [
        'influence',
        'influence.math',
        'influence.list',
        'influence.string',
        'influence.array',
        'influence.dict',
        'influence.set',
  ],
  version = '1.1a4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A utility package influenced by java, coded in python',   # Give a short description about your library
  long_description = ld,
  author = 'Neil',                   # Type in your name
  author_email = 'nghugare2@outlook.com',      # Type in your E-Mail
  url = 'https://github.com/RandomKiddo/influence',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/RandomKiddo/influence/archive/v1.1a4.tar.gz',    # I explain this later on
  keywords = ['PYTHON', 'EXTENDER', 'UPGRADER'],   # Keywords that define your package best
  #install_requires=[            # I get to this in a second
          #'numpy',
          #'matplotlib',
          #'wheel',
      #],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.8',
  ],
  #setup_requires=['wheel'],
)
