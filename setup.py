from setuptools import setup, find_packages

with open('requirements.txt') as f:
	requirements = f.readlines()

long_description = 'Sample Package made for a demo \
	of its making for the GeeksforGeeks Article.'

setup(
		name ='Linux GNOME Wallpapper change',
		version ='1.0.0',
		author ='Jerky676',
		author_email ='me@jerky676.com',
		url ='https://github.com/Vibhu-Agarwal/vibhu4gfg',
		description ='Demo Package for GfG Article.',
		long_description = long_description,
		long_description_content_type ="text/markdown",
		license ='MIT',
		packages = find_packages(),
		entry_points ={
			'console_scripts': [
				'gfg = vibhu4gfg.gfg:main'
			]
		},
time_filter=month
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
		),
		keywords ='geeksforgeeks gfg article python package vibhu4agarwal',
		install_requires = requirements,
		zip_safe = False
)
