from distutils.core import setup

with open("README.md", "r") as fh:
  long_description = fh.read()

version = '0.6.2'
  
setup(
  name = 'pyfie',
  packages = ['pyfie'],
  version = version,
  license='MIT',
  description = 'pyfie is a simple Python script, that you can use to encrypt and decrypt files.',
  long_description = long_description,
  author = 'Kazafka',
  author_email = 'caffiqu@gmail.com',
  url = 'https://github.com/Kafajku/pyfie',
  download_url = 'https://github.com/Kafajku/PyFiE/archive/v_{}.tar.gz'.format(version),
  keywords = ['PyFiE', 'Python', 'File', 'Encrypter', 'Encryption', 'pyfie', 'python', 'file', 'encrypter', 'encryption'],
  classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8'
  ]
)
