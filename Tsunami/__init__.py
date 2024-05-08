from Tsunami.ProjectLoader import ProjectLoader
from Tsunami.Downloader import Downloader
from Tsunami.Analyzer import Analyzer


def start_project(project_config_json_path):
    # Load configurations
    project = ProjectLoader(project_config_json_path)

    downloader = Downloader(
        project.get_project_config(),
        project.get_data_request_jobs()
    )

    analyzer = Analyzer(
        project.get_project_config(),
        project.get_analysis_requests()
    )

    return project, downloader, analyzer