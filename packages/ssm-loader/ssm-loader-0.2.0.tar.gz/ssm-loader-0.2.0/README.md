# SSM
This project aims to help dump and load AWS SSM parameters.


## Usage Example
```bash
# One .json file will be generated in your local with all variables
ssm dump "/app/myapp/app-path"

# All variables described will be inputed inside the IAM configured
ssm load -f ssm.json
```

## Dependencies
- Docker

## Load file format
The file to use the `ssm load` command should be in this format.
```json
{
    "parameters": [
        {
            "Name": "param1",
            "Value": "value1"
        }
    ]
}
```

## Docker

#### Build
Now you are ready to build an image from this project Dockerfile.
```bash
docker build -t ssm .
```

#### Run

After your image has been built successfully, you can run it as a container. In your terminal, run the command docker images to view your images.

```bash
# Dump
docker run -rm \
    -e AWS_REGION='ap-southeast-2' \
    -e AWS_ACCESS_KEY_ID='<your-access-key-id>' \
    -e AWS_SECRET_ACCESS_KEY='<your-secret-access-key>' \
    ssm dump "/app/myapp/app-path"

# Loading
docker run -rm \
    -e AWS_REGION='ap-southeast-2' \
    -e AWS_ACCESS_KEY_ID='<your-access-key-id>' \
    -e AWS_SECRET_ACCESS_KEY='<your-secret-access-key>' \
    ssm load -f ssm.json
```

## Setup development environment

#### Install dependencies

```bash
make build
```

#### Run
```bash
make run
```

#### Test
```bash
make test
```

#### Lint Flake8
```bash
make flake8
```

## Author
App managed by [DNX Solutions](https://github.com/DNXLabs).

## License
Apache 2 Licensed. See [LICENSE](https://github.com/DNXLabs/ssm-loader/blob/master/LICENSE) for full details.