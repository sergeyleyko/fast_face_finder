# URL Face Finder

To build Docker image:

docker build -t face_finder .

It will take awhile as dlib compiling is a long process.

Then run:

docker run -d --name face_finder -p 80:80 -v images:/app/images face_finder

It will mount the directory myvol2 into /app/ in the container
Faces will be collected into 'images' directory on the docker host machine.