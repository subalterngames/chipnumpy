from pathlib import Path
from setuptools import setup, find_packages


setup(
    name='chipnumpy',
    version='1.0.0',
    description='Create simple "chiptune" style audio waveforms using numpy.',
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type='text/markdown',
    url='https://github.com/subalterngames/chipnumpy',
    author_email='subalterngames@gmail.com',
    author='Esther Alter',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords='audio chiptune synthesizer waveform',
    install_requires=['numpy'],
)
