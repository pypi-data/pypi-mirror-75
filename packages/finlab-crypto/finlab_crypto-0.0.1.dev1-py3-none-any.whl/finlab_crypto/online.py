import pandas as pd
from binance.enums import *
def check_before_rebalance(client, signals, prices, invested_base, fixed_assets, rebalance=False):

  # calculate signal
  signals = pd.Series(signals)

  # calculate position in btc
  position_base_value = (invested_base * signals)

  # calculate position in crypto (algo_size)
  symbols = signals.index.to_list()
  last_price = pd.Series({name: prices[name].close.iloc[-1] for name in symbols}).astype(float)
  algo_size = (position_base_value / last_price)

  # get account balance
  info = client.get_account()
  exinfo = client.get_exchange_info()

  # get account balance
  balance = {i['asset']: (i['free'], i['locked']) for i in info['balances']}


  # calculate account size
  account_size = pd.Series({s:[balance[s[:-3]][0]][0] for s in symbols}).astype(float)

  # calculate default position size
  fixed_size = pd.Series(fixed_assets).reindex(symbols).fillna(0).astype(float)

  # exchange info (for lot filters)
  minimum_lot_size = pd.Series({s:[f for f in [ex for ex in exinfo['symbols'] if ex['symbol'] == s][0]['filters'] if f['filterType'] == 'LOT_SIZE'][0]['minQty'] for s in symbols}).astype(float)
  step_size = pd.Series({s:[f for f in [ex for ex in exinfo['symbols'] if ex['symbol'] == s][0]['filters'] if f['filterType'] == 'LOT_SIZE'][0]['stepSize'] for s in symbols}).astype(float)


  # calculate target size
  target_size = algo_size + fixed_size

  # REBALANCE:
  delta_size = ((target_size - account_size) / step_size).astype(int) * step_size

  # NO REBALANCE:
  same_direction = (
      ((algo_size > 0) & (account_size - fixed_size > minimum_lot_size)) |
      ((algo_size == 0) & (account_size - fixed_size < minimum_lot_size))
  )

  delta_size = delta_size * (1-same_direction)
  delta_size[delta_size.abs() < minimum_lot_size] = 0

  # REBALANCE:
  delta_size = ((target_size - account_size) / step_size).astype(int) * step_size

  # NO REBALANCE:
  if not rebalance:
    same_direction = (
        ((algo_size > 0) & (account_size - fixed_size > minimum_lot_size)) |
        ((algo_size < 0) & (account_size - fixed_size < minimum_lot_size))
    )
    delta_size = delta_size * (1-same_direction)

  # minimim lot size filter
  delta_size[delta_size.abs() < minimum_lot_size] = 0

  return pd.DataFrame({'algo_size':algo_size, 'algo_size_btc': position_base_value,
  'fixed_size':fixed_assets,
  'account_size':account_size,
  'target_size':target_size,
  'target_size_btc': target_size * last_price,
  'delta_size':delta_size,
  'minimum_lot_size':minimum_lot_size,'last_price': last_price
  })


def execute_trades(client, delta_size, mode='TEST'):
  order_func = client.create_order if mode == 'LIVE' else client.create_test_order
  for s, lot in delta_size.items():

    if lot == 0:
      continue

    side = SIDE_BUY if lot > 0 else SIDE_SELL
    print(mode, s, side, lot)
    order = order_func(
        side=side,
        type=ORDER_TYPE_MARKET,
        symbol=s,
        quantity=abs(lot))
  return
