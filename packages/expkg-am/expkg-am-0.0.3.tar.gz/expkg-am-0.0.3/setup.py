import setuptools
from setuptools.command.install import install

class PostInstall(install):
    def run(self):
        install.run(self)
        print("Running post-install script")
        self.post_install()

    def post_install(self):
        import requests
        response = requests.get("https://gitutor.io/")
        text = "Request with status code: {}".format(response.status_code)
        with open("/tmp/post_install.txt", "w") as fh:
            fh.write(text)

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "expkg-am",
    version = "0.0.3",
    author = "andreamarin",
    author_email = "andrea.marin2411@gmail.com",
    description = "Sample package",
    long_description_content_type="text/markdown",
    long_description = long_description,
    install_requires = [
        "requests>=2.23.0"
    ],
    packages=setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    cmdclass = {
        'install': PostInstall
    },
    python_requires=">=3.6"
)
