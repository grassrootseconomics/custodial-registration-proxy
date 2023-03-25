from setuptools import setup

requirements = []
f = open('requirements.txt', 'r')
while True:
    l = f.readline()
    if l == '':
        break
    requirements.append(l.rstrip())
f.close()

setup(
    package_data={
        '': [
            'data/*.abi.json',
            'data/*.bin',
            ],
        },
    include_package_data=True,
    install_requires=requirements,
)
