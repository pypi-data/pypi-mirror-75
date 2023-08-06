from setuptools import setup

required_libraries = ["numpy", "scikit-learn", "jupyter", "pandas"]


setup(
    name="sksofia",
    version="0.1.1",
    description="a scikit learn wrapper for sofiaml",
    author="jattenberg",
    author_email="josh@attenberg.org",
    url="https://github.com/jattenberg/sksofia",
    download_url='https://github.com/jattenberg/sksofia/archive/v0.1.1.tar.gz',
    license="MIT",
    packages=['sksofia'],
    zip_safe=False,
    install_requires=required_libraries,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License', 
        'Programming Language :: Python :: 3.6',
  ],
)
