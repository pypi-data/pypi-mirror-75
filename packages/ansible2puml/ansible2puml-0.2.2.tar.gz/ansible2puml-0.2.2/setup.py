from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(name='ansible2puml',
      version='0.2.2',
      description='Create an PlantUML Activity Diagram from Playbooks or Roles trough Python.',
      #   url='http://ictshore.com/',
      author='profileid',
      author_email='profileid@protonmail.com',
      url="https://github.com/ProfileID/ansible2puml",
      license='MIT',
      packages=['ansible2puml'],
      install_requires=required,
      entry_points={
          "console_scripts": ["ansible2puml = ansible2puml.cli:main"]
      },
      classifiers=[
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8'
      ]
      )
