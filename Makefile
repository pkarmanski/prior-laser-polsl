build:
	docker build -t prior-laser-polsl .


up:
	docker-compose up

run:
	docker run -it --rm \
    -e DISPLAY=host.docker.internal:0 \
    --name prior-laser-polsl prior-laser-polsl
