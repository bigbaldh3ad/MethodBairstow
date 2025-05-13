# bairstow_app/forms.py
from django import forms

class BairstowForm(forms.Form):
    ecuacion = forms.CharField(label='Ecuación polinómica (ej: x**3 - 6*x**2 + 11*x - 6)', max_length=200)
    r = forms.FloatField(label='Valor inicial r', initial=1.0)
    s = forms.FloatField(label='Valor inicial s', initial=1.0)
    tol = forms.FloatField(label='Tolerancia', initial=0.0001)
    max_iter = forms.IntegerField(label='Máximo de iteraciones', initial=100)
