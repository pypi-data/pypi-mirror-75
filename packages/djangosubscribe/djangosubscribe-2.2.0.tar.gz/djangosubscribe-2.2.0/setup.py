from setuptools import setup


def readme():
	with open('README.md') as f:
		return f.read()


setup(
	name="djangosubscribe",
	version="2.2.0",
	license="MIT",
	description="Djangosubsribe: Django Reusable app for Email Subscription.",
	long_description=readme(),
	long_description_content_type="text/markdown",
	url="https://github.com/bhojrampawar/djangosubscribe",
	author="Bhojram pawar",
	author_email="bhojrampawar@hotmail.com",
	packages=["djangosubscribe"],
	include_package_data=True,
	classifiers=[
		'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
	],
	install_requires=['django', 'djangoadmin', 'djangotools']
)