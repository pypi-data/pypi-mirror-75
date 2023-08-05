"""
MIT License
Copyright (c) 2020 williamfzc
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from minadb import ADBDevice
from loguru import logger
import requests
import typing
import time
import psutil
import pathlib
import tempfile
import shutil

__PROJECT_NAME__ = r"cort_client"
__AUTHOR__ = r"williamfzc"
__AUTHOR_EMAIL__ = r"fengzc@vip.qq.com"
__LICENSE__ = r"MIT"
__VERSION__ = r"0.3.1"


class CortJob(object):
    def __init__(self, product_name: str, user_name: str, *_, **__):
        self.product_name = product_name
        self.user_name = user_name

        # build this job
        self.package_name = self.get_package_name()
        self.version_name = self.get_version_name()
        self.hash_name = self.get_hash_name()
        logger.info(
            f"job generated: {self.product_name} / {self.package_name} / {self.version_name} / {self.hash_name}"
        )

    def get_package_name(self) -> str:
        raise NotImplementedError

    def get_version_name(self) -> str:
        raise NotImplementedError

    def get_hash_name(self) -> str:
        raise NotImplementedError


class _JobExecutor(object):
    def __init__(self, cli: "_BaseClient"):
        self.host = cli.host
        self.port = cli.port

    def start(self, job: CortJob, *args, **kwargs) -> psutil.Process:
        raise NotImplementedError


class AndroidJobExecutor(_JobExecutor):
    def start(self, job: CortJob, *args, **kwargs) -> psutil.Process:
        serial_no = kwargs.pop("serial_no", default="")
        assert serial_no, "no `serial_no` found in kwargs"
        # ok
        device = ADBDevice(serial_no)

        command = [
            "am",
            "instrument",
            "-w",
            "-r",
            # required
            "-e",
            "coverage",
            "true",
            "-e",
            "debug",
            "false",
            "-e",
            "class",
            f"{job.package_name}.CortInstrumentedTest",
            # optional
            # product name
            "-e",
            "productName",
            job.product_name,
            # package name
            "-e",
            "packageName",
            job.package_name,
            # version name
            "-e",
            "versionName",
            job.version_name,
            # hash name
            "-e",
            "hashName",
            job.hash_name,
            # user name
            "-e",
            "userName",
            job.user_name,
            # serial no
            "-e",
            "serialNo",
            serial_no,
            # host
            "-e",
            "host",
            self.host,
            # port
            "-e",
            "port",
            str(self.port),
            # file type (android things)
            "-e",
            "fileType",
            "ec",
            # step (period)
            "-e",
            "step",
            # todo: now locked
            str(5000),
            # runner
            f"{job.package_name}.test/{job.package_name}.CortTestRunner",
        ]
        logger.debug(f"job start with command: {command}")
        process = device.shell(command, no_wait=True)
        return psutil.Process(process.pid)
        # todo: test will never stop by default. need a cleanup here


class CortAPI(object):
    METHOD_GET = "GET"
    METHOD_POST = "POST"

    _METHOD_MAP = {METHOD_GET: requests.get, METHOD_POST: requests.post}
    # fill these
    method_name: typing.Union[METHOD_GET, METHOD_POST]
    path: str

    @property
    def method(self) -> typing.Callable[..., requests.Response]:
        return self._METHOD_MAP[self.method_name]


class ProviderArtifactAPI(CortAPI):
    method_name = CortAPI.METHOD_GET
    path = "/artifact"


class ProviderSessionSyncAPI(CortAPI):
    method_name = CortAPI.METHOD_POST
    path = "/session/sync"


class ProviderJobStatusAPI(CortAPI):
    method_name = CortAPI.METHOD_GET
    path = "/rq"


class ProviderSessionQueryAPI(CortAPI):
    method_name = CortAPI.METHOD_GET
    path = "/session/query"


class ProviderSessionNewAPI(CortAPI):
    method_name = CortAPI.METHOD_POST
    path = "/session/new"


class ReceiverUploadArtifact(CortAPI):
    method_name = CortAPI.METHOD_POST
    path = "/upload/artifact"


class ReceiverUploadCov(CortAPI):
    method_name = CortAPI.METHOD_POST
    path = "/upload/cov"


class CortAPIError(BaseException):
    pass


class _BaseClient(object):
    def __init__(self, host: str, port: int):
        # server
        self.host = host
        self.port = port
        self.base_url = f"http://{self.host}:{self.port}"
        self.ver = "v1"
        # api
        # provider
        self.api_provider_artifact = ProviderArtifactAPI()
        self.api_provider_job_status = ProviderJobStatusAPI()
        self.api_provider_session_sync = ProviderSessionSyncAPI()
        self.api_provider_session_query = ProviderSessionQueryAPI()
        self.api_provider_session_new = ProviderSessionNewAPI()
        # receiver
        self.api_receiver_upload_artifact = ReceiverUploadArtifact()
        self.api_receiver_upload_cov = ReceiverUploadCov()

    def heartbeat(self) -> bool:
        try:
            return requests.get(f"{self.base_url}/").ok
        except requests.exceptions.BaseHTTPError:
            return False

    def exec_api(self, api: CortAPI, *args, **kwargs) -> requests.Response:
        url = f"{self.base_url}/api/{self.ver}{api.path}"
        logger.debug(f"exec api: {url}")
        return api.method(url, *args, **kwargs)

    @staticmethod
    def handle_resp(resp: requests.Response) -> typing.Union[str, dict, list]:
        logger.debug(f"response: {resp.text}")
        if resp.ok:
            return resp.json()
        raise CortAPIError(resp.text)


class _JobLayer(_BaseClient):
    class JobStatus(object):
        def __init__(self, status: str, result: dict):
            self.status = status
            self.result = result

        def ok(self) -> bool:
            return self.status == "finished"

        def __str__(self):
            return f"CortJobStatus: status={self.status}; result={self.result}"

        __repr__ = __str__

    def new_job(
        self,
        job_kls: typing.Type[CortJob],
        product_name: str,
        user_name: str,
        *args,
        **kwargs,
    ) -> CortJob:
        return job_kls(product_name, user_name, *args, **kwargs)

    def job_status(self, job_id: str) -> JobStatus:
        resp = self.exec_api(self.api_provider_job_status, params={"job_id": job_id})
        result = self.handle_resp(resp)
        # error happened
        if not isinstance(result, dict):
            raise CortAPIError(result)
        return self.JobStatus(**self.handle_resp(resp))

    def wait_job_until_done(self, job_id: str, step: int = 1) -> JobStatus:
        status = self.job_status(job_id)
        if not status.ok():
            time.sleep(step)
            return self.wait_job_until_done(job_id)
        return status


class _SessionLayer(_BaseClient):
    def sync_session(self, session_id: str, **kwargs) -> str:
        resp = self.exec_api(
            self.api_provider_session_sync, data={"session_id": session_id, **kwargs}
        )
        return self.handle_resp(resp)

    def query_session(self, **kwargs) -> dict:
        resp = self.exec_api(self.api_provider_session_query, params=kwargs)
        return self.handle_resp(resp)

    def new_session(self, **kwargs) -> str:
        resp = self.exec_api(self.api_provider_session_new, data=kwargs)
        return self.handle_resp(resp)


class _ArtifactLayer(_BaseClient):
    def query_artifact(self, **kwargs) -> typing.Union[list, dict]:
        resp = self.exec_api(self.api_provider_artifact, params=kwargs)
        return self.handle_resp(resp)


class _ReceiverLayer(_BaseClient):
    @staticmethod
    def _str2path(path_like: typing.Union[str, pathlib.Path]) -> pathlib.Path:
        if isinstance(path_like, pathlib.Path):
            return path_like
        return pathlib.Path(path_like)

    def _read_data(self, file_path: typing.Union[str, pathlib.Path]) -> bytes:
        file_path = self._str2path(file_path)
        # can be a zip file or a directory
        # dir?
        if file_path.is_dir():
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_dir_path = pathlib.Path(temp_dir)
                archive_path = shutil.make_archive(
                    (temp_dir_path / "archive").as_posix(),
                    "zip",
                    root_dir=file_path.as_posix(),
                )
                logger.info(f"zip {file_path} to {archive_path}")
                with open(archive_path, "rb") as f:
                    data = f.read()
        elif file_path.is_file():
            with open(file_path.as_posix(), "rb") as f:
                data = f.read()
        else:
            raise FileNotFoundError(file_path)
        return data

    def upload_artifact(self, file_path: typing.Union[str, pathlib.Path], **kwargs):
        data = self._read_data(file_path)
        resp = self.exec_api(
            self.api_receiver_upload_artifact, files={"file": data}, data=kwargs,
        )
        return self.handle_resp(resp)

    def upload_cov(self, file_path: typing.Union[str, pathlib.Path], **kwargs):
        data = self._read_data(file_path)
        resp = self.exec_api(
            self.api_receiver_upload_cov, files={"file": data}, data=kwargs,
        )
        return self.handle_resp(resp)


class _ExecLayer(_BaseClient):
    def exec_job(
        self, executor_cls: typing.Type[_JobExecutor], job: CortJob, *args, **kwargs
    ) -> psutil.Process:
        executor = executor_cls(self)
        return executor.start(job, *args, **kwargs)


class CortClient(_JobLayer, _SessionLayer, _ArtifactLayer, _ReceiverLayer, _ExecLayer):
    pass


__all__ = [
    "CortClient",
    "CortJob",
]
