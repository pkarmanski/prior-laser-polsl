# Ustawienia
IMAGE_NAME = prior-laser-polsl
CONTAINER_NAME = prior-laser-polsl
DISPLAY_PORT = 6000

.PHONY: build run stop clean

build:
	docker build -t $(IMAGE_NAME) .

socat:
	@echo "Running socat on port $(DISPLAY_PORT)..."
	@socat TCP-LISTEN:$(DISPLAY_PORT),reuseaddr,fork UNIX-CLIENT:/tmp/.X11-unix/X0 &

run: socat
	@echo "Running Docker container..."
	docker run -it --rm \
	    -e DISPLAY=host.docker.internal:$(DISPLAY_PORT) \
	    --name $(CONTAINER_NAME) \
	    $(IMAGE_NAME)

stop:
	@echo "Stopping socat..."
	@pkill -f 'socat TCP-LISTEN:$(DISPLAY_PORT)'

clean: stop
	@echo "Cleaning images and containers..."
	docker rmi -f $(IMAGE_NAME) || true
	docker container prune -f
