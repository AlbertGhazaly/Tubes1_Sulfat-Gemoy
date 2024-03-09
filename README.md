
## Tubes 1 : IF2211 Strategi Algoritma
## Implementasi Algoritma Greedy dalam Permainan Diamonds by Etimo

Bot yang kami rancang merupakan implementasi dari "Algoritma Greedy by Biggest Weight Divided by Distance" yang merupakan modifikasi dari algoritma greedy yang awalnya berfokus pada jarak terpendek ke lokasi target. Dalam modifikasi ini, algoritma memprioritaskan diamond dengan bobot terbesar, dihitung dengan membagi skor diamond dengan hasil kali dari jarak bot ke diamond dengan akar dari jarak diamond ke base.


## Instalasi

### Persyaratan:

1. [Python](https://www.python.org/)
2. [Node.js](https://nodejs.org/en) 
3. [Docker desktop](https://www.docker.com/products/docker-desktop/)
4. [Yarn](https://classic.yarnpkg.com/lang/en/docs/install/#windows-stable)
5. [Game Engine](https://github.com/haziqam/tubes1-IF2211-game-engine/releases/tag/v1.1.0)

### Konfigurasi Game Engine

1. Ekstrak file game engine

2. Masuk ke root directory dari project 
```bash.
cd tubes1-IF2110-game-engine-1.1.0
```

3. Install dependencies menggunakan Yarn
```bash.
yarn
```

4. Setup default environment variable dengan menjalankan script berikut


```bash.
# Untuk Windows
./scripts/copy-env.bat

# Untuk Linux / (possibly) macOS
chmod +x ./scripts/copy-env.sh
./scripts/copy-env.sh
```

5. Setup local database (buka aplikasi docker desktop terlebih dahulu, lalu jalankan command berikut di terminal)

```bash.
docker compose up -d database
```

Lalu jalankan script berikut. 
```bash.
# Untuk Windows
./scripts/setup-db-prisma.bat


# Untuk Linux / (possibly) macOS
chmod +x ./scripts/setup-db-prisma.sh
./scripts/setup-db-prisma.sh
```

6. Build
```bash.
npm run build
```

7. Run
```bash.
npm run start
```

8. Buka http://localhost:8082/ pada web browser

Note: Langkah 1-6 hanya perlu dilakukan sekali, untuk selanjutnya cukup pastikan aplikasi Docker desktop sedang berjalan sebelum menjalankan langkah 7.

### Konfigurasi Bot

1. Clone github repository ini dan pindah ke root directory nya
```bash.
https://github.com/albert260302/botStima.git
cd botStima
```

2. Pastikan game engine sudah menyala

3. Jalankan perintah untuk menjalankan botStima

Untuk menjalankan satu bot
```bash.
python main.py --logic SulfatGemoy --email=SulfatGemoy@email.com --name=SulfatGemoy --password=123456 --team etimo --board 1
```

Untuk menjalankan banyak bot sekaligus
```bash.
# Untuk windows
./run-bots.bat

# Untuk Linux / (possibly) macOS
./run-bots.sh
```

## Authors

- [Ahmad Rafi Maliki 13522137](https://github.com/rafimaliki)
- [Nicholas Reymond Sihite 13522144](https://github.com/nicholasrs05)
- [Albert Ghazally](https://github.com/albert260302)

