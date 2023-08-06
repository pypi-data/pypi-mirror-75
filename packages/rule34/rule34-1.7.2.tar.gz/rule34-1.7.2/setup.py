from setuptools import setup, find_packages

setup(
    name='rule34',
    version="1.7.2",
    description='An async API wrapper for rule34.xxx',
    long_description= 'An async API wrapper for rule34.xxx using aiohttp',
    long_description_content_type='text/markdown',
    url='https://github.com/LordOfPolls/Rule34-API-Wrapper',
    author='LordOfPolls',
    author_email='ddavidallen13@gmail.com',
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.

        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'],
    keywords='rule34, porn, api, wrapper',
    project_urls={'Source': 'https://github.com/LordOfPolls/Rule34-API-Wrapper'},
    packages=find_packages(include=['rule34']),
    install_requires=['asyncio', 'aiohttp'],
    python_requires='>=3.5',
    py_modules=["rule34"]
)
