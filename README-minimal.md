# Minimal versiya

Minimal versiya - bitta faylda

### Ishga tushirishdan oldin vaqtinchalik subdomen beradigan remote tunnel yaratish kerak va tunnel manzilini .env fayl yaratib qo'yib olishimiz kerak. Tunnel uchun vs code da tayyor [port forwarding](https://code.visualstudio.com/docs/debugtest/port-forwarding) funksiyasi bor

```
#.env

CALLBACK_URL=https://s8c4r16w-8000.euw.devtunnels.ms/
```

## Fayllar

- `minimal.py` - Asosiy dastur (server va client)
- `run_minimal.sh` - Test script

## Ishlatish

### 1. Dependencylarni o'rnatish (Package manager uchun uv ishlatilgan)
```bash
uv sync --frozen
```

### 4. Ishga tushirish
```bash
./run_minimal.sh "test message"
```
