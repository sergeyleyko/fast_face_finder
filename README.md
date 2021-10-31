# URL Face Finder

To build Docker image:

docker build -t face_finder .

It will take a while as dlib compiling is a long process.

Then run the container:

docker run -d --name face_finder -p 80:80 -v detected_faces:/app/images face_finder

It will mount the directory images into /app/ in the container
Faces will be collected into 'images' directory on the docker host machine.

The container exposes port 80, you can make _get_ requests to it, the endpoint name is **faces**. 
It accepts **url** query argument with the url to parse for images.

Url has to be encoded, you can use _https://www.urlencoder.org/_ for that.
Example:

http://127.0.0.1/faces?url=https%3A%2F%2Fwww.bbc.com%2Fnews%2Fworld-59109186

