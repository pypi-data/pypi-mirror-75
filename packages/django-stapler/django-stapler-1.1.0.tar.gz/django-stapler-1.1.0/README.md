# django-stapler
[![Build Status](https://travis-ci.org/danjer/django-stapler.svg?branch=master)](https://travis-ci.org/danjer/django-stapler)

Provides a simple way to combine multiple ModelForm classes

## Description


Django's ModelForm class lets you create a Form class for a model. This lets you conveniently create and update model instances. In some specific cases it would be desiarble to combine multiple ModelForms so that you can create and update multiple model instances in one view with one form. django-stapler provides this functionality


### Dependencies

[![Python 3.6](https://img.shields.io/badge/python-3.6-green.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.7](https://img.shields.io/badge/python-3.7-green.svg)](https://www.python.org/downloads/release/python-370/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-green.svg)](https://www.python.org/downloads/release/python-380/)

* Django 2.2+

### Installing

```python
pip install django-stapler
```

### Basic usage
Add app to settings.py
```python

INSTALLED_APPS = [ ...
                   'stapler',
                 ]
```
 Define Model classes as usual

models.py
```python
from django.db import models

# Create your models here.
class Bike(models.Model):

    name = models.CharField(max_length=10)
    frame_type = models.CharField(max_length=10, blank=True, null=True)

class Manufacturer(models.Model):

    name = models.CharField(max_length=10)
    chief = models.CharField(max_length=10)
```

Also declare the ModelForm classes as usual, and in addition staple the ModelForms together by creating a new StapleForm class.
In the inner ```Meta``` class set the ```modelforms``` attribute to a tuple of to staple ```ModelForms```.

forms.py
```python
from django.forms import ModelForm
from stapler.forms import StaplerForm
from .models import Bike, Manufacturer


class BikeModelForm(ModelForm):

    class Meta:
        model = Bike
        fields = ['name', 'price']


class ManufacturerModelForm(ModelForm):

    class Meta:
        model = Manufacturer
        fields = ['name', 'revenue']

class StapledForm(StaplerForm):

    class Meta:
        modelforms = (BikeModelForm, ManufacturerModelForm)
        #auto_prefix = False, defaults is True
```

The ```StapledForm``` yields a form with four fields: ```bike__name, bike__price, manufacturer__name, manufacturer__revenue```.
If you want to keep the original field names, you can set the ```auto_prefix``` attribute in the Meta class to ```False```.
This may lead to unexpected behaviour when fieldnames between models clash.

You can use the ```StapledForm``` in views.py to create a new ```Bike``` and ```Manufacturer``` instance in one go by calling
```form.save()```. This wil return a dictionary with keys resembling the Model class names in lowercase with the ```_instance```
 suffix. The keys map to the newly created instances:

views.py
```python
from django.views.generic.edit import FormView
from .forms import StapledForm

class SomeView(FormView):
    template_name = 'example.html'
    form_class = StapledForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        result = form.save()
        nw_bike = result['bike_instance']   # the saved bike instance
        nw_manufacturer = result['manufacturer_instance'] # the saved manufacturer instance
        return super().form_valid(form)
```

You can also use the form to update existing instances by providing a ```tuple``` of instances to the named ```instances``` argument:
```python
from .models import Bike, Manufacturer
from .forms import StapledForm

...

# inside view function
bike = Bike.objects.first()
manufacturer = Manufacturer.objects.first()

form = StapledForm(data=request.POST, instances=(bike, manufacturer))
if form.is_valid():
    result = form.save()
    result # this is a dictionary with the updated instances

```
StapledForm provides the ```pre_save``` and ```post_save``` hooks. These methods
are called before and after the instances are saved when the ```save()``` method is called:

```python
class StapledForm(StaplerForm):

    ...

    def pre_save(self):
        print("did you get the memo?")


    def post_save(self):
        print("have you seen my stapler?")

```

## Extra options
In addition to modelforms attribute, you can set a few options in ```Meta``` class that alter the behaviour of the ```StaplerForm```
-  ```auto_prefix```: defaults to ```True```. This will append a prefix of the model class name to the appropriate fields
-  ```required```: A tuple of the ```ModelForm``` classes that are required. By default, all ```ModelForm``` classes defined in ```modelforms``` are required.
If a ```ModelForm``` is not in the ```required``` attribute,  it's errors are ignored and ```is_valid()``` can still return ```True```. 
Calling ```save()``` in this case will only save the instances of ```ModelForms``` that did validate. Instead of an instance, ```None``` is stored in the returned dictionary



## License

This project is licensed under the MIT License - see the LICENSE.md file for details