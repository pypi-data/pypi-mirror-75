if __name__ == '__main__':
    from setuptools import find_packages, setup
    from pathlib import Path

    project = 'xu'
    parent = Path(__file__).parent.resolve()
    readme = (parent / 'README.md').read_text()

    setup(
        name=project,
        version='0.0.2',
        description='Random utils',
        long_description=readme,
        long_description_content_type='text/markdown',
        url='https://github.com/onerbs/' + project,
        author='AAAA',
        author_email='dev@onerbs.com',
        license='MIT',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
        keywords='random generator',
        package_dir={'': 'src'},
        py_modules=[project],
    )
