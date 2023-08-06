import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rl_tools",
    version="0.0.1",
    author="Gong Xiaoyu",
    author_email="gxywy@hotmail.com",
    description="A general toolset for reinforcement learning (RL)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gxywy/rl-tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)