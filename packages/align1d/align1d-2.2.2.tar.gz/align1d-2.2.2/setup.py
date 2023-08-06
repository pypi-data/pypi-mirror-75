from setuptools import setup
from torch.utils.cpp_extension import CppExtension, BuildExtension

setup(
    name='align1d',
    packages=['align1d',],
    license='Apache License',
    version="2.2.2",
    author="Frost Mengmeng Xu",
    author_email="xu.frost@gmail.com",
    description="A small package for 1d aligment in cuda",
    long_description='''
    If you cannot install this package from pip, please go to https://github.com/frostinassiky/gtad to install from source.
    Suggest requirement: torch>=1.6.0, cuda>=10.2,GCC >= 4.9
    
    ''',
    long_description_content_type="text/markdown",
    url="https://github.com/frostinassiky/gtad",
    download_url="https://github.com/frostinassiky/align1d/archive/2.2.1.tar.gz",
    keywords = ['alignment', '1d', 'temporal'],
    classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        
    ],
    ext_modules=[
       CppExtension(
           name = 'Align1D',
           sources = [
             'Align1D_cuda.cpp',
             'Align1D_cuda_kernal.cu',
           ],
           extra_compile_args={'cxx': ['-std=c++14', '-fopenmp'],
             'nvcc': ['--expt-relaxed-constexpr']}
        )
    ],
    cmdclass={
       'build_ext': BuildExtension
    })
