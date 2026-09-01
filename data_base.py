import pymysql
from PyQt6.QtWidgets import QMessageBox

def con_db():
    try:
        return pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='ooo_boots',
            charset='utf8mb4'
        )
    except Exception as e:
        print(e)
        QMessageBox.information(None, "ошибка", "ошибка подключения, попробуйте позже")



class Sql():
    def auth(self, log, pas):
        try:
            con = con_db()
            cursor = con.cursor()

            cursor.execute('select id_user, role, f_name, l_name, m_name from users '
                           'where login = %s and passwrd = %s', (log, pas))
            res = cursor.fetchone()

            return res

        except Exception as e:
            print(e)
            QMessageBox.information(None, "ошибка", "ошибка подключения, попробуйте позже")
        finally:
            cursor.close()
            con.close()

    def all_card(self):
        try:
            con = con_db()
            cursor = con.cursor()

            cursor.execute('select * from product')
            res = cursor.fetchall()

            return res, len(res)

        except Exception as e:
            print(e)
            QMessageBox.information(None, "ошибка", "ошибка подключения, попробуйте позже")
        finally:
            cursor.close()
            con.close()

    def combo_filter(self):
        try:
            con = con_db()
            cursor = con.cursor()

            cursor.execute('select distinct categoty from product')
            res = cursor.fetchall()

            return res, len(res)

        except Exception as e:
            print(e)
            QMessageBox.information(None, "ошибка", "ошибка подключения, попробуйте позже")
        finally:
            cursor.close()
            con.close()

    def sort_card(self, search, sort, filtr):
        try:
            con = con_db()
            cursor = con.cursor()

            querry = 'select * from product where 1=1'
            params = []

            if search:
                querry += ' and (id_prod like %s or type_prod like %s or creater like %s)'
                search_pat = f"%{search}%"
                params.extend([search_pat, search_pat, search_pat])
            if filtr:
                querry += ' and categoty = %s'
                params.append(filtr)

            if sort == 'по возрастанию цены':
                querry += ' order by price asc'
            elif sort == 'по убыванию цены':
                querry += ' order by price desc'


            cursor.execute(querry, params)
            res = cursor.fetchall()

            return res, len(res)

        except Exception as e:
            print(e)
            QMessageBox.information(None, "ошибка", "ошибка подключения, попробуйте позже")
        finally:
            cursor.close()
            con.close()


    def get_all_orders(self):
        try:
            con = con_db()
            cursor = con.cursor()

            cursor.execute("select o.id_ord, o.date_ord, o.date_delev, p.city, p.street, p.house,  u.f_name, u.l_name, u.m_name, o.get_code, status from orders o join users u on o.id_user = u.id_user join pvz p on o.id_pvz = p.id_pvz")
            res = cursor.fetchall()

            return res, len(res)

        except Exception as e:
            print(e)
            QMessageBox.information(None, "ошибка", "ошибка подключения, попробуйте позже")
        finally:
            cursor.close()
            con.close()

    def get_more_ord(self, oid):
        try:
            con = con_db()
            cursor = con.cursor()

            cursor.execute("select id_ord, id_prod, num from in_ord where id_ord = %s", (oid,))
            res = cursor.fetchall()

            return res, len(res)

        except Exception as e:
            print(e)
            QMessageBox.information(None, "ошибка", "ошибка подключения, попробуйте позже")
        finally:
            cursor.close()
            con.close()

    def del_ord(self, oid):
        try:
            con = con_db()
            cursor = con.cursor()

            cursor.execute("delete from orders where id_ord = %s", (oid,))
            con.commit()



        except Exception as e:
            print(e)
            QMessageBox.information(None, "ошибка", "ошибка подключения, попробуйте позже")
        finally:
            cursor.close()
            con.close()

    def del_prod(self, oid):
        try:
            con = con_db()
            cursor = con.cursor()

            cursor.execute("delete from product where id_prod = %s", (oid,))
            con.commit()



        except Exception as e:
            print(e)
            QMessageBox.information(None, "ошибка", "ошибка подключения, попробуйте позже")
        finally:
            cursor.close()
            con.close()

    def photo(self, fn, oid):
        try:
            con = con_db()
            cursor = con.cursor()

            cursor.execute("update product set photo = %s where id_prod = %s", (fn, oid,))
            con.commit()



        except Exception as e:
            print(e)
            QMessageBox.information(None, "ошибка", "ошибка подключения, попробуйте позже")
        finally:
            cursor.close()
            con.close()