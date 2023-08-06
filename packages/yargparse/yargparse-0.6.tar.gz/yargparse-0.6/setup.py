from distutils.core import setup
setup(
  name = 'yargparse',         # How you named your package folder (MyLib)
  packages = ['yargparse'],   # Chose the same as "name"
  version = '0.6',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'YAML / Argparse merger',   # Give a short description about your library
  long_description=open('README.md', 'rt').read(),
  author = 'Joel Pfeiffer',                   # Type in your name
  author_email = 'jpfeiffe@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/jpfeiffe/yargparse',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/jpfeiffe/yargparse/archive/v_05.tar.gz',    # I explain this later on
  keywords = ['argparse', 'yaml', 'config'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pyyaml'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
