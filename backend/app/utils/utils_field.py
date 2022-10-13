import validate_docbr


class DocumentField(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not isinstance(value, str):
            raise TypeError("string required")

        if len(value) < 11 or len(value) > 18:
            raise TypeError("Invalid Document")

        cpf, cnpj = validate_docbr.CPF(), validate_docbr.CNPJ()
        if not (cpf.validate(value) or cnpj.validate(value)):
            raise TypeError("Invalid Document")

        return "".join(filter(str.isdigit, value))

    def __repr__(self):
        return f"DocumentField({super().__repr__()})"
