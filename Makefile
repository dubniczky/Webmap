# Environment detection
# "python" command on windows, "python3" on others
py := python3
ifeq ($(OS),Windows_NT)
	py := python
endif

# Demo
demo_path := ./demo
demo_port := 8080
demo_url := http://localhost:8080

# Does a test run of the application
.PHONY: run
run:
	$(py) webmap/main.py map $(demo_url)

# Run pylint on the application
.PHONY: lint
lint:
	$(py) -m pylint webmap/*

# Start serving the demo server satic files
demo::
	@cd $(demo_path) && \
		$(py) -m http.server $(demo_port)

# Cleans repostiry of build files
.PHONY: clean
clean:
	git clean -fdx
