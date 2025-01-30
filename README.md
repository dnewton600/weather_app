### Reproducing this example:
* I used Python version 3.12.0 to complete the assignment. The code should work with Python versions 3.12.0 or greater (and likely earlier versions), but the exact version can be used to ensure compatibility.
* To reproduce this example, create a new virtual environment using
  
```python -m venv /path/to/venv```

* Next, download the source code, and navigate to the project directory.
* Activate the virtual environment with
  
```source /path/to/venv/Scripts activate```

(this may depend on your OS; I used Git bash on Windows, your setup may be different)
* To setup the virtual environment, run $pip install -r requirements.txt
* Then, you should be able to run the required functions, for example:
  
```python historical_weather.py days-of-precip bos```

```python historical_weather.py chance-of-precip bos 1 30```

### Notes from the assignment:
 - I will assume that an "nan" value for SNOW implies 0 snowfall.
 - I did not implement detailed input checking/sanitization of user inputs (though I implemented some); I will assume the inputs are valid
 - I explored a few models for predicting the chance of rainfall given this was a short task, but I could imagine exploring additional approaches.
 - The code fits/trains a model each time the historical_weather.py function is run. In practice, I would typically opt to save the trained model and only load it for predictions. 
 - I used library documentation to complete the assignment, but I did not use any code generation AI tools.
 - To ensure an even higher chance of the code running cross-platform, I could have wrapped this application in a Docker container, but I wasn't sure if that was overkill for the assignment, and this would also require the reviewer to have Docker installed on their computer.
