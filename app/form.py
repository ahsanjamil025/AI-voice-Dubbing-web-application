from django import forms
from .models import Audio_upload,Ai_bot

#DataFlair #File_Upload
class Audio_upload(forms.ModelForm):

    class Meta:
        model = Audio_upload
        fields = [
        'Upload_Audio'
        ]

class Ai_bot(forms.ModelForm):
    class Meta:
        model = Ai_bot
        fields = "__all__"
        labels = {"text": "Type Text Here", "Bot_Sound": "Upload Sample Audio"}