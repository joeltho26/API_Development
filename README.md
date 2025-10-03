# API_Development

1. Create a virtual environment:

    ```python -m venv venv```

2. Install fastapi:

   ```pip install fastapi[all]```

3. Select the environment's python interpreter:
    - Inside VS code -> go to view options in toolbar -> select python interpreter
        - provide the url:
            - eg: ```.\venv\Scripts\python.exe``` or manually choose the file

4. Activate the environment using the command below:
    
    ```.\venv\Scripts\activate```

- To run the app:

    ```uvicorn app.main:app --reload```

======================================================

Note:

- sometimes, there are issues while having 2 projects inside same folder directory with different ```venv/``` environments and trying to install packages eg: ```fastapi[all]``` into the respective environments. To resolve these issues try the command below,

    ```python -m pip install -r requirements.txt```

- To change the port of server:

    ```uvicorn app.main:app --reload --port 8001```

- Schema/Pydantic Model defines the structure of the request/response.
- SQLModel defines the structure of the table in the database created (eg: postgres)

- To check the libraries installed:

    ```pip freeze```

- We have authorization tab in postman to perform authentication operation to the resepctive APIs
    1. Select ```Bearer Token``` option
    2. Enter the generated token during login into the token field

- Instead of hardcoding the url (http://127.0.0.1:8000/) in the post API URL section, we can create environments which consists of the URL variable and its value (which is the port)
    1. create environment in postman
    2. create a variable called ```URL``` and set its value (eg: ```http://127.0.0.1:8000/```)
    3. now to use the environment variable in the URL of the API eg: ```{{URL}}posts```, ```{{URL}}login```, ```{{URL}}users```, etc

- to make the process simpler of copying the JWT token into each API manually, we can set an environment variable under the test option under each api.
    1. eg: ```pm.environment.set("JWT", pm.response.json().access_token);```
    2. now, go to the authorization tab and set the token as ```{{JWT}}```

Under Postgres Foreign Keys Implementation in Postgres Admin tool:
- while adding foreign keys, we have option to ```CASCADE``` 
- CASCADE will enable that if an user is deleted then the posts associated with it also is deleted

