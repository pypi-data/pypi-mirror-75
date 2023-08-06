import os
import nose
import time
from nose.tools import assert_equal
from nose.tools import assert_true
from nose.tools import assert_raises
from nose.tools import assert_is_instance
from boonamber import AmberClient, AmberUserError, AmberCloudError

TEST_SENSOR_ID = '52fa82fbf86758bf'


class TestInit:
    def unset_environment_variables(self):
        os.environ['AMBER_LICENSE_FILE'] = ''
        os.environ['AMBER_LICENSE_ID'] = ''
        os.environ['AMBER_USERNAME'] = ''
        os.environ['AMBER_PASSWORD'] = ''
        os.environ['AMBER_SERVER'] = ''

    def test_init(self):
        self.unset_environment_variables()

        # set credentials using license file
        amber = AmberClient(license_id="default", license_file="test.Amber.license")

        # set credentials using license file specified via environment variables
        os.environ['AMBER_LICENSE_FILE'] = "test.Amber.license"
        os.environ['AMBER_LICENSE_ID'] = "default"
        amber = AmberClient(license_id=None, license_file=None)

        # set credentials directly using environment variables
        os.environ['AMBER_USERNAME'] = "amber-test-user"
        os.environ['AMBER_PASSWORD'] = "filler-password"
        os.environ['AMBER_SERVER'] = "https://amber-local.boonlogic.com/dev"
        amber = AmberClient(license_id=None, license_file=None)

        self.unset_environment_variables()

    def test_init_negative(self):
        self.unset_environment_variables()
        assert_raises(AmberUserError, AmberClient, "default", "nonexistent-license-file")
        assert_raises(AmberUserError, AmberClient, "nonexistent-license-id", "test.Amber.license")
        assert_raises(AmberUserError, AmberClient, "missing-username", "test.Amber.license")
        assert_raises(AmberUserError, AmberClient, "missing-password", "test.Amber.license")
        assert_raises(AmberUserError, AmberClient, "missing-server", "test.Amber.license")


class TestAuth:
    def setUp(self):
        self.amber = AmberClient(license_file="test.Amber.license")
        self.amber.password = os.environ['AMBER_TEST_PASSWORD']

    def setup_garbage_credentials(self):
        self.amber = AmberClient(license_id="garbage", license_file="test.Amber.license")

    def test_authenticate(self):
        result = self.amber._authenticate()

    def test_authenticate_negative(self):
        self.setup_garbage_credentials()
        with assert_raises(AmberCloudError) as context:
            self.amber._authenticate()
        assert_equal(context.exception.code, 401)


class TestEndpoints:
    def setUp(self):
        self.amber = AmberClient(license_file="test.Amber.license")
        self.amber.password = os.environ['AMBER_TEST_PASSWORD']
        self.amber._authenticate()

    def setup_created_sensor(self):
        try:
            sensor_id = self.amber.create_sensor('test-sensor')
        except Exception as e:
            raise RuntimeError("setup failed: {}".format(e))
        self.sensor_id = sensor_id

    def teardown_created_sensor(self, sensor_id):
        try:
            self.amber.delete_sensor(sensor_id)
        except Exception as e:
            raise RuntimeError("teardown failed, sensor was not deleted: {}".format(e))

    def test_create_sensor(self):
        sensor_id = self.amber.create_sensor('test-sensor')
        self.teardown_created_sensor(sensor_id)

    def test_delete_sensor(self):
        self.setup_created_sensor()
        self.amber.delete_sensor(self.sensor_id)

    def test_delete_sensor_negative(self):
        with assert_raises(AmberCloudError) as context:
            self.amber.delete_sensor('nonexistent-sensor-id')
        assert_equal(context.exception.code, 404)

    def test_update_label(self):
        label = self.amber.update_label(TEST_SENSOR_ID, 'new-label')
        assert_equal(label, 'new-label')

        try:
            self.amber.update_label(TEST_SENSOR_ID, 'test-sensor')
        except Exception as e:
            raise RuntimeError("teardown failed, label was not changed back to 'test-sensor': {}".format(e))

    def test_update_label_negative(self):
        with assert_raises(AmberCloudError) as context:
            label = self.amber.update_label('nonexistent-sensor-id', 'test-sensor')
        assert_equal(context.exception.code, 404)

    def test_get_sensor(self):
        expected = {
            'label': 'test-sensor',
            'sensorId': TEST_SENSOR_ID,
            'tenantId': 'amber-test-user'
        }
        sensor = self.amber.get_sensor(TEST_SENSOR_ID)
        assert_equal(sensor['label'], 'test-sensor')
        assert_equal(sensor['sensorId'], TEST_SENSOR_ID)
        assert_equal(sensor['tenantId'], 'amber-test-user')
        assert_true('usageInfo' in sensor)

    def test_get_sensor_negative(self):
        with assert_raises(AmberCloudError) as context:
            sensor = self.amber.get_sensor('nonexistent-sensor-id')
        assert_equal(context.exception.code, 404)

    def test_list_sensors(self):
        sensors = self.amber.list_sensors()
        assert_true(TEST_SENSOR_ID in sensors.keys())

    def test_configure_sensor(self):
        expected = {
            'featureCount': 1,
            'streamingWindowSize': 25,
            'samplesToBuffer': 1000,
            'learningRateNumerator': 10,
            'learningRateDenominator': 10000,
            'learningMaxClusters': 1000,
            'learningMaxSamples': 1000000,
        }
        config = self.amber.configure_sensor(TEST_SENSOR_ID, feature_count=1, streaming_window_size=25,
                                             samples_to_buffer=1000,
                                             learning_rate_numerator=10,
                                             learning_rate_denominator=10000,
                                             learning_max_clusters=1000,
                                             learning_max_samples=1000000)
        assert_equal(config, expected)

    def test_configure_sensor_negative(self):
        with assert_raises(AmberCloudError) as context:
            config = self.amber.configure_sensor('nonexistent-sensor-id')
        assert_equal(context.exception.code, 404)

        # invalid feature_count or streaming_window_size
        assert_raises(AmberUserError, self.amber.configure_sensor, TEST_SENSOR_ID, feature_count=-1)
        assert_raises(AmberUserError, self.amber.configure_sensor, TEST_SENSOR_ID, feature_count=1.5)
        assert_raises(AmberUserError, self.amber.configure_sensor, TEST_SENSOR_ID, streaming_window_size=-1)
        assert_raises(AmberUserError, self.amber.configure_sensor, TEST_SENSOR_ID, streaming_window_size=1.5)

    def test_get_config(self):
        expected = {
            'featureCount': 1,
            'streamingWindowSize': 25,
            'samplesToBuffer': 1000,
            'learningRateNumerator': 10,
            'learningRateDenominator': 10000,
            'learningMaxClusters': 1000,
            'learningMaxSamples': 1000000,
            'percentVariation': 0.05,
            'features': [{'minVal': 0, 'maxVal': 1}]
        }
        config = self.amber.get_config(TEST_SENSOR_ID)
        assert_equal(config, expected)

    def test_get_config_negative(self):
        with assert_raises(AmberCloudError) as context:
            config = self.amber.get_config('nonexistent-sensor-id')
        assert_equal(context.exception.code, 404)

    def test_stream_sensor(self):
        results = self.amber.stream_sensor(TEST_SENSOR_ID, 1)
        assert_true('state' in results)
        assert_true('message' in results)
        assert_true('progress' in results)
        assert_true('clusterCount' in results)
        assert_true('retryCount' in results)
        assert_true('streamingWindowSize' in results)
        assert_true('SI' in results)
        assert_true('AD' in results)
        assert_true('AH' in results)
        assert_true('AM' in results)
        assert_true('AW' in results)

        # scalar data should return SI of length 1
        assert_true(len(results['SI']) == 1)

        # array data should return SI of same length
        results = self.amber.stream_sensor(TEST_SENSOR_ID, [1, 2, 3, 4, 5])
        assert_true(len(results['SI']) == 5)

    def test_stream_sensor_negative(self):
        with assert_raises(AmberCloudError) as context:
            results = self.amber.stream_sensor('nonexistent-sensor-id', [1, 2, 3, 4, 5])
        assert_equal(context.exception.code, 404)

        # invalid data
        assert_raises(AmberUserError, self.amber.stream_sensor, TEST_SENSOR_ID, [])
        assert_raises(AmberUserError, self.amber.stream_sensor, TEST_SENSOR_ID, [1, '2', 3])
        assert_raises(AmberUserError, self.amber.stream_sensor, TEST_SENSOR_ID, [1, [2, 3], 4])

    def test_get_status(self):
        status = self.amber.get_status(TEST_SENSOR_ID)
        assert_true('pca' in status)
        assert_true('numClusters' in status)

    def test_get_status_negative(self):
        with assert_raises(AmberCloudError) as context:
            status = self.amber.get_status('nonexistent-sensor-id')
        assert_equal(context.exception.code, 404)


class TestAPICall:
    def setUp(self):
        self.amber = AmberClient(license_file="test.Amber.license")
        self.amber.password = os.environ['AMBER_TEST_PASSWORD']

        self.server = self.amber.server
        self.headers = {
            'Content-Type': 'application/json',
        }

    def test_api_call(self):
        # first call covers reauth case, second call covers no reauth case
        self.amber._api_call('GET', self.server + '/sensors', self.headers)
        self.amber._api_call('GET', self.server + '/sensors', self.headers)

    def test_api_call_negative(self):
        # call that fails due to a garbage internal token
        self.amber.reauth_time = time.time() + 60
        self.amber.token = 'garbage-token'
        assert_raises(AmberCloudError, self.amber._api_call, 'GET', self.server + '/sensors', self.headers)


class TestDataHandling:
    def setUp(self):
        self.amber = AmberClient(license_file="test.Amber.license")

    def test_convert_to_csv(self):
        # valid scalar inputs
        assert_equal("1.0", self.amber._convert_to_csv(1))
        assert_equal("1.0", self.amber._convert_to_csv(1.0))

        # valid 1d inputs
        assert_equal("1.0,2.0,3.0", self.amber._convert_to_csv([1, 2, 3]))
        assert_equal("1.0,2.0,3.0", self.amber._convert_to_csv([1, 2, 3.0]))
        assert_equal("1.0,2.0,3.0", self.amber._convert_to_csv([1.0, 2.0, 3.0]))

        # valid 2d inputs
        assert_equal("1.0,2.0,3.0,4.0", self.amber._convert_to_csv([[1, 2], [3, 4]]))
        assert_equal("1.0,2.0,3.0,4.0", self.amber._convert_to_csv([[1, 2, 3, 4]]))
        assert_equal("1.0,2.0,3.0,4.0", self.amber._convert_to_csv([[1], [2], [3], [4]]))
        assert_equal("1.0,2.0,3.0,4.0", self.amber._convert_to_csv([[1, 2], [3, 4.0]]))
        assert_equal("1.0,2.0,3.0,4.0", self.amber._convert_to_csv([[1.0, 2.0], [3.0, 4.0]]))

    def test_convert_to_csv_negative(self):
        # empty data
        assert_raises(ValueError, self.amber._convert_to_csv, [])
        assert_raises(ValueError, self.amber._convert_to_csv, [[]])
        assert_raises(ValueError, self.amber._convert_to_csv, [[], []])

        # non-numeric data
        assert_raises(ValueError, self.amber._convert_to_csv, None)
        assert_raises(ValueError, self.amber._convert_to_csv, 'a')
        assert_raises(ValueError, self.amber._convert_to_csv, 'abc')
        assert_raises(ValueError, self.amber._convert_to_csv, [1, None, 3])
        assert_raises(ValueError, self.amber._convert_to_csv, [1, 'a', 3])
        assert_raises(ValueError, self.amber._convert_to_csv, [1, 'abc', 3])
        assert_raises(ValueError, self.amber._convert_to_csv, [[1, None], [3, 4]])
        assert_raises(ValueError, self.amber._convert_to_csv, [[1, 'a'], [3, 4]])
        assert_raises(ValueError, self.amber._convert_to_csv, [[1, 'abc'], [3, 4]])

        # badly-shaped data
        assert_raises(ValueError, self.amber._convert_to_csv, [1, [2, 3], 4])            # mixed nesting
        assert_raises(ValueError, self.amber._convert_to_csv, [[1, 2], [3, 4, 5]])       # ragged array
        assert_raises(ValueError, self.amber._convert_to_csv, [[[1, 2, 3, 4]]])          # nested too deep
        assert_raises(ValueError, self.amber._convert_to_csv, [[[1], [2], [3], [4]]])


if __name__ == '__main__':
    argv = ['nosetests', '--verbosity=2']
    nose.run(defaultTest=__name__ + ':TestInit', argv=argv)
    nose.run(defaultTest=__name__ + ':TestAuth', argv=argv)
    nose.run(defaultTest=__name__ + ':TestAPICall', argv=argv)
    nose.run(defaultTest=__name__ + ':TestDataHandling', argv=argv)
    nose.run(defaultTest=__name__ + ':TestEndpoints', argv=argv)
