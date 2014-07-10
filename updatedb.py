# coding: utf-8

import sqlite3

con = sqlite3.connect('../database.sqlite')
c = con.cursor()
c.execute('''ALTER TABLE models_itemlicitacao ADD controleItem varchar(10);''')
c.execute('''ALTER TABLE models_cotacao ADD controleItem varchar(10);''')
con.commit()
c.close()