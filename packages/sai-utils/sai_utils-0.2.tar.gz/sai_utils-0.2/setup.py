from distutils.core import setup
setup(
  name = 'sai_utils',         # How you named your package folder (MyLib)
  packages = ['sai_utils'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Practice library for publishing to PyPi',   # Give a short description about your library
  author = 'Sai',                   # Type in your name
  author_email = 'SaiPenamakuri@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/saipenamakuri/sai_utils',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/saipenamakuri/sai_utils/archive/v_02.tar.gz',    # I explain this later on
  keywords = ['utilities'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'Pillow'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
  ],
)
