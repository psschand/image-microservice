# Image Microservice
A set of microservices to store, host and manipulate image files using a rest api

## Architecture
Services:
1. image-storage - Stores uploaded images and serves them back to the consumer
2. image-storage-db - A postgres container to store image metadata
3. image-transform - Takes a uploaded image, url or image_id for above service and transforms the iamge according to the passed parameters
4. nginx - An API layer which fronts all other microservices

Each service is contained within it's own docker container and can be built with the Dockerfiles. The full service can be builts and run with the docker-compose.yml file.

## Usage
### Image Storage/Retrieval
- POST: /image with a form data key = 'Image' and Value as the file -  will return a json response with the image_id
- GET: /image/{image_id} -  will return the image in orginal format
- GET: /image/{image_id}.ext -  will return the image converted into the file format defined by ext

### Image Transformation
- POST: /transform?query_string with form data key = 'Image' and Value as a file - will return a tranformed file according to the query string.

Query String can contain a chained set of transformation from the following list:
- rotate={degrees}
- thumb={height_and_width}
- blur={radius_pixels}
- compress={0-100 where 100 is maximum quality}

And example is ```/trasnform?rotate=90&blur=10```


## Development
1. Install Docker and docker-compose
2. Run ```docker-compose up``` which will build the docker images and run them
3. If the code for the two python microservices changes the service will reload

## Deployment
To start the microservices with a production web server (gunicorn) change the FLASK_ENV to 'prod' in the docker-compose file


## To Improve
- Investigate if some image type converstions or transformations are common enough to justify pre-computing
- Decide if we need user access managment or are all images open to anyone?
- Add API versioning to endpoints using nginx
- Add varnish cache in front of the API to improve the image transforming service if the same request is made multiple times