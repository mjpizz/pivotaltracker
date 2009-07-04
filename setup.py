import os
from distutils.core import setup

setup(
    name="pivotaltracker",
    packages=["pivotaltracker"],
    version="0.0.1",
    license="BSD",
    author="Matt Pizzimenti",
    author_email="mjpizz+pivotaltracker@gmail.com",
    url="http://pypi.python.org/pypi/pivotaltracker/",
    install_requires=["PyYAML"],
    # install_recommends=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Software Development",
    ],
    description="pivotaltracker is a Pythonic wrapper around the PivotalTracker API",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.txt")).read(),
    entry_points='''
[console_scripts]
pt = pivotaltracker.tool:run
''',
    # zip_safe=False,
    # cmdclass=cmdclass,
    # ext_modules=ext_modules,
    )