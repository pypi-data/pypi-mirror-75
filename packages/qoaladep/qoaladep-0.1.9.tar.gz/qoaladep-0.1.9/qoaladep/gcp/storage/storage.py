from google.cloud import storage
import numpy as np 
import cv2 
import base64


def download_from_storage(bucket_name, source_blob_name, destination_file_name):
    """[Function to download object from google cloud storage to local]
    
    Arguments:
        bucket_name {[string]} -- [Name of bucket in google cloud storage]
        source_blob_name {[string]} -- [Path to object in google cloud storage]
        destination_file_name {[string]} -- [Name and Path object in local]
    
    Returns:
        object  -- [Downloaded object from storage]
    """    
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)


def upload_to_storage(bucket_name, file_bytes, destination_blob_name, content_type):
    """[Function to upload object from local to google cloud storage]
    
    Arguments:
        bucket_name {[string]} -- [Name of bucket in google cloud storage]
        file_bytes {[bytes]} -- [Bytes of object that want to upload to google cloud storage]
        destination_blob_name {[string]} -- [Name and Path object in google cloud storage]
        content_type {[string]} -- [Type of data to save object in google cloud storage]
    """    
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(file_bytes, content_type=content_type)


def read_image_gcs_b64(bucket, image_file): 
    """[summary]

    Args:
        bucket ([type]): [description]
        image_file ([type]): [description]

    Returns:
        [type]: [description]
    """    
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket)
    blob = bucket.blob(image_file)

    blob_array = np.asarray(bytearray(blob.download_as_string()), 
                                dtype=np.uint8)
    img_np = cv2.imdecode(blob_array, cv2.IMREAD_COLOR)
    if img_np is None: 
        img_np = cv2.imdecode(blob_array, cv2.IMREAD_UNCHANGED)
    img_jpg = cv2.imencode('.jpeg', img_np)[1]
    image_b64 = base64.b64encode(img_jpg).decode('utf-8')
    return image_b64
