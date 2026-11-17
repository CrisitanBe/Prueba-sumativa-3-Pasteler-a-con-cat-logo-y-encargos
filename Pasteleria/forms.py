from datetime import date
from django import forms
from .models import Encargo

class EncargoForm(forms.ModelForm):
    class Meta:
        model = Encargo
        fields = ['nombre', 'email', 'fecha_retiro', 'cantidad']
        widgets = {'fecha_retiro': forms.DateInput(attrs={'type': 'date'}),
                   }

        def clean_cantidad(self):
            cantidad = self.cleaned_data['cantidad']
            if cantidad < 1 or cantidad > 3:raise forms.ValidationError('La cantidad debe estar entre 1 y 3.')
            return cantidad

        def clean_fecha_retiro(self):
            fecha = self.cleaned_data['fecha_retiro']
            if fecha < date.today():raise forms.ValidationError('La fecha de retiro no puede ser anterior a hoy.')
            return fecha