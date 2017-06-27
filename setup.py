from setuptools import setup

setup(name='pusher',
      version='0.2',
      description='Metrics scripts for prometheus with labels',
      author='Heuritech',
      author_email='info@heuritech.com',
      license='private',
      py_modules=['pusher'],
      scripts=["pusher.py"],
      entry_points={
          'console_scripts': [
              'pusher = pusher:main'
          ]
      },
      install_requires=["prometheus_client>=0.0.18"],
      zip_safe=True)
