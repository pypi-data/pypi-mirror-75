import numpy as np
import pandas as pd
import vectorbt as vbt
from IPython.display import display, HTML, IFrame, clear_output
from collections.abc import Iterable

def Strategy(**default_parameters):

  class Strategy:
    def __init__(self, func):
      self.stoploss = None
      self.profit_targets = None
      self.func = func
      self._variables = None
      self.set_parameters(default_parameters)

    def set_parameters(self, variables):
      self.stoploss = None
      self.profit_targets = None
      if variables:
        for key, val in variables.items():
          setattr(self, key, val)
      self._variables = variables

    def exits_sl_tp(self, entries, exits, price, variables):

      if 'stoploss' in variables:
        stoploss_exits = entries.vbt.signals.generate_stop_loss_exits(price, variables['stoploss'])
        exits = exits.vbt.signals.OR(stoploss_exits)

      if 'profit_targets' in variables:
        take_profit_exits = entries.vbt.signals.generate_take_profit_exits(price, variables['profit_targets'])
        exits = exits.vbt.signals.OR(take_profit_exits)

      return exits

    def backtest(self, ohlcv, variables=None, plot=True, price_decision='close', S=10, **args):

      if variables:
        self.set_parameters(variables)
      else:
        variables = self._variables
      # check if the backtest is an optimization of combinations of parameters
      is_combination = sum(isinstance(v, Iterable) and not isinstance(v, str) for name, v in variables.items()) != 0

      # generate entries and exits signals
      results = self.func(ohlcv, is_combination)

      if len(results) == 2:
        entries, exits = results
        fig_data = {}
      elif len(results) == 3:
        entries, exits, fig_data = results
      else:
        raise("strategy outputs multiple results!")

      # backtest price

      if 'trading' not in variables or ('trading' in variables and variables['trading'] == 'long'):
        price = ohlcv[price_decision]
      elif 'trading' in variables and variables['trading'] == 'short':
        price = (ohlcv[price_decision].shift()/ohlcv[price_decision]).cumprod()
      else:
        raise Exception('variable "trading" should be either "long" or "short". Get ' + variables['trading'] + ' instead.')

      exits = self.exits_sl_tp(entries, exits, price, variables)

      portfolio = vbt.Portfolio.from_signals(price, entries, exits, **args)

      if 'trading' in variables and variables['trading'] == 'short':
        portfolio.position_records['OpenPrice'] = (ohlcv[price_decision].iloc[portfolio.position_records.OpenAt] * (1 - vbt.defaults.portfolio['slippage'])).values
        portfolio.position_records['ClosePrice'] = (ohlcv[price_decision].iloc[portfolio.position_records.CloseAt] * (1 + vbt.defaults.portfolio['slippage'])).values

      if plot:
        if not is_combination:
          self.plot(ohlcv, entries, exits, portfolio , fig_data)
        else:
          # Plot heatmap
          i1, i2 = np.array([len(set(l)) for l in portfolio.total_return.index.levels]).argsort()[-2:][::-1]
          name1, name2 = portfolio.total_return.index.names[i1], portfolio.total_return.index.names[i2]
          portfolio.total_return.vbt.heatmap(
              x_level=name1, y_level=name2, symmetric=False,
              trace_kwargs=dict(colorbar=dict(title='Total return', tickformat='%'))
          ).show_png()

          # plot best returns
          best_n = 5
          best_results = portfolio.total_return.sort_values().index[-best_n:][::-1]
          portfolio.cumulative_returns[best_results].plot()

          import matplotlib.pyplot as plt
          plt.show()

          # check the probability of backtest overfitting
          from crypto import overfitting
          results = overfitting.CSCV(portfolio.daily_returns, S=S)

      return portfolio

    def plot(self, ohlcv, entries, exits, portfolio ,fig_data):

      # format trade data
      txn = portfolio.positions.records
      txn['enter_time'] = ohlcv.iloc[portfolio.trades.records.entry_idx].index.values
      txn['exit_time'] = ohlcv.iloc[portfolio.trades.records.exit_idx].index.values

      # plot trade data
      mark_lines = []
      for name, t in txn.iterrows():
        x = [str(t.enter_time), str(t.exit_time)]
        y = [t.entry_price, t.exit_price]
        name = t.loc[['entry_price', 'exit_price', 'return']].to_string()
        mark_lines.append((name, x, y))



      # calculate overlap figures
      overlaps = {}
      if 'overlaps' in fig_data:
        overlaps = fig_data['overlaps']

      # calculate sub-figures
      figures = {}
      if 'figures' in fig_data:
        figures = fig_data['figures']

      figures['entries & exits'] = pd.DataFrame({'entries':entries.squeeze(), 'exits': exits.squeeze()})
      figures['performance'] = portfolio.equity

      from crypto import chart
      c, info = chart.chart(ohlcv, overlaps=overlaps, figures=figures, markerlines=mark_lines, start_date='2018', end_date='2020')
      c.load_javascript()
      c.render()
      display(HTML(filename="render.html"))

    def test_function(self, ohlcv, variables=None):
      if variables:
        self.set_parameters(variables)
      else:
        variables = self._variables
      # check if the backtest is an optimization of combinations of parameters
      is_combination = sum(isinstance(v, list) for name, v in variables.items()) != 0

      # generate entries and exits signals
      return self.func(ohlcv, is_combination)

    def recent_signal(self, ohlcv, variables=None, lookback_period=0):
      portfolio = self.backtest(ohlcv.iloc[-abs(lookback_period):], variables=variables, plot=False)
      #return portfolio.shares.iloc[-1]
      return portfolio


  def deco(func):
    return Strategy(func)

  return deco
