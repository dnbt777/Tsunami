import time
from Tsunami.Metrics.CostTracker import CostTracker

class ProjectConfig():
    def __init__(self, workspace=None, cost_tracker=None, continue_analysis=False, **kwargs):
        if not workspace:
            workspace = str(round(time.time()))
        self.workspace_directory = f"workspaces/{workspace}"
        self.data_download_directory = f"{self.workspace_directory}/data_downloads"
        self.data_analysis_directory = f"{self.workspace_directory}/data_anaysis"
        self.rag_directory = f"{self.workspace_directory}/rag_analysis"
        self.continue_analysis = continue_analysis # Continues an analysis from the deepest level found - use for broken analyses
        
        if not cost_tracker:
            self.cost_tracker=CostTracker()
        else:
            self.cost_tracker=cost_tracker
        
        # Cover any other misc kwargs
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
        