
from enum import Enum
class MintedOn(Enum):
    koda = 'koda'
    eth = 'eth'
    btc = 'btc'

logo_map = {
    MintedOn.koda: {
        'src': '../../KodadarkV4.png',
        'width': '224px'
        },
    MintedOn.eth: {
        'src': '../../ethereum-eth.svg',
        'width': '120px'
    },
    MintedOn.btc: {
        'src': '../../bitcoin-btc-logo.svg',
        'width': '120px'
    }
}
    