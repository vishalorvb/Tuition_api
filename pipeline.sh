docker run -d \
    -p 8000:8000 \
    -e SECRET_KEY='django-insecure-ct4r=zj1svv8=!#8y((jo8wd*ihgpwz9@x-4!%3l))j6w)=nb&' \
    -e DB_NAME=Tuition \
    -e DB_USER=admin \
    -e DB_PASSWORD=Vb&third04 \
    -e DB_HOST=hometuition.cnk2zaoorljp.us-east-1.rds.amazonaws.com \
    -e DB_PORT=3306 \
    -e EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend \
    -e EMAIL_HOST=smtp.gmail.com \
    -e EMAIL_PORT=587 \
    -e EMAIL_USE_TLS=True \
    -e EMAIL_HOST_USER=v.kumar70760@gmail.com \
    -e EMAIL_HOST_PASSWORD=Vb&third1 \
    -e API_KEY=5ddefe3a-b029-11ec-a4c2-0200cd936042 \
    -e RAZOR_KEY_ID=rzp_test_QvSukHJCQx98aF \
    -e RAZOR_KEY_SECRET=C32zIZ9XCiHE0DYdGLC6lUI9 \
    -e AWS_ACCESS_KEY_ID=AKIA4TJE6XEGXIDOXN2D \
    -e AWS_SECRET_ACCESS_KEY=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 \
    -e AWS_STORAGE_BUCKET_NAME=vishal-homet \
    -e AWS_DEFAULT_FILE_STORAGE=storages.backends.s3boto3.S3Boto3Storage \
    --name my-django-container \
    app