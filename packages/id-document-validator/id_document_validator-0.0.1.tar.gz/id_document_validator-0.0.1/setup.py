import setuptools

setuptools.setup(
    name = "id_document_validator",
    version = "0.0.1",
    author = "Erick M. Fana (roy-mustang)",
    author_email = "efanaportes@gmail.com", 
    description = """A simple Identity Document Characters Validator (just for DNI and cedula identity documents)
    you use it as follows: from validator.validato import Validator. Then, you call the is_valid method:
    Validato.is_valid(document_name, document_numeration), this must return or True or False""",
    url = "https://github.com/greatBrain/id_document_validator", 
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    python_requires='>=3.7',
)
