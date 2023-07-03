import datetime
from flask import Flask, redirect, render_template, request, session, url_for, Response, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import os
import re


current_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + \
    os.path.join(current_dir, "edelweiss_hackathon.sqlite3")
app.config['SECRET_KEY'] = 'thisismysecretkey'
db = SQLAlchemy(app)
api = Api(app)
CORS(app)


class All_expiry_symbols_meta(db.Model):
    __tablename__ = 'all_expiry_symbols_meta'
    symbol = db.Column(db.String, nullable=False, primary_key=True)
    expiry_date = db.Column(db.DateTime, nullable=False, primary_key=True)
    call = db.Column(db.Integer, default=0)
    put = db.Column(db.Integer, default=0)
    future = db.Column(db.Integer, default=0)


class Futures(db.Model):
    __tablename__ = 'futures'
    symbol = db.Column(db.String, nullable=False, primary_key=True)
    expiry_date = db.Column(db.DateTime, nullable=False, primary_key=True)
    LTP = db.Column(db.Integer, nullable=False)
    LTQ = db.Column(db.Integer, nullable=False)
    totalTradedVolume = db.Column(db.Integer, nullable=False)
    bestBid = db.Column(db.Integer, nullable=False)
    bestAsk = db.Column(db.Integer, nullable=False)
    bestBidQty = db.Column(db.Integer, nullable=False)
    bestAskQty = db.Column(db.Integer, nullable=False)
    openInterest = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.String, nullable=False)
    sequence = db.Column(db.Integer, nullable=False)
    prevClosePrice = db.Column(db.Integer, nullable=False)
    prevOpenInterest = db.Column(db.Integer, nullable=False)


class Calls(db.Model):
    __tablename__ = 'calls'
    symbol = db.Column(db.String, nullable=False, primary_key=True)
    expiry_date = db.Column(db.DateTime, nullable=False, primary_key=True)
    strike_price = db.Column(db.Integer, nullable=False, primary_key=True)
    LTP = db.Column(db.Integer, nullable=False)
    LTQ = db.Column(db.Integer, nullable=False)
    totalTradedVolume = db.Column(db.Integer, nullable=False)
    bestBid = db.Column(db.Integer, nullable=False)
    bestAsk = db.Column(db.Integer, nullable=False)
    bestBidQty = db.Column(db.Integer, nullable=False)
    bestAskQty = db.Column(db.Integer, nullable=False)
    openInterest = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.String, nullable=False)
    sequence = db.Column(db.Integer, nullable=False)
    prevClosePrice = db.Column(db.Integer, nullable=False)
    prevOpenInterest = db.Column(db.Integer, nullable=False)


class Puts(db.Model):
    __tablename__ = 'puts'
    symbol = db.Column(db.String, nullable=False, primary_key=True)
    expiry_date = db.Column(db.DateTime, nullable=False, primary_key=True)
    strike_price = db.Column(db.Integer, nullable=False, primary_key=True)
    LTP = db.Column(db.Integer, nullable=False)
    LTQ = db.Column(db.Integer, nullable=False)
    totalTradedVolume = db.Column(db.Integer, nullable=False)
    bestBid = db.Column(db.Integer, nullable=False)
    bestAsk = db.Column(db.Integer, nullable=False)
    bestBidQty = db.Column(db.Integer, nullable=False)
    bestAskQty = db.Column(db.Integer, nullable=False)
    openInterest = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.String, nullable=False)
    sequence = db.Column(db.Integer, nullable=False)
    prevClosePrice = db.Column(db.Integer, nullable=False)
    prevOpenInterest = db.Column(db.Integer, nullable=False)


class Indexes(db.Model):
    __tablename__ = 'indexes'
    symbol = db.Column(db.String, nullable=False, primary_key=True)
    LTP = db.Column(db.Integer, nullable=False)
    LTQ = db.Column(db.Integer, nullable=False)
    totalTradedVolume = db.Column(db.Integer, nullable=False)
    bestBid = db.Column(db.Integer, nullable=False)
    bestAsk = db.Column(db.Integer, nullable=False)
    bestBidQty = db.Column(db.Integer, nullable=False)
    bestAskQty = db.Column(db.Integer, nullable=False)
    openInterest = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.String, nullable=False)
    sequence = db.Column(db.Integer, nullable=False)
    prevClosePrice = db.Column(db.Integer, nullable=False)
    prevOpenInterest = db.Column(db.Integer, nullable=False)


def intrensic_value():
    return (-100)


def date_converter_to_output_format(input_date):
    input_date = str(input_date).strip().split('-')
    month_dict = {1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN',
                  7: 'JUL', 8: 'AUG', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DEC'}
    return (input_date[-1]+month_dict[int(input_date[1])]+input_date[0][-2:])


def input_date_to_system_format(input_data):
    input_data_date = input_data[0:2]
    input_data_month = input_data[2:5]
    input_data_year = input_data[5:]
    months_dict = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05',
                   'JUN': '06', 'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}
    month_num = months_dict[input_data_month]
    current_year = datetime.datetime.now().year
    current_year = str(current_year)[0:2]
    formated_expiry_date = str(
        current_year+input_data_year+"-"+month_num+"-"+input_data_date)+" 15:15:00"
    date_format = "%Y-%m-%d %H:%M:%S"
    datetime_object = datetime.datetime.strptime(
        formated_expiry_date, date_format)
    return (datetime_object)


def contains_only_letters(input_string):
    pattern = r'^[a-zA-Z]+$'
    match = re.match(pattern, input_string)
    return match is not None


def contains_only_numerical(string):
    return re.match(r'^\d+$', string) is not None


def symbolexists(symbol):
    if (All_expiry_symbols_meta.query.filter(All_expiry_symbols_meta.symbol == symbol).first()):
        return True
    else:
        return False


class Symbol_date_option_API(Resource):
    def get(self, symbol, expiry):
        if (symbolexists(symbol)):
            if ((len(expiry) == 7) and (contains_only_numerical(expiry[0:2])) and (contains_only_letters(expiry[2:5])) and (contains_only_numerical(expiry[5:]))):
                all_expiry_for_symbol = All_expiry_symbols_meta.query.with_entities(All_expiry_symbols_meta.expiry_date).filter(All_expiry_symbols_meta.symbol == symbol and (
                    All_expiry_symbols_meta.put == 1 or All_expiry_symbols_meta.call == 1)).order_by(All_expiry_symbols_meta.expiry_date).distinct()
                if (all_expiry_for_symbol):
                    all_symbols = All_expiry_symbols_meta.query.with_entities(
                        All_expiry_symbols_meta.symbol).order_by(All_expiry_symbols_meta.symbol).distinct()
                    if (all_symbols):
                        all_strike_price_call = Calls.query.with_entities(Calls.strike_price).filter(
                            Calls.symbol == symbol).order_by(Calls.strike_price).distinct()
                        all_strike_price_put = Puts.query.with_entities(Puts.strike_price).filter(
                            Puts.symbol == symbol).order_by(Puts.strike_price).distinct()
                        if (all_strike_price_call or all_strike_price_put):
                            symbols = []
                            for i in all_symbols:
                                symbols.append(i.symbol)
                            all_dates = []
                            for i in all_expiry_for_symbol:
                                all_dates.append(
                                    date_converter_to_output_format(i.expiry_date.date()))
                            all_strike_price = []
                            for i in all_strike_price_call:
                                all_strike_price.append(int(i.strike_price))
                            for i in all_strike_price_put:
                                all_strike_price.append(int(i.strike_price))
                            all_strike_price = list(set(all_strike_price))
                            all_strike_price = sorted(all_strike_price)
                            final = []
                            oi_call_total = 0
                            oi_put_total = 0
                            volumn_call_total = 0
                            volumn_put_total = 0
                            expiry = input_date_to_system_format(expiry)
                            symbol_call_option_available = All_expiry_symbols_meta.query.filter(
                                All_expiry_symbols_meta.symbol == symbol, All_expiry_symbols_meta.expiry_date == expiry, All_expiry_symbols_meta.call == 1).first()
                            # Cannot perform join where a certain entity in the put or call column doesn't exists and we have to put in some default value in that case.
                            if (symbol_call_option_available):
                                symbol_calls = Calls.query.with_entities(Calls.openInterest, Calls.prevOpenInterest, Calls.LTQ, Calls.LTP, Calls.prevClosePrice, Calls.bestBid, Calls.bestBidQty,
                                                                         Calls.bestAsk, Calls.bestAskQty, Calls.strike_price).filter(Calls.symbol == symbol, Calls.expiry_date == expiry).order_by(Calls.strike_price).all()
                                for i in symbol_calls:
                                    symbol_put = Puts.query.with_entities(Puts.bestBidQty, Puts.bestBid, Puts.bestAsk, Puts.bestAskQty, Puts.prevClosePrice, Puts.LTP, Puts.LTQ, Puts.prevOpenInterest, Puts.openInterest).filter(
                                        Puts.symbol == symbol, Puts.expiry_date == expiry, Puts.strike_price == i.strike_price).first()
                                    if (symbol_put):
                                        oi_call_total = oi_call_total + \
                                            int(i.openInterest)
                                        oi_put_total = oi_put_total + \
                                            int(symbol_put.openInterest)
                                        volumn_call_total = volumn_call_total + \
                                            int(i.LTQ)
                                        volumn_put_total = volumn_put_total + \
                                            int(symbol_put.LTQ)
                                        final.append({'oi_c': i.openInterest, 'oi_change_c': (i.openInterest-i.prevOpenInterest), 'volume_c': i.LTQ, 'iv_c': intrensic_value(), 'ltp_c': (i.LTP/100), 'change_c': ((i.LTQ-i.prevClosePrice)/100), 'bidqty_c': i.bestBidQty, 'bid_c': i.bestBid, 'ask_c': i.bestAsk, 'askqty_c': i.bestAskQty, 'strike_price': i.strike_price, 'bidqty_p': symbol_put.bestBidQty,
                                                     'bid_p': symbol_put.bestBid, 'ask_p': symbol_put.bestAsk, 'askqty_p': symbol_put.bestAskQty, 'change_p': ((symbol_put.prevClosePrice-symbol_put.prevClosePrice)/100), 'ltp_p': (symbol_put.LTP/100), 'iv_p': intrensic_value(), 'volume_p': symbol_put.LTQ, 'oi_change_p': (symbol_put.prevOpenInterest-symbol_put.openInterest), 'oi_p': symbol_put.openInterest})
                                    else:
                                        oi_call_total = oi_call_total + \
                                            int(i.openInterest)
                                        oi_put_total = oi_put_total+0
                                        volumn_call_total = volumn_call_total + \
                                            int(i.LTQ)
                                        volumn_put_total = volumn_put_total+0
                                        final.append({'oi_c': i.openInterest, 'oi_change_c': (i.openInterest-i.prevOpenInterest), 'volume_c': i.LTQ, 'iv_c': intrensic_value(), 'ltp_c': (i.LTP/100), 'change_c': ((i.LTQ-i.prevClosePrice)/100), 'bidqty_c': i.bestBidQty, 'bid_c': i.bestBid,
                                                     'ask_c': i.bestAsk, 'askqty_c': i.bestAskQty, 'strike_price': i.strike_price, 'bidqty_p': 'NA', 'bid_p': 0, 'ask_p': 0, 'askqty_p': 'NA', 'change_p': 'NA', 'ltp_p': 0, 'iv_p': intrensic_value(), 'volume_p': 'NA', 'oi_change_p': 'NA', 'oi_p': -1})
                                return ({'symbols': symbols, 'expiry_dates': all_dates, 'strike_price': all_strike_price, 'data': final, 'oi_call_total': oi_call_total, 'oi_put_total': oi_put_total, 'volumn_call_total': volumn_call_total, 'volumn_put_total': volumn_put_total})
                            else:
                                symbol_put_option_available = All_expiry_symbols_meta.query.filter(
                                    All_expiry_symbols_meta.symbol == symbol, All_expiry_symbols_meta.expiry_date == expiry, All_expiry_symbols_meta.put == 1).first()
                                if (symbol_put_option_available):
                                    symbol_puts = Puts.query.with_entities(Puts.openInterest, Puts.prevOpenInterest, Puts.LTQ, Puts.LTP, Puts.prevClosePrice, Puts.bestBid, Puts.bestBidQty,
                                                                           Puts.bestAsk, Puts.bestAskQty, Puts.strike_price).filter(Puts.symbol == symbol, Puts.expiry_date == expiry).order_by(Puts.strike_price).all()
                                    for i in symbol_puts:
                                        symbol_call = Calls.query.with_entities(Calls.bestBidQty, Calls.bestBid, Calls.bestAsk, Calls.bestAskQty, Calls.prevClosePrice, Calls.LTP, Calls.LTQ, Calls.prevOpenInterest, Calls.openInterest).filter(
                                            Calls.symbol == symbol, Calls.expiry_date == expiry, Calls.strike_price == i.strike_price).first()
                                        if (symbol_call):
                                            oi_call_total = oi_call_total + \
                                                int(i.openInterest)
                                            oi_put_total = oi_put_total + \
                                                int(symbol_call.openInterest)
                                            volumn_call_total = volumn_call_total + \
                                                int(i.LTQ)
                                            volumn_put_total = volumn_put_total + \
                                                int(symbol_call.LTQ)
                                            final.append({'oi_c': symbol_call.openInterest, 'oi_change_c': (symbol_call.openInterest-symbol_call.prevOpenInterest), 'volume_c': symbol_call.LTQ, 'iv_c': intrensic_value(), 'ltp_c': (i.LTP/100), 'change_c': ((symbol_call.LTQ-i.prevClosePrice)/100), 'bidqty_c': symbol_call.bestBidQty, 'bid_c': symbol_call.bestBid, 'ask_c': symbol_call.bestAsk,
                                                         'askqty_c': symbol_call.bestAskQty, 'strike_price': i.strike_price, 'bidqty_p': i.bestBidQty, 'bid_p': i.bestBid, 'ask_p': i.bestAsk, 'askqty_p': i.bestAskQty, 'change_p': ((i.prevClosePrice-i.prevClosePrice)/100), 'ltp_p': (i.LTP/100), 'iv_p': intrensic_value(), 'volume_p': i.LTQ, 'oi_change_p': (i.prevOpenInterest-i.openInterest), 'oi_p': i.openInterest})
                                        else:
                                            oi_call_total = oi_call_total+0
                                            oi_put_total = oi_put_total + \
                                                int(symbol.openInterest)
                                            volumn_call_total = volumn_call_total+0
                                            volumn_put_total = volumn_put_total + \
                                                int(symbol.LTQ)
                                            final.append({'oi_c': -1, 'oi_change_c': 'NA', 'volume_c': 'NA', 'iv_c': intrensic_value(), 'ltp_c': 0, 'change_c': 'NA', 'bidqty_c': 'NA', 'bid_c': 0, 'ask_c': 0, 'askqty_c': 'NA', 'strike_price': i.strike_price, 'bidqty_p': i.bestBidQty, 'bid_p': i.bestBid,
                                                         'ask_p': i.bestAsk, 'askqty_p': i.bestAskQty, 'change_p': ((i.prevClosePrice-i.prevClosePrice)/100), 'ltp_p': (i.LTP/100), 'iv_p': intrensic_value(), 'volume_p': i.LTQ, 'oi_change_p': (i.prevOpenInterest-i.openInterest), 'oi_p': i.openInterest})
                                    return ({'symbols': symbols, 'expiry_dates': all_dates, 'strike_price': all_strike_price, 'data': final, 'oi_call_total': oi_call_total, 'oi_put_total': oi_put_total, 'volumn_call_total': volumn_call_total, 'volumn_put_total': volumn_put_total})
                                else:
                                    return ({"E006 : True"})
                        else:
                            return ({'E005 : True'})
                    else:
                        return ({'E004:True'})
                else:
                    return ("E003 : True")
            else:
                return ("E002 : True")
        else:
            return ("E001 : True")


class Symbol_price_option_API(Resource):
    def get(self, symbol, price):
        if (symbolexists(symbol)):
            if (contains_only_numerical(price)):
                price = int(price)
                all_expiry_for_symbol = All_expiry_symbols_meta.query.with_entities(All_expiry_symbols_meta.expiry_date).filter(All_expiry_symbols_meta.symbol == symbol and (
                    All_expiry_symbols_meta.put == 1 or All_expiry_symbols_meta.call == 1)).order_by(All_expiry_symbols_meta.expiry_date).distinct()
                if (all_expiry_for_symbol):
                    all_symbols = All_expiry_symbols_meta.query.with_entities(
                        All_expiry_symbols_meta.symbol).order_by(All_expiry_symbols_meta.symbol).distinct()
                    if (all_symbols):
                        all_strike_price_call = Calls.query.with_entities(Calls.strike_price).filter(
                            Calls.symbol == symbol).order_by(Calls.strike_price).distinct()
                        all_strike_price_put = Puts.query.with_entities(Puts.strike_price).filter(
                            Puts.symbol == symbol).order_by(Puts.strike_price).distinct()
                        if (all_strike_price_call or all_strike_price_put):
                            symbols = []
                            for i in all_symbols:
                                symbols.append(i.symbol)
                            all_dates = []
                            for i in all_expiry_for_symbol:
                                all_dates.append(
                                    date_converter_to_output_format(i.expiry_date.date()))
                            all_strike_price = []
                            for i in all_strike_price_call:
                                all_strike_price.append(int(i.strike_price))
                            for i in all_strike_price_put:
                                all_strike_price.append(int(i.strike_price))
                            all_strike_price = list(set(all_strike_price))
                            all_strike_price = sorted(all_strike_price)
                            final = []
                            oi_call_total = 0
                            oi_put_total = 0
                            volumn_call_total = 0
                            volumn_put_total = 0
                            symbol_call_option_available = All_expiry_symbols_meta.query.filter(
                                All_expiry_symbols_meta.symbol == symbol, All_expiry_symbols_meta.call == 1).first()
                            # Cannot perform join where a certain entity in the put or call column doesn't exists and we have to put in some default value in that case.
                            if (symbol_call_option_available):
                                symbol_calls = Calls.query.with_entities(Calls.openInterest, Calls.prevOpenInterest, Calls.LTQ, Calls.LTP, Calls.prevClosePrice, Calls.bestBid, Calls.bestBidQty,
                                                                         Calls.bestAsk, Calls.bestAskQty, Calls.expiry_date).filter(Calls.symbol == symbol, Calls.strike_price == price).order_by(Calls.expiry_date).all()
                                for i in symbol_calls:
                                    symbol_put = Puts.query.with_entities(Puts.bestBidQty, Puts.bestBid, Puts.bestAsk, Puts.bestAskQty, Puts.prevClosePrice, Puts.LTP, Puts.LTQ, Puts.prevOpenInterest, Puts.openInterest).filter(
                                        Puts.symbol == symbol, Puts.strike_price == price, Puts.expiry_date == i.expiry_date).first()
                                    if (symbol_put):
                                        oi_call_total = oi_call_total + \
                                            int(i.openInterest)
                                        oi_put_total = oi_put_total + \
                                            int(symbol_put.openInterest)
                                        volumn_call_total = volumn_call_total + \
                                            int(i.LTQ)
                                        volumn_put_total = volumn_put_total + \
                                            int(symbol_put.LTQ)
                                        final.append({'oi_c': i.openInterest, 'oi_change_c': (i.openInterest-i.prevOpenInterest), 'volume_c': i.LTQ, 'iv_c': intrensic_value(), 'ltp_c': (i.LTP/100), 'change_c': ((i.LTQ-i.prevClosePrice)/100), 'bidqty_c': i.bestBidQty, 'bid_c': i.bestBid, 'ask_c': i.bestAsk, 'askqty_c': i.bestAskQty, 'expiry_date': date_converter_to_output_format(i.expiry_date.date(
                                        )), 'bidqty_p': symbol_put.bestBidQty, 'bid_p': symbol_put.bestBid, 'ask_p': symbol_put.bestAsk, 'askqty_p': symbol_put.bestAskQty, 'change_p': ((symbol_put.prevClosePrice-symbol_put.prevClosePrice)/100), 'ltp_p': (symbol_put.LTP/100), 'iv_p': intrensic_value(), 'volume_p': symbol_put.LTQ, 'oi_change_p': (symbol_put.prevOpenInterest-symbol_put.openInterest), 'oi_p': symbol_put.openInterest})
                                    else:
                                        oi_call_total = oi_call_total + \
                                            int(i.openInterest)
                                        oi_put_total = oi_put_total+0
                                        volumn_call_total = volumn_call_total + \
                                            int(i.LTQ)
                                        volumn_put_total = volumn_put_total+0
                                        final.append({'oi_c': i.openInterest, 'oi_change_c': (i.openInterest-i.prevOpenInterest), 'volume_c': i.LTQ, 'iv_c': intrensic_value(), 'ltp_c': (i.LTP/100), 'change_c': ((i.LTQ-i.prevClosePrice)/100), 'bidqty_c': i.bestBidQty, 'bid_c': i.bestBid, 'ask_c': i.bestAsk,
                                                     'askqty_c': i.bestAskQty, 'expiry_date': date_converter_to_output_format(i.expiry_date.date()), 'bidqty_p': 'NA', 'bid_p': 0, 'ask_p': 0, 'askqty_p': 'NA', 'change_p': 'NA', 'ltp_p': 0, 'iv_p': intrensic_value(), 'volume_p': 'NA', 'oi_change_p': 'NA', 'oi_p': -1})
                                return ({'symbols': symbols, 'expiry_dates': all_dates, 'strike_price': all_strike_price, 'data': final, 'oi_call_total': oi_call_total, 'oi_put_total': oi_put_total, 'volumn_call_total': volumn_call_total, 'volumn_put_total': volumn_put_total})
                            else:
                                symbol_put_option_available = All_expiry_symbols_meta.query.filter(
                                    All_expiry_symbols_meta.symbol == symbol, All_expiry_symbols_meta.put == 1).first()
                                if (symbol_put_option_available):
                                    symbol_puts = Puts.query.with_entities(Puts.openInterest, Puts.prevOpenInterest, Puts.LTQ, Puts.LTP, Puts.prevClosePrice, Puts.bestBid, Puts.bestBidQty,
                                                                           Puts.bestAsk, Puts.bestAskQty, Puts.expiry_date).filter(Puts.symbol == symbol, Puts.strike_price == price).order_by(Puts.expiry_date).all()
                                    for i in symbol_puts:
                                        symbol_call = Calls.query.with_entities(Calls.bestBidQty, Calls.bestBid, Calls.bestAsk, Calls.bestAskQty, Calls.prevClosePrice, Calls.LTP, Calls.LTQ, Calls.prevOpenInterest, Calls.openInterest).filter(
                                            Calls.symbol == symbol, Calls.expiry_date == i.expiry_date, Calls.strike_price == i.price).first()
                                        if (symbol_call):
                                            oi_call_total = oi_call_total + \
                                                int(i.openInterest)
                                            oi_put_total = oi_put_total + \
                                                int(symbol_call.openInterest)
                                            volumn_call_total = volumn_call_total + \
                                                int(i.LTQ)
                                            volumn_put_total = volumn_put_total + \
                                                int(symbol_call.LTQ)
                                            final.append({'oi_c': symbol_call.openInterest, 'oi_change_c': (symbol_call.openInterest-symbol_call.prevOpenInterest), 'volume_c': symbol_call.LTQ, 'iv_c': intrensic_value(), 'ltp_c': (i.LTP/100), 'change_c': ((symbol_call.LTQ-i.prevClosePrice)/100), 'bidqty_c': symbol_call.bestBidQty, 'bid_c': symbol_call.bestBid, 'ask_c': symbol_call.bestAsk, 'askqty_c': symbol_call.bestAskQty,
                                                         'expiry_date': date_converter_to_output_format(i.expiry_date.date()), 'bidqty_p': i.bestBidQty, 'bid_p': i.bestBid, 'ask_p': i.bestAsk, 'askqty_p': i.bestAskQty, 'change_p': ((i.prevClosePrice-i.prevClosePrice)/100), 'ltp_p': (i.LTP/100), 'iv_p': intrensic_value(), 'volume_p': i.LTQ, 'oi_change_p': (i.prevOpenInterest-i.openInterest), 'oi_p': i.openInterest})
                                        else:
                                            oi_call_total = oi_call_total+0
                                            oi_put_total = oi_put_total + \
                                                int(symbol.openInterest)
                                            volumn_call_total = volumn_call_total+0
                                            volumn_put_total = volumn_put_total + \
                                                int(symbol.LTQ)
                                            final.append({'oi_c': -1, 'oi_change_c': 'NA', 'volume_c': 'NA', 'iv_c': intrensic_value(), 'ltp_c': 0, 'change_c': 'NA', 'bidqty_c': 'NA', 'bid_c': 0, 'ask_c': 0, 'askqty_c': 'NA', 'expiry_date': date_converter_to_output_format(i.expiry_date.date()), 'bidqty_p': i.bestBidQty,
                                                         'bid_p': i.bestBid, 'ask_p': i.bestAsk, 'askqty_p': i.bestAskQty, 'change_p': ((i.prevClosePrice-i.prevClosePrice)/100), 'ltp_p': (i.LTP/100), 'iv_p': intrensic_value(), 'volume_p': i.LTQ, 'oi_change_p': (i.prevOpenInterest-i.openInterest), 'oi_p': i.openInterest})
                                    return ({'symbols': symbols, 'expiry_dates': all_dates, 'strike_price': all_strike_price, 'data': final, 'oi_call_total': oi_call_total, 'oi_put_total': oi_put_total, 'volumn_call_total': volumn_call_total, 'volumn_put_total': volumn_put_total})
                                else:
                                    return ({"E006 : True"})
                        else:
                            return ({'E005 : True'})
                    else:
                        return ({'E004:True'})
                else:
                    return ("E003 : True")
            else:
                return ("E007 : True")
        else:
            return ("E001 : True")


class Mounting_api(Resource):
    def get(self):
        symbol = 'MAINIDX'
        expiry = All_expiry_symbols_meta.query.with_entities(All_expiry_symbols_meta.expiry_date).filter(
            All_expiry_symbols_meta.symbol == symbol and All_expiry_symbols_meta.call == 1 and All_expiry_symbols_meta.put == 1 and All_expiry_symbols_meta.future == 1).order_by(All_expiry_symbols_meta.expiry_date).first()
        if (expiry):
            all_expiry_for_symbol = All_expiry_symbols_meta.query.with_entities(All_expiry_symbols_meta.expiry_date).filter(All_expiry_symbols_meta.symbol == symbol and (
                All_expiry_symbols_meta.put == 1 or All_expiry_symbols_meta.call == 1)).order_by(All_expiry_symbols_meta.expiry_date).distinct()
            if (all_expiry_for_symbol):
                all_symbols = All_expiry_symbols_meta.query.with_entities(
                    All_expiry_symbols_meta.symbol).order_by(All_expiry_symbols_meta.symbol).distinct()
                if (all_symbols):
                    all_strike_price_call = Calls.query.with_entities(Calls.strike_price).filter(
                        Calls.symbol == symbol).order_by(Calls.strike_price).distinct()
                    all_strike_price_put = Puts.query.with_entities(Puts.strike_price).filter(
                        Puts.symbol == symbol).order_by(Puts.strike_price).distinct()
                    if (all_strike_price_call or all_strike_price_put):
                        symbols = []
                        for i in all_symbols:
                            symbols.append(i.symbol)
                        all_dates = []
                        for i in all_expiry_for_symbol:
                            all_dates.append(
                                date_converter_to_output_format(i.expiry_date.date()))
                        all_strike_price = []
                        for i in all_strike_price_call:
                            all_strike_price.append(int(i.strike_price))
                        for i in all_strike_price_put:
                            all_strike_price.append(int(i.strike_price))
                        all_strike_price = list(set(all_strike_price))
                        all_strike_price = sorted(all_strike_price)
                        final = []
                        oi_call_total = 0
                        oi_put_total = 0
                        volumn_call_total = 0
                        volumn_put_total = 0
                        symbol_call_option_available = All_expiry_symbols_meta.query.filter(
                            All_expiry_symbols_meta.symbol == symbol, All_expiry_symbols_meta.expiry_date == expiry.expiry_date, All_expiry_symbols_meta.call == 1).first()
                        # Cannot perform join where a certain entity in the put or call column doesn't exists and we have to put in some default value in that case.
                        if (symbol_call_option_available):
                            symbol_calls = Calls.query.with_entities(Calls.openInterest, Calls.prevOpenInterest, Calls.LTQ, Calls.LTP, Calls.prevClosePrice, Calls.bestBid, Calls.bestBidQty,
                                                                     Calls.bestAsk, Calls.bestAskQty, Calls.strike_price).filter(Calls.symbol == symbol, Calls.expiry_date == expiry.expiry_date).order_by(Calls.strike_price).all()
                            for i in symbol_calls:
                                symbol_put = Puts.query.with_entities(Puts.bestBidQty, Puts.bestBid, Puts.bestAsk, Puts.bestAskQty, Puts.prevClosePrice, Puts.LTP, Puts.LTQ, Puts.prevOpenInterest, Puts.openInterest).filter(
                                    Puts.symbol == symbol, Puts.expiry_date == expiry.expiry_date, Puts.strike_price == i.strike_price).first()
                                if (symbol_put):
                                    oi_call_total = oi_call_total + \
                                        int(i.openInterest)
                                    oi_put_total = oi_put_total + \
                                        int(symbol_put.openInterest)
                                    volumn_call_total = volumn_call_total + \
                                        int(i.LTQ)
                                    volumn_put_total = volumn_put_total + \
                                        int(symbol_put.LTQ)
                                    final.append({'oi_c': i.openInterest, 'oi_change_c': (i.openInterest-i.prevOpenInterest), 'volume_c': i.LTQ, 'iv_c': intrensic_value(), 'ltp_c': (i.LTP/100), 'change_c': ((i.LTQ-i.prevClosePrice)/100), 'bidqty_c': i.bestBidQty, 'bid_c': i.bestBid, 'ask_c': i.bestAsk, 'askqty_c': i.bestAskQty, 'strike_price': i.strike_price, 'bidqty_p': symbol_put.bestBidQty,
                                                 'bid_p': symbol_put.bestBid, 'ask_p': symbol_put.bestAsk, 'askqty_p': symbol_put.bestAskQty, 'change_p': ((symbol_put.prevClosePrice-symbol_put.prevClosePrice)/100), 'ltp_p': (symbol_put.LTP/100), 'iv_p': intrensic_value(), 'volume_p': symbol_put.LTQ, 'oi_change_p': (symbol_put.prevOpenInterest-symbol_put.openInterest), 'oi_p': symbol_put.openInterest})
                                else:
                                    oi_call_total = oi_call_total + \
                                        int(i.openInterest)
                                    oi_put_total = oi_put_total+0
                                    volumn_call_total = volumn_call_total + \
                                        int(i.LTQ)
                                    volumn_put_total = volumn_put_total+0
                                    final.append({'oi_c': i.openInterest, 'oi_change_c': (i.openInterest-i.prevOpenInterest), 'volume_c': i.LTQ, 'iv_c': intrensic_value(), 'ltp_c': (i.LTP/100), 'change_c': ((i.LTQ-i.prevClosePrice)/100), 'bidqty_c': i.bestBidQty, 'bid_c': i.bestBid,
                                                 'ask_c': i.bestAsk, 'askqty_c': i.bestAskQty, 'strike_price': i.strike_price, 'bidqty_p': 'NA', 'bid_p': 0, 'ask_p': 0, 'askqty_p': 'NA', 'change_p': 'NA', 'ltp_p': 0, 'iv_p': intrensic_value(), 'volume_p': 'NA', 'oi_change_p': 'NA', 'oi_p': -1})
                            return ({'symbols': symbols, 'expiry_dates': all_dates, 'strike_price': all_strike_price, 'data': final, 'oi_call_total': oi_call_total, 'oi_put_total': oi_put_total, 'volumn_call_total': volumn_call_total, 'volumn_put_total': volumn_put_total})
                        else:
                            symbol_put_option_available = All_expiry_symbols_meta.query.filter(
                                All_expiry_symbols_meta.symbol == symbol, All_expiry_symbols_meta.expiry_date == expiry.expiry_date, All_expiry_symbols_meta.put == 1).first()
                            if (symbol_put_option_available):
                                symbol_puts = Puts.query.with_entities(Puts.openInterest, Puts.prevOpenInterest, Puts.LTQ, Puts.LTP, Puts.prevClosePrice, Puts.bestBid, Puts.bestBidQty, Puts.bestAsk, Puts.bestAskQty, Puts.strike_price).filter(
                                    Puts.symbol == symbol, Puts.expiry_date == expiry.expiry_date).order_by(Puts.strike_price).all()
                                for i in symbol_puts:
                                    symbol_call = Calls.query.with_entities(Calls.bestBidQty, Calls.bestBid, Calls.bestAsk, Calls.bestAskQty, Calls.prevClosePrice, Calls.LTP, Calls.LTQ, Calls.prevOpenInterest, Calls.openInterest).filter(
                                        Calls.symbol == symbol, Calls.expiry_date == expiry.expiry_date, Calls.strike_price == i.strike_price).first()
                                    if (symbol_call):
                                        oi_call_total = oi_call_total + \
                                            int(i.openInterest)
                                        oi_put_total = oi_put_total + \
                                            int(symbol_call.openInterest)
                                        volumn_call_total = volumn_call_total + \
                                            int(i.LTQ)
                                        volumn_put_total = volumn_put_total + \
                                            int(symbol_call.LTQ)
                                        final.append({'oi_c': symbol_call.openInterest, 'oi_change_c': (symbol_call.openInterest-symbol_call.prevOpenInterest), 'volume_c': symbol_call.LTQ, 'iv_c': intrensic_value(), 'ltp_c': (i.LTP/100), 'change_c': ((symbol_call.LTQ-i.prevClosePrice)/100), 'bidqty_c': symbol_call.bestBidQty, 'bid_c': symbol_call.bestBid, 'ask_c': symbol_call.bestAsk,
                                                     'askqty_c': symbol_call.bestAskQty, 'strike_price': i.strike_price, 'bidqty_p': i.bestBidQty, 'bid_p': i.bestBid, 'ask_p': i.bestAsk, 'askqty_p': i.bestAskQty, 'change_p': ((i.prevClosePrice-i.prevClosePrice)/100), 'ltp_p': (i.LTP/100), 'iv_p': intrensic_value(), 'volume_p': i.LTQ, 'oi_change_p': (i.prevOpenInterest-i.openInterest), 'oi_p': i.openInterest})
                                    else:
                                        oi_call_total = oi_call_total+0
                                        oi_put_total = oi_put_total + \
                                            int(symbol.openInterest)
                                        volumn_call_total = volumn_call_total+0
                                        volumn_put_total = volumn_put_total + \
                                            int(symbol.LTQ)
                                        final.append({'oi_c': -1, 'oi_change_c': 'NA', 'volume_c': 'NA', 'iv_c': intrensic_value(), 'ltp_c': 0, 'change_c': 'NA', 'bidqty_c': 'NA', 'bid_c': 0, 'ask_c': 0, 'askqty_c': 'NA', 'strike_price': i.strike_price, 'bidqty_p': i.bestBidQty, 'bid_p': i.bestBid,
                                                     'ask_p': i.bestAsk, 'askqty_p': i.bestAskQty, 'change_p': ((i.prevClosePrice-i.prevClosePrice)/100), 'ltp_p': (i.LTP/100), 'iv_p': intrensic_value(), 'volume_p': i.LTQ, 'oi_change_p': (i.prevOpenInterest-i.openInterest), 'oi_p': i.openInterest})
                                return ({'symbols': symbols, 'expiry_dates': all_dates, 'strike_price': all_strike_price, 'data': final, 'oi_call_total': oi_call_total, 'oi_put_total': oi_put_total, 'volumn_call_total': volumn_call_total, 'volumn_put_total': volumn_put_total})
                            else:
                                return ({"E006 : True"})
                    else:
                        return ({'E005 : True'})
                else:
                    return ({'E004:True'})
            else:
                return ("E003 : True")
        else:
            return ({'EOO1 : True'})


api.add_resource(Symbol_date_option_API,
                 '/api/symbol_date_option/<string:symbol>+<string:expiry>')
api.add_resource(Symbol_price_option_API,
                 '/api/symbol_price_option/<string:symbol>+<string:price>')
api.add_resource(Mounting_api, '/api/mount_options')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
