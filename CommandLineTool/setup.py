from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

long_description = 'Python package for DNSIP dataset downloads and updates'

setup(
		name ='DNS-Command-Line-Tool',
		version ='1.0.0',
		author ='Vinuri Bandara',
		author_email ='vinurib@scorelab.org',
		license ='MIT',
		packages = find_packages(),
		entry_points ={
			'console_scripts': [
				'dnsip = CommandLineTool.script:main'
			]
		},
		classifiers =(
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
		),
		keywords ='DNSIP cmd update',
		install_requires = requirements,
		zip_safe = False
)
