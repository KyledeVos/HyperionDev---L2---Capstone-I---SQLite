# Retrieve alternative Python Interpreter to work with pure python file
FROM pypy:latest
# Dependency - Install 'Tabulate' for book stock console display
RUN  pip install tabulate
# Set Working Directory to current directory - base against which other commands are executed
# relative to
WORKDIR /
# Copy all files in current directory to Docker Image
COPY . /
# Define Default executable for Docker file - start application
CMD python book_stock_management.py