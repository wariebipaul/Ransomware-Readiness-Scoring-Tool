from setuptools import setup, find_packages

setup(
    name='ransomware-resilience-tool',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A tool to assess and improve organizational readiness against ransomware attacks.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/ransomware-resilience-tool',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # List your project dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)