from setuptools import setup, Extension

module = Extension('virxrlcu', sources=['./virxrlcu.c'])

setup(name='VirxERLU CLib',
      version='1.0',
      description='C modules for VirxERLU',
      ext_modules=[module],
      license="Unlicense",
      author='VirxEC',
      author_email='virx@virxcase.dev',
      url="https://github.com/VirxEC/VirxERLU"  
      )
