SHELL := /bin/bash
.PHONY: start stop restart clean logs

PID_FILE = .flask_pid

start:
	@echo "Starting Flask server..."
	@/home/krapaud/holbertonschool-porte_folio/venv/bin/python app.py > flask.log 2>&1 &
	@echo $$! > $(PID_FILE)
	@echo "Flask server started with PID $$!"
	@sleep 2
	@bash -c 'if command -v xdg-open >/dev/null 2>&1; then xdg-open http://127.0.0.1:5000; \
	elif command -v gnome-open >/dev/null 2>&1; then gnome-open http://127.0.0.1:5000; \
	elif command -v kde-open >/dev/null 2>&1; then kde-open http://127.0.0.1:5000; \
	elif command -v open >/dev/null 2>&1; then open http://127.0.0.1:5000; \
	elif command -v firefox >/dev/null 2>&1; then firefox http://127.0.0.1:5000 >/dev/null 2>&1 & \
	elif command -v google-chrome >/dev/null 2>&1; then google-chrome http://127.0.0.1:5000 >/dev/null 2>&1 & \
	elif command -v chromium >/dev/null 2>&1; then chromium http://127.0.0.1:5000 >/dev/null 2>&1 & \
	else echo "Impossible d'\''ouvrir automatiquement le navigateur. Ouvrez http://127.0.0.1:5000 manuellement."; fi'

stop:
	@if [ -f $(PID_FILE) ]; then \
		PID=$$(cat $(PID_FILE)); \
		if [[ "$$PID" =~ ^[0-9]+$$ ]]; then \
			if ps -p $$PID > /dev/null; then \
				echo "Stopping Flask server with PID $$PID..."; \
				kill $$PID; \
				rm $(PID_FILE); \
				echo "Flask server stopped."; \
			else \
				echo "PID file found, but process $$PID not running. Cleaning up PID file."; \
				rm $(PID_FILE); \
			fi; \
		else \
			echo "Invalid PID found in $(PID_FILE). Cleaning up PID file."; \
			rm $(PID_FILE); \
		fi; \
	else \
		echo "No Flask server PID file found. Is it running?"; \
	fi

restart:
	$(MAKE) stop
	$(MAKE) start

clean:
	@echo "Cleaning up..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -f $(PID_FILE)
	@echo "Cleanup complete."

logs:
	@tail -n 30 flask.log