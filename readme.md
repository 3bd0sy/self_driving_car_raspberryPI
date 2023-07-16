# SELF DRIVING CAR USING RASPBERRY PI
This is a short introduction to my  project.
![logo](data/logo.jpg?raw=true "Tlogo")



### Features :
- a website where you can control the car
- you can use manual mode to control the car by the joystick   
- you can use AI mode to let the car drive itself 
- edge tracking algorithm
- tensorflow lite model

### car parts :
- arduino car 4WD
- rasbperry pi 4
- camera pi
- google coral (i didnt use it , but you need it)  


### note :
- you need to change the lower and upper color in the AIdrive/edgeDetectionModule.py
- you need to change the PATH_TO_CKPT and PATH_TO_LABELS in the AIdrive/tfliteDetection.py
- 

To install this project, you need to have Python 3 and some dependencies. You can use pip to install them:
```python 
pip install -r requirements.txt
```

Then, you can run the main script:

```python 
python app.py
```


Usage
To use this project, you need to provide some input data in the data folder. The data should be in CSV format with the following columns:

Column 1: This is what it means
Column 2: This is what it means
Column 3: This is what it means
The output will be saved in the output folder as a JSON file with some results.

License
This project is licensed under the MIT License. See the LICENSE file for more details.


## License

MIT

**Free Software, Hell Yeah!**


