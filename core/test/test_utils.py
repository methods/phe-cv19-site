import filecmp
import io
import os
import shutil
import tempfile

from contextlib import redirect_stdout

import boto3
from moto import mock_s3

from CMS.test.utils import MethodsTestCase
from core import utils


@mock_s3
class TestUtilsS3Upload(MethodsTestCase):

    # =================== # helpers # =================== #

    def _are_dir_trees_equal(self, dir1: str, dir2: str) -> bool:
        """
        Compare two directories recursively. Files in each directory are
        assumed to be equal if their names and contents are equal.

        Return True if the directory trees are the same and there were no
        errors while accessing the directories or files, False otherwise.

        Taken from: https://stackoverflow.com/questions/4187564
        """

        dirs_cmp = filecmp.dircmp(dir1, dir2)
        if (
            len(dirs_cmp.left_only) > 0
            or len(dirs_cmp.right_only) > 0
            or len(dirs_cmp.funny_files) > 0
        ):
            return False
        (_, mismatch, errors) = filecmp.cmpfiles(
            dir1, dir2, dirs_cmp.common_files, shallow=False
        )
        if len(mismatch) > 0 or len(errors) > 0:
            return False
        for common_dir in dirs_cmp.common_dirs:
            new_dir1 = os.path.join(dir1, common_dir)
            new_dir2 = os.path.join(dir2, common_dir)
            if not self._are_dir_trees_equal(new_dir1, new_dir2):
                return False
        return True

    @staticmethod
    def _write_html_file(file_name: str, dir_path: str) -> None:
        content = f""""
        <h1>{file_name}</h1>
        <div>{file_name}</div>
        """
        with open(os.path.join(dir_path, file_name), "w") as f:
            f.write(content)

    @staticmethod
    def _write_random_bin_file(file_name: str, dir_path: str) -> None:
        with open(os.path.join(dir_path, file_name), "wb") as f:
            f.write(os.urandom(1024))

    def _setup_test_directory(self, test_dir: str, include_non_html: bool=False) -> None:
        """
        Setup three-deep, trifurcating directory tree with unique pseudo-html
        files in each directory. If include_non_html=True, also include unique,
        random-content pseudo img files in each directory.
        """
        for lvl1_seed in range(1, 4):
            dirpath = os.path.join(test_dir, f"dir{lvl1_seed}")
            os.makedirs(dirpath, exist_ok=True)
            base_filename = lvl1_seed
            self._write_html_file(f"{base_filename}.html", dirpath)
            if include_non_html:
                self._write_random_bin_file(f"{base_filename}.not_jpg", dirpath)

            for lvl2_seed in range(1, 4):
                dirpath = os.path.join(test_dir, f"dir{lvl1_seed}", f"dir{lvl2_seed}")
                base_filename = f"{lvl1_seed}_{lvl2_seed}"
                os.makedirs(dirpath, exist_ok=True)
                self._write_html_file(f"{base_filename}.html", dirpath)
                if include_non_html:
                    self._write_random_bin_file(f"{base_filename}.not_jpg", dirpath)

                for lvl3_seed in range(1, 4):
                    dirpath = os.path.join(
                        test_dir,
                        f"dir{lvl1_seed}",
                        f"dir{lvl2_seed}",
                        f"dir{lvl3_seed}",
                    )
                    base_filename = f"{lvl1_seed}_{lvl2_seed}_{lvl3_seed}"
                    os.makedirs(dirpath, exist_ok=True)
                    self._write_html_file(f"{base_filename}.html", dirpath)
                    if include_non_html:
                        self._write_random_bin_file(f"{base_filename}.not_jpg", dirpath)

    def _s3_to_local_dir(self, local_dir: str) -> None:
        """
        Get objects from s3 bucket (mocked,  presumably) and replicate structure
        implied in key names as directory tree with root in local_dir.
        """
        bucket_keys = (object["Key"] for object in self.s3_client.list_objects(Bucket=self.mock_bucket)["Contents"])
        for s3_key in bucket_keys:
            # split s3_key into directory-like component and filename-like component
            path, filename = os.path.split(s3_key)
            local_dir_path = os.path.join(local_dir, path)
            local_file_path = os.path.join(local_dir, s3_key)
            # if there was a directory-like component, create that directory
            if bool(path):
                os.makedirs(local_dir_path, exist_ok=True)
            # download file to local_dir
            self.s3_client.download_file(
                Bucket=self.mock_bucket, Key=s3_key, Filename=local_file_path
            )

    # =================== # setup # =================== #

    def setUp(self):
        super().setUp()
        self.test_dir = tempfile.mkdtemp()
        self.backup_utils_settings = utils.settings
        self.mock_key_id = "mock-key-ID"
        self.mock_key = "mock-key"
        self.mock_bucket = "mock-bucket"
        self.mock_region = "eu-west-2"
        utils.settings.AWS_ACCESS_KEY_ID_DEPLOYMENT = self.mock_key_id
        utils.settings.AWS_SECRET_ACCESS_KEY_DEPLOYMENT = self.mock_key
        utils.settings.AWS_STORAGE_BUCKET_NAME_DEPLOYMENT = self.mock_bucket
        utils.settings.AWS_REGION_DEPLOYMENT = self.mock_region
        utils.settings.BUILD_DIR = self.test_dir
        self.s3_client = boto3.client(
            "s3",
            region_name=self.mock_region,
            aws_access_key_id=self.mock_key_id,
            aws_secret_access_key=self.mock_key,
        )
        self.s3_client.create_bucket(Bucket=self.mock_bucket)

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        utils.settings = self.backup_utils_settings

    # =================== # tests # =================== #

    def test_export_directory_html_only(self):
        """
        Assert export_directory uploads all files when just given html.
        """
        # setup test dir
        self._setup_test_directory(self.test_dir)

         # upload temp directory to mocked s3 bucket
        utils.export_directory()

        # assert mock bucket has correct files and directory structure
        with tempfile.TemporaryDirectory() as mock_bucket_contents_directory:
            self._s3_to_local_dir(mock_bucket_contents_directory)
            trees_equal =  self._are_dir_trees_equal(self.test_dir, mock_bucket_contents_directory)
            diff_report = ""
            if not trees_equal:
                # filecmp annoyingly likes to report to stdout, but we want the output as a string for the assert msg
                with io.StringIO() as buf, redirect_stdout(buf):
                    filecmp.dircmp(self.test_dir, mock_bucket_contents_directory).report_full_closure()
                    diff_report = "Directory tree in s3 bucket does not match test directory tree: " + buf.getvalue()
            self.assertTrue(trees_equal, diff_report)


    def test_export_directory_html_and_binaries(self):
        """
        Assert export_directory uploads only html when given a mix of html and binary image-like files.
        """
        # setup test dir
        self._setup_test_directory(self.test_dir, include_non_html=True)

        # upload temp directory to mocked s3 bucket
        utils.export_directory()

        # setup the same thing, without non-html
        with tempfile.TemporaryDirectory() as test_dir_html_only:

            self._setup_test_directory(test_dir_html_only)

            # assert mock bucket has ONLY the html files
            with tempfile.TemporaryDirectory() as mock_bucket_contents_directory:
                self._s3_to_local_dir(mock_bucket_contents_directory)
                trees_equal =  self._are_dir_trees_equal(test_dir_html_only, mock_bucket_contents_directory)
                diff_report = ""
                if not trees_equal:
                    # filecmp annoyingly likes to report to stdout, but we want the output as a string for the assert msg
                    with io.StringIO() as buf, redirect_stdout(buf):
                        filecmp.dircmp(test_dir_html_only, mock_bucket_contents_directory).report_full_closure()
                        diff_report = "Directory tree in s3 bucket does not match test directory tree: " + buf.getvalue()
                self.assertTrue(trees_equal, diff_report)




# test upload of modded files only
# test scheduled upload
