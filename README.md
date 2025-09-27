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

To run the app:

```uvicorn app.main:app --reload```
