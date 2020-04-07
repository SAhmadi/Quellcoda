# Serverless Testing App  
>**Execute and test simple Java programs in an isolated environment.**

## Requirements  
1. Python 3.7
2. Flask 1.1.1
3. Google Cloud Platform Account (*to run Cloud Run & Container Registry*)

## Build
**[Google Cloud SDK](https://cloud.google.com/sdk/install?hl=de) & Project**

1. Create a Google Cloud Project and install `gcloud` (Google Cloud SDK)
2. Authorize gcloud: `gcloud auth login`
3. Configure gcp-project: `gcloud config set project [PROJECT_ID]`
4. Enable services: <br>
`gcloud services enable containerregistry.googleapis.com cloudbuild.googleapis.com run.googleapis.com`
5. Install beta components: `gcloud components install beta`
6. Update components: `gcloud components update`

**Push to [Google Container Registry](https://cloud.google.com/container-registry?hl=de) and [Google Cloud Run](https://cloud.google.com/run?hl=de)** <br>
Navigate to the `cloudbuild.yml` file inside the project: `cd ~/path/to/ba-ahmadi-code`
1. Run `gcloud builds submit`
