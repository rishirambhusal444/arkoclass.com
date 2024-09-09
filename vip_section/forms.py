# vip_section/forms.py
from django import forms
from .models import OfflinePayment

class OfflinePaymentForm(forms.ModelForm):
    class Meta:
        model = OfflinePayment
        fields = ['subject_id', 'total_amount', 'phone', 'email', 'payment_proof']
        
    # Optionally, you can add custom validation here if needed
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Add custom phone validation logic here if needed
        return phone
