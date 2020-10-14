from django.shortcuts import render


from fdfs_client.client import Fdfs_client
client=Fdfs_client('utils/fastdfs/client.conf')

client.upload_by_filename('/home/ubuntu/Desktop/01.jpg')

