from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.models import BaseOperator
from typing import Dict, List, Any, Optional
import json
import requests

class LoadFileFromAPI(BaseOperator):

    """
    This custom operator will get the data from an API requests
    and load the file into a GCS bucket.
    It will use Airflow's GCSHook rather than the client
    library directly.

    Args:
        bucket_name (str): The name of the bucket to
            load the data.
        prefix (Optional[str]): The prefix for files. Optional, defaults
            to None.
        proxy(str): The proxy to reach public internet. Optional, defaults to None
        token(str): The token for the API. Optional, defaults to None
        url(str): the url for the API.  
        gcp_conn_id (str): The connection ID to use for
            interacting with GCS. Like we mentioned above,
            the connection contains the credentails
            that will be used. The default connection
            ID is usually 'google_cloud_default'.
    
    Resources:
        * GCSHook documentation: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/hooks/gcs/index.html?highlight=gcshook#airflow.providers.google.cloud.hooks.gcs.GCSHook
    """

    def __init__(
        self,
        bucket_name: str,
        prefix: Optional[str] = None,
        proxies: Optional[str] = None,
        token: Optional[str] = None,
        url: str,
        file_name: str,
        mime_type: str,
        gcp_conn_id: str = 'google_cloud_default',
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.bucket_name: str = bucket_name
        self.prefix: Optional[str] = prefix
        self.proxy: Optional[str]= proxy
        self.token: Optional[str] = token
        self.url: str = url
        self.file_name: str = file_name
        self.mime_type: str = mime_type
        self.gcp_conn_id: str = gcp_conn_id
    
    def execute(self, context: Dict[str, Any]) -> None:

        head = {'Authorization': 'token {}'.format(self.token)}
 
        file_from_api = requests.get(
            url = url,
            #proxies = proxies
            #headers = head
        )
        data = file_from_api.content

        file_from_api.raise_for_status()
        self.log.info(f'Response HTTP status code {file_from_api.status_code} ')

        # We instantiate the GCSHook using the connection ID
        # The hook will handle Authentication with GCP
        gcs_hook: GCSHook = GCSHook(gcp_conn_id=self.gcp_conn_id)   

        gcs_hook.upload(
            bucket_name= self.bucket_name,
            object_name= self.file_name,
            mime_type=  self.mime_type,
            data= data
        )

