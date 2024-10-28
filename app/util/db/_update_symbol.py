from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from .connect_db import engine

# MySQL 연결 설정
Session = sessionmaker(bind=engine)
session = Session()

def upsert_stock_info(data):
    # MySQL의 INSERT INTO ... ON DUPLICATE KEY UPDATE 쿼리 작성
    sql = text("""
        INSERT INTO stock_info (
            symbol, stock_name, market, sector_name, price, volume, amount, market_cap, 
            sign, risk, halt, overbought, prev_price, prev_volume, `change`, high_limit, 
            low_limit, unit, tick, decimal_places, currency, exchange_rate, `open`, high, 
            low, `close`, rate, sign_name, eps, bps, per, pbr, week52_high, week52_low, 
            week52_high_date, week52_low_date
        ) VALUES (
            :symbol, :stock_name, :market, :sector_name, :price, :volume, :amount, 
            :market_cap, :sign, :risk, :halt, :overbought, :prev_price, :prev_volume, 
            :change, :high_limit, :low_limit, :unit, :tick, :decimal_places, :currency, 
            :exchange_rate, :open, :high, :low, :close, :rate, :sign_name, :eps, :bps, 
            :per, :pbr, :week52_high, :week52_low, :week52_high_date, :week52_low_date
        ) 
        ON DUPLICATE KEY UPDATE 
            stock_name=VALUES(stock_name),
            market=VALUES(market),
            sector_name=VALUES(sector_name),
            price=VALUES(price),
            volume=VALUES(volume),
            amount=VALUES(amount),
            market_cap=VALUES(market_cap),
            sign=VALUES(sign),
            risk=VALUES(risk),
            halt=VALUES(halt),
            overbought=VALUES(overbought),
            prev_price=VALUES(prev_price),
            prev_volume=VALUES(prev_volume),
            `change`=VALUES(`change`),
            high_limit=VALUES(high_limit),
            low_limit=VALUES(low_limit),
            unit=VALUES(unit),
            tick=VALUES(tick),
            decimal_places=VALUES(decimal_places),
            currency=VALUES(currency),
            exchange_rate=VALUES(exchange_rate),
            `open`=VALUES(`open`),
            high=VALUES(high),
            low=VALUES(low),
            `close`=VALUES(`close`),
            rate=VALUES(rate),
            sign_name=VALUES(sign_name),
            eps=VALUES(eps),
            bps=VALUES(bps),
            per=VALUES(per),
            pbr=VALUES(pbr),
            week52_high=VALUES(week52_high),
            week52_low=VALUES(week52_low),
            week52_high_date=VALUES(week52_high_date),
            week52_low_date=VALUES(week52_low_date)
    """)

    # 데이터 바인딩 및 SQL 실행
    session.execute(sql, {
        'symbol': data['symbol'],
        'stock_name': data['stock_name'],
        'market': data['market'],
        'sector_name': data['sector_name'],
        'price': data['price'],
        'volume': data['volume'],
        'amount': data['amount'],
        'market_cap': data['market_cap'],
        'sign': data['sign'],
        'risk': data['risk'],
        'halt': data['halt'],
        'overbought': data['overbought'],
        'prev_price': data['prev_price'],
        'prev_volume': data['prev_volume'],
        'change': data['change'],
        'high_limit': data['high_limit'],
        'low_limit': data['low_limit'],
        'unit': data['unit'],
        'tick': data['tick'],
        'decimal_places': data['decimal_places'],
        'currency': data['currency'],
        'exchange_rate': data['exchange_rate'],
        'open': data['open'],
        'high': data['high'],
        'low': data['low'],
        'close': data['close'],
        'rate': data['rate'],
        'sign_name': data['sign_name'],
        'eps': data['eps'],
        'bps': data['bps'],
        'per': data['per'],
        'pbr': data['pbr'],
        'week52_high': data['week52_high'],
        'week52_low': data['week52_low'],
        'week52_high_date': data['week52_high_date'],
        'week52_low_date': data['week52_low_date'],
    })

    # 트랜잭션 커밋
    session.commit()
