"""
Questions:
 

    1. Complete the `MiniVenmo.create_user()` method to allow our application to create new users.

    2. Complete the `User.pay()` method to allow users to pay each other. Consider the following: if user A is paying user B, user's A balance should be used if there's enough balance to cover the whole payment, if not, user's A credit card should be charged instead.

    3. Venmo has the Feed functionality, that shows the payments that users have been doing in the app. If Bobby paid Carol $5, and then Carol paid Bobby $15, it should look something like this
   

    Bobby paid Carol $5.00 for Coffee
    Carol paid Bobby $15.00 for Lunch

    Implement the `User.retrieve_activity()` and `MiniVenmo.render_feed()` methods so the MiniVenmo application can render the feed.

    4. Now users should be able to add friends. Implement the `User.add_friend()` method to allow users to add friends.
    5. Now modify the methods involved in rendering the feed to also show when user's added each other as friends.
"""

"""
MiniVenmo! Imagine that your phone and wallet are trying to have a beautiful
baby. In order to make this happen, you must write a social payment app.
Implement a program that will feature users, credit cards, and payment feeds.
"""

import re
import unittest
import uuid
import datetime


class UsernameException(Exception):
    pass


class PaymentException(Exception):
    pass


class CreditCardException(Exception):
    pass


class Activity:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.timestamp = datetime.datetime.now()

class Payment(Activity):

    def __init__(self, amount, actor, target, note):
        super().__init__()
        self.amount = float(amount)
        self.actor = actor
        self.target = target
        self.note = note
 

class FriendActivity(Activity):
    def __init__(self, actor, target):
        super().__init__()
        self.actor = actor
        self.target = target

    def __str__(self):
        return f"{self.actor.username} and {self.target.username} became friends"

class User:

    def __init__(self, username):
        self.credit_card_number = None
        self.balance = 0.0
        self.activities = []
        self.friends = []

        if self._is_valid_username(username):
            self.username = username
        else:
            raise UsernameException('Username not valid.')


    def retrieve_activity(self):
        return sorted(self.activities, key=lambda a: a.timestamp, reverse=True)

    def add_friend(self, new_friend):
        if self.username == new_friend.username:
            raise UsernameException('Cannot add yourself as friend')
            
        if new_friend in self.friends:
            raise UsernameException('User is already a friend')
            
        self.friends.append(new_friend)
        new_friend.friends.append(self)
        
        # Record friend activity for both users
        friend_activity = FriendActivity(self, new_friend)
        self.activities.append(friend_activity)
        new_friend.activities.append(friend_activity)

    def add_to_balance(self, amount):
        self.balance += float(amount)

    def add_credit_card(self, credit_card_number):
        if self.credit_card_number is not None:
            raise CreditCardException('Only one credit card per user!')

        if self._is_valid_credit_card(credit_card_number):
            self.credit_card_number = credit_card_number

        else:
            raise CreditCardException('Invalid credit card number.')

    def pay(self, target, amount, note):
        amount = float(amount)
        
        if self.username == target.username:
            raise PaymentException('User cannot pay themselves.')
            
        if amount <= 0.0:
            raise PaymentException('Amount must be a non-negative number.')
            
        try:
            if self.balance >= amount:
                return self.pay_with_balance(target, amount, note)
            else:
                return self.pay_with_card(target, amount, note)
        except PaymentException as e:
            raise PaymentException(f'Payment failed: {str(e)}')

    def pay_with_card(self, target, amount, note):
        amount = float(amount)

        if self.username == target.username:
            raise PaymentException('User cannot pay themselves.')

        elif amount <= 0.0:
            raise PaymentException('Amount must be a non-negative number.')

        elif self.credit_card_number is None:
            raise PaymentException('Must have a credit card to make a payment.')

        self._charge_credit_card(self.credit_card_number)
        payment = Payment(amount, self, target, note)
        self.activities.append(payment)
        target.activities.append(payment)
        target.add_to_balance(amount)

        return payment

    def pay_with_balance(self, target, amount, note):
        amount = float(amount)
        
        if self.username == target.username:
            raise PaymentException('User cannot pay themselves.')
            
        if amount <= 0.0:
            raise PaymentException('Amount must be a non-negative number.')
            
        if self.balance < amount:
            raise PaymentException('Insufficient balance.')
            
        payment = Payment(amount, self, target, note)
        self.activities.append(payment)
        target.activities.append(payment)
        self.balance -= amount
        target.add_to_balance(amount)
        
        return payment

    def _is_valid_credit_card(self, credit_card_number):
        return credit_card_number in ["4111111111111111", "4242424242424242"]

    def _is_valid_username(self, username):
        return re.match('^[A-Za-z0-9_\\-]{4,15}$', username)

    def _charge_credit_card(self, credit_card_number):
        # magic method that charges a credit card thru the card processor
        pass


class MiniVenmo:
    def create_user(self, username, balance, credit_card_number):
        user = User(username)
        user.add_to_balance(balance)
        user.add_credit_card(credit_card_number)
        return user

    def render_feed(self, feed):
        for activity in feed:
            if isinstance(activity, Payment):
                print(f"{activity.actor.username} paid {activity.target.username} ${activity.amount:.2f} for {activity.note}")
            elif isinstance(activity, FriendActivity):
                print(str(activity))

    @classmethod
    def run(cls):
        venmo = cls()

        bobby = venmo.create_user("Bobby", 5.00, "4111111111111111")
        carol = venmo.create_user("Carol", 10.00, "4242424242424242")

        try:
            # should complete using balance
            bobby.pay(carol, 5.00, "Coffee")
 
            # should complete using card
            carol.pay(bobby, 15.00, "Lunch")
        except PaymentException as e:
            print(e)

        feed = bobby.retrieve_feed()
        venmo.render_feed(feed)

        bobby.add_friend(carol)


class TestUser(unittest.TestCase):

    def test_this_works(self):
        with self.assertRaises(UsernameException):
            raise UsernameException()


if __name__ == '__main__':
    unittest.main()