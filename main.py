import os
import yfinance as yf
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/analiz/<ticker>')
def analiz(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        if not info or info.get('regularMarketPrice') is None:
            return jsonify({"error": "Hisse bulunamadı"}), 404
        return jsonify({
            "price": {
                "regularMarketPrice": {"raw": info.get("currentPrice") or info.get("regularMarketPrice")},
                "regularMarketChangePercent": {"raw": info.get("regularMarketChangePercent")},
                "currency": info.get("currency"),
                "longName": info.get("longName"),
                "shortName": info.get("shortName")
            },
            "financialData": {
                "currentPrice": {"raw": info.get("currentPrice")},
                "returnOnEquity": {"raw": info.get("returnOnEquity")},
                "profitMargins": {"raw": info.get("profitMargins")},
                "grossMargins": {"raw": info.get("grossMargins")},
                "revenueGrowth": {"raw": info.get("revenueGrowth")},
                "totalRevenue": {"raw": info.get("totalRevenue")},
                "debtToEquity": {"raw": info.get("debtToEquity")},
                "financialCurrency": info.get("financialCurrency") or info.get("currency")
            },
            "defaultKeyStatistics": {
                "forwardPE": {"raw": info.get("forwardPE")},
                "trailingPE": {"raw": info.get("trailingPE")},
                "priceToBook": {"raw": info.get("priceToBook")},
                "enterpriseToEbitda": {"raw": info.get("enterpriseToEbitda")}
            },
            "summaryProfile": {
                "sector": info.get("sector"),
                "industry": info.get("industry")
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
