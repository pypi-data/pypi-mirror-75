# Common Python Helper Functions

This library contains reused code for all the EASIER-AI projects written in Python.

## Using the library

### Install
This library is available through [PIP](https://pypi.org/project/easierai-common-functions/) package manager.
To install it, execute 
> pip install easierai-common-functions

### Importing
The library needs to be imported in order to use it:
> import common_functions.helpers as helpers

> from minio import Minio

> from common_functions.logger import Logger

Then, there needs to be some configuration:
> helpers.config = helpers.read_config_file(config_file_path)

> helpers.minioClient = Minio(minio_host + ':' + minio_port, minio_access, minio_secret, secure=False)

> helpers._logger = Logger('helpers', 'helpers.py')

If you wish to check the validity of the configuration provided for an inferencer, you can use this method (it will notify at start if there are no valid models):
> helpers.check_initial_config(eslib, False)

Where eslib is a valid started instance of the [elasticsearch library](https://pypi.org/project/easierai-elasticsearchlib/).

### Necessary environmental variables
This library reads from the following environmental variables:
- LOGSTASH_HOST: IP/hostname hosting the Logstash service to upload the logs
- LOGSTASH_PORT: port of where the Logstash service is listening

### Usage

The library has these functions available:

> get_data_shape(data_type, num_features, num_samples, algorithm)

Outputs the data_shape required according to the parameters passed.

> importer(algorithm, inference_type=constants.ESTIMATOR, lr=0.001)

Returns a predictor instance according to the parameters passed.

> load_model_file(eslib, id, inference_type=constants.ESTIMATOR)

Returns the document stored on Elasticsearch, which includes, among other things, the h5 and pkl files where we had saved the model and the scalers, respectively.
:param id: id of the entity
:param inference_type: this param helps us to download the right model according to its features and parameters
:return: dict with the format {"extension": object, "extension2": object2}

> read_config_file(config_path)

Initializes the config variable

> check_initial_config(eslib, is_classifier)

Checks if there is any model in the database that matches the configuration provided.

> scale_dataset(scaler, data, i, ft_range=(-1, 1), training=True)

Scale data (in np.array or list format) using MinMaxScaler and the ft_range given (default is (-1,1)
    :param data: array of data to be scaled
    :param i: feature corresponding to the scaler
    :param ft_range: tuple containing minimum and maximum values of the data already scaled
    :return: tuple of scaler and data scaled

> compose_model_params(is_classifier)

Composes a json object with the parameters of a trained model to store in the database

> compose_model_params_filter(is_classifier)

Composes a json object with the parameters in the config file used to look for the models in the database.

> save_model(eslib, id, metadata, dict={}, inference_type=constants.ESTIMATOR, _id=None, save_tflite=False, calibration_data=None)

Saves the model related files after training. Has the ability to save a model as tflite format.
The parameter dict should come in the format {"extension1": object1, "extension2": object2 ... }.
The calibration_data is only used when saving a model as tflite format, and should be a representation of the dataset.

## Additional features 

### Constants file
The constants used on EASIER-AI services are stored in _common_functions/constants.py_ file. It can be imported as:

> import common_functions.constants as constants

### Advanced logger
This logger has the same syntax as the default _logging_ python library. It needs to be imported and initialized as:

> from common_functions.logger import Logger

> logger = Logger(service_name, filename)

It then can be used as logger.info(message), logger.debug(message, additional_info), etc.

This logger, apart from printing to console, uploads each log instance to Elasticsearch via Logstash, through a TCP port. To use this functionality it is needed to define the previously mentioned LOGSTASH_HOST and LOGSTASH_PORT environment variables.

### Edge toolkit
This class is in charge of converting a tensorflow or keras model into tensorflow lite. It can be used as:

> from edge_tools import Edge_Toolkit

> edge_toolkit = Edge_Toolkit(logger)

> edge_toolkit.convert_model_lite(calibration_data=calibration_data, keras_model_path=filename + '.' + constants.MODEL_EXTENSION)

After executing these lines, the tflite file will be stored in ../storage/ and can be uploaded to a remote filesystem.

### Model definitions
The model definitions used by EASIER are also stored in this library. They are imported by the helpers file using the _importer( ... )_ function. 

# Copyright

Copyright (C) 2020 ATOS Spain	All Rights Reserved.
