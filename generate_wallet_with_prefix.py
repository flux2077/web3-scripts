import threading
import time
from eth_account import Account

stop_signal = threading.Event()

def create_wallet():
    Account.enable_unaudited_hdwallet_features()
    account, mnemonic = Account.create_with_mnemonic()
    privateKey = account._key_obj
    publicKey = privateKey.public_key
    address = publicKey.to_checksum_address()
    return str(mnemonic), str(privateKey), str(address)

def search_wallet_with_prefix(prefix, thread_num):
    while not stop_signal.is_set():
        mnemonic, privateKeyEnc, address = create_wallet()
        if address.lower().startswith(prefix):
            print(f'\n--------------------------------------------------------\n')
            print(f'助记词：{mnemonic}\n私钥：{privateKeyEnc}\n钱包地址：{str(address)}')
            print(f"Worker {thread_num} detected termination condition.")
            print(f'\n--------------------------------------------------------\n')
            stop_signal.set()
            break 
        print(f"No wallet found with prefix {prefix}, in current {thread_num}, address: {address}")

def main():
    prefix = "0x123"  # 定制的地址前缀
    threads = []
    thread_count = 20  # 线程数

    for i in range(thread_count):
        t = threading.Thread(target=search_wallet_with_prefix, args=(prefix, i,))
        threads.append(t)
        t.start()

    # 等待所有线程完成
    for t in threads:
        t.join()


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Completed in {end_time - start_time:.2f} seconds.")