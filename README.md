# Photo Search

Project for "Introduction to Computer Vision" Course at Innopolis University.

A tool to search for a given face on the collection of photos of mass events. 

## Running

Before doing anything, build the service image:

```bash
docker-compose build
```

Running:
```bash
docker-compose up -d
```

Stopping:
```bash
docker-compose down
```

Logs:
```bash
docker-compose logs -f service
docker-compose logs -f postgres
```

Service Links:

- Page to upload files: http://localhost:8000/images
- Page to search by file: http://localhost:8000/search
