########################################################################################################################
#    File: main.py
#  Author: Dan Huckson, https://github.com/unodan
#    Date: 2018-09-19
# Purpose: MVC (Model View Controller) Demo
########################################################################################################################

from tkinter import Tk, Toplevel, Label, Entry, Button


class Transaction:
    def __init__(self):
        self.value = 0
        self.callbacks = {}

    def add_callback(self, func):
        self.callbacks[func] = None

    def _callbacks(self):
        for func in self.callbacks:
            func(self.value)

    def set(self, value):
        self.value = value
        self._callbacks()

    def get(self):
        return self.value


class Account:  # The Model
    def __init__(self):
        self.transaction = Transaction()

    def deposit(self, value):
        self.transaction.set(self.transaction.get() + value)

    def withdrawal(self, value):
        self.transaction.set(self.transaction.get() - value)


class BankView(Toplevel):  # View 1
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)

        Label(self, text='Account Balance').pack(side='left')
        self.balance = Entry(self, width=8)
        self.balance.pack(side='left')

    def set_balance(self, amount):
        self.balance.delete(0, 'end')
        self.balance.insert('end', str(amount))


class TellerView(Toplevel):  # View 2
    def __init__(self, master):
        Toplevel.__init__(self, master)

        Label(self, text='Amount').pack(side='left')
        self.amount = Entry(self, width=8)
        self.amount.pack(side='left')

        self.btn_deposit = Button(self, text='Deposit', width=8)
        self.btn_deposit.pack(side='left')

        self.btn_withdrawal = Button(self, text='Withdrawal', width=8)
        self.btn_withdrawal.pack(side='left')


class Bank(Tk):  # The Controller
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.withdraw()

        self.account = Account()
        self.account.transaction.add_callback(self.update_account)

        self.bank_view = BankView(self)
        self.bank_view.title('The Bank')

        self.teller_view = TellerView(self.bank_view)
        self.teller_view.title('The Teller')

        self.teller_view.btn_deposit.config(command=self.make_deposit)
        self.teller_view.btn_withdrawal.config(command=self.make_withdrawal)

        self.update_account(self.account.transaction.get())

    def make_deposit(self):
        self.account.deposit(int(self.teller_view.amount.get()))

    def make_withdrawal(self):
        self.account.withdrawal(int(self.teller_view.amount.get()))

    def update_account(self, amount):
        self.bank_view.set_balance(amount)


if __name__ == '__main__':
    Bank().mainloop()
