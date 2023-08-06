import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'pyolxbrazil',         # How you named your package folder (MyLib)
  packages = ['pyolxbrazil'],   # Chose the same as "name"
  version = '1.0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Scrapper for OLX Brazil',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Luís Eduardo Pompeu',                   # Type in your name
  author_email = 'luiseduardobr1@hotmail.com',      # Type in your E-Mail
  url = 'https://github.com/luiseduardobr1/pyolxbrazil',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/luiseduardobr1/pyolxbrazil/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['SCRAPPER', 'OLX', 'BRAZIL'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
          'beautifulsoup4',
          'fake-useragent'
      ],
  classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)