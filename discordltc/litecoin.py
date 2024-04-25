import requests

apikey = "t-65e5b882d452f2001cee2ec0-f6be0bd83d2849df82c00ffa"
xpubs = "Ltub2aZWGDL2tB7b7iu1DwvHsbnd7hA7zwTNvRAKoTGNnCyEoXFc67kyD9uaS25RHxuTSVxDuUgBijxFsXmfFSK7YkcgbPXWwkitr8aS2R5DXe2"
menmonics = "curtain alone stereo supreme tongue debris board creek empty hood vessel autumn rather enable wealth pencil snack number buddy emotion twice search noise kitten"
fees_addy = "ltc1qrs5ez0qws4x7vqje4efsm0q6gpun3gtsgqzp9c"

def usd_to_ltc(amount):
  url = f'https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=USD'
  r = requests.get(url)
  d = r.json()
  price = d['USD']
  ltcval = amount/price
  ltcvalf = round(ltcval, 7)
  return ltcvalf

def ltc_to_usd(amount):
  url = f'https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=USD'
  r = requests.get(url)
  d = r.json()
  price = d['USD']
  usd = amount*price
  usdf = round(usd, 3)
  return usdf

def create_new_ltc_address(inx) :
  xpub = xpubs
  index = f"{inx}"
  url = "https://api.tatum.io/v3/litecoin/address/" + xpub + "/" + index

  headers = {"x-api-key": apikey}

  response = requests.get(url, headers=headers)

  data = response.json()
  addy = data['address']
  return addy

def get_key(index):
  url = "https://api.tatum.io/v3/litecoin/wallet/priv"

  payload = {
    "index": index,
    "mnemonic": menmonics
  }

  headers = {
    "Content-Type": "application/json",
    "x-api-key": apikey
  }

  response = requests.post(url, json=payload, headers=headers)

  data = response.json()
  key = data['key']
  return key
  
def get_hash(address):
  endpoint = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/full"

  response = requests.get(endpoint)
  data = response.json()


  latest_transaction = data['txs'][0]
  latest_hash = latest_transaction['hash']
  conf = latest_transaction['confirmations']

  return latest_hash, conf
  
def get_address_balance(address) :
  endpoint = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/full"

  response = requests.get(endpoint)
  data = response.json()

  balance = data['balance'] / 10**8
  unconfirmed_balance = data['unconfirmed_balance'] / 10**8


  return balance, unconfirmed_balance

def send_ltc(sendaddy, private_key, recipient_address, amount) :
    url = "https://api.tatum.io/v3/litecoin/transaction"

    payload = {
    "fromAddress": [
        {
        "address": sendaddy,
        "privateKey": private_key
        }
    ],
    "to": [
        {
        "address": recipient_address,
        "value": amount
        }
    ],
    "fee": "0.00005",  
    "changeAddress": fees_addy
    }

    headers = {
    "Content-Type": "application/json",
    "x-api-key": apikey
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    tx = data["txId"]
    return tx
