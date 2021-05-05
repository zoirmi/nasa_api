# nasa_api

The nasa_api.py queries Nasa'a api server. Requests can filter string, file size or type. Output can be save to local csv file or to sqlite database. script can run in 2 different modes:

1. Directly on Linux/Windows machine. It accepts the following arguemnts:
  -q/--query_string (Free text search terms to compare to all indexed metadata. default is "Ilan Ramon")
  -m/--media_type (edia types to restrict the search to. Available types: "image", "audio" Separate multiple values with commas.) Default is "image".
  -s/--size (Original image size). Default minimum size is 100kB
  -o/--output (Select output type). Options are csv or db. By default, script will write to CSV.
  
  
2. As docker container. the command <_docker build -t nasa_api ._> will build a minimal image based on the Dockerfile supplied. To make it easier on the end user to query for different strings without building the docker image over and over, the build process will copy entrypoint.sh script to WORKDIR. This script will allow running the Docker image with or without query arguement.
  For example, running the image with the following command -  <_docker run -e QUERY=KSC-02pd1922 --rm nasa_api_> will result in:
  
  ![Screenshot from 2021-05-05 23-54-28](https://user-images.githubusercontent.com/18490872/117208056-5c315480-adfd-11eb-90e6-41c52a6aeec1.png)


Running the docker image without specifying query <_docker run --rm nasa_api_> string will result in:

![Screenshot from 2021-05-06 00-26-53](https://user-images.githubusercontent.com/18490872/117211571-db288c00-ae01-11eb-832a-14f61568d8e6.png)


![Screenshot from 2021-05-06 00-27-17](https://user-images.githubusercontent.com/18490872/117211592-e1b70380-ae01-11eb-8534-9dcb25076a55.png)


![Screenshot from 2021-05-06 00-27-23](https://user-images.githubusercontent.com/18490872/117211607-e8457b00-ae01-11eb-8994-34315644abc0.png)
