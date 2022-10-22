### Assignment 4

1. Pulling image of hello-world.
[1.mp4](1.mp4)

2. Dockerfile for JobPortal application.

```dockerfile
FROM jobportal:latest
WORKDIR ~/Desktop/
ADD . jobportal/
WORKDIR ~/Desktop/jobportal
RUN pip install -r requirements
RUN chmod +x app.sh
CMD ["/bin/sh","app.sh"]
```

3. Created an IBM container registry and deployed hello-world image in it.
[3.mp4](3.mp4)

4. Created a Kubernetes cluster and exposed it using NodePort.
[4.mp4](4.mp4)