import setuptools

with open("README.md", "r") as doc:
    long_description = doc.read()

setuptools.setup(
    name='qr_code_generator_api',
    version='0.1.2',
    author='Job Veldhuis',
    author_email='job@baukefrederik.me',
    description='Python wrapper for qr-code-generator.com API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jobveldhuis/python-qr-code-generator-api',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'requests',
        'pyYaml',
    ],
    entry_points='''
    [console_scripts]
    qr_code_generator=qr_code_generator.__main__:main
    ''',
    python_requires='>=3.6'
)
