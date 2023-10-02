from django.core.exceptions import ValidationError


def validate_cpf(value):
    
    cpf = [int(char) for char in value if char.isdigit()]

    if len(cpf) != 11:
        raise ValidationError('O CPF deve ter 11 dígitos')
    
    if cpf == cpf[::-1]:
        raise ValidationError('O CPF não pode ter todos os números iguais')

    for i in range(9, 11):
        value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            raise ValidationError('O CPF é inválido verifique e digite novamente')


def validate_phone(value):

    phone = [int(char) for char in value if char.isdigit()]

    if len(phone) != 9:
        raise ValidationError('O telefone deve ter 9 dígitos')

    if phone == phone[::-1]:
        raise ValidationError('O telefone não pode ter todos os números iguais')


def validate_positive_number(value):
    if value < 0:
        raise ValidationError('O número de aulas não pode ser negativo')