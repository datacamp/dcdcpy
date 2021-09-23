"""Import data connector data from Amazon S3."""

from os import environ
from boto3.session import Session
from awswrangler.s3 import read_csv
from datetime import date
from . import internal

def create_s3_session(
        aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"],
        region_name=environ["AWS_DEFAULT_REGION"]):
    """
    Create an Amazon Amazon Simple Storage Service Session (where DataCamp
    Data Connector data is hosted.)
    
    Parameters
    ----------
    aws_access_key_id :
         (Default value = os.environ["AWS_ACCESS_KEY_ID"])
         String containing the S3 access key.
    aws_secret_access_key :
         (Default value = os.environ["AWS_SECRET_ACCESS_KEY"])
         String containing the S3 secret access key.
    region_name :
         (Default value = os.environ["AWS_DEFAULT_REGION"])
         String containing the S3 default region.
         
    Find the arguments to this function in the Admin Portal for
    your DataCamp group. See Reporting -> Export -> Data Connector -> View
    Configuration Details. It is recommended to store these values as  
    environment variables.
    
    Returns
    -------
    A boto3 session object. See
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html
    """
    return Session(                         # boto3.session.Session
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name)

"""
Available datasets.
"""
DC_DATASETS = ['assessment_dim',
 'chapter_dim',
 'course_dim',
 'exercise_dim',
 'learning_assessment_fact',
 'learning_chapter_fact',
 'learning_course_fact',
 'learning_exercise_fact',
 'learning_practice_fact',
 'learning_project_fact',
 'practice_dim',
 'project_dim',
 'team_dim',
 'user_dim',
 'user_team_bridge']

def get_dc_datasets(s3_sess, datasets=DC_DATASETS, date="latest",
                    bucket=environ["AWS_S3_BUCKET_NAME"]):
    """
    Gets DataCamp Data Connector datasets from S3.
    
    Parameters
    ----------
    s3_sess :
        An S3 session, as returned by create_s3_session().
    datasets :
         (Default value = DC_DATASETS)
         Names of the datasets to import.
    date :
         (Default value = "latest")
         A Date or string in "%Y-%m-%d" format denoting the date at 
         which to retrieve data for. Use "latest" to get the most recent data.
    bucket :
         (Default value = os.environ["AWS_S3_BUCKET_NAME"])
         A string containing the DataCamp Data Connector bucket name.

    Returns
    -------
    A dictionary of pandas DataFrames. The keys are the datasets argument; the
    values are the corresponding Data Connector datasets.
    """
    assert set(datasets).issubset(DC_DATASETS), \
        "Only datasets in DC_DATASETS are available."
    if date != "latest":
        if type(today) == datetime.date:
            date = date.strftime("%Y-%m-%d")
        else:
            assert is_yyyymmdd(date)
    
    def read_dataset(dataset):
        """
        Read a CSV file from S3
        
        Parameters
        ----------
        dataset :
           A string naming the dataset 

        Returns
        -------
        A pandas DataFrame.
        """
        filename = f"s3://{bucket}/{date}/{dataset}.csv"
        return read_csv(filename) #  wr.s3.read_csv()
    
    dataframes = [read_dataset(dataset) for dataset in datasets]
    return dict(zip(datasets, dataframes))