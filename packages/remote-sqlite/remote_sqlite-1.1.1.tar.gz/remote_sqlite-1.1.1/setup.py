from setuptools import setup

with open('README.md') as f:
  long_description = f.read()

setup(
  name = 'remote_sqlite',         # How you named your package folder (MyLib)
  packages = ['remote_sqlite'],   # Chose the same as "name"
  version = '1.1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'RemoteSqlite is a way to easily access a remote Sqlite database and perform queries',   # Give a short description about your library
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  author = 'Vijay Balasubramaniam',                   # Type in your name
  author_email = 'your.email@domain.com',      # Type in your E-Mail
  url = 'https://github.com/vbalasu/RemoteSqlite',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/vbalasu/RemoteSqlite/archive/v1.1.tar.gz',
  keywords = ['sqlite3', 'remote'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
      'fs',
      'fs-s3fs',
      'fs.sshfs'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
