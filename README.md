# README.md (Minimal versiya uchun README-minimal.md faylga qarang)

## Tayyorlash va tushuntirish
### Avvaliga proyektni ko'proq sozlamalar bilan yozmoqchi edim (docker, postgres), reviewer (interviewer)ga barchasini ko'rsatish uchun, qila oladigan ishlarimni ko'rsatish maqsadida, lekin keyin shunchaki ishga tushadigan qilib davom ettirdim (minimal versiya README-minimal.md faylda)

### Ishga tushirishdan oldin vaqtinchalik subdomen beradigan remote tunnel yaratish kerak va tunnel manzilini .env fayl yaratib qo'yib olishimiz kerak. Tunnel uchun vs code da tayyor [port forwarding](https://code.visualstudio.com/docs/debugtest/port-forwarding) funksiyasi bor, public tunnel qilib ishga tushirish kerak

```
#.env

CALLBACK_URL=https://s8c4r16w-8000.euw.devtunnels.ms/
```

### Package manager uchun uv ishlatilgan

## Ishlatish
### Ishga tushirish

```
bash start.sh
```
