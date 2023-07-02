from flask import Flask, redirect,render_template, request, session,url_for,Response,make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func,desc
from flask_restful import Resource,Api,reqparse
from flask_cors import CORS
import os

current_dir=os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(current_dir,"edelweiss_hackathon.sqlite3")
app.config['SECRET_KEY']='thisismysecretkey'
db=SQLAlchemy(app)
api=Api(app)
CORS(app)

class All_expiry_symbols_meta(db.Model):
    __tablename__='all_expiry_symbols_meta'
    symbol=db.Column(db.String,nullable=False,primary_key=True)
    expiry_date=db.Column(db.String,nullable=False,primary_key=True)
    call=db.Column(db.Integer,default=0)
    put=db.Column(db.Integer,default=0)
    future=db.Column(db.Integer,default=0)

class Financials(db.Model):
    __tablename__='financials'
    symbol=db.Column(db.String,nullable=False,primary_key=True)
    expiry_date=db.Column(db.Date,nullable=False,primary_key=True)
    LTP=db.Column(db.Integer,nullable=False)
    LTQ=db.Column(db.Integer,nullable=False) 
    totalTradedVolume=db.Column(db.Integer,nullable=False)
    bestBid=db.Column(db.Integer,nullable=False) 
    bestAsk=db.Column(db.Integer,nullable=False)
    bestBidQty=db.Column(db.Integer,nullable=False) 
    bestAskQty=db.Column(db.Integer,nullable=False)
    openInterest=db.Column(db.Integer,nullable=False) 
    timestamp=db.Column(db.String,nullable=False)
    sequence=db.Column(db.Integer,nullable=False)
    prevClosePrice=db.Column(db.Integer,nullable=False) 
    prevOpenInterest=db.Column(db.Integer,nullable=False)

class Calls(db.Model):
    __tablename__='calls'
    symbol=db.Column(db.String,nullable=False,primary_key=True)
    expiry_date=db.Column(db.Date,nullable=False,primary_key=True)
    strike_price=db.Column(db.Integer,nullable=False,primary_key=True)
    LTP=db.Column(db.Integer,nullable=False)
    LTQ=db.Column(db.Integer,nullable=False) 
    totalTradedVolume=db.Column(db.Integer,nullable=False)
    bestBid=db.Column(db.Integer,nullable=False) 
    bestAsk=db.Column(db.Integer,nullable=False)
    bestBidQty=db.Column(db.Integer,nullable=False) 
    bestAskQty=db.Column(db.Integer,nullable=False)
    openInterest=db.Column(db.Integer,nullable=False) 
    timestamp=db.Column(db.String,nullable=False)
    sequence=db.Column(db.Integer,nullable=False)
    prevClosePrice=db.Column(db.Integer,nullable=False) 
    prevOpenInterest=db.Column(db.Integer,nullable=False)

class Puts(db.Model):
    __tablename__='puts'
    symbol=db.Column(db.String,nullable=False,primary_key=True)
    expiry_date=db.Column(db.Date,nullable=False,primary_key=True)
    strike_price=db.Column(db.Integer,nullable=False,primary_key=True)
    LTP=db.Column(db.Integer,nullable=False)
    LTQ=db.Column(db.Integer,nullable=False) 
    totalTradedVolume=db.Column(db.Integer,nullable=False)
    bestBid=db.Column(db.Integer,nullable=False) 
    bestAsk=db.Column(db.Integer,nullable=False)
    bestBidQty=db.Column(db.Integer,nullable=False) 
    bestAskQty=db.Column(db.Integer,nullable=False)
    openInterest=db.Column(db.Integer,nullable=False) 
    timestamp=db.Column(db.String,nullable=False)
    sequence=db.Column(db.Integer,nullable=False)
    prevClosePrice=db.Column(db.Integer,nullable=False) 
    prevOpenInterest=db.Column(db.Integer,nullable=False)

class Indexes(db.Model):
    __tablename__='indexes'
    symbol=db.Column(db.String,nullable=False,primary_key=True)
    LTP=db.Column(db.Integer,nullable=False)
    LTQ=db.Column(db.Integer,nullable=False) 
    totalTradedVolume=db.Column(db.Integer,nullable=False)
    bestBid=db.Column(db.Integer,nullable=False) 
    bestAsk=db.Column(db.Integer,nullable=False)
    bestBidQty=db.Column(db.Integer,nullable=False) 
    bestAskQty=db.Column(db.Integer,nullable=False)
    openInterest=db.Column(db.Integer,nullable=False) 
    timestamp=db.Column(db.String,nullable=False)
    sequence=db.Column(db.Integer,nullable=False)
    prevClosePrice=db.Column(db.Integer,nullable=False) 
    prevOpenInterest=db.Column(db.Integer,nullable=False)

def intrensic_value():
    return(-100)

class single_symbol_optionAPI(Resource):
  def get(self,symbol,expiry):
    symbol_call_option_available=All_expiry_symbols_meta.query.filter(All_expiry_symbols_meta.symbol==symbol,All_expiry_symbols_meta.expiry_date==expiry,All_expiry_symbols_meta.call==1).first()
    asset_price=Indexes.query.with_entities(Indexes.LTP).filter(Indexes.symbol==symbol).first()
    final=[]
    if(symbol_call_option_available):
        symbol_calls=Calls.query.with_entities(Calls.openInterest,Calls.prevOpenInterest,Calls.LTQ,Calls.LTP,Calls.prevClosePrice,Calls.bestBid,Calls.bestBidQty,Calls.bestAsk,Calls.bestAskQty,Calls.strike_price).filter(Calls.symbol==symbol,Calls.expiry_date==expiry).order_by(Calls.strike_price).all()
        for i in symbol_calls:
            symbol_put=Puts.query.with_entities(Puts.bestBidQty,Puts.bestBid,Puts.bestAsk,Puts.bestAskQty,Puts.prevClosePrice,Puts.LTP,Puts.LTQ,Calls.prevOpenInterest,Calls.openInterest).filter(Puts.symbol==symbol,Puts.expiry_date==expiry,Puts.strike_price==i.strike_price).first()
            if(symbol_put):
                final.append({'oi_c':i.openInterest,'oi_change_c':(i.openInterest-i.prevOpenInterest),'volume_c':i.LTQ,'iv_c':intrensic_value(),'ltp_c':(i.LTP/100),'change_c':((i.LTQ-i.prevClosePrice)/100),'bidqty_c':i.bestBidQty,'bid_c':i.bestBid,'ask_c':i.bestAsk,'askqty_c':i.bestAskQty,'strike_price':i.strike_price,'bidqty_p':symbol_put.bestBidQty,'bid_p':symbol_put.bestBid,'ask_p':symbol_put.bestAsk,'askqty_p':symbol_put.bestAskQty,'change_p':((symbol_put.prevClosePrice-symbol_put.prevClosePrice)/100),'ltp_p':(symbol_put.LTP/100),'iv_p':intrensic_value(),'volume_p':symbol_put.LTQ,'oi_change_p':(symbol_put.prevOpenInterest-symbol_put.openInterest),'oi_p':symbol_put.openInterest})
            else:
                final.append({'oi_c':i.openInterest,'oi_change_c':(i.openInterest-i.prevOpenInterest),'volume_c':i.LTQ,'iv_c':intrensic_value(),'ltp_c':(i.LTP/100),'change_c':((i.LTQ-i.prevClosePrice)/100),'bidqty_c':i.bestBidQty,'bid_c':i.bestBid,'ask_c':i.bestAsk,'askqty_c':i.bestAskQty,'strike_price':i.strike_price,'bidqty_p':'NA','bid_p':0,'ask_p':0,'askqty_p':'NA','change_p':'NA','ltp_p':0,'iv_p':intrensic_value(),'volume_p':'NA','oi_change_p':'NA','oi_p':-1})
    else:
        symbol_put_option_available=All_expiry_symbols_meta.query.filter(All_expiry_symbols_meta.symbol==symbol,All_expiry_symbols_meta.expiry_date==expiry,All_expiry_symbols_meta.put==1).first()
        if(symbol_put_option_available):
            symbol_puts=Puts.query.with_entities(Puts.openInterest,Puts.prevOpenInterest,Puts.LTQ,Puts.LTP,Puts.prevClosePrice,Puts.bestBid,Puts.bestBidQty,Puts.bestAsk,Puts.bestAskQty,Puts.strike_price).filter(Puts.symbol==symbol,Puts.expiry_date==expiry).order_by(Puts.strike_price).all()
            for i in symbol_puts:
                symbol_call=Calls.query.with_entities(Calls.bestBidQty,Calls.bestBid,Calls.bestAsk,Calls.bestAskQty,Calls.prevClosePrice,Calls.LTP,Calls.LTQ,Calls.prevOpenInterest,Calls.openInterest).filter(Calls.symbol==symbol,Calls.expiry_date==expiry,Calls.strike_price==i.strike_price).first()
                if(symbol_call):
                    final.append({'oi_c':symbol_call.openInterest,'oi_change_c':(symbol_call.openInterest-symbol_call.prevOpenInterest),'volume_c':symbol_call.LTQ,'iv_c':intrensic_value(),'ltp_c':(i.LTP/100),'change_c':((symbol_call.LTQ-i.prevClosePrice)/100),'bidqty_c':symbol_call.bestBidQty,'bid_c':symbol_call.bestBid,'ask_c':symbol_call.bestAsk,'askqty_c':symbol_call.bestAskQty,'strike_price':i.strike_price,'bidqty_p':i.bestBidQty,'bid_p':i.bestBid,'ask_p':i.bestAsk,'askqty_p':i.bestAskQty,'change_p':((i.prevClosePrice-i.prevClosePrice)/100),'ltp_p':(i.LTP/100),'iv_p':intrensic_value(),'volume_p':i.LTQ,'oi_change_p':(i.prevOpenInterest-i.openInterest),'oi_p':i.openInterest})
                else:
                    final.append({'oi_c':-1,'oi_change_c':'NA','volume_c':'NA','iv_c':intrensic_value(),'ltp_c':0,'change_c':'NA','bidqty_c':'NA','bid_c':0,'ask_c':0,'askqty_c':'NA','strike_price':i.strike_price,'bidqty_p':i.bestBidQty,'bid_p':i.bestBid,'ask_p':i.bestAsk,'askqty_p':i.bestAskQty,'change_p':((i.prevClosePrice-i.prevClosePrice)/100),'ltp_p':(i.LTP/100),'iv_p':intrensic_value(),'volume_p':i.LTQ,'oi_change_p':(i.prevOpenInterest-i.openInterest),'oi_p':i.openInterest})
    return(final)
    # if(userid.isnumeric()):
    #   #print(userid)
    #   userid=int(userid)
    #   user=User_table.query.with_entities(User_table.lastlogin).filter_by(id=userid).first()
    #   if(user):
    #     userlastlogin=user[0]
    #     #print(userlastlogin)
    #     alluserfollows=Follows.query.with_entities(Follows.followee).filter_by(follower=userid).all()
    #     alluserfollowslist=[]
    #     if(alluserfollows):
    #       for i in alluserfollows:
    #         alluserfollowslist.append(i[0])
    #     #print(alluserfollowslist)
    #     rawfeed=[]
    #     posts=Posts.query.with_entities(Posts.uid,User_table.username,Posts.post,Posts.title,Posts.description,Posts.dateposted).join(User_table,User_table.id==Posts.uid).filter(Posts.dateposted.between(userlastlogin,date.today())).order_by(Posts.dateposted).all()
    #     for i in posts:
    #       if i[0] in alluserfollowslist:
    #         rawfeed.append(i)
    #     finishedfeed=[]
    #     for i in rawfeed:
    #       finishedfeed.append({'followerid':i[0],'followerusername':i[1],'postpic':i[2],'posttitle':i[3],'postcaption':i[4],'dateposted':str(i[5])})
    #     return(finishedfeed)

    #   else:
    #     return({'E002':'True'})
    # else:
    #   return ({'EOO1':'True'})

api.add_resource(single_symbol_optionAPI,'/api/single_symbol_options/<string:symbol>+<string:expiry>')

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080)