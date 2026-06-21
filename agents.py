import pandas as pd
import json
import io  # <--- ADD THIS LINE
class IngestionAgent:
    """Specialized agent to collect data automatically from CSV or JSON sources."""
    def run(self, file_path):
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            return df.to_json(orient="records"), "CSV Data Ingested Successfully."
        elif file_path.endswith('.json'):
            with open(file_path, 'r') as f:
                data = json.load(f)
            return json.dumps(data), "JSON Data Ingested Successfully."
        else:
            raise ValueError("Unsupported format! System only accepts CSV or JSON.")

class ValidationAgent:
    """Specialized agent to ensure data quality and perform autonomous self-healing."""
    def run(self, json_data):
        # Wrap json_data in io.StringIO to prevent path errors
        df = pd.read_json(io.StringIO(json_data))
        
        # Calculate initial anomalies/missing values
        missing_count = df.isnull().sum().to_dict()
        status = "Healthy"
        
        # Autonomous Self-Healing Logic: Find numeric columns with missing values and patch them
        fixed_columns = []
        for col in df.select_dtypes(include=['number']).columns:
            if df[col].isnull().any():
                df[col] = df[col].fillna(0)  # Self-healing action: replace NaN with 0
                fixed_columns.append(col)
                status = "Self-Healed Anomalies Automatically"

        report = {
            "total_records": len(df),
            "missing_values_detected": missing_count,
            "patched_columns": fixed_columns,
            "status": status
        }
        return df.to_json(orient="records"), report

class TransformationAgent:
    """Specialized agent to standardize and prepare schemas for downstream processing."""
    def run(self, json_data):
        # Wrap json_data in io.StringIO to prevent path errors
        df = pd.read_json(io.StringIO(json_data))
        
        # Schema standardization: convert columns to lowercase and replace spaces with underscores
        df.columns = [str(col).lower().strip().replace(" ", "_") for col in df.columns]
        return df

class AgenticOrchestrator:
    """The central management layer that allocates tasks and maintains tracking logs."""
    def __init__(self):
        self.ingestion = IngestionAgent()
        self.validation = ValidationAgent()
        self.transformation = TransformationAgent()
        self.logs = []

    def log_step(self, message):
        self.logs.append(message)

    def execute_pipeline(self, file_path):
        try:
            self.log_step("🤖 Pipeline triggered by Central Orchestrator.")
            
            # 1. Ingestion Stage
            raw_json, ingest_msg = self.ingestion.run(file_path)
            self.log_step(f"✅ Ingestion Agent: {ingest_msg}")
            
            # 2. Validation & Self-Healing Stage
            clean_json, val_report = self.validation.run(raw_json)
            self.log_step(f"✅ Validation Agent: Quality check completed. Status: [{val_report['status']}]")
            if val_report['patched_columns']:
                self.log_step(f"⚠️ Self-Healing Action: Fixed null fields in columns: {val_report['patched_columns']}")
            
            # 3. Transformation Stage
            final_df = self.transformation.run(clean_json)
            self.log_step("✅ Transformation Agent: Schema successfully standardized to lower_case.")
            
            self.log_step("🏁 Pipeline execution successfully finished. System standby.")
            return final_df, self.logs
            
        except Exception as e:
            error_msg = f"❌ Pipeline Failure: {str(e)}. Initiating safe diagnostic shutdown."
            self.log_step(error_msg)
            return None, self.logs