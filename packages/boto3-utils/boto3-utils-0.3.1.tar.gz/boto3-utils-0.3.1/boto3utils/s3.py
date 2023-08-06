import boto3
import json
import hashlib
import hmac
import logging
import os
import os.path as op

from botocore.exceptions import ClientError
from copy import deepcopy
from datetime import datetime, timedelta
from gzip import GzipFile
from io import BytesIO
from os import makedirs, getenv
from shutil import rmtree
from tempfile import mkdtemp
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class s3(object):

    def __init__(self, session=None, requester_pays=False):
        self.requester_pays = requester_pays
        if session is None:
            self.s3 = boto3.client('s3')
        else:
            self.s3 = session.client('s3')

    @classmethod
    def urlparse(cls, url):
        """ Split S3 URL into bucket, key, filename """
        _url = deepcopy(url)
        if url[0:5] == 'https':
            _url = cls.https_to_s3(url)
        if _url[0:5] != 's3://':
            raise Exception('Invalid S3 url %s' % _url)

        url_obj = _url.replace('s3://', '').split('/')

        # remove empty items
        url_obj = list(filter(lambda x: x, url_obj))

        return {
            'bucket': url_obj[0],
            'key': '/'.join(url_obj[1:]),
            'filename': url_obj[-1] if len(url_obj) > 1 else ''
        }

    @classmethod
    def https_to_s3(cls, url):
        """ Convert https s3 URL to an s3 URL """
        parts = urlparse(url)
        bucket = parts.netloc.split('.')[0]
        s3url = f"s3://{bucket}{parts.path}"
        return s3url

    @classmethod
    def s3_to_https(cls, url, region=getenv('AWS_REGION', getenv('AWS_DEFAULT_REGION', 'us-east-1'))):
        """ Convert an s3 URL to an s3 https URL """    
        parts = cls.urlparse(url)
        return 'https://%s.s3.%s.amazonaws.com/%s' % (parts['bucket'], region, parts['key'])

    def exists(self, url):
        """ Check if this URL exists on S3 """
        parts = self.urlparse(url)
        try:
            self.s3.head_object(Bucket=parts['bucket'], Key=parts['key'])
            return True
        except ClientError as exc:
            if exc.response['Error']['Code'] != '404':
                raise
            return False

    def upload(self, filename, url, public=False, extra={}, http_url=False):
        """ Upload object to S3 uri (bucket + prefix), keeping same base filename """
        logger.debug("Uploading %s to %s" % (filename, url))
        parts = self.urlparse(url)
        url_out = 's3://%s' % op.join(parts['bucket'], parts['key'])
        if public:
            extra['ACL'] = 'public-read'
        with open(filename, 'rb') as data:
            self.s3.upload_fileobj(data, parts['bucket'], parts['key'], ExtraArgs=extra)
        if http_url:
            region = self.s3.get_bucket_location(Bucket=parts['bucket'])['LocationConstraint']
            return self.s3_to_https(url_out, region)
        else:
            return url_out

    def upload_json(self, data, url, extra={}, **kwargs):
        """ Upload dictionary as JSON to URL """
        tmpdir = mkdtemp()
        filename = op.join(tmpdir, 'catalog.json')
        _extra = {
            'ContentType': 'application/json'
        }
        _extra.update(extra)
        with open(filename, 'w') as f:
            f.write(json.dumps(data))
        try:
            self.upload(filename, url, extra=_extra, **kwargs)
        except Exception as err:
            logger.error(err)
        finally:
            rmtree(tmpdir)

    def get_object(self, bucket, key):
        """ Get an S3 object """
        if self.requester_pays:
            response = self.s3.get_object(Bucket=bucket, Key=key, RequestPayer='requester')
        else:
            response = self.s3.get_object(Bucket=bucket, Key=key)
        return response

    def download(self, uri, path=''):
        """
        Download object from S3
        :param uri: URI of object to download
        :param path: Output path
        """
        s3_uri = self.urlparse(uri)
        fout = op.join(path, s3_uri['filename'])
        logger.debug("Downloading %s as %s" % (uri, fout))
        if path != '':
            makedirs(path, exist_ok=True)
        extra_args = None
        if self.requester_pays:
            extra_args = {'RequestPayer': 'requester'}
        self.s3.download_file(s3_uri['bucket'], s3_uri['key'], fout, ExtraArgs=extra_args)
        return fout

    def read(self, url):
        """ Read object from s3 """
        parts = self.urlparse(url)
        response = self.get_object(parts['bucket'], parts['key'])
        body = response['Body'].read()
        if op.splitext(parts['key'])[1] == '.gz':
            body = GzipFile(None, 'rb', fileobj=BytesIO(body)).read()
        return body.decode('utf-8')

    def read_json(self, url):
        """ Download object from S3 as JSON """
        return json.loads(self.read(url))

    def delete(self, url):
        """ Remove object from S3 """
        parts = self.urlparse(url)
        response = self.s3.delete_object(Bucket=parts['Bucket'], Key=parts['Key'])
        return response

    # function derived from https://alexwlchan.net/2018/01/listing-s3-keys-redux/
    def find(self, url, suffix=''):
        """
        Generate objects in an S3 bucket.
        :param url: The beginning part of the URL to match (bucket + optional prefix)
        :param suffix: Only fetch objects whose keys end with this suffix.
        """
        parts = self.urlparse(url)
        kwargs = {'Bucket': parts['bucket']}

        # If the prefix is a single string (not a tuple of strings), we can
        # do the filtering directly in the S3 API.
        if isinstance(parts['key'], str):
            kwargs['Prefix'] = parts['key']

        while True:
            # The S3 API response is a large blob of metadata.
            # 'Contents' contains information about the listed objects.
            resp = self.s3.list_objects_v2(**kwargs)
            try:
                contents = resp['Contents']
            except KeyError:
                return

            for obj in contents:
                key = obj['Key']
                if key.startswith(parts['key']) and key.endswith(suffix):
                    yield f"s3://{parts['bucket']}/{obj['Key']}"

            # The S3 API is paginated, returning up to 1000 keys at a time.
            # Pass the continuation token into the next response, until we
            # reach the final page (when this field is missing).
            try:
                kwargs['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
                break

    def read_inventory_file(self, fname, keys, prefix=None, suffix=None, start_date=None, end_date=None, datetime_key='LastModifiedDate'):
        logger.debug('Reading inventory file %s' % (fname))
        
        inv = [{keys[i]: v for i, v in  enumerate(line.replace('"', '').split(','))} for line in self.read(fname).split('\n')]

        def fvalid(info):
            return True if 'Key' in info and 'Bucket' in info else False

        def fprefix(info):
            return True if info['Key'][:len(prefix)] == prefix else False

        def fsuffix(info):
            return True if info['Key'].endswith(suffix) else False

        def fstartdate(info):
            dt = datetime.strptime(info[datetime_key], "%Y-%m-%dT%H:%M:%S.%fZ").date()
            return True if dt > start_date else False

        def fenddate(info):
            dt = datetime.strptime(info[datetime_key], "%Y-%m-%dT%H:%M:%S.%fZ").date()
            return True if dt < end_date else False

        inv = filter(fvalid, inv)
        if prefix:
            inv = filter(fprefix, inv)
        if suffix:
            inv = filter(fsuffix, inv)
        if start_date:
            inv = filter(fstartdate, inv)
        if end_date:
            inv = filter(fenddate, inv)
        for i in inv:
            yield 's3://%s/%s' % (i['Bucket'], i['Key'])

    def latest_inventory_manifest(self, url):
        """ Get latest inventory manifest file """
        parts = self.urlparse(url)
        # get latest manifest file
        today = datetime.now()
        manifest_url = None
        for dt in [today, today - timedelta(1)]:
            _key = op.join(parts['key'], dt.strftime('%Y-%m-%d'))
            _url = 's3://%s/%s' % (parts['bucket'], _key)
            manifests = [k for k in self.find(_url, suffix='manifest.json')]
            if len(manifests) == 1:
                manifest_url = manifests[0]
                break
        if manifest_url:
            return self.read_json(manifest_url)
        else:
            return None

    def latest_inventory_files(self, url):
        bucket = self.urlparse(url)['bucket']
        manifest = self.latest_inventory_manifest(url)
        if manifest:
            files = manifest.get('files', [])
            numfiles = len(files)
            logger.info('Getting latest inventory from %s (%s files)' % (url, numfiles))            

            for f in files:
                _url = 's3://%s/%s' % (bucket, f['key'])
                yield _url

    def latest_inventory(self, url, **kwargs):
        """ Return generator function for objects in Bucket with suffix (all files if suffix=None) """
        bucket = self.urlparse(url)['bucket']
        manifest = self.latest_inventory_manifest(url)
        # read through latest manifest looking for matches
        if manifest:
            # get file schema
            keys = [str(key).strip() for key in manifest['fileSchema'].split(',')]

            for i, url in enumerate(self.latest_inventory_files(url)):
                logger.info('Reading inventory file %s' % (i+1))
                results = self.read_inventory_file(url, keys, **kwargs)
                yield from results


def get_presigned_url(url, aws_region=None,
                      rtype='GET', public=False, requester_pays=False, content_type=None):
    """ Get presigned URL """
    access_key = os.environ.get('AWS_BUCKET_ACCESS_KEY_ID', os.environ.get('AWS_ACCESS_KEY_ID'))
    secret_key = os.environ.get('AWS_BUCKET_SECRET_ACCESS_KEY', os.environ.get('AWS_SECRET_ACCESS_KEY'))
    region = os.environ.get('AWS_BUCKET_REGION', os.environ.get('AWS_REGION', 'eu-central-1'))
    if aws_region is not None:
        region = aws_region
    if access_key is None or secret_key is None:
        # if credentials not provided, just try to download without signed URL
        logger.debug('Not using signed URL for %s' % url)
        return url, None

    parts = s3.urlparse(url)
    bucket = parts['bucket']
    key = parts['key']

    service = 's3'
    host = '%s.%s.amazonaws.com' % (bucket, service)
    request_parameters = ''

    # Key derivation functions. See:
    # http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
    def sign(key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    def getSignatureKey(key, dateStamp, regionName, serviceName):
        kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
        kRegion = sign(kDate, regionName)
        kService = sign(kRegion, serviceName)
        kSigning = sign(kService, 'aws4_request')
        return kSigning
 
    # Create a date for headers and the credential string
    t = datetime.utcnow()
    amzdate = t.strftime('%Y%m%dT%H%M%SZ')
    datestamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope

    # create signed request and headers
    canonical_uri = '/' + key
    canonical_querystring = request_parameters

    payload_hash = 'UNSIGNED-PAYLOAD'
    headers = {
        'host': host,
        'x-amz-content-sha256': payload_hash,
        'x-amz-date': amzdate
    }

    if requester_pays:
        headers['x-amz-request-payer'] = 'requester'
    if public:
        headers['x-amz-acl'] = 'public-read'
    if os.environ.get('AWS_SESSION_TOKEN') and 'AWS_BUCKET_ACCESS_KEY_ID' not in os.environ:
        headers['x-amz-security-token'] = os.environ.get('AWS_SESSION_TOKEN')
    canonical_headers = '\n'.join('%s:%s' % (key, headers[key]) for key in sorted(headers)) + '\n'
    signed_headers = ';'.join(sorted(headers.keys()))

    canonical_request = '%s\n%s\n%s\n%s\n%s\n%s' % (
        rtype, canonical_uri, canonical_querystring, canonical_headers, signed_headers, payload_hash
    )
    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'
    string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
    signing_key = getSignatureKey(secret_key, datestamp, region, service)
    signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
    authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' \
        + 'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

    request_url = 'https://%s%s' % (host, canonical_uri)
    headers['Authorization'] = authorization_header
    if content_type is not None:
        headers['content-type'] = content_type
    return request_url, headers
