from setuptools import setup, find_packages


DESCRIPTION = """
            Detection of outlier with mahanalobis distance 
            which have access of the parameters (means and precision matrice) with algo GMM or Bayesian GMM provide by sklearn
            """
setup(
    name="Mahanalobis_Detection_Outliers",
    version="1.0",
    author="Jonathan Ndamba",
    author_email="jonathan.ndamba.pro@gmail.com",
    url="https://github.com/JonathanNdambaPro/MDO",
    description=DESCRIPTION,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pandas>=1.0.5',
                      'scikit-learn>=0.23.1',
                      'sklearn>=0.0'
                      ]
)



