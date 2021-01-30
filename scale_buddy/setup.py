from setuptools import setup

setup(name="scale_buddy",
      version="0.1",
      scripts=["bin/scale_buddy"],
      description="Scale buddy, scale buddy, more than meets the eye!",
      url="http://github.com/btoll/music_buddy/scale_buddy",
      author="btoll",
      author_email="benjam72@yahoo.com",
      license="GPLv3+",
      packages=["scale_buddy"],
      include_package_data=True,
      classifiers=[
          # https://pypi.org/pypi?%3Aaction=list_classifiers
          "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.7",
      ],
      zip_safe=False)

