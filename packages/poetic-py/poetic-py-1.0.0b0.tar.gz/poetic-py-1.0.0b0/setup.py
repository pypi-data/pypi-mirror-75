import setuptools

setuptools.setup(
    name = "poetic-py",
    version = "1.0.0-Beta",
    url = "https://github.com/kevin931/poetic",
    author = "Kevin Wang",
    author_email = "bridgemarian@gmail.com",
    description = "Predicts how poetic sentences are.",
    long_description = "Please refer to http://github.com/kevin931/poetic",
    packages=["poetic"],
    install_requires = ["tensorflow>=2.1",
                        "gensim>=1.18",
                        "nltk>=3.8"
    ],
    install_package_data=True,
    data_files = [("poetic/data", ["word_dictionary_complete.txt"]),
                  ("docs"), ["gui_demo.gif", "Logo.png"]],
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only"
    ]
)