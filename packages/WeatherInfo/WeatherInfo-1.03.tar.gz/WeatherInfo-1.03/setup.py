from distutils.core import setup
setup(
  name = 'WeatherInfo',         # How you named your package folder (MyLib)
  packages = ['WeatherInfo'],   # Chose the same as "name"
  version = '1.03',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Takes city name as input and gives youy weather for 5 days.',   # Give a short description about your library
  author = 'Palitha Sriraj',                   # Type in your name
  author_email = 'srirajpalitha@gmail.com',      # Type in your E-Mail
  install_requires=[            # I get to this in a second
          'requests'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)