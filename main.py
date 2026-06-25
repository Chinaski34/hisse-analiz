import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/analiz/<ticker>')
def analiz(ticker):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        }
        res = requests.get(url, headers=headers, timeout=15)
        data = res.json()
        
        chart = data.get("chart", {})
        result = chart.get("result", [])
        if not result:
            return jsonify({"error": "Hisse bulunamadı"}), 404
        
        meta = result[0].get("meta", {})
        
        url2 = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=financialData%2CdefaultKeyStatistics%2CsummaryProfile"
        res2 = requests.get(url2, headers=headers, timeout=15)
        data2 = res2.json()
        
        qs = data2.get("quoteSummary", {})
        result2 = qs.get("result") or [{}]
        extra = result2[0] if result2 else {}
        
        return jsonify({
            "price": {
                "regularMarketPrice": {"raw": meta.get("regularMarketPrice")},
                "regularMarketChangePercent": {"raw": meta.get("regularMarketChangePercent")},
                "currency": meta.get("currency"),
                "longName": meta.get("longName") or meta.get("shortName"),
                "shortName": meta.get("shortName")
            },
            "financialData": extra.get("financialData", {}),
            "defaultKeyStatistics": extra.get("defaultKeyStatistics", {}),
            "summaryProfile": extra.get("summaryProfile", {})
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
