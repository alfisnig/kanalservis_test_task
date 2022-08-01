import time


def delivery_monitoring():
    print('delivery_monitoring')


def start_delivery_monitoring():
    while True:
        try:
            delivery_monitoring()
        except Exception as e:
            print(e)
        time.sleep(60)


if __name__ == '__main__':
    start_delivery_monitoring()
