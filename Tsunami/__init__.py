from Tsunami.ProjectLoader import ProjectLoader
from Tsunami.Downloader import Downloader
from Tsunami.Analyzer import Analyzer
from Tsunami.RagGenerator import RAGGenerator


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

    rag_generator = RAGGenerator(
        project.get_project_config(),
        project.get_rag_creation_job()
    )

    return project, downloader, analyzer, rag_generator