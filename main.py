from qr_handler import QrHandler


def main():
    qr_handler = QrHandler(0, 'info.xlsx')  # 0 for internal camera, 1 for external

    qr_handler.run()


if __name__ == '__main__':
    main()
