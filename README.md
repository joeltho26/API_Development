# API_Development

1. Create a virtual environment

    ```python -m venv venv```

2. Select the environment python interpreter
    - Inside VS code -> go to view options in toolbar -> select python interpreter
        - provide the url
            - eg: ```.\venv\Scripts\python.exe``` or manually choose the file

3. Activate the environment using below command
    
    ```.\venv\Scripts\activate```

To Run the app:

```uvicorn app.main:app --reload```
