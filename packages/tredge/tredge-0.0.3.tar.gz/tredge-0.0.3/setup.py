from setuptools import setup

ext_modules = None
with open('README.md', mode='r', encoding='utf8') as f:
    long_description = f.read()

setup(
    name='tredge',
    version='0.0.3',
    description='Python module for finding transitive edges in a directed acyclic graph',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pgolo/tredge',
    author='Pavel Golovatenko-Abramov',
    author_email='p.golovatenko@gmail.com',
    packages=['tredge'],
    ext_modules=ext_modules,
    include_package_data=True,
    license='MIT',
    platforms=['any'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)
