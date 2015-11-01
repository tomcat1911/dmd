import psycopg2

class Article:

  """This class decides which type of search it would be based on provided params"""

  conn = psycopg2.connect("dbname=projnew user=postgres")
  cur = conn.cursor()

  @staticmethod
  def find(author, category, title, year, limit):
    # BASE_SQL = "SELECT DISTINCT ON(title) title, summary, name, link, category FROM articles, categories, authors, connection WHERE "
    # conditions = "articles.id = connection.id and categories.cid = connection.cid and authors.aid = connection.aid "

    # if not (title or year or author or category):
    #   return -1
    # if title:
    #   conditions = conditions + "and lexemes @@ plainto_tsquery(%(title)s) "
    # if year:
    #   conditions = conditions + "and year = %(year)s "
    # if author:
    #   conditions = conditions + "and authors.name ILIKE '%% " + author + "%%' "
    # if category:
    #   conditions = conditions + "and categories.category = %(category)s "
    # if limit:
    #   limit = "LIMIT " + limit
    # else:
    #   limit = "LIMIT 50"

    # Article.cur.execute(BASE_SQL + conditions + limit, dict(title=title, category=category, year=year))
    BASE_SQL = "SELECT DISTINCT ON(title) title, summary, link, category "
    conditions = "WHERE articles.id = article_categories.id and articles.id = article_categories.id and article_categories.cid = categories.cid "

    if not (title or year or author or category):
      return -1

    if author:
      BASE_SQL = BASE_SQL + ", name FROM articles, categories, authors, article_authors, article_categories "
      conditions = conditions + "and articles.id = article_authors.id and article_authors.aid = authors.aid and authors.name ILIKE " + repr("%%"+author+"%%") + " "
    else:
      BASE_SQL = BASE_SQL + "FROM articles, article_categories, categories "

    if title:
      conditions = conditions + "and lexemes @@ plainto_tsquery(%(title)s) "
    if year:
      conditions = conditions + "and year = %(year)s "
    if category:
      conditions = conditions + "and categories.category = %(category)s"

    if limit:
      conditions = conditions + "LIMIT (%(limit)s)"
    else:
      conditions = conditions + "LIMIT 50"

    print(BASE_SQL + conditions)

    Article.cur.execute(BASE_SQL + conditions, dict(title=title, category=category, year=year, limit=limit))
    data = Article.cur.fetchall()

    return data

  @staticmethod
  def find_by_id(id):
    authors = []
    categories = []

    Article.cur.execute("SELECT DISTINCT ON (title) title, summary, link FROM articles WHERE id = %s", (id, ))
    data = Article.cur.fetchall()
    Article.cur.execute("SELECT DISTINCT name FROM authors as au, articles as ar, connection as co WHERE au.aid = co.aid and ar.id = co.id and ar.id = %s", (id, ))
    authors_data = Article.cur.fetchall()
    Article.cur.execute("SELECT DISTINCT category FROM categories as ca, articles as ar, connection as co WHERE ca.cid = co.cid and ar.id = co.id and ar.id = %s", (id, ))
    categories_data = Article.cur.fetchall()

    for i in range(0, len(authors_data)):
      authors.append(authors_data[i][0])

    for x in range(0, len(categories_data)):
      categories.append(categories_data[x][0])

    return dict(title=data[0][0], summary=data[0][1], link=data[0][2], authors=authors, categories=categories)



