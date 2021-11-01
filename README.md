# Fast Face Finder
Finds faces at an url

## Description

Finds all faces on images at the specified URL.
Based on _FastAPI_ library for serving HTTP endpoint.
It uses _dlib_ library for face detection and alignment. All the detected images are saved to ./images directory, 
with a separate subdirectory for each URL parsed.

Configuration is in the _config.yml_ file. Here you can configure the dlib model binary used for 
face landmarks detection, and the final face image file size.  

## Usage 
To build Docker image:

docker build -t fast_face_finder .

It will take a while as dlib compiling is a long process.

Then run the container:

> mkdir $(pwd)/detected_faces
>
> docker run -d --name fast_face_finder -p 80:80 -v $(pwd)/detected_faces:/app/images fast_face_finder

It will mount the host directory ./detected_faces/ into /app/images/ in the container.
Faces will be collected into 'images' directory on the docker host machine.

The container exposes port 80, you can make _get_ requests to it, the endpoint name is **faces**. 
It accepts **url** query argument with the url to parse for images.

Url has to be encoded, you can use _https://www.urlencoder.org/_ for that.

Example (open in browser):
> http://127.0.0.1/faces?url=abc.com

or with wget
> wget http://127.0.0.1/faces?url=https%3A%2F%2Fwww.bbc.com%2Fnews%2Fworld-59109186
