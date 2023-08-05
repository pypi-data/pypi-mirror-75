
from setuptools import setup, find_packages 

long_description = 'Package for traindex-cli to upload large datasets to S3.' 
  
setup( 
        name ='traindexcli', 
	version ='0.0.4', 
        author ='Mohsin Ashraf', 
        author_email ='mohsin@foretheta.com', 
        description ='Demo Package for traindex-cli.', 
        long_description = long_description, 
        license ='MIT', 
	url ='https://www.traindex.io/',
	download_url ='https://github.com/foretheta/traindex-cli/archive/v0.0.4.tar.gz', 
        packages = find_packages(), 
        entry_points ={ 
            'console_scripts': [ 
                'traindex_cli = src.traindex_cli:main'
            ]
        }, 
        classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ], 
        keywords =['traindex-cli','traindex_cli','traindex'], 
        install_requires = [
		"boto3==1.10.19"	
	], 
        zip_safe = False
) 

