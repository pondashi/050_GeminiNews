import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
import logging
from . import config

logger = logging.getLogger(__name__)

# Configure Gemini
if config.GEMINI_API_KEY:
    genai.configure(api_key=config.GEMINI_API_KEY)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def summarize_data(theme: str, news: list[dict], stocks: list[dict]) -> str:
    """
    Summarize the fetched news and stock data using Gemini.
    """
    logger.info("Generating summary with Gemini API.")
    
    if not news and not stocks:
        return f"{theme}に関する新しいニュースおよび株価データはありませんでした。"

    # Format the input data
    news_text = "\n".join([f"- {n['title']} ({n['url']})" for n in news])
    stock_text = "\n".join([
        f"- {s['ticker']}: 終値 {s['close']} (前日比 {s['change']} / {s['change_percent']}%) 出来高: {s['volume']}" 
        for s in stocks
    ])
    
    prompt = f"""
あなたはプロの金融アナリストです。以下の提供されたニュースと株価データを基に、本日の「{theme}」関連の市場動向を要約してください。

【指示】
1. 全体で300〜400文字程度にまとめること。
2. 箇条書きを適切に使い、視覚的に読みやすいレイアウトにすること。
3. 架空のデータやハルシネーションを含めず、提供されたデータのみを根拠とすること。

【ニュースデータ】
{news_text if news else 'ニュースデータなし'}

【株価データ（前日比等）】
{stock_text if stocks else '株価データなし'}
"""

    model = genai.GenerativeModel('gemini-3.5-flash')
    response = model.generate_content(prompt)
    
    logger.info("Summary generated successfully.")
    return response.text
