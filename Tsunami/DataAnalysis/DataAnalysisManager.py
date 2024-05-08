from Tsunami.DataAnalysis.DataAnalysisJob import DataAnalysisJob
from Tsunami.ProjectConfig import ProjectConfig
from Tsunami.ModelInterface import ModelInterface
from Tsunami.Utils.basicutils import *
from Tsunami.logger import log
from tqdm import tqdm
import os
import re



class DataAnalysisManager:
    def __init__(self, project_config: ProjectConfig):
        self.project_config = project_config
        self.model_interface = ModelInterface()  # Assuming this handles interaction with AI models
        self.compilation_delimiter = "\n\n\n ###\n### Next data:\n### \n\n\n"



    def execute_job(self, data_analysis_job: DataAnalysisJob):
        if self.project_config.continue_analysis:
            highest_level_dir = self.find_highest_level_directory()
            responses = self.read_responses_from_directory(highest_level_dir)
        else:
            file_paths = self.get_file_paths_to_analyze(data_analysis_job.excluded_directories)
            log(f"Analyzing {len(file_paths)} files...")
            responses = []
            for i, file_path in enumerate(tqdm(file_paths)):
                log(f"Analyzing file {i+1}/{len(file_paths)}")
                log(f"File path: '{file_path}'")
                content = get_chars_from_file(file_path)
                response_text, _ = self.model_interface.send_to_ai(
                    data_analysis_job.doc_analysis_prompt + "\n\n" + content,
                    model=data_analysis_job.doc_analysis_model
                )
                responses.append(response_text)

        # Handle compilation of responses
        self.handle_compilations(responses, data_analysis_job)



    def find_highest_level_directory(self):
        analysis_dir = self.project_config.data_analysis_directory
        dirs = [d for d in os.listdir(analysis_dir) if os.path.isdir(os.path.join(analysis_dir, d))]
        level_dirs = [d for d in dirs if re.match(r'level_\d+', d)]
        if not level_dirs:
            return None
        highest_level = max([int(d.split('_')[1]) for d in level_dirs])
        return os.path.join(analysis_dir, f"level_{highest_level}")



    def read_responses_from_directory(self, directory):
        responses = []
        if directory and os.path.exists(directory):
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        responses.append(file.read())
        return responses



    def handle_compilations(self, responses, data_analysis_job : DataAnalysisJob):
        level = 0
        while len(responses) > data_analysis_job.max_compilations_per_final_report:
            grouped_responses = [responses[i:i + data_analysis_job.max_docs_per_compilation]
                                 for i in range(0, len(responses), data_analysis_job.max_docs_per_compilation)]
            compiled_responses = []
            for group in grouped_responses:
                compiled_response, metrics = self.model_interface.send_to_ai(
                    data_analysis_job.doc_report_compilation_prompt + "\n\n" + self.compilation_delimiter.join(group),
                    model=data_analysis_job.recursive_compilation_model
                )
                compiled_responses.append(compiled_response)
            responses = compiled_responses
            level += 1
            # Save each compilation
            for i, response in enumerate(compiled_responses):
                save_chars_as_file(response, f"{self.project_config.data_analysis_directory}/level_{level}/{i}.txt")

        # Final compilation
        compiled_responses = self.compilation_delimiter.join(responses)
        final_report, metrics = self.model_interface.send_to_ai(
            data_analysis_job.final_report_prompt + "\n\n" + compiled_responses,
            model=data_analysis_job.final_report_model
        )
        save_chars_as_file(final_report, f"{self.project_config.workspace_directory}/final_report.txt")



    def get_file_paths_to_analyze(self, excluded_directories):
        root_dir = f"{self.project_config.data_download_directory}"
        file_paths = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            dirnames[:] = [d for d in dirnames if os.path.join(dirpath, d) not in excluded_directories] # wont properly identify excluded top level dirs
            for filename in filenames:
                file_paths.append(dirpath + "/" + filename)
        return file_paths

