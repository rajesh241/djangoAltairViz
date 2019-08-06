# Django Altair Visualization

This is example design for creating interactive web plots using Django and Altair. There is a interactive example plot of Cricket Records using Django and Altair.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

You need python3 and virtualenvironment installed on your system. 

### Installing

A step by step instruction on getting the project working on your system. 

Go to directory of your choice and clone the git repository.

```
cd <directory of your choice>
git clone https://github.com/rajesh241/djangoAltairViz.git
```
Create virtual environment and install all the packages

```
cd djangoAltairViz
virtualenv -p python3 venv
source venv/bin/activate
cd src
pip install -r requirements.txt
```

Run the Django Application

```
python manage.py runserver
```

This should run the server, and now you can open the browser and open the url, http://127.0.0.1:8000/.

There are three examples on display which can be viewed

National Family Health Survey Data: http://127.0.0.1:8000/nfhs/

India Export Data Analysis: http://127.0.0.1:8000/export/

Cricket Data: http://127.0.0.1:8000/


## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Altair](https://altair-viz.github.io/) - Altair is visualization library for python

## Acknowledgments

* [Altair](https://altair-viz.github.io/) - To creators of Altair.
* [django-altair](https://github.com/Jesse-jApps/django-altair) - A simple template tag to render Altair chart

