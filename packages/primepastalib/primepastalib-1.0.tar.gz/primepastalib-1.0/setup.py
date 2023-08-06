from distutils.core import setup

long_description = """
Makes the necessary changes to your django files and deploys them to heroku.

Usage:

from primepastalib import herokuLogin, djangoDeploy

#projectName is the name of your django project, and appName is the name that you'd your heroku app to have.

#adds the required files and makes changes to the settings.py file, and deploys them to heroku. Make sure you're logged in. Heroku will choose a name for the app.

djangoDeploy('projectName')

#Does the same as above, except the name you pass will be used for the app.

djangoDeploy('projectName', 'appName')

#You can also login to heroku by running the following: (It is recommended that you log into the heroku CLI yourself.)

herokuLogin()
"""

setup(
  name = 'primepastalib',         # How you named your package folder (MyLib)
  packages = ['primepastalib'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Helps in deploying django files to heroku.',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'primepasta',                   # Type in your name
  author_email = 'theprimepasta@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/primepasta/primepastalib',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/primepasta/primepastalib/archive/v_08.tar.gz',    # I explain this later on
  keywords = ['django', 'heroku', 'deploy'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
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
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)