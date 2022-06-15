# Environment
py := python

# Demo
demo_path := ./demo
demo_port := 8080

# Does a test run of the application
run:
	$(py) webmap/crawler.py http://localhost:8080 map.txt

# Start serving the demo server satic files
.PHONY: demo
demo: $(demo_path)
	cd $(demo_path) && \
		$(py) -m http.server $(demo_port)
