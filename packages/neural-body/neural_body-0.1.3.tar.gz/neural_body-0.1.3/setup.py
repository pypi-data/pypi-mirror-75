"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
#This block of code builds the Sphinx html files
#from sphinx.setup_command import BuildDoc
#cmdclass = {'build_sphinx': BuildDoc}

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

# Global arguments for both the setup config and the sphinx config.
name='neural_body'
version='1.1.0'
release='0.1.3'

setup(
    # This is the name of your project. The first time you publish this
    # package, this name will be registered for you. It will determine how
    # users can install this project, e.g.:
    #
    # $ pip install sampleproject
    #
    # And where it will live on PyPI: https://pypi.org/project/sampleproject/
    #
    # There are some restrictions on what makes a valid project name
    # specification here:
    # https://packaging.python.org/specifications/core-metadata/#name
    name=name,  # Required

    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    #
    # For a discussion on single-sourcing the version across setup.py and the
    # project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=release,  # Required

    # This is the code that will allow you to autogenerate your html files   
    # from the command line at the top of the tree (so in the 0_dem-sim folder directory)
    # you need to type sphinx-quickstart. Most of the options are going to be default.
    # You need to input the project name, Author names, and project release information when that appears.
    # When the option 'Name of your master document (without suffix) [index]: pops up you must type contents
    # The option under this you must type y. THis is to automatically instert docstrings from modules.
    # Everything else is default. When this is done you must then drop the contents.rst file into the docs folder.
    # then run python3 setup.py build_sphinx on the command line from the same directory.
#    command_options={
#        'build_sphinx': {
#           'project': ('setup.py', name),
#            'version': ('setup.py', version),
#            'release': ('setup.py', release),
#            'source_dir': ('setup.py', 'docs'),
#            'build_dir': ('setup.py', 'docs')}},

    # This is a one-line description or tagline of what your project does. This
    # corresponds to the "Summary" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#summary
    description='An n-body simulator',  # Optional

    # This is an optional longer description of your project that represents
    # the body of text which users will see when they visit PyPI.
    #
    # Often, this is the same as your README, so you can just read it in from
    # that file directly (as we have already done above)
    #
    # This field corresponds to the "Description" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=long_description,  # Optional

    # Denotes that our long_description is in Markdown; valid values are
    # text/plain, text/x-rst, and text/markdown
    #
    # Optional if long_description is written in reStructuredText (rst) but
    # required for plain-text or Markdown; if unspecified, "applications should
    # attempt to render [the long_description] as text/x-rst; charset=UTF-8 and
    # fall back to text/plain if it is not valid rst" (see link below)
    #
    # This field corresponds to the "Description-Content-Type" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
    long_description_content_type='text/markdown',  # Optional (see note above)

    # This should be a valid link to your project's main homepage.
    #
    # This field corresponds to the "Home-Page" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#home-page-optional
    url='https://github.com/nedgar76/neural-body',  # Optional

    # This should be your name or the name of the organization which owns the
    # project.
    author='AstroGators',  # Optional

    # This should be a valid email address corresponding to the author listed
    # above.
    # author_email='author@example.com',  # Optional

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    # packages=find_packages(),  # Required
    packages=['neural_body'],

    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project if the version does not match. See
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires='>=3.8, <4',

    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['pandas==1.1.0', 'numpy<1.18.5, >=1.16.0', 'tensorflow==2.3.0', 'pygame==2.0.0.dev10', 'xlrd', 'h5py', 'pynput'],  # Optional

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={  # Optional
        'neural_body': ['*.csv', '*.png', '*.h5', 'nn/*.h5', 'img/*.png', 'sim_configs/*', 'sim_archives/*'],  # include these files and file extensions in the neural_body package
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    ##################data_files=[('my_data', ['data/data_file'])],  # Optional

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        'console_scripts': [
            'neural_body=neural_body.grav2:main',
        ],
    },
)
