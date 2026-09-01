import os
import shutil
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from data_base import Sql
os.makedirs("pix_db", exist_ok=True)
def rp(path):
    try:
        base = sys._MEIPASS
    except AttributeError:
        base = os.path.abspath(".")
    return os.path.join(base, path)

class Auth_win(QWidget):
    def __init__(self):
        super().__init__()
        self.sql = Sql()
        self.name = ""
        self.role = None
        self.uid = None
        ui = rp("ui/auth_win.ui")
        uic.loadUi(ui, self)
        self.setWindowTitle('Обувь')
        self.setWindowIcon(QIcon(rp('assets/Icon.png')))

        self.pb_auth.clicked.connect(self.go_auth)
        self.pb_anonim.clicked.connect(self.go_main)


    def go_auth(self):
        log = self.le_log.text()
        pas = self.le_pas.text()

        if not log or not pas:
            QMessageBox.information(self, 'ошибка', "одно из полей пустое")
            return
        else:
            res = self.sql.auth(log, pas)
            if res:
                self.name = res[2] + " " + res[3] + " " + res[4]
                self.role = res[1]
                self.uid = res[0]
                self.go_main()
            else:
                QMessageBox.information(self, 'ошибка', "учетная запись не найдена")
                return


    def go_main(self):
        self.main_win = Main_win(self.uid, self.role, self.name)
        self.main_win.show()
        self.close()



class Main_win(QWidget):
    def __init__(self, uid, role, name):
        super().__init__()
        self.sql = Sql()
        self.name = name
        self.role = role
        self.uid = uid
        self.resize(750, 600)
        self.setWindowTitle('Обувь')
        self.setWindowIcon(QIcon(rp('assets/Icon.png')))

        root_layout = QVBoxLayout(self)

        up_layout = QHBoxLayout()
        root_layout.addLayout(up_layout)

        logo_lab = QLabel()
        logo_pix = QPixmap(rp('assets/Icon.png'))
        scld_logo = logo_pix.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio)
        logo_lab.setPixmap(scld_logo)


        pb_exit = QPushButton("выйти")
        pb_exit.clicked.connect(self.go_auth)
        lab_name = QLabel(str(self.name))

        up_layout.addWidget(logo_lab)
        up_layout.addStretch()
        up_layout.addWidget(lab_name)
        up_layout.addWidget(pb_exit)


        lab_name_company = QLabel("Обувь")
        lab_name_company.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lab_name_company.setStyleSheet('font-size: 14pt;')
        root_layout.addWidget(lab_name_company)

        self.manager_wid_catalog = QWidget()
        manager_layout_catalog = QHBoxLayout(self.manager_wid_catalog)
        root_layout.addWidget(self.manager_wid_catalog)

        self.le_search = QLineEdit()
        self.le_search.setPlaceholderText('артикул/наименование/производитель')
        manager_layout_catalog.addWidget(self.le_search)

        pb_search = QPushButton("поиск")
        pb_search.clicked.connect(self.search)
        manager_layout_catalog.addWidget(pb_search)

        self.cmb_filter = QComboBox()
        self.add_combo_filter()
        manager_layout_catalog.addWidget(self.cmb_filter)

        self.cmb_sort = QComboBox()
        self.cmb_sort.addItems(['', 'по возрастанию цены', "по убыванию цены"])
        manager_layout_catalog.addWidget(self.cmb_sort)

        pb_clean_search = QPushButton("сбросить все")
        pb_clean_search.clicked.connect(self.clean_search)
        manager_layout_catalog.addWidget(pb_clean_search)

        pb_orders = QPushButton("заказы")
        pb_orders.clicked.connect(self.all_orders)
        manager_layout_catalog.addWidget(pb_orders)

        self.manager_wid_orders = QWidget()
        manager_layout_orders = QHBoxLayout(self.manager_wid_orders)
        root_layout.addWidget(self.manager_wid_orders)

        pb_catalog = QPushButton("каталог")
        pb_catalog.clicked.connect(self.all_card)
        manager_layout_orders.addWidget(pb_catalog)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        root_layout.addWidget(self.scroll)
        self.all_card()

        if self.role == None or self.role == 'Авторизированный клиент':
            self.manager_wid_catalog.hide()

        self.manager_wid_orders.hide()

        self.cmb_filter.currentTextChanged.connect(self.search)
        self.cmb_sort.currentTextChanged.connect(self.search)

    def all_card(self):
        self.card, self.num_card = self.sql.all_card()
        self.create_card()
        self.manager_wid_orders.hide()
        self.manager_wid_catalog.show()

    def add_combo_filter(self):
        filter, num_filter = self.sql.combo_filter()
        self.cmb_filter.addItem('')

        for i in range(num_filter):
            self.cmb_filter.addItem(filter[i][0])

    def search(self):
        search = self.le_search.text()
        sort = self.cmb_sort.currentText()
        filtr = self.cmb_filter.currentText()

        self.card, self.num_card = self.sql.sort_card(search, sort, filtr)
        self.create_card()

    def clean_search(self):
        self.le_search.clear()
        self.cmb_sort.setCurrentIndex(0)
        self.cmb_filter.setCurrentIndex(0)
        self.all_card()

    def create_card(self):
        old = self.scroll.takeWidget()
        old = None

        main_scroll_wid = QWidget()
        self.scroll.setWidget(main_scroll_wid)
        self.main_scroll_wid_layout = QVBoxLayout(main_scroll_wid)

        for i in range(self.num_card):
            self.main_scroll_wid_layout.addWidget(self.one_card(i))

    def one_card(self, i):
        card_wid = QWidget()
        card_layuot = QVBoxLayout(card_wid)
        self.pid = self.card[i][0]

        main_frame = QFrame()
        main_frame.setFrameShape(QFrame.Shape.Box)
        main_frame_layuot = QHBoxLayout(main_frame)
        card_layuot.addWidget(main_frame)

        logo_lab = QLabel()
        logo_pix = QPixmap(rp(self.card[i][10]))
        scld_logo = logo_pix.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio)
        logo_lab.setPixmap(scld_logo)
        main_frame_layuot.addWidget(logo_lab)

        desc = (f'артикул: {str(self.card[i][0])} \n'
                f'категория: {str(self.card[i][6])} \n'
                f'наименование: {str(self.card[i][1])}\n'
                f'поставщик: {str(self.card[i][4])} || производитель: {str(self.card[i][5])}\n'
                f'\n'
                f'описание: {str(self.card[i][9])}\n'
                f'цена: {str(self.card[i][3])} руб.\n'
                f'в наличии: {str(self.card[i][8])} {str(self.card[i][2])}\n')
        lab_desc = QLabel(desc)
        main_frame_layuot.addWidget(lab_desc)

        sale_frame = QFrame()
        sale_frame.setFrameShape(QFrame.Shape.Box)
        sale_frame_layuot = QVBoxLayout(sale_frame)
        main_frame_layuot.addWidget(sale_frame)

        sale = self.card[i][8]
        sale_lab = QLabel(str(sale))
        sale_lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sale_frame_layuot.addWidget(sale_lab)

        pb_delete = QPushButton('удалить')
        sale_frame_layuot.addWidget(pb_delete)

        pb_update = QPushButton('редактировать(фото)')
        sale_frame_layuot.addWidget(pb_update)

        if self.role == 'Менеджер':
            pb_delete.hide()

        if sale > 15:
            sale_frame.setStyleSheet('background-color: #2E8B57;')

        main_frame.mousePressEvent = lambda event, pid = self.pid: self.press_card(event, pid)
        pb_delete.clicked.connect(lambda checked, pid=self.pid: self.del_prod(pid))
        pb_update.clicked.connect(lambda checked, pid=self.pid: self.update_photo(pid))

        return card_wid

    def del_prod(self, pid):
        self.win_del_pr = Del_prod(pid)
        self.win_del_pr.show()
        self.create_card()

    def update_photo(self, pid):
        try:
            fp = QFileDialog.getOpenFileName(self)[0]
            fn = os.path.basename(fp)

            if fn:
                shutil.copy(fp, 'pix_db/' + fn)

                fn_db = 'pix_db/' + fn
                self.sql.photo(fn_db, pid)

                QMessageBox.information(self, "успех", "фото обновлено")
                self.update_after_update()

        except Exception as e:
            print(e)
            QMessageBox.critical(self, "Ошибка", str(e))

    def update_after_update(self):
        self.main_win = Main_win(self.uid, self.role, self.name)
        self.close()
        self.main_win.show()

    def all_orders(self):
        self.ord, self.num_ord = self.sql.get_all_orders()
        self.create_orders()
        self.manager_wid_orders.show()
        self.manager_wid_catalog.hide()

    def create_orders(self):
        old = self.scroll.takeWidget()
        old = None

        main_scroll_wid = QWidget()
        self.scroll.setWidget(main_scroll_wid)
        self.main_scroll_wid_layout = QVBoxLayout(main_scroll_wid)

        for i in range(self.num_ord):
            self.main_scroll_wid_layout.addWidget(self.one_ord(i))

    def one_ord(self, i):
        card_wid = QWidget()
        card_layuot = QVBoxLayout(card_wid)
        self.oid = self.ord[i][0]

        main_frame = QFrame()
        main_frame.setFrameShape(QFrame.Shape.Box)
        main_frame_layuot = QHBoxLayout(main_frame)
        card_layuot.addWidget(main_frame)

        fio = self.ord[i][6] + ' ' + self.ord[i][7] + ' ' + self.ord[i][8]
        pvz = 'г.' + self.ord[i][3] + ' ул.' + self.ord[i][4] + ' д.' + self.ord[i][5]
        desc = (f'номер заказа: {str(self.ord[i][0])} \n'
                f'дата заказа: {str(self.ord[i][1])} || дата доставки: {str(self.ord[i][2])}\n'
                f'\n'
                f'ФИО заказчика: {fio}\n'
                f'адрес пункта выдачи: {pvz} \n'
                f'код получения: {str(self.ord[i][9])} \n'
                f'статус: {str(self.ord[i][10])}\n')
        lab_desc = QLabel(desc)
        main_frame_layuot.addWidget(lab_desc)

        sale_frame = QFrame()
        sale_frame.setFrameShape(QFrame.Shape.Box)
        sale_frame_layuot = QVBoxLayout(sale_frame)
        main_frame_layuot.addWidget(sale_frame)

        pb_more = QPushButton('подробнее')
        sale_frame_layuot.addWidget(pb_more)

        pb_delete = QPushButton('удалить')
        sale_frame_layuot.addWidget(pb_delete)

        if self.role == 'Менеджер':
            pb_delete.hide()

        pb_more.clicked.connect(lambda checked, oid = self.oid: self.more_ord(oid))
        pb_delete.clicked.connect(lambda checked, oid=self.oid: self.del_ord(oid))

        return card_wid

    def more_ord(self, oid):
        self.win_or = More_ord(oid)
        self.win_or.show()

    def del_ord(self, oid):
        self.win_del = Del_ord(oid)
        self.win_del.show()


    def press_card(self, event, pid):
        print(pid)


    def go_auth(self):
        self.auth_win = Auth_win()
        self.auth_win.show()
        self.close()

class More_ord(QWidget):
    def __init__(self, oid):
        super().__init__()
        self.oid = oid
        self.sql = Sql()
        self.resize(250, 150)
        self.setWindowTitle('Обувь')
        self.setWindowIcon(QIcon(rp('assets/Icon.png')))

        self.root_l = QVBoxLayout(self)
        self.prod_in_ord()

        pb_close = QPushButton('закрыть')
        pb_close.clicked.connect(self.go_close)
        self.root_l.addWidget(pb_close)

    def prod_in_ord(self):
        self.prod_in_ord, num_prod_in_ord = self.sql.get_more_ord(self.oid)

        for i in range(num_prod_in_ord):
            self.root_l.addWidget(self.create_lab(i))

    def create_lab(self, i):
        desc = (f'товар: {str(self.prod_in_ord[i][1])} \n'
                f'количество: {str(self.prod_in_ord[i][2])} \n')

        lab = QLabel(desc)
        return lab

    def go_close(self):
        self.close()

class Del_ord(QWidget):
    def __init__(self, oid):
        super().__init__()
        self.oid = oid
        self.sql = Sql()
        self.resize(250, 150)
        self.setWindowTitle('Обувь')
        self.setWindowIcon(QIcon(rp('assets/Icon.png')))

        root_l = QVBoxLayout(self)
        pb_l = QHBoxLayout()

        decs = f'вы действительно хотите удалить заказ {oid} ?'
        lab_del = QLabel(decs)
        root_l.addWidget(lab_del)

        pb_close = QPushButton('закрыть')
        pb_close.clicked.connect(self.go_close)
        pb_l.addWidget(pb_close)

        pb_del = QPushButton('удалить')
        pb_del.clicked.connect(self.del_ord)
        pb_l.addWidget(pb_del)

        root_l.addLayout(pb_l)

    def del_ord(self):
        res = self.sql.del_ord(self.oid)
        QMessageBox.information(self, 'успех', "заказ удален")
        self.go_close()

    def go_close(self):
        self.close()

class Del_prod(QWidget):
    def __init__(self, pid):
        super().__init__()
        self.oid = pid
        self.sql = Sql()
        self.resize(250, 150)
        self.setWindowTitle('Обувь')
        self.setWindowIcon(QIcon(rp('assets/Icon.png')))

        root_l = QVBoxLayout(self)
        pb_l = QHBoxLayout()

        decs = f'вы действительно хотите удалить товар {pid} ?'
        lab_del = QLabel(decs)
        root_l.addWidget(lab_del)

        pb_close = QPushButton('закрыть')
        pb_close.clicked.connect(self.go_close)
        pb_l.addWidget(pb_close)

        pb_del = QPushButton('удалить')
        pb_del.clicked.connect(self.del_prod)
        pb_l.addWidget(pb_del)

        root_l.addLayout(pb_l)

    def del_prod(self):
        res = self.sql.del_prod(self.oid)
        QMessageBox.information(self, 'успех', "товар удален")
        self.go_close()

    def go_close(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Auth_win()
    win.show()
    sys.exit(app.exec())
