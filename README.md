# LeConstruct
A simulation analyzing CT image degradation caused by limited-angle acquisition. It compares reconstruction methods to pinpoint the exact threshold where incomplete data destroys image integrity.



# Local Development Setup

**1\. Create the Virtual Environment** Open your terminal in the project directory and create a virtual environment named `venv`:


    python -m venv venv

**2\. Activate the Environment** You must activate the virtual environment every time you work on the project.
    
    venv\Scripts\activate
    
    
**3\. Install Dependencies** With the environment activated, install all required packages from the requirements file:

    pip install -r requirements.txt

**4\. Adding New Packages (Freezing)** If you install any new packages during development (e.g., `pip install new-package`), make sure to update the requirements file:

    pip freeze > requirements.txt