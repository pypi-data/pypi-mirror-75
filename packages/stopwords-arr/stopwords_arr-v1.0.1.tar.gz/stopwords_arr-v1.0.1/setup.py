from distutils.core import setup
setup(
  name = 'stopwords_arr',         # How you named your package folder (MyLib)
  packages = ['stopwords_arr'],   # Chose the same as "name"
  version = 'v1.0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'stopwords for arabic language',   # Give a short description about your library
  author = 'Ziyad Al-Qahtani',                   # Type in your name
  author_email = 'ziyadmsq@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Ziyadmsq/stopwords_arr',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/ziyadmsq/stopwords_arr/archive/v1.0.1.tar.gz',    # I explain this later on
  keywords = ['stopword', 'NLP', 'arabic', 'tokens'],   # Keywords that define your package best
#   install_requires=[            # I get to this in a second
#           'pickle',
#       ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)