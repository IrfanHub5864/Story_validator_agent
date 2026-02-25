import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from engine.ai_evaluator import evaluate_story
from engine.azure_commenter import add_comment_to_work_item

app = Flask(__name__)
CORS(app)  # Enable CORS for extension
@app.after_request
def add_private_network_header(response):
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    return response

PROMPT_TEXT = """Your prompt text here..."""

@app.route('/validate', methods=['POST'])
def validate():
    try:
        data = request.json
        work_item_id = data.get('workItemId')
        story_text = data.get('storyText')
        
        # Run validation
        result = evaluate_story(story_text, PROMPT_TEXT)
        
        # Add comment to Azure DevOps
        add_comment_to_work_item(work_item_id, result)
        
        return jsonify({
            'success': True,
            'validation': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
