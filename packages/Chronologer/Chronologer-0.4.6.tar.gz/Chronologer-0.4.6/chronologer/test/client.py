import io
import json
import time
import queue
import unittest
import itertools
import logging.config
import logging.handlers
from unittest import mock
from http import HTTPStatus
from urllib.response import addinfourl
from urllib.request import build_opener, HTTPHandler, HTTPBasicAuthHandler

from . import bootstrap, warntoexc
from ..client import QueueProxyHandler, BatchJsonHandler


def setUpModule():
  warntoexc()
  bootstrap()


class DummyBufferHandler(logging.handlers.BufferingHandler):

  flushed = None


  def flush(self):
    self.acquire()
    try:
      if not self.flushed:
        self.flushed = []

      self.flushed.extend(self.buffer)
      self.buffer.clear()
    finally:
      self.release()


class TestQueueProxyHandler(unittest.TestCase):

  testee = None
  logger = None


  def setUp(self):
    q = queue.Queue(8)
    self.testee = QueueProxyHandler(q, DummyBufferHandler, capacity = 1024)

    self.logger = logging.getLogger(__name__)
    self.logger.setLevel(logging.INFO)
    self.logger.propagate = False
    self.logger.handlers = [self.testee]

  def tearDown(self):
    # atexit logging handler would fail otherwise as testee.close is not reentrant
    for wr in logging._handlerList:
      if wr() is self.testee:
        logging._removeHandlerRef(wr)

  def testLog(self):
    self.logger.info('Foo %s', 'bar', extra = {'struct': 'LOL'})

    self.testee.queue.join()
    self.assertEqual(1, len(self.testee._listener.handlers[0].buffer))

    record = self.testee._listener.handlers[0].buffer[0]
    self.assertEqual('INFO', record.levelname)
    self.assertEqual('Foo bar', record.message)
    self.assertEqual('LOL', record.struct)

  def testLogQueueFull(self):
    self.testee._listener.stop()
    for _ in range(8):
      self.logger.info('Excessive logging', extra = {'struct': 'LOL'})

    with mock.patch('logging.sys.stderr') as m:
      self.logger.info('Excessive logging', extra = {'struct': 'LOL'})
    message = ''.join(v[0][0] for v in m.write.call_args_list)
    self.assertIn('queue.Full', message)
    self.assertIn('Excessive logging', message)

    self.testee._listener.start()

  def testLoggerNamePrefix(self):
    testee = QueueProxyHandler(
      self.testee.queue, logging.handlers.BufferingHandler, capacity = 8, prefix = 'appname')
    self.logger.handlers = [testee]
    self.logger.warning('Logging NIH')

    self.testee.queue.join()
    self.assertEqual(1, len(self.testee._listener.handlers[0].buffer))

    record = self.testee._listener.handlers[0].buffer[0]
    self.assertEqual('appname.chronologer.test.client', record.name)

  def testLoggerNameSuffix(self):
    testee = QueueProxyHandler(
      self.testee.queue, logging.handlers.BufferingHandler, capacity = 8, prefix = 'appname')
    self.logger.handlers = [testee]
    self.logger.warning('Logging NIH', extra = {'suffix': 'classname'})

    self.testee.queue.join()
    self.assertEqual(1, len(self.testee._listener.handlers[0].buffer))

    record = self.testee._listener.handlers[0].buffer[0]
    self.assertEqual('appname.chronologer.test.client.classname', record.name)

  def testQueueAsNonConvertedFactory(self):
    configurator = logging.config.DictConfigurator({'()': 'queue.Queue', 'maxsize': 8})
    q = configurator.config
    self.testee = QueueProxyHandler(q, logging.handlers.BufferingHandler, capacity = 1024)
    self.logger = logging.getLogger(__name__)
    self.logger.setLevel(logging.INFO)
    self.logger.propagate = False
    self.logger.handlers = [self.testee]

    self.logger.info('Foo %s', 'bar', extra = {'struct': 'LOL'})

    self.testee.queue.join()
    self.assertEqual(1, len(self.testee._listener.handlers[0].buffer))

    record = self.testee._listener.handlers[0].buffer[0]
    self.assertEqual('INFO', record.levelname)
    self.assertEqual('Foo bar', record.message)
    self.assertEqual('LOL', record.struct)

  def testClose(self):
    for _ in range(7):
      self.logger.info(
        'Back in the times of Misunderstood it was a thing...')

    self.assertEqual(0, len(self.testee._listener.handlers[0].buffer))
    self.testee.close()
    self.assertIsNone(self.testee._listener._thread)

    self.assertEqual(7, len(self.testee._listener.handlers[0].flushed))

  def testCloseLogQueueFull(self):
    for i in range(8):
      self.logger.warning('Record {}'.format(i))

    self.assertEqual(0, len(self.testee._listener.handlers[0].buffer))
    with mock.patch('logging.sys.stderr') as m:
      self.testee.close()
    message = ''.join(v[0][0] for v in m.write.call_args_list)
    self.assertIn('queue.Full', message)
    self.assertIn('Record 0', message)

    # The result of the queue is processes normally
    self.assertEqual(7, len(self.testee._listener.handlers[0].flushed))


class MockHttpHandler(HTTPHandler):

  requests = None

  statuses = itertools.repeat(HTTPStatus.OK)


  def __init__(self, debuglevel = 0):
    super().__init__(debuglevel)

    self.requests = []

  def http_open(self, req):
    self.requests.append(req)

    status = next(self.statuses)
    res = addinfourl(io.BytesIO(), headers = {}, url = req.get_full_url(), code = status.value)
    res.msg = status.phrase
    return res


class TestBatchJsonHandler(unittest.TestCase):

  testee = None
  logger = None

  mockHandler = None


  def setUp(self):
    self.testee = BatchJsonHandler(
      capacity              = 8,
      host                  = 'localhost',
      url                   = '/does/not/matter',
      flushLevel            = logging.WARN,
      flushTimeout          = 0.1,
      flushTimeoutWatcher   = False,
      credentials           = ('foo', 'bar'),
      secure                = False,
      requestAttemptLimit   = 2,
      requestAttemptDelayFn = lambda _i: 0.01
    )
    self.mockHandler = MockHttpHandler()
    self.testee._origurlopener = self.testee._urlopener
    self.testee._urlopener = build_opener(self.mockHandler)

    self.logger = logging.getLogger(__name__)
    self.logger.setLevel(logging.INFO)
    self.logger.propagate = False
    self.logger.handlers = [self.testee]

  def assertFlush(self, size):
    self.assertEqual(1, len(self.mockHandler.requests))
    req = self.mockHandler.requests[0]
    self.assertEqual('http://localhost/does/not/matter', req.full_url)

    lines = req.data.decode().splitlines()
    self.assertEqual(size, len(lines))
    for i, l in enumerate(lines):
      recordDict = json.loads(l)
      self.assertEqual('chronologer.test.client', recordDict['name'])
      self.assertEqual('LOL', recordDict['struct'])
      self.assertEqual('Buffer size {}'.format(i + 1), recordDict['msg'])

  def testFlushBuffer(self):
    for i in range(8):
      self.logger.info('Buffer size {}'.format(i + 1), extra = {'struct': 'LOL'})

    self.assertFlush(8)

  def testFlushTimeout(self):
    for i in range(6):
      self.logger.info('Buffer size {}'.format(i + 1), extra = {'struct': 'LOL'})
    self.assertEqual(0, len(self.mockHandler.requests))

    time.sleep(0.1)

    self.logger.info('Buffer size {}'.format(i + 2), extra = {'struct': 'LOL'})
    self.assertFlush(7)

  def testFlushTimeoutWatcher(self):
    testee = BatchJsonHandler(
      capacity            = 8,
      host                = 'localhost',
      url                 = '/does/not/matter',
      flushLevel          = logging.WARN,
      flushTimeout        = 0.1,
      flushTimeoutWatcher = True,
      credentials         = ('foo', 'bar'),
    )
    testee._urlopener = build_opener(self.mockHandler)
    self.logger.handlers = [testee]

    for i in range(6):
      self.logger.info('Buffer size {}'.format(i + 1), extra = {'struct': 'LOL'})
    self.assertEqual(0, len(self.mockHandler.requests))
    self.assertEqual(6, len(testee.buffer))

    time.sleep(0.15)

    try:
      self.assertFlush(6)
    finally:
      testee.close()

  def testFlushLevel(self):
    for i in range(6):
      self.logger.info('Buffer size {}'.format(i + 1), extra = {'struct': 'LOL'})
    self.assertEqual(0, len(self.mockHandler.requests))

    self.logger.warning('Buffer size {}'.format(i + 2), extra = {'struct': 'LOL'})
    self.assertFlush(7)

  def testFlushEmpty(self):
    self.testee.close()
    self.assertEqual(0, len(self.mockHandler.requests))

  def testRetrySuccess(self):
    self.mockHandler.statuses = iter([HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.OK])

    with mock.patch('logging.sys.stderr') as m:
      for i in range(8):
        self.logger.info('Buffer size {}'.format(i + 1), extra = {'struct': 'LOL'})

    message = ''.join(v[0][0] for v in m.write.call_args_list)
    self.assertIn('Batch-flush error, retrying in 0.01s', message)
    self.assertIn('urllib.error.HTTPError: HTTP Error 500: Internal Server Error', message)

    self.assertEqual(2, len(self.mockHandler.requests))
    self.assertEqual(self.mockHandler.requests[0].full_url, self.mockHandler.requests[1].full_url)
    self.assertEqual(self.mockHandler.requests[0].data, self.mockHandler.requests[1].data)

    req = self.mockHandler.requests[1]
    self.assertEqual('http://localhost/does/not/matter', req.full_url)

    lines = req.data.decode().splitlines()
    self.assertEqual(8, len(lines))
    for i, l in enumerate(lines):
      recordDict = json.loads(l)
      self.assertEqual('chronologer.test.client', recordDict['name'])
      self.assertEqual('LOL', recordDict['struct'])
      self.assertEqual('Buffer size {}'.format(i + 1), recordDict['msg'])

  def testRetryRunOut(self):
    self.mockHandler.statuses = itertools.repeat(HTTPStatus.INTERNAL_SERVER_ERROR, 2)

    with mock.patch('logging.sys.stderr') as m:
      for i in range(8):
        self.logger.info('Buffer size {}'.format(i + 1), extra = {'struct': 'LOL'})

    message = ''.join(v[0][0] for v in m.write.call_args_list)
    self.assertIn('Batch-flush error, retrying in 0.01s', message)
    self.assertIn('Batch-flush error, flushing buffer into stderr', message)
    self.assertEqual(2, message.count('HTTPError: HTTP Error 500: Internal Server Error'))

    lines = message.splitlines()[-8:]
    self.assertEqual(8, len(lines))
    for i, l in enumerate(lines):
      recordDict = json.loads(l)
      self.assertEqual('chronologer.test.client', recordDict['name'])
      self.assertEqual('LOL', recordDict['struct'])
      self.assertEqual('Buffer size {}'.format(i + 1), recordDict['msg'])

  def testRetryOnClientError(self):
    self.mockHandler.statuses = iter([HTTPStatus.BAD_REQUEST])

    with mock.patch('logging.sys.stderr') as m:
      self.logger.warning('Non-retriable')

    self.assertEqual(1, len(self.mockHandler.requests))

    message = ''.join(v[0][0] for v in m.write.call_args_list)
    self.assertEqual(1, message.count('HTTPError: HTTP Error 400: Bad Request'))

  def testNoAuthResetOnErrorForNextRequest(self):
    self.mockHandler.statuses = iter(
      [HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.OK]
    )

    origAuthHandler = [
      h for h in self.testee._origurlopener.handlers if isinstance(h, HTTPBasicAuthHandler)
    ][0]
    self.testee._urlopener = build_opener(origAuthHandler, self.mockHandler)
    self.testee.flushLevel = logging.INFO

    with mock.patch('logging.sys.stderr') as m:
      self.logger.info('Retry failed')
    self.logger.warning('Deep state')

    message = ''.join(v[0][0] for v in m.write.call_args_list)
    self.assertIn('Batch-flush error, retrying in 0.01s', message)
    self.assertIn('Batch-flush error, flushing buffer into stderr', message)
    self.assertEqual(2, message.count('HTTPError: HTTP Error 500: Internal Server Error'))

    self.assertEqual(3, len(self.mockHandler.requests))
    for req in self.mockHandler.requests:
      self.assertEqual('Basic Zm9vOmJhcg==', req.get_header('Authorization'))

