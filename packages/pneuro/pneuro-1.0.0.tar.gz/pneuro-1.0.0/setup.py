from setuptools import setup

# This call to setup() does all the work


PACKAGE_NAME = 'pneuro'

# Read-in the README.md
with open('README.md', 'r') as f:
    readme = f.readlines()
readme = ''.join(readme)


setup(
    name=PACKAGE_NAME,
    long_description="pneuro Library",
    description='Template python package',
    long_description_content_type="text/markdown",
    version="1.0.0",
    author="Punit Nanda",
    author_email="punit.nanda01@gmail.com",
    license="MIT",
    packages=[  PACKAGE_NAME,
                '{}.dataLoad'.format(PACKAGE_NAME),
                '{}.dataPreprocessing'.format(PACKAGE_NAME),
                '{}.dataVisualization'.format(PACKAGE_NAME),
                '{}.fileOperations'.format(PACKAGE_NAME),
                '{}.logger'.format(PACKAGE_NAME),
                '{}.logs'.format(PACKAGE_NAME),
                '{}.models'.format(PACKAGE_NAME),
                '{}.modelTraining'.format(PACKAGE_NAME),
                '{}.prediction'.format(PACKAGE_NAME),
                '{}.static'.format(PACKAGE_NAME),
                '{}.templates'.format(PACKAGE_NAME)],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    #py_modules='{}.Autoneuro'.format(PACKAGE_NAME),
    entry_points={
        'console_scripts': [
            'pneuro = pneuro.__main__:main'
        ],
    },
    #package_dir={'':'Autoneuro'},
    install_requires=["APScheduler","certifi","click","colorhash","configparser","cycler","Flask","Flask-Cors","Flask-MonitoringDashboard","imbalanced-learn","imblearn","itsdangerous","Jinja2","joblib""kiwisolver","MarkupSafe","numpy","pandas","patsy","pymongo","pyparsing","python-dateutil","pytz","retrying","scikit-learn","scipy","seaborn","six","SQLAlchemy","statsmodels","threadpoolctl","tzlocal","Werkzeug","wincertstore","xgboost"],
)