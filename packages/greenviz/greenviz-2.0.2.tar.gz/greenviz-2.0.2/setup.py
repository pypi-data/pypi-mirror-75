from setuptools import setup
from distutils.core import setup
setup(
      name="greenviz",
      version="2.0.2",
      description="Greenviz is a package to support students/ users, who face difficulty in comprehending machine learning and data analytics algorithms. Greenviz uses the python programming constructs to run various learning algorithms. Hence users can understand working of various learning algorithms practically and visually.",
      author="R.raja subramanian",
      url="https://github.com/RRajaSubramanian/Greenviz",
      author_email="rajasubramanian.r1@gmail.com",
      py_modules=["greenviz"],
      package_dir={"":"src"},
      data_files=[("",["shiridi pic rezied.jpeg","bg5.jpg","raja12.jpeg","resized achuth pic.jpeg"])],
      include_package_data=True,
      install_requires=["pillow","matplotlib","sklearn","pydotplus","seaborn","dnspython","pandas","pymongo","numpy","IPython","graphviz"]
      )

