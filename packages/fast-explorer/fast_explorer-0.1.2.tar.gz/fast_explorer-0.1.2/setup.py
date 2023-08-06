from setuptools import setup, find_packages
  
setup(
    name='fast_explorer',
    version='0.1.2',
    description='package to explore pandas data easily',
    long_description="package to explore pandas data easily",
    long_description_content_type="text/markdown",
    keywords=['pandas', 'data', 'anaysis'],
    url='',
    author='Priyal Bankar',
    author_email='bankarpriyal08@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['pandas'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3.7',
    ],
    package_data={
        # If any package contains *.txt files, include them:
        #         '': ['*.sav'],
        # And include any *.dat files found in the 'data' subdirectory
        # of the 'mypkg' package, also:
        #'customer_models': ['model_objs/*.sav'],
    })