from setuptools import setup

project_urls = {
    'github':'https://github.com/trisdav/htmlxword/tree/main'
}

setup(include_package_data = True,
      description="Create Static HTML/Js Crosswords",
      long_description=open("README.md").read(),
      long_description_content_type='text/markdown',
      project_urls = project_urls,
      )