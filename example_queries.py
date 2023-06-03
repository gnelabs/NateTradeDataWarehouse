
__author__ = "Nathan Ward"

from datetime import datetime
from dw.natetrade_database import DatabaseHelper


class Examples(object):
    def __init__(self):
        self.helper = DatabaseHelper()
    
    def get_latest_date_for_daily_underlying(self) -> str:
        """
        Returns the latest date available for stocks in the daily_underlying table.
        
        Used because this data is on a delay.
        """
        query = """
        SELECT date
        FROM stocks.daily_underlying
        WHERE ticker = 'SPY'
        ORDER BY DATE
        DESC
        LIMIT 1;
        """
        data = self.helper.generic_select_query('stocks', query)
        
        try:
            return str(data[0]['date'])
        except IndexError:
            return ''
        except KeyError:
            return ''
    
    def contract_price_over_time(self, ticker: str, option_type: str, expiration: str, strike: int) -> list:
        """
        Example query to track changes in vol, contract price, and underlying price over a time series.
        """
        if option_type not in 'pc':
            raise StrictSchemaError('Invalid arguments. {0}'.format(locals()))
        
        query = """
        SELECT timestamp_utc, implied_volatility, midpoint, underlying
        FROM options.greeks
        WHERE ticker = '{sym}'
        AND option_type = '{op_type}'
        AND expiration = '{exp}'
        AND strike = {strike}
        ORDER BY timestamp_utc
        DESC
        LIMIT 1000;
        """.format(
            sym = ticker,
            op_type = option_type,
            exp = expiration,
            strike = strike
        )
        
        return self.helper.generic_select_query('options', query)
    
    def top_stocks_activity(self) -> list:
        """
        Example query to get the top 50 stocks by transactions.
        """
        query = """
        SELECT 
          *,
          CONCAT("$",ROUND((close_price*volume)/1000000000,2),"B") AS notional_traded,
          CONCAT(ROUND(((close_price-open_price)/open_price* 100), 2), "%") AS percent_change
        FROM stocks.daily_underlying 
        WHERE date = '{0}'
        ORDER BY num_transactions 
        DESC
        LIMIT 50;
        """.format(self.get_latest_date_for_daily_underlying())
        
        return self.helper.generic_select_query('stocks', query)
    
    def options_impact_by_bullish_liquidity(self) -> list:
        """
        Example query to get the top 20 latest options block trades based on their 
        impact to the underlying stock from a bullish liquidity ratio perspective.
        
        For instance, the size of the delta-adjusted impact at the time of trade can 
        represent a significant fraction of the underlying daily traded volume for 
        a stock. These types of trades tend to move the stock price as dealers 
        hedge the delta risk by buying the underlying stock. 
        """
        latest_daily_underlying_date = self.get_latest_date_for_daily_underlying()
        e_timestamp = int(datetime.strptime(latest_daily_underlying_date, '%Y-%m-%d').timestamp())
        
        query = """
        SELECT 
          *,
          CONCAT(ROUND((t.share_impact*ABS(g.delta)/d.volume)*100, 2), "%") AS percent_daily_volume
        FROM options.trades t
          JOIN options.greeks g
             ON t.timestamp_utc = g.timestamp_utc
             AND t.strike = g.strike
             AND t.expiration = g.expiration
             AND t.ticker = g.ticker
           JOIN stocks.daily_underlying d
             ON t.ticker = d.ticker
             AND d.date = '{date}'
        WHERE t.timestamp_utc > {tstamp}
        AND t.share_impact > 100000
        ORDER BY percent_daily_volume
        DESC
        LIMIT 20
        ;
        ;
        """.format(
            date = latest_daily_underlying_date,
            tstamp = e_timestamp
        )
        
        return self.helper.generic_select_query('options', query)