from django import forms

from s3direct.widgets import S3DirectWidget


class PictureForm(forms.Form):
    Adicionar_foto = forms.URLField(widget=S3DirectWidget(
        dest='destination_key_from_settings',
        html=(
            '<div class="s3direct" data-policy-url="{policy_url}">'
            '  <a class="file-link" target="_blank" href="{file_url}">{file_url}</a>'
            '  <a class="file-remove" href="#remove">Trocar</a>'
            '  <input class="file-url" type="hidden" value="{file_url}" id="teste.png" name="name" />'
            '  <input class="file-dest" type="hidden" value="add_picture">'
            '  <input class="file-input" type="file" />'
            '  <div class="progress progress-striped active">'
            '    <div class="bar"></div>'
            '  </div>'
            '</div>'
            '<br>'
        )))
