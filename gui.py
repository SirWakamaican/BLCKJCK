import tkinter as tk
from tkinter import ttk
import locale
import objects
import db
import math
from datetime import date, time, datetime


class BlackjackFrame(ttk.Frame):
    def __init__(self, parent):

        ttk.Frame.__init__(self,parent, padding="10 10 10 10")
        self.parent = parent
        self.deck = objects.Deck()
        self.dealer = objects.Hand()
        self.player = objects.Hand()
        self.resetNeeded = False
        self.isDone = False

        self.money = tk.StringVar()
        self.bet = tk.StringVar()
        self.result = tk.StringVar()
        self.dHand = tk.StringVar()
        self.dTotal = tk.StringVar()
        self.pHand = tk.StringVar()
        self.pTotal = tk.StringVar()

        location = locale.setlocale(locale.LC_ALL, '')
        if location == 'C':
            locale.setlocale(locale.LC_ALL, 'en_US')

        try:
            self.money.set(locale.currency(startMoney, grouping=True))
        except TypeError:
            self.money.set(locale.currency(float(startMoney[1:]), grouping=True))
        openMsg = "You must place a valid bet to play."
        self.result.set(openMsg)

        self.initComponents()

    def initComponents(self):
        self.pack()

        ttk.Label(self, text="Money: ").grid(column=0, row=0, sticky=tk.E)
        ttk.Entry(self, width=50, textvariable=self.money, state="readonly").grid(column=1, row=0)

        ttk.Label(self, text="Bet: ").grid(column=0, row=1, sticky=tk.E)
        ttk.Entry(self, width=50, textvariable=self.bet).grid(column=1, row=1)


        ttk.Label(self, text="DEALER").grid(column=0, row=3, sticky =tk.E)
        ttk.Label(self, text="Cards: ").grid(column=0, row=4, sticky=tk.E)
        ttk.Entry(self, width=50, textvariable=self.dHand, state="readonly").grid(column=1, row=4)
        ttk.Label(self, text= "Points: ").grid(column=0, row =5, sticky=tk.E)
        ttk.Entry(self, width=50, textvariable=self.dTotal, state="readonly").grid(column=1, row=5)

        ttk.Label(self, text="PLAYER").grid(column=0, row=7, sticky=tk.E)
        ttk.Label(self, text="Cards: ").grid(column=0, row=8, sticky=tk.E)
        ttk.Entry(self, width=50, textvariable=self.pHand, state="readonly").grid(column=1, row=8)
        ttk.Label(self, text="Points: ").grid(column=0, row=9, sticky=tk.E)
        ttk.Entry(self, width=50, textvariable=self.pTotal, state="readonly").grid(column=1, row=9)

        ttk.Label(self, text="\n").grid(column=0, row= 11, sticky=tk.E)
        ttk.Label(self, text="RESULT:").grid(column=0, row=12, sticky=tk.E)
        ttk.Entry(self, width=50, textvariable=self.result, state="readonly").grid(column=1, row=12)

        self.makeButtons()

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady= 3)

    def makeButtons(self):

        buttonFrame = ttk.Frame(self)
        buttonFrame.grid( column=0, row=10, columnspan=2, sticky=tk.E)

        ttk.Button(buttonFrame, text="Hit", command=self.hit).grid(column=0, row=0, padx=5)
        ttk.Button(buttonFrame, text="Stand", command=self.finish).grid(column=1, row=0, padx=5)

        buttonFrame2 = ttk.Frame(self)
        buttonFrame2.grid( column=0, row=13,columnspan=2, sticky=tk.E)
        ttk.Button(buttonFrame2, text="Play", command=self.play).grid(column=0, row=0)
        ttk.Button(buttonFrame2, text="Exit", command=self.parent.destroy).grid(column=3, row=0)

    def hit(self):
        if self.player.total() > 21:
            pass

        elif self.isDone:
            pass

        elif self.validateBet() and self.player.count() >= 2:
            self.deck.deal(1, self.player)
            self.pHand.set(self.player.show())
            self.pTotal.set(self.player.total())
            if self.player.total() > 21:
                self.finish()

        else:
            self.result.set("Please click play after valid bet is placed!")

    def finish(self):
        if self.isDone:
            pass

        if self.validateBet() and self.player.count() >= 2 and self.dealer.total() < 17:

            while self.dealer.total() < 17:
                self.deck.deal(1, self.dealer)

            self.dHand.set(self.dealer.show())
            self.dTotal.set(self.dealer.total())
            self.money.set(self.money.get()[1:])

            if self.dealer.total() > 21:
                if self.player.total() <= 21:
                    if self.player.count() == 2 and self.player.total() == 21:
                        newBet = float(self.bet.get()) * 1.5
                        self.money.set( round(float(self.money.get()) + newBet, 2) )
                        self.result.set("Hooray you won! Blackjack obtained payout 3:2")
                    else:
                        self.money.set( round(float(self.money.get()) + float(self.bet.get()), 2) )
                        self.result.set("Horray you won!")
                else:
                    self.result.set("It is a tie!")

            elif self.player.total() > self.dealer.total():
                if self.player.total() > 21:
                    self.result.set("Sorry. You lose!")
                    self.money.set( round( float( self.money.get()) - float(self.bet.get() ), 2 ) )
                else:
                    if self.player.count() == 2 and self.player.total() == 21:
                        newBet = float(self.bet.get()) * 1.5
                        self.money.set(round(float(self.money.get()) + newBet, 2))
                        self.result.set("Hooray you won! Blackjack obtained payout 3:2")
                    else:
                        self.money.set( round(float(self.money.get()) + float(self.bet.get()), 2) )
                        self.result.set("Horray you won!")

            elif self.player.total() == self.dealer.total():
                self.result.set("It is a tie!")

            else:
                self.result.set("Sorry. You lose!")
                self.money.set( round( float( self.money.get()) - float(self.bet.get() ), 2 ) )

            self.money.set(locale.currency(float(self.money.get()), grouping=True))
            self.resetNeeded = True
            self.isDone = True
            global stopMoney
            stopMoney = self.money.get()[1:]


        else:
            self.result.set("Please click play after valid bet is placed!")


    def play(self):
        if self.dealer.count() == 1:
            self.resetNeeded = True

        if self.resetNeeded:
            # put cards back and reset hand objects
            while self.dealer.count() > 0:
                self.dealer.reset(self.deck)
            while self.player.count() > 0:
                self.player.reset(self.deck)
            self.isDone = False

        if self.validateBet():
            self.deck.shuffle()
            self.deck.deal(1, self.dealer)
            self.deck.deal(2, self.player)
            self.dHand.set(self.dealer.show())
            self.pHand.set(self.player.show())
            self.pTotal.set(self.player.total())
            self.dTotal.set("")
            self.result.set("")

        else:
            pass


    def validateBet(self):
        try:
            if math.floor(float(self.bet.get())) >= 5.00 and math.ceil(float(self.bet.get())) <= 1000.00 and float(self.money.get()[1:]) >= float(self.bet.get()):
                return True
            else:
                self.result.set('Invalid Bet, Please try again!')
                return False

        except ValueError:
            self.result.set('Invalid number, Please try again!')
            return False

    def getStopMoney(self):
        return self.money.get()


if __name__ == "__main__":
    global stopMoney
    startTime = datetime.now()
    db.connect()
    db.create_session()
    # Reads from previous stopMoney value to be starting balance for current session
    startMoney = db.get_last_session()[4]
    stopMoney = startMoney
    root = tk.Tk()
    root.title("Blackjack")
    BlackjackFrame(root)
    root.mainloop()
    session = objects.Session(startTime,startMoney,datetime.now(),stopMoney)
    db.add_session(session)
    db.close()



