import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    #Here is the module name.
    name="chatbot_ner",

    #version of the module
    version="0.0.5",

    #Name of Author
    author="gnani",

    #your Email address
    author_email="suman@gnani.ai",

    license="GNU",

    #Small Description about module
    description="date and time entity extractor",

    #long_description=long_description,

    #Specifying that we are using markdown file for description
    # long_description_content_type="text/markdown",


    #Any link to reach this module, if you have any webpage or github profile
    url="https://github.com/hellohaptik/chatbot_ner",

    packages=setuptools.find_packages(),


    package_data = {
        # If any package contains *.txt or *.rst .......files, include them:
        '': ['*.txt', '*.csv', '*.crv','*.conf' ,'*.sh','*.json','*.md','*.crf', '*.yml','*.jpg','*.svg','*.png','*.html','*.css','*.js',],
    },

    # include_package_data=True,

    install_requires=[
'cython',
'phonenumberslite==8.10.18',
'six==1.11.0',
'pytz==2014.2',
'nltk==3.4.5',
'numpy==1.16',
'elasticsearch==5.5.0',
'requests==2.20.0',
'requests-aws4auth==0.9',
'Django==1.11.29',
'django-dotenv==1.4.2',
'weighted-levenshtein==0.1',
'regex==2018.7.11',
'ipython',
'word2number==1.1',
'python-crfsuite==0.9.6',
'boto==2.49.0',
'boto3==1.8.4',
'python-dateutil==2.7.3',
'pandas==1.0.3',
'mock==2.0.0',
'django-nose==1.4.5',
'typing==3.6.2',
'flake8==3.4.1',
'pyaml==19.4.1',
'coverage==4.5.3',
'nose-exclude==0.5.0',
      ],


    #classifiers like program is suitable for python3, just leave as it is.
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

