# dari folder website import function create_app
from website import create_app

app = create_app()

# jika file ini dijalankan, bukan file ini di import
if __name__ == '__main__':
    # maka akan menjalankan line di bawah
    # jika true maka ketika kita mengubah code pada file maka otomatis
    # menjalankan flask ulang
    app.run(debug=True)