from flask import Flask, request, jsonify
from flask_cors import CORS
from crew import SourceCodeAnalyzer

# Importing crewAI tools
from crewai_tools import DirectoryReadTool, FileReadTool
app = Flask(__name__)
CORS(app) # Enable CORS

@app.route('/run', methods=['POST'])
def run():
    """
    Run the crew.
    """
    data = request.get_json()
    file_path = data.get('path')
    
    # Assuming you need to set the directory path for the tools
    docs_tool = DirectoryReadTool(directory=file_path)
    file_tool = FileReadTool(directory=file_path)
    
    analyzer = SourceCodeAnalyzer(docs_tool=docs_tool, file_tool=file_tool)
    result = analyzer.crew().kickoff()
    result = str(result)
    return jsonify({"status": "success", "result": result}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)