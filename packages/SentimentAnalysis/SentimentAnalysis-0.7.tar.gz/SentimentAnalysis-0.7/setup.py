from distutils.core import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'SentimentAnalysis',         # How you named your package folder (MyLib)
  packages = ['AnalyseSentiment'],   # Chose the same as "name"
  version = '0.7',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Helps to analyse sentiment',   # Give a short description about your library
  long_description = long_description,
  author = 'Arun Kesavan',                   # Type in your name
  author_email = 'arunkottilukkal@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/arunkottilukkal/AnalyseSentiment',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/arunkottilukkal/AnalyseSentiment/archive/v_07.tar.gz',    # I explain this later on
  keywords = ['Sentiment Analysis', 'Sentence Sentiment', 'Emotion Analysis'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
          'urllib3',
          'vaderSentiment',
          'nltk',
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

# import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

# setuptools.setup(
#     name="SentimentAnalysis", # Replace with your own username
#     version="0.5.0",
#     author="Arun Kesavan",
#     author_email="arunkottilukkal@gmail.com",
#     description="A small example package",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/arunkottilukkal/AnalyseSentiment",
#     packages=setuptools.find_packages(),
#     download_url = 'https://github.com/arunkottilukkal/AnalyseSentiment/archive/v_05.tar.gz',    # I explain this later on
#     keywords = ['Sentiment Analysis', 'Sentence Sentiment', 'Emotion Analysis'],   # Keywords that define your package best
#     install_requires=[
#       'requests',
#       'urllib3',
#       'vaderSentiment',
#       'nltk',
#     ],
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires='>=3.6',
# )