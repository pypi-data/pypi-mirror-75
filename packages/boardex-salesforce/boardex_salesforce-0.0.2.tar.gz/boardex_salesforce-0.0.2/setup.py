import setuptools

def readme():
    with open("README.md") as f:
        return f.read()

setuptools.setup(
    name="boardex_salesforce",
    version="0.0.2",
    author="BoardEx PTS",
    author_email="helpdesk@boardex.com",
    description="Downloads and Uploads to SalesForce from BoardEx stfp",
    long_description=readme(),
    long_description_content_type='text/markdown',
    url="https://aws-bxtfs01.global.root/tfs/BoardExCollection/PTS/_git/Salesforce%20Integration",
    packages = setuptools.find_packages(),
    license='MIT',
    install_requires =['simple_salesforce==1.10.1','pandas','pysftp==0.2.8','tqdm==4.48.0', 'pytest==6.0.1'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    python_requires='>=3.5',
)