#!/usr/bin/env python

cli_cmd_lines = {
    "shelley address key-gen": {
        '--normal-key',
        '--extended-key',
        '--byron-key',
        '--verification-key-file',
        '--signing-key-file'
    },
    "shelley address key-hash": {
        '--payment-verification-key-file',
        '--out-file'
    },
    "shelley address build": {
        '--payment-verification-key-file',
        '--stake-verification-key-file',
        '--mainnet',
        '--testnet-magic',
        '--out-file'
    },
    "shelley address build-multisig": {

    },
    "shelley address info": {
        '--address',
        '--out-file'
    },
    "shelley stake-address key-gen": {
        '--verification-key-file',
        '--signing-key-file'
    },
    "shelley stake-address build": {
        '--stake-verification-key-file',
        '--mainnet',
        '--testnet-magic',
        '--out-file'
    },
    "shelley stake-address key-hash": {
        '--stake-verification-key-file',
        '--out-file'
    },
    "shelley stake-address register": {
        '--signing-key-file',
        '--host-addr',
        '--port'
    },
    "shelley stake-address delegate": {
        '--signing-key-file',
        '--pool-id',
        '--delegation-fee',
        '--host-addr',
        '--port'
    },
    "shelley stake-address de-register": {
        '--signing-key-file',
        '--host-addr',
        '--port'
    },
    "shelley stake-address registration-certificate": {
        '--stake-verification-key-file',
        '--out-file'
    },
    "shelley stake-address deregistration-certificate": {
        '--stake-verification-key-file',
        '-out-file'
    },
    "shelley stake-address delegation-certificate": {
        '--stake-verification-key-file',
        '--cold-verification-key-file',
        '--cole-verification-key-hash',
        '--out-file'
    },
    "shelley key verification-key": {
        '--signing-key-file',
        '--verification-key-file'
    },
    "shelley key non-extended-key": {
        '--extended-verification-key-file',
        '--verification-key-file'
    },
    "shelley key convert-byron-key": {
        '--byron-payment-key-type',
        '--byron-genesis-delegate-key-type',
        '--legacy-byron-genesis-key-type',
        '--byron-genesis-delegate-key-type',
        '--legacy-byron-genesis-delegate-key-type',
        '--byron-signing-key-file',
        '--byron-verification-key-file',
        '--out-file'
    },
    "shelley key convert-byron-genesis-vkey": {
        '--byron-genesis-verification-key',
        '--out-file'
    },
    "shelley key convert-itn-key": {
        '--itn-signing-key-file',
        '--itn-verification-key-file',
        '--out-file'
    },
    "shelley transaction build-raw": {
        '--tx-in',
        '--tx-out',
        '--ttl',
        '--fee',
        '--certificate-file',
        '--withdrawal',
        '--metadata-json-file',
        '--metadata-cbor-file',
        '--update-proposal-file',
        '--out-file'
    },
    "shelley transaction sign": {
        '--tx-body-file',
        '--signing-key-file',
        '--mainnet',
        '--testnet-magic',
        '--out-file'
    },
    "shelley transaction witness": {
        '--tx-body-file',
        '--witness-signing-key-file',
        '--mainnet',
        '--testnet-magic',
        '--out-file'
    },
    "shelley transaction sign-witness": {
        '--tx-body-file',
        '--witness-file',
        '--out-file'
    },
    "shelley transaction check": {

    },
    "shelley transaction submit": {
        '--shelley-mode',
        '--byron-mode',
        '--epoch-slots',
        '--security-param',
        '--cardano-mode',
        '--epoch-slots',
        '--security-param',
        '--mainnet',
        '--testnet-magic',
        '--tx-file'
    },
    "shelley transaction calculate-min-fee": {
        '--tx-body-file',
        '--mainnet',
        '--testnet-magic',
        '--protocol-params-file',
        '--tx-in-count',
        '--tx-out-count',
        '--witness-count',
        '--byron-witness-count'
    },
    "shelley transaction txid": {
        '--tx-body-file'
    },
    "shelley node key-gen": {
        '--cold-verification-key-file',
        '--cold-signing-key-file',
        '--operational-certificate-issue-counter-file'
    },
    "shelley node key-gen-KES": {
        '--verification-key-file',
        '--signing-key-file'
    },
    "shelley node key-gen-VRF": {
        '--verification-key-file',
        '--signing-key-file'
    },
    "shelley node key-hash-VRF": {
        '--verification-key-file',
        '--out-file'
    },
    "shelley node new-counter": {
        '--cold-verification-key-file',
        '--counter-value',
        '--operational-certificate-issue-counter-file'
    },
    "shelley node issue-op-cert": {
        '--kes-verification-key-file',
        '--cold-signing-key-file',
        '--operational-certificate-issue-counter-file'
        '--kes-period',
        '--out-file'
    },
    "shelley stake-pool register": {
        '--pool-id'
    },
    "shelley stake-pool re-register": {
        '--pool-id'
    },
    "shelley stake-pool retire": {
        '--pool-id',
        'epoch',
        '--host-addr',
        '--port'
    },
    "shelley stake-pool registration-certificate": {
        '--cold-verification-key-file',
        '--vrf-verification-key-file',
        '--pool-pledge',
        '--pool-cost',
        '--pool-margin',
        '--pool-reward-account-verification-key-file',
        '--pool-owner-stake-verification-key-file',
        '--pool-relay-ipv4',
        '--pool-relay-ipv6',
        '--pool-relay-port',
        '--single-host-pool-relay',
        '--pool-relay-port',
        '--multi-host-pool-relay',
        '--metadata-url',
        '--metadata-hash',
        '--mainnet',
        '--testnet-magic',
        '--out-file'
    },
    "shelley stake-pool deregistration-certificate": {
        '--cold-verification-key-file',
        '--epoch',
        '--out-file'
    },
    "shelley stake-pool id": {
        '--verification-key-file'
    },
    "shelley stake-pool metadata-hash": {
        '--pool-metadata-file',
        '--out-file'
    },
    "shelley query pool-id": {},
    "shelley query protocol-paramters": {
        '--shelley-mode',
        '--byron-mode',
        '--epoch-slots',
        '--security-param',
        '--cardano-mode',
        '--mainnet',
        '--testnet-magic',
        '--out-file'
    },
    "shelley query tip": {
        '--shelley-mode',
        '--byron-mode',
        '--epoch-slots',
        '--security-param',
        '--cardano-mode',
        '--mainnet',
        '--testnet-magic',
        '--out-file'
    },
    "shelley query stake-distribution": {
        '--shelley-mode',
        '--byron-mode',
        '--epoch-slots',
        '--security-param',
        '--cardano-mode',
        '--mainnet',
        '--testnet-magic',
        '--out-file'
    },
    "shelley query stake-address-info": {
        '--shelley-mode',
        '--byron-mode',
        '--epoch-slots',
        '--security-param',
        '--cardano-mode',
        '--address',
        '--mainnet',
        '--testnet-magic',
        '--out-file'
    },
    "shelley query utxo": {
        '--shelley-mode',
        '--byron-mode',
        '--epoch-slots',
        '--security-param',
        '--cardano-mode',
        '--address',
        '--mainnet',
        '--testnet-magic',
        '--out-file'
    },
    "shelley query version": {},
    "shelley query ledger-state": {
        '--shelley-mode',
        '--byron-mode',
        '--epoch-slots',
        '--security-param',
        '--cardano-mode',
        '--mainnet',
        '--testnet-magic',
        '--out-file'
    },
    "shelley query status": {},
    "shelley block info": {
        '--block-id',
        '--host-addr',
        '--port'
    },
    "shelley system start": {
        '--genesis',
        '--host-addr',
        '--port'
    },
    "shelley system stop": {},
    "shelley genesis key-gen-genesis": {
        '--verification-key-file',
        '--signing-key-file'
    },
    "shelley genesis key-gen-delegate": {
        '--verification-key-file',
        '--signing-key-file',
        '--operational-certificate-issue-counter-file'
    },
    "shelley genesis key-gen-utxo": {
        '--verification-key-file',
        '--signing-key-file',
    },
    "shelley genesis key-hash": {
        '--verification-key-file',
    },
    "shelley genesis get-ver-key": {
        '--verification-key-file',
        '--signing-key-file',
    },
    "shelley genesis initial-addr": {
        '--mainnet',
        '--testnet-magic',
        '--out-file'
    },
    "shelley genesis initial-txin": {
        '--verification-key-file',
        '--mainnet',
        '--testnet-magic',
        '--out-file'
    },
    "shelley genesis create": {
        '--genesis-dir',
        '--gen-genesis-keys',
        '--gen-utxo-keys',
        '--start-time',
        '--supply',
        '--mainnet',
        '--testnet-magic'
    },
    "shelley genesis hash": {
        '--genesis'
    },
    "shelley governance create-mir-certificate": {
        '--reserves',
        '--treasury',
        '--stake-verification-key-file',
        '--reward',
        '--out-file'
    },
    "shelley governance create-update-proposal": {
        '--out-file',
        '--epoch',
        '--genesis-verification-key-file',
        '--protocol-magic-version',
        '--protocol-minor-version',
        '--decentralization-parameter',
        '--extra-entropy',
        '--reset-extra-entropy',
        '--max-block-header-size',
        '--max-block-body-size',
        '--max-tx-size',
        '--min-fee-constant',
        '--min-fee-linear',
        '--min-utxo-value',
        '--key-reg-deposit-amt',
        '--pool-reg-deposit',
        '--min-pool-cost',
        '--pool-retirement-epoch-boundary',
        '--number-of-pools',
        '--pool-influence',
        '--monetary-expansion',
        '--treasury-expansion'
    },
    "shelley governance protocol-update": {
        '--cold-signing-key-file'
    },
    "shelley governance cold-keys": {
        '--cold-signing-key-file'
    },
    "shelley text-view decode-cbor": {
        '--in-file',
        '--out-file'
    }
}
