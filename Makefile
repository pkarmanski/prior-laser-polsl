# Ustawienia
IMAGE_NAME = prior-laser-polsl
CONTAINER_NAME = my_running_app
DISPLAY_PORT = 6000

.PHONY: build run stop clean socat

# Buduje obraz Docker
build:
	docker build -t $(IMAGE_NAME) .

# Uruchamia socat w osobnym kontenerze
socat:
	@echo "Uruchamianie socat w osobnym kontenerze na porcie $(DISPLAY_PORT)..."
	docker run -d --rm \
	    --name socat \
	    -p $(DISPLAY_PORT):$(DISPLAY_PORT) \
	    alpine/socat \
	    TCP-LISTEN:$(DISPLAY_PORT),reuseaddr,fork UNIX-CLIENT:/tmp/.X11-unix/X0

# Uruchamia kontener Docker
run: socat
	@echo "Uruchamianie kontenera Docker..."
	docker run -it --rm \
	    -e DISPLAY=host.docker.internal:$(DISPLAY_PORT) \
	    --name $(CONTAINER_NAME) \
	    $(IMAGE_NAME)

# Zatrzymuje socat
stop:
	@echo "Zatrzymywanie socat..."
	docker stop socat || true

# Czyści zbudowane obrazy i kontenery
clean: stop
	@echo "Czyszczenie zbudowanych obrazów i kontenerów..."
	docker rmi -f $(IMAGE_NAME) || true
	docker container prune -f
