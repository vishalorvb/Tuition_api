from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from .useful import GenerateString

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
    image_format = "png"
    
    # Save the image to the BytesIO object with the determined format
    image.save(image_io, format=image_format)
    
    # Return the resized image as an InMemoryUploadedFile


    # rename image
    name = GenerateString(str(id)).encode()
    resized_image = InMemoryUploadedFile(
        image_io,
        None,
        f'{name}.{image_format.lower()}',
        f'image/{image_format.lower()}',
        image_io.tell(),
        None
    )
    
    return resized_image