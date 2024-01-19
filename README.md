## Fetch Take Home Assessment

- A Webservices created with Python, Flask/Gunicorn
- The application runs on port 5000
- API endpoints are as described in the probem statement
- Logs generated are saved in logs.log file
- The Receipts data is stored in receipts.json file


## Steps to run the service

- Build the docker container with :

        docker build -t fetch .

- Run the docker container :

        docker run -p 5000:5000 --name fetchimage fetch

- The service will run on localhost:5000
