import random

from .db_funcs import *


def add_test_tickets():
    """Add test tickets to the database."""
    types = [1, 2, 3]
    numbers = '0123456789'
    with session() as sess:
        for i in range(100):
            user_id = int(''.join(random.choices(numbers, k=18)))
            type_ = random.choice(types)
            ticket = Tickets(subject=f"Test Ticket {i} + {type_}", content=f"Test Content {i}", type=type_,
                             user_id=user_id,
                             open=1)
            sess.add(ticket)

        sess.commit()
        return True


def add_test_comments():
    """Add test comments to the database."""
    with session() as sess:
        for i in range(100):
            user_id = int(''.join(random.choices(numbers, k=18)))
            ticket_id = random.randint(1, 100)
            comment = TicketComments(content=f"Test Comment {i}", ticket_id=ticket_id, user_id=user_id)
            sess.add(comment)

        sess.commit()
        return True
