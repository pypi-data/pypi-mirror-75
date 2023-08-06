import setuptools
import pathlib

HERE = pathlib.Path(__file__).parent
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "PyHand_Earth",
    version = "1.0.2",
    description = "Google Earth navigation driven by gesture recognition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/liujohnj/PyHand_Earth",
    classifiers = [
        "Programming Language :: Python :: 3",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
   'opencv-python==4.2.0.34',
    'matplotlib==3.2.2',
    'tensorflow==2.2.0',
    'Keras==2.4.2',
    'pyautogui==0.9.50',
    'PyQt5',
    'psutil==5.7.0	',
],
    entry_points={
        "console_scripts": ["PyHand-Earth=PyHand_Earth.main_qt:main"]
    }
    
    

)
