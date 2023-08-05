from distutils.core import setup


setup(
  name = 'delete_folder_jupyter',   
  packages = ['delete_folder_jupyter'],  
  version = '0.0.3',      
  license='MIT',      
  description = 'delete non-empty folder from jupyter and jupyter-lab',
  author = 'Roni Gold',                  
  author_email = 'ronigoldsmid@gmail.com', 
  url = 'https://github.com/ronigold',
  download_url = 'https://github.com/ronigold/delete_folder_jupyter/archive/0.0.3.tar.gz',   
  keywords = ['jupyter', 'jupyter-lab', 'delete non-empty folder'],  
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers', 
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)