import itertools
import json
import os
import requests
import time
from collections.abc import Iterable
from numbers import Number, Integral


############################
# Boon Amber Python SDK v1 #
############################


class AmberUserError(Exception):
    """Raised to indicate an error in SDK usage"""

    def __init__(self, message):
        self.message = message


class AmberCloudError(Exception):
    """Raised upon any non-200 response from the Amber cloud"""

    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__("{}: {}".format(code, message))


class AmberClient():
    def __init__(self, license_id='default', license_file="~/.Amber.license"):
        """Main client which interfaces with the Amber cloud. Amber account
        credentials are discovered within a .Amber.license file located in the
        home directory, or optionally overridden using environment variables.

        Args:
            license_id (str): license identifier label found within .Amber.license file
            license_file (str): path to .Amber.license file
        
        Environment:

            `AMBER_LICENSE_FILE`: sets license_file path

            `AMBER_LICENSE_ID`: sets license_id

            `AMBER_USERNAME`: overrides the username as found in .Amber.license file

            `AMBER_PASSWORD`: overrides the password as found in .Amber.license file

            `AMBER_SERVER`: overrides the server as found in .Amber.license file

        Raises:
            AmberUserError: if error supplying authentication credentials
        """

        self.token = None

        env_license_file = os.environ.get('AMBER_LICENSE_FILE', None)
        env_license_id = os.environ.get('AMBER_LICENSE_ID', None)
        env_username = os.environ.get('AMBER_USERNAME', None)
        env_password = os.environ.get('AMBER_PASSWORD', None)
        env_server = os.environ.get('AMBER_SERVER', None)

        # if username, password and server are all specified via environment, we're done here
        if env_username and env_password and env_server:
            self.username = env_username
            self.password = env_password
            self.server = env_server
            return

        # otherwise we acquire either or both of them from license file
        license_file = env_license_file if env_license_file else license_file
        license_id = env_license_id if env_license_id else license_id

        license_path = os.path.expanduser(license_file)
        if not os.path.exists(license_path):
            raise AmberUserError("license file {} does not exist".format(license_path))

        try:
            with open(license_path, 'r') as f:
                file_data = json.load(f)
        except json.JSONDecodeError as e:
            raise AmberUserError(
                "JSON formatting error in license file: {}, line: {}, col: {}".format(e.msg, e.lineno, e.colno))

        try:
            license_data = file_data[license_id]
        except KeyError:
            raise AmberUserError("license_id \"{}\" not found in license file".format(license_id))

        # load the username, password and server, still giving precedence to environment
        try:
            self.username = env_username if env_username else license_data['username']
        except KeyError:
            raise AmberUserError("\"username\" is missing from the specified license in license file")

        try:
            self.password = env_password if env_password else license_data['password']
        except KeyError:
            raise AmberUserError("\"password\" is missing from the specified license in license file")

        try:
            self.server = env_server if env_server else license_data['server']
        except KeyError:
            raise AmberUserError("\"server\" is missing from the specified license in license file")

        self.reauth_time = time.time()

    def _authenticate(self):
        """Authenticate client for the next hour using the credentials given at
        initialization. This acquires and stores an oauth2 token which remains
        valid for one hour and is used to authenticate all other API requests.

        Raises:
            AmberCloudError: if Amber cloud gives non-200 response
        """

        url = self.server + '/oauth2'
        headers = {
            'Content-Type': 'application/json'
        }
        body = {
            'username': self.username,
            'password': self.password
        }

        response = requests.request(method='POST', url=url, headers=headers, json=body)

        if response.status_code != 200:
            message = "authentication failed: {}".format(response.json()['message'])
            raise AmberCloudError(response.status_code, message)

        # invalid credentials return a 200 where token is an empty string
        if not response.json()['idToken']:
            raise AmberCloudError(401, "authentication failed: invalid credentials")

        self.token = response.json()['idToken']

        expire_secs = int(response.json()['expiresIn'])
        self.reauth_time = time.time() + expire_secs - 60

    def _api_call(self, method, url, headers, body=None):
        """Make a REST call to the Amber server and handle the response"""

        if time.time() > self.reauth_time:
            self._authenticate()

        headers['Authorization'] = 'Bearer {}'.format(self.token)
        response = requests.request(method=method, url=url, headers=headers, json=body)

        if response.status_code != 200:
            raise AmberCloudError(response.status_code, response.json()['message'])

        # todo: why 200 status codes with error codes/message in body instead?
        if 'code' in response.json() and response.json()['code'] != 200:
            raise AmberCloudError(response.json()['code'], response.json()['message'])

        # lambda runtime errors return 200 with errorMessage in response body
        if 'errorMessage' in response.json():
            raise AmberCloudError(500, response.json()['errorMessage'])

        return response.json()

    def create_sensor(self, label=''):
        """Create a new sensor instance

        Args:
            label (str): label to assign to created sensor

        Returns:
            A string containing the `sensor_id` that was created

        Raises:
            AmberUserError: if client is not authenticated
            AmberCloudError: if Amber cloud gives non-200 response
        """

        url = self.server + '/sensor'
        headers = {
            'Content-Type': 'application/json'
        }
        body = {
            'label': label
        }
        response = self._api_call('POST', url, headers, body=body)
        sensor_id = response['sensorId']

        return sensor_id

    def update_label(self, sensor_id, label):
        """Update the label of a sensor instance

        Args:
            sensor_id (str): sensor identifier
            label (str): new label to assign to sensor

        Returns:
            A string containing the new label assigned to sensor

        Raises:
            AmberUserError: if client is not authenticated
            AmberCloudError: if Amber cloud gives non-200 response
        """

        url = self.server + '/sensor'
        headers = {
            'Content-Type': 'application/json',
            'sensorId': sensor_id
        }
        body = {
            'label': label
        }
        response = self._api_call('PUT', url, headers, body=body)
        label = response['label']

        return label

    def delete_sensor(self, sensor_id):
        """Delete an amber sensor instance

        Args:
            sensor_id (str): sensor identifier

        Raises:
            AmberUserError: if client is not authenticated
            AmberCloudError: if Amber cloud gives non-200 response
        """

        url = self.server + '/sensor'
        headers = {
            'sensorId': sensor_id
        }
        response = self._api_call('DELETE', url, headers)

    def list_sensors(self):
        """List all sensor instances currently associated with Amber account

        Returns:
            A dictionary mapping sensor IDs to corresponding labels

        Raises:
            AmberUserError: if client is not authenticated
            AmberCloudError: if Amber cloud gives non-200 response
        """

        url = self.server + '/sensors'
        headers = {}
        response = self._api_call('GET', url, headers)
        sensors = {s['sensorId']: s.get('label', None) for s in response}

        return sensors

    def configure_sensor(self, sensor_id, feature_count=1, streaming_window_size=25,
                         samples_to_buffer=1000,
                         learning_rate_numerator=10,
                         learning_rate_denominator=10000,
                         learning_max_clusters=1000,
                         learning_max_samples=1000000):
        """Configure an amber sensor instance

        Args:
            sensor_id (str): sensor identifier
            feature_count (int): number of features (dimensionality of each data sample)
            streaming_window_size (int): streaming window size (number of samples)
            samples_to_buffer (int): number of samples to load before autotuning
            learning_rate_numerator (int): sensor "graduates" (i.e. transitions from
                learning to monitoring mode) if fewer than learning_rate_numerator
                new clusters are opened in the last learning_rate_denominator samples
            learning_rate_denominator (int): see learning_rate_numerator
            learning_max_clusters (int): sensor graduates if this many clusters are created
            learning_max_samples (int): sensor graduates if this many samples are processed

        Returns:
            A dictionary containing:

                {
                    'feature_count': int,
                    'streaming_window_size': int,
                    'samples_to_buffer': int
                    'learning_rate_numerator': int
                    'learning_rate_denominator': int
                    'learning_max_clusters': int
                    'learning_max_samples': int
                }

        Raises:
            AmberUserError: if client is not authenticated or supplies invalid options
            AmberCloudError: if Amber cloud gives non-200 response
        """
        if not feature_count > 0 or not isinstance(feature_count, Integral):
            raise AmberUserError("invalid 'feature_count': must be positive integer")

        if not streaming_window_size > 0 or not isinstance(streaming_window_size, Integral):
            raise AmberUserError("invalid 'streaming_window_size': must be positive integer")

        url = self.server + '/config'
        headers = {
            'Content-Type': 'application/json',
            'sensorId': sensor_id
        }
        body = {
            'featureCount': feature_count,
            'streamingWindowSize': streaming_window_size,
            'samplesToBuffer': samples_to_buffer,
            'learningRateNumerator': learning_rate_numerator,
            'learningRateDenominator': learning_rate_denominator,
            'learningMaxClusters': learning_max_clusters,
            'learningMaxSamples': learning_max_samples
        }
        config = self._api_call('POST', url, headers, body=body)

        return config

    def _isiterable(self, x):
        # consider strings non-iterable for shape validation purposes,
        # that way they are printed out whole when caught as nonnumeric
        if isinstance(x, str):
            return False

        # collections.abc docs: "The only reliable way to determine
        # whether an object is iterable is to call iter(obj)."
        try:
            iter(x)
        except TypeError:
            return False

        return True

    def _validate_dims(self, data):
        """Validate that data is non-empty and one of the following:
           scalar value, list-like or list-of-lists-like where all
           sublists have equal length. Return 0, 1 or 2 as inferred
           number of array dimensions
        """

        # not-iterable data is a single scalar data point
        if not self._isiterable(data):
            return 0

        # iterable and unnested data is a 1-d array
        if not any(self._isiterable(d) for d in data):
            if len(list(data)) == 0:
                raise ValueError("empty")

            return 1

        # iterable and nested data is 2-d array
        if not all(self._isiterable(d) for d in data):
            raise ValueError("cannot mix nested scalars and iterables")

        sublengths = [len(list(d)) for d in data]
        if len(set(sublengths)) > 1:
            raise ValueError("nested sublists must have equal length")

        flattened_2d = list(itertools.chain.from_iterable(data))

        if any(isinstance(i, Iterable) for i in flattened_2d):
            raise ValueError("cannot be nested deeper than list-of-lists")

        if sublengths[0] == 0:
            raise ValueError("empty")

        return 2

    def _convert_to_csv(self, data):
        """Validate data and convert to a comma-separated plaintext string"""

        # Note: as in the Boon Nano SDK, there is no check that data dimensions
        # align with number of features and streaming window size.
        ndim = self._validate_dims(data)

        if ndim == 0:
            data_flat = [data]
        elif ndim == 1:
            data_flat = list(data)
        elif ndim == 2:
            data_flat = list(itertools.chain.from_iterable(data))

        for d in data_flat:
            if not isinstance(d, Number):
                raise ValueError("contained {} which is not numeric".format(d.__repr__()))

        return ','.join([str(float(d)) for d in data_flat])

    def stream_sensor(self, sensor_id, data):
        """Stream data to an amber sensor and return the inference result

        Args:
            sensor_id (str): sensor identifier
            data (array-like): data to be inferenced. Must be non-empty,
                entirely numeric and one of the following: scalar value,
                list-like or list-of-lists-like where all sublists have
                equal length.

        Returns:
            A dictionary containing inferencing results:

                {
                    'state': str,
                    'message': str,
                    'progress': int,
                    'clusterCount': int,
                    'retryCount': int,
                    'streamingWindowSize': int,
                    'ID': [int],
                    'SI': [float],
                    'AD': [int],
                    'AH': [int],
                    'AM': [float],
                    'AW': [int]
                }

                'state': current state of the sensor. One of:
                    "Buffering": gathering initial sensor data
                    "Autotuning": autotuning configuration in progress
                    "Learning": sensor is active and learning
                    "Monitoring": sensor is active but monitoring only (learning disabled)
                    "Error": fatal error has occurred
                'message': accompanying message for current sensor state
                'progress' progress as a percentage value (applicable for "Buffering" and "Autotuning" states)
                'clusterCount' number of clusters created so far
                'retryCount' number of times autotuning was re-attempted to tune streamingWindowSize
                'streamingWindowSize': streaming window size of sensor (may differ from value given at configuration if window size was adjusted during autotune)
                'ID': list of cluster IDs. The values in this list correspond one-to-one
                    with input samples, indicating the cluster to which each input pattern
                    was assigned.
                'SI': smoothed anomaly index. The values in this list correspond
                    one-for-one with input samples and range between 0.0 and 1.0. Values
                    closer to 0 represent input patterns which are ordinary given the data
                    seen so far on this sensor. Values closer to 1 represent novel patterns
                    which are anomalous with respect to data seen before.
                'AD': list of binary anomaly detection values. These correspond one-to-one
                    with input samples and are produced by thresholding the smoothed anomaly
                    index (SI). The threshold is determined automatically from the SI values.
                    A value of 0 indicates that the SI has not exceeded the anomaly detection
                    threshold. A value of 1 indicates it has, signaling an anomaly at the
                    corresponding input sample.
                'AH': list of anomaly history values. These values are a moving-window sum of
                    the AD value, giving the number of anomaly detections (1's) present in the
                    AD signal over a "recent history" window whose length is the buffer size.
                'AM': list of "Amber Metric" values. These are floating point values between
                    0.0 and 1.0 indicating the extent to which each corresponding AH value
                    shows an unusually high number of anomalies in recent history. The values
                    are derived statistically from a Poisson model, with values close to 0.0
                    signaling a lower, and values close to 1.0 signaling a higher, frequency
                    of anomalies than usual.
                'AW': list of "Amber Warning Level" values. This index is produced by thresholding
                    the Amber Metric (AM) and takes on the values 0, 1 or 2 representing a discrete
                    "warning level" for an asset based on the frequency of anomalies within recent
                    history. 0 = normal, 1 = asset changing, 2 = asset critical. The default
                    thresholds for the two warning levels are the standard statistical values
                    of 0.95 (outlier, asset changing) and 0.997 (extreme outlier, asset critical).

        Raises:
            AmberUserError: if client is not authenticated or supplies invalid data
            AmberCloudError: if Amber cloud gives non-200 response
        """

        # Server expects data as a plaintext string of comma-separated values.
        try:
            data_csv = self._convert_to_csv(data)
        except ValueError as e:
            raise AmberUserError("invalid data: {}".format(e))

        url = self.server + '/stream'
        headers = {
            'Content-Type': 'application/json',
            'sensorId': sensor_id
        }
        body = {
            'data': data_csv
        }

        results = self._api_call('POST', url, headers, body=body)

        # normalize index values from the range [0, 1000] to [0.0, 1.0]
        results['SI'] = [r / 1000.0 for r in results['SI']]

        return results

    def get_sensor(self, sensor_id):
        """Get info about a sensor

        Args:
            sensor_id (str): sensor identifier

        Returns:
            A dictionary containing sensor information:

                {
                    'label': str,
                    'sensorId': str,
                    'tenantId': str,
                    'usageInfo': {
                        putSensor {
                            'callsTotal': int
                            'callsThisPeriod': int
                            'lastCalled': str
                        },
                        getSensor {
                            'callsTotal': int
                            'callsThisPeriod': int
                            'lastCalled': str
                        },
                        getConfig {
                            'callsTotal': int
                            'callsThisPeriod': int
                            'lastCalled': str
                        },
                        postStream {
                            'callsTotal': int
                            'callsThisPeriod': int
                            'lastCalled': int
                            'samplesTotal': int
                            'samplesThisPeriod': int
                        }
                        getStatus {
                            'callsTotal': int
                            'callsThisPeriod': int
                            'lastCalled': str
                        }
                    }
                }

                'label' (str): sensor label
                'sensorId' (str): sensor identifier
                'tenantId' (str): username of associated Amber account
                'callsTotal': total number of calls to this endpoint
                'callsThisPeriod': calls this billing period to this endpoint
                'lastCalled': ISO formatted time of last call to this endpoint
                'samplesTotal': total number of samples processed
                'samplesThisPeriod': number of samples processed this billing period

        Raises:
            AmberUserError: if client is not authenticated
            AmberCloudError: if Amber cloud gives non-200 response
        """

        url = self.server + '/sensor'
        headers = {
            'Content-Type': 'application/json',
            'sensorId': sensor_id
        }
        sensor = self._api_call('GET', url, headers)

        return sensor

    def get_config(self, sensor_id):
        """Get current sensor configuration

        Args:
            sensor_id (str): sensor identifier

        Returns:
            A dictionary containing the current sensor configuration:

                {
                    'featureCount': int,
                    'streamingWindowSize': int,
                    'samplesToBuffer': int,
                    'learningRateNumerator': int,
                    'learningRateDenominator': int,
                    'learningMaxClusters': int,
                    'learningMaxSamples': int,
                    'percentVariation': float,
                    'features':
                    [
                        {
                            'min': float,
                            'max': float
                        }
                    ]
                }

                'featureCount': number of features (dimensionality of each data sample)
                'streamingWindowSize': streaming window size (number of samples)
                'samplesToBuffer': number of samples to load before autotuning
                'learningRateNumerator': sensor "graduates" (i.e. transitions from
                    learning to monitoring mode) if fewer than learning_rate_numerator
                    new clusters are opened in the last learning_rate_denominator samples
                'learningRateDenominator': see learning_rate_numerator
                'learningMaxClusters': sensor graduates if this many clusters are created
                'learningMaxSamples': sensor graduates if this many samples are processed
                'percentVariation': percent variation parameter discovered by autotuning
                'features': min/max values per feature discovered by autotuning
        Raises:
            AmberUserError: if client is not authenticated
            AmberCloudError: if Amber cloud gives non-200 response
        """

        url = self.server + '/config'
        headers = {
            'Content-Type': 'application/json',
            'sensorId': sensor_id
        }
        config = self._api_call('GET', url, headers)

        return config

    def get_status(self, sensor_id):
        """Get sensor status

        Args:
            sensor_id (str): sensor identifier

        Returns:
            A dictionary containing the clustering status for a sensor:

                {
                    'pca' [(int,int,int)],
                    'clusterGrowth' [int],
                    'clusterSizes' [int],
                    'anomalyIndexes' [int],
                    'frequencyIndexes' [int],
                    'distanceIndexes' [int],
                    'totalInferences' [int],
                    'numClusters' [int],
                }

                'pca': list of length-3 vectors representing cluster centroids
                    with dimensionality reduced to 3 principal components. List length
                    is one plus the maximum cluster ID, with element 0 corresponding
                    to the "zero" cluster, element 1 corresponding to cluster ID 1, etc.
                'clusterGrowth': sample index at which each new cluster was created.
                    Elements for this and other list results are ordered as in 'pca'.
                'clusterSizes': number of samples in each cluster
                'anomalyIndexes': anomaly index associated with each cluster
                'frequencyIndexes': frequency index associated with each cluster
                'distanceIndexes': distance index associated with each cluster
                'totalInferences': total number of inferences performed so far
                'numClusters': number of clusters created so far (includes zero cluster)

        Raises:
            AmberUserError: if client is not authenticated
            AmberCloudError: if Amber cloud gives non-200 response
        """

        url = self.server + '/status'
        headers = {
            'Content-Type': 'application/json',
            'sensorId': sensor_id
        }
        status = self._api_call('GET', url, headers)

        return status
