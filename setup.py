from setuptools import setup

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

reqs = parse_requirements('requirements.txt')

setup(
    name="fluffy_bot",
    version="1.0.0",
    description="robot controller",
    packages=["fluffy_bot"],
    package_data={"fluffy_bot": ["*.json", "*.xml", "*.crt", "emotions/*", "emotions/*/*", "emotions/*/*/*"]},
    install_requires=reqs,
)
