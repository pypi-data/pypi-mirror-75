import json
import os
import glob
from blyzer.common.video import AnnotatedVideo

"""
    blzprj-file structure:
    {
        "meta":
            {
                "name":"<Project name>",
                "version":1
                "auto_scan":False
            },
        "videos":
            [
                {
                    "video_path":"<relative if near blzprj>",
                    "raw_annotation":<relative if near blzprj>"
                },
                {...}
            ]
    }
"""

CONFIG_FILE_EXTENSION = '.blzprj'

class BlyzerProject():
    def __init__(self, project_path: str):
        if not os.path.isfile(project_path):
            raise ValueError("Project path should be file")
        if not project_path.endswith(CONFIG_FILE_EXTENSION):
            raise ValueError("Wrong extention")
        self._project_dir = os.path.dirname(project_path)
        self._project_path = project_path
        self.load()
        self._videos_in_folders = []
        self._full_processed_videos = []
        self.rescan_folder()

    def add_video_source(self, source):
        pass

    def save(self):
        BlyzerProject._save(self._project_path, self._project_configuration)

    def load(self):
        with open(self._project_path, 'r', encoding='utf-8') as file:
            self._project_configuration = json.load(file)

    def get_video_count(self) -> int:
        count = len(self._project_configuration["videos"]) + len(self._videos_in_folders)
        return count

    def get_video_base_info(self, index: int) -> str:
        """
        For now similar to the path
        """
        name = None
        progress = 0.0
        if index >= self.get_video_count():
            return None

        if index < len(self._project_configuration["videos"]):
            name = self._project_configuration["videos"][index]["video_path"]
        else:
            f_index = index - len(self._project_configuration["videos"])
            name = self._videos_in_folders[f_index]

        if name in self._full_processed_videos:
            progress = 1.0
        else:
            v = self.get_video(index)
            progress = v.get_progress()

        if progress == 1.0:
            self._full_processed_videos.append(name)

        return name, progress

    def get_video(self, index: int) -> AnnotatedVideo:
        if index >= self.get_video_count():
            return None

        ret_val = None

        if  index < len(self._project_configuration["videos"]):
            video_desc = self._project_configuration["videos"][index]

            if os.path.isabs(video_desc["video_path"]):
                ret_val = AnnotatedVideo(video_desc["video_path"], video_desc["raw_annotation"])
            else:
                ret_val = AnnotatedVideo(os.path.join(self._project_dir,
                                                      video_desc["video_path"]),
                                         os.path.join(self._project_dir,
                                                      video_desc["raw_annotation"]))
        else:
            index -= len(self._project_configuration["videos"])
            video_path = self._videos_in_folders[index]
            if os.path.isabs(video_path):
                ret_val = AnnotatedVideo(video_path)
            else:
                ret_val = AnnotatedVideo(os.path.join(self._project_dir, video_path))
        return ret_val

    def get_project_name(self) -> str:
        return self._project_configuration['meta']['name']

    def get_model_path(self) -> str:
        m_path = self._project_configuration['meta']['model_path']
        if not os.path.isabs(m_path):
            m_path = os.path.join(self._project_dir, m_path)
        return m_path

    def add_video_obj(self, video: AnnotatedVideo):
        raise NotImplementedError()

    def add_video_folder(self, folder_path: str):
        status = False
        if self._check_relativity(folder_path):
            folder_path = os.path.relpath(folder_path, self._project_dir)
        if folder_path not in self._project_configuration["video_folders"]:
            self._project_configuration["video_folders"].append(folder_path)
            status = True
            self.save()
            self.rescan_folder()
        return status

    def add_video_path(self, video_path: str, annotation_path: str = None) -> bool:
        status = False
        if self._check_relativity(video_path):
            video_path = os.path.relpath(video_path, self._project_dir)
        if (annotation_path is not None) and self._check_relativity(annotation_path):
            annotation_path = os.path.relpath(annotation_path, self._project_dir)

        if not self._check_duplicates(video_path):
            video = {}
            video["video_path"] = video_path
            if annotation_path is None:
                video["raw_annotation"] = os.path.splitext(video_path)[0] + '.json'
            else:
                video["raw_annotation"] = annotation_path
            self._project_configuration["videos"].append(video)
            status = True
            self.save()
        return status

    def rescan_folder(self, force=False):
        """
        Rescan folders
        """
        if force:
            self._videos_in_folders = []

        for folder in self._project_configuration["video_folders"]:
            files = []
            if os.path.isabs(folder):
                files = glob.glob(folder + '/*.mp4')
            else:
                f = os.path.join(self._project_dir, folder)
                files_abs = glob.glob(f + '/*.mp4')
                for file_name in files_abs:
                    files.append(os.path.relpath(file_name, self._project_dir))
            for file_name in files:
                if file_name not in self._videos_in_folders:
                    self._videos_in_folders.append(file_name)

    def _check_duplicates(self, video_path: str) -> bool:
        for video in self._project_configuration['videos']:
            if video_path == video["video_path"]:
                return True
        return False

    def _check_relativity(self, path) -> bool:
        return os.path.commonprefix([path, self._project_dir]) == self._project_dir

    @staticmethod
    def _save(path: str, data):
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file)

    @staticmethod
    def create_project(project_dir: str,
                       project_name: str,
                       model_path: str,
                       project_version=1) -> str:
        if not os.path.isdir(project_dir):
            raise ValueError("Project path should be directory")

        if os.path.commonprefix([model_path, project_dir]) == project_dir:
            model_path = os.path.relpath(model_path, project_dir)
        project_configuration = {}
        project_configuration['meta'] = {}
        project_configuration['meta']['name'] = project_name
        project_configuration['meta']['model_path'] = model_path
        project_configuration['meta']['version'] = project_version
        project_configuration['meta']['auto_scan'] = False
        project_configuration['videos'] = []
        project_configuration['video_folders'] = []

        cnf_path = os.path.join(project_dir, project_name+CONFIG_FILE_EXTENSION)
        BlyzerProject._save(cnf_path, project_configuration)

        return cnf_path
