from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from utility.useful import encryption
from django.conf import settings

def reSizeImage(input_image, output_size,id):
    # Open the input image using PIL
    image = Image.open(input_image)
    
    # Transpose the image based on its EXIF information
    image = ImageOps.exif_transpose(image)
    
    # Create a thumbnail with the specified output size
    image.thumbnail(output_size)
    
    # Create a BytesIO object to store the resized image
    image_io = BytesIO()
    
    # Determine the image format from the input image's format

    image_format = input_image.name.split('.')[-1].upper() 
    
    print(image_format)
    # Save the image to the BytesIO object with the determined format
    image.save(image_io, format=image_format)
    
    # Return the resized image as an InMemoryUploadedFile


    # rename image
    encypt = encryption(settings.SECRET_KEY)
    name = encypt.encrypt_string(str(id))
    resized_image = InMemoryUploadedFile(
        image_io,
        None,
        f'{name}.{image_format.lower()}',
        f'image/{image_format.lower()}',
        image_io.tell(),
        None
    )
    
    return resized_image