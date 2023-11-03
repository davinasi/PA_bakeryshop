import csv
from prettytable import PrettyTable
import getpass

# Data produk sebagai contoh
products = [
    {"id": "1", "nama": "strawberry cheesecake", "harga": 37000, "stock": 13},
    {"id": "2", "nama": "apple pie", "harga": 20000, "stock": 8},
    {"id": "3", "nama": "Donat", "harga": 17000, "stock": 15},
    {"id": "4", "nama": "Roti Coklat", "harga": 25000, "stock": 27},
    {"id": "5", "nama": "basque burnt cheesecake", "harga": 14000, "stock": 22},
    {"id": "6", "nama": "croissant original", "harga": 12000, "stock": 9},
    {"id": "7", "nama": "chocolate mousse", "harga": 18000, "stock": 17},
    {"id": "8", "nama": "tiramisu", "harga": 14000, "stock": 14},
    {"id": "9", "nama": "cupcake", "harga": 10000, "stock": 23},
]

# Nama file CSV yang akan dibuat
csv_filename = 'databakery.csv'

# Menulis data produk ke dalam file CSV
with open(csv_filename, mode='w', newline='') as file:
    fieldnames = ['id', 'nama', 'harga', 'stock']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()  # Menulis header (nama kolom)

    for product in products:
        writer.writerow(product)

# Database untuk menyimpan informasi pengguna (username dan password)
user_database = {
    "danil": "1111",
    "davina": "2222",
    "ichfan": "3333",
    "bilo": "4444"
}

# Fungsi untuk membuat akun baru
def create_account():
    print('__________________')
    print('Membuat akun baru')
    print('__________________')
    while True:
        new_username = input('Buat username baru: ').strip()
        if not new_username:
            print("Username tidak boleh kosong. Silakan coba lagi.")
        elif not new_username.isalpha():
            print("Username Invalid. Silakan coba lagi.")
        elif new_username in user_database:
            print("Username sudah ada. Silakan coba username lain.")
        else:
            break

    while True:
        new_password = getpass.getpass('Buat kata sandi baru: ').strip()
        if not new_password:
            print("Kata sandi tidak boleh kosong. Silakan coba lagi.")
        else:
            break

    user_database[new_username] = new_password
    print('\nAkun telah berhasil dibuat.')

# Fungsi login pelanggan
def login():
    while True:
        username = input("Masukkan username: ").strip()
        password = getpass.getpass("Masukkan kata sandi: ").strip()
        if username in user_database and user_database[username] == password:
            return username
        else:
            print("Username atau kata sandi salah. Silakan coba lagi.")

# Definisi kelas Produk
class Product:
    def __init__(self, id, name, price, stock):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock

# Definisi kelas Toko
class Store:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def view_products(self):
        table = PrettyTable()
        table.field_names = ["ID", "Nama Produk", "Harga", "Stock"]
        for product in self.products:
            table.add_row([product.id, product.name, product.price, product.stock])
        print(table)

# Fungsi untuk memuat produk dari file CSV ke dalam list
def load_products():
    products = []
    with open('databakery.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            products.append(Product(row['id'], row['nama'], int(float(row['harga'])), int(row['stock'])))
    return products

# Fungsi untuk menyimpan produk dari list ke file CSV
def save_products(products):
    with open('databakery.csv', 'w', newline='') as file:
        fieldnames = ['id', 'nama', 'harga', 'stock']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for product in products:
            csv_writer.writerow({'id': product.id, 'nama': product.name, 'harga': product.price, 'stock': product.stock})

# Definisi kelas Pelanggan
class Customer:
    def __init__(self, emoney):
        self.shopping_cart = {}
        self.emoney = emoney

    # Fungsi untuk melihat produk di toko
    def view_products(self, store):
        store.view_products()

    # Fungsi untuk menambahkan produk ke keranjang
    def add_to_cart(self, store):
        product_id = input("Masukkan ID produk yang ingin Anda beli: ")

        while True:
            quantity_input = input("Masukkan jumlah: ")
            if quantity_input.isdigit():
                quantity = int(quantity_input)
                if quantity >= 1:  
                    product = next((p for p in store.products if p.id == product_id), None)
                    if product:
                        product_name = product.name
                        total_price = product.price * quantity
                        if total_price <= self.emoney:
                            if product_name in self.shopping_cart:
                                self.shopping_cart[product_name] += quantity
                            else:
                                self.shopping_cart[product_name] = quantity
                            self.emoney -= total_price  # Kurang saldo E-Money
                            print(f"{quantity} {product_name} ditambahkan ke keranjang Anda.")
                            break
                        else:
                            print("Saldo E-Money tidak mencukupi untuk menambahkan produk ini ke keranjang.")
                            return
                    else:
                        print("Produk tidak ditemukan.")
                        return
                else:
                    print("Jumlah Invalid.")
                    return
            else:
                print("Masukkan jumlah yang valid.")
                return

    # Fungsi untuk melihat isi keranjang
    def view_cart(self, store):
        table = PrettyTable()
        table.field_names = ["ID Produk", "Nama Produk", "Jumlah", "Harga Satuan", "Total Harga"]
        for product_name, quantity in self.shopping_cart.items():
            product = next((p for p in store.products if p.name == product_name), None)
            if product:
                harga_satuan = product.price
                total_harga = harga_satuan * quantity
                table.add_row([product.id, product.name, quantity, harga_satuan, total_harga])
        print(table)

    # Fungsi untuk menghapus produk dari keranjang berdasarkan ID produk
    def remove_from_cart(self, store):
        self.view_cart(store)
        product_id = input("Masukkan ID produk yang ingin Anda hapus dari keranjang: ")
        product = next((p for p in store.products if p.id == product_id), None)
        if product:
            product_name = product.name
            if product_name in self.shopping_cart:
                quantity_in_cart = self.shopping_cart[product_name]
                while True:
                    quantity_to_remove = input(f"Masukkan jumlah (maksimum {quantity_in_cart}) yang ingin dihapus: ")
                    if quantity_to_remove.isdigit():
                        quantity_to_remove = int(quantity_to_remove)
                        if 1 <= quantity_to_remove <= quantity_in_cart:
                            self.shopping_cart[product_name] -= quantity_to_remove
                            if self.shopping_cart[product_name] == 0:
                                del self.shopping_cart[product_name]
                            
                            total_price_to_refund = product.price * quantity_to_remove
                            self.emoney += total_price_to_refund
                            print(f"{quantity_to_remove} {product_name} dihapus dari keranjang Anda.")
                            self.view_cart(store)
                            return
                        else:
                            print("Masukkan jumlah yang valid (tidak dapat melebihi jumlah maksimum di keranjang anda).")
                    else:
                        print("Masukkan jumlah yang valid.")
            else:
                print(f"{product_name} tidak ada dalam keranjang Anda.")
        else:
            print("Produk tidak ditemukan.")

    # Fungsi untuk menambahkan produk ke keranjang
    def add_to_cart(self, store):
        product_id = input("Masukkan ID produk yang ingin Anda beli: ")

        while True:
            quantity_input = input("Masukkan jumlah: ")
            if quantity_input.isdigit():
                quantity = int(quantity_input)
                if quantity >= 1: 
                    product = next((p for p in store.products if p.id == product_id), None)
                    if product:
                        product_name = product.name
                        total_price = product.price * quantity
                        if total_price <= self.emoney:
                            if product_name in self.shopping_cart:
                                self.shopping_cart[product_name] += quantity
                            else:
                                self.shopping_cart[product_name] = quantity
                            self.emoney -= total_price  
                            product.stock -= quantity 
                            store.view_products()
                            print(f"{quantity} {product_name} ditambahkan ke keranjang Anda.")
                            break
                        else:
                            print("Saldo E-Money tidak mencukupi untuk menambahkan produk ini ke keranjang.")
                            return
                    else:
                        print("Produk tidak ditemukan.")
                        return
                else:
                    print("jumlah Invalid, silahkan coba lagi.")
                    return
            else:
                print("Masukkan jumlah yang valid.")
                return

    # Fungsi untuk menyelesaikan pembelian
    def checkout(self, store):
        total_price = 0
        insufficient_stock = []  # List untuk melacak produk yang stoknya tidak mencukupi

        # Menghitung total harga pembelian
        for product_name, quantity in self.shopping_cart.items():
            product = next((p for p in store.products if p.name == product_name), None)
            if product:
                if quantity <= product.stock:
                    total_price += product.price * quantity
                else:
                    insufficient_stock.append(product_name)

        if insufficient_stock:
            print("Pembelian tidak dapat diselesaikan karena stok tidak mencukupi untuk produk berikut:")
            for product_name in insufficient_stock:
                print(f"{product_name}")
        else:
            if total_price > 0:
                # Melakukan pembayaran dan mengurangkan saldo E-Money
                self.emoney -= total_price
                print("Pembayaran berhasil.")
                print(f"Total harga: Rp{total_price}")
                print("Isi keranjang Anda:")
                self.view_cart(store)
                print("Terima kasih atas pembelian Anda!")
                self.shopping_cart = {}
                save_products(store.products)
            else:
                print("Keranjang Anda kosong.")


# Fungsi untuk menu pelanggan
def customer_menu(store, emoney):
    customer = Customer(emoney)
    while True:
        print("\nMenu Pelanggan:")
        print("1. Tambah ke keranjang")
        print("2. Lihat keranjang")
        print("3. Hapus dari keranjang")
        print("4. Checkout")
        print("5. keluar")
        choice = input("Masukkan pilihan Anda: ")

        if choice == '1':
            customer.view_products(store)
            customer.add_to_cart(store)
        elif choice == '2':
            customer.view_cart(store)
        elif choice == '3':
            customer.remove_from_cart(store)
        elif choice == '4':
            customer.checkout(store)
        elif choice == '5':
            print("Selamat tinggal!")
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

# Fungsi untuk menu admin
def admin_menu(store):
    while True:
        print("\nMenu Admin:")
        print("1. Lihat Produk")
        print("2. Tambah Produk")
        print("3. Hapus Produk")
        print("4. Perbarui Produk")
        print("5. Keluar")
        choice = input("Masukkan pilihan Anda: ")

        if choice == '1':
            store.view_products()
        elif choice == '2':
            while True:
                name = input("Masukkan nama produk: ")
                if name.isalpha():
                    break
                else:
                    print("Nama invalid. Silakan coba lagi.")

            while True:
                price_input = input("Masukkan harga produk: ")
                if price_input.isdigit() and int(price_input) >= 1:
                    price = int(price_input)
                    break
                else:
                    print("Harga invalid, silahkan coba lagi.")

            while True:
                stock_input = input("Masukkan stok produk: ")
                if stock_input.isdigit() and int(stock_input) >= 1:
                    stock = int(stock_input)
                    break
                else:
                    print("Stok invalid, silahkan coba lagi.")

            product_id = str(len(store.products) + 1)  # Buat ID produk baru
            product = Product(product_id, name, price, stock)
            store.add_product(product)
            save_products(store.products)
            print("Produk berhasil ditambahkan.")
        elif choice == '3':
            product_id = input("Masukkan ID produk yang akan dihapus: ")
            product = next((p for p in store.products if p.id == product_id), None)
            if product:
                store.products.remove(product)
                save_products(store.products)
                print("Produk berhasil dihapus.")
            else:
                print("Produk tidak ditemukan.")
        elif choice == '4':
            product_id = input("Masukkan ID produk yang akan diperbarui: ")
            product = next((p for p in store.products if p.id == product_id), None)
            if product:
                while True:
                    price_input = input("Masukkan harga produk baru: ")
                    if price_input.isdigit() and int(price_input) >= 1:
                        price = int(price_input)
                        break
                    else:
                        print("Harga invalid, silahkan coba lagi.")

                while True:
                    stock_input = input("Masukkan stok produk baru: ")
                    if stock_input.isdigit() and int(stock_input) >= 1:
                        stock = int(stock_input)
                        break
                    else:
                        print("Stok invalid, silahkan coba lagi.")

                product.price = price
                product.stock = stock
                save_products(store.products)
                print("Informasi produk diperbarui dengan berhasil.")
            else:
                print("Produk tidak ditemukan.")
        elif choice == '5':
            print("Keluar dari menu admin.")
            break
        else:
            print('Pilihan tidak valid.')




if __name__ == "__main__":
    store = Store()
    store.products = load_products()

    print('___________________________________')
    print('Selamat datang di program toko roti')
    print('___________________________________')

    while True:
        print('\nMenu:')
        print('1. Pelanggan')
        print('2. Admin')
        print('3. Keluar')

        choice = input('Pilih peran Anda: ')

        if choice == '1':
            print('__________________')
            print('Pilih aksi untuk Pelanggan:')
            print('1. Buat Akun')
            print('2. Login')
            action = input('Pilih aksi: ')

            if action == '1':
                create_account()
            elif action == '2':
                logged_in_user = login()
                if logged_in_user:
                    print('Selamat datang, ' + logged_in_user)
                    emoney = int(input("Masukkan saldo E-Money Anda: Rp"))
                    customer_menu(store, emoney)
                    break
            else:
                print('Pilihan tidak valid. Silakan coba lagi.')
        elif choice == '2':
            logged_in_user = login()
            if logged_in_user:
                print('Selamat datang, ' + logged_in_user)
                admin_menu(store)
        elif choice == '3':
            print("Terima kasih! Sampai jumpa lagi.")
            break
        else:
            print('Pilihan tidak valid.')
