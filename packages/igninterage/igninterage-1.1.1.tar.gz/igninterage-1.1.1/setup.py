from setuptools import setup

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
print(long_description)
setup(name='igninterage',
      version='1.1.1',
      description='Modulo para interagir no forum IGNboards+',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/psychodinae/Igninterage',
      author='Psychodinae',
      author_email='noteprof213@gmail.com',
      packages=['igninterage'],
      install_requires=['requests', 'lxml'],
      classifiers=[
          "Programming Language :: Python :: 3.6",
          "Operating System :: Microsoft :: Windows",
          "License :: OSI Approved :: MIT License"
      ],
      python_requires='>=3.6'
      )
