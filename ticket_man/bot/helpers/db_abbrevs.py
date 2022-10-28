import random
from . import dummy_gen
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
        for i in range(31):
            user_choice = random.choice(dummy_gen.user_data()[0])
            admin_choice = random.choice(dummy_gen.user_data()[1])
            user_id, ticket_id = user_choice.id, user_choice.ticket_id
            admin_id = admin_choice.id
            pass_ = random.randint(10000000000000000000, 99999999999999999999)
            admin_comment = TicketComments(content=f"Test Admin Comment {pass_}", ticket_id=ticket_id, user_id=admin_id)
            comment = TicketComments(content=f"Test User Comment {pass_}", ticket_id=ticket_id, user_id=user_id)
            sess.add(admin_comment)
            sess.add(comment)

        sess.commit()
        return True
