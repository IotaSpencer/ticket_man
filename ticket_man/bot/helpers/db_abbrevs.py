import random

import sqlalchemy.engine
from sqlalchemy import delete, select
from sqlalchemy.engine import LegacyCursorResult, Result, ResultProxy, Row, ScalarResult

from ticket_man.db import async_session
from ticket_man.tables.tickets import TicketComments, TicketTypes, Tickets
from ticket_man.loggers import logger


async def get_ticket_type(type_: int) -> sqlalchemy.engine.ScalarResult:
    async with async_session() as session:
        result: Result = await session.execute(select(TicketTypes).where(TicketTypes.id == type_))
        return result.scalars().first()


async def submit_ticket(subject: str, content: str, type_: int, user_id: int) -> ResultProxy:
    async with async_session() as session:
        ticket = Tickets(subject=subject, content=content, type=type_, user_id=user_id, open=1)
        session.add(ticket)
        await session.commit()
        return ticket


async def submit_comment(content: str, ticket_id: int, user_id: int) -> ResultProxy:
    async with async_session() as session:
        comment = TicketComments(content=content, ticket_id=ticket_id, user_id=user_id)
        session.add(comment)
        await session.commit()
        return comment


async def get_all_user_tickets(user_id: int) -> ResultProxy:
    async with async_session() as session:
        result: Result = await session.execute(select(Tickets).where(Tickets.user_id == user_id))
        return result.scalars().all()


async def get_all_ticket_types() -> ResultProxy:
    async with async_session() as session:
        result: Result = await session.execute(select(TicketTypes))
        return result.scalars().all()


async def delete_comment(comment_id: int) -> ResultProxy:
    async with async_session() as session:
        result: Result = await session.execute(select(TicketComments).where(TicketComments.id == comment_id))
        comment = result.scalars().first()
        await session.delete(comment)
        await session.commit()
        return comment


async def close_ticket(ticket_id: int) -> ResultProxy:
    async with async_session() as session:
        result: Result = await session.execute(select(Tickets).where(Tickets.id == ticket_id))
        ticket = result.scalars().first()
        ticket.open = 0
        await session.commit()
        return ticket


async def open_ticket(ticket_id: int) -> ResultProxy:
    async with async_session() as session:
        result: Result = await session.execute(select(Tickets).where(Tickets.id == ticket_id))
        ticket = result.scalars().first()
        ticket.open = 1
        await session.commit()
        return ticket


async def delete_ticket(ticket_id: int) -> Result:
    ticket_id = int(ticket_id)
    async with async_session() as session:
        result: Result = await session.execute(delete(Tickets).where(Tickets.id == ticket_id))
        ticket: Result = result
        await session.commit()
        return ticket


async def get_ticket(ticket_id: int) -> Row | None:
    logger.info(f"Getting ticket {ticket_id}")
    logger.info(f"Expression: {select(Tickets).where(Tickets.id == ticket_id)}")
    async with async_session() as session:
        logger.info(f"Session: {session}")
        result: Result = await session.execute(select(Tickets).where(Tickets.id == ticket_id))
        return result.scalars().first()


async def get_ticket_comments(ticket_id: int) -> ResultProxy:
    async with async_session() as session:
        result: Result = await session.execute(select(TicketComments).where(TicketComments.ticket_id == ticket_id))
        return result.scalars().all()


async def get_ticket_comment(user_id: int, ticket_id, comment_id: int) -> ResultProxy:
    async with async_session() as session:
        result: Result = await session.execute(
                select(TicketComments).where(TicketComments.user_id == user_id).where(
                        TicketComments.id == comment_id).where(TicketComments.ticket_id == ticket_id))
        return result.scalars().first()


async def get_latest_ticket(user_id: int) -> ResultProxy:
    """Get the latest ticket submitted by a user."""
    async with async_session() as session:
        result: Result = await session.execute(select(Tickets).
                                               where(Tickets.user_id == user_id).
                                               order_by(Tickets.id.desc()).
                                               limit(1))
        return result.scalars().first()


async def get_latest_comment(user_id: int) -> ResultProxy:
    """Get the latest comment submitted by a user."""
    async with async_session() as session:
        result: Result = await session.execute(
                select(TicketComments).where(TicketComments.user_id == user_id).order_by(
                        TicketComments.id.desc()).limit(1))
        return result.scalars().first()


async def get_all_tickets() -> ResultProxy:
    async with async_session() as session:
        result: Result = await session.execute(select(Tickets))
        return result.scalars().all()


async def get_all_comments(user_id: int) -> ResultProxy:
    """Get all comments submitted by a user."""
    async with async_session() as session:
        result: Result = await session.execute(select(TicketComments).where(TicketComments.user_id == user_id))
        return result.scalars().all()


async def get_all_ticket_comments(user_id: int, ticket_id: int) -> ResultProxy:
    async with async_session() as session:
        result: Result = await session.execute(
                select(TicketComments).where(TicketComments.ticket_id == ticket_id).where(
                        TicketComments.user_id == user_id))
        return result.scalars().all()


async def add_test_tickets():
    tickets = []
    types = [1, 2, 3]
    user_ids = [262670376910747822, 467916770165755453, 575448016781326540, 197993111601441752, 395230262608817281,
                829953361890242500, 547718453325395413, 747486388667547174, 421634262213051747, 354674777000292196,
                177143297927334701, 929285580208420173, 621011931570644422, 940727468471816922, 134262611429348418,
                245831269909774511, 911292657751367422, 369534440822930157, 320165189743868480, 285251052507144996,
                479432194990490714, 655538827932465465, 289617900497750475, 844296189796459407, 523118186129495291,
                800311739453389531, 182193290262853103, 237950146898707000, 428327761585935474, 780170496492303041,
                153123592595914028, 654325019422189701, 135072283982289361, 753471202268120026, 309993301572827027,
                393721330610864792, 222786199019635427, 509578633744674179, 200089455228135714, 939068325651973227,
                246843781618168053, 469130110172820049, 283906448342920933, 615324224094067528, 628913430316449342,
                968395879126343459, 721238635835693775, 675014513318900687, 515148267376143534, 165997614239587272,
                515382758075267535, 694416234622564606, 523499505776649696, 679742507964914934, 241170856540836081,
                645128101774915588, 454958919364842776, 242019367634702359, 311932423381912394, 418706531356152788,
                888675646305958334, 860304076904070483, 560594861965876416, 505715222122319120, 970527950205282434,
                516277272588503411, 927704256984319475, 637679388902162524, 800395548465864237, 653861478477842588,
                366067378996512585, 754828067181767240, 506584622085811230, 695516203866156410, 785483450539238088,
                717057834092559851, 291605548011703987, 178073451104369817, 745911266898633820, 214506216026168763,
                543532896003913058, 895735624270068656, 684047526030692370, 296461642181793779, 856392808042520579,
                601827395221522327, 487902730876941596, 187971164397631485, 329466321449147009, 551652085117167516,
                134563611840428336, 858296356866234127, 912562620948889390, 243164176873241619, 926390860133783367,
                288291022312940143, 392887014069653358, 397010133209449625, 114052392637120978, 635573515507626076,
                766005490148643720, 869805278317343941, 739228380265261870, 531333282288063713, 438741405734555633,
                526404738245937684, 832502513667608023, 472195024404860379, 593616853633093352, 655170285843513722,
                379500823762467028, 362222806636806303, 172441911099102835, 331240737807856351, 907660280255544932,
                570517397259297285, 437985461083146222, 170056024788242507, 435725451118403969, 175323403287312899,
                128629008992562662, 794933648730326646, 528150981140319730, 653094870839820232, 757327824202768075,
                133201515807290231, 931596603161334435, 589248560204620291, 247100646285926584, 901328960878423536,
                965932032223611092, 625208244374934889, 470622811889690282, 703627025616227067, 304556638521447670,
                237658065231518467, 665533791613604709, 321755702206867668, 531682693066790314, 463385286615331689,
                879824917372717786, 797725697622842853, 447294868763657163, 661277042359623626, 180175970657451151,
                631885516477685357, 951390102235583683, 845165112567532508, 912840030363838759, 601506736622477914,
                502355979119798633, 930682721995404138, 100469239919007314, 726178120132660455, 706449225654785897,
                902612450641160473, 710524954408122372, 441746987189573990, 348159854782085671, 628418651273327285,
                921438402082153122, 409673497562986102, 240741217092500398, 697388976980399789, 613078675937925034,
                558907946641065018, 593266232442181559, 559868003313152670, 910214902452574408, 285162838370432358,
                199396287636368431, 472315872705415020, 797785038647265820, 759809143657088031, 488672500990268001,
                268533802003497045, 517723452101545924, 372658007224698873, 359619436215847307, 577131637459588438,
                816910891312051952, 598002555418691100, 880004247461929725, 832650973410519610, 253720922168754944,
                296753225243859402, 314240160164772616, 327775661758198861, 345297957980967426, 681646961617824826,
                306835461816804829, 386287683194064751, 839229896837741613, 237162328501451892, 350220119694185158,
                798623853902720037, 226787198895099811, 375959449175732347, 198299247841436436, 350139865250758532]
    async with async_session() as session:
        for i in user_ids:
            type_ = random.choice(types)
            ticket = Tickets(subject=f"Test Ticket {i} + {type_}", content=f"Test Content {i}", type=type_, user_id=i,
                             open=1)
            session.add(ticket)

        await session.commit()
        return True
