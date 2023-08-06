from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name= 'cloud-toolkit',
    version= '1.0.9',
    url='https://github.com/GaryHsu77/cloud-iot-toolkit',
    keywords=['cloud', 'iot', 'azure', 'aws'],
    description= 'A toolkit help to management cloud iot.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3.7',
        ],
    license= 'MIT License',
    install_requires=[
        'requests',
        'azure-eventhub',
        'boto3',
        'awscli',
        'AWSIoTPythonSDK',
        ],
    author= 'garyhsu',
    author_email= 'bibbylong@hotmail.com',
    packages=find_packages(),
    platforms= 'any',
    python_requires='>=3.6',
)
