from backend.process import process_csv, generate_novel_graph
from front.app import app

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port='8050', debug=True,dev_tools_ui=False)
    #generate_novel_graph('plain')

