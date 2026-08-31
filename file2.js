{
    const bukvj = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя";

    const tldnum = Math.floor(Math.random() * 2) + 2;

    const tld1 = bukvj[Math.floor(Math.random() * bukvj.length)];
    const tld2 = bukvj[Math.floor(Math.random() * bukvj.length)];
    const tld3 = bukvj[Math.floor(Math.random() * bukvj.length)];

    let tld = "";

    if (tldnum === 3) {
        tld = tld1 + tld2 + tld3;
    } else {
        tld = tld1 + tld2;
    }

    tld = "." + tld;

    let dominnum = Math.floor(Math.random() * 63) + 1;

    const protokol1 = [
        "https://",
        "http://",
        "ftp://",
        "",
        "sftp://"
    ];

    const protokol = protokol1[Math.floor(Math.random() * protokol1.length)];

    let domin = "";

    while (dominnum) {
        const dominbuk = bukvj[Math.floor(Math.random() * bukvj.length)];
        domin += dominbuk;
        dominnum--;
    }

    domin += tld;
    domin = protokol + domin;

    console.log(domin);

    const link = document.getElementById("domain333");

    link.href = domin;
    link.textContent = domin;
    link.style.color = "green";
}
