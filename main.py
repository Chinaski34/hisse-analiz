import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://finance.yahoo.com"
}

@app.route('/analiz/<ticker>')
def analiz(ticker):
    try:
        url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}"
        params = "modules=financialData,defaultKeyStatistics,summaryProfile,price"
        res = requests.get(f"{url}?{params}", headers=HEADERS, timeout=15)
        data = res.json()
        
        qs = data.get("quoteSummary") or data.get("quoteTimeoutError") or {}
        result = qs.get("result")
        
        if result:
            return jsonify(result[0])
        
        url2 = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=financialData,defaultKeyStatistics,summaryProfile,price"
        res2 = requests.get(url2, headers=HEADERS, timeout=15)
        data2 = res2.json()
        qs2 = data2.get("quoteSummary", {})
        result2 = qs2.get("result")
        if result2:
            return jsonify(result2[0])
        
        return jsonify({"error": "Veri alınamadı"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
