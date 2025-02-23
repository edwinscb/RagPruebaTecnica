from flask import Flask, request, jsonify
from llm import generate_response

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    """Endpoint para recibir una consulta y devolver la respuesta del LLM con los chunks."""
    data = request.json
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "La consulta no puede estar vacía"}), 400

    # Obtener respuesta y chunks
    response, chunks = generate_response(query)
    
    # Retornar respuesta y chunks en el formato solicitado
    return jsonify({
        "response": response,
        "content": chunks
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
