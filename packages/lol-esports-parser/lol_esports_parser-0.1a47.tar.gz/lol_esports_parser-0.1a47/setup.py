import setuptools

setuptools.setup(
    name="lol_esports_parser",
    version="0.1a47",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
        "dateparser",
        "lol-id-tools>=1.6.0",
        "riot-transmute>=0.1a12",
        "lol-dto>=0.1a8",
        "riotwatcher",
        "retry",
        "beautifulsoup4",
        "mwclient"
    ],
    url="https://github.com/mrtolkien/lol_esports_parser",
    license="MIT",
    author='Gary "Tolki" Mialaret',
    author_email="gary.mialaret+pypi@gmail.com",
    description="A utility to query and transform LoL games from QQ and ACS into the LolGame DTO format.",
    long_description="See github",
    long_description_content_type="text/markdown",
)
