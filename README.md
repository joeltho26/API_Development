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

Note:

sometimes, there are issues while having 2 projects inside same folder directory with different ```venv/``` environments and trying to install packages eg: ```fastapi[all]``` into the respective environments. To resolve these issues try the command below,

```python -m pip install -r requirements.txt```
