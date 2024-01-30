from setuptools import find_packages,setup

setup(
    name='Job_Recommendation_System',
    version='0.0.1',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')

)
