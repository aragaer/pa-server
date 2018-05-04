#!/usr/bin/env python3
import getpass, imaplib

def main():
    M = imaplib.IMAP4(host="127.0.0.1", port=8007)
    M.login(getpass.getuser(), "")
    M.select()
    typ, data = M.search(None, 'ALL')
    for num in data[0].split():
        num = num.decode()
        typ, data = M.fetch(num, '(RFC822)')
        print(num, data[0][1].decode().strip())
        M.store(num, "+FLAGS", r'\Seen \Deleted')
    M.close()
    M.logout()

if __name__ == '__main__':
    main()
