from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat

def validate_image_file_size(instance):
    """Prevents image files too large from being uploaded."""
    file_size = instance.file.size
    max_file_image_size = 5242880 # A little over 5 MB

    if file_size > max_file_image_size:
        raise ValidationError(_(f'Image size too large. Tried to upload on image of size {filesizeformat(file_size)}'
                                 f'Please upload an image of {filesizeformat(max_file_image_size)} or less.'))

