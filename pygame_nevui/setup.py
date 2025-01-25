from setuptools import setup, find_packages
setup(
    name='pygame_nevui',  
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'pygame',
        'Pillow',
        'numpy'
    ],
    author='NIKITA', 
    author_email='bebrovgolem@gmail.com',
    description='UI Library for Pygame',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/GolemBebrov/pygame-NevUI',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Games/Entertainment',
    ],
)