# StoreIT Backend

A serverless file-storage API on AWS. It lets a client upload, download, delete and list files stored in Amazon S3, through API Gateway and AWS Lambda. The infrastructure is defined as code with AWS SAM.

A web frontend for this API is deployed separately and is not part of this repository.

## Architecture

```
Client  ->  API Gateway (REST)  ->  Lambda (Python 3.12)  ->  Amazon S3
```

Each operation is its own Lambda function, and each function only gets access to the one bucket through a scoped SAM policy (`S3CrudPolicy` / `S3ReadPolicy`). CORS is enabled on the API.

## API

| Method | Path | Request body | Response |
|--------|------|--------------|----------|
| POST | `/upload` | `{"file_key": "name.txt", "file_content": "<base64>"}` | Success message |
| POST | `/download` | `{"file_key": "name.txt"}` | File content as base64 |
| POST | `/delete` | `{"file_key": "name.txt"}` | Success message |
| GET | `/list` | none | All files (name, size, last modified) plus storage metrics |

The `/list` response also includes total size, file count, storage in GB, and an approximate monthly storage cost in INR, calculated from a fixed S3 price and a fixed exchange rate.

## Project structure

```
.
├── upload_function/app.py
├── download_function/app.py
├── delete_function/app.py
├── list_function/app.py
├── template.yaml       # SAM template: functions, API routes, policies
└── samconfig.toml      # SAM deploy settings
```

## Deploy

You need an AWS account, the AWS CLI configured with your credentials, the SAM CLI, and Docker.

1. Create an S3 bucket. The template does not create it.
2. In `template.yaml`, replace `my-bucketstorage123` with your bucket name (it appears in each function's policy and environment variables).
3. Build and deploy:

```bash
sam build --use-container
sam deploy --guided
```

The deploy output prints the API Gateway URL for each endpoint.

## Known limitations

- **No authentication on the API.** Every route is set to `Authorizer: NONE`, so anyone with the API URL can list, download and delete files. Adding a Cognito authorizer to the API is the main next step.
- **No per-user separation.** All files share one bucket and `/list` returns everything in it.
- **File size is limited.** Files are sent as base64 inside JSON, which runs into Lambda's request size limit at a few MB. S3 pre-signed URLs would remove this limit.
- **CORS allows all origins** (`*`).
- The bucket name is hardcoded in the template instead of being a parameter.
- No automated tests yet.
