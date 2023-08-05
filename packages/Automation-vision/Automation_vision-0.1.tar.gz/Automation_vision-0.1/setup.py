from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

# with open('HISTORY.md') as history_file:
#     HISTORY = history_file.read()

setup_args = dict(
    name='Automation_vision',
    version='0.1',
    description='auto clicking and writing',
    long_description_content_type="text/markdown",
    long_description=README ,
    license='MIT',
    packages=find_packages(),
    author='AyazYousafxai',
    author_email='ayazpk6630@gmail.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)

install_requires = [
    'certifi==2020.6.20',
    'chardet==3.0.4','idna==2.10','MouseInfo==0.1.3','numpy==1.19.1','opencv-python==4.3.0.36'
    ,'pandas==1.0.5','Pillow==7.2.0','PyAutoGUI==0.9.50','PyGetWindow==0.0.8','PyMsgBox==1.0.8','pyperclip==1.8.0'
    ,'PyRect==0.1.4','PyScreeze==0.1.26'
    ,'python-dateutil==2.8.1','PyTweening==1.0.3'
    ,'pytz==2020.1','pywin32==228'
    ,'six==1.15.0','urllib3==1.25.10'
]

if __name__ == '__main__':
    # setup(**setup_args)
    setup(**setup_args, install_requires=install_requires)