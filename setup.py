from setuptools import setup, find_packages


setup(
    name='chipnumpy',
    version='0.0.1',
    description='Create simple "chiptune" style audio waveforms using numpy.',
    long_description='Create simple "chiptune" style audio waveforms using numpy.',
    long_description_content_type='text/markdown',
    url='https://github.com/subalterngames/orbit2d',
    author_email='subalterngames@gmail.com',
    author='Esther Alter',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords='orbit planet star celestial kepler orbital',
    install_requires=['numpy'],
)
