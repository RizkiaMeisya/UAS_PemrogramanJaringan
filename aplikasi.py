import socket
import threading
import paramiko
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Fungsi untuk akses port socket
def access_port_socket():
    host = input("Masukkan alamat host: ")
    port = int(input("Masukkan nomor port: "))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"Terkoneksi ke {host}:{port}")
        message = input("Masukkan pesan untuk dikirim: ")
        s.sendall(message.encode())
        data = s.recv(1024)
        print(f"Pesan dari server: {data.decode()}")

# Fungsi untuk FTP server
def start_ftp_server():
    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "12345", ".", perm="elradfmw")
    authorizer.add_anonymous(".")
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(("0.0.0.0", 21), handler)
    print("FTP Server berjalan di port 21")
    server.serve_forever()

# Fungsi untuk FTP client
def ftp_client():
    from ftplib import FTP
    ftp = FTP()
    host = input("Masukkan alamat FTP server: ")
    ftp.connect(host, 21)
    ftp.login(user='user', passwd='12345')
    print(ftp.getwelcome())
    file_to_upload = input("Masukkan nama file untuk diupload: ")
    with open(file_to_upload, 'rb') as file:
        ftp.storbinary(f'STOR {file_to_upload}', file)
    ftp.quit()
    print(f"File {file_to_upload} berhasil diupload")

# Fungsi untuk SSH server
def start_ssh_server():
    host_key = paramiko.RSAKey(filename='test_rsa.key')
    ssh_server = paramiko.ServerInterface()
    transport = paramiko.Transport(("0.0.0.0", 22))
    transport.add_server_key(host_key)
    transport.start_server(server=ssh_server)
    print("SSH Server berjalan di port 22")
    channel = transport.accept(20)
    if channel is None:
        print("Tidak ada koneksi")
        return
    print("Koneksi SSH berhasil")

# Fungsi untuk SSH client
def ssh_client():
    hostname = input("Masukkan alamat SSH server: ")
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)
    stdin, stdout, stderr = client.exec_command('ls')
    print(stdout.read().decode())
    client.close()

# Fungsi untuk cek port server
def check_server_port():
    host = input("Masukkan alamat host: ")
    port = int(input("Masukkan nomor port: "))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    if result == 0:
        print(f"Port {port} di {host} terbuka")
    else:
        print(f"Port {port} di {host} tertutup")
    sock.close()

# Menu utama aplikasi
def main_menu():
    while True:
        print("\nMenu Utama:")
        print("1. Akses Port Socket")
        print("2. FTP Server")
        print("3. FTP Client")
        print("4. SSH Server")
        print("5. SSH Client")
        print("6. Cek Port Server")
        print("7. Keluar")
        
        choice = input("Pilih opsi (1-7): ")
        
        if choice == '1':
            access_port_socket()
        elif choice == '2':
            threading.Thread(target=start_ftp_server).start()
        elif choice == '3':
            ftp_client()
        elif choice == '4':
            threading.Thread(target=start_ssh_server).start()
        elif choice == '5':
            ssh_client()
        elif choice == '6':
            check_server_port()
        elif choice == '7':
            print("Keluar dari aplikasi")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")

if __name__ == "__main__":
    main_menu()
