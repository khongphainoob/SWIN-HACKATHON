from tools.search_tool import SearchNewsTool

tool = SearchNewsTool()
articles = tool.execute("NVDA", 5)

for a in articles:
    print(a["published"], "-", a["title"])
    print(a["link"])
    print("---")