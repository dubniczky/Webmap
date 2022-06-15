# Environment
py := python

# Demo
demo_path := ./demo
demo_port := 8080
demo_url := http://localhost:8080

# Does a test run of the application
.PHONY: run
run:
	$(py) webmap/crawler.py $(demo_url) map.txt

# Start serving the demo server satic files
.PHONY: demo
demo: $(demo_path)
	cd $(demo_path) && \
		$(py) -m http.server $(demo_port)

# Cleans repostiry of build files
.PHONY: clean
clean:
	git clean -fdx
