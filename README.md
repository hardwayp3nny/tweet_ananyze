Twitter 数据分析网站
项目简介
这是一个基于 Flask 的 Web 应用程序，用于分析和可视化 Twitter 数据。该应用程序允许用户选择不同的 Twitter 数据表，并生成词云图、统计图表以及显示推文数据。

主要功能
表格选择：用户可以从数据库中选择不同的 Twitter 数据表进行分析。
词云生成：基于选定表格中的推文内容生成词云图，支持中英文。
统计图表：显示过去 30 天内平均点赞数、转发数和回复数的趋势图。
推文数据展示：以表格形式展示最新的 2000 条推文数据，包括发布时间、内容、点赞数、转发数和回复数。
技术栈
后端：Flask, SQLAlchemy
数据库：Microsoft SQL Server
前端：HTML, JavaScript, Chart.js
数据处理：pandas, nltk, jieba
可视化：matplotlib, wordcloud
安装指南
克隆项目仓库到本地。
安装所需的 Python 包：

pip install flask sqlalchemy pyodbc pandas nltk jieba wordcloud matplotlib
确保已安装 Microsoft SQL Server 和相应的 ODBC 驱动程序。
在 main.py 中配置数据库连接字符串（DATABASE_URL）。
使用说明
运行 main.py 启动 Flask 服务器。
在浏览器中访问 http://localhost:5000。
从下拉菜单中选择要分析的 Twitter 数据表。
查看生成的词云图、统计图表和推文数据。
主要路由
/: 首页，显示可用的数据表列表。
/select_table: 处理表格选择请求。
/wordcloud: 生成并返回词云图。
/stats_chart: 返回统计图表数据。
/tweet_data: 返回推文数据。
注意事项
确保 simhei.ttf 字体文件路径正确，用于中文词云生成。
应用程序默认使用 Twitter_elonmusk 表，如果该表不存在，请修改默认值。
词云生成过程中会排除一些常见词和停用词，可以根据需要在代码中调整。
自定义和扩展
可以在 excluded_words 列表中添加或删除要排除的词语。
统计图表当前显示 30 天的数据，可以通过修改 timedelta(days=30) 来调整时间范围。
推文数据展示限制为 2000 条，可以通过修改 SQL 查询中的 TOP 2000 来调整。
截图
应用程序截图
![屏幕截图 2024-07-29 102520](https://github.com/user-attachments/assets/ff46f52e-ff84-493b-bdfc-3c4b1181df60)

该截图展示了应用程序的主界面，包括词云图、统计图表和推文数据表格。

贡献
欢迎提交 issues 和 pull requests 来改进这个项目。
