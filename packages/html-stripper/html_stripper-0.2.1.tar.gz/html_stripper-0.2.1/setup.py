from setuptools import setup

with open("README.md", "r") as readme:
    long_description = readme.read()


def read_requirements(filename="requirements.txt"):
    def valid_line(line):
        line = line.strip()
        return line and not any(line.startswith(p) for p in ("#", "-"))

    def extract_requirement(line):
        egg_eq = "#egg="
        if egg_eq in line:
            _, requirement = line.split(egg_eq, 1)
            return requirement
        return line

    with open(filename) as f:
        lines = f.readlines()
        return list(map(extract_requirement, filter(valid_line, lines)))


setup(
    name="html_stripper",
    use_scm_version=True,
    packages=["html_stripper"],
    setup_requires=["setuptools_scm"],
    description="A simple package to extract text from (even broken/invalid) HTML",
    author="Jiri Helebrant",
    author_email="helb@helb.cz",
    url="https://gitlab.com/helb/html_stripper",
    install_requires=read_requirements(),
    keywords=["html"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6",
    long_description=long_description,
    long_description_content_type="text/markdown"
)
