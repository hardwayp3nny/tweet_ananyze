from flask import Flask, render_template, jsonify, request, session
from sqlalchemy import create_engine, func, cast, Date, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text as sql_text  # 重命名为 sql_text
from datetime import datetime, timedelta
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import jieba

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE_URL = "mssql+pyodbc://1:1@localhost/twitter?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

@app.route('/')
def index():
    db_session = Session()
    tables = db_session.execute(sql_text("SELECT name FROM sys.tables WHERE schema_name(schema_id) = 'dbo'")).fetchall()
    db_session.close()
    return render_template('index.html', tables=[table[0] for table in tables])

@app.route('/select_table', methods=['POST'])
def select_table():
    selected_table = request.form['table_name']
    session['selected_table'] = selected_table
    print(f"Selected table: {selected_table}")
    return jsonify({'selected_table': selected_table})

@app.route('/wordcloud')
def get_wordcloud():
    table_name = request.args.get('table') or session.get('selected_table', 'Twitter_elonmusk')
    table_name = table_name.split('.')[-1]  # 移除可能的架构名
    db_session = Session()
    query = sql_text(f"SELECT tweet_content FROM {table_name}")
    tweets = db_session.execute(query).fetchall()
    db_session.close()

    tweet_text = ' '.join([tweet[0] for tweet in tweets if tweet[0]])

    # 排除的单词列表
    excluded_words = set([
        'nan', '了', '的','也','万','以','从' ,'小时','分钟','目前','他','在','通过','是','前','将','然后','已' # 添加你想要排除的单词
    ])

    # 判断文本是否包含中文字符
    def contains_chinese(text):
        return any('\u4e00' <= char <= '\u9fff' for char in text)

    if contains_chinese(tweet_text):
        # 中文文本处理
        word_tokens = jieba.cut(tweet_text)
        filtered_text = [word for word in word_tokens if len(word.strip()) > 0 and word not in excluded_words]
        font_path = r'C:\Windows\Fonts\simhei.ttf'  # 确保这是正确的字体路径
    else:
        # 英文文本处理
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(tweet_text)
        filtered_text = [
            word.lower() for word in word_tokens
            if word.isalnum() and word.lower() not in stop_words and word.lower() not in excluded_words
        ]
        font_path = None  # 不使用特定字体

    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        font_path=font_path  # 传递字体路径
    ).generate(' '.join(filtered_text))

    img = io.BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(img, format='png')
    img.seek(0)

    return base64.b64encode(img.getvalue()).decode()
@app.route('/stats_chart')
def get_stats_chart():
    table_name = request.args.get('table') or session.get('selected_table', 'Twitter_elonmusk')
    table_name = table_name.split('.')[-1]  # 移除可能的架构名
    db_session = Session()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    query = sql_text(f"""
    SELECT 
        CAST(tweet_time AS DATE) AS date,
        AVG(CAST(favorite_count AS FLOAT)) AS avg_favorite,
        AVG(CAST(retweet_count AS FLOAT)) AS avg_retweet,
        AVG(CAST(reply_count AS FLOAT)) AS avg_reply
    FROM {table_name}
    WHERE tweet_time BETWEEN :start_date AND :end_date
    GROUP BY CAST(tweet_time AS DATE)
    ORDER BY CAST(tweet_time AS DATE)
    """)

    results = db_session.execute(query, {'start_date': start_date, 'end_date': end_date}).fetchall()
    db_session.close()

    dates = [result.date.strftime('%Y-%m-%d') for result in results]
    avg_favorites = [float(result.avg_favorite) for result in results]
    avg_retweets = [float(result.avg_retweet) for result in results]
    avg_replies = [float(result.avg_reply) for result in results]

    return jsonify({
        'dates': dates,
        'avg_favorites': avg_favorites,
        'avg_retweets': avg_retweets,
        'avg_replies': avg_replies
    })

@app.route('/tweet_data')
def get_tweet_data():
    table_name = request.args.get('table') or session.get('selected_table', 'Twitter_elonmusk')
    table_name = table_name.split('.')[-1]  # 移除可能的架构名
    sort_by = request.args.get('sort_by', 'tweet_time')
    order = request.args.get('order', 'desc')

    db_session = Session()
    query = sql_text(f"""
    SELECT TOP 2000 tweet_time, tweet_content, favorite_count, retweet_count, reply_count
    FROM {table_name}
    ORDER BY {sort_by} {order}
    """)
    tweets = db_session.execute(query).fetchall()
    db_session.close()

    df = pd.DataFrame(tweets,
                      columns=['tweet_time', 'tweet_content', 'favorite_count', 'retweet_count', 'reply_count'])
    return df.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
