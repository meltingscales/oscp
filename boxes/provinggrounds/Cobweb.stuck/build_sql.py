
def build_sql(route_string):
  sql = "SELECT page_data FROM webpages WHERE route_string = \"" + route_string + "\";";
  print(sql);
  return sql;


build_sql('"; select * from test; --')
