from useful import encryption


token = "django-insecure-ct4r=zj1svv8=!#8y((jo8wd*ihgpwz9@x-4!%3l))j6w)=nb&"
encrypt = encryption(token)


encode= encrypt.decrypt_string("gAAAAABkt-5jogQscqn_I4_VrQGNh0RRaqVEfpoj5TsJHbgTEiYaYCoksdp875uAIH2i16geHD3czJUxg3CyNI3MQfj1aRW0Rw==")
print(encode)



