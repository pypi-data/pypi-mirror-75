"""Updates the balance sheet for the month"""
import sys
from datetime import datetime
import balanceSheet


class Program:
    def __init__(self):
        self.bs = balanceSheet.BalanceSheet()
        self.today = datetime.today().date()

    def add(self):
        "Prompt the user to add new items to the balance sheet"
        done = False
        while not done:
            res = []            # where we store the item to enter
            # prompt for item type
            a_o_l = input("\nAsset or Liability (a/l)? ")
            if a_o_l.lower() == "a":
                res.append("Asset")
            elif a_o_l.lower() == "l":
                res.append("Liability")
            else:
                print("Error: invalid input")
                continue
            # prompt for the name of the item
            name = input("Item name: ")
            res.append(name)
            # prompt for the value of the item
            val = input("Value: ")
            try:
                res.append(float(val))
            except ValueError:
                print("Error: invalid input")
                continue
            # prompt for the description of the item
            desc = input("Description (optional): ")
            res.append(desc)
            # insert the result into the table
            self.bs.insert(res)
            # show current balance sheet
            self.bs.read(); self.bs.display()
            # prompt to continue
            cont = input("Continue (y/n)? ")
            if cont.lower() == "n":
                done = True
            elif cont.lower() != "y":
                print("Error: invalid input")
                continue
            
    def modify(self):
        "Modifies entries in the current balance sheet"
        done = False
        while not done:
            # whether we are modifying an asset or liability
            a_o_l = input("\nAsset or Liability (a/l)? ")
            if a_o_l.lower() == "a":
                type_sec = "Asset"
            elif a_o_l.lower() == "l":
                type_sec = "Liability"
            else:
                print("Error: invalid input")
                continue
            # which item to modify
            item = input("Which item would you like to modify? ")
            try:
                item = int(item)
            except ValueError:
                print("Error: invalid input")
                continue
            # the field to modify
            field = input("Which field? (name/n, value/v, description/d) ")
            # interpret the shorthand
            if field == "n":
                field = "name"
            elif field == "v":
                field = "value"
            elif field == "d":
                field = "description"
            # what to make the new value
            value = input("What is the new value? ")
            # make the modification
            self.bs.modify(type_sec, item, field, value)
            # show current balance sheet
            self.bs.read(); self.bs.display()
            # ask to continue
            cont = input("Continue (y/n)? ")
            if cont.lower() == "n":
                done = True
            elif cont.lower() != "y":
                print("Error: invalid input")
                continue
    
    def delete(self):
        "Deletes entries in the balance sheet"
        done = False
        while not done:
            # whether we are deleting an asset or liability
            a_o_l = input("\nAsset or Liability (a/l)? ")
            if a_o_l.lower() == "a":
                type_sec = "Asset"
            elif a_o_l.lower() == "l":
                type_sec = "Liability"
            else:
                print("Error: invalid input ")
                continue
            # which item to modify
            item = input("Which item would you like to delete? ")
            try:
                item = int(item)
            except ValueError:
                print("Error: invalid input")
                continue
            # make the deletion
            self.bs.delete(type_sec, item)
            # show current balance sheet
            self.bs.read(); self.bs.display()
            # ask to continue
            cont = input("Continue (y/n)? ")
            if cont.lower() == "n":
                done = True
            elif cont.lower() != "y":
                print("Error: invalid input")
                continue

    def check_for_update(self):
        "Check if we need to make a new balance sheet for the month"
        # get the last time we updated a balance sheet
        last_update = datetime.strptime(self.bs.last_date, "%Y-%m-%d")
        # check if we need to make a new one
        if last_update.month < self.today.month:
            # move the balance sheet from last time into this month
            self.bs.move_forward()
        else:
            # update the last updated date to today
            self.bs.update_date(self.today)

    def check_init(self):
        "Checks if we have a previous balance sheet to carry through or edit"
        # get the last date the balance sheet was updated
        self.bs.get_date()
        if not self.bs.last_date:
            # make a new balance sheet
            print("Setting first balance sheet")
            # add the date of the new balance sheet
            self.bs.insert_date(str(self.today))
            # add items to the new balance sheet
            self.add()
            # read the current balance sheet
            self.bs.read()
            print(f"\nBalance sheet for {self.today}:\n")
            # display the sheet
            self.bs.display()
            # quit the parent program
            sys.exit()

    def run(self):
        "Guides through the balance sheet workflow"
        # check if we have a current balance sheet
        self.check_init()
        # check for a new month
        self.check_for_update()
        # read the saved balance sheet
        self.bs.read()
        # display the current balance sheet
        print(f"Balance sheet for {self.today}:")
        self.bs.display()
        # prompt to edit the balance sheet
        edit = input(f"\nEdit your current balance sheet for {self.today}? (y/n) ")
        if edit.lower() == 'y':
            done = False
            while not done:
                prompt = input("add, modify, delete, or done? (a, m, d, n) ")
                if prompt in ["a", "add"]:
                    self.add()
                elif prompt in ["m", "modify"]:
                    self.modify()
                elif prompt in ["d", "delete"]:
                    self.delete()
                elif prompt in ["n", "done"]:
                    done = True
                else:
                    print("Invalid entry")


if __name__ == "__main__":
    Program().run()