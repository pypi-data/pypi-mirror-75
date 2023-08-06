# coding: utf-8


from setuptools import setup, find_packages  # type: ignore

setup(
    name='arcor2_kinali',
    version_config={
        "template": "{tag}.dev{cc}",
        "starting_version": "0.1.0"
    },
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={"arcor2_kinali": ["py.typed"]},
    url='',
    license='',
    author='Robo@FIT',
    author_email='imaterna@fit.vut.cz',
    description='',
    setup_requires=['another-setuptools-git-version'],
    install_requires=[
        'dataclasses',
        'dataclasses-jsonschema[fast-validation]',
        'arcor2>=0.8.0b3.*',
        'Pillow'
    ],
    zip_safe=False,
)
