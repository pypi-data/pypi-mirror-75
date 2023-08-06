#!/usr/bin/env python3
from qr_code_generator.errors import *
from qr_code_generator.helpers import Config, Options, load_yaml

import requests
import os
import json
import time


class QrGenerator:
    """
    QRGenerator Class, which wraps the API of qr-code-generator.com

    Parameters
    ----------
    token : str
        API Access Token, which can be retrieved from https://app.qr-code-generator.com/api/?from=options
        Set to '.env' to load access-token from environment (export ACCESS_TOKEN=your token here)

    **kwargs
        A way to directly set the options and configuration settigs when calling the generator.
        >>> t = QrGenerator(qr_code_text='TEST')
        >>> t.get('qr_code_text')
        'TEST'

    Attributes
    ----------
    options : dict
        Dictionary with the options object used in the POST request to the API

    config : dict
        Configuration settings for the project. Can be updated to change workings of the program.

    output_filename : str
        Filename to output to. Should not include extension. Can either be changed directly or gets updated in the request function.
    """
    def __init__(self, token=None, **kwargs):
        self.options = Options()
        self.config = Config()
        self.output_filename = None

        if token:
            self.set('access_token', token)
        else:
            try:
                self.set('access_token', os.environ['ACCESS_TOKEN'])
            except KeyError:
                pass

        for key, value in kwargs.items():
            self.set(key, value)

        if not os.path.exists(self.config['OUT_FOLDER']):
            self.__log(f'Folder {self.config["OUT_FOLDER"]} does not exist. Creating it.', 'warning')
            os.mkdir(self.config['OUT_FOLDER'])

        if not os.path.exists(self.config['OUT_FOLDER'] + '/' + self.config['OUTPUT_FOLDER']):
            self.__log(f'Folder {self.config["OUTPUT_FOLDER"]} does not exist. Creating it.', 'warning')
            os.mkdir(self.config['OUT_FOLDER'] + '/' + self.config['OUTPUT_FOLDER'])

    def set(self, key, value):
        """
        Setter for both the options and the configuration. If exists, updates the key value.
        >>> t = QrGenerator()
        >>> t.set('qr_code_text', 'Job')
        >>> t.get('qr_code_text')
        'Job'

        >>> t.set('doesnotexist', 'value')
        Traceback (most recent call last):
        KeyError

        Parameters
        ----------
        key : str
            The key that we want to change, all caps for config, otherwise will be interpreted as option
        value : str
            The value we want to update specified key to

        Raises
        ------
        KeyError
            The parameter that is requested to be updated does not exist

        Returns
        -------
        None
        """
        if key == key.upper():
            if key not in self.config:
                self.__log(f'Error when setting configuration variable "{key}", it does not exist', 'error')
                raise KeyError
            self.__log(f'Setting configuration variable "{key}" to "{value}"')
            self.config[key] = value
        else:
            if key not in self.options:
                self.__log(f'Error when setting option "{key}", it does not exist.', 'error')
                raise KeyError
            self.__log(f'Setting option "{key}" to "{value}"')
            self.options[key] = value

    def get(self, key):
        """
        Getter for the options and configuration dictionary. If key exists, returns the value.
        >>> t = QrGenerator()
        >>> t.get('qr_code_text') == t.options['qr_code_text']
        True

        >>> t = QrGenerator()
        >>> not t.get('xdwdwedewdwede')
        True

        Parameters
        ----------
        key : str
            The key of which the value is requested to be returned, all caps for configuration key

        Returns
        -------
        value : str
            The value of the requested key in the data dictionary
        """
        try:
            if key == key.upper():
                return self.config[key]
            return self.options[key]
        except KeyError:
            return None

    def create_query_url(self):
        """
        Generates the query URL which is necessary to retrieve the QR code from the API

        Returns
        -------
        query_url : str
            The URL including querystring that can be used to send the POST request
        """
        self.__log('Starting to create the query URL.')
        query_url = self.config['API_URI']
        for key, value in self.options.items():
            if value:
                if query_url == self.config['API_URI']:
                    query_url = query_url + str(key) + "=" + str(value)
                else:
                    query_url = query_url + "&" + str(key) + "=" + str(value)
        query_url = query_url.replace(' ', '%20')
        self.__log(f'Done creating query url. URL to query: "{query_url}"')
        return query_url

    def request(self, file_name=None):
        """
        Requests a QR code from the API with the settings specified in the options object.

        Parameters
        ----------
        file_name : str
            Default None. Used to set the name of the file that should be outputted. Do not give in extension.

        Returns
        -------
        None
        """
        self.__log('Starting to build a request.', 'warning')
        if file_name:
            self.__log(f'File name specified. Setting output filename to "{file_name}"')
            self.output_filename = file_name

        self.validate()
        url = self.create_query_url()
        self.__log('Initiating post request to query URL.')
        req = requests.post(url, data=self.options)
        self.handle_response(req)
        self.cleanup()

    def handle_response(self, response):
        """
        Handles the response from the API by checking status code and choosing whether or not to call error handling.

        Parameters
        ----------
        response : Response
            The full Response object that was retrieved from the API

        Returns
        -------
        None
        """
        self.__log(f'Received response from server. The code is: "{response}"')
        if not response.status_code == 200:
            self.handle_api_error(response)
        self.to_output_file(response.text)

    def cleanup(self):
        """
        Resets the file name after receiving a QR code, so that file is never overwritten when not called for by user.
        >>> t = QrGenerator()
        >>> t.output_filename = 'Radishes'
        >>> print(t.output_filename)
        Radishes
        >>> t.cleanup()
        >>> print(t.output_filename)
        None

        Returns
        -------
        None
        """
        self.__log('Resetting value for output_filename, making way for another go.')
        self.output_filename = None

    def to_output_file(self, content):
        """
        Writes the content of the response to the output file.

        Parameters
        ----------
        content : Response.text
            The text content of the response that was sent by the API.

        Raises
        ------
        FileExistsError
            Output file does already exist and cannot be overwritten due to config settings.

        Returns
        -------
        None
        """
        self.__log(f'Starting to write response content to output file.')
        if self.output_file_exists() and not self.config['FORCE_OVERWRITE']:
            self.__log(f'Cannot write to file. Selected output file exists and FORCE_OVERWRITE is disabled.', 'error')
            raise FileExistsError
        file = self.config['OUT_FOLDER'] + '/' + self.config['OUTPUT_FOLDER'] + '/' + self.output_filename + '.' \
            + self.options['image_format'].lower()
        with open(file, 'w') as f:
            f.writelines(content)
        self.__log(f'Successfully wrote response content to "{file}".', 'success')

    def handle_api_error(self, response):
        """
        Error handling for status codes sent back by the API.

        Parameters
        ----------
        response : Response
            The full Response object that was returned by the API.

        Raises
        ------
        InvalidCredentialsError
            The access-token has been rejected by the API and is considered invalid.
        FileNotFoundError
            The requested API URI does not exist.
        UnprocessableRequestError
            The request could not be processed by the API.
        MonthlyRequestLimitExceededError
            The current authenticated user has run out of monthly requests. Either change token, upgrade or wait.

        Returns
        -------
        None
        """
        code = response.status_code
        self.__log(f'Handling API error with status code {code}.', 'error')
        if code == 401:
            self.__log(f'Invalid credentials. Please make sure your token is correct.', 'error')
            raise InvalidCredentialsError
        if code == 404:
            self.__log(f'File not found on query. Make sure query URL is correct and retry.', 'error')
            raise FileNotFoundError
        if code == 422:
            content = json.loads(response.content)
            for error in content['errors']:
                self.__log(f'API could not process the request. Message: {error["message"]}.', 'error')
                raise UnprocessableRequestError(f'Issue with field {error["field"]}: {error["message"]}')
        if code == 429:
            self.__log(f'Monthly request limits exceeded. Upgrade billing or change token.', 'error')
            raise MonthlyRequestLimitExceededError
        self.__log(f'Response for code: "{code}" was unhandled by wrapper. Sorry to not be more helpful.', 'error')
        raise UnknownApiError("An unhandled API exception occurred")

    def output_file_exists(self):
        """
        Checks whether or not the output file exists in the selected output folders.

        Returns
        -------
        exists : bool
            Whether or not the output file does exists in the set output folder mapping.
        """
        file = self.config['OUT_FOLDER'] + '/' + self.config['OUTPUT_FOLDER'] + '/' + self.output_filename + '.' + \
            self.options['image_format'].lower()
        self.__log(f'Checking if output file: "{file}" already exists.')
        if os.path.exists(file) and not os.stat(file).st_size == 0:
            self.__log(f'Output file: "{file}" does exist.')
            return True
        self.__log(f'Output file: "{file}" does not exist.')
        return False

    def hash_time(self):
        """
        Create a unique name based on the hashed unix timestamp.

        Returns
        -------
        filename : str
            The name for the output file, based on the current timestamp
        """
        self.__log('Hashing time to create a unique filename.')
        filename = f'QR-{time.strftime("%Y%m%d-%H%M%S")}'
        self.__log(f'The file name is {filename}.')

        return filename

    def __log(self, message, sort='Message'):
        """
        Send a message to the console, when VERBOSE setting has been enabled.

        Parameters
        ----------
        message : str
            The message to relay to the user.
        sort : str
            The type of message to relay to the user, defaults to 'message'

        Returns
        -------
        None
        """
        if self.config['VERBOSE'] is True:
            # Set color prefix for error message
            if sort.lower() == 'error':
                prefix = '\033[91m\033[1m'
            elif sort.lower() == 'warning':
                prefix = '\033[93m'
            elif sort.lower() == 'success':
                prefix = '\033[92m\033[1m'
            else:
                prefix = '\033[94m'

            # Suffix will return console text to normal
            suffix = '\033[0m'

            # Set time
            current_time = time.strftime('%H:%M:%S')

            # Set the total message and send it to the console
            msg = f'{prefix}[{current_time}] {message}{suffix}'
            print(msg)

    def load(self, file):
        """
        Loads in the yaml file and splits the contents.

        Parameters
        ----------
        file : str
            The relative path to the yaml file with the settings in it

        Raises
        ------
        UnknownYamlContentError
            Content in the yaml-file does not meet requirements as specified in documentation

        Returns
        -------
        None
        """
        self.__log(f'Starting to load settings from {file}', 'warning')
        contents = load_yaml(file)
        for item in contents:
            if item == 'options':
                self.__log(f'Found options in {file}, loading them', 'warning')
                for i in contents[item]:
                    self.__log(f'Setting {i.lower()} to {contents[item][i]}')
                    self.set(i.lower(), contents[item][i])
            elif item == 'config':
                self.__log(f'Found configuration variables in {file}, loading them', 'warning')
                for i in contents[item]:
                    self.__log(f'Setting {i.upper()} to {contents[item][i]}')
                    self.set(i.upper(), contents[item][i])
            else:
                raise UnknownYamlContentError

    def validate(self):
        """
        Validates the content in the request client-side to avoid getting errors processing.
        Since the API does not give back an error on missing parameter, we validate this to avoid pointless requests.

        Raises
        ------
        FileNotFoundError
            Either the combination of OUT_FOLDER and OUTPUT_FOLDER does not exist, or there was no filename to write to.
        MissingRequiredParameterError
            The request is sent with a missing parameter, which would lead to an error on the server side.
        ValueError
            Output file name contains a '.' and thus an extension, which it should not.

        Returns
        -------
        None
        """
        self.__log('Validating whether all conditions are met.')
        if not self.config['OUT_FOLDER'] or not self.config['OUTPUT_FOLDER']:
            self.__log('The path to the output folder cannot be found.', 'error')
            raise FileNotFoundError

        try:
            if '.' in self.output_filename:
                self.__log('The output filename should not contain an extension.', 'error')
                raise ValueError
        except TypeError:
            pass

        if not self.output_filename:
            self.__log('The output filename has not been specified.', 'warning')
            self.output_filename = self.hash_time()
            i = 0
            while self.output_file_exists():
                self.__log('Adding a unique identifier to current filename.', 'warning')
                self.output_filename = self.output_filename + '-' + i
                i += 1
            self.__log(f'Continuing with file: "{self.output_filename}"', 'success')

        # Iterate over options to check for required parameters, as to not waste requests
        self.__log('Starting to check if all required parameters are set')
        for key, value in self.options.items():
            if key in self.config['REQUIRED_PARAMETERS'] and not value:
                self.__log(f'Missing a required parameter: {key}', 'error')
                raise MissingRequiredParameterError(key)

        self.__log('All validation successful.', 'success')
