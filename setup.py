from setuptools import setup, find_packages

version = 'svn/1.7-dev'

setup(name='Products.QuillsEnabled',
      version=version,
      description="A Blogging Product for Plone",
      long_description="""\
QuillsEnabled is an Enterprise Weblog System for the Plone content management system. It is designed from the ground up to work well and provide specialized features for a multi-blog, multi-user environment.""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone blogging',
      author='Quills Team',
      author_email='quills-dev@lists.etria.com',
      url='http://plone.org/products/quills',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
