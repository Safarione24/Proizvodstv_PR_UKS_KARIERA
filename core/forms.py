import re
from django import forms
from django.core.exceptions import ValidationError

# Валидатор для имени: только буквы (кириллица и латиница), пробелы и дефис
def validate_name(value):
    if not re.fullmatch(r'[A-Za-zА-Яа-яЁё\s\-]{2,100}', value):
        raise ValidationError(
            'Имя может содержать только буквы (русские и английские), '
            'пробел и дефис, от 2 до 100 символов.'
        )

# Валидатор телефона: российский формат +7XXXXXXXXXX
def validate_phone(value):
    digits = re.sub(r'\D', '', value)  # убираем всё, кроме цифр
    if digits.startswith('8'):
        digits = '7' + digits[1:]
    if not re.fullmatch(r'7\d{10}', digits):
        raise ValidationError('Введите номер в формате +7 XXX XXX-XX-XX.')

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        validators=[validate_name],
        error_messages={'required': 'Пожалуйста, укажите имя.'}
    )
    phone = forms.CharField(
        required=False,          # если телефон не обязателен
        validators=[validate_phone],
        error_messages={'required': 'Укажите телефон.'}
    )
    email = forms.EmailField(
        error_messages={
            'required': 'Укажите email.',
            'invalid': 'Введите корректный email, например name@mail.ru',
        }
    )
    message = forms.CharField(
        min_length=10,           # минимум 10 символов, при желании уберите
        max_length=2000,         # ограничение символов сообщения
        widget=forms.Textarea(attrs={'rows': 5}),
        error_messages={'required': 'Напишите сообщение.'}
    )
