from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

long_description = 'Python package for DNSIP dataset downloads and updates'

setup(
		name ='DNSIP_commandLine_tool',
        version ='1.0.0',
		author ='Vinuri Bandara',
		# author_email ='vibhu4agarwal@gmail.com',
		# url ='https://github.com/Vibhu-Agarwal/vibhu4gfg',
		# description ='Demo Package for GfG Article.',
		# long_description = long_description,
		# long_description_content_type ="text/markdown",
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
