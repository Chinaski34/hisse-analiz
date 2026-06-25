import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/analiz/<ticker>')
def analiz(ticker):
    try:
        url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}"
        params = {"modules": "financialData,defaultKeyStatistics,summaryProfile,price"}
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, params=params, headers=headers, timeout=15)
        data = res.json()
        if data.get("quoteSummary", {}).get("error"):
            return jsonify({"error": "Hisse bulunamadı"}), 404
        return jsonify(data["quoteSummary"]["result"][0])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
