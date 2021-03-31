import os

from google.cloud import storage
import datetime
import google.auth

def generate_signed_url(bucket, blob_object):
    credentials, project_id = google.auth.default()

    # Perform a refresh request to get the access token of the current credentials (Else, it's None)
    from google.auth.transport import requests
    r = requests.Request()
    if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
        credentials.refresh(r)

    client = storage.Client()
    bucket = client.get_bucket(bucket)
    blob = bucket.get_blob(blob_object)
    if blob is None:
        return None
    expires = datetime.datetime.now() + datetime.timedelta(seconds=86400)

    if hasattr(credentials, "service_account_email"):
        service_account_email = credentials.service_account_email
    service_account_email = 'dailybrieftw@dailybrieftw-302512.iam.gserviceaccount.com'
    url = blob.generate_signed_url(expiration=expires,service_account_email=service_account_email, access_token=credentials.token)
    return url